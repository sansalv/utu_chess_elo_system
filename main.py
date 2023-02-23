import player
import game
import save_and_load as sl
import input_data

import matplotlib.pyplot as plt
import datetime as dt
import os # For clearing terminal

#_______________________________________________________________________
# Tournament data input. Creates games and players from csv data and updated databases.
def update_from_data():

	new_tournament_files, new_free_games_files = sl.get_new_input_file_lists()
	new_files = new_tournament_files + new_free_games_files
	
	if len(new_files) == 0:
		print("Everything up to date. No new data files to update.")
		input("\nPress enter to continue.")
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
			input_data.input_tournament(source_file=f, level=0)
			sl.save_input_source(f)
		elif file_info == "Intermediate":
			input_data.input_tournament(source_file=f, level=1)
			sl.save_input_source(f)
		elif file_info == "Experienced":
			input_data.input_tournament(source_file=f, level=2)
			sl.save_input_source(f)
		elif file_info == "Free":
			if f.split(" - ")[1] == "Games Output.csv":
				input_data.input_games(free_games_csv_pairs[free_games_idx])
				sl.save_input_source(f)
				free_games_idx += 1
			elif f.split(" - ")[1] == "New Players Output.csv":
				sl.save_input_source(f)
				continue
			else:
				print(f"\nFree games file {f} not identified. This file will be skipped.")
				input("\nPress enter to continue.")
		else:
			print(f"\nFile {f} not identified. This file will be skipped.")
			input("\nPress enter to continue.")

#_____________________________________________________________________
# Reset all databases and input all

def reset_and_input_all():
	sl.reset_json_database("databases/players_database.json")
	sl.reset_json_database("databases/games_database.json")
	sl.reset_txt_file("databases/inputed_files.txt")
	print()
	update_from_data()
#_____________________________________________________________________
# Data lookup
# TODO: Comment and document

def data_query():

	x = input("Input the name of the player you wish to look up or press enter to go back:\n")

	if x == "":
		return
	players = sl.load_players()
	found = False
	for p in players:
		if p.name == x:
			found = True
			clear_terminal()
			games = sl.load_games()
			player.print_player_games(p, games)
			break
	if found == False:
		input("No player with that name")
		return
	plot = input("\nDo you want a Elo history plot? (y/n)\n")
	if plot == "y":
		p.plot_elo_history()
	return
#_____________________________________________________________________
# Print Elo leaderboard
# TODO: Comment and document

def print_elo_leaderboard():
	players = sl.load_players()
	players = sorted(players, key=lambda h: h.elo, reverse=True)
	i = 1
	clear_terminal()
	# TODO: print("TYLO rating leaderboard (last update: DATE):\n")
	print("TYLO rating leaderboard:\n")
	for p in players:
		print(f"{i}: {p.elo}, {p.name}")
		i += 1

	plot = input("\nDo you want a leaderboard bar plot? (y/n)\n")
	if plot == "y":
		names = [f"{p.name[0]}. " + p.name.split(" ")[1] for p in reversed(players)]
		elos = [p.elo for p in reversed(players)]
		plt.barh(names, elos)
		plt.grid()
		plt.show()

	input("\nPress enter to continue.")

def clear_terminal():
	os.system("cls" if os.name == "nt" else "clear") # Clear terminal
#_______________________________________________________________________
#_______________________________________________________________________
	
def main():
	#TODO: Comment and document

	# 1: Update databases
	# 2: Reset and input all (caution)
	# 3: Look at a profile
	# 4: Print TYLO leaderboard
	# Press enter to exit

	while True:
		# System clears are commented out because different commands work for Linux and Windows
		clear_terminal()
		command = input("Input a command\n\n1: Check for new data\n2: Reset and input all (CAUTION)\n3: Look at a profile\n4: Print TYLO leaderboard\n\nENTER: Exit\n\n")
		clear_terminal()
		match command:
			case "1":
				clear_terminal()
				update_from_data()
			case "2":
				ans = input("WARNING:\nAre you sure you want to reset (and input) all? (y/n)\n")
				if ans == "y":
					clear_terminal()
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