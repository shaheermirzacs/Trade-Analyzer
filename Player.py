from __future__ import print_function
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
import pandas

class Player(object):
    def __init__(self, player):
        id = player['id']
        name = player['full_name']
        player_stats = playercareerstats.PlayerCareerStats(player_id=id, per_mode36='PerGame')

        data_frame = player_stats.get_data_frames()[0]

        self.full_name = player['full_name']
        self.last_name = player['last_name']
        self.first_name = player['first_name']
        self.MIN = data_frame['MIN'].iloc[-1]
        self.FGP = data_frame['FG_PCT'].iloc[-1]
        self.FTP = data_frame['FT_PCT'].iloc[-1]
        self.F3PM = data_frame['FG3M'].iloc[-1]
        self.REB = data_frame['REB'].iloc[-1]
        self.AST = data_frame['AST'].iloc[-1]
        self.STL = data_frame['STL'].iloc[-1]
        self.BLK = data_frame['BLK'].iloc[-1]
        self.PTS = data_frame['PTS'].iloc[-1]

    def print_stats(self, with_header=False, name_buffer=0):
        header = ''

        if with_header == True:
            for i in range(len(self.full_name)):
                header += ' '

            header += '\tMIN\t3PM\tREB\tAST\tSTL\tBLK\tPTS'
            print(header)

        print('{0}\t'.format(self.full_name), end='')
        print('{message:<{max_length}}'.format(message=self.full_name, max_length=name_buffer), end='\t')

        print('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}'.format(
            self.MIN, self.F3PM, self.REB, self.AST, self.STL, self.BLK, self.PTS,
        ))