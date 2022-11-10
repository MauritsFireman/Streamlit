#Link van de dataset
#https://www.kaggle.com/datasets/fedesoriano/gender-pay-gap-dataset

#alle Pips
#!pip install kaggle


#Alle imports
from platform import java_ver
import requests
import pandas as pd
import zipfile
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import json





#API Inladen
#!kaggle datasets download -d fedesoriano/gender-pay-gap-dataset
#with zipfile.ZipFile("gender-pay-gap-dataset.zip","r") as zip_ref:
#    zip_ref.extractall()
#!kaggle datasets download -d fedesoriano/gender-pay-gap-dataset
#with zipfile.ZipFile("gender-pay-gap-dataset.zip","r") as zip_ref:
#    zip_ref.extractall()


#CODE
pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)



#Main DF goedmaken
df1 = pd.read_csv('1.csv')
df2 = pd.read_csv('2.csv')
df3 = pd.read_csv('3.csv')
df4 = pd.read_csv('4.csv')


df = pd.concat([df1, df2,df3,df4])




#DF van het gemiddelde uren gewerkt
df_hrswork_mean = df.groupby(['year','geslacht'])['hrswork'].mean().round(1)
df_hrswork_mean = pd.DataFrame(df_hrswork_mean, index=None)
df_hrswork_mean['year'] = df_hrswork_mean.index.get_level_values(0)
df_hrswork_mean['geslacht'] = df_hrswork_mean.index.get_level_values(1)

#DF van de Gemiddelde jaarinkomen
df_niincwage_mean = df.groupby(['year','geslacht'])['niincwage'].mean().round(1)
df_niincwage_mean = pd.DataFrame(df_niincwage_mean, index=None)
df_niincwage_mean['year'] = df_niincwage_mean.index.get_level_values(0)
df_niincwage_mean['geslacht'] = df_niincwage_mean.index.get_level_values(1)

#DF van de Gemiddelde uurloon aangepast naar inflatie
df_realhrwage_mean = df.groupby(['year','geslacht'])['realhrwage'].mean().round(1)
df_realhrwage_mean = pd.DataFrame(df_realhrwage_mean, index=None)
df_realhrwage_mean['year'] = df_realhrwage_mean.index.get_level_values(0)
df_realhrwage_mean['geslacht'] = df_realhrwage_mean.index.get_level_values(1)

#DF van de gemiddelde uren gewerkt per jaar
df_annhrs_mean = df.groupby(['year','geslacht'])['annhrs'].mean().round(1)
df_annhrs_mean = pd.DataFrame(df_annhrs_mean, index=None)
df_annhrs_mean['year'] = df_annhrs_mean.index.get_level_values(0)
df_annhrs_mean['geslacht'] = df_annhrs_mean.index.get_level_values(1)

#Plaatjes van fig 1 t/m 4
fig1 = px.bar(df_realhrwage_mean, x='year', y='realhrwage', color='geslacht', barmode='group')
fig1.update_layout(title="Histogram van de geslachten")
#fig1.show()

fig2 = px.bar(df_hrswork_mean, x='year', y='hrswork', color='geslacht', barmode='group')
fig2.update_layout(title="Histogram van de geslachten")
#fig2.show()

fig3 = px.bar(df_niincwage_mean, x='year', y='niincwage', color='geslacht', barmode='group')
fig3.update_layout(title="Histogram van de geslachten")
#fig3.show()

fig4 = px.bar(df_annhrs_mean, x='year', y='annhrs', color='geslacht', barmode='group')
fig4.update_layout(title="Histogram van de geslachten")
#fig4.show()

#begin streamlit
sidebar = st.sidebar.radio('kies', (('Intro', 'Analyse','Kaart','Conclusie')))


#STREAMLITT
if sidebar == 'Intro':
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)
    st.plotly_chart(fig3)
    st.plotly_chart(fig4)
elif sidebar == 'Analyse':
    jaar = st.select_slider('Selecteer een jaartal', options=[1981, 1990,1999,2007,2009,2011,2013], label_visibility='visible')
        #DF filteren op jaar 1999
    df_jaar = df[df['year'] == jaar]

    #DF van gemiddelde gewerkte uren per jaar per geslacht
    df1999_annhrs_mean = df_jaar.groupby(['geslacht','beroep'])['annhrs'].mean().round(1)
    df1999_annhrs_mean = pd.DataFrame(df1999_annhrs_mean, index=None)
    df1999_annhrs_mean['geslacht'] = df1999_annhrs_mean.index.get_level_values(0)
    df1999_annhrs_mean['beroep'] = df1999_annhrs_mean.index.get_level_values(1)

    #Df van de Gemiddelde uurloon per geslacht
    df1999_hrwage_mean = df_jaar.groupby(['geslacht','beroep'])['hrwage'].mean().round(1)
    df1999_hrwage_mean = pd.DataFrame(df1999_hrwage_mean, index=None)
    df1999_hrwage_mean['geslacht'] = df1999_hrwage_mean.index.get_level_values(0)
    df1999_hrwage_mean['beroep'] = df1999_hrwage_mean.index.get_level_values(1)

    #Plaatjes van fig 5 t/m 10
    fig5 = px.scatter(data_frame=df_jaar, x='annhrs', y='hrwage', color='beroep', height=900, width=1000,
                    labels={
                     "annhrs": "Uren",
                     "hrwage": "Uurloon ($)"
                 },title="Uurloon t.o.v. jaarlijkse gewerkte uren per beroepsgroep")
    #fig5.show()

    fig6 = px.box(data_frame=df_jaar, x='annhrs', y='beroep', color='beroep', height=900, width=1000, points='suspectedoutliers',
                    labels={
                     "annhrs": "Uren"
                 },title="Gemiddeld aantal uren per beroepsgroep")
    fig6.add_vline(x=df_jaar.annhrs.median(), line_width=3, line_dash="dash", line_color="green")
    #fig6.show()


    fig9 = px.bar(df1999_annhrs_mean, x='beroep', y='annhrs', color='geslacht', barmode='group', width=1000,
                    labels={
                     "annhrs": "Uren"
                 },title="Gewerkte uren per beroepsgroep per geslacht")
    #fig9.show()

    fig10 = px.bar(df1999_hrwage_mean, x='beroep', y='hrwage', color='geslacht', barmode='group', width=1000,
                    labels={
                     "hrwage": "Uurloon ($)"
                 },title="Uurloon per beroepsgroep per geslacht")
    #fig10.show()
    st.plotly_chart(fig5)
    st.plotly_chart(fig6)
    st.plotly_chart(fig9)
    st.plotly_chart(fig10)
elif sidebar == 'Kaart':
    jaar = st.select_slider('Selecteer een jaartal', options=[1981, 1990,1999,2007,2009,2011,2013], label_visibility='visible')
    df_jaar = df[df['year'] == jaar]
    #DF jaarlijkse gewerkte uren per staat
    df_2 = df_jaar.groupby('stusps')['annhrs'].mean().round(1)
    df_2 = pd.DataFrame(df_2)
    print(df_2)
    #df_2['stusps'] = df_2['stusps'].str.strip()
    df_2['stusps'] = df_2.index

    #DF Uurloon per staat
    df_3 = df_jaar.groupby('stusps')['hrwage'].median().reset_index().round(2)
    df_3 = pd.DataFrame(df_3)
    df_3['stusps'] = df_3['stusps'].str.strip()

    #DF verschil per geslacht in uurloon per staat 
    df_4 = df_jaar.groupby(['stusps','geslacht'])['hrwage'].mean().reset_index().round(2)
    df_4 = pd.DataFrame(df_4)
    df_4['stusps'] = df_4['stusps'].str.strip()
    df_4_wide = pd.pivot(df_4, index='stusps', columns = 'geslacht',values = 'hrwage')
    df_4_wide['verschil'] = df_4_wide['man']/df_4_wide['vrouw']


    #DF verschil per geslacht in jaarloon per staat
    df_5 = df_jaar.groupby(['stusps','geslacht'])['niincwage'].mean().reset_index().round(2)
    df_5 = pd.DataFrame(df_5)
    df_5['stusps'] = df_5['stusps'].str.strip()
    df_5_wide = pd.pivot(df_5, index='stusps', columns = 'geslacht',values = 'niincwage')
    df_5_wide['verschil'] = df_5_wide['man']/df_5_wide['vrouw']


    #DF verschil jaarlijkse gewerkte uren per geslacht per staat
    df_6 = df_jaar.groupby(['stusps','geslacht'])['annhrs'].mean().reset_index().round(2)
    df_6 = pd.DataFrame(df_6)
    df_6['stusps'] = df_6['stusps'].str.strip()
    df_6_wide = pd.pivot(df_6, index='stusps', columns = 'geslacht',values = 'annhrs')
    df_6_wide['verschil'] = df_6_wide['man']/df_6_wide['vrouw']

    #Fig 11 t/m 15
    fig11 = px.choropleth(df_2,
                        locations='stusps', 
                        locationmode="USA-states", 
                        scope="usa",
                        color='annhrs',
                        color_continuous_scale="Viridis_r",
                        width=900,
                        height=900,
                        labels={
                        "annhrs": "Uren"
                        },title="Gemiddelde gewerkte uren per staat" 
                        )
    #fig11.show()

    fig12 = px.choropleth(df_3,
                        locations='stusps', 
                        locationmode="USA-states", 
                        scope="usa",
                        color='hrwage',
                        color_continuous_scale="Viridis_r",
                        width=900,
                        height=900,
                        labels={
                        "hrwage": "loon ($)"
                        },title="Gemiddelde uurloon per staat" 
                        )
    #fig12.show()

    fig13 = px.choropleth(df_4_wide,
                        locations=df_4_wide.index, 
                        locationmode="USA-states", 
                        scope="usa",
                        color='verschil',
                        color_continuous_scale="Viridis_r",
                        width=1000,
                        height=1000,
                        labels={
                        "verschil": "Verhouding jaarlijks gewerkte uren man t.o.v. vrouw"
                        },title="Verhouding jaarlijks gewerkte uren man t.o.v. vrouw per staat" 
                        
                        )
    #fig13.show()

    fig14 = px.choropleth(df_5_wide,
                        locations=df_5_wide.index, 
                        locationmode="USA-states", 
                        scope="usa",
                        color='verschil',
                        color_continuous_scale="Viridis_r",
                        width=1000,
                        height=1000,
                        labels={
                        "verschil": "Verhouding jaarloon man t.o.v. vrouw"
                        },title="Verhouding jaarloon man t.o.v. vrouw per staat" 
                        )
    #fig14.show()

    fig15 = px.choropleth(df_6_wide,
                        locations=df_6_wide.index, 
                        locationmode="USA-states", 
                        scope="usa",
                        color='verschil',
                        color_continuous_scale="Viridis_r",
                        width=1000,
                        height=1000,
                        labels={
                        "verschil": "Uren"
                        },title="Gewerkte uren per beroepsgroep per geslacht"
                        )
    #fig15.show()
    st.plotly_chart(fig11)
    st.plotly_chart(fig12)
    st.plotly_chart(fig13)
    st.plotly_chart(fig14)
    st.plotly_chart(fig15)    







