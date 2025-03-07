import streamlit as st
from pybaseball import spraychart, playerid_lookup, statcast_batter
import pandas as pd
import matplotlib.pyplot as plt
from pybaseball import plotting
from PIL import Image, ImageDraw
import io

st.title("Field Manager Spraychart Generator")
st.write(
    "This is a simple app. Enter a MLB player's first and last name only, no Jr's or II or anything else. Then select the stadium you want to see their spraychart for."
    "The 'Toggle All Hits' toggle will turn all hits for a player on and off.  Currently no legend for hits, but if you toggle all hits on, colors are as follows:"
    "  \n  Single - Blue"
    "  \n  Double - Green"
    "  \n  Triple - Red"
    "  \n  Home Run - Orange"
    "  \n  So you can toggle all hits on to see what something is if there aren't very many hits in a stadium."
)

options_dict = {
    'generic': 'Generic', 'angels': 'Angels', 'astros': 'Astros', 'athletics': 'Athletics', 'blue_jays': 'Blue Jays',
    'braves': 'Braves', 'brewers': 'Brewers', 'cardinals': 'Cardinals', 'cubs': 'Cubs', 'diamondbacks': 'Diamondbacks',
    'dodgers': 'Dodgers', 'giants': 'Giants', 'indians': 'Guardians', 'mariners': 'Mariners', 'marlins': 'Marlins',
    'mets': 'Mets', 'nationals': 'Nationals', 'orioles': 'Orioles', 'padres': 'Padres', 'phillies': 'Phillies',
    'pirates': 'Pirates', 'rangers': 'Rangers', 'rays': 'Rays', 'red_sox': 'Red Sox', 'reds': 'Reds', 'rockies': 'Rockies',
    'royals': 'Royals', 'tigers': 'Tigers', 'twins': 'Twins', 'white_sox': 'White Sox', 'yankees': 'Yankees'
}


#options_dict_2 = dict([(value, key) for key, value in options_dict.items()])
options_dict_2 = {'Generic':'generic', 'Angels':'angels', 'Astros':'astros', 'Athletics':'athletics', 'Blue Jays':'blue_jays',
               'Braves':'braves', 'Brewers':'brewers', 'Cardinals':'cardinals', 'Cubs':'cubs', 'Diamondbacks':'diamondbacks',
               'Dodgers':'dodgers', 'Giants':'giants', 'Guardians':'indians', 'Mariners':'mariners', 'Marlins':'marlins',
               'Mets':'mets', 'Nationals':'nationals', 'Orioles':'orioles', 'Padres':'padres', 'Phillies':'phillies',
               'Pirates':'pirates', 'Rangers':'rangers', 'Rays':'rays', 'Red Sox':'red_sox', 'Reds':'reds', 'Rockies':'rockies',
               'Royals':'royals', 'Tigers':'tigers', 'Twins':'twins', 'White Sox':'white_sox', 'Yankees':'yankees'
               }
#options_list = ['Generic', 'Angels', 'Astros', 'Athletics', 'Yankees']
#options_list = list(options_dict.values())
options_list = ['Generic', 'Angels', 'Astros', 'Athletics', 'Blue Jays', 'Braves', 'Brewers', 'Cardinals', 'Cubs', 'Diamondbacks',
                'Dodgers', 'Giants', 'Guardians', 'Mariners', 'Marlins', 'Mets', 'Nationals', 'Orioles', 'Padres', 'Phillies',
                'Pirates', 'Rangers', 'Rays', 'Red Sox', 'Reds', 'Rockies', 'Royals', 'Tigers', 'Twins', 'White Sox', 'Yankees'
                ]
name_first = st.text_input("Enter Player First Name:")
name_last = st.text_input("Enter Player Last Name:")
team_stadium = st.selectbox("Choose a stadium:", options_list)
team_stadium_display = options_dict_2.get(team_stadium, None)
away_off = st.checkbox('Toggle All Hits')

if name_first and name_last:
    lookup_number = playerid_lookup(name_last, name_first, fuzzy=True)
    if not lookup_number.empty:
        hitter = lookup_number['key_mlbam'].iloc[0]
        hitter_name_last = lookup_number['name_last'].iloc[0]
        hitter_name_first = lookup_number['name_first'].iloc[0]
        
        team_stadium_dict = {'angels': 'LAA', 'astros': 'HOU', 'athletics': 'OAK', 'blue_jays': 'TOR', 'braves': 'ATL',
                             'brewers': 'MIL', 'cardinals': 'STL', 'cubs': 'CHC', 'diamondbacks': 'AZ', 'dodgers': 'LAD',
                             'giants': 'SF', 'indians': 'CLE', 'mariners': 'SEA', 'marlins': 'MIA', 'mets': 'NYM',
                             'nationals': 'WSH', 'orioles': 'BAL', 'padres': 'SD', 'phillies': 'PHI', 'pirates': 'PIT',
                             'rangers': 'TEX', 'rays': 'TB', 'red_sox': 'BOS', 'reds': 'CIN', 'rockies': 'COL',
                             'royals': 'KC', 'tigers': 'DET', 'twins': 'MIN', 'white_sox': 'CWS', 'yankees': 'NYY'}
        
        team_stadium_dict_2025 = {'angels': 'LAA', 'astros': 'HOU', 'athletics': 'ATH', 'blue_jays': 'TOR', 'braves': 'ATL',
                             'brewers': 'MIL', 'cardinals': 'STL', 'cubs': 'CHC', 'diamondbacks': 'AZ', 'dodgers': 'LAD',
                             'giants': 'SF', 'indians': 'CLE', 'mariners': 'SEA', 'marlins': 'MIA', 'mets': 'NYM',
                             'nationals': 'WSH', 'orioles': 'BAL', 'padres': 'SD', 'phillies': 'PHI', 'pirates': 'PIT',
                             'rangers': 'TEX', 'rays': 'TB', 'red_sox': 'BOS', 'reds': 'CIN', 'rockies': 'COL',
                             'royals': 'KC', 'tigers': 'DET', 'twins': 'MIN', 'white_sox': 'CWS', 'yankees': 'NYY'}

        home_team = team_stadium_dict.get(team_stadium_display, None)
        chart_title = f"{hitter_name_first} {hitter_name_last} @ {team_stadium_display} Stadium"

        pitch_data = statcast_batter('2024-03-28', '2024-09-30', hitter)
        pitch_data = pitch_data.loc[pitch_data['batter'] == hitter]
        pitch_data = pitch_data.loc[pitch_data['events'].isin(['single', 'double', 'triple', 'home_run'])]
        pitch_data.sort_values('events')

        if home_team:
            if away_off == False:
                pitch_data = pitch_data.loc[pitch_data['home_team'] == home_team]
        img = Image.new('RGB', (800, 800), 'white')
        draw = ImageDraw.Draw(img)


        
        spray_img = spraychart(pitch_data, team_stadium_display, title=chart_title, width=800, height=800)  # Get spray chart image
        
        buffer = io.BytesIO()
        spray_img.figure.savefig(buffer, format='png')
        buffer.seek(0)
        overlay = Image.open(buffer)
        img.paste(overlay, (0, 0), overlay)
        
        st.image(img, caption=chart_title, use_container_width=True)
        #st.pyplot(spray_img)
    else:
        st.error("Player not found. Please check the spelling and try again.")


