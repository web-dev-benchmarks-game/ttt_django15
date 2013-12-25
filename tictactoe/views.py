from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.views import generic

from tictactoe.models import TicTacToeGame

class IndexView(generic.ListView):
    template_name = 'tictactoe/index.html'
    context_object_name = 'latest_game_list'

    def get_queryset(self):
        return TicTacToeGame.objects.order_by('-updated')[:5]

class DetailView(generic.DetailView):
    model = TicTacToeGame
    template_name = 'tictactoe/detail.html'
    context_object_name = 'game'

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
