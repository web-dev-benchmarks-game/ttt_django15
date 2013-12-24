from django.http import HttpResponse
from django.shortcuts import render
from tictactoe.models import TicTacToeGame

def index(request):
    latest_game_list = TicTacToeGame.objects.order_by('-updated')[:5]
    return render(request, 'tictactoe/index.html', {
        'latest_game_list': latest_game_list,
    })

def detail(request, game_id):
    return HttpResponse("You're looking at game {}.".format(game_id))

def move(request, game_id):
    return HttpResponse("You're making a move on game {}.".format(game_id))
