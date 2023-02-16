import pandas as pd    
from main import from_table_to_games_list
from main import get_players_from_table

file_location = r"C:\Users\elias\Documents\VS Code projects\UTU_chess_rating_system\utu_chess_rating_system\tournament_data\2023-02-15_Beginners_Group - csv out.csv"
games_table = pd.read_csv(file_location, dtype=str, index_col=0)

games = from_table_to_games_list(games_table, verbose=False)
#print(games)


players = get_players_from_table(games_table)
print(players)