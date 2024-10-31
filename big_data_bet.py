import pandas as pd
import streamlit as st
from datetime import timedelta
import plotly.graph_objs as go
import numpy as np

st.set_page_config(page_title="Big Data Bet", page_icon="", layout="wide")

custom_css = open("custom.css")
st.markdown('<style>{}</style>'.format(custom_css.read()), unsafe_allow_html=True)



html_br = """
        <br>
        """

cor_azul = '#004d99'
cor_vermelho = 'rgb(255, 75, 75)'
cor_preto = 'rgba(0, 0, 0, 0.6)'

with st.container():
        col1, col2, col3, col4 = st.columns([3, 2, 2, 3])
        with col1:
            st.markdown(html_br, unsafe_allow_html=True)
        with col2:
            st.image("./Alexandre.png")
        with col3:
            st.image("./BigDataBet.jpeg")
        with col4:
            st.markdown(html_br, unsafe_allow_html=True)

#url_database_flashscore = "https://github.com/futpythontrader/YouTube/blob/main/Bases_de_Dados/FlashScore/Base_de_Dados_FlashScore_v2.csv?raw=true"
#database_flashscore = pd.read_csv(url_database_flashscore)

url_database_footystats1 = "https://github.com/futpythontrader/YouTube/blob/main/Bases_de_Dados/FootyStats/Base_de_Dados_FootyStats_(2022_2024).csv?raw=true"
url_database_footystats2 = "https://github.com/futpythontrader/YouTube/blob/main/Bases_de_Dados/FootyStats/Base_de_Dados_FootyStats_(2006_2021).csv?raw=true"
database_flashscore1 = pd.read_csv(url_database_footystats1)
#database_flashscore2 = pd.read_csv(url_database_footystats2)
#database_flashscore = pd.concat([database_flashscore1, database_flashscore2], ignore_index=True)
database_flashscore = database_flashscore1
database_flashscore['Date'] = pd.to_datetime(database_flashscore['Date']).dt.date

#### MODIFICACOES FOOTYSTATS
database_flashscore.rename(columns = {'Goals_H_Minutes':'Goals_Minutes_Home', 'Goals_A_Minutes':'Goals_Minutes_Away','Odd_H_FT':'Odd_H','Odd_A_FT':'Odd_A','Odd_D_FT':'Odd_D','Odd_Over25_FT':'Odd_Over25','Odd_Under25_FT':'Odd_Under25','Goals_H_FT':'Goals_H','Goals_A_FT':'Goals_A'}, inplace = True)


league = sorted(set(database_flashscore['League'].tolist()))

# Sessão de Estado para armazenar os valores selecionados
if 'selected_league' not in st.session_state:
    st.session_state.selected_league = []

if 'selected_team_home' not in st.session_state:
    st.session_state.selected_team_home = []

if 'selected_team_away' not in st.session_state:
    st.session_state.selected_team_away = []

if 'selected_season' not in st.session_state:
    st.session_state.selected_season = []

if 'selected_min_date' not in st.session_state:
    st.session_state.selected_min_date = None

if 'selected_max_date' not in st.session_state:
    st.session_state.selected_max_date = None

if 'selected_1st_goal' not in st.session_state:
    st.session_state.selected_1st_goal = 'Todos'

if 'selected_2nd_goal' not in st.session_state:
    st.session_state.selected_2nd_goal = 'Todos'

if 'selected_3rd_goal' not in st.session_state:
    st.session_state.selected_3rd_goal = 'Todos'

if 'selected_4th_goal' not in st.session_state:
    st.session_state.selected_4th_goal = 'Todos'

if 'selected_min_odd_home' not in st.session_state:
    st.session_state.selected_min_odd_home = 1.00

if 'selected_max_odd_home' not in st.session_state:
    st.session_state.selected_max_odd_home = 9.00

if 'selected_min_odd_away' not in st.session_state:
    st.session_state.selected_min_odd_away = 1.00

if 'selected_max_odd_away' not in st.session_state:
    st.session_state.selected_max_odd_away = 9.00

if 'selected_min_odd_over25' not in st.session_state:
    st.session_state.selected_min_odd_over25 = 1.00

if 'selected_max_odd_over25' not in st.session_state:
    st.session_state.selected_max_odd_over25 = 9.00

with st.container():
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.session_state.selected_league = st.multiselect('Selecione a(s) liga(s):', league)
    with col2:
        filtered_league = database_flashscore[database_flashscore['League'].isin(st.session_state.selected_league)]
        if filtered_league.empty:
            team_home = sorted(set(database_flashscore['Home'].tolist()))
        else:
            team_home = sorted(set(filtered_league['Home'].tolist()))
        st.session_state.selected_team_home = st.multiselect('Selecione o(s) time(s) mandante(s):', team_home)
    with col3:
        filtered_league = database_flashscore[database_flashscore['League'].isin(st.session_state.selected_league)]
        if filtered_league.empty:
            team_away = sorted(set(database_flashscore['Away'].tolist()))
        else:
            team_away = sorted(set(filtered_league['Away'].tolist()))
        st.session_state.selected_team_away = st.multiselect('Selecione o(s) time(s) visitante(s):', team_away)
    with col4:
        filtered_league = database_flashscore[database_flashscore['League'].isin(st.session_state.selected_league)]
        if filtered_league.empty:
            season = sorted(set(database_flashscore['Season'].tolist()))
        else:
            season = sorted(set(filtered_league['Season'].tolist()))
        st.session_state.selected_season = st.multiselect('Selecione a(s) temporada(s):', season)

min_date = database_flashscore['Date'].min()
max_date = database_flashscore['Date'].max()

st.session_state.selected_min_date, st.session_state.selected_max_date = st.slider("Selecione o intervalo de datas:",
                                                min_value=min_date,
                                                max_value=max_date,
                                                value=(min_date, max_date),
                                                format="YYYY-MM-DD",
                                                key="slider1" )

total_days = (max_date - min_date).days
selected_days = (st.session_state.selected_min_date - min_date).days
percentage = (selected_days / total_days) * 100

mask_league = database_flashscore['League'].isin(st.session_state.selected_league) if st.session_state.selected_league else database_flashscore['League'].notnull()
mask_team_home = database_flashscore['Home'].isin(st.session_state.selected_team_home) if st.session_state.selected_team_home else database_flashscore['Home'].notnull()
mask_team_away = database_flashscore['Away'].isin(st.session_state.selected_team_away) if st.session_state.selected_team_away else database_flashscore['Away'].notnull()
mask_season = database_flashscore['Season'].isin(st.session_state.selected_season) if st.session_state.selected_season else database_flashscore['Season'].notnull()
mask_date = (database_flashscore['Date'] >= st.session_state.selected_min_date) & (database_flashscore['Date'] <= st.session_state.selected_max_date)

database_flashscore_filtered = database_flashscore[mask_league & mask_team_home & mask_team_away & mask_season & mask_date]
database_flashscore_filtered_league = database_flashscore[mask_league & mask_season & mask_date]

database_flashscore_filtered['Goals_Minutes_Home'] = database_flashscore_filtered['Goals_Minutes_Home'].apply(lambda x: [] if x == '0' else eval(x))
database_flashscore_filtered['Goals_Minutes_Away'] = database_flashscore_filtered['Goals_Minutes_Away'].apply(lambda x: [] if x == '0' else eval(x))

database_flashscore_filtered_league['Goals_Minutes_Home'] = database_flashscore_filtered_league['Goals_Minutes_Home'].apply(lambda x: [] if x == '0' else eval(x))
database_flashscore_filtered_league['Goals_Minutes_Away'] = database_flashscore_filtered_league['Goals_Minutes_Away'].apply(lambda x: [] if x == '0' else eval(x))


def mark_goal_sequence(row):
    sequence = ''
    home_goals = row['Goals_Minutes_Home']
    away_goals = row['Goals_Minutes_Away']
    
    # Ordena os minutos de gols e concatena 'H' para gols do mandante e 'A' para gols do visitante
    all_goals = sorted(home_goals + away_goals)
    
    for minute in all_goals:
        if minute in home_goals:
            sequence += 'H'
        elif minute in away_goals:
            sequence += 'A'
    
    # Junta a sequência em uma string separada por vírgula
    sequence_str = ''.join(sequence)
    
    return sequence_str

database_flashscore_filtered['Goal_Sequence'] = database_flashscore_filtered.apply(mark_goal_sequence, axis=1)

database_flashscore_filtered_league['Goal_Sequence'] = database_flashscore_filtered_league.apply(mark_goal_sequence, axis=1)

def create_goal_columns(row, index):
    goal_sequence = row['Goal_Sequence']
    
    if len(goal_sequence) > index:
        if goal_sequence[index] == 'H':
            return 'Home'
        elif goal_sequence[index] == 'A':
            return 'Away'
    
    return 'Nenhum'

# Aplicando a função para criar as colunas de gol
database_flashscore_filtered['1º gol'] = database_flashscore_filtered.apply(lambda row: create_goal_columns(row, 0), axis=1)
database_flashscore_filtered['2º gol'] = database_flashscore_filtered.apply(lambda row: create_goal_columns(row, 1), axis=1)
database_flashscore_filtered['3º gol'] = database_flashscore_filtered.apply(lambda row: create_goal_columns(row, 2), axis=1)
database_flashscore_filtered['4º gol'] = database_flashscore_filtered.apply(lambda row: create_goal_columns(row, 3), axis=1)

database_flashscore_filtered_league['1º gol'] = database_flashscore_filtered_league.apply(lambda row: create_goal_columns(row, 0), axis=1)
database_flashscore_filtered_league['2º gol'] = database_flashscore_filtered_league.apply(lambda row: create_goal_columns(row, 1), axis=1)
database_flashscore_filtered_league['3º gol'] = database_flashscore_filtered_league.apply(lambda row: create_goal_columns(row, 2), axis=1)
database_flashscore_filtered_league['4º gol'] = database_flashscore_filtered_league.apply(lambda row: create_goal_columns(row, 3), axis=1)

first_goal_filter = ['Todos'] + sorted(set(database_flashscore_filtered['1º gol'].tolist()))
second_goal_filter = ['Todos'] + sorted(set(database_flashscore_filtered['2º gol'].tolist()))
third_goal_filter = ['Todos'] + sorted(set(database_flashscore_filtered['3º gol'].tolist()))
fourth_goal_filter = ['Todos'] + sorted(set(database_flashscore_filtered['4º gol'].tolist()))

with st.container():
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.session_state.selected_1st_goal = st.radio('1º gol:', first_goal_filter)
    with col2:
        st.session_state.selected_2nd_goal = st.radio('2º gol:', second_goal_filter)
    with col3:
        st.session_state.selected_3rd_goal = st.radio('3º gol:', third_goal_filter)
    with col4:
        st.session_state.selected_4th_goal = st.radio('4º gol:', fourth_goal_filter)

if st.session_state.selected_1st_goal == 'Todos':
    mask_1st_goal = database_flashscore_filtered['1º gol'].notnull()
    mask_1st_goal_league = database_flashscore_filtered_league['1º gol'].notnull()
else:
    mask_1st_goal = database_flashscore_filtered['1º gol'] == st.session_state.selected_1st_goal
    mask_1st_goal_league = database_flashscore_filtered_league['1º gol'] == st.session_state.selected_1st_goal

if st.session_state.selected_2nd_goal == 'Todos':
    mask_2nd_goal = database_flashscore_filtered['2º gol'].notnull()
    mask_2nd_goal_league = database_flashscore_filtered_league['2º gol'].notnull()
else:
    mask_2nd_goal = database_flashscore_filtered['2º gol'] == st.session_state.selected_2nd_goal
    mask_2nd_goal_league = database_flashscore_filtered_league['2º gol'] == st.session_state.selected_2nd_goal

if st.session_state.selected_3rd_goal == 'Todos':
    mask_3rd_goal = database_flashscore_filtered['3º gol'].notnull()
    mask_3rd_goal_league = database_flashscore_filtered_league['3º gol'].notnull()
else:
    mask_3rd_goal = database_flashscore_filtered['3º gol'] == st.session_state.selected_3rd_goal
    mask_3rd_goal_league = database_flashscore_filtered_league['3º gol'] == st.session_state.selected_3rd_goal

if st.session_state.selected_4th_goal == 'Todos':
    mask_4th_goal = database_flashscore_filtered['4º gol'].notnull()
    mask_4th_goal_league = database_flashscore_filtered_league['4º gol'].notnull()
else:
    mask_4th_goal = database_flashscore_filtered['4º gol'] == st.session_state.selected_4th_goal
    mask_4th_goal_league = database_flashscore_filtered_league['4º gol'] == st.session_state.selected_4th_goal

st.session_state.selected_1st_goal = [st.session_state.selected_1st_goal] if st.session_state.selected_1st_goal else first_goal_filter
st.session_state.selected_2nd_goal = [st.session_state.selected_2nd_goal] if st.session_state.selected_2nd_goal else second_goal_filter
st.session_state.selected_3rd_goal = [st.session_state.selected_3rd_goal] if st.session_state.selected_3rd_goal else third_goal_filter
st.session_state.selected_4th_goal = [st.session_state.selected_4th_goal] if st.session_state.selected_4th_goal else fourth_goal_filter

with st.container():
    col1, col2, col3, col4, col5 = st.columns([1,0.4,1,0.4,1])

    with col1:
        min_odd_home = np.float64(database_flashscore['Odd_H'].min())
        max_odd_home = np.float64(database_flashscore['Odd_H'].max())

        st.session_state.selected_min_odd_home, st.session_state.selected_max_odd_home = st.slider("Selecione o intervalo da Odd Home:",
                                                                min_value=1.00,
                                                                max_value=9.00,
                                                                value=(1.00, 9.00))
        
    with col3:
        min_odd_away = np.float64(database_flashscore['Odd_A'].min())
        max_odd_away = np.float64(database_flashscore['Odd_A'].max())

        st.session_state.selected_min_odd_away, st.session_state.selected_max_odd_away = st.slider("Selecione o intervalo da Odd Away:",
                                                                min_value=1.00,
                                                                max_value=9.00,
                                                                value=(1.00, 9.00))
        
    with col5:
        min_odd_over25 = np.float64(database_flashscore['Odd_Over25'].min())
        max_odd_over25 = np.float64(database_flashscore['Odd_Over25'].max())

        st.session_state.selected_min_odd_over25, st.session_state.selected_max_odd_over25 = st.slider("Selecione o intervalo da Odd Over 2.5 gols:",
                                                                min_value=1.00,
                                                                max_value=float(max_odd_over25),
                                                                value=(1.00, float(max_odd_over25)))

final_max_odd_home = st.session_state.selected_max_odd_home if st.session_state.selected_max_odd_home != 9 else max_odd_home
mask_odd_home = (database_flashscore_filtered['Odd_H'] >= st.session_state.selected_min_odd_home) & (database_flashscore_filtered['Odd_H'] <= final_max_odd_home)

final_max_odd_away = st.session_state.selected_max_odd_away if st.session_state.selected_max_odd_away != 9 else max_odd_away
mask_odd_away = (database_flashscore_filtered['Odd_A'] >= st.session_state.selected_min_odd_away) & (database_flashscore_filtered['Odd_A'] <= final_max_odd_away)

#mask_odd_home = (database_flashscore_filtered['Odd_H'] >= selected_min_odd_home) & (database_flashscore_filtered['Odd_H'] <= selected_max_odd_home)
#mask_odd_away = (database_flashscore_filtered['Odd_A'] >= selected_min_odd_away) & (database_flashscore_filtered['Odd_A'] <= selected_max_odd_away)
mask_odd_over25 = (database_flashscore_filtered['Odd_Over25'] >= st.session_state.selected_min_odd_over25) & (database_flashscore_filtered['Odd_Over25'] <= st.session_state.selected_max_odd_over25)

mask_odd_home_league = (database_flashscore_filtered_league['Odd_H'] >= st.session_state.selected_min_odd_home) & (database_flashscore_filtered_league['Odd_H'] <= final_max_odd_home)
mask_odd_away_league = (database_flashscore_filtered_league['Odd_A'] >= st.session_state.selected_min_odd_away) & (database_flashscore_filtered_league['Odd_A'] <= final_max_odd_away)
mask_odd_over25_league = (database_flashscore_filtered_league['Odd_Over25'] >= st.session_state.selected_min_odd_over25) & (database_flashscore_filtered_league['Odd_Over25'] <= st.session_state.selected_max_odd_over25)

database_flashscore_filtered2 = database_flashscore_filtered[mask_1st_goal & mask_2nd_goal & mask_3rd_goal & mask_4th_goal & mask_odd_home & mask_odd_away & mask_odd_over25]
database_flashscore_filtered_league2 = database_flashscore_filtered_league[mask_1st_goal_league & mask_2nd_goal_league & mask_3rd_goal_league & mask_4th_goal_league & mask_odd_home_league & mask_odd_away_league & mask_odd_over25_league]

# Contagem de gols por categoria
count_1st_home = database_flashscore_filtered2['1º gol'].value_counts().get('Home', 0)
count_1st_away = database_flashscore_filtered2['1º gol'].value_counts().get('Away', 0)
count_1st_none = database_flashscore_filtered2['1º gol'].value_counts().get('Nenhum', 0)

count_2nd_home = database_flashscore_filtered2['2º gol'].value_counts().get('Home', 0)
count_2nd_away = database_flashscore_filtered2['2º gol'].value_counts().get('Away', 0)
count_2nd_none = database_flashscore_filtered2['2º gol'].value_counts().get('Nenhum', 0)

count_3rd_home = database_flashscore_filtered2['3º gol'].value_counts().get('Home', 0)
count_3rd_away = database_flashscore_filtered2['3º gol'].value_counts().get('Away', 0)
count_3rd_none = database_flashscore_filtered2['3º gol'].value_counts().get('Nenhum', 0)

count_4th_home = database_flashscore_filtered2['4º gol'].value_counts().get('Home', 0)
count_4th_away = database_flashscore_filtered2['4º gol'].value_counts().get('Away', 0)
count_4th_none = database_flashscore_filtered2['4º gol'].value_counts().get('Nenhum', 0)

# Contagem de gols por categoria nas ligas selecionadas

count_1st_home_league = database_flashscore_filtered_league2['1º gol'].value_counts().get('Home', 0)
count_1st_away_league = database_flashscore_filtered_league2['1º gol'].value_counts().get('Away', 0)
count_1st_none_league = database_flashscore_filtered_league2['1º gol'].value_counts().get('Nenhum', 0)

count_2nd_home_league = database_flashscore_filtered_league2['2º gol'].value_counts().get('Home', 0)
count_2nd_away_league = database_flashscore_filtered_league2['2º gol'].value_counts().get('Away', 0)
count_2nd_none_league = database_flashscore_filtered_league2['2º gol'].value_counts().get('Nenhum', 0)

count_3rd_home_league = database_flashscore_filtered_league2['3º gol'].value_counts().get('Home', 0)
count_3rd_away_league = database_flashscore_filtered_league2['3º gol'].value_counts().get('Away', 0)
count_3rd_none_league = database_flashscore_filtered_league2['3º gol'].value_counts().get('Nenhum', 0)

count_4th_home_league = database_flashscore_filtered_league2['4º gol'].value_counts().get('Home', 0)
count_4th_away_league = database_flashscore_filtered_league2['4º gol'].value_counts().get('Away', 0)
count_4th_none_league = database_flashscore_filtered_league2['4º gol'].value_counts().get('Nenhum', 0)

# Total de jogos
total_games = len(database_flashscore_filtered2)

# Total de jogos liga
total_games_league = len(database_flashscore_filtered_league2)

# Calculando as porcentagens
percent_1st_home = (count_1st_home / total_games) * 100
percent_1st_away = (count_1st_away / total_games) * 100
percent_1st_none = (count_1st_none / total_games) * 100

percent_2nd_home = (count_2nd_home / total_games) * 100
percent_2nd_away = (count_2nd_away / total_games) * 100
percent_2nd_none = (count_2nd_none / total_games) * 100

percent_3rd_home = (count_3rd_home / total_games) * 100
percent_3rd_away = (count_3rd_away / total_games) * 100
percent_3rd_none = (count_3rd_none / total_games) * 100

percent_4th_home = (count_4th_home / total_games) * 100
percent_4th_away = (count_4th_away / total_games) * 100
percent_4th_none = (count_4th_none / total_games) * 100

# Calculando as porcentagens das ligas
percent_1st_home_league = (count_1st_home_league / total_games_league) * 100
percent_1st_away_league = (count_1st_away_league / total_games_league) * 100
percent_1st_none_league = (count_1st_none_league / total_games_league) * 100

percent_2nd_home_league = (count_2nd_home_league / total_games_league) * 100
percent_2nd_away_league = (count_2nd_away_league / total_games_league) * 100
percent_2nd_none_league = (count_2nd_none_league / total_games_league) * 100

percent_3rd_home_league = (count_3rd_home_league / total_games_league) * 100
percent_3rd_away_league = (count_3rd_away_league / total_games_league) * 100
percent_3rd_none_league = (count_3rd_none_league / total_games_league) * 100

percent_4th_home_league = (count_4th_home_league / total_games_league) * 100
percent_4th_away_league = (count_4th_away_league / total_games_league) * 100
percent_4th_none_league = (count_4th_none_league / total_games_league) * 100

# Criando os gráficos com Plotly
fig_1st = go.Figure()
fig_1st.add_trace(go.Bar(y=['Home', 'Away', 'Nenhum'],
                         x=[percent_1st_home, percent_1st_away, percent_1st_none],
                         orientation='h',
                         name='1º gol',
                         text=[f'{count_1st_home} - {percent_1st_home:.2f}%', f'{count_1st_away} - {percent_1st_away:.2f}%', f'{count_1st_none} - {percent_1st_none:.2f}%'],
                         textposition='auto',
                         textangle = 0,
                         marker=dict(color=[cor_azul, cor_vermelho, cor_preto])))

average_values_1st = [percent_1st_home_league, percent_1st_away_league, percent_1st_none_league]

show_average_line = (len(st.session_state.selected_team_home) > 0 or len(st.session_state.selected_team_away) > 0)

if show_average_line:

    # Adicionando as linhas verticais para as médias gerais
    for idx, avg in enumerate(average_values_1st):
        # Ajustando as coordenadas y0 e y1 para que a linha vertical se ajuste à respectiva categoria
        y0 = idx - 0.4  # Posição inicial da linha vertical
        y1 = idx + 0.4  # Posição final da linha vertical
        
        fig_1st.add_shape(
            type="line",
            x0=avg, y0=y0, x1=avg, y1=y1,  # Definindo a posição da linha vertical
            line=dict(color='black', width=2),  # Linha vertical preta
            name=f'Average: {avg:.2f}',
            xref='x', yref='y'
        )

        fig_1st.add_annotation(
            x=avg,
            y=y1 + 0.1,  # Posição acima da linha vertical
            text=f'{avg:.2f}%',  # Mostrar o valor como percentual com duas casas decimais
            showarrow=False,
            font=dict(color='black'),
            xshift=10,  # Ajuste de posição horizontal para o valor ficar ao lado da linha
        )

fig_1st.update_layout(height=400, xaxis_title='Porcentagem (%)',
                      xaxis=dict(range=[0, 100]))

fig_2nd = go.Figure()
fig_2nd.add_trace(go.Bar(y=['Home', 'Away', 'Nenhum'],
                         x=[percent_2nd_home, percent_2nd_away, percent_2nd_none],
                         orientation='h',
                         name='2º gol',
                         text=[f'{count_2nd_home} - {percent_2nd_home:.2f}%', f'{count_2nd_away} - {percent_2nd_away:.2f}%', f'{count_2nd_none} - {percent_2nd_none:.2f}%'],
                         textposition='auto',
                         textangle = 0,
                         marker=dict(color=[cor_azul, cor_vermelho, cor_preto])))

average_values_2nd = [percent_2nd_home_league, percent_2nd_away_league, percent_2nd_none_league]

show_average_line = (len(st.session_state.selected_team_home) > 0 or len(st.session_state.selected_team_away) > 0)

if show_average_line:

    # Adicionando as linhas verticais para as médias gerais
    for idx, avg in enumerate(average_values_2nd):
        # Ajustando as coordenadas y0 e y1 para que a linha vertical se ajuste à respectiva categoria
        y0 = idx - 0.4  # Posição inicial da linha vertical
        y1 = idx + 0.4  # Posição final da linha vertical
        
        fig_2nd.add_shape(
            type="line",
            x0=avg, y0=y0, x1=avg, y1=y1,  # Definindo a posição da linha vertical
            line=dict(color='black', width=2),  # Linha vertical preta
            name=f'Average: {avg:.2f}',
            xref='x', yref='y'
        )

        fig_2nd.add_annotation(
            x=avg,
            y=y1 + 0.1,  # Posição acima da linha vertical
            text=f'{avg:.2f}%',  # Mostrar o valor como percentual com duas casas decimais
            showarrow=False,
            font=dict(color='black'),
            xshift=10,  # Ajuste de posição horizontal para o valor ficar ao lado da linha
        )

fig_2nd.update_layout(height=400, xaxis_title='Porcentagem (%)',
                      xaxis=dict(range=[0, 100]))

fig_3rd = go.Figure()
fig_3rd.add_trace(go.Bar(y=['Home', 'Away', 'Nenhum'],
                         x=[percent_3rd_home, percent_3rd_away, percent_3rd_none],
                         orientation='h',
                         name='3º gol',
                         text=[f'{count_3rd_home} - {percent_3rd_home:.2f}%', f'{count_3rd_away} - {percent_3rd_away:.2f}%', f'{count_3rd_none} - {percent_3rd_none:.2f}%'],
                         textposition='auto',
                         textangle = 0,
                         marker=dict(color=[cor_azul, cor_vermelho, cor_preto])))

average_values_3rd = [percent_3rd_home_league, percent_3rd_away_league, percent_3rd_none_league]

show_average_line = (len(st.session_state.selected_team_home) > 0 or len(st.session_state.selected_team_away) > 0)

if show_average_line:

    # Adicionando as linhas verticais para as médias gerais
    for idx, avg in enumerate(average_values_3rd):
        # Ajustando as coordenadas y0 e y1 para que a linha vertical se ajuste à respectiva categoria
        y0 = idx - 0.4  # Posição inicial da linha vertical
        y1 = idx + 0.4  # Posição final da linha vertical
        
        fig_3rd.add_shape(
            type="line",
            x0=avg, y0=y0, x1=avg, y1=y1,  # Definindo a posição da linha vertical
            line=dict(color='black', width=2),  # Linha vertical preta
            name=f'Average: {avg:.2f}',
            xref='x', yref='y'
        )

        fig_3rd.add_annotation(
            x=avg,
            y=y1 + 0.1,  # Posição acima da linha vertical
            text=f'{avg:.2f}%',  # Mostrar o valor como percentual com duas casas decimais
            showarrow=False,
            font=dict(color='black'),
            xshift=10,  # Ajuste de posição horizontal para o valor ficar ao lado da linha
        )

fig_3rd.update_layout(height=400, xaxis_title='Porcentagem (%)',
                      xaxis=dict(range=[0, 100]))

fig_4th = go.Figure()
fig_4th.add_trace(go.Bar(y=['Home', 'Away', 'Nenhum'],
                         x=[percent_4th_home, percent_4th_away, percent_4th_none],
                         orientation='h',
                         name='4º gol',
                         text=[f'{count_4th_home} - {percent_4th_home:.2f}%', f'{count_4th_away} - {percent_4th_away:.2f}%', f'{count_4th_none} - {percent_4th_none:.2f}%'],
                         textposition='auto',
                         textangle = 0,
                         marker=dict(color=[cor_azul, cor_vermelho, cor_preto])))

average_values_4th = [percent_4th_home_league, percent_4th_away_league, percent_4th_none_league]

show_average_line = (len(st.session_state.selected_team_home) > 0 or len(st.session_state.selected_team_away) > 0)

if show_average_line:

    # Adicionando as linhas verticais para as médias gerais
    for idx, avg in enumerate(average_values_4th):
        # Ajustando as coordenadas y0 e y1 para que a linha vertical se ajuste à respectiva categoria
        y0 = idx - 0.4  # Posição inicial da linha vertical
        y1 = idx + 0.4  # Posição final da linha vertical
        
        fig_4th.add_shape(
            type="line",
            x0=avg, y0=y0, x1=avg, y1=y1,  # Definindo a posição da linha vertical
            line=dict(color='black', width=2),  # Linha vertical preta
            name=f'Average: {avg:.2f}',
            xref='x', yref='y'
        )

        fig_4th.add_annotation(
            x=avg,
            y=y1 + 0.1,  # Posição acima da linha vertical
            text=f'{avg:.2f}%',  # Mostrar o valor como percentual com duas casas decimais
            showarrow=False,
            font=dict(color='black'),
            xshift=10,  # Ajuste de posição horizontal para o valor ficar ao lado da linha
        )

fig_4th.update_layout(height=400, xaxis_title='Porcentagem (%)',
                      xaxis=dict(range=[0, 100]))

with st.container():
    col1, col2= st.columns(2)

    with col1:

        st.markdown(
            f"""
                <div style="background-color: white; color: black; padding: 10px; border-top-left-radius: 10px; border-top-right-radius: 10px;  ">
                    <strong>Probabilidade de marcar o 1º gol</strong>
                        </div>
                    """,
                    unsafe_allow_html=True
            )

        st.markdown(f"""
                    <hr style="border: 1px solid {cor_azul}; margin-top: 0;">  """, unsafe_allow_html=True)
        st.markdown(
            """
            <div style="background-color: white; color: black; padding: 10px; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px; font-size: smaller; margin-top: -25px;">
                A linha vertical em preto representa a média das ligas selecionadas.
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.plotly_chart(fig_1st, use_container_width=True)

        st.markdown(
            f"""
                <div style="background-color: white; color: black; padding: 10px; border-top-left-radius: 10px; border-top-right-radius: 10px;  ">
                    <strong>Probabilidade de marcar o 3º gol</strong>
                        </div>
                    """,
                    unsafe_allow_html=True
            )

        st.markdown(f"""
                    <hr style="border: 1px solid {cor_azul}; margin-top: 0;">  """, unsafe_allow_html=True)
        st.markdown(
            """
            <div style="background-color: white; color: black; padding: 10px; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px; font-size: smaller; margin-top: -25px;">
                A linha vertical em preto representa a média das ligas selecionadas.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.plotly_chart(fig_3rd, use_container_width=True)
    with col2:

        st.markdown(
            f"""
                <div style="background-color: white; color: black; padding: 10px; border-top-left-radius: 10px; border-top-right-radius: 10px;  ">
                    <strong>Probabilidade de marcar o 2º gol</strong>
                        </div>
                    """,
                    unsafe_allow_html=True
            )

        st.markdown(f"""
                    <hr style="border: 1px solid {cor_azul}; margin-top: 0;">  """, unsafe_allow_html=True)
        st.markdown(
            """
            <div style="background-color: white; color: black; padding: 10px; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px; font-size: smaller; margin-top: -25px;">
                A linha vertical em preto representa a média das ligas selecionadas.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.plotly_chart(fig_2nd, use_container_width=True)

        st.markdown(
            f"""
                <div style="background-color: white; color: black; padding: 10px; border-top-left-radius: 10px; border-top-right-radius: 10px;  ">
                    <strong>Probabilidade de marcar o 4º gol</strong>
                        </div>
                    """,
                    unsafe_allow_html=True
            )

        st.markdown(f"""
                    <hr style="border: 1px solid {cor_azul}; margin-top: 0;">  """, unsafe_allow_html=True)
        st.markdown(
            """
            <div style="background-color: white; color: black; padding: 10px; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px; font-size: smaller; margin-top: -25px;">
                A linha vertical em preto representa a média das ligas selecionadas.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.plotly_chart(fig_4th, use_container_width=True)

def determine_result(row):
    if row['Goals_H'] > row['Goals_A']:
        return 'Home'
    elif row['Goals_H'] < row['Goals_A']:
        return 'Away'
    else:
        return 'Draw'

# Aplicando a função para criar a coluna 'Result'
database_flashscore_filtered2['Result'] = database_flashscore_filtered2.apply(lambda row: determine_result(row), axis=1)

count_result_home = database_flashscore_filtered2['Result'].value_counts().get('Home', 0)
count_result_away = database_flashscore_filtered2['Result'].value_counts().get('Away', 0)
count_result_none = database_flashscore_filtered2['Result'].value_counts().get('Draw', 0)

def determine_over_under(row):
    total_goals = row['Goals_H'] + row['Goals_A']
    if total_goals > 2:
        return 'Over 2,5'
    else:
        return 'Under 2,5'

# Aplicando a função para criar a coluna 'Over/Under 2,5'
database_flashscore_filtered2['Over/Under 2,5'] = database_flashscore_filtered2.apply(lambda row: determine_over_under(row), axis=1)

count_over25 = database_flashscore_filtered2['Over/Under 2,5'].value_counts().get('Over 2,5', 0)
count_under25 = database_flashscore_filtered2['Over/Under 2,5'].value_counts().get('Under 2,5', 0)

def determine_btts(row):
    if row['Goals_H'] > 0 and row['Goals_A'] > 0:
        return 'BTTS Yes'
    else:
        return 'BTTS No'

# Aplicando a função para criar a coluna 'BTTS Yes/No'
database_flashscore_filtered2['BTTS Yes/No'] = database_flashscore_filtered2.apply(lambda row: determine_btts(row), axis=1)

count_btts_yes = database_flashscore_filtered2['BTTS Yes/No'].value_counts().get('BTTS Yes', 0)
count_btts_no = database_flashscore_filtered2['BTTS Yes/No'].value_counts().get('BTTS No', 0)

def determine_first_goal_range(row, coluna):
    if not row[coluna]:  # Verifica se a lista está vazia
        return 'No Goals'
    
    min_minute = min(row[coluna])

    if '+' in min_minute:
        min_minute = int(min_minute.split('+')[0])
    
    if int(min_minute) >= 0 and int(min_minute) <= 15:
        return '0 - 15'
    elif int(min_minute) >= 16 and int(min_minute) <= 30:
        return '16 - 30'
    elif int(min_minute) >= 31 and int(min_minute) <= 45:
        return '31 - 45'
    elif int(min_minute) >= 46 and int(min_minute) <= 60:
        return '46 - 60'
    elif int(min_minute) >= 61 and int(min_minute) <= 75:
        return '61 - 75'
    elif int(min_minute) >= 76:
        return '76 - 90'
    else:
        return 'No Goals'



# Aplicando a função para criar a coluna 'First_Goal_Home'
database_flashscore_filtered2['First_Goal_Home'] = database_flashscore_filtered2.apply(lambda row: determine_first_goal_range(row, 'Goals_Minutes_Home'), axis=1)
database_flashscore_filtered2['First_Goal_Away'] = database_flashscore_filtered2.apply(lambda row: determine_first_goal_range(row, 'Goals_Minutes_Away'), axis=1)

database_flashscore_filtered_league2['First_Goal_Home'] = database_flashscore_filtered_league2.apply(lambda row: determine_first_goal_range(row, 'Goals_Minutes_Home'), axis=1)
database_flashscore_filtered_league2['First_Goal_Away'] = database_flashscore_filtered_league2.apply(lambda row: determine_first_goal_range(row, 'Goals_Minutes_Away'), axis=1)

cores = {
    'Result': {'Home': cor_azul, 'Away': cor_vermelho, 'Draw': cor_preto},
    'Over/Under 2,5': {'Over 2,5': cor_azul, 'Under 2,5': cor_vermelho},
    'BTTS Yes/No': {'BTTS Yes': cor_azul, 'BTTS No': cor_vermelho}
}

def create_pie_chart(df, column, colors):
    counts = df[column].value_counts()
    labels = counts.index.tolist()
    values = counts.values.tolist()
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4, 
                                 marker=dict(colors=[colors[label] for label in labels]))])
    
    st.plotly_chart(fig, use_container_width=True)

with st.container():
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
                <div style="background-color: white; color: black; padding: 10px; border-top-left-radius: 10px; border-top-right-radius: 10px;  ">
                    <strong>Distribuição do resultado dos jogos</strong>
                        </div>
                    """,
                    unsafe_allow_html=True
            )

        st.markdown(f"""
                    <hr style="border: 1px solid {cor_azul}; margin-top: 0;">  """, unsafe_allow_html=True)
        create_pie_chart(database_flashscore_filtered2, 'Result', cores['Result'])

    with col2:
        st.markdown(
            f"""
                <div style="background-color: white; color: black; padding: 10px; border-top-left-radius: 10px; border-top-right-radius: 10px;  ">
                    <strong>Distribuição do número de gols dos jogos</strong>
                        </div>
                    """,
                    unsafe_allow_html=True
            )

        st.markdown(f"""
                    <hr style="border: 1px solid {cor_azul}; margin-top: 0;">  """, unsafe_allow_html=True)
        create_pie_chart(database_flashscore_filtered2, 'Over/Under 2,5', cores['Over/Under 2,5'])

    with col3:
        st.markdown(
            f"""
                <div style="background-color: white; color: black; padding: 10px; border-top-left-radius: 10px; border-top-right-radius: 10px;  ">
                    <strong>Distribuição do ambas marcam nos jogos</strong>
                        </div>
                    """,
                    unsafe_allow_html=True
            )

        st.markdown(f"""
                    <hr style="border: 1px solid {cor_azul}; margin-top: 0;">  """, unsafe_allow_html=True)
        create_pie_chart(database_flashscore_filtered2, 'BTTS Yes/No', cores['BTTS Yes/No'])

    
categories = ['0 - 15', '16 - 30', '31 - 45', '46 - 60', '61 - 75', '76 - 90', 'No Goals']

# Função para criar gráfico de colunas
def create_bar_chart(data, column_name, categories):
    # Convertendo para DataFrame
    df = pd.DataFrame(data)
    
    # Inicializando lista para contar as categorias
    counts = [0] * len(categories)
    
    # Contagem de cada categoria
    for value in df[column_name]:
        if pd.notna(value) and value in categories:
            index = categories.index(value)
            counts[index] += 1

    text_values = [f'{count}' if count > 0 else '' for count in counts]
    
    # Criação do gráfico de colunas com valores nas barras
    fig = go.Figure(data=[go.Bar(x=categories, y=counts, text=text_values, textposition='auto', marker_color=cor_azul)])
    #fig.update_yaxes(range=[0, 100], autorange=False)
    fig.update_layout(xaxis_title='Intervalo de Minutos', yaxis_title='Número de Jogos')
    st.plotly_chart(fig, use_container_width=True)

def calculate_stats(df):
    # Função auxiliar para encontrar o primeiro gol
    def first_goal_minutes(goals_list):
        if goals_list:

            min_minute = min(goals_list)

            if '+' in min_minute:
                min_minute = int(min_minute.split('+')[0])

            return min_minute
        return None
    
    # Encontrar o primeiro gol para cada time
    df['First_Goal_Minutes_Home'] = df['Goals_Minutes_Home'].apply(first_goal_minutes)
    df['First_Goal_Minutes_Away'] = df['Goals_Minutes_Away'].apply(first_goal_minutes)
    
    def process_minute(min_minute):
        # Verifica se o valor é None ou uma string que representa None
        if min_minute is None or str(min_minute).strip().lower() == 'none':
            return None  # Ou um valor padrão que você desejar
        min_minute_str = str(min_minute)
        if '+' in min_minute_str:
            return int(min_minute_str.split('+')[0])
        return int(min_minute_str)

    df['First_Goal_Minutes_Home'] = df['First_Goal_Minutes_Home'].apply(process_minute)
    mean_home = df['First_Goal_Minutes_Home'].mean()
    std_home = df['First_Goal_Minutes_Home'].std()
    
    df['First_Goal_Minutes_Away'] = df['First_Goal_Minutes_Away'].apply(process_minute)
    mean_away = df['First_Goal_Minutes_Away'].mean()
    std_away = df['First_Goal_Minutes_Away'].std()
    
    return mean_home, std_home, mean_away, std_away

# Calcular média e desvio padrão
mean_home, std_home, mean_away, std_away = calculate_stats(database_flashscore_filtered2)

with st.container():
    col1, col2, col3, col4 = st.columns([2,2,2,2])

    with col1:
        st.markdown(
            f"""
                <div style="background-color: white; color: black; padding: 10px; border-top-left-radius: 10px; border-top-right-radius: 10px;  ">
                    <strong>Média de minutos do 1º gol Home</strong>
                        </div>
                    """,
                    unsafe_allow_html=True
            )

        st.markdown(f"""
                    <hr style="border: 1px solid {cor_azul}; margin-top: 0;">  """, unsafe_allow_html=True)
        
        st.markdown(
                    f"""
                    <div style="background-color: white; color: {cor_azul}; padding: 0px; border-top-left-radius: 0px; border-top-right-radius: 0px; text-align: center; font-size: 36px; margin-bottom: 10px;">
                        <strong>{mean_home:.2f}</strong>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
    with col2:
        st.markdown(
            f"""
                <div style="background-color: white; color: black; padding: 10px; border-top-left-radius: 10px; border-top-right-radius: 10px;  ">
                    <strong>Desvio padrão do 1º gol Home</strong>
                        </div>
                    """,
                    unsafe_allow_html=True
            )

        st.markdown(f"""
                    <hr style="border: 1px solid {cor_azul}; margin-top: 0;">  """, unsafe_allow_html=True)
        
        st.markdown(
                    f"""
                    <div style="background-color: white; color: {cor_azul}; padding: 0px; border-top-left-radius: 0px; border-top-right-radius: 0px; text-align: center; font-size: 36px; margin-bottom: 10px;">
                        <strong>{std_home:.2f}</strong>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
    with col3:
        st.markdown(
            f"""
                <div style="background-color: white; color: black; padding: 10px; border-top-left-radius: 10px; border-top-right-radius: 10px;  ">
                    <strong>Média de minutos do 1º gol Away</strong>
                        </div>
                    """,
                    unsafe_allow_html=True
            )

        st.markdown(f"""
                    <hr style="border: 1px solid {cor_azul}; margin-top: 0;">  """, unsafe_allow_html=True)
        
        st.markdown(
                    f"""
                    <div style="background-color: white; color: {cor_azul}; padding: 0px; border-top-left-radius: 0px; border-top-right-radius: 0px; text-align: center; font-size: 36px; margin-bottom: 10px;">
                        <strong>{mean_away:.2f}</strong>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
    with col4:
        st.markdown(
            f"""
                <div style="background-color: white; color: black; padding: 10px; border-top-left-radius: 10px; border-top-right-radius: 10px;  ">
                    <strong>Desvio padrão do 1º gol Away</strong>
                        </div>
                    """,
                    unsafe_allow_html=True
            )

        st.markdown(f"""
                    <hr style="border: 1px solid {cor_azul}; margin-top: 0;">  """, unsafe_allow_html=True)
        
        st.markdown(
                    f"""
                    <div style="background-color: white; color: {cor_azul}; padding: 0px; border-top-left-radius: 0px; border-top-right-radius: 0px; text-align: center; font-size: 36px; margin-bottom: 10px;">
                        <strong>{std_away:.2f}</strong>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


with st.container():
    col1, col2 = st.columns([4,4])

    with col1:
        st.markdown(
            f"""
                <div style="background-color: white; color: black; padding: 10px; border-top-left-radius: 10px; border-top-right-radius: 10px;  ">
                    <strong>Momento do 1º gol Home</strong>
                        </div>
                    """,
                    unsafe_allow_html=True
            )

        st.markdown(f"""
                    <hr style="border: 1px solid {cor_azul}; margin-top: 0;">  """, unsafe_allow_html=True)
        
        create_bar_chart(database_flashscore_filtered2, 'First_Goal_Home', categories)

    with col2:
        st.markdown(
            f"""
                <div style="background-color: white; color: black; padding: 10px; border-top-left-radius: 10px; border-top-right-radius: 10px;  ">
                    <strong>Momento do 1º gol Away</strong>
                        </div>
                    """,
                    unsafe_allow_html=True
            )

        st.markdown(f"""
                    <hr style="border: 1px solid {cor_azul}; margin-top: 0;">  """, unsafe_allow_html=True)

        create_bar_chart(database_flashscore_filtered2, 'First_Goal_Away', categories)

categories_accu = {
    '0 - 15': ['Até 15', 'Até 30', 'Até 45', 'Até 60', 'Até 75', 'Até 90'],
    '16 - 30': ['Até 30', 'Até 45', 'Até 60', 'Até 75', 'Até 90'],
    '31 - 45': ['Até 45', 'Até 60', 'Até 75', 'Até 90'],
    '46 - 60': ['Até 60', 'Até 75', 'Até 90'],
    '61 - 75': ['Até 75', 'Até 90'],
    '76 - 90': ['Até 90'],
    'No Goals': []
}

def map_categories(goal_category):
    return categories_accu.get(goal_category, [])

# Criando as colunas 'Home' e 'Away' com listas de categorias acumuladas
database_flashscore_filtered2['First_Goal_Home_Accu'] = database_flashscore_filtered2['First_Goal_Home'].apply(map_categories)
database_flashscore_filtered2['First_Goal_Away_Accu'] = database_flashscore_filtered2['First_Goal_Away'].apply(map_categories)

database_flashscore_filtered_league2['First_Goal_Home_Accu'] = database_flashscore_filtered_league2['First_Goal_Home'].apply(map_categories)
database_flashscore_filtered_league2['First_Goal_Away_Accu'] = database_flashscore_filtered_league2['First_Goal_Away'].apply(map_categories)

def count_categories(df, column_name, all_categories):
    counts = {cat: 0 for cat in all_categories}
    for row in df[column_name]:
        for cat in row:
            counts[cat] += 1
    return counts

# Definindo todas as categorias possíveis
all_categories = ['Até 15', 'Até 30', 'Até 45', 'Até 60', 'Até 75', 'Até 90']

def create_bar_chart2(df1, df2, column_name, show_average_line):
    # Contagem e porcentagem para o primeiro DataFrame
    counts1 = count_categories(df1, column_name, all_categories)
    total_lines1 = len(df1)
    percentages1 = {cat: (count / total_lines1) * 100 for cat, count in counts1.items()}
    
    categories_sorted = sorted(all_categories, key=lambda x: int(x.split(' ')[1]))
    counts_sorted1 = [percentages1[cat] for cat in categories_sorted]
    
    # Criando o gráfico de barras para o primeiro DataFrame
    fig = go.Figure()
    
    # Adicionando as barras verticais para o primeiro DataFrame
    fig.add_trace(go.Bar(x=categories_sorted, y=counts_sorted1, text=[f'{val:.1f}%' for val in counts_sorted1], textposition='auto', 
                         marker_color=cor_azul, name='Porcentagem - DF1'))
    
    if show_average_line:

        # Contagem para o segundo DataFrame
        counts2 = count_categories(df2, column_name, all_categories)
        total_lines2 = len(df2)
        
        # Calculando a média para o segundo DataFrame
        mean_values2 = {cat: (count / total_lines2) * 100 for cat, count in counts2.items()}
        
        # Adicionando as linhas horizontais para cada categoria do segundo DataFrame
        for cat in categories_sorted:
            mean_value = mean_values2.get(cat, 0)  # Valor médio ou 0 se não houver dados
            
            # Encontrando a posição do início e fim da linha horizontal
            x_start = categories_sorted.index(cat) - 0.4
            x_end = categories_sorted.index(cat) + 0.4
            
            fig.add_shape(type="line",
                        x0=x_start, y0=mean_value,  # Início da linha horizontal
                        x1=x_end, y1=mean_value,  # Fim da linha horizontal
                        line=dict(color="black", width=2),
                        name=f'Média - {cat}', 
                        xref='x', yref='y')
            
        
            fig.add_annotation(
                x=x_end + 0.1,  # Posição central entre o início e fim da linha
                y=mean_value,  # Posição da linha horizontal
                text=f'{mean_value:.1f}%',  # Texto formatado com duas casas decimais
                showarrow=False,
                font=dict(color='black'),
                yshift=10,  # Ajuste de posição vertical para o texto ficar abaixo da linha
            )
    
    # Configurando layout do gráfico
    fig.update_layout(xaxis_title='Intervalo de Minutos', yaxis_title='Porcentagem de Jogos', yaxis=dict(range=[0, 100]))
    
    st.plotly_chart(fig, use_container_width=True)

with st.container():
    col1, col2 = st.columns([4,4])

    with col1:
        st.markdown(
            f"""
                <div style="background-color: white; color: black; padding: 10px; border-top-left-radius: 10px; border-top-right-radius: 10px;  ">
                    <strong>Porcentagem de jogos com 1º gol Home até dado momento</strong>
                        </div>
                    """,
                    unsafe_allow_html=True
            )

        st.markdown(f"""
                    <hr style="border: 1px solid {cor_azul}; margin-top: 0;">  """, unsafe_allow_html=True)
        
        st.markdown(
            """
            <div style="background-color: white; color: black; padding: 10px; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px; font-size: smaller; margin-top: -25px;">
                A linha horizontal em preto representa a média das ligas selecionadas.
            </div>
            """,
            unsafe_allow_html=True
        )

        create_bar_chart2(database_flashscore_filtered2, database_flashscore_filtered_league2, 'First_Goal_Home_Accu', show_average_line)

    with col2:
        st.markdown(
            f"""
                <div style="background-color: white; color: black; padding: 10px; border-top-left-radius: 10px; border-top-right-radius: 10px;  ">
                    <strong>Porcentagem de jogos com 1º gol Away até dado momento</strong>
                        </div>
                    """,
                    unsafe_allow_html=True
            )

        st.markdown(f"""
                    <hr style="border: 1px solid {cor_azul}; margin-top: 0;">  """, unsafe_allow_html=True)
        
        st.markdown(
            """
            <div style="background-color: white; color: black; padding: 10px; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px; font-size: smaller; margin-top: -25px;">
                A linha horizontal em preto representa a média das ligas selecionadas.
            </div>
            """,
            unsafe_allow_html=True
        )

        create_bar_chart2(database_flashscore_filtered2, database_flashscore_filtered_league2, 'First_Goal_Away_Accu', show_average_line)


        
        