from termcolor import colored
import player
import pandas as pd

# TODO: document and comment this libraby
# After Player class there are methods involving Game instances

class Game:

    def __init__(self, date, white_name, white_elo, black_name, black_elo, white_score):
        self.date = date
        self.white_name = white_name
        self.black_name = black_name
        self.white_elo = white_elo
        self.black_elo = black_elo
        self.white_score = white_score
        
    # Getters
    def get_white_name(self):
        return self.white_name
    def get_black_name(self):
        return self.black_name
    def get_white_elo(self):
        return self.white_elo
    def get_black_elo(self):
        return self.black_elo
    def get_white_score(self):
        return self.white_score
    
    def print_game(self, name):
        # Date / White name (rating) / black name (rating) / white_score
        if (name == self.white_name and self.white_score == 1) or (name == self.black_name and self.white_score == 0):
            print("[" + str(self.date) + "] " + self.white_name + " (" + str(self.white_elo) +") "+ self.black_name + " (" + str(self.black_elo) +") " + str(self.white_score)  + colored(" Victory", "yellow"))
        else:
            if (self.white_score == 0.5):
                print("[" + str(self.date) + "] " + self.white_name + " (" + str(self.white_elo) +") "+ self.black_name + " (" + str(self.black_elo) +") " + str(self.white_score)  + colored(" Tie", "light_blue"))
            else:
                print("[" + str(self.date) + "] " + self.white_name + " (" + str(self.white_elo) +") "+ self.black_name + " (" + str(self.black_elo) +") " + str(self.white_score)  + colored(" Defeat", "red"))


#_______________________________________________________________________
# Methods to convert tournament .csv to games list:

def from_table_to_games_list(file_location, verbose=False):
    """
	Turns tournament game table (csv) in to list of games in format [white_name, black_name, white_result].

	Parameters
	----------
	file_location : string
		Location of the table of tournament games. In which Indexes and columns have players names, and in the cells there is info of who won. Eg. ww=white win, bl=black lose, bd=black draw.
	verbose : bool
		If True, print table and games_list.

	Returns
	-------
	games_list : list of [string, string, float]
	"""
	# Read the table from file_location
    games_table = pd.read_csv(file_location, dtype=str, index_col=0)

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

def game_lists_to_game_instances(date, raw_games_list, players):
	"""
    Turns raw list of [white_name, black_name, white_result] elements to list of game instances.
    The raw list of games comes from method from_table_to_games_list(...).
    
	Parameters
	----------
    date : string
        In format yyyy-mm-dd.
	raw_games_list : list of [string, string, float]
	players : list of Player instances

	Returns
	-------
	games : list of Game instances
    """
	games = []
	for g in raw_games_list:
		w = player.find_player(players, g[0])
		b = player.find_player(players, g[1])
		g = Game(date, g[0], w.get_elo(), g[1], b.get_elo(), g[2])
		games.append(g)
	return games