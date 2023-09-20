#! /bin/bash

#Last updated: 26/Aug/2022

#Make Directory
mkdir -p "repro"
mkdir -p "analysis/regions"
mkdir -p "analysis/events"
mkdir -p "analysis/bary"
mkdir -p "analysis/lcf"
mkdir -p "analysis/lcimg"
mkdir -p "analysis/ztest"
touch analysis/ztest_record.log

#Reprocess
chandra_repro "./" "repro"
evt=`find repro/ -name *evt2.fits`
cp "$evt" "analysis"
mv "analysis/${evt##*/}" "analysis/acis_event.fits"
