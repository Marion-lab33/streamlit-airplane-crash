import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

df = pd.read_csv("assets/Plane_crashes.csv")

# Titre de la page + texte
st.title("Les accidents aériens depuis 1908")
st.text('Ici on peut écrire une petite description du projet')

############################################ DEBUT LEA ###############################################
# Header part 1
st.subheader("Titre partie", divider='gray')

df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.strftime('%Y')
df['Month'] = df['Date'].dt.strftime('%B')

# Graphique 1 : Répartition du nombre de crashs en fonction des années
fig = px.histogram(df, x="Year")
fig.update_layout(
    title_text='Répartition du nombre de crashs en fonction des années', # title of plot
    xaxis_title_text='Année', # xaxis label
    yaxis_title_text='Nombre de crashs', # yaxis label
    bargap=0.2,
    bargroupgap=0.1,
)
st.plotly_chart(fig)
# Graphique 2 : Répartition du nombre de crashs en fonction des années et des régions du monde
fig = px.histogram(df, x="Year", color="Region")
fig.update_layout(
    title_text='Répartition du nombre de crashs en fonction des années et des continents du monde', # title of plot
    xaxis_title_text='Année', # xaxis label
    yaxis_title_text='Nombre de crashs', # yaxis label
    bargap=0.2,
    bargroupgap=0.1,
    width=800
)
st.plotly_chart(fig)
# Graphique 3 : Nombre de crashs par mois et par année en fonction des régions du monde
ordered_months = ["January", "February", "March", "April", "May", "June",
      "July", "August", "September", "October", "November", "December"]# sorting data accoring to ordered_months
df['to_sort']=df['Month'].apply(lambda x:ordered_months.index(x))
df_month = df.sort_values(['to_sort', 'Year'])
fig = px.histogram(df_month, x="Month", barmode='group', animation_frame='Year')
fig.update_yaxes(range=[0, 40])
fig.update_layout(
    title_text='Nombre de crashs par mois et par année en fonction des continents du monde', # title of plot
    xaxis_title_text='Mois', # xaxis label
    yaxis_title_text='Nombre de crashs', # yaxis label
    width=800
)
st.plotly_chart(fig)
# Graphique 4 : Nombre de crashs par mois et par année en fonction des régions du monde
fig = px.scatter(df, x="Year", y="Total fatalities", size="Total fatalities", color="Region", size_max=60)
fig.update_layout(
    title_text='Nombre total de décès par année et par continent', # title of plot
    xaxis_title_text='Année', # xaxis label
    yaxis_title_text='Nombre total de décès', # yaxis label
    width=800
)
st.plotly_chart(fig)# DATAFRAME Countries Lat / Lon
df_countries = pd.read_csv("assets/countries.csv")
df = pd.merge(df,
              df_countries,
              how = "inner",
              left_on = "Country",
              right_on ="name")
df_final = df[['Country', 'latitude', 'longitude', 'Crash cause']]
st.map(df, size=20, color='#0044FF')

############################################ FIN LEA ####################################################################


# Header part
st.subheader("Analyse des causes d'accidents aériens", divider='gray')

# Données pour le graph de la partie 1
series_crash = df['Crash cause'].value_counts()
df_crash = pd.DataFrame({'Crash cause': series_crash.index, 'Count': series_crash.values})

col1, col2 = st.columns([2.5, 1.5])
fig = px.bar(df_crash.sort_values(by='Count', ascending=True), x='Crash cause', y='Count')
fig.update_layout(
title_text='Distribution des causes de crash', 
yaxis_title_text='Nb de crashs', 
bargap=0.1,
width=450,
height=350
)
col1.plotly_chart(fig)

col2.markdown("##### Interprétation")
col2.write("Ici on écrit le texte")

# Header part 2
st.subheader('Corrélations entre le nombre de décès et les autres variables', divider='gray')

# Données préparation pour les graphs de la partie 2
df_gravity = df[['Total fatalities', 'Region', 'Crash site', 'Crash cause', 'Flight type', 'Flight phase']]
df_by_region = df_gravity.groupby('Region')['Total fatalities'].sum().reset_index()
df_by_crashsite = df_gravity.groupby('Crash site')['Total fatalities'].sum().reset_index()
df_by_crashsite.at[0, 'Crash site'] = "Airport (or less than 10km)"
df_by_crashcause= df_gravity.groupby('Crash cause')['Total fatalities'].sum().reset_index()
df_by_fighttype = df_gravity.groupby('Flight type')['Total fatalities'].sum().reset_index()
df_by_fighttype.at[6, 'Flight type'] = "Charter/Taxi"
df_by_fightphase = df_gravity.groupby('Flight phase')['Total fatalities'].sum().reset_index()

# Division en 2 colonnes
col1, col2 = st.columns([1.5, 2.5])

# Liste déroulante
option = col1.selectbox(
    'Avec quelle variable voulez-vous comparer le nombre de décès ?',
    ('Continent', 'Lieu du crash', 'Cause du crash', 'Type de vol', 'Phase du vol'))

# Affiche le graph en fonction de la variable sélectionnée
if option == 'Continent':
    fig = px.bar(df_by_region.sort_values(by='Total fatalities', ascending=True), x='Total fatalities', y='Region')
    fig.update_layout(
    title_text='Nombre de crashs en fonction du continent', 
    xaxis_title_text='Nb de crashs', 
    bargap=0.1,
    width=450,
    height=390
    )
    col2.plotly_chart(fig)
elif option == 'Lieu du crash':
    fig = px.bar(df_by_crashsite.sort_values(by='Total fatalities', ascending=True), x='Total fatalities', y='Crash site')
    fig.update_layout(
    title_text='Nombre de crashs en fonction du lieu de crash', 
    xaxis_title_text='Nb de crashs', 
    bargap=0.1,
    width=450,
    height=350
    )
    col2.plotly_chart(fig)
elif option == 'Cause du crash':
    fig = px.bar(df_by_crashcause.sort_values(by='Total fatalities', ascending=True), x='Total fatalities', y='Crash cause')
    fig.update_layout(
    title_text='Nombre de crashs en fonction de la cause du crash', 
    xaxis_title_text='Nb de crashs', 
    bargap=0.1,
    width=450,
    height=350
    )
    col2.plotly_chart(fig)
elif option == 'Type de vol':
    fig = px.bar(df_by_fighttype.sort_values(by='Total fatalities', ascending=True), x='Total fatalities', y='Flight type')
    fig.update_layout(
    title_text='Nombre de crashs en fonction du type de vol', 
    xaxis_title_text='Nb de crashs', 
    bargap=0.1,
    width=450,
    height=650
    )
    col2.plotly_chart(fig)
elif option == 'Phase du vol':
    fig = px.bar(df_by_fightphase.sort_values(by='Total fatalities', ascending=True), x='Total fatalities', y='Flight phase')
    fig.update_layout(
    title_text='Nombre de crashs en fonction de la phase du vol', 
    xaxis_title_text='Nb de crashs', 
    bargap=0.1,
    width=450,
    height=280
    )
    col2.plotly_chart(fig)
