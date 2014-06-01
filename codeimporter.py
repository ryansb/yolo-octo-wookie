import requests
import bs4
from collections import namedtuple
from pymongo import MongoClient
import multiprocessing


UrbanArea = namedtuple('UrbanArea', ['state', 'area', 'code', 'part', 'population'])
FIPS = namedtuple('FIPS', ['code', 'description'])

def gen_urban_codes():
    html = requests.get('http://www.fhwa.dot.gov/policyinformation/hpms/fieldmanual/appendixi.cfm')
    soup = bs4.BeautifulSoup(html.text)
    for tr in soup.find_all('tr'):
        if tr.get('bgcolor') is None:
            daters = []
            for th in tr.children:
                if th.string is not None and th.string != '\n':
                    daters.append(th.string.strip())
            yield UrbanArea(*daters)

def import_urban_codes(dater):
    urban_areas = dater.urbanareas
    for code in gen_urban_codes():
        urban_areas.insert({
            'state': code.state,
            'area': code.area,
            'code': code.code,
            'part': code.part,
            'population': code.population
        })
        print("Inserted {0}".format(code))


def gen_fips():
    html = requests.get('http://www.fhwa.dot.gov/policyinformation/hpms/fieldmanual/appendixc.cfm')
    soup = bs4.BeautifulSoup(html.text)
    for tr in soup.find_all('tr'):
        if tr.get('bgcolor') is None:
            daters = []
            for th in tr.children:
                if th.string is not None and th.string != '\n':
                    daters.append(th.string.strip())
            yield FIPS(*daters)


def import_fips_codes(dater):
    fips = dater.fips
    for fip in gen_fips():
        fips.insert({
            'code', fip.code,
            'description', fip.description,
        })
        print("Inserted {0}".format(fip))


if __name__ == "__main__":
    procs = []
    client = MongoClient()
    dater = client.dater
    fips_proc = multiprocessing.Process(target=import_fips_codes, args=(dater,))
    procs.append(fips_proc)
    #ua_proc = multiprocessing.Process(target=import_urban_codes, args=(dater,))
    #procs.append(ua_proc)
    for proc in procs:
        proc.start()
    for proc in procs:
        proc.join()
