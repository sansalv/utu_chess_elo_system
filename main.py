import json
import player
#import game

def newPlayer(name):
	id = 0
	new_player = player.Player(name, 1500, [1500], 0, id)
	return new_player

def save_players(players):
	playerstable = [vars(p) for p in players]
	print(playerstable)
	json_format = json.dumps(playerstable, indent=2)
	#print(json_format)
	with open("database.json", "w") as db:
		db.write(json_format)

def load_players():
    with open("database.json", "r") as db:
        json_format = db.read()
    players = json.loads(json_format)
    return players

#_______________________________________________________________________
	
def main():

	game1 = ["2023-02-14", "Santeri Salomaa", "Elias Ervelä", 1]
	game2 = ["2023-02-14", "Santeri Salomaa", "Kimmo Pyyhtiä", 1]

	players = load_players()

	new_player_names = ["Santeri Salomaa", "Elias Ervelä", "Kimmo Pyyhtiä"]
	for name in new_player_names:
		new_player = newPlayer(name)
		players.append(new_player)

	"""
	For every player (row in dataframe), update Elo ratings

	for row in dataframe:
		player = player
		player.calculate_new_elo_single()
	"""

	save_players(players)


	

	
		

if __name__ == "__main__":
    main()
	
