class Player:
    def __init__(self, name, elo, elo_history, games_played):
        self.name = name
        self.elo = elo
        self.elo_history = elo_history
        self.games_played = games_played
        #self.id = id

    # Setters and getters:
    def get_name(self):
        return self.name
    def get_id(self):
        return self.id
    def get_elo(self):
        return self.elo
    def get_elo_history(self):
        return self.elo_history
    
    def update_elo_and_history(self, date, new_elo):
        self.elo = new_elo
        self.elo_history.append((date, new_elo))

    """
    Functions:
    - player_as_dictionary()            = Return player as a dictionary (for json)
    - calculate_new_elo_single(...)     = Return new Elo from a single game
    - calculate_new_elo_tournament(...) = Return new Elo from many games
    """

    def calculate_new_elo_single(self, opponent_elo, score):
        """
        Method that returns new Elo rating from a SINGLE game

        To understand Elo, read:
        https://www.omnicalculator.com/sports/elo
        https://en.wikipedia.org/wiki/Elo_rating_system
        """

        # Define the K-factor form number of games (=n)
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
        
        # Define the K-factor form number of games previous to these (=n)
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
            if self.name == g.get_white_name():
                white = True
            elif self.name == g.get_black_name():
                black = True
            else:
                continue # Not your game

            # If your game
            self.games_played += 1

            if white:
                score = g.get_white_score()
                opponent_elo = g.get_black_elo()
            else:
                score = 1 - g.get_white_score()
                opponent_elo = g.get_white_elo()
            score_sum += score
    
            expected_score = 1/(1 + 10**((opponent_elo - self.elo)/400))
            expected_score_sum += expected_score
        
        # Calculate new Elo rating
        new_elo = self.elo + K*(score_sum - expected_score_sum)
        
        # Round to nearest integer
        new_elo = int(new_elo + 0.5)
        
        return new_elo

    def print_player(self):
        # Name, elo history
        print(self.name + " (" + str(self.elo) + ")")