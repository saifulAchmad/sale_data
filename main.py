import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px 



df = pd.read_csv("data_source/cleaned_data3.csv",compression="gzip")
ts= df["Total"].sum()
# st.write(df)

default_value = "all"
filtered_df=df



Cat = df['Product Category'].drop_duplicates()

all_cat =filtered_df['Product Category'].unique()
selectcat = st.sidebar.multiselect("Select Product Category:", all_cat, default=all_cat)
filtered_df =filtered_df[filtered_df['Product Category'].isin(selectcat)] 

cust_type =filtered_df['Customer Type'].unique()
selectcustype = st.sidebar.multiselect("Select Customer Type :", cust_type, default=cust_type)
filtered_df =filtered_df[filtered_df['Customer Type'].isin(selectcustype)]   


st.write(filtered_df)

tab1,tab2 = st.tabs(['Number Of Sales By City',"Number Of Sales by State"])
with tab1 :
    City = filtered_df['City'].value_counts()
    fig = px.pie(names=City.index, values=City.values,
                hover_data={'City': City.index})
    st.plotly_chart(fig)

with tab2: 
    City = filtered_df['State'].value_counts()
    fig = px.pie(names=City.index, values=City.values,
                hover_data={'State': City.index})
    st.plotly_chart(fig)

df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Order Date'] = df['Order Date'].dt.strftime('%m/%y')
# df['Order Date'] = df['Order Date'].apply(lambda x: x[-5:])

total_unit_price_by_date =df.groupby(df['Order Date']).agg({'Retail Price': 'sum', 'Cost Price': 'sum'}).reset_index()
fig = px.line(total_unit_price_by_date, x='Order Date',  y=['Retail Price', 'Cost Price'])

st.plotly_chart(fig)