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
class TicTacToeGame(models.Model):
    next_player = models.SmallIntegerField(default=1) # expecting just 1 and 2
    player_1 = models.ForeignKey(User, related_name='+')
    player_2 = models.ForeignKey(User, related_name='+')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class InvalidMove(Exception):
        pass

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
            return 'X'
        return 'O'

    def move(self, user, x, y):
        assert self.get_next_player() == user
        if self.spaces.filter(x=x, y=y):
            raise self.InvalidMove("This space is already full.")
        self.spaces.create(x=x, y=y, value=self.next_player_symbol())
        if self.next_player == PLAYER_X:
            self.next_player = PLAYER_Y
        else:
            self.next_player = PLAYER_X

    def is_over(self):
        return True

    def winner(self):
        pass
