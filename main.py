import json
import player
import game
#_______________________________________________________________________
'''
Functions:

- update_elo_single(...)     = Elo calculator for single game
- update_elo_tournament(...) = Elo calculator for whole tournament day
- from_table_to_games_list(...)	= Turns tournament score table in to list of games
'''


def from_table_to_games_list(games_table, verbose=False):
    """
	Turns tournament game table in to list of games.

		Variables:
			games_table: Table of tournament games. Indexes and columns have players names, and in the cells there is info of who won. Eg. ww=white win, bl=black lose, bt=black tie 
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
            elif games_table.loc[ind,col] == "wt":
                games_list.append([str(ind), str(col), 0.5])
            elif games_table.loc[ind,col] == "wl":
                games_list.append([str(ind), str(col), 0])

            elif games_table.loc[ind,col] == "bw":
                games_list.append([str(col), str(ind), 0])
            elif games_table.loc[ind,col] == "bt":
                games_list.append([str(col), str(ind), 0.5])
            elif games_table.loc[ind,col] == "bl":
                games_list.append([str(col), str(ind), 1])

    if verbose:
        print("List of games:")
        for i in games_list:
            print(i)

    return games_list




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

	# Test (win, lose, draw)
    print(update_rating_tournament(1200, [(1,1200), (0,1500), (0.5,1000)], 0))
    

if __name__ == "__main__":
    main()
	
