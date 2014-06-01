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

def import_urban_codes():
    client = MongoClient()
    dater = client.newdaters
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


def import_fips_codes():
    client = MongoClient()
    dater = client.newdaters
    fips = dater.fips
    for fip in gen_fips():
        fips.insert({
            'code': fip.code.decode('utf-8'),
            'description': fip.description.decode('utf-8'),
        })
        print("Inserted {0}".format(fip))

def import_owner_codes():
    client = MongoClient()
    dater = client.newdaters
    owners = dater.owners
    codes = {
        1: 'State Highway Agency',
        2: 'County Highway Agency',
        3: 'Town or Township Highway Agency',
        4: 'City or Municipal Highway Agency',
        11: 'State Park, Forest, or Reservation Agency',
        12: 'Local Park, Forest, or Reservation Agency',
        21: 'Other State Agency',
        25: 'Other Local Agency',
        26: 'Private (other than Railroad)',
        27: 'Railroad',
        31: 'State Toll Authority',
        32: 'Local Toll Authority',
        40: 'Other Public Instrumentality (e.g., Airport, School, University)',
        50: 'Indian Tribe Nation',
        60: 'Other Federal Agency',
        62: 'Bureau of Indian Affairs',
        63: 'Bureau of Fish and Wildlife',
        64: 'U.S. Forest Service',
        66: 'National Park Service',
        67: 'Tennessee Valley Authority',
        68: 'Beureau of Land Management',
        69: 'Bureau of Reclamation',
        70: 'Corps of Engineers',
        72: 'Air Force',
        73: 'Navy/Marines',
        74: 'Army',
        80: 'Other',
    }
    for key, val in codes.iteritems():
        owner = {'code': key, 'description': val}
        owners.insert(owner)
        print("Inserted {0}".format(owner))

if __name__ == "__main__":
    procs = []
    fips_proc = multiprocessing.Process(target=import_fips_codes)
    procs.append(fips_proc)
    ua_proc = multiprocessing.Process(target=import_urban_codes)
    procs.append(ua_proc)
    owner_proc = multiprocessing.Process(target=import_owner_codes)
    procs.append(owner_proc)
    for proc in procs:
        proc.start()
    for proc in procs:
        proc.join()
