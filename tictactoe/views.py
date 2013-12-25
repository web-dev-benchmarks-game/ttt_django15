from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from tictactoe.models import TicTacToeGame

def index(request):
    latest_game_list = TicTacToeGame.objects.order_by('-updated')[:5]
    return render(request, 'tictactoe/index.html', {
        'latest_game_list': latest_game_list,
    })

def detail(request, game_id):
    game = get_object_or_404(TicTacToeGame, pk=game_id)
    return render(request, 'tictactoe/detail.html', {'game': game})

def move(request, game_id):
    game = get_object_or_404(TicTacToeGame, pk=game_id)
    try:
        x, y = request.POST['space'].split(',')
        game.move(request.user, x, y)
    except TicTacToeGame.InvalidMove as e:
        return render(request, 'tictactoe/detail.html', {
            'game': game,
            'error_message': str(e),
        })

    game.save()
    return HttpResponseRedirect(reverse('tictactoe:detail', args=(game.id,)))
