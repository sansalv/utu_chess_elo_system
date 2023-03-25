import player
import game
import json
import glob
import os

# Methods for resetting, saving and loading the json data
# TODO: Comment and document rest of this libraby


def reset_json_database(database_file):
    empty_dir_list = []
    json_format = json.dumps(empty_dir_list)
    with open(database_file, "w") as db:
        db.write(json_format)
    print(f"Database {database_file} resetted.")


def reset_txt_file(txt_file):
    with open(txt_file, "w") as txt:
        pass
    print(f"Database {txt_file} resetted.")


def save_input_source(source_name, filename="databases/inputed_files.txt"):
    with open(filename, "a") as txt:
        txt.write(source_name + "\n")


def get_new_input_file_lists(filename="databases/inputed_files.txt"):
    old_files = []
    if os.stat(filename).st_size != 0:
        with open(filename, "r") as txt:
            old_files = txt.read().splitlines()

    # New tournament file names that are not in inputed_files.txt
    tournament_paths = glob.glob("tournament_data/*")
    tournament_files = []
    for path in tournament_paths:
        tournament_files.append(path.split("/")[-1])

    new_tournament_files = []
    for f in tournament_files:
        if f not in old_files:
            new_tournament_files.append(f)

    # New free games file names that are not in inputed_files.txt
    free_games_paths = glob.glob("free_rated_games_data/*")
    free_games_files = []
    for path in free_games_paths:
        free_games_files.append(path.split("/")[-1])

    new_free_games_files = []
    for f in free_games_files:
        if f not in old_files:
            new_free_games_files.append(f)

    return new_tournament_files, new_free_games_files


def save_players(players, filename="databases/players_database.json"):
    """
        Method for saving players list to database.

    Parameters
    ----------
        players : list of Player instances
    """
    # Make a list of Player dictionaries
    playerstable = [vars(p) for p in players]
    json_format = json.dumps(playerstable, indent=4)
    with open(filename, "w") as db:
        db.write(json_format)


# Update games database
# Read old json, extend list to new data and dump all to json
def save_new_games(new_games, filename="databases/games_database.json"):
    """
        Method for saving NEW games to games database.

    Parameters
    ----------
    first_games : list of Game instances
    """
    # Read old json
    with open(filename, "r") as db:
        old_json = db.read()
    game_dictionaries = json.loads(old_json)

    # List of new game dictionaries to new json data
    newgamestable = [vars(g) for g in new_games]
    # Extend old data to new games
    game_dictionaries.extend(newgamestable)
    updated_json = json.dumps(game_dictionaries, indent=4)

    # Write the updated json
    with open(filename, "w") as db:
        db.write(updated_json)


def load_players(filename="databases/players_database.json"):
    """
        Method for loading whole players list from database.

    Returns
        -------
        players : list of Player instances
    """
    with open(filename, "r") as db:
        json_format = db.read()
    player_dictionaries = json.loads(json_format)
    players = []
    for j in player_dictionaries:
        players.append(player.Player(**j))
    return players


def load_games(filename="databases/games_database.json"):
    """
        Method for loading whole games list from database.

    Returns
        -------
        games : list of Game instances
    """
    with open(filename, "r") as db:
        json_format = db.read()
    game_dictionaries = json.loads(json_format)
    games = []
    for j in game_dictionaries:
        games.append(game.Game(**j))
    return games
