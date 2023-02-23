import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
import numpy as np

# TODO: Comment and document rest of this libraby

# After Player class there are methods involving Player instances

class Player:
    def __init__(self, name, elo, elo_history, games_played):
        self.name = name
        self.elo = elo
        self.elo_history = elo_history
        self.games_played = games_played

    # Setter for elo and elo_history
    def update_elo_and_history(self, date, new_elo):
        self.elo = new_elo
        self.elo_history.append((date, new_elo))

    def plot_elo_history(self):
        dates = [eh[0] for eh in self.elo_history]
        x = [dt.datetime.strptime(d,"%Y-%m-%d").date() for d in dates]
        y = [eh[1] for eh in self.elo_history]
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator())
        plt.plot(x,y, '-o')
        plt.xlabel("Date")
        plt.ylabel("TYLO rating")
        plt.gcf().autofmt_xdate()
        plt.show()

    def calculate_new_elo_single(self, opponent_elo, score):
        """
        Method that returns new Elo rating from a SINGLE game
        """

        # Define the K-factor from games played
        if self.games_played <= 10:
            K = 128
        elif self.games_played <= 20:
            K = 64
        else:
            K = 32

        # Calculate expected score of the game
        expected_score = 1/(1 + 10**((opponent_elo - self.elo)/400))
            
        # Calculate new elo rating
        new_elo = self.elo + K*(score - expected_score)

        # Round to nearest integer
        new_elo = int(new_elo + 0.5)
        
        return new_elo

    def calculate_new_elo_tournament(self, games):
        """
        Method that returns new Elo rating from games list (from whole tournament day)
        """
        
        # Define the K-factor from games played
        # (New players get bigger Elo correction jumps)
        if self.games_played <= 10:
            K = 128
        elif self.games_played <= 20:
            K = 64
        else:
            K = 32
        
        # Calculate score of the day vs. expected score of the day
        score_sum = 0
        expected_score_sum = 0
        # Iterate games of the day
        for g in games:
            white = False
            black = False
            if self.name == g.white_name:
                white = True
            elif self.name == g.black_name:
                black = True
            else:
                continue # Not your game

            # If your game
            self.games_played += 1

            if white:
                score = g.white_score
                opponent_elo = g.black_elo
            else:
                score = 1 - g.white_score
                opponent_elo = g.white_elo
            score_sum += score
    
            expected_score = 1/(1 + 10**((opponent_elo - self.elo)/400))
            expected_score_sum += expected_score
        
        # Calculate new Elo rating
        new_elo = self.elo + K*(score_sum - expected_score_sum)
        
        # Round to nearest integer
        new_elo = int(new_elo + 0.5)
        
        return new_elo

    def print_player(self):
        # Name (Elo)
        print(f"Player: {self.name} ({self.elo})")

#_______________________________________________________________________

# Methods outside of class:

# Create new player instance. Starting Elo rating depends on the level
# level 0 = beginner league, level 1 = intermediate league, level 2 = experienced league
def newPlayer(name, level):
    if level == 0: 		# starting at beginner league
        starting_elo = 500
    elif level == 1: 	# starting at intermediate league
        starting_elo = 1000
    else: 				# starting at experienced league
        starting_elo = 1500
    new_player = Player(name, starting_elo, [], 0) # elo_history = [] and games_played = 0
    return new_player

# Return Player (instance) from name (string)
def find_player(players, name):
	for p in players:
		if p.name == name:
			return p
	return 0

def print_player_games(p, games):
	p.print_player()
	print() # New line
	found = False
	print("    Date       White player             Black player      Player's score\n")
	for g in games:
		if (g.white_name == p.name or g.black_name == p.name):
			found = True
			g.print_game(p.name)
	if found == False:
		print("No games found")

def get_players_from_table(file_location):
	"""
	Gets list of players name from tournament table (pandas dataframe) and returns list of strings.

	Parameters
	----------
	file_location : string
		Location of the table of tournament games. In which Indexes and columns have players names.
	
	Returns
	-------
	player_list : list of strings
		Player names in list of strings.
	"""
	games_table = pd.read_csv(file_location, dtype=str, index_col=0)
	player_list = list(games_table.index)
	return player_list

def get_unique_players_from_games_csv(file_location):
    """
    Parameters
    ----------
    file_location : String
        File location path of the file.

    Returns
    -------
    List of String. All unique players from columns "White Player" and "Black Player".
    """
    free_games = pd.read_csv(file_location)
    return list(np.unique(np.hstack([free_games["White Player"],free_games["Black Player"]])))

def get_new_players_with_level_from_games_csv(file_location):
    """
    Parameters
    ----------
    file_location : String
        File location path of the file.
    
    Returns
    -------
    List of tuples, with player name and starting TYLO rank (0, 1 or 2). Eg. [["Elias Ervelä", 1],["Santeri Salomaa",2]].
    """
    new_players_table = pd.read_csv(file_location)
    new_players_list = []
    for i in range(len(new_players_table)):
        new_players_list.append(list(new_players_table.iloc[i]))
    return new_players_list