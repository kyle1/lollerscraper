import pandas as pd
import requests
from pyquery import PyQuery as pq


class Team:
    def __init__(self, tr):
        self._lol_team_id = None
        self._team_name = None

        self._parse_team(tr)

    def _parse_team(self, tr):
        for td in tr('td').items():
            for a in td('a').items():
                team_id = a.attr['href'].split('/')[2]
            team_name = td.text()
            break

        setattr(self, '_lol_team_id', team_id)
        setattr(self, '_team_name', team_name)

    @property
    def dataframe(self):
        fields_to_include = {
            'LolTeamId': self._lol_team_id,
            'TeamName': self._team_name
        }
        return pd.DataFrame([fields_to_include], index=[self._lol_team_id])

    @property
    def to_dict(self):
        dataframe = self.dataframe
        dic = dataframe.to_dict('records')[0]
        return dic


class Teams:
    def __init__(self):
        self._teams = []

        self._get_teams()

    def __repr__(self):
        return self._teams

    def __iter__(self):
        return iter(self.__repr__())

    def _get_teams(self):
        url = 'https://gol.gg/teams/list/season-S10/split-Spring/region-ALL/tournament-ALL/week-ALL/'
        teams_html = pq(url, verify=False)
        for table in teams_html('table').items():
            if 'playerslist' in table.attr['class']:  # not a typo
                teams_list = table

        first_tr = True
        for tr in teams_list('tr').items():
            if first_tr:
                first_tr = False  # Skip the header row
                continue
            team = Team(tr)
            self._teams.append(team)

    @property
    def dataframes(self):
        frames = []
        for team in self.__iter__():
            frames.append(team.dataframe)
        return pd.concat(frames)

    @property
    def to_dicts(self):
        dics = []
        for team in self.__iter__():
            dics.append(team.to_dict)
        return dics
