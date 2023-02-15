#import ???

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


def update_elo_single(old_elo, opponent_elo, score, n):
	'''
	Method that returns new Elo rating from a SINGLE game

		score: 0=lose, 0.5=tie, 1=win
		opponent_elo: f.ex. 1500
		n: number of games played until this
		
	To understand Elo, read https://www.omnicalculator.com/sports/elo
	'''
	
	# Define the K-factor form number of games (=n)
	if n <= 10:
		K = 128
	elif n <= 20:
		K = 64
	else:
		K = 32
	
	# Calculate expected score of the game
	expected_score = 1/(1 + 10**((opponent_elo - old_elo)/400))
		
	# Calculate new elo rating
	new_elo = old_elo + K*(score - expected_score)
	
	return new_elo


def update_elo_tournament(old_elo, games, n):
	'''
	Method that returns new Elo rating from games list (from whole tournament day)
	
		tuple elements in games list:
			score: 0=lose, 0.5=tie, 1=win
			opponent_elo: f.ex. 1500
		n: number of games played until this DAY
	'''
	
	# Define the K-factor form number of games previous to these (=n)
	# (New players get bigger Elo correction jumps)
	if n <= 10:
		K = 128
	elif n <= 20:
		K = 64
	else:
		K = 32
	
	# Calculate score of the day vs. expected score of the day
	score_sum = 0
	expected_score_sum = 0
	for g in games:
	
		score = g[0]
		score_sum += score
		
		opponent_elo = g[1]
		expected_score = 1/(1 + 10**((opponent_elo - old_elo)/400))
		expected_score_sum += expected_score
	
	# Calculate new Elo rating
	new_elo = old_elo + K*(score_sum - expected_score_sum)
	
	# Round to nearest integer
	new_elo = int(new_elo + 0.5)
	
	return new_elo

#_______________________________________________________________________
	
def main():

	# Test (win, lose, draw)
    print(update_rating_tournament(1200, [(1,1200), (0,1500), (0.5,1000)], 0))
    

if __name__ == "__main__":
    main()
	
