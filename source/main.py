"""
Module containing the UI for menu while loop.

Methods of the main() while-loop:

1: Start new tournament day (do the name list first)
2: Check for new data
3: Reset and input all (CAUTION)
4: Look at a profile
5: Print TYLO leaderboard
6: Print sorted players
"""

import datetime as dt
import os
import random as rd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import player
import game
import save_and_load as sl
import input_data
from pathlib import Path
import crypter
import time
from pathlib import Path
from cryptography.fernet import InvalidToken
import shutil
from tkinter import filedialog


PASSWORD_CHECKER_FILE = Path(__file__).parent / "password_checker.bin"
DECRYPTED_DATA_FOLDER = Path(__file__).parent.parent / "decrypted_data"
GAMES_DATABASE = DECRYPTED_DATA_FOLDER / "games_database.json"
PLAYERS_DATABASE = DECRYPTED_DATA_FOLDER / "players_database.json"
INPUTED_FILES = DECRYPTED_DATA_FOLDER / "inputed_files.txt"


# 1: Start new tournament day (do the name list first)
def start_tournament():
    """
    This method starts a tournament by reading player names from a txt file,
    loading old players from a database,
    finding new players and appending them to the old players list,
    suggesting tournament groups splits by reading their Elo ratings,
    and printing the randomized seating orders.

    Returns
    -------
    None
    """
    # Prompt user for the date of the tournament
    date = input("Input date, in the format YYYY-MM-DD:\n")

    # Read tournament names from txt file
    with open("tournament_names.txt", "r") as f:
        tournament_names = f.read().split("\n")[2:]

    # Load old players into a list
    all_players = sl.load_players()

    # Check for new players and append them to all_players list
    is_new_players = False
    old_names = [p.name for p in all_players]
    for name in tournament_names:
        # If new player is found

        if name not in old_names:
            is_new_players = True

            ans = input(
                f"Is {name} a new player? Abort and correct name if there is a spelling error. (y/abort)\n"
            )

            # If invalid answer, ask again
            while ans not in ["y", "abort"]:
                ans = input("Try answering again (y/abort)\n")
                
            if ans == "abort":
                print("Databases didn't update.")
                input("\nPress enter to continue.\n")
                return

            # Create new player and append it to all_players
            level = int(
                input(
                    f"What is the starting level of this player? (0=500, 1=1000, 2=1500)\n"
                )
            )

            new_player = player.new_player(name, level, date)
            all_players.append(new_player)

    # If new players were found, save all players back into json database
    if is_new_players:
        sl.save_players(all_players)
        print("\nUpdated players to players_database.json successfully.\n")

    # tournament_players are the players who are in the tournament
    tournament_players = [p for p in all_players if p.name in tournament_names]

    # Sort tournament players into beginner, intermediate and experienced groups
    sorted_lists = player.get_tournament_group_lists(tournament_players)

    # Suggest and correct tournament split
    with open("tournament_split.txt", "w") as f:
        print("Suggested tournament split. You can move players.", file=f)
        for group in sorted_lists:
            print("----------------------------", file=f)
            name_elo_list = [(p.name, p.elo) for p in group]
            print(*name_elo_list, sep="\n", file=f)
    
    # Print message to user. The suggested split is at the txt file and it can be manually altered
    print()
    ans = input(
        "Suggested tournament split is now in tournament_split.txt. You can move players.\nAfter this, type continue/abort.\n"
    )
    
    # If invalid answer, ask again
    while ans not in ["continue", "abort"]:
        ans = input("Try answering again (continue/abort)\n")
        
    if ans == "abort":
        return

    # Read tournament split from txt file
    with open("tournament_split.txt", "r") as f:
        # tournament_names_elos is a list of the txt file rows
        # (either a player's name and elo or a --- line that splits groups)
        tournament_names_elos = f.read().split("\n")[2:]

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

    input("\nPress enter to continue.")

# _______________________________________________________________________

# 2: Input new source file
def input_new_csv_and_update():
    print(
        "File name insructions:\n\n"
        "The tournament csv file should be name in format:\n"
        "%Y-%m-%d_Beginner/Intermediate/Experienced_Group[+ optional extra].csv\n\n"
        "The free games csv file should be named in format:\n"
        "%Y-%m-%d_Free_Rated_Games - Games/New Players Output.csv\n\n"
    )
    input("\nPress enter open file dialog GUI.")
    try:
        new_file_path_to_input = Path(filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")]))
    except TypeError:
        return

    if not new_file_path_to_input.is_file():
        print("Invalid file path or file does not exist.")
        input("\nPress enter to go to menu.")
        return

    if "Free_Rated" in new_file_path_to_input.name:
        destination_folder = DECRYPTED_DATA_FOLDER / "free_rated_games_data"
    elif "Group" in new_file_path_to_input.name:
        destination_folder = DECRYPTED_DATA_FOLDER / "tournament_data"
    else:
        print("Check the selected source file name, and retry!")
        input("\nPress enter to go to menu.")
        return

    shutil.copy(new_file_path_to_input, destination_folder / new_file_path_to_input.name )
    print(f"File copy-pasted successfully to source files folder '{new_file_path_to_input.parent.name}'!")
    update_from_data()

# _______________________________________________________________________

# 2: Check for new data
def update_from_data():
    """
    This method checks if there is some new data to input.
    Directs into input_tournament() or input_games().

    Returns
    -------
    None
    """
    
    # New files to input
    new_tournament_files, new_free_games_files = sl.get_new_input_file_lists()
    new_files = new_tournament_files + new_free_games_files

    # Check if there are any new files to update
    if len(new_files) == 0:
        print("Everything up to date. No new data files to update.")
        input("\nPress enter to continue.")
        return

    # Sort files by datetime for the input order
    new_files.sort(key=lambda f: dt.datetime.strptime(f.split("_")[0], "%Y-%m-%d"))

    print("New files found:\n")
    print(*new_files, sep="\n")

    # Confirm if user wants to update the new files
    ans = input("\nDo you want to update this/these files? (y/n)\n")
    if ans != "y":
        return

    # Free games data consist of two files: the games and new players
    # These are paired up here
    free_games_csv_pairs = game.get_free_games_csv_pairs(new_files)
    free_games_idx = 0

    # Loop through each file and update accordingly
    for f in new_files:

        # Necessary info is in the file names
        file_info = f.split("_")[1]

        # If file is a tournament file, do input_tournament
        if file_info in [
            "Beginners",
            "Beginners/Intermediate",
            "Intermediate",
            "Intermediate/Experienced",
            "Experienced",
            "Beginners/Intermediate/Experienced",
        ]:
            input_data.input_tournament(source_file=f)
            sl.save_input_source(f)

        # If file is a free games file, do input_games. New players are created there, also.
        elif file_info == "Free":
            if f.split(" - ")[1] == "Games Output.csv":
                input_data.input_games(free_games_csv_pairs[free_games_idx])
                sl.save_input_source(f)
                free_games_idx += 1
            elif f.split(" - ")[1] == "New Players Output.csv":
                sl.save_input_source(f)
                continue
            else:
                print(
                    f"\nFree games file {f} not identified. This file will be skipped."
                )
                input("\nPress enter to continue.")
        
        # Every file should be either tournament or free games file
        else:
            print(f"\nFile {f} not identified. This file will be skipped.")
            input("\nPress enter to continue.")

# _____________________________________________________________________

# 3: Reset and input all (CAUTION)
def reset_and_input_all():
    """
    Reset all databases and input all.
    This consists of reset and update_from_data()

    Returns:
    --------
    None
    """

    # Reset databases
    sl.reset_json_database(PLAYERS_DATABASE)
    sl.reset_json_database(GAMES_DATABASE)
    sl.reset_txt_file(INPUTED_FILES)
    print()

    # Input all
    update_from_data()

# _____________________________________________________________________

# 4: Look at a profile
def data_query():
    """
    Prompts the user to input a player's name to look up, then displays the player's game history
    along with an option to plot their Elo history.

    Returns:
    --------
    None
    """

    # Prompt the user to input the name of the player they want to look up
    x = input(
        "Input the name of the player you wish to look up or press enter to go back (Enter = Exit):\n"
    )

    # If the user pressed enter, exit the function
    if x == "":
        return
    
    # Load the list of players from the database
    players = sl.load_players()

    # Search for the player with the given name
    found = False
    for p in players:
        if p.name == x:
            found = True
            clear_terminal()
            # Load the list of games from the database
            games = sl.load_games()
            # Print the player's game history
            player.print_player_games(p, games)
            break

    # If no player was found with the given name, display an error message and exit the function
    if found == False:
        input("No player with that name")
        return
    
    # Plot the player's Elo history
    plot = input("\nDo you want a Elo history plot? (y/n)\n")
    if plot == "y":
        p.plot_elo_history()

# _____________________________________________________________________

# 5: Print TYLO leaderboard
def print_elo_leaderboard():
    """
    Prints the TYLO rating leaderboard for players and their rating history,
    and shows optional plots of the leaderboard and rating history.

    Returns:
    --------
    None
    """

    # Load players from file and sort by current elo rating
    players = sl.load_players()
    players = sorted(players, key=lambda h: h.elo, reverse=True)

    # Get the last update date from the last updated file
    with open(INPUTED_FILES, "r") as txt:
        files = txt.read().splitlines()
    date = files[-1].split("_")[0]

    # Ask user if they want to filter players only by latest update
    ans = input("Do you want to filter players only by latest update? (y/n)\n")
    clear_terminal()
    if ans == "y":
        # Filter players latest update
        players = [p for p in players if p.elo_history[-1][0] == date]
        print(f"TYLO rating leaderboard\n(players filtered by last update {date}):\n")
    else:
        print(f"Overall TYLO rating leaderboard\n(last update: {date}):\n")

    # Print player name, current Elo rating, and Elo update from last update
    i = 1
    for p in players:
        elo_update = str(p.elo_history[-1][1] - p.elo_history[-2][1])
        if elo_update[:1] != "-":
            elo_update = "+" + elo_update
        if p.elo_history[-1][0] == date:
            print(f"{i}: {p.elo} ({elo_update}) {p.name}")
        else:
            print(f"{i}: {p.elo}       {p.name}")
        i += 1

    # Show a bar plot of the leaderboard if requested
    plot = input("\nDo you want a leaderboard bar plot? (y/n)\n")
    if plot == "y":
        # Extract player names in format F. Lastname and ratings for plotting
        names = [f"{p.name[0]}. " + p.name.split(" ")[1] for p in reversed(players)]
        elos = [p.elo for p in reversed(players)]
        # Create bar plot
        plt.barh(names, elos)
        plt.grid()
        plt.show()

    # Show a Elo rating history plot for each player if requested
    plot2 = input("\nDo you want a TYLO rating history plot? (y/n)\n")
    if plot2 == "y":
        # Plot rating history for each player
        for p in players:
            name = f"{p.name[0]}. " + p.name.split(" ")[1]
            dates = [eh[0] for eh in p.elo_history]
            x = [dt.datetime.strptime(d, "%Y-%m-%d").date() for d in dates]
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
            y = [eh[1] for eh in p.elo_history]
            plt.gca().xaxis.set_major_locator(mdates.DayLocator())
            plt.plot(x, y, "-o", label=name)

        # Add legend to plot
        plt.legend(bbox_to_anchor=(1.04, 0.5), loc="center left", borderaxespad=0)

        plt.gcf().autofmt_xdate()
        plt.xlabel("Date")
        plt.ylabel("TYLO rating")
        plt.grid()
        plt.show()

    input("\nPress enter to continue.")

# _______________________________________________________________________

# 6: Print sorted players
def sort_players():
    """
    Sorts the players by a user-selected criterion and prints the sorted leaderboard.

    Returns
    -------
    None
    """

    # Load the list of players from the database
    players = sl.load_players()

    # Prompt the user to select the criterion for sorting
    ans = input("How do you want to sort players?\n(a = all players for free games table \n n = number of games)\n")
    clear_terminal()

    # Sort the players by the number of games played
    if ans == "a":
        players = sorted(players, key=lambda h: h.games_played, reverse=True)
        for p in players:
            print(p.name)
        input("\nCopy players and press enter.")
        return
    elif ans == "n":
        players = sorted(players, key=lambda h: h.games_played, reverse=True)
        print("Players sorted by their number of games played:")
        print("games played, name (TYLO rating)\n")

    # Print the sorted leaderboard
    i = 1
    for p in players:
        print(f"{i}: {p.games_played}, {p.name} ({p.elo})")
        i += 1

    input("\nPress enter to continue.")

# _______________________________________________________________________

def check_password(password_checker_file: Path = PASSWORD_CHECKER_FILE):
    """
    This function checks the password against a password checker file.
    It asks for a password and decrypts the password checker file with it.
    If it successfully decrypts the file, the password is correct.
    
    Parameters
    ----------
    password_checker_file : Path, optional
        Path to the password checker file. The default is PASSWORD_CHECKER_FILE.
    """
    clear_terminal()
    
    # This is the expected response after decrypting the password checker file.
    response = (
        "Kiitos, että luet koodiamme. Tää meidän salasanasysteemi ei oo kauheen "
        "hyvä mut tarpeeks hyvä tähän tarkotukseen :DDDD."
    )
    while True:
        password = input("Input password:\n")
        clear_terminal()

        try:
            decrypted_file = crypter.decrypt_file(password, password_checker_file)
        except InvalidToken:
            print("Incorrect password.")
            continue

        if decrypted_file != response:
            print("Incorrect password")
        else:
            print("Welcome!")
            time.sleep(1)
            break

# _______________________________________________________________________

def clear_terminal():
    # There are different commands to Windows, Mac and Linux to clear terminal
    os.system("cls" if os.name == "nt" else "clear") 

# _______________________________________________________________________

def main():
    
    check_password()

    while True:

        clear_terminal()

        command = input(
            "Input a command\n\n" +
            "1: Start new tournament day (do the name list first)\n" +
            "2: Input data file (.csv) and update databases\n" +
            "3: Check for new data\n" +
            "4: Reset and input all (CAUTION)\n" +
            "5: Look at a profile\n" +
            "6: Print TYLO leaderboard\n" +
            "7: Print sorted players\n\n" +
            "ENTER: Exit\n\n"
        )

        clear_terminal()

        match command:
            case "1":
                start_tournament()
            case "2":
                input_new_csv_and_update()
            case "3":
                update_from_data()
            case "4":
                ans = input(
                    "WARNING:\nAre you sure you want to reset (and input) all? (y/n)\n"
                )
                if ans == "y":
                    clear_terminal()
                    reset_and_input_all()
            case "5":
                data_query()
            case "6":
                print_elo_leaderboard()
            case "7":
                sort_players()
            case "":
                exit()
            
            case _:
                print("Incorrect command")

if __name__ == "__main__":
    main()
