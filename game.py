import pandas as pd
import requests
from pyquery import PyQuery as pq


class PlayerBoxscore:
    def __init__(self, tr):
        self._player_name = None
        self._player_role = None
        self._kills = None
        self._deaths = None
        self._assists = None
        self._kda = None
        self._cs = None
        self._gold = None
        self._gold_per_minute = None
        self._total_dmg_to_champion = None

        self._parse_player(tr)

    def _parse_player(self, tr):
        print(tr)


class PlayerBoxscores:
    def __init__(self, game_id):
        self._boxscores = []

        self._get_player_boxscores(game_id)

    def _get_player_boxscores(self, game_id):
        url = f'https://gol.gg/game/stats/{game_id}/page-fullstats/'
        boxscores_html = pq(url, verify=False)
        for table in boxscores_html('table').items():
            keys = ['Champion']
            value_lists = []
            row_index = 0
            for tr in table('tr').items():
                value_list = []
                # First row is the played champion
                if row_index == 0:
                    for th in tr('th').items():
                        for img in th('img').items():
                            value_list.append(img.attr['alt'])
                            break
                    value_lists.append(value_list)
                    row_index += 1
                    continue

                first_td = True
                for td in tr('td').items():
                    if first_td:
                        keys.append(td.text())
                        first_td = False
                    else:
                        value_list.append(td.text())
                value_lists.append(value_list)
                row_index += 1
            break

        #players = []
        for i in range(10):
            player = {}
            for j in range(len(keys)):
                player[keys[j]] = value_lists[j][i]
            self._boxscores.append(player)

        # for p in players:
        #     print(p)
        #     print('\n')

    @property
    def to_dict(self):
        return self._boxscores


class Game:
    def __init__(self, game_id):
        self._lol_game_id = None
        self._game_length = None
        self._blue_team_id = None
        self._blue_team_win = None
        self._blue_kills = None
        self._blue_towers = None
        self._blue_dragons = None
        self._blue_barons = None
        self._blue_gold = None
        self._red_team_id = None
        self._red_kills = None
        self._red_towers = None
        self._red_dragons = None
        self._red_barons = None
        self._red_gold = None
        self._players = None

        self._blue_top_gold_pct = None
        self._blue_jungle_gold_pct = None
        self._blue_mid_gold_pct = None
        self._blue_adc_gold_pct = None
        self._blue_support_gold_pct = None
        self._blue_top_dmg_pct = None
        self._blue_jungle_dmg_pct = None
        self._blue_mid_dmg_pct = None
        self._blue_adc_dmg_pct = None
        self._blue_support_dmg_pct = None

        self._get_game(game_id)

    def _get_game(self, game_id):
        url = f'https://gol.gg/game/stats/{game_id}/page-game/'
        game_html = pq(url, verify=False)

        setattr(self, '_lol_game_id', game_id)

        first_h1 = False
        for h1 in game_html('h1').items():
            if first_h1:
                first_h1 = False
                continue
            setattr(self, '_game_length', h1.text())

        for div in game_html('div').items():
            div_class = div.attr['class']

            if div_class and 'blue-line-header' in div_class:
                for a in div('a').items():
                    blue_team_id = a.attr['href'].split('/')[3]
                    setattr(self, '_blue_team_id', blue_team_id)
                    break
                blue_team_win = False
                if 'WIN' in div.text():
                    blue_team_win = True
                setattr(self, '_blue_team_win', blue_team_win)

            if div_class and 'red-line-header' in div_class:
                for a in div('a').items():
                    red_team_id = a.attr['href'].split('/')[3]
                    setattr(self, '_red_team_id', red_team_id)
                    break
                red_team_win = False
                if 'WIN' in div.text():
                    red_team_win = True
                setattr(self, '_red_team_win', red_team_win)

        blue_spans = []
        for span in game_html('span').items():
            # print(span.text())
            if span.attr['class'] == 'score-box blue_line':
                for img in span('img').items():
                    if img.attr['alt'] == 'Kills':
                        setattr(self, '_blue_kills', span.text())
                    if img.attr['alt'] == 'Towers':
                        setattr(self, '_blue_towers', span.text())
                    if img.attr['alt'] == 'Dragons':
                        setattr(self, '_blue_dragons', span.text())
                    if img.attr['alt'] == 'Nashor':
                        setattr(self, '_blue_barons', span.text())
                    if img.attr['alt'] == 'Team Gold':
                        setattr(self, '_blue_gold', span.text())
            if span.attr['class'] == 'score-box red_line':
                for img in span('img').items():
                    if img.attr['alt'] == 'Kills':
                        setattr(self, '_red_kills', span.text())
                    if img.attr['alt'] == 'Towers':
                        setattr(self, '_red_towers', span.text())
                    if img.attr['alt'] == 'Dragons':
                        setattr(self, '_red_dragons', span.text())
                    if img.attr['alt'] == 'Nashor':
                        setattr(self, '_red_barons', span.text())
                    if img.attr['alt'] == 'Team Gold':
                        setattr(self, '_red_gold', span.text())

        setattr(self, '_players', PlayerBoxscores(game_id))

    @property
    def dataframe(self):
        fields_to_include = {
            'LolGameId': self._lol_game_id,
            'GameLength': self._game_length,
            'BlueTeamId': self._blue_team_id,
            'BlueTeamWin': self._blue_team_win,
            'BlueKills': self._blue_kills,
            'BlueTowers': self._blue_towers,
            'BlueDragons': self._blue_dragons,
            'BlueBarons': self._blue_barons,
            'BlueGold': self._blue_gold,
            'RedTeamId': self._red_team_id,
            'RedTeamWin': self._red_team_win,
            'RedKills': self._red_kills,
            'RedTowers': self._red_towers,
            'RedDragons': self._red_dragons,
            'RedBarons': self._red_barons,
            'RedGold': self._red_gold
        }
        return pd.DataFrame([fields_to_include], index=[self._lol_game_id])

    @property
    def to_dict(self):
        dataframe = self.dataframe
        dic = dataframe.to_dict('records')[0]
        dic['Players'] = self._players.to_dict
        return dic
