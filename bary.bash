#! /bin/bash

#Last updated: 25/Aug/2022
###Notice: This script operate on Directory:"analysis".

#Barycentric correction
n=0
orbitfile=`find ../primary/ -name orbitf*`

rm -f all_bary.reg
touch all_bary.reg
while read -r coord; do
    n=$(($n+1))  
    IFS=','
    arr=${coord#ellipse(} && arr=${arr%)}
    arr=($arr)
    x=${arr[0]}
    y=${arr[1]}
    rmax=${arr[2]}
    rmin=${arr[3]}
    if [ $rmin = "0.000000" ];then
        continue
    fi
    punlearn dmcoords
    dmcoords acis_events_0.5_7keV.fits asol=None option=sky x=$x y=$y celfmt=deg
    ra=`pget dmcoords ra`
    dec=`pget dmcoords dec`
    
    infile="events/src"$n"_events.fits"
    outfile="bary/src"$n"_events_bary.fits"
    axbary infile=$infile orbitfile=$orbitfile outfile=$outfile  ra=$ra dec=$dec clobber=yes 
    
    touch all_bary.reg
    echo "src"$n"_events_bary.fits" >> all_bary.reg
done < all_src.reg
