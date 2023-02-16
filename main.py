import json
import player
import game
import os

def from_table_to_games_list(games_table, verbose=False):
    """
	Turns tournament game table in to list of games.

		Variables:
			games_table: Table of tournament games. Indexes and columns have players names, and in the cells there is info of who won. Eg. ww=white win, bl=black lose, bd=black draw 
			verbose: if True, print table and games_list

		Returns: List of games, where every games are in format [white_name, black_name, white_result]

	"""

    if verbose: print("Table: \n", games_table)

    # Get players names from tables index and columns (they should be the same).
    games_table_index = games_table.index
    games_table_columns = games_table.columns

    # Change table to format:
    # [white_name, black_name, white_result]
    # Goes through only the upper triangle in the table.
    games_list = []
    for i in range(len(games_table_index)):
        for j in range(i+1,len(games_table_columns)):
            
            # Names of players from index and columns
            ind = games_table_index[i]
            col = games_table_columns[j]

            # Reads the cell and appends the game to the games_list in appropriate form.
            # ww=white win, wt=white tie, wl=white loss, bw=black win, bt=black tie, bl=black lose
            if games_table.loc[ind,col] == "ww":
                games_list.append([str(ind), str(col), 1])
            elif games_table.loc[ind,col] == "wd":
                games_list.append([str(ind), str(col), 0.5])
            elif games_table.loc[ind,col] == "wl":
                games_list.append([str(ind), str(col), 0])

            elif games_table.loc[ind,col] == "bw":
                games_list.append([str(col), str(ind), 0])
            elif games_table.loc[ind,col] == "bd":
                games_list.append([str(col), str(ind), 0.5])
            elif games_table.loc[ind,col] == "bl":
                games_list.append([str(col), str(ind), 1])

    if verbose:
        print("List of games:")
        for i in games_list:
            print(i)

    return games_list

#_______________________________________________________________________

# Gets list of players name from tournament table (pandas dataframe) and returns list of strings.
def get_players_from_table(games_table):
     player_list = games_table.index
     return list(player_list)


def generate_fakeplayers():
	players = []
	new_player_names = ["Onni Snåre", "Elias Ervelä", "Kimmo Pyyhtiä", "Santeri Salomaa", "Lauri Maila"]
	for name in new_player_names:
		new_player = newPlayer(name, 0)
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
	for d in data:
		w = find_player(players, d[0])
		b = find_player(players, d[1])
		w_elo = w.get_elo()
		b_elo = b.get_elo()

		g = game.Game("1.1.2023", d[0], w_elo, d[1], b_elo, d[2])
		games.append(g)
	return games

# Create new player instance. Starting Elo rating depends on the level
# level 0 = beginner league, level 1 = intermediate league, level 2 = experienced league
def newPlayer(name, level):
	if level == 0: 		# starting at beginner league
		starting_elo = 500
	elif level == 1: 	# starting at intermediate league
		starting_elo = 1000
	else: 				# starting at experienced league
		starting_elo = 1500
	new_player = player.Player(name, starting_elo, [], 0)
	return new_player

# Return Player (instance) from name (string)
def find_player(players, name):
	for p in players:
		if p.get_name() == name:
			return p
	return 0
#_______________________________________________________________________
# Methods for saving and loading the json data

def save_players(players, filename = "players_database.json"):
	# Make a list of Player dictionaries
	playerstable = [vars(p) for p in players]
	json_format = json.dumps(playerstable, indent = 4)
	with open(filename, "w") as db:
		db.write(json_format)

def save_first_games(first_games, filename = "games_database.json"):
	# Make a list of Game dictionaries
	gamestable = [vars(g) for g in first_games]
	json_format = json.dumps(gamestable, indent = 4)
	with open(filename, "w") as db:
		db.write(json_format)

# Update games database
# Read old json, extend list to new data and dump all to json
def save_new_games(new_games, filename = "games_database.json"):

	# Read old json
	with open(filename, "r") as db:
		old_json = db.read()
	game_dictionaries = json.loads(old_json)

	# List of new game dictionaries to new json data
	newgamestable = [vars(g) for g in new_games]
	# Extend old data to new games
	game_dictionaries.extend(newgamestable)
	updated_json  = json.dumps(game_dictionaries, indent = 4)

	# Write the updated json
	with open(filename, "w") as db:
		db.write(updated_json)

def load_players():
	with open("players_database.json", "r") as db:
		json_format = db.read()
	player_dictionaries = json.loads(json_format)
	players = []
	for j in player_dictionaries:
		players.append(player.Player(**j))
	return players

def load_games(filename = "games_database.json"):
	with open(filename, "r") as db:
		json_format = db.read()
	game_dictionaries = json.loads(json_format)
	games = []
	for j in game_dictionaries:
		games.append(game.Game(**j))
	return games


#_______________________________________________________________________
#Tournament data input

def input_tournament():
	filename = input("Insert filename of the tournament .csv-file: ")
	players = load_players()
	"""
	Here input_tournament() handles tournament data. Creates games and players from test data.
	TODO: combine with @Elias Ervelä code that handles tournament data
	TODO: load old data and only update new
	TODO: Identify whether databases exist and choose between save_first_games() and save_new_games()
	"""

	# First tournament day
	# TODO: Input(date) or something
	date = "2023-02-15"
	
	# TODO: load old players and new players from sheets data (@Elias Ervelä)
	players = []

	# Create new players (test version)
	# TODO: check from sheets data, who are new players (not in "players" list), and create them (@Elias Ervelä)
	new_intermediate_player_names = ["Elias Ervelä", "Onni Snåre", "Kaisa Hakkarainen", "Kerttu Pusa"]
	new_experienced_player_names = ["Santeri Salomaa", "Kimmo Pyyhtiä", "Testi"]
	for name in new_intermediate_player_names:
		new_player = newPlayer(name, 1)
		players.append(new_player)
	for name in new_experienced_player_names:
		new_player = newPlayer(name, 2)
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
	#data = from_table_to_games_list(filename)
	games = []
	for d in data:
		w = find_player(players, d[0])
		b = find_player(players, d[1])
		w_elo = w.get_elo()
		b_elo = b.get_elo()
		# game = (date, white_name, white_elo, black_name, black_elo, white_score)
		g = game.Game(date, d[0], w_elo, d[1], b_elo, d[2])
		games.append(g)
	save_first_games(games)

	for p in players:
		new_elo = p.calculate_new_elo_tournament(games)
		p.update_elo_and_history(date, new_elo)
	save_players(players)

"""
	# Second tournament day
	date = "2023-02-16"

	players = []
	players = load_players()

	data1 = ["Santeri Salomaa", "Elias Ervelä", 0.5]
	data2 = ["Santeri Salomaa", "Kimmo Pyyhtiä", 0]
	data = [data1, data2]
	new_games = []
	for d in data:
		w = find_player(players, d[0])
		b = find_player(players, d[1])
		w_elo = w.get_elo()
		b_elo = b.get_elo()
		# game = (date, white_name, white_elo, black_name, black_elo, white_score)
		g = game.Game(date, d[0], w_elo, d[1], b_elo, d[2])
		new_games.append(g)
	save_new_games(new_games) # Extend games database

	for p in players:
		new_elo = p.calculate_new_elo_tournament(new_games)
		p.update_elo_and_history(date, new_elo)
	save_players(players)

	for p in players:
		new_elo = p.calculate_new_elo_tournament(games)
		p.update_elo_and_history(date, new_elo)
	save_players(players)
"""
#_____________________________________________________________________
#Data lookup

def data_query():
	os.system("cls")
	x = input("Input the name of the player you wish to look up or press enter to go back: ")
	if x == "":
		return
	players = []
	players = load_players()
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
	games = load_games()
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


	#1: Input tournament data from a csv file
	#2: Look up player specific data
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
	
