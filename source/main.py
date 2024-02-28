"""
Module containing the UI for menu while loop.
"""

import datetime as dt
import os
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import crypter
import time
import shutil
import io
import zipfile
from pathlib import Path
from tkinter import filedialog
from cryptography.fernet import InvalidToken

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
from tkinter import filedialog, Tk
import io
import zipfile

from tournament_starter import start_tournament


PASSWORD_CHECKER_FILE = Path(__file__).parent / "password_checker.bin"
DECRYPTED_DATA_FOLDER = Path(__file__).parent.parent / "decrypted_data"
ENCRYPTED_DATA_FILE = Path(__file__).parent.parent / "encrypted_data.bin"
GAMES_DATABASE = DECRYPTED_DATA_FOLDER / "games_database.json"
PLAYERS_DATABASE = DECRYPTED_DATA_FOLDER / "players_database.json"
INPUTED_FILES = DECRYPTED_DATA_FOLDER / "inputed_files.txt"


# Input new source files, and update
def input_new_csv_files_and_update_databases():
    """docs"""

    print(
        "File explorer window opened. \n\n"
        "File name insructions:\n\n"
        "The tournament csv file should be name in format:\n"
        "%Y-%m-%d_Beginner/Intermediate/Experienced_Group[+ optional extra].csv\n\n"
        "The free games csv file should be named in format:\n"
        "%Y-%m-%d_Free_Rated_Games - Games/New Players Output.csv\n\n"
    )
    input_more = "y"
    while input_more == "y":
        _input_new_csv()
        input_more = input("Do you want to input more csv files? (y/n)\n")

    update_from_data()


def _input_new_csv():
    try:
        root = Tk()
        root.withdraw()  # Hide the main window
        root.attributes("-topmost", True)  # Bring the root window to the front
        new_file_path_to_input = Path(
            filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        )
        # root.attributes('-topmost', False)  # Set the root window back to normal
    except TypeError:
        return

    if not new_file_path_to_input.is_file():
        print("Invalid file path or file does not exist.")
        # input("\nPress enter to go to menu.")
        return

    if "free_rated" in new_file_path_to_input.name.lower():
        destination_folder = DECRYPTED_DATA_FOLDER / "free_rated_games_data"
    elif "group" in new_file_path_to_input.name.lower():
        destination_folder = DECRYPTED_DATA_FOLDER / "tournament_data"
    else:
        print("Check the selected source file name, and retry!")
        # input("\nPress enter to go to menu.")
        return

    print(f'"{new_file_path_to_input.name}"')
    shutil.copy(
        new_file_path_to_input, destination_folder / new_file_path_to_input.name
    )
    print(
        f"File copy-pasted successfully to source files folder from '{new_file_path_to_input.parent.name}'!\n"
    )


# _______________________________________________________________________


# Check for new data
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

    # Legacy way to handle free games:
    # Free games data consist of two files: the games and new players
    # These are paired up here
    free_games_csv_pairs = game.get_free_games_csv_pairs(new_files)
    free_games_idx = 0

    # Loop through each file and update accordingly
    for f in new_files:
        # Necessary info is in the file names
        file_info = f.split("_")[1]
        file_info_2 = f.split("_")[-1]

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

        elif file_info == "Free" and not (
            file_info_2 == "Games - Games Output.csv"
            or file_info_2 == "Games - New Players Output.csv"
        ):
            input_data.input_free_games(f)
            sl.save_input_source(f)

        # Legacy way to handle free games:
        # If file is a free games file, do input_games. New players are created there, also.
        elif file_info == "Free" and (
            file_info_2 == "Games - Games Output.csv"
            or file_info_2 == "Games - New Players Output.csv"
        ):
            if f.split(" - ")[1] == "Games Output.csv":
                input_data.input_free_games_legacy(free_games_csv_pairs[free_games_idx])
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


# Reset and input all (CAUTION)
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


# Look at a profile
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


# Print TYLO leaderboard
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
    with open(INPUTED_FILES, "r", encoding="utf-8") as txt:
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
        names = []
        for p in reversed(players):
            try:
                names.append(f"{p.name[0]}. " + p.name.split(" ")[1])
            except IndexError:
                names.append(p.name)
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
            try:
                name = f"{p.name[0]}. " + p.name.split(" ")[1]
            except IndexError:
                name = p.name
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


# Print sorted players
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
    ans = input(
        "How do you want to sort players?\n(a = all players for free games table \n n = number of games)\n"
    )
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

    # This is the expected response after decrypting the password checker file.
    response = (
        "Kiitos, että luet koodiamme. Tää meidän salasanasysteemi ei oo kauheen "
        "hyvä mut tarpeeks hyvä tähän tarkotukseen :DDDD."
    )
    while True:
        password = input("Input password:\n")

        try:
            decrypted_file = crypter.decrypt_file(
                password, password_checker_file
            ).decode()
        except InvalidToken:
            print("Incorrect password.")
            continue

        if decrypted_file != response:
            print("Incorrect password")
        else:
            break

    return password


# _______________________________________________________________________


def print_database_status():
    # Check the latest file update date
    with open(INPUTED_FILES, "r", encoding="utf-8") as txt:
        files = txt.read().splitlines()
    try:
        latest_update_date = files[-1].split("_")[0]
    except IndexError:
        latest_update_date = "No update files found"

    # Check number of players in database
    players = sl.load_players()
    n_players = len(players)

    # Check number of games in database
    games = sl.load_games()
    n_games = len(games)

    print(
        f"Date of the latest update file: {latest_update_date}.\n"
        f"Number of players in database: {n_players}.\n"
        f"Number of games in databse: {n_games}.\n"
    )


# _______________________________________________________________________


def clear_terminal():
    # There are different commands to Windows, Mac and Linux to clear terminal
    os.system("cls" if os.name == "nt" else "clear")


# _______________________________________________________________________


def main():
    clear_terminal()
    password = check_password()
    print("Correct password.")
    time.sleep(0.2)
    print('decrypting database from "encrypted_data.bin"...')
    crypter.decrypt_database(password)
    time.sleep(0.2)
    print('database decrypted to "decrypted_data\\.".')
    time.sleep(0.6)
    print("Welcome!")
    time.sleep(1.2)

    while True:
        clear_terminal()

        print("UNIVERSITY HILL CHESS CLUB RANKING SYSTEM")

        print_database_status()

        command = input(
            "Input a command\n\n"
            + "1: Start new tournament day\n"
            + "2: Input data file (.csv) and update databases\n"
            + "3: Check for new data\n"
            + "4: Reset and input all (CAUTION)\n"
            + "5: Look at a profile\n"
            + "6: Print TYLO leaderboard\n"
            + "7: Print sorted players\n\n"
            + "ENTER: Exit\n\n"
        )

        clear_terminal()

        match command:
            case "1":
                start_tournament()
            case "2":
                input_new_csv_files_and_update_databases()
                crypter.encrypt_database(password)
                print(
                    'database encrypted from "decrypted_data\\."... to "encrypted_data.bin".'
                )
                time.sleep(1)
            case "3":
                update_from_data()
                crypter.encrypt_database(password)
                print(
                    'database encrypted from "decrypted_data\\."... to "encrypted_data.bin".'
                )
                time.sleep(1)
            case "4":
                ans = input(
                    "WARNING:\nAre you sure you want to reset (and input) all? (y/n)\n"
                )
                if ans == "y":
                    clear_terminal()
                    reset_and_input_all()
                    crypter.encrypt_database(password)
                    print(
                        'database encrypted from "decrypted_data\\."... to "encrypted_data.bin".'
                    )
                    time.sleep(1)
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
