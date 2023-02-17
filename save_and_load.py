import player
import game
import json

# Methods for saving and loading the json data

def save_players(players, filename = "players_database.json"):
	"""
	Method for saving players list to database
	
        Variables:
            players: List of Players instances you want to save
	"""
	# Make a list of Player dictionaries
	playerstable = [vars(p) for p in players]
	json_format = json.dumps(playerstable, indent = 4)
	with open(filename, "w") as db:
		db.write(json_format)
		
# Update games database
# Read old json, extend list to new data and dump all to json
def save_new_games(new_games, filename = "games_database.json"):
	"""
	Method for saving NEW games to games database
	
        Variables:
            first_games: List of Game instances you want to save
	"""
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

def save_first_games(first_games, filename = "games_database.json"):
	"""
	Method for saving FIRST games to EMPTY database
	
        Variables:
            first_games: List of Game instances you want to save
	"""
	# Make a list of Game dictionaries
	gamestable = [vars(g) for g in first_games]
	json_format = json.dumps(gamestable, indent = 4)
	with open(filename, "w") as db:
		db.write(json_format)

def load_players():
	"""
	Method for loading players list from database
	
        Returns: players list of all Player instances in the database
	"""
	with open("players_database.json", "r") as db:
		json_format = db.read()
	player_dictionaries = json.loads(json_format)
	players = []
	for j in player_dictionaries:
		players.append(player.Player(**j))
	return players

def load_games(filename = "games_database.json"):
	"""
	Method for loading games list from database
	
        Returns: games list of all Game instances in the database
	"""
	with open(filename, "r") as db:
		json_format = db.read()
	game_dictionaries = json.loads(json_format)
	games = []
	for j in game_dictionaries:
		games.append(game.Game(**j))
	return games