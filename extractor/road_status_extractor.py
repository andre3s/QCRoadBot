import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
from datetime import datetime

from extractor.settings import qc511_base_url
from extractor.road_list_extractor import get_list_roads, list_roads
from extractor.utility import get_timestamp, tweet_sender

list_url = []

datetime_obj = get_timestamp()

# DataFrame to store the content.
columns = ['highway_code', 'highway_type', 'location_id', 'from_name', 'to_name',
           'roadway', 'visibility', 'last_update']
df_road_status_content = pd.DataFrame(columns=columns)
df_snow_alert = pd.DataFrame(columns=columns)


def create_list_url():
    global list_url

    get_list_roads()

    for road_code in list_roads:
        url_tmp = (qc511_base_url + str(road_code))
        list_url.append(url_tmp)

    return list_url


def get_road_status(url):
    # Global objects
    global list_url
    global df_road_status_content
    global df_snow_alert
    global datetime_obj

    # List of regex patterns used
    regen_from = r"""(?<=From :</b>)(.*)(?=</p><p>)"""
    regen_to = r"""(?<=To :</b>)(.*)(?=</p>)"""
    regen_rdwy = r"""(?<=>)([a-zA-ZÀ-ÿ].*)"""
    regen_visibility = r"""(?<=>)([a-zA-ZÀ-ÿ].*)"""
    regen_highway_code = r"""(?<=id=)([0-9].*)"""

    # Counters
    i = 0

    res = requests.get(url)
    if res.status_code == 200:
        pass
    else:
        print('Not able to download the content.')

    soup = BeautifulSoup(res.text, 'html.parser')

    # Get the list of location ids (with no hindrances)
    pattern = re.compile(r"(ctl00_cphContenu_ctl[0-9]+_tdLocalisation)")
    tmp_list_regular_locations = soup.select('.etat_reseau')
    list_regular_locations = pattern.findall(str(tmp_list_regular_locations))

    pattern = re.compile(r"(ctl00_cphContenu_ctl[0-9]+_tdChaussee)")
    tmp_list_regular_roadway = soup.select('.etat_reseau')
    list_regular_roadway = pattern.findall(str(tmp_list_regular_roadway))

    pattern = re.compile(r"(ctl00_cphContenu_ctl[0-9]+_tdVisibilite)")
    tmp_list_regular_visibility = soup.select('.etat_reseau')
    list_regular_visibility = pattern.findall(str(tmp_list_regular_visibility))

    tmp_highway_code = int(re.search(regen_highway_code, url)[0])

    list_autoroute = [5, 10, 13, 15, 19, 20, 25, 30, 31, 35, 40, 50, 55, 70, 73, 85, 410,
                      440, 520, 540, 573, 610, 640, 720, 730, 740, 955, 973]
    tmp_highway_type = 'Autoroute' if tmp_highway_code in list_autoroute else 'Route'

    tmp_datetime_obj = datetime_obj

    while i <= len(list_regular_locations) - 1:
        tmp_from2 = str(soup.find(id='%s' % list_regular_locations[i]))
        from_text = re.search(regen_from, tmp_from2)[0]

        tmp_to2 = str(soup.find(id='%s' % list_regular_locations[i]))
        to_text = re.search(regen_to, tmp_to2)[0]

        tmp_rdwy2 = str(soup.find(id='%s' % list_regular_roadway[i]))
        rdwy_text = re.search(regen_rdwy, tmp_rdwy2)[0]

        tmp_visibility2 = str(soup.find(id='%s' % list_regular_visibility[i]))
        visibility_text = re.search(regen_visibility, tmp_visibility2)[0]

        df_road_status_content = df_road_status_content.append(
            dict(highway_code=tmp_highway_code, highway_type=tmp_highway_type, location_id=list_regular_locations[i],
                 from_name=from_text.replace(u'\xa0', u''), to_name=to_text.replace(u'\xa0', u''),
                 roadway=rdwy_text.replace('</strong>', ''), visibility=visibility_text.replace('</strong>', ''),
                 last_update=tmp_datetime_obj),
            ignore_index=True)

        df_snow_alert.drop(df_snow_alert.index, inplace=True, axis=0)
        df_snow_alert = df_road_status_content.loc[(df_road_status_content['roadway'] == 'Partly Snow Covered') |
                                                   (df_road_status_content['roadway'] == 'Partly Snow Packed') |
                                                   (df_road_status_content['roadway'] == 'Partly Ice Covered') |
                                                   (df_road_status_content['roadway'] == 'Snow Covered') |
                                                   (df_road_status_content['roadway'] == 'Snow Packed') |
                                                   (df_road_status_content['roadway'] == 'Ice Covered')]

        i += 1

    return df_snow_alert


# Preparing and sending twitter message.
def message_sender():
    global df_snow_alert

    j = 0
    while j <= len(df_snow_alert) - 1:
        tmp_time = datetime.now()
        tmp_highway_type = str(df_snow_alert.iloc[j, 1])
        tmp_highway_code = str(df_snow_alert.iloc[j, 0])
        tmp_from_text = df_snow_alert.iloc[j, 3]
        tmp_from_to = df_snow_alert.iloc[j, 4]
        tmp_roadway = df_snow_alert.iloc[j, 5]
        tmp_visibility = df_snow_alert.iloc[j, 6]

        # Testing for any missing value.
        if tmp_highway_type is None or tmp_highway_code is None or tmp_from_text is None or tmp_from_to is None or \
                tmp_roadway is None or tmp_visibility is None:
            j += 1
            continue
        else:
            message = ('Snow alert for ' + '%s' + ' ' + '%s' + '\n' + 'From: ' + '%s' + '\n' + 'To: ' + '%s' + '\n' +
                       'Roadway: ' + '%s' + '\n' + 'Visibility: ' + '%s' + '\n' +
                       'Updated at: ' + str(tmp_time.strftime('%Y-%m-%d %H:%M:%S')) + '\n' + '#QC' + '%s' + '%s' +
                       ' #drivesafe') % \
                      (tmp_highway_type, tmp_highway_code, tmp_from_text, tmp_from_to, tmp_roadway, tmp_visibility,
                       tmp_highway_type, tmp_highway_code)

            tweet_sender(message)
            j += 1
            time.sleep(2)


def road_status():
    # Create list of URLs
    create_list_url()

    # Insert data into dataframe
    for url in list_url:
        print(url)
        global datetime_obj

        datetime_obj = get_timestamp()
        get_road_status(url)
        message_sender()

        time.sleep(30)


if __name__ == "__main__":
    road_status()
