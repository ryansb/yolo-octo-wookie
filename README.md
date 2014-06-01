DOT HPMS Data Import System
===========================

This repository contains a series of scripts that can be used to download and import all
HPMS GIS data into a mongodb databse.

This importer will import:
* All shape files from [the FHWA][fhwadata]
* Appendencies from the [the FHWA data appendix][appendix] containing data that
  are useful to understanding the shapefile data.

Requirements
============

* Python 2.7
* PyMongo
* Requests
* BeautifulSoup4
* zsh 4.5+
* gdal
* A running mongodb server version 2.6+

State of the Project
====================

The data required to make the federal-level information useful is across
[various][statesites] state web sites and is thus prohibitively complex to
import. The formats of the state data is not consistent and would be difficult
to programmatically import.

Currently, a mongodb installation with the GeoJSON imported from the shapefiles
could be used for spatial queries about the location of routes, and the
location of travel boundaries between states. Since route quality information
is in the state-level data, we weren't able to ue that.

[fhwadata]: http://www.fhwa.dot.gov/policyinformation/hpms/shapefiles.cfm
[appendix]: https://www.fhwa.dot.gov/policyinformation/hpms/fieldmanual/index.cfm
[statesites]: http://www.fhwa.dot.gov/policyinformation/hpms/states.cfm
