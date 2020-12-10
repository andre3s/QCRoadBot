import requests
from bs4 import BeautifulSoup
import re
from extractor.settings import qc511_road_list

list_roads = []


def get_list_roads():

    global list_roads

    regex_roads = r"""(?<=>)([0-9]*)"""

    res = requests.get(qc511_road_list)
    soup = BeautifulSoup(res.text, 'html.parser')

    all_roads_two_digits = soup.select('.digit2')
    roads_two_digits = str(all_roads_two_digits).split(",")
    for road in roads_two_digits:
        tmp_road_number = re.search(regex_roads, road)[0]
        list_roads.append(int(tmp_road_number))

    all_roads_three_digits = soup.select('.digit3')
    roads_three_digits = str(all_roads_three_digits).split(",")
    for road in roads_three_digits:
        tmp_road_number = re.search(regex_roads, road)[0]
        list_roads.append(int(tmp_road_number))

    return list_roads

    # global list_roads
    # list_roads = [5, 10, 197]
    # return list_roads


if __name__ == "__main__":
    get_list_roads()
