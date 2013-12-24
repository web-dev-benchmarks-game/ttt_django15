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

class TicTacToeGame(models.Model):
    next_player = models.SmallIntegerField() # expecting just 1 and 2
    player_1 = models.ForeignKey(User, related_name='+')
    player_2 = models.ForeignKey(User, related_name='+')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def board(self):
        board = [[None, None, None], [None, None, None], [None, None, None]]
        spaces = self.spaces.all()
        for s in spaces:
            board[s.y][s.x] = s.value

        return board
