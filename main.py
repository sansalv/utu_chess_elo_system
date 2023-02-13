#import ???

#_______________________________________________________________________
'''
Functions:

- update_elo_single(...)     = Elo calculator for single game
- update_elo_tournament(...) = Elo calculator for whole tournament day
'''


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
	
