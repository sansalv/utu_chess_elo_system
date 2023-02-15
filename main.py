import json
import player
import game
#_______________________________________________________________________

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
#_______________________________________________________________________
	
def main():
	"""
	Here main() handles tournament data. Creates games and players from test data.

	TODO: combine with @Elias Ervelä code that handles tournament data
	TODO: load old data and only update new
	"""

	
	# TODO: Input(date) or something
	date = "2023-02-15"
	
	# TODO: load old players and new players from sheets data (@Elias Ervelä)
	players = []

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

	save_games(games)

	for p in players:
		new_elo = p.calculate_new_elo_tournament(games)
		p.update_elo_and_history(date, new_elo)

	save_players(players)


#_______________________________________________________________________	

if __name__ == "__main__":
    main()
	
