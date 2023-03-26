import player
import game
import json
import glob
import os

# Methods for resetting, saving and loading the databases

def reset_json_database(database_file):
    """
    Resets a JSON database file by overwriting it with an empty list.
    
    Parameters
    ----------
    database_file : str
        The path to the JSON database file to reset.
    
    Returns
    -------
    None
    """
    empty_dir_list = []
    json_format = json.dumps(empty_dir_list)
    with open(database_file, "w") as db:
        db.write(json_format)
    print(f"Database {database_file} resetted.")


def reset_txt_file(txt_file):
    """
    Resets a text file by opening it and immediately closing it, effectively deleting all contents.
    
    Parameters
    ----------
    txt_file : str
        The path to the text file to reset.
    
    Returns
    -------
    None
    """
    with open(txt_file, "w") as txt:
        pass
    print(f"Database {txt_file} resetted.")


def save_input_source(source_name, filename="databases/inputed_files.txt"):
    """
    Appends the name of an input source to a text file.
    
    Parameters
    ----------
    source_name : str
        The name of the input source to save.
    filename : str
        The path to the text file to append to. Default is "databases/inputed_files.txt".
    
    Returns
    -------
    None
    """
    with open(filename, "a") as txt:
        txt.write(source_name + "\n")


def get_new_input_file_lists(filename="databases/inputed_files.txt"):
    """
    Returns lists of new input files that have not been processed before, based on a file containing a list 
    of previously input files.

    This method reads the contents of the specified file and splits it into a list of previously input file names. 
    It then searches for new tournament and free games files that are not in this list, and returns the names of 
    these new files as separate lists.

    Parameters
    ----------
    filename : str
        The path to the file containing the list of previously input files. Default is "databases/inputed_files.txt".

    Returns
    -------
    new_tournament_files, new_free_games_files : tuple
        A tuple containing two lists - the names of new tournament files and new free games files, respectively.
    """

    # First, read the contents of the file containing previously input files
    old_files = []
    if os.stat(filename).st_size != 0: # check if file is empty
        with open(filename, "r") as txt:
            old_files = txt.read().splitlines()

    # Next, search for new tournament files that have not been processed before
    tournament_paths = glob.glob("tournament_data/*")
    tournament_files = [path.split("/")[-1] for path in tournament_paths] # extract file name from path
    new_tournament_files = [f for f in tournament_files if f not in old_files]

    # Similarly, search for new free games files that have not been processed before
    free_games_paths = glob.glob("free_rated_games_data/*")
    free_games_files = [path.split("/")[-1] for path in free_games_paths] # extract file name from path
    new_free_games_files = [f for f in free_games_files if f not in old_files]

    # Return a tuple containing the new tournament and free games file names
    return new_tournament_files, new_free_games_files


def save_players(players, filename="databases/players_database.json"):
    """
    Method for saving players list to database.

    Parameters
    ----------
    players : list of Player instances

    Returns
    -------
    None
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
    Method for saving new games to games database.

    Parameters
    ----------
    new_games : list of Game instances

    Returns
    -------
    None
    """
    # Convert new games to a list of dictionaries
    new_game_dictionaries = [vars(g) for g in new_games]

    # Open the JSON file in append mode
    with open(filename, "a") as db:
        # Write each new game dictionary as a separate line of JSON text
        for game_dict in new_game_dictionaries:
            db.write(json.dumps(game_dict, indent=4) + "\n")

    # The old code. It is here, just in case, if the new append method above doesn't work.
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
    """

def load_players(filename="databases/players_database.json"):
    """
    Load the list of players from a JSON file.

    Parameters
    ----------
    filename : str, optional
        The filename of the JSON file to load. Default is "databases/players_database.json".

    Returns
    -------
    players : list of Player instances
        The list of Player instances loaded from the file.
    """

    # Open the file in read mode
    with open(filename, "r") as db:
        # Read the JSON text from the file
        json_format = db.read()

    # Parse the JSON text as a list of dictionaries
    player_dicts = json.loads(json_format)

    # Convert each dictionary into a Player instance
    players = [player.Player(**j) for j in player_dicts]

    return players


def load_games(filename="databases/games_database.json"):
    """
    Load games list from a JSON database file.

    Parameters
    ----------
    filename : str, optional
        The path of the JSON file to load, by default "databases/games_database.json"

    Returns
    -------
    games : list of Game instances
        The list of games loaded from the file.
    """

    # Open the file for reading
    with open(filename, "r") as db:
        # Read the JSON data from the file
        json_format = db.read()

     # Parse the JSON data into a list of dictionaries
    game_dicts = json.loads(json_format)

    # Create a list of Game instances from the dictionary data
    games = [game.Game(**j) for j in game_dicts]

    return games
