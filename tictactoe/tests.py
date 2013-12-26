"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from tictactoe.models import TicTacToeGame as Game, TicTacToeSpace as Space
from django.contrib.auth.models import User

class TicTacToeBase(TestCase):
    def setUp(self):
        self.player_1 = User.objects.create(username='player_1')
        self.player_2 = User.objects.create(username='player_2')

class TicTacToeTest(TicTacToeBase):
    def test_basic_game_starts_not_over(self):
        """filling in the first row means game over"""
        game = Game(player_1=self.player_1,
                    player_2=self.player_2)
        self.failIf(game.is_over())

    def test_basic_game_over_has_winner(self):
        """filling in the first row means game over"""
        game = Game.objects.create(player_1=self.player_1,
                                   player_2=self.player_2)
        game.move(self.player_1, x=0, y=0)
        game.move(self.player_2, x=0, y=1)
        game.move(self.player_1, x=1, y=0)
        game.move(self.player_2, x=1, y=1)
        game.move(self.player_1, x=2, y=0)
        self.assert_(game.is_over())
        self.assertEqual(game.winner(), self.player_1)

    def test_detect_ties(self):
        game = Game.objects.create(player_1=self.player_1,
                                   player_2=self.player_2)
        # A complicated match
        game.move(self.player_1, x=0, y=0)
        game.move(self.player_2, x=0, y=1)
        # X - -
        # O - -
        # - - -

        game.move(self.player_1, x=1, y=0)
        game.move(self.player_2, x=2, y=0)
        # X X O
        # O - -
        # - - -

        game.move(self.player_1, x=1, y=1)
        game.move(self.player_2, x=2, y=2)
        # X X O
        # O X -
        # - - O

        game.move(self.player_1, x=2, y=1)
        game.move(self.player_2, x=1, y=2)
        # X X O
        # O X X
        # X O O

        game.move(self.player_1, x=0, y=2)

        self.assert_(game.is_over())
        self.assert_(game.is_tied())

class TicTacToeManagerTest(TicTacToeBase):
    def test_for_player_1(self):
        game = Game.objects.create(player_1=self.player_1, player_2=self.player_2)
        self.assertEqual(list(Game.objects.for_user(self.player_1)),
                         [game])

    def test_for_player_2(self):
        game = Game.objects.create(player_1=self.player_1, player_2=self.player_2)
        self.assertEqual(list(Game.objects.for_user(self.player_2)),
                         [game])

    def test_user_to_play_player_1(self):
        game = Game.objects.create(player_1=self.player_1, player_2=self.player_2,
                                   next_player=1)
        self.assertEqual(list(Game.objects.user_to_play(self.player_1)),
                         [game])
        self.assertEqual(list(Game.objects.user_to_play(self.player_2)),
                         [])

    def test_user_to_play_player_1(self):
        game = Game.objects.create(player_1=self.player_1, player_2=self.player_2,
                                   next_player=2)
        self.assertEqual(list(Game.objects.user_to_play(self.player_2)),
                         [game])
        self.assertEqual(list(Game.objects.user_to_play(self.player_1)),
                         [])
