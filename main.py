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

#_______________________________________________________________________
	
def main():
	
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

	
		

if __name__ == "__main__":
    main()
	
