#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 18:55:49 2022

@author: seal
"""
import os
import shutil
from astropy.io import fits
import matplotlib.pylab as plt

#Bin-time
bin_time = input("Enter bin time(s): ")

path = "{:}/match64bit.reg".format(os.getcwd())
cnt = 0
f = open(path, 'r')
for line in f.readlines():
    cnt += 1
    path = "{:}/SourceMatch/Src{:}".format(os.getcwd(),cnt)
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path)
    tmp = []
    print("Data{:}".format(cnt))
    src = line.split(' ')
    for i in range(0, len(src), 2):
        try:
            lcf = "{:}/analysis/lcf/src{:}_lightcurve_{:}s.fits".format(src[i],src[i+1],bin_time)
            name = lcf.split('/')[-1].split('.')[0]
            hdu = fits.open(lcf)
            Time = hdu[1].data.field(2)
            Time = Time - Time[0]
            Time_Min = hdu[1].data.field(1)
            Time_Max = hdu[1].data.field(3)
            Net_Rate = hdu[1].data.field(19)
            Err_Rate = hdu[1].data.field(20)
            
            plt.figure(dpi=150)
            plt.errorbar(Time, Net_Rate, yerr=Err_Rate, \
                         marker="o", color="red", mfc="black", ecolor="gray")
            plt.title(name)
            plt.xlabel("$\Delta$ T (sec)")
            plt.ylabel("Net Count Rate (counts/sec)")
            plt.savefig("{:}/obsid{:}{:}.png".format(path,src[i],name))
            print("Output: {}.png".format(name))
            plt.close()
            tmp.append(j[1])
        except:
            pass
        
'''
cnt = 0
MJDREF = 5.0614*10**4
for i in reslist:
    cnt += 1
    for j in i:
        try:
            lcf = "{:}/analysis/lcf/src{:}_lightcurve_{:}s.fits".format(j[0],int(j[1]),bin_time)
            name = lcf.split('/')[-1].split('.')[0]
            hdu = fits.open(lcf)
            Time = hdu[1].data.field(2)
            Time = Time/86400
            Time = Time - MJDREF
            Time_Min = hdu[1].data.field(1)
            Time_Max = hdu[1].data.field(3)
            Net_Rate = hdu[1].data.field(19)
            Err_Rate = hdu[1].data.field(20)
            
            plt.figure(dpi=150)
            plt.errorbar(Time, Net_Rate, yerr=Err_Rate, \
                         marker="o", color="red", mfc="black", ecolor="gray")
            plt.xlabel("Time")
            plt.ylabel("Net Count Rate (counts/sec)")
            tmp.append(j[1])
        except:
            pass
    for j in tmp:
        pass
    plt.title("Match{:}".format(cnt))
    plt.savefig("{:}/Match{:}.png".format(path,cnt))
    plt.close()
'''
