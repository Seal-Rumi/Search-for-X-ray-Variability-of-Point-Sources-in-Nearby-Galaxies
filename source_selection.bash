#! /bin/bash

#Last updated: 25/Aug/2022
###Notice: This script operate on Directory:"analysis".

#Standard Operating Procedures
dmcopy "acis_event.fits[energy=500:7000]" acis_events_0.5_7keV.fits
fluximage "acis_events_0.5_7keV.fits" binsize=1 \
	bands=broad outroot=all psfecf=0.393 clobber=yes
mkpsfmap "all_broad_thresh.img" outfile="step_by_step_all_psfmap.fits" \
	energy=1.4967 ecf=0.393 clobber=yes
wavdetect infile="all_broad_thresh.img" psffile="all_broad_thresh.psfmap" outfile="all_src.fits" \
	scellfile="all_scell.fits" imagefile="all_imgfile.fits" defnbkgfile="all_nbgd.fits" \
	regfile="all_src.reg" scales="1.0 2.0 4.0 8.0 16.0" clobber=yes


#Separating Regions--Used for further timing analysis(e.g. Ztest)
n=0
if [ -f all_src.reg ]; then
    while read -r line; do
        n=$(($n+1))
        IFS=','
        arr=${line#ellipse(} && arr=${arr%)}
        arr=($arr)
        rmin=${arr[3]}
        if [ $rmin = "0.000000" ];then
            continue
        fi
        echo $line
        touch regions/src"$n".reg
        echo "$line" > regions/src"$n".reg
        if [ -f events/src"$n"_events.fits ]
        then
            rm events/src"$n"_events.fits
        fi
        infile="acis_events_0.5_7keV.fits[sky=region(regions/src"$n".reg)]"
        outfile="events/src"$n"_events.fits"
        dmcopy $infile $outfile
    done < all_src.reg
fi
