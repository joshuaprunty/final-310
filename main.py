import requests
import pandas as pd
import os
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from colorama import Style
# import json

# Pandas setting to turn off truncated output
pd.set_option('display.max_rows', None)

# ANSI color codes dictionary for each team
team_colors = {
    'ATL': '\033[31m',  # Red
    'BOS': '\033[32m',  # Green
    'BKN': '\033[30m',  # Black
    'CHA': '\033[34m',  # Blue
    'CHI': '\033[31m',  # Red
    'CLE': '\033[33m',  # Yellow
    'DAL': '\033[34m',  # Blue
    'DEN': '\033[36m',  # Cyan
    'DET': '\033[31m',  # Red
    'GSW': '\033[33m',  # Yellow
    'HOU': '\033[31m',  # Red
    'IND': '\033[34m',  # Blue
    'LAC': '\033[31m',  # Red
    'LAL': '\033[35m',  # Purple
    'MEM': '\033[34m',  # Blue
    'MIA': '\033[31m',  # Red
    'MIL': '\033[32m',  # Green
    'MIN': '\033[34m',  # Blue
    'NOP': '\033[34m',  # Blue
    'NYK': '\033[33m',  # Yellow
    'OKC': '\033[34m',  # Blue
    'ORL': '\033[34m',  # Blue
    'PHI': '\033[34m',  # Blue
    'PHX': '\033[31m',  # Red
    'POR': '\033[31m',  # Red
    'SAC': '\033[35m',  # Purple
    'SAS': '\033[30m',  # Black
    'TOR': '\033[31m',  # Red
    'UTA': '\033[32m',  # Green
    'WAS': '\033[31m'   # Red
}

# Base URL for PrizePicks API
pp_props_url = (
    "https://api.prizepicks.com/projections?league_id=7&per_page=250&single_stat=true"
)

# Headers for the request
headers = {
    "Connection": "keep-alive",
    "Accept": "application/json; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    "Access-Control-Allow-Credentials": "true",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Referer": "https://app.prizepicks.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
}

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

# Create a pandas DataFrame for formatted output
df = pd.DataFrame(data)

# Main loop for input
while True:
  # Print unique team names
  unique_teams = df['Team'].unique()
  #
  print('\n')
  print(Style.BRIGHT + 'Available teams:')
  print('-' * 50)
  for team in unique_teams:
      print(team_colors[team] + team + '\033[0m')
  #
  print('\n')

  # Get team input
  while True:
      # Autocomplete input from prompt_toolkit
      team_completer = WordCompleter(unique_teams.tolist(), ignore_case=True)
      team_name = prompt("Enter a team name: ", completer=team_completer)
      if team_name in unique_teams:
          print('\n')
          break
      # Invalid input, retry
      else:
          print("Error: Team not found. Please try again.")

  # Print unique player names for the selected team
  team_players = df[df['Team'] == team_name]['Player'].unique()
  #
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