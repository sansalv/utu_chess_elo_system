import player
import game
import save_and_load as sl
import input_data

import random as rd
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
import os  # For clearing terminal

# Methods of the main() while-loop


def start_tournament():
    # Read tournament names from txt file
    with open("tournament_names.txt", "r") as f:
        tournament_names = f.read().split("\n")[2:]

    # Load old players
    all_players = sl.load_players()

    # ___________________________________
    # Find new players and append them to all_players list
    is_new_players = False
    old_names = [p.name for p in all_players]
    for name in tournament_names:
        # If new player found
        if name not in old_names:
            is_new_players = True

            ans = input(
                f"Is {name} a new player? Abort and correct name if there is a spelling error. (y/abort)\n"
            )
            while ans not in ["y", "abort"]:
                ans = input("Try answering again (y/abort)\n")
            if ans == "abort":
                print("Databases didn't update. Try again.")
                input("\nPress enter to continue.\n")
                return

            # Create new player and append it to all_players
            level = int(
                input(
                    f"What is the starting level of this player? (0=500, 1=1000, 2=1500)\n"
                )
            )
            new_player = player.new_player(name, level)
            all_players.append(new_player)

    if is_new_players:
        # Save all players back into json database
        sl.save_players(all_players)
        print("\nUpdated players to players_database.json successfully.\n")
    # ___________________________________

    # clear_terminal()
    tournament_players = [p for p in all_players if p.name in tournament_names]

    sorted_lists = player.get_tournament_group_lists(tournament_players)

    # Suggest and correct tournament split
    with open("tournament_split.txt", "w") as f:
        print("Suggested tournament split. You can move players.", file=f)
        for group in sorted_lists:
            print("----------------------------", file=f)
            name_elo_list = [(p.name, p.elo) for p in group]
            print(*name_elo_list, sep="\n", file=f)
    print()
    ans = input(
        "Suggested tournament split is now in tournament_split.txt. You can move players.\nAfter this, type continue/abort.\n"
    )
    while ans not in ["continue", "abort"]:
        ans = input("Try answering again (continue/abort)\n")
    if ans == "abort":
        return

    with open("tournament_split.txt", "r") as f:
        tournament_names_elos = f.read().split("\n")[2:]

    # Create beginners, intermediate and experienced groups
    groups = [[], [], []]
    group_index = 0
    for name_elo in tournament_names_elos:
        if name_elo not in ["", "----------------------------"]:
            groups[group_index].append(name_elo)
        else:
            group_index += 1

    print("\n\nGroups in seating orders (random order):\n")
    print("----------------------------")
    # Number of non-zero groups
    n_groups = sum([1 if len(group) != 0 else 0 for group in groups])
    for i in range(n_groups):
        rd.shuffle(groups[i])
        print(f"Group {i}:")
        for name_elo in groups[i]:
            ne = eval(name_elo)
            print(ne[0])
        print("----------------------------")
    input("\nPress enter to continue.")


# _______________________________________________________________________
# Checks if there is some new data to input. Directs into input_tournament() or input_games()
# TODO: Comment and document


def update_from_data():
    new_tournament_files, new_free_games_files = sl.get_new_input_file_lists()
    new_files = new_tournament_files + new_free_games_files

    if len(new_files) == 0:
        print("Everything up to date. No new data files to update.")
        input("\nPress enter to continue.")
        return

    # Sort files by datetime for the input order
    new_files.sort(key=lambda f: dt.datetime.strptime(f.split("_")[0], "%Y-%m-%d"))

    print("New files found:\n")
    print(*new_files, sep="\n")

    ans = input("\nDo you want to update this/these files? (y/n)\n")
    if ans != "y":
        return

    free_games_csv_pairs = game.get_free_games_csv_pairs(new_files)
    free_games_idx = 0

    for f in new_files:
        file_info = f.split("_")[1]
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
        else:
            print(f"\nFile {f} not identified. This file will be skipped.")
            input("\nPress enter to continue.")


# _____________________________________________________________________
# Reset all databases and input all, i.e. reset + update_from_data()


def reset_and_input_all():
    sl.reset_json_database("databases/players_database.json")
    sl.reset_json_database("databases/games_database.json")
    sl.reset_txt_file("databases/inputed_files.txt")
    print()
    update_from_data()


# _____________________________________________________________________
# Data lookup
# TODO: Comment and document


def data_query():
    x = input(
        "Input the name of the player you wish to look up or press enter to go back:\n"
    )

    if x == "":
        return
    players = sl.load_players()
    found = False
    for p in players:
        if p.name == x:
            found = True
            clear_terminal()
            games = sl.load_games()
            player.print_player_games(p, games)
            break
    if found == False:
        input("No player with that name")
        return
    plot = input("\nDo you want a Elo history plot? (y/n)\n")
    if plot == "y":
        p.plot_elo_history()
    return


# _____________________________________________________________________
# Print Elo leaderboard
# TODO: Comment and document


def print_elo_leaderboard():
    players = sl.load_players()
    players = sorted(players, key=lambda h: h.elo, reverse=True)

    i = 1
    # TODO: print("TYLO rating leaderboard (last update: DATE):\n")
    with open("databases/inputed_files.txt", "r") as txt:
        files = txt.read().splitlines()
    date = files[-1].split("_")[0]

    ans = input("Do you want to filter players only by latest update? (y/n)\n")

    clear_terminal()

    if ans == "y":
        players = [p for p in players if p.elo_history[-1][0] == date]
        print(f"TYLO rating leaderboard\n(players filtered by last update {date}):\n")
    else:
        print(f"Overall TYLO rating leaderboard\n(last update: {date}):\n")

    for p in players:
        elo_update = str(p.elo_history[-1][1] - p.elo_history[-2][1])
        if elo_update[:1] != "-":
            elo_update = "+" + elo_update
        if p.elo_history[-1][0] == date:
            print(f"{i}: {p.elo} ({elo_update}) {p.name}")
        else:
            print(f"{i}: {p.elo}       {p.name}")
        i += 1

    plot = input("\nDo you want a leaderboard bar plot? (y/n)\n")
    if plot == "y":
        names = [f"{p.name[0]}. " + p.name.split(" ")[1] for p in reversed(players)]
        elos = [p.elo for p in reversed(players)]
        plt.barh(names, elos)
        plt.grid()
        plt.show()

    plot2 = input("\nDo you want a TYLO rating history plot? (y/n)\n")
    if plot2 == "y":
        for p in players:
            name = f"{p.name[0]}. " + p.name.split(" ")[1]
            dates = [eh[0] for eh in p.elo_history]
            x = [dt.datetime.strptime(d, "%Y-%m-%d").date() for d in dates]
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
            y = [eh[1] for eh in p.elo_history]
            plt.gca().xaxis.set_major_locator(mdates.DayLocator())
            plt.plot(x, y, "-o", label=name)

        plt.legend(bbox_to_anchor=(1.04, 0.5), loc="center left", borderaxespad=0)

        plt.gcf().autofmt_xdate()
        plt.xlabel("Date")
        plt.ylabel("TYLO rating")
        plt.grid()
        # plt.legend()
        plt.show()

    input("\nPress enter to continue.")


def sort_players():
    players = sl.load_players()

    ans = input("How do you want to sort players? (n = number of games)\n")
    clear_terminal()
    if ans == "n":
        players = sorted(players, key=lambda h: h.games_played, reverse=True)
        print("Players sorted by their number of games played:")
        print("games played, name (TYLO rating)\n")
    i = 1
    for p in players:
        print(f"{i}: {p.games_played}, {p.name} ({p.elo})")
        i += 1

    input("\nPress enter to continue.")


def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")  # Clear terminal


# _______________________________________________________________________
# _______________________________________________________________________


def main():
    # TODO: Comment and document

    # 1: Update databases
    # 2: Reset and input all (caution)
    # 3: Look at a profile
    # 4: Print TYLO leaderboard
    # Press enter to exit

    while True:
        # System clears are commented out because different commands work for Linux and Windows
        clear_terminal()
        command = input(
            "Input a command\n\n1: Start new tournament day (do the name list first)\n2: Check for new data\n3: Reset and input all (CAUTION)\n4: Look at a profile\n5: Print TYLO leaderboard\n6: Print sorted players\n\nENTER: Exit\n\n"
        )
        clear_terminal()
        match command:
            case "1":
                start_tournament()
            case "2":
                update_from_data()
            case "3":
                ans = input(
                    "WARNING:\nAre you sure you want to reset (and input) all? (y/n)\n"
                )
                if ans == "y":
                    clear_terminal()
                    reset_and_input_all()
            case "4":
                data_query()
            case "5":
                clear_terminal()
                print_elo_leaderboard()
            case "6":
                sort_players()
            case "":
                exit()
            case _:
                print("Incorrect command")


if __name__ == "__main__":
    main()
