import json
import player
import game
import os

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
# level 0 = beginner league player, level 1 = experienced league player
def newPlayer(name, level):
	if level == 0:
		starting_elo = 800
	else:
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

def save_players(players):
	# Make a list of Player dictionaries
	playerstable = [vars(p) for p in players]
	json_format = json.dumps(playerstable, indent=4)
	with open("players_database.json", "w") as db:
		db.write(json_format)

def save_games(games):
	# Make a list of Game dictionaries
	gamestable = [vars(g) for g in games]
	json_format = json.dumps(gamestable, indent=4)
	with open("games_database.json", "w") as db:
		db.write(json_format)

# TODO: Finish this method. Now only makes player dictionaries
def load_players():
    with open("players_database.json", "r") as db:
        json_format = db.read()
    players_dictionary = json.loads(json_format)
    return players_dictionary

# TODO: Finish this method. Now only makes game dictionaries
def load_games():
    with open("games_database.json", "r") as db:
        json_format = db.read()
    games_dictionary = json.loads(json_format)
    return games_dictionary

#_______________________________________________________________________
def input_tournament():
	"""
	TODO: load old data and only update new
	"""

	# TODO: Input(date) or something
	date = "2023-02-15"
	# Create players (test version)
	# TODO: load old players and new players from sheets data
	players = []
	players = generate_fakeplayers()

	# Create new players (test version)
	# TODO: check from sheets data, who are new players (not in "players" list), and create them (@Elias Ervelä)
	new_beginner_player_names = ["Elias Ervelä"]
	new_experienced_player_names = ["Santeri Salomaa", "Kimmo Pyyhtiä"]
	for name in new_beginner_player_names:
		new_player = newPlayer(name, 0)
		players.append(new_player)
	for name in new_experienced_player_names:
		new_player = newPlayer(name, 1)
		players.append(new_player)

	# New games from a tournament data
	# date, white_name, white_elo, black_name, black_elo, white_score
	games = []
	games = generate_fakegames()

	save_games(games)

	for p in players:
		new_elo = p.calculate_new_elo_tournament(games)
		p.update_elo_and_history(date, new_elo)

	save_players(players)

def data_query():
	os.system("cls")
	x = input("Input the name of the player you wish to look up or press enter to go back: ")
	if x == "":
		return
	# TODO: load old players from json data

	# Fake players
	players = []
	players = generate_fakeplayers()
	# Ends

	for p in players:
		if p.get_name() == x:
			print_player_games(p)
			break
	data_query()
	return

def print_player_games(x):
	# TODO: load old players and games from json data

	# Fake players
	players = []
	players = generate_fakeplayers()
	# Ends

	# Fake games
	games = []
	games = generate_fakegames()
	# Ends

	x.print_player()
	for peli in games:
		if (peli.get_white_name() == x.get_name() or peli.get_black_name() == x.get_name()):
			peli.print_game(x.get_name())
	input()



#_______________________________________________________________________
	
def main():
	#Main 
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
	
