import sqlite3
import player
import game

# Define the ChessClub class to manage the database and player/game information
class ChessClub:
    def __init__(self, db):
        # Connect to the database and create necessary tables if they don't exist
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS players (
                              id INTEGER PRIMARY KEY,
                              name TEXT,
                              elo INTEGER,
                              games_played INTEGER,)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS games (
                              id INTEGER PRIMARY KEY,
                              date TEXT,
                              white_id TEXT,
                              white_elo INTEGER,
                              black_id TEXT,
                              black_elo INTEGER,
                              result TEXT,
                              source_file_id INTEGER)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS elo_histories (
                              id INTEGER PRIMARY KEY,
                              date TEXT,
                              player_id INTEGER,
                              source_file_id INTEGER)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS inputed_files (
                              id INTEGER PRIMARY KEY,
                              file_name TEXT,
                              tournament BIT,
                              free_games BIT
                              free_games_new_players BIT)''')

    def add_player(self, player):
        # Add a new player to the players table
        self.cursor.execute('''INSERT INTO players (name, elo, games_played) VALUES (?, ?, ?)''',
                            (player.name, player.elo, player.games_played))
        self.conn.commit()

    def get_player(self, id):
        # Retrieve a player's information from the players table by ID
        self.cursor.execute('''SELECT id, name, elo, games_played FROM players WHERE id = ?''', (id,))
        row = self.cursor.fetchone()
        if row:
            return player.Player(*row)

    def get_all_players(self):
        # Retrieve all players' information from the players table
        self.cursor.execute('''SELECT id, name, elo, games_played FROM players''')
        rows = self.cursor.fetchall()
        if rows:
            return [player.Player(*row) for row in rows]

    def add_game(self, game):
        # Add a new match to the matches table
        self.cursor.execute('''INSERT INTO games
                              (date, white_id, white_elo, black_id, black_elo, result, source_file_id)
                              VALUES (?, ?, ?, ?, ?, ?, ?)''',
                            (game.date, game.white_player.id, game.white_player.elo, game.black_player.id, game.black_player.elo, game.result, game.source_file_id))
        self.conn.commit()

#---------- belove not corrected

    def get_all_matches(self):
        # Retrieve all matches' information from the matches table, including player objects
        self.cursor.execute('''SELECT matches.id, player1, player2, result, date, players1.name as name1, players1.email as email1, players1.phone as phone1, players1.rating as rating1, players2.name as name2, players2.email as email2, players2.phone as phone2, players2.rating as rating2 FROM matches
                              JOIN players as players1 ON matches.player1 = players1.id
                              JOIN players as players2 ON matches.player2 = players2.id''')
        rows = self.cursor.fetchall()
        if rows:
            matches = []
            for row in rows:
                player1 = Player(row[6], row[7], row[8], row[9])
                player