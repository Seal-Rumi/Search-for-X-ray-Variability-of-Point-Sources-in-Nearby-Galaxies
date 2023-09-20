#! /bin/bash

#Last updated: 26/Aug/2022
###Notice: This script operate on Directory:"analysis".
### This script and pltlc.py are match together. 

#Extract source light curve
n=0
read -p "Please enter bin time(s):" bin_time
while read -r coord; do
    n=$(($n+1))
    IFS=','
    arr=${coord#ellipse(} && arr=${arr%)}
    arr=($arr)
    rmin=${arr[3]}
    if [ $rmin = "0.000000" ];then
        continue
    fi
    outfile="lcf/src"$n"_lightcurve_"$bin_time"s.fits"
    bkg="acis_events_0.5_7keV.fits[sky=region(bg.reg)]"
    dmextract "acis_events_0.5_7keV.fits[sky=region(regions/src"$n".reg)][bin time=::"$bin_time"]"\
    		outfile=$outfile bkg=$bkg opt=ltc1 clobber=yes
    echo "Output: "$outfile
done < all_src.reg
