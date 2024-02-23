import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px 
import plotly.graph_objs as go
from geopy.geocoders import Nominatim

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

con_type =filtered_df['Product Container'].unique()
selectcontype = st.sidebar.multiselect("Select Product Container :", con_type, default=con_type)
filtered_df =filtered_df[filtered_df['Product Container'].isin(selectcontype)]




st.write(filtered_df)

tab1,tab2 = st.tabs(['Number Of Sales By City',"Number Of Sales by State"])
with tab1 :
    City = filtered_df['City'].value_counts()
    fig = px.pie(names=City.index, values=City.values,
                hover_data={'City': City.index})
    st.plotly_chart(fig)

# with tab2: 

#     data = {'City': ['New York', 'Los Angeles', 'Chicago', 'Houston'],
#         'Total Orders': [1000, 800, 600, 400]}
#     df = pd.DataFrame(data)

#     # Create a scatter plot
#     fig = px.scatter(df, x=df.index, y='Total Orders', text='City', size='Total Orders', 
#                     title='Total Orders by City', labels={'x': 'City Index', 'y': 'Total Orders'})
#     fig.show()
    # filtered_df = df[df['City'] == 'Melbourne']
    # Suburb = filtered_df['Suburb'].value_counts()
    # fig = px.pie(names=Suburb.index, values=Suburb.values,
    #             hover_data={'Suburb': Suburb.index})
    # fig = px.bar(x=Suburb.index, y=Suburb.values,
    #          hover_data={'Suburb': Suburb.index})
    # fig = px.scatter_mapbox(filtered_df, lat='Latitude', lon='Longitude', hover_data=['Suburb'],
    #                     zoom=10, height=300)
    # fig.update_layout(mapbox_style="carto-positron")
    # st.plotly_chart(fig)

# df['Order Date'] = pd.to_datetime(df['Order Date'])
# df['Order Date'] = pd.to_datetime(df['Order Date'])


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


col3,col4= st.columns([1,1])

with col3 : 
    min_date = df['Order Date'].min()
    max_date = df['Order Date'].max()
    
    start_date = st.date_input("Start date", min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.date_input("End date", min_value=min_date, max_value=max_date, value=max_date)
    start_date = np.datetime64(start_date)
    end_date = np.datetime64(end_date)
    filtered_df = filtered_df[(filtered_df['Order Date'] >= start_date) & (filtered_df['Order Date'] <= end_date)]


col1,col2,col3 = st.columns([1,1,1])

with col1 :
    rev_df= filtered_df
    total_value =rev_df['Total'].sum()
    total_value =  '{:,.0f}'.format(total_value)

    st.metric(label="Total Revenue :", value=total_value+ " $" )
    
with col2 : 
    order_df = filtered_df
    total_order = order_df.size
    st.metric(label="Total Order :", value=total_order )

with col3 :
    date_start =filtered_df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d-%m-%Y')
    date_end =filtered_df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d-%m-%Y')
    avg_date= ((date_end-date_start).dt.total_seconds() / 3600).mean()
    avg_date=round(avg_date, 2)
    avg_date_difference_str = str(avg_date)

    st.metric(label="Avg Order To Shipment  :", value=avg_date_difference_str +" hour" )
