#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 08:19:06 2022

@author: seal
"""

import os
import shutil
from astropy.io import fits

class Chandra_data:
    def __init__(self):
        self.galaxy = None
        self.obsid = None
        self.id = None
        self.ralist = []
        self.declist = []
        self.rahash = None
        self.dechash = None
    #HashTable
    def builthash(self):
        self.rahash = [[] for _ in range(100)]
        self.dechash = [[] for _ in range(100)]
        for i in range(len(self.ralist)):
            ra = int(self.ralist[i]*100)
            dec = int(self.declist[i]*100)
            self.rahash[ra%100].append(self.ralist[i])
            self.dechash[dec%100].append(self.declist[i])

def matchdfs(database, des, index):
    ra = des.ralist[index]
    dec = des.declist[index]
    ranum = int(ra*100)%100
    decnum = int(dec*100)%100
    record = [(des.obsid,index)]
    for i in database:
        if (i==des):
            continue
        tmp = []
        qualified = []
        for j in i.rahash[ranum]:
            if (abs(j-ra)<5e-4):
                tmp.append(i.ralist.index(j))
        for j in i.dechash[decnum]:
            if abs(j-dec)<5e-3 and i.declist.index(j) in tmp:
                qualified.append(i.declist.index(j))
        if len(qualified)==0:
            continue
        if len(qualified)==1:
            record.append((i.obsid, qualified[0]))
            continue
        tmp = [-1,100]
        for j in qualified:
            diff = (i.ralist[j]-ra)**2+(i.declist[j]-dec)**2
            if diff < tmp[1]:
                tmp[0] = j
                tmp[1] = diff
        if tmp[0]>-1:
            record.append((i.obsid,tmp[0]+1))
    return record
           
#Build Object 
galaxy = os.getcwd().split('/')[-1]
Obsid = []
for i in os.listdir(os.getcwd()):
    if i.isdigit():
        Obsid.append(int(i))
Obsid.sort()

Archive = []
for i in range(len(Obsid)):
    Archive.append(Chandra_data())
    Archive[i].galaxy = galaxy
    Archive[i].obsid = Obsid[i]
    Archive[i].id = i
    hdu = fits.open("{:}/analysis/all_src.fits".format(Obsid[i]))
    Archive[i].ralist = hdu[1].data.field(0).tolist()
    Archive[i].declist = hdu[1].data.field(1).tolist()
    Archive[i].builthash()

#Build related directory
path = "{:}/SourceMatch".format(os.getcwd())
if os.path.isdir(path):
    shutil.rmtree(path)
os.mkdir(path)

#Match
print("Matching...\n")
reslist = []
check = dict()
for data in Archive:
    for i in range(len(data.ralist)):
        res = matchdfs(Archive, data, i)
        if len(res)>1:
            res.sort(key = lambda s:int(s[0]))
            if res[0] not in check:
                check[res[0]] = res
            else:
                tmp = check[res[0]]
                for i in res:
                    if i not in tmp:
                        tmp.append(i)
                check[res[0]] = tmp
for i in check.values():
    reslist.append(i)

cnt = 0
path = "{:}/match.reg".format(os.getcwd())

f = open(path, 'w+')
for i in reslist:
    cnt += 1
    f.write("No.{:}: {:}\n".format(cnt, i))
f.close()
