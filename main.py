import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px 
import plotly.graph_objs as go


df = pd.read_csv("data_source/cleaned_data3.csv",compression="gzip")
# ts= df["Total"].sum()
# st.write(df)
df['Order Date'] = pd.to_datetime(df['Order Date'])
df = df.sort_values(by='Order Date')

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
    Suburb = filtered_df['Suburb'].value_counts()
    fig = px.pie(names=Suburb.index, values=Suburb.values,
                hover_data={'Suburb': Suburb.index})
    st.plotly_chart(fig)

# df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Order Date'] = pd.to_datetime(df['Order Date'])


tab3, tab4 = st.tabs(['Retail & Cost Price By Time','Total Order with Account Manager'])
Orderdf = filtered_df
with tab3 : 
   
    Orderdf.set_index('Order Date', inplace=True)
    Orderdf.resample('M').sum()
    Orderdf.reset_index(inplace=True)
    Orderdf['Order Date'] = df['Order Date'].dt.strftime('%m/%Y')
    Orderdf['Order Date']  = pd.to_datetime(Orderdf['Order Date'] , format='%m/%Y')
    Orderdf= Orderdf.sort_values(by='Order Date')


    total_unit_price_by_date =Orderdf.groupby(Orderdf['Order Date']).agg({'Retail Price': 'sum', 'Cost Price': 'sum'}).reset_index()
    # total_unit_price_by_date= total_unit_price_by_date.sort_values(by=["Order Date"], ascending=[True])
    fig = px.line(total_unit_price_by_date, x='Order Date',  y=['Retail Price', 'Cost Price'], title='Retail & Cost Price By Time')
    fig.update_xaxes(tickangle=45)

    st.plotly_chart(fig)
with tab4:  

    Orderdf.set_index('Order Date', inplace=True)
    Orderdf.resample('M').sum()
    Orderdf.reset_index(inplace=True)
    Orderdf['Order Date'] = df['Order Date'].dt.strftime('%m/%Y')
    Orderdf['Order Date']  = pd.to_datetime(Orderdf['Order Date'] , format='%m/%Y')
    Orderdf= Orderdf.sort_values(by='Order Date')

    total_order_by_date_manager = filtered_df.groupby(['Order Date', 'Account Manager']).size().reset_index(name='Total Order')

    total_order_by_date_manager_monthly = total_order_by_date_manager.groupby([pd.Grouper(key='Order Date', freq='M'), 'Account Manager']).agg({'Total Order': 'sum'}).reset_index()

    fig = px.bar(total_order_by_date_manager_monthly, x='Order Date', y='Total Order', color='Account Manager', )

    st.plotly_chart(fig)
    st.write(total_order_by_date_manager_monthly)

# Orderdf.set_index('Order Date', inplace=True)
# Orderdf.resample('M').sum()
# Orderdf.reset_index(inplace=True)
# Orderdf['Order Date'] = df['Order Date'].dt.strftime('%m/%Y')
# Orderdf['Order Date']  = pd.to_datetime(Orderdf['Order Date'] , format='%m/%Y')
# Orderdf= Orderdf.sort_values(by='Order Date')

col1,col2 = st.columns([1,1])

with col1 :
    rev_df= filtered_df
    
    st.metric(label="Price per unit Percentage Compared from previous data :", value=f"{price_change:.2f} %" )
