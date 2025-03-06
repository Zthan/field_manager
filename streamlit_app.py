import streamlit as st
from pybaseball import spraychart, playerid_lookup, statcast_batter
import pandas as pd
import matplotlib.pyplot as plt  # Fixed typo in import

st.title("Field Manager Spraychart Generator")
st.write(
    "This is a simple app. Enter a MLB player's first and last name only, no Jr's or II or anything else. Then select the stadium you want to see their spraychart for.")


options_dict = {
    'generic': 'Generic', 'angels': 'Angels', 'astros': 'Astros', 'athletics': 'Athletics', 'blue_jays': 'Blue Jays',
    'braves': 'Braves', 'brewers': 'Brewers', 'cardinals': 'Cardinals', 'cubs': 'Cubs', 'diamondbacks': 'Diamondbacks',
    'dodgers': 'Dodgers', 'giants': 'Giants', 'indians': 'Guardians', 'mariners': 'Mariners', 'marlins': 'Marlins',
    'mets': 'Mets', 'nationals': 'Nationals', 'orioles': 'Orioles', 'padres': 'Padres', 'phillies': 'Phillies',
    'pirates': 'Pirates', 'rangers': 'Rangers', 'rays': 'Rays', 'red_sox': 'Red Sox', 'reds': 'Reds', 'rockies': 'Rockies',
    'royals': 'Royals', 'tigers': 'Tigers', 'twins': 'Twins', 'white_sox': 'White Sox', 'yankees': 'Yankees'
}

name_first = st.text_input("Enter Player First Name:")
name_last = st.text_input("Enter Player Last Name:")
team_stadium = st.selectbox("Choose a stadium:", list(options_dict.keys()))
team_stadium_display = options_dict.get(team_stadium, team_stadium)

if name_first and name_last:
    lookup_number = playerid_lookup(name_last, name_first, fuzzy=True)
    if not lookup_number.empty:
        hitter = lookup_number['key_mlbam'].iloc[0]
        hitter_name_last = lookup_number['name_last'].iloc[0]
        hitter_name_first = lookup_number['name_first'].iloc[0]
        
        team_stadium_dict = {'angels': 'LAA', 'astros': 'HOU', 'athletics': 'ATH', 'blue_jays': 'TOR', 'braves': 'ATL',
                             'brewers': 'MIL', 'cardinals': 'STL', 'cubs': 'CHC', 'diamondbacks': 'AZ', 'dodgers': 'LAD',
                             'giants': 'SF', 'indians': 'CLE', 'mariners': 'SEA', 'marlins': 'MIA', 'mets': 'NYM',
                             'nationals': 'WSH', 'orioles': 'BAL', 'padres': 'SD', 'phillies': 'PHI', 'pirates': 'PIT',
                             'rangers': 'TEX', 'rays': 'TB', 'red_sox': 'BOS', 'reds': 'CIN', 'rockies': 'COL',
                             'royals': 'KC', 'tigers': 'DET', 'twins': 'MIN', 'white_sox': 'CWS', 'yankees': 'NYY'}

        home_team = team_stadium_dict.get(team_stadium, None)
        chart_title = f"{hitter_name_first} {hitter_name_last} @ {team_stadium_display} Stadium"

        pitch_data = statcast_batter('2024-03-28', '2024-09-30', hitter)
        pitch_data = pitch_data.loc[pitch_data['batter'] == hitter]
        pitch_data = pitch_data.loc[pitch_data['events'].isin(['single', 'double', 'triple', 'home_run'])]

        if home_team:
            pitch_data = pitch_data.loc[pitch_data['home_team'] == home_team]
        
        fig, ax = plt.subplots(figsize=(10, 8))  # Create figure and axis
        spraychart(pitch_data, team_stadium, title=chart_title, ax=ax)  # Pass ax explicitly
        st.pyplot(fig)  # Display the figure
    else:
        st.error("Player not found. Please check the spelling and try again.")


