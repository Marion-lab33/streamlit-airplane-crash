import pandas as pd
import streamlit as st
import seaborn as sns
import plotly.express as px


df = pd.read_csv("assets/Plane_crashes.csv")

df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.strftime('%Y')
df['Month'] = df['Date'].dt.strftime('%B')

# Titre de la page
st.title("Coucou Léa !!")

# Header part 1
st.header('Partie 1 !!!!', divider='rainbow')

series_crash = df['Crash cause'].value_counts()
df_crash = pd.DataFrame({'Crash cause': series_crash.index, 'Count': series_crash.values})

st.bar_chart(df_crash, x = 'Crash cause', y = 'Count', color=None, width=0, height=0, use_container_width=True)

# Header part 2
st.header('Partie 2 !!!!', divider='rainbow')

fig = px.histogram(df, x="Year")
st.plotly_chart(fig)

# Liste déroulante
option = st.selectbox(
    'Avec quelle variable voulez-vous comparer le nombre de victimes ?',
    ('Région', 'Lieu de crash', 'Mobile phone'))


# OLD Filtre le DataFrame en fonction du bouton sélectionné
# if us_button:
#     filtered_cars = cars[cars['continent'] == 'US']
# elif europe_button:
#     filtered_cars = cars[cars['continent'] == 'Europe']
# elif japan_button:
#     filtered_cars = cars[cars['continent'] == 'Japan']
# elif all_button:
#     filtered_cars = cars
# else:
#     filtered_cars = cars


# Header part 2 OLD
st.header('Partie 2', divider='rainbow')
# viz_correlation = sns.heatmap(filtered_cars.select_dtypes(include=['int', 'float']).corr(), center=0, cmap=sns.color_palette("vlag", as_cmap=True))
# st.pyplot(viz_correlation.figure)

# Header part 3 OLD
# st.header('Scatterplot', divider='rainbow')
# st.scatter_chart(filtered_cars, x='cubicinches', y='weightlbs')

# Header part 3
# st.header('Scatterplot', divider='rainbow')
# st.scatter_chart(filtered_cars, x='cubicinches', y='weightlbs')