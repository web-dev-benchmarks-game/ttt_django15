This is the Django implementation of the Tic-Tac-Toe benchmark.

It was created using ``django-admin startproject django15_ttt``.

To use
======

Setting up::

    $ emacs settings.py
    # Change DB settings, in particular the sqlite3 path, if needed
    $ python manage.py syncdb
    # you might want to create a superuser, just follow the prompts

Running::

    $ python manage.py runserver
