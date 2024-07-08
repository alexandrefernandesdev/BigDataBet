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

url_database_flashscore = "https://github.com/futpythontrader/YouTube/blob/main/Bases_de_Dados/FlashScore/Base_de_Dados_FlashScore_v2.csv?raw=true"


database_flashscore = pd.read_csv(url_database_flashscore)
database_flashscore['Date'] = pd.to_datetime(database_flashscore['Date']).dt.date

league = sorted(set(database_flashscore['League'].tolist()))


with st.container():
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        selected_league = st.multiselect('Selecione a(s) liga(s):', league)
    with col2:
        filtered_league = database_flashscore[database_flashscore['League'].isin(selected_league)]
        team_home = sorted(set(filtered_league['Home'].tolist()))
        selected_team_home = st.multiselect('Selecione o(s) time(s) mandante(s):', team_home)
    with col3:
        filtered_league = database_flashscore[database_flashscore['League'].isin(selected_league)]
        team_away = sorted(set(filtered_league['Away'].tolist()))
        selected_team_away = st.multiselect('Selecione o(s) time(s) visitante(s):', team_away)
    with col4:
        filtered_league = database_flashscore[database_flashscore['League'].isin(selected_league)]
        season = sorted(set(filtered_league['Season'].tolist()))
        selected_season = st.multiselect('Selecione a(s) temporada(s):', season)

min_date = database_flashscore['Date'].min()
max_date = database_flashscore['Date'].max()

selected_min_date, selected_max_date = st.slider("Selecione o intervalo de datas:",
                                                min_value=min_date,
                                                max_value=max_date,
                                                value=(min_date, max_date),
                                                format="YYYY-MM-DD",
                                                key="slider1" )

total_days = (max_date - min_date).days
selected_days = (selected_min_date - min_date).days
percentage = (selected_days / total_days) * 100

mask_league = database_flashscore['League'].isin(selected_league) if selected_league else database_flashscore['League'].notnull()
mask_team_home = database_flashscore['Home'].isin(selected_team_home) if selected_team_home else database_flashscore['Home'].notnull()
mask_team_away = database_flashscore['Away'].isin(selected_team_away) if selected_team_away else database_flashscore['Away'].notnull()
mask_season = database_flashscore['Season'].isin(selected_season) if selected_season else database_flashscore['Season'].notnull()
mask_date = (database_flashscore['Date'] >= selected_min_date) & (database_flashscore['Date'] <= selected_max_date)

database_flashscore_filtered = database_flashscore[mask_league & mask_team_home & mask_team_away & mask_season & mask_date]

database_flashscore_filtered['Goals_Minutes_Home'] = database_flashscore_filtered['Goals_Minutes_Home'].apply(lambda x: [] if x == '0' else eval(x))
database_flashscore_filtered['Goals_Minutes_Away'] = database_flashscore_filtered['Goals_Minutes_Away'].apply(lambda x: [] if x == '0' else eval(x))

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

first_goal_filter = ['Todos'] + sorted(set(database_flashscore_filtered['1º gol'].tolist()))
second_goal_filter = ['Todos'] + sorted(set(database_flashscore_filtered['2º gol'].tolist()))
third_goal_filter = ['Todos'] + sorted(set(database_flashscore_filtered['3º gol'].tolist()))
fourth_goal_filter = ['Todos'] + sorted(set(database_flashscore_filtered['4º gol'].tolist()))

with st.container():
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        selected_1st_goal = st.radio('1º gol:', first_goal_filter)
    with col2:
        selected_2nd_goal = st.radio('2º gol:', second_goal_filter)
    with col3:
        selected_3rd_goal = st.radio('3º gol:', third_goal_filter)
    with col4:
        selected_4th_goal = st.radio('4º gol:', fourth_goal_filter)

if selected_1st_goal == 'Todos':
    mask_1st_goal = database_flashscore_filtered['1º gol'].notnull()
else:
    mask_1st_goal = database_flashscore_filtered['1º gol'] == selected_1st_goal

if selected_2nd_goal == 'Todos':
    mask_2nd_goal = database_flashscore_filtered['2º gol'].notnull()
else:
    mask_2nd_goal = database_flashscore_filtered['2º gol'] == selected_2nd_goal

if selected_3rd_goal == 'Todos':
    mask_3rd_goal = database_flashscore_filtered['3º gol'].notnull()
else:
    mask_3rd_goal = database_flashscore_filtered['3º gol'] == selected_3rd_goal

if selected_4th_goal == 'Todos':
    mask_4th_goal = database_flashscore_filtered['4º gol'].notnull()
else:
    mask_4th_goal = database_flashscore_filtered['4º gol'] == selected_4th_goal

selected_1st_goal = [selected_1st_goal] if selected_1st_goal else first_goal_filter
selected_2nd_goal = [selected_2nd_goal] if selected_2nd_goal else second_goal_filter
selected_3rd_goal = [selected_3rd_goal] if selected_3rd_goal else third_goal_filter
selected_4th_goal = [selected_4th_goal] if selected_4th_goal else fourth_goal_filter

with st.container():
    col1, col2, col3, col4, col5 = st.columns([1,0.2,1,0.2,1])

    with col1:
        min_odd_home = np.float64(database_flashscore['Odd_H'].min())
        max_odd_home = np.float64(database_flashscore['Odd_H'].max())

        selected_min_odd_home, selected_max_odd_home = st.slider("Selecione o intervalo da Odd Home:",
                                                                min_value=float(min_odd_home),
                                                                max_value=float(max_odd_home),
                                                                value=(float(min_odd_home), float(max_odd_home)))
        
    with col3:
        min_odd_away = np.float64(database_flashscore['Odd_A'].min())
        max_odd_away = np.float64(database_flashscore['Odd_A'].max())

        selected_min_odd_away, selected_max_odd_away = st.slider("Selecione o intervalo da Odd Away:",
                                                                min_value=float(min_odd_away),
                                                                max_value=float(max_odd_away),
                                                                value=(float(min_odd_away), float(max_odd_away)))
        
    with col5:
        min_odd_over25 = np.float64(database_flashscore['Odd_Over25'].min())
        max_odd_over25 = np.float64(database_flashscore['Odd_Over25'].max())

        selected_min_odd_over25, selected_max_odd_over25 = st.slider("Selecione o intervalo da Odd Over 2.5 gols:",
                                                                min_value=float(min_odd_over25),
                                                                max_value=float(max_odd_over25),
                                                                value=(float(min_odd_over25), float(max_odd_over25)))

mask_odd_home = (database_flashscore_filtered['Odd_H'] >= selected_min_odd_home) & (database_flashscore_filtered['Odd_H'] <= selected_max_odd_home)
mask_odd_away = (database_flashscore_filtered['Odd_A'] >= selected_min_odd_away) & (database_flashscore_filtered['Odd_A'] <= selected_max_odd_away)
mask_odd_over25 = (database_flashscore_filtered['Odd_Over25'] >= selected_min_odd_over25) & (database_flashscore_filtered['Odd_Over25'] <= selected_max_odd_over25)

database_flashscore_filtered2 = database_flashscore_filtered[mask_1st_goal & mask_2nd_goal & mask_3rd_goal & mask_4th_goal & mask_odd_home & mask_odd_away & mask_odd_over25]

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

# Total de jogos
total_games = len(database_flashscore_filtered2)

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
    
    if min_minute >= 0 and min_minute <= 15:
        return '0 - 15'
    elif min_minute >= 16 and min_minute <= 30:
        return '16 - 30'
    elif min_minute >= 31 and min_minute <= 45:
        return '31 - 45'
    elif min_minute >= 46 and min_minute <= 60:
        return '46 - 60'
    elif min_minute >= 61 and min_minute <= 75:
        return '61 - 75'
    elif min_minute >= 76:
        return '76 - 90'
    else:
        return 'No Goals'


# Aplicando a função para criar a coluna 'First_Goal_Home'
database_flashscore_filtered2['First_Goal_Home'] = database_flashscore_filtered2.apply(lambda row: determine_first_goal_range(row, 'Goals_Minutes_Home'), axis=1)
database_flashscore_filtered2['First_Goal_Away'] = database_flashscore_filtered2.apply(lambda row: determine_first_goal_range(row, 'Goals_Minutes_Away'), axis=1)

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
    fig.update_layout(xaxis_title='Intervalo de Minutos', yaxis_title='Número de Jogos')
    st.plotly_chart(fig, use_container_width=True)

def calculate_stats(df):
    # Função auxiliar para encontrar o primeiro gol
    def first_goal_minutes(goals_list):
        if goals_list:
            return min(goals_list)
        return None
    
    # Encontrar o primeiro gol para cada time
    df['First_Goal_Minutes_Home'] = df['Goals_Minutes_Home'].apply(first_goal_minutes)
    df['First_Goal_Minutes_Away'] = df['Goals_Minutes_Away'].apply(first_goal_minutes)
    
    # Calcular média e desvio padrão
    mean_home = df['First_Goal_Minutes_Home'].mean()
    std_home = df['First_Goal_Minutes_Home'].std()
    
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


        
        