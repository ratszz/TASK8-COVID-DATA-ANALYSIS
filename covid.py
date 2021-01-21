import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from streamlit_folium import folium_static
import folium
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import chart_studio.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs,init_notebook_mode,plot,iplot
url="https://covid.ourworldindata.org/data/owid-covid-data.csv"
df_=pd.read_csv(url)
df=df_.copy()
a=df.isnull().sum()/len(df)*100
variables=df.columns
variable=[]
for i in range(len(variables)):
  if a[i]<30:
    variable.append(variables[i])
df=df.loc[:,variable]
#df.dropna(inplace=True)
df["date"]=pd.to_datetime(df["date"])

st.title("COVID-19 Data Analysis")
st.sidebar.title("COUNTRY")
select = st.sidebar.selectbox('Area', ['Albania', 'Algeria', 'Argentina', 'Australia', 'Austria',
       'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados',
       'Belarus', 'Belgium', 'Benin', 'Bosnia and Herzegovina',
       'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso',
       'Canada', 'Cape Verde', 'Chile', 'China', 'Colombia', 'Costa Rica',
       'Croatia', 'Cyprus', 'Czechia', 'Denmark', 'Djibouti',
       'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Eritrea',
       'Estonia', 'Eswatini', 'Ethiopia', 'Finland', 'France', 'Gambia',
       'Georgia', 'Germany', 'Ghana', 'Greece', 'Haiti', 'Hungary',
       'Iceland', 'India', 'Indonesia', 'Iran', 'Ireland', 'Israel',
       'Italy', 'Jamaica', 'Japan', 'Kazakhstan', 'Kenya', 'Kuwait',
       'Kyrgyzstan', 'Latvia', 'Lebanon', 'Liberia', 'Lithuania',
       'Luxembourg', 'Malawi', 'Malaysia', 'Mali', 'Malta', 'Mauritius',
       'Mexico', 'Moldova', 'Mongolia', 'Morocco', 'Mozambique',
       'Myanmar', 'Nepal', 'Netherlands', 'New Zealand', 'Niger',
       'Norway', 'Oman', 'Pakistan', 'Panama', 'Paraguay', 'Philippines',
       'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia', 'Saudi Arabia',
       'Seychelles', 'Singapore', 'Slovakia', 'Slovenia', 'South Africa',
       'South Korea', 'Spain', 'Sri Lanka', 'Suriname', 'Sweden',
       'Switzerland', 'Tanzania', 'Thailand', 'Togo', 'Tunisia', 'Turkey',
       'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom',
       'United States', 'Uruguay', 'Uzbekistan', 'Vietnam', 'Yemen',
       'Zambia', 'Zimbabwe'], key='1')

group_f=df_.groupby(["iso_code","location"],as_index=False)[["total_deaths","total_cases"]].sum()
init_notebook_mode(connected=True)
data=dict(type='choropleth',
          locations=group_f["iso_code"],
          z=group_f["total_cases"],
          text=group_f["location"],
          colorbar={"title":"Total Covid Cases"})
layout=dict(title="Total Covid Cases all over the world",
            geo=dict(showframe=False,
                     projection={'type':'winkel tripel'}))
choromap=go.Figure(data=[data],layout=layout)
choromap.update_layout(height=650,width=1000, margin={"r":0,"t":0,"l":0,"b":0})
st.title("Total Cases all over the world")
st.plotly_chart(choromap)
temp=df[['iso_code', 'continent', 'location', 'date', 'total_cases', 'total_deaths','new_cases','total_cases_per_million','new_deaths_per_million','total_deaths_per_million',
       'new_cases_per_million','stringency_index', 'population','median_age', 'aged_65_older', 'aged_70_older',
       'gdp_per_capita', 'diabetes_prevalence','hospital_beds_per_thousand', 'life_expectancy',
       'human_development_index','cardiovasc_death_rate']]


group5=df_.groupby("location",as_index=False).agg({"total_cases":"sum","total_deaths":"sum","date":["max","min"]})
t=group5[group5["location"]==select]
st.title("Covid Data")
st.markdown("Select the country from the sidebar")
st.write("Currently, its ",select)
st.write("Total Cases from date {} to {}: {}".format(t.loc[:,"date"].loc[:,"min"].values[0],t.loc[:,"date"].loc[:,"max"].values[0],int(t.loc[:,"total_cases"].values[0])))
st.write("Total Deaths from date {} to {}: {}".format(t.loc[:,"date"].loc[:,"min"].values[0],t.loc[:,"date"].loc[:,"max"].values[0],int(t.loc[:,"total_deaths"].values[0])))


group1=temp.groupby("location",as_index=False)[["total_cases"]].sum()
group1.sort_values(by="total_cases",axis=0,ascending=False,inplace=True)
group1=group1[1:11]
fig1= px.bar(group1, y='total_cases', x='location',color="location")
st.title("Top 10 Countries with highest number of cases")
st.plotly_chart(fig1)

group2=temp.groupby("location",as_index=False)[["total_deaths"]].sum()
group2.sort_values(by="total_deaths",inplace=True,ascending=False)
group2=group2[1:11]
fig2= px.bar(group2, x='location', y='total_deaths',color="location")
st.title("Top 10 Countries with highest number of Deaths due to covid")
st.plotly_chart(fig2)

group4=temp.groupby("location",as_index=False)['aged_65_older', 'aged_70_older','total_deaths_per_million'].sum()
group4["Above 60"]=group4["aged_65_older"]+group4["aged_70_older"]
group4.drop(['aged_65_older', 'aged_70_older'],axis=1,inplace=True)
group4.sort_values(by="Above 60",inplace=True,ascending=False)
#group4=group4[:10]
fig4= px.scatter(x=group4["Above 60"], y=group4["total_deaths_per_million"],color=group4["location"], labels={'x':'No. of people above 60', 'y':'Total Deaths'})
#st.title("Top 10 countries with highest aged population")
st.title("Population Above 60 vs Total Deaths per million")
st.plotly_chart(fig4)


group3=temp.groupby("location",as_index=False).agg({"gdp_per_capita":"mean","life_expectancy":"mean"})
group3.sort_values(by="gdp_per_capita",inplace=True,ascending=False)
group3=group3[:15]
fig3 = px.scatter(group3, x='gdp_per_capita', y='life_expectancy',color="location")
st.title("GDP vs Life Expectancy of Top 15 countries having highest GDP per Capita")
st.plotly_chart(fig3)

group5=temp.groupby("location",as_index=False).agg({"hospital_beds_per_thousand":"mean","life_expectancy":"mean"})
group5.sort_values(by="hospital_beds_per_thousand",inplace=True,ascending=False)
#group5=group5[:15]
fig5 = px.scatter(group5, x='hospital_beds_per_thousand', y='life_expectancy',color="location")
st.title("Hospital beds per thousand vs life expectancy")
st.write("Top 15 countries having highest number of Hospital beds per thousand are used here for clear visualisation")
st.plotly_chart(fig5)

group6=temp.groupby("location",as_index=False).agg({"diabetes_prevalence":"mean","life_expectancy":"mean"})
group6.sort_values(by="diabetes_prevalence",inplace=True,ascending=False)
group6=group6[:15]
fig6 = px.scatter(group6, x='diabetes_prevalence', y='life_expectancy',color="location")
st.title("Diabetes Prevalence vs Life expectancy")
st.write("Top 15 countries having highest number of Diabetes Prevalence are used here for clear visualisation")
st.plotly_chart(fig6)
