import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
import numpy as np
from pathlib import Path

# After Player class there are methods involving Player instances


class Player:
    """
    A class representing a chess club player.

    Attributes
    ----------
    name : str
        The name of the player in format "Firstname Lastname".
    elo : int
        The current TYLO rating of the player.
    elo_history : list of tuple
        The player's TYLO rating history, where each tuple represents a date and a TYLO rating.
    games_played : int
        The number of games the player has played.
    """

    def __init__(self, name, elo, elo_history, games_played):
        self.name = name
        self.elo = elo
        self.elo_history = elo_history
        self.games_played = games_played

    def __str__(self):
        return (
            f"{self.name} - TYLO rating: {self.elo} - Games played: {self.games_played}"
        )

    def __repr__(self):
        return f"Player(name='{self.name}', rating={self.rating})"

    # Setter for elo and elo_history
    def update_elo_and_history(self, date, new_elo):
        """
        Update the player's TYLO rating and rating history.

        Parameters
        ----------
        date : str
            The date of the rating update in the format "YYYY-MM-DD".
        new_elo : int
            The new TYLO rating of the player.
        """
        self.elo = new_elo
        self.elo_history.append((date, new_elo))

    def plot_elo_history(self):
        """
        Plot the player's TYLO rating history.
        """
        dates = [eh[0] for eh in self.elo_history]
        x = [dt.datetime.strptime(d, "%Y-%m-%d").date() for d in dates]
        y = [eh[1] for eh in self.elo_history]
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator())
        plt.plot(x, y, "-o")
        plt.xlabel("Date")
        plt.ylabel("TYLO rating")
        plt.gcf().autofmt_xdate()
        plt.show()

    # Method that returns new Elo rating from a SINGLE game
    def calculate_new_elo_single(self, opponent_elo, score):
        """
        Calculates and returns new updated Elo rating from a SINGLE game.

        Parameters
        ----------
        opponent_elo : int or float
            The Elo rating of the opponent in the game.
        score : int or float
            The score obtained by the player in the game (0 for a loss, 0.5 for a draw, and 1 for a win).

        Returns
        -------
        new_elo : int
            The new Elo rating of the player after the game.
        """

        # Define the K-factor from games played. New players get bigger Elo correction jumps.
        if self.games_played <= 10:
            K = 128
        elif self.games_played <= 20:
            K = 64
        else:
            K = 32

        # Calculate expected score of the game
        expected_score = 1 / (1 + 10 ** ((opponent_elo - self.elo) / 400))

        # Calculate new elo rating
        new_elo = self.elo + K * (score - expected_score)

        # Round to the nearest integer
        new_elo = int(new_elo + 0.5)

        return new_elo

    # Method that returns new Elo rating from games list (from whole tournament day)
    def calculate_new_elo_tournament(self, games):
        """
        Calculates and returns new updated Elo rating from games list (from the whole tournament day).

        Parameters
        ----------
        games : list of Game instances
            The list of games played by the player during the tournament day.

        Returns
        -------
        new_elo : int
            The new Elo rating of the player after the tournament day.
        """

        # Define the K-factor from games played. New players get bigger Elo correction jumps.
        if self.games_played <= 10:
            K = 128
        elif self.games_played <= 20:
            K = 64
        else:
            K = 32

        # Calculate the player's score sum of the day and expected score sum of the day
        score_sum = 0
        expected_score_sum = 0
        # Iterate all games of the day
        for g in games:
            # Check if this player played with white or black in each game
            white = False
            black = False
            if self.name == g.white_name:
                white = True
            elif self.name == g.black_name:
                black = True
            else:
                continue  # Not this player's game

            # Increase player's game count
            self.games_played += 1

            # Get player's game score from the white_score
            if white:
                score = g.white_score
                opponent_elo = g.black_elo
            else:
                score = 1 - g.white_score
                opponent_elo = g.white_elo

            # Add the game score to the player's score sum of the day
            score_sum += score

            # Calculate the expected score of the game .
            # This depends on the difference between the player's and opponent's rating
            expected_score = 1 / (1 + 10 ** ((opponent_elo - self.elo) / 400))

            # Add the expected score to the player's expected sum of the day
            expected_score_sum += expected_score

        # Calculate new Elo rating
        new_elo = self.elo + K * (score_sum - expected_score_sum)

        # Round to nearest integer
        new_elo = int(new_elo + 0.5)

        return new_elo


# _______________________________________________________________________

# Methods outside of class:


def new_player(name, level, date):
    """
    This function creates a new instance of the Player class and sets its starting Elo rating
    based on the chosen level of the player.

    Parameters
    ----------
    name : str
        The name of the player, in the format "Firstname Lastname"
    level : int
        The level of the player -
        0 (rating = 500), 1 (rating = 1000), or 2 (rating = 1500)
    date : str
        date when the player was created, in the format "YYYY-MM-DD"

    Returns
    -------
    new_player : Player object
        A new instance of the Player class with the chosen starting Elo rating,
        an initial tuple in the elo_history containing the starting Elo rating and the date when it was set,
        and games_played set to 0.
    """

    if level == 0:  # beginner level
        starting_elo = 500
    elif level == 1:  # intermediate level
        starting_elo = 1000
    elif level == 2:  # experienced level
        starting_elo = 1500

    # Create the new player object with initial elo_history tuple and set the games_played at zero.
    new_player = Player(name, starting_elo, [(date, starting_elo)], 0)

    return new_player


def find_player(players, name):
    """
    Search for a player by name in a list of Player instances.

    Parameters
    ----------
    players : list
        A list of Player instances to search through.
    name : str
        The name of the player to search for.

    Returns
    -------
    player : Player instance
        The Player instance with the matching name.

    Raises
    ------
    ValueError: If no Player instance is found with the given name.
    """
    for player in players:
        if player.name == name:
            return player
    # If no matching player is found, raise an exception with an informative message.
    raise ValueError(f"No player found with name '{name}'")


def print_player_games(p, games):
    print(p)
    print()  # New line
    found = False
    print("    Date       White player             Black player      Player's score\n")
    for g in games:
        if g.white_name == p.name or g.black_name == p.name:
            found = True
            g.print_game(p.name)
    if found == False:
        print("No games found")


def get_players_from_table(file_location: Path):
    """
    Returns the list of players name from tournament table (pandas dataframe) and returns list of strings.

    Parameters
    ----------
    file_location : str
        Location of the table of tournament games. In which Indexes and columns have players names.

    Returns
    -------
    player_list : list
        Player names in list of strings.
    """
    games_table = pd.read_csv(file_location, dtype=str, index_col=0)
    player_list = list(games_table.index)
    return player_list


def get_unique_players_from_games_csv(file_location: Path):
    """
    Returns a list of unique player names from the "White Player" and "Black Player" columns of the CSV file.

    Parameters
    ----------
    file_location : Path
        The path of the CSV file.

    Returns
    -------
    unique_players : list
        A list of unique player names as strings.
    """

    # Read the CSV file into a Pandas DataFrame
    games_df = pd.read_csv(file_location)

    # Get the unique player names from the "White Player" and "Black Player" columns
    unique_players = list(
        set(games_df["White Player"]).union(set(games_df["Black Player"]))
    )

    # Remove any null or empty player names from the list
    unique_players = [player for player in unique_players if player]

    # The old code, just in case, if the new code above doesn't work properly
    """
    unique_players = list(
        np.unique(np.hstack([games_df["White Player"], games_df["Black Player"]]))
    )
    """

    return unique_players


def get_new_players_with_level_from_free_games_csv(file_location: Path):
    """
    Reads free games CSV file and returns list of tuples,
    with player name and starting TYLO rank (0, 1 or 2).
    Eg. [("Elias Ervelä", 1), ("Santeri Salomaa", 2)]
    """

    free_games_csv = pd.read_csv(file_location)
    new_players_table = free_games_csv[
        ["New players", "Starting TYLO (0,1,2)"]
    ].dropna()
    new_players_list = [
        list(new_players_table.iloc[i]) for i in range(len(new_players_table))
    ]

    return new_players_list


def get_new_players_with_level_from_free_games_csv_legacy(file_location):
    """
    This is now legacy method, but kept here to be compatible with old filess.
    Reads free games CSV file and returns list of tuples,
    with player name and starting TYLO rank (0, 1 or 2).
    Eg. [("Elias Ervelä", 1), ("Santeri Salomaa", 2)]

    Parameters
    ----------
    file_location : str
        The path of the CSV file.

    Returns
    -------
    new_players_list : list
        A list of tuples, in the format ("Firstname Lastname", int)
    """
    # Read the CSV file into a Pandas DataFrame
    new_players_table = pd.read_csv(file_location)

    # Create the list
    new_players_list = [
        list(new_players_table.iloc[i]) for i in range(len(new_players_table))
    ]

    return new_players_list


def get_tournament_group_lists(tournament_players):
    """
    Returns a list of groups of tournament players sorted by TYLO rating.

    Parameters
    ----------
    tournament_players : list of Player objects
        A list of player objects representing the tournament players.

    Returns
    -------
    groups : list of lists of Player objects
        A list of lists of player objects representing the tournament groups.
    """

    # Dictionary containing hard-coded group splits based on heuristics:
    # - Prioritise even number of players.
    # - Beginners group have always even number of players.
    # - len(intermediate) >= len(experienced) >= len(beginners)
    # TODO Do some better implementation than hard coding.  :DDD
    hard_coded_group_splits = {
        1: [1],
        2: [2],
        3: [3],
        4: [4],
        5: [5],
        6: [6],
        7: [4, 3],
        8: [4, 4],
        9: [4, 5],
        10: [4, 6],
        11: [6, 5],
        12: [4, 4, 4],
        13: [4, 5, 4],
        14: [4, 6, 4],
        15: [4, 6, 5],
        16: [4, 6, 6],
        17: [6, 6, 5],
        18: [6, 6, 6],
        19: [6, 7, 6],
        20: [6, 8, 6],
        21: [6, 8, 7],
        22: [6, 8, 8],
        23: [6, 9, 8],
        24: [8, 8, 8],
        25: [8, 9, 8],
        26: [8, 10, 8],
        27: [8, 10, 9],
        28: [8, 10, 10],
        29: [8, 11, 10],
        30: [8, 12, 10],
        31: [8, 12, 11],
        32: [8, 12, 12],
        33: [10, 12, 11],
        34: [10, 12, 12],
        35: [10, 13, 12],
        36: [10, 14, 12],
    }

    # Sort players by TYLO rating, lowest first
    sorted_Players_list = sorted(tournament_players, key=lambda p: p.elo)

    # If there are more than 36 players, split them evenly into three groups
    if len(sorted_Players_list) > 36:
        groups = np.array_split(np.array(sorted_Players_list), 3)
        return [list(groups[0]), list(groups[1]), list(groups[2])]

    # Else, use the hard coded splits
    else:
        group_split = hard_coded_group_splits[len(sorted_Players_list)]

        if len(group_split) == 3:
            # Split players into three groups: beginners, intermediate, experienced
            beginners_group = sorted_Players_list[: group_split[0]]
            intermediate_group = sorted_Players_list[
                group_split[0] : group_split[0] + group_split[1]
            ]
            experienced_group = sorted_Players_list[group_split[0] + group_split[1] :]

            groups = [beginners_group, intermediate_group, experienced_group]

        elif len(group_split) == 2:
            # Split players into two groups: beginners and experienced
            beginners_group = sorted_Players_list[: group_split[0]]
            experienced_group = sorted_Players_list[group_split[0] :]

            groups = [beginners_group, experienced_group]

        elif len(group_split) == 1:
            # Only a single group
            groups = [sorted_Players_list]

        return groups
