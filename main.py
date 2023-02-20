import player
import game
import save_and_load as sl
#import pandas as pd
import os # For clearing terminal



#_______________________________________________________________________
# Tournament data input. Creates games and players from csv data and updated databases.

# TODO: Comment the end section of this
def input_tournament():
	
	# Input tournament date and file location
	date = input("Insert date of the tournament in yyyy-mm-dd:\n")
	file_location = input("Insert file location (path) of the tournament .csv-file:\n")

	# Load old players from database
	all_players = sl.load_players() # After this old players but later also new players will be appended
	
	#___________________________________
	# Check and create new players:

	# Creates lists of player names from database and list of names from csv table
	old_players_names = [p.name for p in all_players]
	tournament_player_names = player.get_players_from_table(file_location)	

	# Check if new players
	if not all(p in old_players_names for p in tournament_player_names):
		# New players found. Creates list of new names and prints
		new_player_names = []
		print("\nNew players found:")
		for name in tournament_player_names:
			if name not in old_players_names:
				new_player_names.append(name)
				print(name)
		# Also, creates new Player instances and appends to players
		level = int(input("\nWhat is the starting level of these players?\n(0 = 500 Elo, 1 = 1000 Elo, 2 = 1500 Elo)\n"))
		for name in new_player_names:
			new_player = player.newPlayer(name, level)
			all_players.append(new_player)
	#___________________________________

	# Filter all players to tournament players
	tournament_players = [p for p in all_players if p.name in tournament_player_names]

	# csv to list of Game instances and save games to json database
	raw_game_list = game.from_table_to_games_list(file_location)
	games = game.game_lists_to_game_instances(date, raw_game_list, tournament_players)
	sl.save_new_games(games)
	print("\nSaved games to game_database.json successfully.")

	# Calculate and update Elos and Elo histories
	for p in tournament_players:
		new_elo = p.calculate_new_elo_tournament(games)
		p.update_elo_and_history(date, new_elo)

	# Save all players back into json database
	sl.save_players(all_players)
	print("Updated players to players_database.json successfully.\n")
	input()

#_____________________________________________________________________
# Data lookup
# TODO: Comment and document

def data_query():
	#os.system("cls")
	x = input("Input the name of the player you wish to look up or press enter to go back:\n")

	if x == "":
		return
	players = []
	players = sl.load_players()
	found = False
	for p in players:
		if p.name == x:
			found = True
			print_player_games(p)
			break
	if found == False:
		input("No player with that name")
		return
	plot = input("\nDo you want a Elo history plot? (y/n)\n")
	if plot == "y":
		p.plot_elo_history()
	return

def print_player_games(p):
	games = []
	games = sl.load_games()
	os.system("cls" if os.name == "nt" else "clear") # Clear terminal
	p.print_player()
	print() # New line
	found = False
	print("    Date       White player             Black player      Player's score\n")
	for g in games:
		if (g.white_name == p.name or g.black_name == p.name):
			found = True
			g.print_game(p.name)
	if found == False:
		print("No games found")



#_____________________________________________________________________
# Print Elo leaderboard
# TODO: Comment and document

def print_elo_leaderboard():
	players = sl.load_players()
	players = sorted(players, key=lambda h: h.elo, reverse=True)
	i = 1
	os.system("cls" if os.name == "nt" else "clear") # Clear terminal
	# TODO: print("TYLO rating leaderboard (last update: DATE):\n")
	print("TYLO rating leaderboard:\n")
	for p in players:
		print(f"{i}: {p.elo}, {p.name}")
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
		os.system("cls" if os.name == "nt" else "clear") # Clear terminal
		command = input("Input a command \n1: Input tournament data \n2: Look at a profile \n3: Print TYLO leaderboard \n")
		os.system("cls" if os.name == "nt" else "clear") # Clear terminal
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