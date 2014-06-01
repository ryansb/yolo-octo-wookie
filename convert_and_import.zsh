#!/bin/zsh

pushd raw
find . -name '*.zip' -type f -exec unzip {} \;
popd

mkdir geojson

for shapefile in $(find raw/ -name '*.shp') ; do
     ogr2ogr -f GeoJSON -t_srs crs:84 "geojson/$(basename $shapefile).geojson" $shapefile
done

for db in $(find geojson/ -name '*.geojson') ; do
   python geojson_importer.py "${db}"
done
