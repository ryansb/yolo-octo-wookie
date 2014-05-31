#!/bin/zsh
local -a states
local -a years
states=("${(f)$(< ./states)}")
url="http://www.fhwa.dot.gov/policyinformation/hpms/shapefiles/"
for s in $(cat ./states) ; do
    wget "${url}${s}2011.zip"
    wget "${url}${s}2012.zip"
done
