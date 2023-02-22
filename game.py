from termcolor import colored
import player
import pandas as pd

# TODO: Comment and document rest of this libraby

# After Game class there are methods involving Game instances

class Game:

    def __init__(self, date, white_name, white_elo, black_name, black_elo, white_score, source_file):
        self.date = date
        self.white_name = white_name
        self.black_name = black_name
        self.white_elo = white_elo
        self.black_elo = black_elo
        self.white_score = white_score
        self.source_file = source_file
        
    def print_game(self, name):
        # Date / White name (rating) / Black name (rating) / Player's score
        print(f"[{self.date}] {self.white_name} ({self.white_elo}) {self.black_name} ({self.black_elo})", end=' ')
        if (name == self.white_name and self.white_score == 1) or (name == self.black_name and self.white_score == 0):
            print(colored("Victory", "yellow"))
        elif (self.white_score == 0.5):
            print(colored("Draw", "light_blue"))
        else:
            print(colored("Defeat", "red"))

#_______________________________________________________________________
# Methods to convert tournament .csv to games list:

def from_table_to_games_list(file_location, verbose=False):
    """
	Turns tournament game table (csv) in to list of games in format [white_name, black_name, white_result].

	Parameters
	----------
	file_location : str
		Location of the table of tournament games. In which Indexes and columns have players names, and in the cells there is info of who won. Eg. ww=white win, bl=black lose, bd=black draw.
	verbose : bool
		If True, print table and games_list.

	Returns
	-------
	games_list : list of [str, str, float]
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

def game_lists_to_game_instances(date, raw_games_list, players, source_file):
	"""
    Turns raw list of [white_name, black_name, white_result] elements to list of game instances.
    The raw list of games comes from either from_table_to_games_list(...) or from_games_csv_to_games_list(...).
    
    Parameters
    ----------
    date : str
        In format yyyy-mm-dd.
    raw_games_list : list of [str, str, float]
    players : list of Player instances
    source_file : str

    Returns
    -------
    games : list of Game instances
    """
	games = []
	for g in raw_games_list:
		w = player.find_player(players, g[0])
		b = player.find_player(players, g[1])
		g = Game(date, g[0], w.get_elo(), g[1], b.get_elo(), g[2], source_file)
		games.append(g)
	return games

def from_games_csv_to_games_list(file_location):
    """
    Parameters
    ----------
    file_location : String
        File location path of the file.
    
    Returns
    -------
    List of games in format [White Player, Black Player, White result]
    """
    free_games = pd.read_csv(file_location)
    free_games_list = []
    for i in range(len(free_games)):
        free_games_list.append(list(free_games.iloc[i]))
    return free_games_list

# Get free games pairs
def get_free_games_csv_pairs(new_files): # new_files is a sorted list (by datetime) of csv files

	# Filter only free games data (others are tournaments)
	# This will leave games and new players
	free_games = [f for f in new_files if f.split("_")[1] == "Free"]
	# Free games csv pairs will be in the list free_games_with_new_players
	n_free_games = len(free_games)/2
	free_games_with_new_players = [[None, None] for i in range(n_free_games)]
	
	new_players_files = []
	i = 0
	for f in free_games:
		t = f.split(" - ")[1]
		if t == "Games Output.csv":
			free_games_with_new_players[i][0] = f
			i += 1
		elif t == "New Players Output.csv":
			new_players_files.append(f)
		else:
			print(f"\nFile {f} not identified. This file will be skipped. Press enter to continue.")
			input()

	# Pair the new players data to the free games data

	# Iterate free games files
	for f_pair in free_games_with_new_players:
		# Free games date
		f_pair_date = f_pair[0].split("_")[0]
		# Find matching date from new_players_files
		for new_players_file in new_players_files:
			new_players_file_date = new_players_file.split("_")[0]
			# If the date matches, make the pair
			if f_pair_date == new_players_file_date:
				f_pair[1] = new_players_file

	# Check that every entry has a pair
	for f_pair in free_games_with_new_players:
		if f_pair[0] == None or f_pair[1] == None:
			raise Exception(f"Free games name ERROR: free games csv entry {f_pair} is not correct format. Check data names.")

	return free_games_with_new_players