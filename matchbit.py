#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 15:52:32 2022

@author: seal
"""
import os

readpath = "{:}/match.reg".format(os.getcwd())
path = "{:}/match64bit.reg".format(os.getcwd())
readfile = open(readpath, 'r')
f = open(path, 'w+')
for line in readfile.readlines():
    string = ""
    flag = False
    for s in line:
        if s.isdigit(): 
            string += s
            flag = False
        else:
            if not flag:
                string += " "
                flag = True
            
    f.write("{:}\n".format(string))
f.close()
readfile.close()
