import streamlit as st
from pybaseball import spraychart
from pybaseball import playerid_lookup
from pybaseball import statcast_batter
import pandas as pd


st.title("Field Manager Spraychart Generator")
st.write(
    "This is a simple app. Enter a MLB players first and last name only, no jr's or II or anything else.  Then select the stadium you want to see their spraychart for."
)
options_dict = {'generic':'Generic', 'angels':'Angels', 'astros':'Astros', 'athletics':'Athletics', 'blue_jays':'Blue Jays', 'braves':'Braves', 'brewers':'Brewers', 'cardinals':'Cardinals', 'cubs':'Cubs', 'diamondbacks':'Diamondbacks', 'dodgers':'Dodgers', 'giants':'Giants', 'indians':'Guardians', 'mariners':'Mariners', 'marlins':'Marlins', 'mets':'Mets', 'nationals':'Nationals', 'orioles':'Orioles', 'padres':'Padres', 'phillies':'Phillies', 'pirates':'Pirates', 'rangers':'Rangers', 'rays':'Rays', 'red_sox':'Red Sox', 'reds':'Reds', 'rockies':'Rockies', 'royals':'Royals', 'tigers':'Tigers', 'twins':'Twins', 'white_sox':'White Sox', 'yankees':'Yankees'}




name_first = st.text_input("Enter Player First Name:")
name_last = st.text_input("Enter Player Last Name:")
team_stadium = st.selectbox("Choose a stadium:", list(options_dict.keys()))
team_stadium_display = team_stadium

#entered_name = 'Jose Altuve'
#name_first = entered_name.split(' ')[0]
#name_last = entered_name.split(' ')[1]


if team_stadium == 'indians':
    team_stadium_display = 'Guardians'
else:
    pass


# make year selecteable from list eventually?
#entered_name.split(' ')

print(name_first)
print(name_last)
lookup_number = playerid_lookup(name_last, name_first, fuzzy=True)
hitter = lookup_number['key_mlbam'].iloc[0]
print(hitter)
hitter_name_last = lookup_number['name_last'].iloc[0]
hitter_name_first = lookup_number['name_first'].iloc[0]

#chart_title = '%s %s @ %s stadium' % (hitter_name_first,  hitter_name_last, team_stadium)

team_stadium_dict = {'angels': 'LAA', 'astros': 'HOU', 'athletics': 'ATH', 'blue_jays': 'TOR', 'braves': 'ATL', 'brewers': 'MIL',
                     'cardinals': 'STL', 'cubs': 'CHC', 'diamondbacks': 'AZ', 'dodgers': 'LAD', 'giants': 'SF', 'indians': 'CLE',
                     'mariners': 'SEA', 'marlins': 'MIA', 'mets': 'NYM', 'nationals': 'WSH', 'orioles': 'BAL', 'padres': 'SD',
                     'phillies': 'PHI', 'pirates':'PIT', 'rangers': 'TEX', 'rays': 'TB', 'red_sox': 'BOS', 'reds': 'CIN',
                     'rockies': 'COL', 'royals': 'KC', 'tigers':'DET', 'twins':'MIN', 'white_sox':'CWS', 'yankees': 'NYY'}


if team_stadium == 'generic':
    pass
else:
    home_team = team_stadium_dict[team_stadium]

chart_title = '%s %s @ %s stadium' % (hitter_name_first,  hitter_name_last, team_stadium_display)

pitch_data = statcast_batter('2024-03-28', '2024-09-30', hitter)

pitch_data = pitch_data.loc[pitch_data['batter'].isin([hitter])]
pitch_data = pitch_data.loc[pitch_data['events'].isin(['single', 'double', 'triple', 'home_run'])]

if team_stadium !='generic':
    pitch_data = pitch_data.loc[pitch_data['home_team'].isin([home_team])]
else:
    pass

spraychart(pitch_data, team_stadium, title=chart_title)