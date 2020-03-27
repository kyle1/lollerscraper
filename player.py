import pandas as pd
import requests
from pyquery import PyQuery as pq


class Player:
    def __init__(self, keys, tr):
        self._lol_player_id = None
        self._player = None
        self._lol_team_id = None
        self._position = None

        self._parse_player(keys, tr)

    def _parse_player(self, keys, tr):
        values = []

        first_td = True
        for td in tr('td').items():
            if first_td:
                for a in td('a').items():
                    link = a.attr['href']
                    break
                first_td = False
            values.append(td.text())
        player_id = link.split('/')[2]

        index = 0
        player = {}
        for key in keys:
            player[key] = values[index]
            index += 1

        setattr(self, '_lol_player_id', player_id)
        setattr(self, '_player', player['Player'])
        setattr(self, '_position', player['Position'])

    @property
    def dataframe(self):
        fields_to_include = {
            'LolPlayerId': self._lol_player_id,
            'Player': self._player,
            'Position': self._position
        }
        return pd.DataFrame([fields_to_include], index=[self._lol_player_id])

    @property
    def to_dict(self):
        dataframe = self.dataframe
        dic = dataframe.to_dict('records')[0]
        return dic


class Players:
    """
    LOL players.

    Parameters
    ----------
    None
    """

    def __init__(self):
        self._players = []

        self._get_players()

    def __repr__(self):
        return self._players

    def __iter__(self):
        return iter(self.__repr__())

    def _get_players(self):
        url = 'https://gol.gg/players/list/season-ALL/split-ALL/tournament-ALL/position-ALL/week-ALL/'
        players_html = pq(url, verify=False)
        for table in players_html('table').items():
            if 'playerslist' in table.attr['class']:
                players_list = table
                break

        keys = []
        for th in players_list('th').items():
            keys.append(th.text())

        first_row = True

        for tr in players_list('tr').items():
            if first_row:
                first_row = False
                continue

            player = Player(keys, tr)
            self._players.append(player)

    @property
    def dataframes(self):
        frames = []
        for player in self.__iter__():
            frames.append(player.dataframe)
        return pd.concat(frames)

    @property
    def to_dicts(self):
        dics = []
        for player in self.__iter__():
            dics.append(player.to_dict)
        return dics


#players = Players()
# print(players.dataframes)
