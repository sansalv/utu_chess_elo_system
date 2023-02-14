import json

class Player:
    def __init__(self, name, elo, game_history):
        self.name = name
        self.elo = elo
        self.game_history = game_history
    
    def give_game_history(self):
        # Give game history in readable format from the game_history attribute
        pass
    
    def add_to_history(self, game):
        # Add game to history
        pass

    def update_elo(self, elo):
        self.elo = elo

    def player_as_dictionary(self):
        player_dict = vars(self)
        return player_dict

