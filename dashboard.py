
# Import libraries
import pandas as pd
import streamlit as st
import plotly.express as px
from pyjstat import pyjstat
import requests

#=====>>> Dashboard title
st.title('Airport passenger traffic in Norway')

#airport latitudes and longitudes
airport_coordinates = {'Oslo Gardermoen': (60.1939, 11.1004),
                       'Stavanger Sola': (58.8821, 5.6262),
                       'Bergen Flesland': (60.2934, 5.2186),
                       'Trondheim Værnes': (63.4578, 10.9234),
                       'Alta': (69.9765, 23.3717),
                       'Andenes Andøya': (69.2925, 16.1442),
                       'Bardufoss': (69.0558, 18.5403),
                       'Berlevåg': (70.8667, 29.0),
                       'Bodø': (67.2692, 14.3653),
                       'Brønnøysund Brønnøy': (65.4634, 12.2186),
                       'Båtsfjord': (70.6000, 29.6917),
                       'Fagernes Leirin': (61.0156, 9.2931),
                       'Florø': (61.5853, 5.0249),
                       'Førde Bringeland': (61.3922, 5.7643),
                       'Hammerfest': (70.6797, 23.6703),
                       'Harstad/Narvik Evenes': (68.4913, 16.6781),
                       'Hasvik': (70.4872, 22.1414),
                       'Haugesund Karmøy': (59.3456, 5.2083),
                       'Honningsvåg Valan': (71.0095, 25.9875),
                       'Kirkenes Høybuktmoen': (69.7250, 29.8917),
                       'Kristiansand Kjevik': (58.2007, 8.0853),
                       'Kristiansund Kvernberget': (63.1118, 7.8242),
                       'Lakselv Banak': (70.0681, 24.9733),
                       'Mehamn': (71.0297, 27.8269),
                       'Mo i Rana Røssvold': (66.3666, 14.3017),
                       'Molde Årø': (62.7447, 7.2628),
                       'Mosjøen Kjærstad': (65.7839, 13.2158),
                       'Namsos': (64.4722, 11.5783),
                       'Narvik Framnes': (68.4263, 17.3983),
                       'Notodden': (59.5662, 9.2122),
                       'Ørsta-Volda Hovden': (62.1783, 6.0756),
                       'Ørland': (63.7000, 9.6056),
                       'Rørvik Ryum': (64.8622, 11.2406),
                       'Sandane Anda': (61.8319, 6.1058),
                       'Sandnessjøen Stokka': (65.9558, 12.4675),
                       'Svalbard Longyear': (78.2461, 15.4656),
                       'Sogndal Haukåsen': (61.1564, 7.1364),
                       'Stokmarknes Skagen': (68.5789, 15.0333),
                       'Svolvær Helle': (68.2333, 14.5667),
                       'Tromsø Langnes': (69.6833, 18.9189),
                       'Vadsø': (70.0650, 29.8447),
                       'Vardø Svartnes': (70.3708, 31.1103),
                       'Vestvågøy Leknes': (68.1522, 13.6092),
                       'Værøy': (67.6678, 12.6839),
                       'Ålesund Vigra': (62.5647, 6.1197)}

#show airports on map
df_map = pd.DataFrame.from_dict(airport_coordinates, 
                                orient='index', 
                                columns=['lat', 'lon'])
df_map['airport'] = df_map.index

#generate plotly map using airport_coordinates
def generate_plotly_map():
    df = pd.DataFrame.from_dict(airport_coordinates, 
                                orient='index', 
                                columns=['lat', 'lon'])
    df['airport'] = df.index
    fig = px.scatter_mapbox(df, 
                            lat="lat", 
                            lon="lon", 
                            hover_name="airport",
                            #caption ='Airports in Norway', 
                            hover_data= {"airport": True, 
                                         "lat": False, 
                                         "lon": False},
                            zoom=3,
                            height=400)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    # Set the marker symbol and color
    fig.update_traces(marker={'color': 'red', 'size': 10})

    return fig

fig_map = generate_plotly_map()

#=====>>> Show airports on map
st.subheader('Airports in Norway')
st.plotly_chart(fig_map)

#json query from Statbank API 
#taken from https://github.com/janbrus/ssb-api-python-examples/blob/master/jsonstatToPandas_function-en.ipynb
api_query = {
  "query": [
    {
      "code": "Lufthavn",
      "selection": {
        "filter": "item",
        "values": [
          "ENGM",
          "ENZV",
          "ENBR",
          "ENVA",
          "ENAT",
          "ENAN",
          "ENDU",
          "ENBV",
          "ENBO",
          "ENBN",
          "ENBS",
          "ENFG",
          "ENFL",
          "ENBL",
          "ENHF",
          "ENEV",
          "ENHK",
          "ENHD",
          "ENHV",
          "ENKR",
          "ENCN",
          "ENKB",
          "ENNA",
          "ENMH",
          "ENRA",
          "ENML",
          "ENMS",
          "ENRY",
          "ENNM",
          "ENNK",
          "ENNO",
          "ENRO",
          "ENRM",
          "ENRS",
          "ENSD",
          "ENTO",
          "ENST",
          "ENSN",
          "ENSG",
          "ENSK",
          "ENSO",
          "ENSB",
          "ENSH",
          "ENSR",
          "ENTC",
          "ENVD",
          "ENSS",
          "ENLK",
          "ENVR",
          "ENOL",
          "ENOV",
          "ENAL"
        ]
      }
    },
    {
      "code": "TrafikkType",
      "selection": {
        "filter": "item",
        "values": [
          "08"
        ]
      }
    },
    {
      "code": "TrafikkFly",
      "selection": {
        "filter": "item",
        "values": [
          "IU"
        ]
      }
    },
    {
      "code": "FlyBevegelse",
      "selection": {
        "filter": "item",
        "values": [
          "00"
        ]
      }
    },
    {
      "code": "ContentsCode",
      "selection": {
        "filter": "item",
        "values": [
          "Flybevegelser"
        ]
      }
    }
  ],
  "response": {
    "format": "json-stat2"
  }
};

# post request to Statbank API URL
postUrl = "https://data.ssb.no/api/v0/en/table/08503/"

#function to convert json into dataframe 
def api_to_df(postUrl, query):
    response = requests.post(postUrl, json=query)
    # put the response in variable ds that has metadata and data
    ds = pyjstat.Dataset.read(response.text)
    df = ds.write('dataframe')
    
    return df

df = api_to_df(postUrl, api_query)

#======>>> Show dataframe
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(df.head(10))

#get a copy of the dataframe
df1 = df.copy()

#convert column dtypes to string
#last one is int64
def convert_to_string(df):
    df.iloc[:, :-1] = df.iloc[:, :-1].astype("string")
    df.iloc[:, -1] = df.iloc[:, -1].astype("int64")
    return df

df2 = convert_to_string(df1)

#convert date column to datetime
def convert_date(df):
    # use string methods to extract year and month from the date column
    df['year'] = df['month'].str[:4]
    df['month'] = df['month'].str[-2:]

    # use pandas to create a datetime object for the last day of each month
    df['date'] = pd.to_datetime(df['year'] + df['month'] + '01', format='%Y%m%d') + pd.offsets.MonthEnd(1)

    # convert year and month columns to integers
    df['year'] = df['year'].astype(int)
    df['month'] = df['month'].astype(int)

    #drop unwanted columns
    df.drop(
    columns=['type of traffic', 
             'domestic/international flights',
             'aircraft movement', 'contents'], inplace=True)

    return df

df_new = convert_date(df2)

#function to groupby airport and year
def group_by(df):
    df_gr = df.groupby(
    ["airport", 
     pd.Grouper(key="date", freq="Y")]
     )\
    ["value"].sum()\
    .reset_index()

    #set date column as index
    df_gr.set_index('date', inplace=True)

    return df_gr

df_gr = group_by(df_new)

#======>>> Show grouped airport and year data on chart
st.subheader('Annual airport passengers in all airports in Norway')
# Get a list of color codes based on the number of unique airports
num_colors = len(df_gr['airport'].unique())
color_sequence = px.colors.qualitative.Dark24[:num_colors]

#create an interactive plot using plotly
fig1 = px.scatter(df_gr, x=df_gr.index, y='value', 
                 size='value',
                 color='airport', 
                 color_discrete_sequence=color_sequence,
                 hover_data=["airport", "value"],
                 title='Air passengers in Norway')

# Customize the chart layout
fig1.update_layout(
    xaxis_title='',
    yaxis_title='Number of passengers',
    legend_title='Airport',
    hovermode='closest',
    hoverlabel=dict(
        bgcolor="white",
        font_size=17,
        font_family="Arial"
    ),
    font=dict(
        family="Arial",
        size=17
    ),
    height=500, width=800
)

# Show the chart in app
st.plotly_chart(fig1, theme=None)

#======>>> Show grouped airport and year data on chart
filteredAirport = st.selectbox('airport', df_gr['airport'].unique())
filteredAirport = df_gr[df_gr['airport'] == filteredAirport]
st.subheader('Annual passengers per airport')

#get the name of the airport
airport_name = filteredAirport['airport'].unique()[0]

fig2 = px.scatter(filteredAirport, x=filteredAirport.index, y='value', 
                 size='value',
                 color='airport', 
                 color_discrete_sequence=color_sequence,
                 hover_data=["airport", "value"],
                 title=f'Air passengers in {airport_name}')

#Customize the chart layout
fig2.update_layout(
    xaxis_title='',
    yaxis_title='Number of passengers',
    legend_title='Airport',
    hovermode='closest',
    hoverlabel=dict(
        bgcolor="white",
        font_size=17,
        font_family="Arial"
    ),
    font=dict(
        family="Arial",
        size=17
    ),
    height=500, width=800
)

# Show the chart in app
st.plotly_chart(fig2, theme=None)

#======>>> Show grouped airport data per year
filteredYear = st.selectbox('year', df_new['year'].unique())
filteredYear = df_new[df_new['year'] == filteredYear]
filteredYear.set_index('date', inplace=True)
print(filteredYear.head(2))
st.subheader('Annual passengers per year')

fig3 = px.scatter(filteredYear, x=filteredYear.index, y='value', 
                 size='value',
                 color='airport', 
                 color_discrete_sequence=color_sequence,
                 hover_data=["airport", "value"],
                 title=f'Air passengers in {filteredYear["year"][0]}')

#Customize the chart layout
fig3.update_layout(
    xaxis_title='',
    yaxis_title='Number of passengers',
    xaxis_tickformat = '%b',
    legend_title='Airport',
    hovermode='closest',
    hoverlabel=dict(
        bgcolor="white",
        font_size=17,
        font_family="Arial"
    ),
    font=dict(
        family="Arial",
        size=17
    ),
    height=500, width=800
)

# Show the chart in app
st.plotly_chart(fig3, theme=None)

#======>>> Show total passengers
st.subheader('Total passengers')

#access first and last year in the dataframe
start_yr = df_new["date"].dt.year.min()
end_yr = df_new["date"].dt.year.max()

#integrated airport passengers per airport
df_top_airport = pd.DataFrame(df_new.groupby('airport')['value']\
    .sum()\
        .sort_values(ascending=False))
#change column name
df_top_airport.columns = ['total passengers']

fig4 = px.bar(df_top_airport, 
              x=df_top_airport.index, 
              y='total passengers',
                #color='total passengers',
                #color_continuous_scale=px.colors.sequential.Reds,
                title=f'Total passengers: {start_yr} - {end_yr}')

# Customize the chart layout
fig4.update_layout(
    xaxis_title='',
    yaxis_title='Number of passengers',
    legend_title='Airport',
    hovermode='closest',
    hoverlabel=dict(
        bgcolor="white",
        font_size=17,
        font_family="Arial"
    ),
    font=dict(
        family="Arial",
        size=17
    ),
    height=400, width=800
)

# Show the chart in app
st.plotly_chart(fig4, theme=None)
