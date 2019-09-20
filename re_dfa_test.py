# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 21:23:43 2019

@author: Distanta
"""


import sys
from dfa_utils import dfa_run
from dfa_utils import re_to_dfa

#print(sys.argv)
args= sys.argv
(Q, E, delta, q0, F) = re_to_dfa(args[1])


for i in range(2, len(args)):
    if(dfa_run(args[i], Q, E, delta, q0, F)==True):
        print(args[i] + " is a match")
    else:
        print(args[i] + " is not a match")

