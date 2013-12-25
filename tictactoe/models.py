from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TicTacToeSpace(models.Model):
    x = models.SmallIntegerField()
    y = models.SmallIntegerField()
    value = models.CharField(max_length=3)   # expecting just "x" and "o"
    game = models.ForeignKey('TicTacToeGame', related_name='spaces')

    def __str__(self):
        return "({0}, {1}): {2}".format(self.x, self.y, self.value)

PLAYER_X = 1
PLAYER_Y = 2
SYMBOL_X = 'X'
SYMBOL_Y = 'O'
class TicTacToeGame(models.Model):
    next_player = models.SmallIntegerField(default=1) # expecting just 1 and 2
    player_1 = models.ForeignKey(User, related_name='+')
    player_2 = models.ForeignKey(User, related_name='+')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class InvalidMove(Exception):
        pass

    def __unicode__(self):
        status = self.status()
        return "{} between {} ({}) and {} ({}) ({})".format(
            self.id, self.player_1, SYMBOL_X, self.player_2, SYMBOL_Y,
            status)

    def status(self):
        """Return a human-readable status for a game."""
        if self.is_over():
            if self.is_tied():
                status = 'over: tied'
            else:
                status = 'won by {}'.format(self.winner())
        else:
            status = '{} ({}) to move'.format(self.get_next_player(),
                                              self.next_player_symbol())
        return status

    def board(self):
        board = [[None, None, None], [None, None, None], [None, None, None]]
        spaces = self.spaces.all()
        for s in spaces:
            board[s.y][s.x] = s
        for y, row in enumerate(board):
            for x, cell in enumerate(row):
                if not cell:
                    row[x] = TicTacToeSpace(x=x, y=y)

        return board

    def get_next_player(self):
        if self.next_player == PLAYER_X:
            return self.player_1
        return self.player_2

    def next_player_symbol(self):
        if self.next_player == PLAYER_X:
            return SYMBOL_X
        return SYMBOL_Y

    def move(self, user, x, y):
        assert self.get_next_player() == user
        if self.is_over():
            raise self.InvalidMove("This game is already over.")
        if self.spaces.filter(x=x, y=y):
            raise self.InvalidMove("This space is already full.")
        self.spaces.create(x=x, y=y, value=self.next_player_symbol())
        if self.next_player == PLAYER_X:
            self.next_player = PLAYER_Y
        else:
            self.next_player = PLAYER_X

    def symbol_to_player(self, symbol):
        if symbol == SYMBOL_X:
            return self.player_1
        if symbol == SYMBOL_Y:
            return self.player_2
        raise ValueError(
            "symbol {} does not correspond to either player".format(
                symbol))

    class TiedGame(object):
        """Singleton to indicate that a game is tied."""

    def winner(self):
        """Return the player that won, or TiedGame, or None."""
        board = self.board()
        def cells_have_same_player(c1, c2, c3):
            return c1.value and c1.value == c2.value == c3.value

        def check_winner(c1, c2, c3):
            if cells_have_same_player(c1, c2, c3):
                return self.symbol_to_player(c1.value)
            return None

        winner = None
        for row in board:
            winner = winner or check_winner(*row)

        for i in range(len(board[0])):
            winner = winner or check_winner(board[0][i], board[1][i], board[2][i])

        winner = winner or check_winner(board[0][0], board[1][1], board[2][2])
        winner = winner or check_winner(board[0][2], board[1][1], board[2][0])
        if winner:
            return winner

        for row in board:
            for cell in row:
                if not cell.value:
                    # Empty space -- the game can continue
                    return None

        return self.TiedGame

    def is_over(self):
        return bool(self.winner())

    def is_tied(self):
        return self.winner() == self.TiedGame
