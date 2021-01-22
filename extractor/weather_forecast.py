from typing import List, Any, Union
from extractor.utility import tweet_sender
from datetime import datetime
import time

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


def weather_forecast():
    global list_regions
    global df_weather_forecast

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

        tmp_time = datetime.now()
        tmp_region = list_regions[i][0]
        tmp_summary = r.json()['currently']['summary']
        # tmp_icon = r.json()['currently']['icon']
        # tmp_precipIntensity = r.json()['currently']['precipIntensity']
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
        # tmp_humidity = r.json()['currently']['humidity']
        # tmp_pressure = r.json()['currently']['pressure']
        tmp_windSpeed = r.json()['currently']['windSpeed']
        # tmp_uvIndex = r.json()['currently']['uvIndex']
        tmp_visibility = r.json()['currently']['visibility']

        if tmp_precipProbability >= 0.45:
            print(f'Sending weather alert for {tmp_region}. Precipitation chance is {tmp_precipProbability*100}%.')
            message = ('Weather forecast alert' + '\n' + 'Region: ' + '%s' + '\n' + 'Summary: ' + '%s' + '\n'
                       + 'Precipitation type: ' + '%s' + '\n' + 'Precipitation probability: ' + '%s' + '\n'
                       + 'Precipitation Accumulation: ' + '%s' + 'cm' + '\n' + 'Temperature: ' + '%s' + '\n'
                       + 'Apparent Temperature: ' + '%s' + '\n' + 'Wind speed: ' + '%s' + '\n' + 'Visibility: ' + '%s'
                       + '\n' + 'Updated at: ' + str(tmp_time.strftime('%Y-%m-%d %H:%M:%S')) + '\n'
                       + 'Powered by Dark Sky: https://darksky.net/dev' + '#drivesafe') % (
                      tmp_region, tmp_summary, tmp_precipType.capitalize(),
                      "{0:.0f}%".format(tmp_precipProbability*100),
                      "{0:.0f}".format(tmp_precipAccumulation), "{0:.0f}°C".format(tmp_temperature),
                      "{0:.0f}°C".format(tmp_apparentTemperature), "{0:.0f}Km/h".format(tmp_windSpeed),
                      "{0:.0f}Km".format(tmp_visibility))
            tweet_sender(message)

        elif tmp_precipProbability < 0.45:
            print(f'No weather alert needed for {tmp_region}. Precipitation chance is {tmp_precipProbability} .')
            pass

        time.sleep(10)
        i += 1


if __name__ == '__main__':
    weather_forecast()
