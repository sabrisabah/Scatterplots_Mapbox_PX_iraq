import numpy as np
import pandas as pd
import shapefile as shp
from datetime import datetime, timedelta
import json
import plotly.express as px
px.set_mapbox_access_token("pk.eyJ1Ijoic2Ficmk3OCIsImEiOiJja2J5Y2E2OXgwZnZ1MnpuNHJqaGt4YmF0In0.ioaJ1U3mhAmAuhbkt99ENg")

path_df = "C:/project/choropleth-python-Iraq/data/iraq.csv" #Source file 
path_gov = "C:/project/gov_xy/iraq.csv" #Coordination by province 
#---- Read file 
df = pd.read_csv(path_df)
iraq_gov = pd.read_csv(path_gov)
#----- Renamed as i wanted 
iraq_gov['dtname'] = iraq_gov['admin1Name']
df['dtname'] = df['Health admin']
result = pd.merge(iraq_gov,df, on='dtname', how='inner')
result['Confirmed'] = result['New Cases']
result['Deaths'] = result['New Deaths']
result['Lat'] = result['x']
result['Long'] = result['y']
#----- Cumulative
result['Cumulative_Cases'] = result['Confirmed'].cumsum(axis=0)
result['Cumulative_Deaths'] = result['New Deaths'].cumsum(axis=0)


result.drop(['Health admin','Cumulative Deaths','Cumulative Cases','admin1Name','New Cases','New Deaths','x','y'],inplace=True, axis=1)

fig = px.scatter_mapbox(result, lat="Lat", lon="Long", 
	animation_frame = 'Date', animation_group = 'dtname', 
	color="Confirmed", size="Confirmed", 
	color_continuous_scale=px.colors.diverging.Picnic, #px.colors.cyclical.IceFire,
    size_max=70, zoom=4.5, hover_name='dtname', 
    hover_data = ['Cumulative_Cases', 'Cumulative_Deaths'], 
    title = 'Visualizing spread of COVID Confirmed Cases and Deaths cases 22/1/2020 until today')
fig.write_html("C:/project/Plotly_express_scatter/output/index.html")
fig.show()

