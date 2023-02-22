import player
import game
import save_and_load as sl
import datetime as dt
import os # For clearing terminal

#_____________________________________________________________________
# Reset all databases and input all

def reset_and_input_all():
	sl.reset_json_database("players_database.json")
	sl.reset_json_database("games_database.json")
	sl.reset_txt_file("inputed_files.txt")

	update_from_data()
#_______________________________________________________________________
# Tournament data input. Creates games and players from csv data and updated databases.
def update_from_data():
	os.system("cls" if os.name == "nt" else "clear") # Clear terminal

	new_tournament_files, new_free_games_files = sl.get_new_input_file_lists()
	new_files = new_tournament_files.extend(new_free_games_files)
	
	if len(new_files) == 0:
		print("Everything up to date. No new data files to update.")
		input()
		return
	
	# Sort files by datetime for the input order
	new_files.sort(key = lambda f: dt.datetime.strptime(f.split("_")[0], "%Y-%m-%d"))


	print("New files found:\n")
	print(*new_files, sep='\n')

	ans = input("\nDo you want to update this/these files? (y/n)\n")
	if ans != "y":
		return
	
	free_games_csv_pairs = game.get_free_games_csv_pairs(new_files)
	free_games_idx = 0
	
	for f in new_files:
		file_info = f.split("_")[1]
		if file_info == "Beginners":
			input_tournament(filename=f, level=0)
			sl.save_input_source(f)
		elif file_info == "Intermediate":
			input_tournament(filename=f, level=1)
			sl.save_input_source(f)
		elif file_info == "Experienced":
			input_tournament(filename=f, level=2)
			sl.save_input_source(f)
		elif file_info == "Free":
			if f.split(" - ")[1] == "Games Output.csv"
				input_games(free_games_csv_pairs[free_games_idx])
				free_games_idx += 1
			elif f.split(" - ")[1] == "New Players Output.csv":
				continue
			else:
				print(f"\nFree games file {f} not identified. This file will be skipped. Press enter to continue.")
				input()
		else:
			print(f"\nFile {f} not identified. This file will be skipped. Press enter to continue.")
			input()



#_______________________________________________________________________
# Tournament data input. Creates games and players from csv data and updated databases.

# TODO: Comment the end section of this
def input_tournament(source_file, level):
	#___________________________________
	# Info of the tournament

	print(f"\nInput tournament from file {source_file} started.")
	file_location = f"tournament_data/{source_file}"
	date = source_file.split("_")[0]
	# Checking the date
	ans = input(f"\nIs the date {date} correct? (y/n)\n")
	if ans != 'y':
		ans = input("\nCorrect the mistake and come back. Continue by pressing enter.\n")
		input()
		return
	#___________________________________
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
		print(f"\nNew level {level} players found:")
		for name in tournament_player_names:
			if name not in old_players_names:
				new_player_names.append(name)
				print(name)
		for name in new_player_names:
			new_player = player.newPlayer(name, level)
			all_players.append(new_player)
	#___________________________________

	# Filter all players to tournament players
	tournament_players = [p for p in all_players if p.name in tournament_player_names]

	# csv to list of Game instances and save games to json database
	raw_game_list = game.from_table_to_games_list(file_location)
	games = game.game_lists_to_game_instances(date, raw_game_list, tournament_players, source_file)
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


def input_games(free_games_csv_pair):

	source_file = free_games_csv_pair[0]
	source_file_location = f"free_rated_games_data/{source_file}"
	new_players_file = free_games_csv_pair[1]
	new_players_file_location = f"free_rated_games_data/{new_players_file}"

	#___________________________________
	# Info of the free rated games

	print(f"\nInput free rated games from file {source_file} started.")
	date = source_file.split("_")[0]
	# Checking the date
	ans = input(f"\nIs the date {date} correct? (y/n)\n")
	if ans != 'y':
		ans = input("\nCorrect the mistake and come back. Continue by pressing enter.\n")
		input()
		return
	#___________________________________

	# Load old players from database
	all_players = sl.load_players() # After this old players but later also new players will be appended
	#___________________________________
	# Create new players:

	# TODO: Eliaksen koodista nämä
	new_player_names_with_level = player.get_new_players_with_level_from_games_csv(new_players_file_location)

	print("\nNew players:")
	for name_level in new_player_names_with_level:
		name = name_level[0]
		level = name_level[1]
		print(f"{name}, starting level: {level}")
		all_players.append(player.newPlayer(name, level))
	#___________________________________

	# Filter all players to present players
	present_player_names = player.get_unique_players_from_games_csv(source_file_location)
	present_players = [p for p in all_players if p.name in present_player_names]

	# csv to list of Game instances and save games to json database
	raw_game_list = game.from_games_csv_to_games_list(source_file_location)
	games = game.game_lists_to_game_instances(date, raw_game_list, present_players, source_file)
	sl.save_new_games(games)
	print("\nSaved games to game_database.json successfully.")

	# Calculate and update Elos and Elo histories
	for p in present_players:
		new_elo = p.calculate_new_elo_tournament(games)
		p.update_elo_and_history(date, new_elo)

	# Save all players back into json database
	sl.save_players(all_players)
	print("Updated players to players_database.json successfully.\n")
	input("\nPress enter to continue.")
#_____________________________________________________________________
# Data lookup
# TODO: Comment and document

def data_query():

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

	# 1: Update databases
	# 2: Reset and input all (caution)
	# 3: Look at a profile
	# 4: Print TYLO leaderboard

	while True:
		# System clears are commented out because different commands work for Linux and Windows
		os.system("cls" if os.name == "nt" else "clear") # Clear terminal
		command = input("Input a command\n1: Update databases\n2: Reset and input all (caution)\n3: Look at a profile\n4: Print TYLO leaderboard\n")
		os.system("cls" if os.name == "nt" else "clear") # Clear terminal
		match command:
			case "1":
				update_from_data()
			case "2":
				ans = input("Are you sure you want to reset (and input) all? (y/n)")
				if ans == "y":
					reset_and_input_all()
			case "3":
				data_query()
			case "4":
				print_elo_leaderboard()
			case "":
				exit()
			case _:
				print("Incorrect command")

if __name__ == "__main__":
    main()