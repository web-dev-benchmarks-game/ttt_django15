from django.conf.urls import patterns, url

from tictactoe import views

urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<game_id>\d+)/move/$', views.move, name='move'),
)
