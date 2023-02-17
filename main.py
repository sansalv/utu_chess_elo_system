import player
import game
import save_and_load as sl
import pandas as pd
import os
import random as rd

#_______________________________________________________________________
# Temporary test methods:

def generate_fakeplayers():
	players = []
	new_player_names = ["Onni Snåre", "Elias Ervelä", "Kimmo Pyyhtiä", "Santeri Salomaa", "Lauri Maila"]
	for name in new_player_names:
		new_player = player.newPlayer(name, 0)
		players.append(new_player)
	return players

def generate_fakegames():
	players = generate_fakeplayers()
	data1 = ["Santeri Salomaa", "Elias Ervelä", 1]
	data2 = ["Santeri Salomaa", "Kimmo Pyyhtiä", 1]
	data3 = ["Santeri Salomaa", "Onni Snåre", 0]
	data4 = ["Lauri Maila", "Santeri Salomaa", 0]
	data5 = ["Onni Snåre", "Elias Ervelä", 1]
	data = [data1, data2, data3, data4, data5]
	games = []
	games = game.games_to_games_instances(data)
	return games
#_______________________________________________________________________
# Tournament data input

# TODO: Comment and clean this. Then test and finish.
def input_tournament():
	date = input("Insert date of the tournament in yyyy-mm-dd:\n")

	# TODO: file location instead of filename
	filename = input("Insert filename of the tournament .csv-file:\n")

	"""
	Here input_tournament() handles tournament data. Creates games and players from test data.
	TODO: Combine with @Elias Ervelä code that handles tournament data
	TODO: Identify whether databases exist and choose between save_first_games() and save_new_games()
	"""
	
	# Load old players from database
	#players = sl.load_players()

	# Test:

	players = []
	# Create new players (test version)
	# TODO: check from sheets data, who are new players (not in "players" list), and create them (@Elias Ervelä)
	new_intermediate_player_names = ["Elias Ervelä", "Onni Snåre", "Kaisa Hakkarainen", "Kerttu Pusa"]
	new_experienced_player_names = ["Santeri Salomaa", "Kimmo Pyyhtiä", "Testi"]
	for name in new_intermediate_player_names:
		new_player = player.newPlayer(name, 1)
		players.append(new_player)
	for name in new_experienced_player_names:
		new_player = player.newPlayer(name, 2)
		players.append(new_player)

	# New games from a tournament data 
	# TODO: games from sheets data (@Elias Ervelä)
	data1 = ["Santeri Salomaa", "Elias Ervelä", 1]
	data2 = ["Santeri Salomaa", "Kimmo Pyyhtiä", 0]
	data3 = ["Onni Snåre", "Elias Ervelä", 1]
	data4 = ["Kimmo Pyyhtiä", "Onni Snåre", 0]
	data5 = ["Kerttu Pusa", "Santeri Salomaa", 0.5]
	data6 = ["Kaisa Hakkarainen", "Santeri Salomaa", 0]
	data = [data1, data2, data3, data4, data5, data6]
	# data = game.from_table_to_games_list(filename)
	games = game.games_to_games_instances(data)
	sl.save_first_games(games)

	for p in players:
		new_elo = p.calculate_new_elo_tournament(games)
		p.update_elo_and_history(date, new_elo)
	sl.save_players(players)

"""
	# Second tournament day
	date = "2023-02-16"

	players = []
	players = sl.load_players()

	data1 = ["Santeri Salomaa", "Elias Ervelä", 0.5]
	data2 = ["Santeri Salomaa", "Kimmo Pyyhtiä", 0]
	data = [data1, data2]
	new_games = game.games_to_games_instances(data)
	sl.save_new_games(new_games) # Extend games database

	for p in players:
		new_elo = p.calculate_new_elo_tournament(new_games)
		p.update_elo_and_history(date, new_elo)
	sl.save_players(players)

	for p in players:
		new_elo = p.calculate_new_elo_tournament(games)
		p.update_elo_and_history(date, new_elo)
	sl.save_players(players)
"""
#_____________________________________________________________________
# Data lookup

def data_query():
	os.system("cls")
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


#_______________________________________________________________________
#_______________________________________________________________________
	
def main():
	#TODO check if player- and gamedatabases exist -> relay that information to input_tournament()

	# 1: Input tournament data from a csv file
	# 2: Look up player specific data
	while True:
		os.system('cls')
		command = input("Input a command \n1: Input tournament data \n2: Look at a profile \n")
		os.system('cls')
		match command:
			case "1":
				input_tournament()
			case "2":
				data_query()
			case "":
				exit()
			case _:
				print("Incorrect command")


if __name__ == "__main__":
    main()