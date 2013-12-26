This is the Django implementation of the Tic-Tac-Toe benchmark.

It was created using ``django-admin startproject django15_ttt``.

To use
======

Setting up::

    # Install a dependency
    $ pip install --user django-model-utils

    $ emacs settings.py
    # Change DB settings, in particular the sqlite3 path, if needed
    $ python manage.py syncdb
    # you might want to create a superuser, just follow the prompts

Running::

    $ python manage.py runserver

FIXMEs
======

The contortions we have to go through in order to define a new query
method are kind of extensive. I followed the recipe from
http://dabapps.com/blog/higher-level-query-api-django-orm/. This seems
like it gets better in newer versions of Django, but I can't swear to
it.

We do some slightly ugly stuff to render the list of available users
in the create game page. There's probably a better way involving
implementing a custom widget or something.

The field called next_player should probably be called player_turn,
and next_player should probably be a property that returns the User
object of the player corresponding to player_turn.
