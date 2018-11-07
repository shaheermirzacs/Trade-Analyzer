from __future__ import print_function
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
from Player import Player
import pandas
import os

def search(name, output_help):
    player = None

    player_list = players.find_players_by_full_name(name)

    if len(player_list) != 1:
        if output_help:
            for p in player_list:
                print('  {0}'.format(p['full_name']))
    else:
        player = Player(player_list[0])
    
    return player

def search_player():
    player = None

    while player == None:
        name = raw_input('Choose a player: ')

        player = search(name, True)

    player.print_stats(with_header=True)
    print()

def list_contains_player(players, name):
    for player in players:
        if player.last_name.lower() == name.lower() or player.first_name.lower() == name.lower() or player.full_name.lower() == name.lower():
            return True
    
    return False

def parse_proposal(proposal):
    user_players = []
    opponent_players = []
    for_found = False
    used_next = False
    proposition = proposal.split()

    for index, name in enumerate(proposition):
        player_name = name

        if name == "for":
            for_found = True
            continue

        if not for_found:
            if list_contains_player(user_players, player_name) or used_next:
                used_next = False
                continue

            player = None

            player = search(player_name, False)

            if player == None:
                if (index < len(proposition) - 1):
                    player_name += ' ' + proposition[index + 1]
                    player = search(player_name, True)
                    used_next = True

                if player == None:
                    print('Please specify who you mean by {0}'.format(name))
                    break

            if player != None:
                user_players.append(player)

        elif for_found:
            if list_contains_player(opponent_players, player_name) or used_next:
                used_next = False
                continue

            player = None

            player = search(player_name, False)

            if player == None:
                if (index < len(proposition) - 1):
                    player_name += ' ' + proposition[index + 1]
                    player = search(player_name, True)
                    used_next = True

                if player == None:
                    print('Please specify who you mean by {0}'.format(name))
                    break

            if player != None:
                opponent_players.append(player)

    proposal = [user_players, opponent_players]
    return proposal

def calculate_trade_difference(proposition):
    user_players = proposition[0]
    opponent_players = proposition[1]

    diff_MIN = 0
    diff_FG3M = 0
    diff_REB = 0
    diff_AST = 0
    diff_STL = 0
    diff_BLK = 0
    diff_PTS = 0


    for player in user_players:
        diff_MIN -= player.MIN
        diff_FG3M -= player.F3PM
        diff_REB -= player.REB
        diff_AST -= player.AST
        diff_STL -= player.STL
        diff_BLK -= player.BLK
        diff_PTS -= player.PTS

    for player in opponent_players:
        diff_MIN += player.MIN
        diff_FG3M += player.F3PM
        diff_REB += player.REB
        diff_AST += player.AST
        diff_STL += player.STL
        diff_BLK += player.BLK
        diff_PTS += player.PTS

    differences = [diff_MIN, diff_FG3M, diff_REB, diff_AST, diff_STL, diff_BLK, diff_PTS]

    return differences

def analyze_trade():
    proposal = raw_input('What\'s the proposal? ')

    if proposal == 'nvm':
        return

    proposition = parse_proposal(proposal)

    display_teams(proposition)

    differences = calculate_trade_difference(proposition)
    
    print('{message:<{max_length}}'.format(message='Difference', max_length=buffer_length(proposition)), end='\t')

    loss_count = 0
    win_count = 0

    for diff in differences:
        if diff < 0:
            loss_count += 1
        else:
            win_count += 1

        print('{0}\t'.format(diff), end='')

    print()
    print('Gains: {0}\nLosses {1}'.format(win_count, loss_count))


def setup_team():
    num_players = 15
    team = []

    player_to_search = raw_input('Enter a player: ')

    while len(team) < num_players and player_to_search.lower() != 'done':
        player = search(player_to_search, True)

        if player != None:
            team.append(player)
            print('Added {0}'.format(player.full_name))

        print('num players: {0}'.format(len(team)))

        if (len(team) == 15):
            break

        player_to_search = raw_input('Enter a player: ')

    for player in team:
        player.print_stats()

def buffer_length(teams):
    max_length = 0
    
    for team in teams:
        for player in team:
            if len(player.full_name) > max_length:
                max_length = len(player.full_name)

    return max_length

def display_teams(teams, with_header=False):
    header = ''

    for i in range(buffer_length(teams)):
        header += ' '

    header += '\tMIN\t3PM\tREB\tAST\tSTL\tBLK\tPTS'
    print(header)

    for team in teams:
        for player in team:
            player.print_stats()
        print()
    print()



    


def main():
    while True:
        choice = raw_input('''\nWhat would you like to do?
        1) Find a player
        2) Analyze a trade
        3) Setup team
        4) Edit team
        5) Make a trade
        6) Add other teams
        7) Quit\n''')

        os.system('clear')

        if choice == '1':
            search_player()
        elif choice == '2':
            analyze_trade()
        elif choice == '3':
            setup_team()
        elif choice == '7':
            exit()


if __name__ == '__main__':
    main()
