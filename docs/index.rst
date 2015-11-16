abiosgaming-api
===============

Release v\ |version|.

abiosgaming-api is python library for interacting with the abiosgaming API
`AbiosGaming API`_

Example
-------

Using the client to get matches::

    from abiosgaming.client import AbiosClient

    client = AbiosClient()

    games = client.get_games()
    matches = client.get_matches()
    tournaments = client.get_tournaments()
    competitors = client.get_competitors()

More Examples
~~~~~~~~~~~~~

.. toctree::
    :maxdepth: 2

.. links

.. _AbiosGaming API: http://api.abiosgaming.com

Modules
-------

.. toctree::
    :maxdepth: 1

    utils

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

