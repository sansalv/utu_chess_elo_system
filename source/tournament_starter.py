"""Module for start_tournament method."""

import datetime as dt
import os
import random as rd
from pathlib import Path

import player
import save_and_load as sl


def start_tournament() -> None:
    """
    This method starts a tournament by reading player names from a txt file,
    loading old players from a database,
    finding new players and appending them to the old players list,
    suggesting tournament groups splits by reading their Elo ratings,
    and printing the randomized seating orders.
    """
    # Prompt user for the date of the tournament
    date = _input_date()

    # Create temporary text file for name inputting
    tournament_names = _input_names_in_txt_file()

    # Load old players into a list
    all_players = sl.load_players()

    # Append potential new playes to the all_players list, and update database
    should_continue = _append_new_players(date, all_players, tournament_names)
    if not should_continue:
        return

    # Sort tournament players into beginner, intermediate and experienced groups
    tournament_players = [p for p in all_players if p.name in tournament_names]
    sorted_lists = player.get_tournament_group_lists(tournament_players)

    # Suggest, edit and get tournament groups split
    tournament_names_elos = _suggest_and_edit_tournament_split(sorted_lists)

    # Print shuffled seating orders of the tournament groups
    _print_seating_orders(tournament_names_elos)

    input("\nPress enter to get back to main menu.")


def _input_date() -> str:
    """Prompts the user for the date of the tournament.

    Returns
    -------
    date : str
        Date of the tournament in string format YYYY-MM-DD.
    """
    while True:
        date = input(
            "Input date, in the format YYYY-MM-DD (leave empty for present day):\n"
        )
        if date:
            try:
                # Validate input date format
                _ = dt.datetime.strptime(date, "%Y-%m-%d")
                return date
            except ValueError:
                print("Invalid date format. Try again.")
        else:
            current_date = dt.datetime.now()
            date = current_date.strftime("%Y-%m-%d")
            return date


def _input_names_in_txt_file() -> list[str]:
    """Creates a temporary text file for name inputting

    Returns
    -------
    tournament_names : list[str]
        List of the players in string format Firstname Lastname
    """
    # Create a new text file in the current directory
    file_name = "tournament_names.txt"
    with open(file_name, "w") as file:
        content = (
            "Write your names in format Firstname Lastname (check spelling):\n"
            "---------------------------------------------------------------\n"
        )
        file.write(content)

    # Get the absolute path of the created file using pathlib, and start file
    file_path = Path(file_name).resolve()  # OR file_path = os.path.abspath(file_name)
    if os.name == "nt":  # For Windows
        os.startfile(file_path)
    else:  # For Linux
        os.system(f"xdg-open {file_path}")
    input("Press enter when the namelist is ready and the file is saved.")

    # Read tournament names from txt file, delete temp file, and return names
    with open("tournament_names.txt", "r", encoding="utf-8") as f:
        tournament_names = f.read().split("\n")[2:]
        tournament_names = [
            name.strip() for name in tournament_names if name.strip() != ""
        ]
    os.remove(file_name)
    print(f"Temporary file '{file_name}' deleted successfully.")
    return tournament_names


def _append_new_players(date: str, all_players: list, tournament_names: list) -> bool:
    """Checks for new players and append them to all_players list.
    Updates the database, if there are new players.

    Parameters
    ----------
    date : str
        Date of the tournamet in string format YYYY-MM-DD.
    all_players : list[Player]
        List of all previous players where new players are added to.
    tournament_names : list[str]
        List of the tournament player names.


    Returns
    -------
    should_continue : bool
        If True, the program continues. If False, the program aborts.
    """
    # Check for new players and append them to all_players list
    is_new_players = False
    old_names = [p.name for p in all_players]
    for name in tournament_names:
        if name not in old_names:  # If new player is found
            is_new_players = True
            ans = input(
                f"Is {name} a new player? Abort and correct name if there is a spelling error. (y/abort)\n"
            )
            while ans not in ["y", "abort"]:  # If invalid answer, ask again
                ans = input("Try answering again (y/abort)\n")
            if ans == "abort":
                print("Databases didn't update.")
                input("\nPress enter to continue.\n")
                return False

            # Create new player and append it to all_players
            level = int(
                input(
                    f"What is the starting level of this player?\n"
                    "0=500=beginner, 1=1000=intermediate, 2=1500=experienced\n"
                )
            )
            new_player = player.new_player(name, level, date)
            all_players.append(new_player)

    # If new players were found, save all players back into json database
    if is_new_players:
        sl.save_players(all_players)
        print("\nUpdated players to players_database.json successfully.\n")

    return True


def _suggest_and_edit_tournament_split(sorted_lists: list) -> list[tuple]:
    """Suggests a tournament split and let's user to edit the split.
    This is done with temporarily created tournament_split txt file.

    Parameters
    ----------
    sorted_lists : list(list(Player))
        A list of lists of player objects representing the tournament groups.

    Returns
    -------
    tournament_names_elos : list(tuple)
        A list of (player_name, player_elo) tuples.
    """
    file_name = "tournament_split.txt"
    with open(file_name, "w") as f:
        print("Suggested tournament split. You can move players.", file=f)
        for group in sorted_lists:
            print("----------------------------", file=f)
            name_elo_list = [(p.name, p.elo) for p in group]
            print(*name_elo_list, sep="\n", file=f)

    # Get the absolute path of the created file using pathlib, and start file
    file_path = Path(file_name).resolve()  # OR file_path = os.path.abspath(file_name)
    if os.name == "nt":  # For Windows
        os.startfile(file_path)
    else:  # For Linux
        os.system(f"xdg-open {file_path}")

    # Print message to user. The suggested split is at the txt file and it can be manually altered
    ans = input(
        "\nSuggested tournament split is now in tournament_split.txt.\n"
        "You can move players.\nAfter this, save, close and type continue/abort.\n"
    )

    # If invalid answer, ask again
    while ans not in ["continue", "abort"]:
        ans = input("Try answering again (continue/abort)\n")

    if ans == "abort":
        return

    # Read tournament split from txt file, and return name elo tuples
    with open(file_name, "r") as f:
        # tournament_names_elos is a list of the txt file rows
        # (either a player's name and elo or a --- line that splits groups)
        tournament_names_elos = f.read().split("\n")[2:]
        tournament_names_elos = [
            ne.strip() for ne in tournament_names_elos if ne.strip() != ""
        ]
    os.remove(file_name)
    print(f"Temporary file '{file_name}' deleted successfully.")
    return tournament_names_elos


def _print_seating_orders(tournament_names_elos: list[tuple]) -> None:
    """Print final tournament splits where players are shuffled

    Parameters
    ----------
    tournament_names_elos : list(tuple)
        A list of (player_name, player_elo) tuples.
    """
    # Create beginners, intermediate and experienced groups. The index is to track the groups
    groups = [[], [], []]
    group_index = 0

    # Iterate through each row in the txt file
    # Each row is either a player (name and elo) or a group splitting line
    for name_elo in tournament_names_elos:
        if name_elo not in ["", "----------------------------"]:
            groups[group_index].append(name_elo)
        else:
            group_index += 1

    # Start printing the final group splits
    print("\n\nGroups in seating orders (random order):\n")
    print("----------------------------")

    # Print all non-zero groups (if there are only few players there are going to be less than 3 groups)
    n_groups = sum([1 if len(group) != 0 else 0 for group in groups])
    for i in range(n_groups):
        # Print a groups in a random seating order
        rd.shuffle(groups[i])
        print(f"Group {i}:")

        # Print only players names (and not their Elo ratings)
        for name_elo in groups[i]:
            ne = eval(name_elo)
            print(ne[0])

        print("----------------------------")
