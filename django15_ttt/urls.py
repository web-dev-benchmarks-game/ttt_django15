from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'django15_ttt.views.home', name='home'),
    # url(r'^django15_ttt/', include('django15_ttt.foo.urls')),
    url(r'^tictactoe/', include('tictactoe.urls', namespace='tictactoe')),
    url(r'^user/', include('django.contrib.auth.urls', namespace='user')),
    url('^$', RedirectView.as_view(url='tictactoe/')),


    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
