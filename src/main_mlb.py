# Imports
import requests
import pandas as pd
import os
# User Interface Imports
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from colorama import Style
# Local Imports
from lib.mlb_colors import mlb_team_colors
from lib.apiconfig_mlb import pp_props_url, headers

# Call the API Get Request
response = requests.get(url=pp_props_url, headers=headers).json()

# Map player IDs to respective information
players = {}
for d in response["included"]:
  players[d["id"]] = d["attributes"]

# Extract prop data (Player, Pos, Team, Stat, Line)
data = []
for d in response['data']:
  atts = d['attributes']
  data.append({
      'Player': players[d['relationships']['new_player']['data']['id']]['name'],
      'Pos': players[d['relationships']['new_player']['data']['id']]['position'],
      'Team': atts['description'],
      'Stat': atts['stat_type'], 
      'Line': atts['line_score']      
  })

# Create pandas DataFrame, disable truncation
pd.set_option('display.max_rows', None)
df = pd.DataFrame(data)

# Main loop for input
while True:
  # Print unique team names
  unique_teams = [team for team in df['Team'].unique() if '/' not in team]
  
  print('\n')
  print(Style.BRIGHT + 'Available teams:')
  print('-' * 50)

  for team in unique_teams:
      print(mlb_team_colors[team] + team + '\033[0m')
  
  print('\n')

  # Get team input
  while True:
      # Autocomplete input from prompt_toolkit
      team_completer = WordCompleter(unique_teams, ignore_case=True)
      team_name = prompt("Enter a team name: ", completer=team_completer)
      if team_name in unique_teams:
          print('\n')
          break
      
      # Invalid input, retry
      else:
          print("Error: Team not found. Please try again.")

  # Print unique player names for the selected team
  team_players = df[df['Team'] == team_name]['Player'].unique()
  
  print(Style.BRIGHT + 'Available players for team', team_name, ':')
  print('-' * 50)
  for player in team_players:
      print(player)
  print('\n')

  # Get player input
  while True:
      # Autocomplete input from prompt_toolkit
      player_completer = WordCompleter(team_players.tolist(), ignore_case=True)
      player_name = prompt("Enter a player name: ", completer=player_completer)
      
      if player_name in team_players:
          print('\n')
          break
      # Invalid input, retry
      else:
          print("Error: Player not found. Please try again.")

  # Print rows where player field matches the input
  print('Available lines for', player_name)
  print('=' * 50)
  print(df[(df['Player'] == player_name) & (df['Team'] == team_name)])
  print('=' * 50)
  print('\n')

  # Ask user if they want to continue searching
  continue_search = input("Would you like to perform another search? (Y/N): \n")
  # Clear the terminal
  os.system('clear')
  # Quit if user selects No
  if continue_search.lower() != 'y':
      break