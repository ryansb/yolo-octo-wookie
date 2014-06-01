DOT HPMS Data Import System
===========================

This repository contains a series of scripts that can be used to download and import all
HPMS GIS data into a mongodb databse.

This importer will import:
* All shape files from http://www.fhwa.dot.gov/policyinformation/hpms/shapefiles.cfm
* a few appendencies from https://www.fhwa.dot.gov/policyinformation/hpms/fieldmanual/index.cfm containing data that are useful to understanding the shapefile data 

Requirements
============

* Python 2.7
* PyMongo
* Requests
* BeautifulSoup4
* zsh 4.5+
* gdal
* A running mongodb server version 2.6+
