import json
import player_register

class Game:

    def __init__(self, date, white_name, black_name, white_score):

        self.date = date
        self.white_name = white_name
        self.black_name = black_name
        self.white_score = white_score
        self.game_id = 1

        self.white_player = player_register.find_player(white_name)

        self.white_id = self.white_player.get_id()
        self.black_id = self.black_player.get_id()
        self.white_elo = self.white_player.get_elo()
        self.black_elo = self.black_player.get_elo()

    

    def print_game(self):
        # Date / White name (rating) / black name (rating) / white_score
        game_list = [self.date, self.white_player.get_name()]
        print(game_list)

