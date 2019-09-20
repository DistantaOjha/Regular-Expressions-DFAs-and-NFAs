# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 20:47:23 2019

@author: Distanta
"""


import sys
from nfa_utils import nfa_run
from re_to_nfa import re_to_nfa_main
#print(sys.argv)
args= sys.argv
(Q, E, delta, q0, F) = re_to_nfa_main(args[1])


for i in range(2, len(args)):
    if(nfa_run(args[i], Q, E, delta, q0, F)==True):
        print(args[i] + " is a match")
    else:
        print(args[i] + " is not a match")




