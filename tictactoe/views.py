from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the tictactoe index.")

def detail(request, game_id):
    return HttpResponse("You're looking at game {}.".format(game_id))

def move(request, game_id):
    return HttpResponse("You're making a move on game {}.".format(game_id))
