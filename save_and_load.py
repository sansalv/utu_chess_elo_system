import json

def save_game(players):
    playerstable = [p.player_as_dictionary for p in players]
    json_format = json.dumps(playerstable, indent=4)
    with open("database.json", "w") as db:
        db.write(json_format)

def load_game():
    with open("database.json", "r") as db:
        json_format = db.read()
    players = json.loads(json_format)
    return players
