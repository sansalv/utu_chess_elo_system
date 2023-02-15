import json
import player
import game

def newPlayer(name):
	id = 0
	new_player = player.Player(name, 1500, [], 0)
	return new_player

def find_player(players, name):
	for p in players:
		if p.get_name() == name:
			return p
	return 0

def save_players(players):
	playerstable = [vars(p) for p in players]
	json_format = json.dumps(playerstable, indent=2)
	with open("players_database.json", "w") as db:
		db.write(json_format)

def load_players():
    with open("players_database.json", "r") as db:
        json_format = db.read()
    players_dictionary = json.loads(json_format)
    return players_dictionary

def save_games(games):
	gamestable = [vars(g) for g in games]
	json_format = json.dumps(gamestable, indent=2)
	with open("games_database.json", "w") as db:
		db.write(json_format)

def load_games():
    with open("games_database.json", "r") as db:
        json_format = db.read()
    games_dictionary = json.loads(json_format)
    return games_dictionary

def input_tournament():
	date = "2023-02-15"
	# Create players (test version)
	# TODO: load old players and new players from sheets data
	players = []
	new_player_names = ["Santeri Salomaa", "Elias Ervelä", "Kimmo Pyyhtiä"]
	for name in new_player_names:
		new_player = newPlayer(name)
		players.append(new_player)

	# New games from a tournament data
	# date, white_name, white_elo, black_name, black_elo, white_score
	data1 = ["Santeri Salomaa", "Elias Ervelä", 1]
	data2 = ["Santeri Salomaa", "Kimmo Pyyhtiä", 1]
	data = [data1, data2]
	games = []
	for d in data:
		w = find_player(players, d[0])
		b = find_player(players, d[1])
		w_elo = w.get_elo()
		b_elo = b.get_elo()

		g = game.Game(date, d[0], w_elo, d[1], b_elo, d[2])
		games.append(g)

	save_games(games)

	for p in players:
		new_elo = p.calculate_new_elo_tournament(games)
		p.update_elo_and_history(date, new_elo)

	save_players(players)

def data_query():
	x = input("Input the name of the player you wish to look up: ")
	if x == "":
		return
	# TODO: load old players from json data

	# Fake players
	players = []
	new_player_names = ["Santeri Salomaa", "Elias Ervelä", "Kimmo Pyyhtiä", "Onni Snåre"]
	for name in new_player_names:
		new_player = newPlayer(name)
		players.append(new_player)
	# Ends

	for p in players:
		if p.get_name() == x:
			print_player_games(p)
			break
	return

def print_player_games(x):
	# TODO: load old games from json data

	# Fake players
	players = []
	new_player_names = ["Onni Snåre", "Elias Ervelä", "Kimmo Pyyhtiä", "Santeri Salomaa"]
	for name in new_player_names:
		new_player = newPlayer(name)
		players.append(new_player)
	# Ends

	# Fake games
	data1 = ["Santeri Salomaa", "Elias Ervelä", 1]
	data2 = ["Santeri Salomaa", "Kimmo Pyyhtiä", 1]
	data3 = ["Santeri Salomaa", "Onni Snåre", 0]
	data = [data1, data2, data3]
	games = []
	for d in data:
		w = find_player(players, d[0])
		b = find_player(players, d[1])
		w_elo = w.get_elo()
		b_elo = b.get_elo()

		g = game.Game("1.1.2023", d[0], w_elo, d[1], b_elo, d[2])
		games.append(g)
	# Ends

	x.print_player()
	for peli in games:
		if (peli.get_white_name() == x.get_name() or peli.get_black_name() == x.get_name()):
			peli.print_game()
	input("Loppu")



#_______________________________________________________________________
	
def main():
	#Fake players
	players = []
	new_player_names = ["Santeri Salomaa", "Elias Ervelä", "Kimmo Pyyhtiä", "Onni Snåre"]
	for name in new_player_names:
		new_player = newPlayer(name)
		players.append(new_player)
	#Ends

	# Fake games
	data1 = ["Santeri Salomaa", "Elias Ervelä", 1]
	data2 = ["Santeri Salomaa", "Kimmo Pyyhtiä", 1]
	data3 = ["Santeri Salomaa", "Onni Snåre", 0]
	data = [data1, data2, data3]
	games = []
	for d in data:
		w = find_player(players, d[0])
		b = find_player(players, d[1])
		w_elo = w.get_elo()
		b_elo = b.get_elo()

		g = game.Game("1.1.2023", d[0], w_elo, d[1], b_elo, d[2])
		games.append(g)
	#Ends
	verbose = True
	#Input tournament data
	#Look up player specific data
	#
	command = input("Input a command \n 1: Input tournament data \n 2: Look at a profile \n")
	match command:
		case "1":
			if verbose:
				print("Entering data input")
			input_tournament()
		case "2":
			if verbose:
				print("Entering data query")
			data_query()
		case "":
			exit()
		case "t":
			games[2].print_game()
		case _:
			print("Incorrect command")

	
		

if __name__ == "__main__":
    main()
	
