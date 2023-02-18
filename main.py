import player
import game
import save_and_load as sl
import pandas as pd
#import os
from os import system
import random as rd
#_______________________________________________________________________
# Tournament data input. Creates games and players from csv data and updated databases.

# TODO: Comment the end section of this
def input_tournament():
	
	# Input tournament date and file location
	date = input("Insert date of the tournament in yyyy-mm-dd:\n")
	file_location = input("Insert file location (path) of the tournament .csv-file:\n")

	# Load old players from database
	players = sl.load_players()
	#___________________________________
	# Check and create new players:

	# Creates lists of player names from database and list of names from csv table
	old_players_names = [p.get_name() for p in players]
	table_names = player.get_players_from_table(file_location)

	# Check if new players
	if not all(p in old_players_names for p in table_names):
		# New players found. Creates list of new names and prints
		new_player_names = []
		print("\nNew players found:")
		for name in table_names:
			if name not in old_players_names:
				new_player_names.append(name)
				print(name)
		# Also, creates new Player instances and appends to players
		level = int(input("\nWhat is the starting level of these players?\n(0 = 500 Elo, 1 = 1000 Elo, 2 = 1500 Elo)\n"))
		for name in new_player_names:
			new_player = player.newPlayer(name, level)
			players.append(new_player)
	#___________________________________

	# TODO: Comment these rest
	raw_game_list = game.from_table_to_games_list(file_location)
	games = game.game_lists_to_game_instances(date, raw_game_list, players)
	sl.save_new_games(games)
	print("Saved games to game_database.json successfully.")

	for p in players:
		new_elo = p.calculate_new_elo_tournament(games)
		p.update_elo_and_history(date, new_elo)
	sl.save_players(players)
	print("Updated players to players_database.json successfully.")

#_____________________________________________________________________
# Data lookup
# TODO: Comment and document

def data_query():
	#os.system("cls")
	x = input("Input the name of the player you wish to look up or press enter to go back: ")
	if x == "":
		return
	players = []
	players = sl.load_players()
	found = False
	for p in players:
		if p.get_name() == x:
			found = True
			print_player_games(p)
			break
	if found == False:
		input("No player with that name")
	data_query()
	return

def print_player_games(x):
	games = []
	games = sl.load_games()
	x.print_player()
	found = False
	for peli in games:
		if (peli.get_white_name() == x.get_name() or peli.get_black_name() == x.get_name()):
			found = True
			peli.print_game(x.get_name())
	if found == False:
		print("No games found")
	input()

#_____________________________________________________________________
# Print Elo leaderboard
# TODO: Comment and document

def print_elo_leaderboard():
	players = sl.load_players()
	players = sorted(players, key=lambda h: h.get_elo(), reverse=True)
	i = 1
	#Linux:
	#system('clear')
	#Windows:
	#os.system('cls')
	# TODO: print("TYLO rating leaderboard (last update: DATE):\n")
	print("TYLO rating leaderboard:\n")
	for p in players:
		print(f"{i}: {p.get_elo()}, {p.get_name()}")
		i += 1
	input()
#_______________________________________________________________________
#_______________________________________________________________________
	
def main():
	#TODO: Comment and document

	# 1: Input tournament data from a csv file
	# 2: Look up player specific data
	# 3: Print Elo leaderboard

	while True:
		# System clears are commented out because different commands work for Linux and Windows
		#TODO: If-else or something that checks if the computer is Linux or Windows
		#Linux:
		#system('clear')
		#Windows:
		#os.system('cls')
		command = input("\nInput a command \n1: Input tournament data \n2: Look at a profile \n3: Print TYLO leaderboard \n")
		#Linux:
		system('clear')
		#Windows:
		#os.system('cls')
		match command:
			case "1":
				input_tournament()
			case "2":
				data_query()
			case "3":
				print_elo_leaderboard()
			case "":
				exit()
			case _:
				print("Incorrect command")

if __name__ == "__main__":
    main()