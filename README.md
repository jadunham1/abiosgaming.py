# abiosgaming.py
Python Library to interact with the abiosgaming.com API

You can instantiate a client in two ways.

from abiosgaming.client import AbiosClient
client = AbiosClient(username='user', password='pass')

-- or if you have an access token already you can instantiate a client with it

client = AbiosClient(access_token='access_token')

The client handles AbiosGaming APIs paginated calls you just have to specify how many items you want.
Number of items fetched by default are 3, each API call has a count parameter where you can specify many you want back.

Examples:

# get 3 upcoming matches
list_of_game_objects = client.get_upcoming_games()

# get 16 upcoming matches for DOTA 2
list_of_dota2_game_objects = client.get_upcoming_games(count=16, games=['1'])

# get current matches for CS:GO
list_of_current_dota2_game_objects = client.get_current_matches(games=['2'])

These are just some examples.
Readthedocs for more.
