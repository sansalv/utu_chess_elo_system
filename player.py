import json

class Player:
    def __init__(self, name, elo, elo_history, N, id):
        self.name = name
        self.elo = elo
        self.elo_history = elo_history
        self.N = N # Number of games played
        self.id = id

    # Setters and getters:
    def get_name(self):
        return self.name
    def get_id(self):
        return self.id
    def get_elo_history(self):
        return self.elo_history
    def update_elo(self, new_elo):
        self.elo = new_elo

    """
    Functions:
    - player_as_dictionary()            = Return player as a dictionary (for json)
    - calculate_new_elo_single(...)     = Return new Elo from a single game
    - calculate_new_elo_tournament(...) = Return new Elo from many games
    """

    def calculate_new_elo_single(self, opponent_elo, score):
        """
        Method that returns new Elo rating from a SINGLE game
            score: 0=lose, 0.5=tie, 1=win
            opponent_elo: eg. 1500

        To understand Elo, read:
        https://www.omnicalculator.com/sports/elo
        https://en.wikipedia.org/wiki/Elo_rating_system
        """

        # Define the K-factor form number of games (=n)
        if self.N <= 10:
            K = 128
        elif self.N <= 20:
            K = 64
        else:
            K = 32

        # Calculate expected score of the game
        expected_score = 1/(1 + 10**((opponent_elo - self.elo)/400))
            
        # Calculate new elo rating
        new_elo = self.elo + K*(score - expected_score)
        
        return new_elo

    def calculate_new_elo_tournament(self, games): # games = row in tournament dataframe?
        """
        Method that returns new Elo rating from games list (from whole tournament day)
        
            tuple elements in games list:
                score: 0=lose, 0.5=tie, 1=win
                opponent_elo: f.ex. 1500
        """
        
        # Define the K-factor form number of games previous to these (=n)
        # (New players get bigger Elo correction jumps)
        if self.N <= 10:
            K = 128
        elif self.N <= 20:
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
            expected_score = 1/(1 + 10**((opponent_elo - self.elo)/400))
            expected_score_sum += expected_score
        
        # Calculate new Elo rating
        new_elo = self.elo + K*(score_sum - expected_score_sum)
        
        # Round to nearest integer
        new_elo = int(new_elo + 0.5)
        
        return new_elo