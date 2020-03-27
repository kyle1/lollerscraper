import requests
from game import Game, PlayerBoxscores
from player import Players
from team import Teams

BASE_URL = 'https://localhost:44374/api/'


# teams = Teams()
# response = requests.post(url=BASE_URL + 'lol/teams', json=teams.to_dicts, verify=False).json()
# print(response)

players = Players()
response = requests.post(url=BASE_URL + 'lol/players', json=players.to_dicts, verify=False).json()
print(response)

# game = Game(22596)
# print(game.dataframe)
# print(game.to_dict)

#pb = PlayerBoxscores(22596)
