from typing import List, Any, Union

import requests
import pandas as pd

list_regions = [
    ["Abitibi - Témiscamingue", 47.6043795, -78.6754939],
    ["Bas-Saint-Laurent - Gaspésie - Îles-de-la-Madeleine", 48.1195325, -65.144312],
    ["Chaudière - Appalaches", 46.5946504, -71.4005985],
    ["Côte - Nord", 51.4145519, -68.0747842],
    ["Estrie", 45.4791239, -72.3281673],
    ["Laurentides - Lanaudière", 46.7095324, -75.0395335],
    ["Laval", 45.6059216, -73.7795483],
    ["Mauricie - Centre-du-Québec", 46.6545326, -73.1375643],
    ["Montérégie", 45.4899765, -73.5015834],
    ["Montréal", 45.5579564, -73.8703839],
    ["Nord-du-Québec", 55.4368108, -80.4954051],
    ["Outaouais", 46.4942268, -76.2270059],
    ["Québec(Capitale-Nationale)", 46.856283, -71.4817738],
    ["Saguenay-Lac-Saint-Jean", 50.3014462, -74.4000797]]

columns: List[Union[str, Any]] = ['region', 'summary', 'icon', 'precipIntensity', 'precipProbability', 'precipType',
                                  'precipAccumulation', 'temperature', 'apparentTemperature', 'humidity',
                                  'pressure', 'windSpeed', 'uvIndex', 'visibility']
df_weather_forecast = pd.DataFrame(columns=columns)

i = 0
while i <= len(list_regions) - 1:
    url = 'https://api.darksky.net/forecast/d3c545c8bfb1e45bda2dcbc89e94a11a/%s,%s?exclude=minutely,hourly,daily,' \
          'alerts,flags&units=ca' % (list_regions[i][1], list_regions[i][2])
    r = requests.get(url)
    r.json()

    if r.status_code == 200:
        pass
    else:
        print(f"Not able to download weather forecast for {list_regions[i][0]}.")
        continue

    tmp_region = list_regions[i][0]
    tmp_summary = r.json()['currently']['summary']
    tmp_icon = r.json()['currently']['icon']
    tmp_precipIntensity = r.json()['currently']['precipIntensity']
    tmp_precipProbability = r.json()['currently']['precipProbability']

    try:
        tmp_precipType = r.json()['currently']['precipType']
    except:
        tmp_precipType = ''

    try:
        tmp_precipAccumulation = r.json()['currently']['precipAccumulation']
    except:
        tmp_precipAccumulation = ''
    tmp_temperature = r.json()['currently']['temperature']
    tmp_apparentTemperature = r.json()['currently']['apparentTemperature']
    tmp_humidity = r.json()['currently']['humidity']
    tmp_pressure = r.json()['currently']['pressure']
    tmp_windSpeed = r.json()['currently']['windSpeed']
    tmp_uvIndex = r.json()['currently']['uvIndex']
    tmp_visibility = r.json()['currently']['visibility']

    i += 1
