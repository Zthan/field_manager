import streamlit as st
from pybaseball import spraychart, playerid_lookup
import pandas as pd

# Title and description
st.title("Field Manager Spraychart Generator")
st.write(
    "Choose an MLB player and then select on which stadium you want to see their hits overlayed. "
    "The 'Toggle Only Hits at this Stadium' box will filter out hits that were not hit at the selected stadium. "
    "Year Toggles will turn on or off the hits from that year. "
    "The default data is from Spring Training 2025."
)

# Dictionary for team stadium names
options_dict = {
    'generic': 'Generic', 'angels': 'Angels', 'astros': 'Astros', 'athletics': 'Athletics', 'blue_jays': 'Blue Jays',
    'braves': 'Braves', 'brewers': 'Brewers', 'cardinals': 'Cardinals', 'cubs': 'Cubs', 'diamondbacks': 'Diamondbacks',
    'dodgers': 'Dodgers', 'giants': 'Giants', 'indians': 'Guardians', 'mariners': 'Mariners', 'marlins': 'Marlins',
    'mets': 'Mets', 'nationals': 'Nationals', 'orioles': 'Orioles', 'padres': 'Padres', 'phillies': 'Phillies',
    'pirates': 'Pirates', 'rangers': 'Rangers', 'rays': 'Rays', 'red_sox': 'Red Sox', 'reds': 'Reds', 'rockies': 'Rockies',
    'royals': 'Royals', 'tigers': 'Tigers', 'twins': 'Twins', 'white_sox': 'White Sox', 'yankees': 'Yankees'
}

# Reverse dictionary for team stadium names
options_dict_2 = {'Generic':'generic', 'Angels':'angels', 'Astros':'astros', 'Athletics':'athletics', 'Blue Jays':'blue_jays',
               'Braves':'braves', 'Brewers':'brewers', 'Cardinals':'cardinals', 'Cubs':'cubs', 'Diamondbacks':'diamondbacks',
               'Dodgers':'dodgers', 'Giants':'giants', 'Guardians':'indians', 'Mariners':'mariners', 'Marlins':'marlins',
               'Mets':'mets', 'Nationals':'nationals', 'Orioles':'orioles', 'Padres':'padres', 'Phillies':'phillies',
               'Pirates':'pirates', 'Rangers':'rangers', 'Rays':'rays', 'Red Sox':'red_sox', 'Reds':'reds', 'Rockies':'rockies',
               'Royals':'royals', 'Tigers':'tigers', 'Twins':'twins', 'White Sox':'white_sox', 'Yankees':'yankees'
               }

# List of stadium options
options_list = ['Generic', 'Angels', 'Astros', 'Athletics', 'Blue Jays', 'Braves', 'Brewers', 'Cardinals', 'Cubs', 'Diamondbacks',
                'Dodgers', 'Giants', 'Guardians', 'Mariners', 'Marlins', 'Mets', 'Nationals', 'Orioles', 'Padres', 'Phillies',
                'Pirates', 'Rangers', 'Rays', 'Red Sox', 'Reds', 'Rockies', 'Royals', 'Tigers', 'Twins', 'White Sox', 'Yankees'
                ]

# Load player data
data = pd.read_csv('https://raw.githubusercontent.com/Zthan/field_manager/refs/heads/main/spraychart_player_list.csv')

# Get full names of players
full_names = data.apply(lambda row: f"{row['name_first']} {row['name_last']}", axis=1).tolist()
full_names.sort()
full_names = [s.title() for s in full_names]

# Default player selection
default_index = full_names.index('Bryce Harper')
entered_name = st.selectbox("Pick an MLB Player.", full_names, index=default_index)
name_first = entered_name.split(' ')[0]
name_last = entered_name.split(' ')[1]

# Stadium selection
team_stadium = st.selectbox("Choose a stadium:", options_list)
team_stadium_display = options_dict_2.get(team_stadium, None)

# Checkbox options
away_off = st.checkbox('Only Hits at this Stadium')
year_2024 = st.checkbox('2024')
year_2023 = st.checkbox('2023')
year_2022 = st.checkbox('2022')

# Load pitch data for different years
pitch_data_22 = pd.read_csv('https://raw.githubusercontent.com/Zthan/field_manager/refs/heads/main/pitch_data_2022_spraychart_events.csv')
pitch_data_23 = pd.read_csv('https://raw.githubusercontent.com/Zthan/field_manager/refs/heads/main/pitch_data_2023_spraychart_events.csv')
pitch_data_24 = pd.read_csv('https://raw.githubusercontent.com/Zthan/field_manager/refs/heads/main/pitch_data_2024_spraychart_events.csv')
pitch_data_25 = pd.read_csv('https://raw.githubusercontent.com/Zthan/field_manager/refs/heads/main/pitch_data_2025_spraychart_events.csv')
# experimenting with adjusting hc_y data to see if I can fix some of the homerun dots.  Apparently the stadium images have some adjustments on them
#pitch_data_24["hc_y"] = pitch_data_24['hc_y'] - 10

# If player name is entered
if name_first and name_last:
    lookup_number = playerid_lookup(name_last, name_first, fuzzy=True)
    if not lookup_number.empty:
        hitter = lookup_number['key_mlbam'].iloc[0]
        hitter_name_last = lookup_number['name_last'].iloc[0]
        hitter_name_first = lookup_number['name_first'].iloc[0]
        
        # Dictionary for home team codes
        team_stadium_dict = {'angels': 'LAA', 'astros': 'HOU', 'athletics': 'ATH', 'blue_jays': 'TOR', 'braves': 'ATL',
                             'brewers': 'MIL', 'cardinals': 'STL', 'cubs': 'CHC', 'diamondbacks': 'AZ', 'dodgers': 'LAD',
                             'giants': 'SF', 'indians': 'CLE', 'mariners': 'SEA', 'marlins': 'MIA', 'mets': 'NYM',
                             'nationals': 'WSH', 'orioles': 'BAL', 'padres': 'SD', 'phillies': 'PHI', 'pirates': 'PIT',
                             'rangers': 'TEX', 'rays': 'TB', 'red_sox': 'BOS', 'reds': 'CIN', 'rockies': 'COL',
                             'royals': 'KC', 'tigers': 'DET', 'twins': 'MIN', 'white_sox': 'CWS', 'yankees': 'NYY'}

        # Get home team code
        home_team = team_stadium_dict.get(team_stadium_display, None)
        chart_title = f"{hitter_name_first} {hitter_name_last} @ {team_stadium_display} Stadium"

        # Combine pitch data based on year toggles
        pitch_data = pitch_data_25
        if year_2022:
            pitch_data = pd.concat([pitch_data, pitch_data_22])
        if year_2023:
            pitch_data = pd.concat([pitch_data, pitch_data_23])
        if year_2024:
            pitch_data = pd.concat([pitch_data, pitch_data_24])

        # Filter pitch data for selected player
        pitch_data = pitch_data.loc[pitch_data['batter'].isin([hitter])]

        # Filter pitch data for selected stadium
        if home_team:
            if away_off:
                pitch_data = pitch_data.loc[pitch_data['home_team'] == home_team]

        # Generate spray chart
        spray_img = spraychart(pitch_data, team_stadium_display, title=chart_title, width=800, height=800)
        
        # Display spray chart
        if st.button("Let's go already!"):
            st.pyplot(spray_img.figure)
    else:
        st.error("Player not found. Please check the spelling and try again.")



