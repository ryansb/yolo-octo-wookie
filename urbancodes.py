import requests
import bs4
from collections import namedtuple
from pymongo import MongoClient


UrbanArea = namedtuple('UrbanArea', ['state', 'area', 'code', 'part', 'population'])


def download_html():
    html = requests.get('http://www.fhwa.dot.gov/policyinformation/hpms/fieldmanual/appendixi.cfm')
    return bs4.BeautifulSoup(html.text)


def gen_codes(html):
    for tr in html.find_all('tr'):
        if tr.get('bgcolor') is None:
            daters = []
            for th in tr.children:
                if th.string is not None and th.string != '\n':
                    daters.append(th.string.strip())
            yield UrbanArea(*daters)


if __name__ == "__main__":
    client = MongoClient()
    dater = client.dater
    urban_areas = dater.urbanareas
    for code in gen_codes(download_html()):
        urban_areas.insert({
            'state': code.state,
            'area': code.area,
            'code': code.code,
            'part': code.part,
            'population': code.population
        })
        print("Inserted {0}".format(code))
