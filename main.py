import json
import player
import game
#_______________________________________________________________________

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
		games.append(game.Games(**j))
	return games


#_______________________________________________________________________
#_______________________________________________________________________
	
def main():
	"""
	Here main() handles tournament data. Creates games and players from test data.

	TODO: combine with @Elias Ervelä code that handles tournament data
	TODO: load old data and only update new
	"""

	# First tournament day
	# TODO: Input(date) or something
	date = "2023-02-15"
	
	# TODO: load old players and new players from sheets data (@Elias Ervelä)
	players = []

	# Create new players (test version)
	# TODO: check from sheets data, who are new players (not in "players" list), and create them (@Elias Ervelä)
	new_intermediate_player_names = ["Elias Ervelä"]
	new_experienced_player_names = ["Santeri Salomaa", "Kimmo Pyyhtiä"]
	for name in new_intermediate_player_names:
		new_player = newPlayer(name, 1)
		players.append(new_player)
	for name in new_experienced_player_names:
		new_player = newPlayer(name, 2)
		players.append(new_player)

	# New games from a tournament data 
	# TODO: games from sheets data (@Elias Ervelä)
	data1 = ["Santeri Salomaa", "Elias Ervelä", 0]
	data2 = ["Santeri Salomaa", "Kimmo Pyyhtiä", 1]
	data = [data1, data2]
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



#_______________________________________________________________________	

if __name__ == "__main__":
    main()
	
