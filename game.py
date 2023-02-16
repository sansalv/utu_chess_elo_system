from termcolor import colored

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
            print("[" + str(self.date) + "] " + self.white_name + " (" + str(self.white_elo) +") "+ self.black_name + " (" + str(self.black_elo) +") " + str(self.white_score)  + colored(" Defeat", "red"))



