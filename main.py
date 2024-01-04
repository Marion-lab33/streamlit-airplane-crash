import pandas as pd
import streamlit as st
import seaborn as sns

link = "https://raw.githubusercontent.com/murpi/wilddata/master/quests/cars.csv"
cars = pd.read_csv(link)
cars['continent'] = cars['continent'].str.replace(".", "").str.replace(" ", "")

# Titre de la page
st.title("Welcome to :blue[Marion\'s] app")

# Ajoute des boutons dans la barre latérale
with st.sidebar:
    st.header('Filter by Region')
    all_button = st.button("All")
    us_button = st.button("US")
    europe_button = st.button("Europe")
    japan_button = st.button("Japan")

# Filtre le DataFrame en fonction du bouton sélectionné
if us_button:
    filtered_cars = cars[cars['continent'] == 'US']
elif europe_button:
    filtered_cars = cars[cars['continent'] == 'Europe']
elif japan_button:
    filtered_cars = cars[cars['continent'] == 'Japan']
elif all_button:
    filtered_cars = cars
else:
    filtered_cars = cars

# Header part 1
st.header('DataFrame Cars', divider='rainbow')
st.write(filtered_cars)

# Header part 2
st.header('Heatmap', divider='rainbow')
viz_correlation = sns.heatmap(filtered_cars.select_dtypes(include=['int', 'float']).corr(), center=0, cmap=sns.color_palette("vlag", as_cmap=True))
st.pyplot(viz_correlation.figure)

# Header part 3
st.header('Scatterplot', divider='rainbow')
st.scatter_chart(filtered_cars, x='cubicinches', y='weightlbs')