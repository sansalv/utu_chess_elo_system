import save_and_load as sl
import player
import game
from pathlib import Path

"""
Library for data input methods:

input_tournament()
input_games()
"""


DECRYPTED_DATA_FOLDER = Path(__file__).parent.parent / "decrypted_data"
TOURNAMENT_DATA_FOLDER = DECRYPTED_DATA_FOLDER / "tournament_data"
FREE_RATED_GAMES_DATA_FOLDER = DECRYPTED_DATA_FOLDER / "free_rated_games_data"


# TODO: Comment rest of this properly
# Tournament data input. Creates games and players from csv data and updated databases.
def input_tournament(source_file: str, tournament_data_folder: Path = TOURNAMENT_DATA_FOLDER):
    print(f"\nInput tournament from file {source_file} started.")

    file_location = tournament_data_folder / source_file
    date = source_file.split("_")[0]
    
    group_info = source_file.split("_")[1]
    if group_info == "Beginners":
        level = 0
    elif group_info == "Intermediate":
        level = 1
    elif group_info == "Experienced":
        level = 2
    else:
        print(
            f"Tournament file '{source_file}' with group identifier '{group_info}' not identified."
        )
        ans = input(
            f"Input manually the level of '{group_info}'\n(0=500=Beginner, 1=1000=Intermediate, 2=1500=Experienced, abort=abort)\n"
        )
        if ans == "abort":
            print("Aborted.")
            return
        else:
            level = int(ans)

    # Load old players from database
    all_players = (
        sl.load_players()
    )  # After this old players but later also new players will be appended
    # Filter to tournament players
    tournament_player_names = player.get_players_from_table(file_location)

    # ___________________________________
    # Create new players that were late and therefore weren't created at start_tournament() method
    is_new_players = False
    old_names = [p.name for p in all_players]
    new_players = []
    for name in tournament_player_names:
        if name not in old_names:
            is_new_players = True
            new_player = player.new_player(name, level, date)
            new_players.append(new_player)
            all_players.append(new_player)

    if is_new_players:
        print(f"All new players:\n")
        print(*[(p.name, p.elo) for p in new_players], sep="\n")
    # ___________________________________
    # Filter all players to tournament players
    tournament_players = [p for p in all_players if p.name in tournament_player_names]
    # ___________________________________
    # csv to list of Game instances and save games to json database
    raw_game_list = game.from_table_to_games_list(file_location)
    games = game.game_lists_to_game_instances(
        date, raw_game_list, tournament_players, source_file
    )
    sl.save_new_games(games)
    print("\nSaved games to game_database.json successfully.")

    # ___________________________________
    # Calculate and update Elos and Elo histories
    for p in tournament_players:
        new_elo = p.calculate_new_elo_tournament(games)
        p.update_elo_and_history(date, new_elo)

    # Save all players back into json database
    sl.save_players(all_players)
    print("Updated players to players_database.json successfully.")
    input("\nPress enter to continue.")


def input_games(
    free_games_csv_pair: list | tuple,
    free_rated_games_data_folder: Path = FREE_RATED_GAMES_DATA_FOLDER,
):
    source_file = free_games_csv_pair[0]
    source_file_location = free_rated_games_data_folder / source_file
    new_players_file = free_games_csv_pair[1]
    new_players_file_location = free_rated_games_data_folder/ new_players_file

    # ___________________________________
    # Info of the free rated games

    print(f"\nInput free rated games from file {source_file} started.")
    date = source_file.split("_")[0]
    # ___________________________________

    # Load old players from database
    all_players = (
        sl.load_players()
    )  # After this old players but later also new players will be appended
    # ___________________________________
    # Create new players:

    new_player_names_with_level = player.get_new_players_with_level_from_games_csv(
        new_players_file_location
    )

    print("\nNew players:")
    for name_level in new_player_names_with_level:
        name = name_level[0]
        level = name_level[1]
        print(f"{name}, starting level: {level}")
        all_players.append(player.new_player(name, level, date))
    # ___________________________________

    # Filter all players to present players
    present_player_names = player.get_unique_players_from_games_csv(
        source_file_location
    )
    present_players = [p for p in all_players if p.name in present_player_names]

    # csv to list of Game instances and save games to json database
    raw_game_list = game.from_games_csv_to_games_list(source_file_location)
    games = game.game_lists_to_game_instances(
        date, raw_game_list, present_players, source_file
    )
    sl.save_new_games(games)
    print("\nSaved games to game_database.json successfully.")

    # Calculate and update Elos and Elo histories
    for p in present_players:
        new_elo = p.calculate_new_elo_tournament(games)
        p.update_elo_and_history(date, new_elo)

    # Save all players back into json database
    sl.save_players(all_players)
    print("Updated players to players_database.json successfully.")
    input("\nPress enter to continue.")
