from termcolor import colored
import player
import pandas as pd
from pathlib import Path

# After the Game class there are methods involving Game instances

class Game:
    """
    A class representing a chess club game.

    Attributes
    ----------
    date : str
        The date of the game, in the format "YYYY-MM-DD"
    white_name : str
        The name of the player with white pieces, in the format "Firstname Lastname".
    white_elo : int
        The rating of the player with white pieces.
    black_name : 
        The name of the player with black pieces, in the format "Firstname Lastname".
    black_elo : int
        The rating of the player with black pieces.
    white_score : int
        The score of the white player, e.g. 0-1 game score would be 0 here.
    source_file : str
        The source file path.
    """
    def __init__(
        self,
        date,
        white_name,
        white_elo,
        black_name,
        black_elo,
        white_score,
        source_file,
    ):
        self.date = date
        self.white_name = white_name
        self.black_name = black_name
        self.white_elo = white_elo
        self.black_elo = black_elo
        self.white_score = white_score
        self.source_file = source_file

    def __str__(self):
        return f"[{self.date}] {self.white_name} ({self.white_elo}) {self.black_name} ({self.black_elo})"

    def __repr__(self):
        return f"Game(w='{self.white_name}', b={self.black_name}, w_score={self.white_score})"

    def print_game(self, name):
        """
        Print's one game's result personized to a one player.

        Parameters
        ----------
        name : str
            The name of the player, in the format "Firstname Lastname".

        Returns
        -------
        None

        Raises
        ------
        ValueError: If player is not found from his own game for some reason.
        """

        # Check if the player was 
        print(self, end=" ")
        if (name == self.white_name and self.white_score == 1) or (
            name == self.black_name and self.white_score == 0
        ):
            print(colored("Victory", "yellow"))
        elif self.white_score == 0.5:
            print(colored("Draw", "light_blue"))
        elif (name == self.white_name and self.white_score == 0) or (
            name == self.black_name and self.white_score == 1
        ):
            print(colored("Defeat", "red"))
        else:
            raise ValueError(f"Player '{name}' not found from his game:\n" +
                             f"Game(w='{self.white_name}', b={self.black_name}, w_score={self.white_score})")


# _______________________________________________________________________
# Methods to convert tournament .csv to games list:

#-------
def from_table_to_games_list(file_location, verbose=False):
    """
    Turns tournament game table (csv) in to list of games in format [white_name, black_name, white_result].

    Parameters
    ----------
    file_location : str
        Location of the table of tournament games. In which Indexes and columns have players names, and in the cells there is info of who won. Eg. ww=white win, bl=black lose, bd=black draw.
    verbose : bool
        If True, print table and games_list.

    Returns
    -------
    games_list : list of [str, str, float]
    """
    # Read the table from file_location
    games_table = pd.read_csv(file_location, dtype=str, index_col=0)

    if verbose:
        print("Table: \n", games_table)

    # Get players names from tables index and columns (they should be the same).
    games_table_index = games_table.index
    games_table_columns = games_table.columns

    # Change table to format:
    # [white_name, black_name, white_result]
    # Goes through only the upper triangle in the table.
    games_list = []
    for i in range(len(games_table_index)):
        for j in range(i + 1, len(games_table_columns)):
            # Names of players from index and columns
            ind = games_table_index[i]
            col = games_table_columns[j]

            # Reads the cell and appends the game to the games_list in appropriate form.
            # ww=white win, wt=white tie, wl=white loss, bw=black win, bt=black tie, bl=black lose
            if games_table.loc[ind, col] == "ww":
                games_list.append([str(ind), str(col), 1.0])
            elif games_table.loc[ind, col] == "wd":
                games_list.append([str(ind), str(col), 0.5])
            elif games_table.loc[ind, col] == "wl":
                games_list.append([str(ind), str(col), 0.0])

            elif games_table.loc[ind, col] == "bw":
                games_list.append([str(col), str(ind), 0.0])
            elif games_table.loc[ind, col] == "bd":
                games_list.append([str(col), str(ind), 0.5])
            elif games_table.loc[ind, col] == "bl":
                games_list.append([str(col), str(ind), 1.0])

    if verbose:
        print("List of games:")
        for i in games_list:
            print(i)

    return games_list


def from_games_csv_to_games_list(file_location: Path):
    """
    Parameters
    ----------
    file_location : Path
        File location path of the file.

    Returns
    -------
    List of games in format [White Player, Black Player, White result]
    """
    free_games = pd.read_csv(file_location)
    free_games_list = []
    for i in range(len(free_games)):
        l = list(free_games[['White Player', 'Black Player', 'White Score']].iloc[i])
        # white result datatype from numpy.int64 to float
        l[2] = float(l[2])
        free_games_list.append(l)
    return free_games_list


def game_lists_to_game_instances(date, raw_games_list, players, source_file):
    """
    Turns raw list of [white_name, black_name, white_result] elements to list of game instances.
    The raw list of games comes from either from_table_to_games_list(...) or from_games_csv_to_games_list(...).

    Parameters
    ----------
    date : str
        In format yyyy-mm-dd.
    raw_games_list : list of [str, str, float]
    players : list of Player instances
    source_file : str

    Returns
    -------
    games : list of Game instances
    """
    games = []
    for g in raw_games_list:
        w = player.find_player(players, g[0])
        b = player.find_player(players, g[1])
        g = Game(date, g[0], w.elo, g[1], b.elo, g[2], source_file)
        games.append(g)
    return games


# Get free games pairs
def get_free_games_csv_pairs(
    new_files,
):  # new_files is a sorted list (by datetime) of csv files
    # Filter only free games data (others are tournaments)
    # This will leave games and new players
    free_games = [f for f in new_files if (f.split("_")[1] == "Free") and (f.split("_")[-1] == 'Games - Games Output.csv' or f.split("_")[-1] == 'Games - New Players Output.csv')]
    # Free games csv pairs will be in the list free_games_with_new_players
    n_free_games = int(len(free_games) / 2)
    free_games_with_new_players = [[None, None] for i in range(n_free_games)]

    new_players_files = []
    i = 0
    try:
        for f in free_games:
            t = f.split(" - ")[1]
            if t == "Games Output.csv":
                free_games_with_new_players[i][0] = f
                i += 1
            elif t == "New Players Output.csv":
                new_players_files.append(f)
            else:
                print(
                    f"\nFile {f} not identified. This file will be skipped. Press enter to continue."
                )
                input()
    except Exception as exc:
        print(
            f"Error while trying to pair free games csv files: {exc}. Check that you have: inputted "
            "the output sheets (not table sheets), and that the New Players Output.csv file is also inputted (even if it is empty)."
        )
        raise exc

    # Pair the new players data to the free games data

    # Iterate free games files
    for f_pair in free_games_with_new_players:
        # Free games date
        f_pair_date = f_pair[0].split("_")[0]
        # Find matching date from new_players_files
        for new_players_file in new_players_files:
            new_players_file_date = new_players_file.split("_")[0]
            # If the date matches, make the pair
            if f_pair_date == new_players_file_date:
                f_pair[1] = new_players_file

    # Check that every entry has a pair
    for f_pair in free_games_with_new_players:
        if f_pair[0] == None or f_pair[1] == None:
            raise Exception(
                f"Free games name ERROR: free games csv entry {f_pair} is not correct format. Check data names."
            )

    return free_games_with_new_players
