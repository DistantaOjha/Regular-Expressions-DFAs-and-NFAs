# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 16:53:55 2019

@author: Distanta
"""

from dfa_xml import load_dfa

def dfa_search_string(w, delta, q0, accepting):
    curState= q0
    for i,c in enumerate(w):
        if(delta[curState, c] in accepting):
            print("match found, ending at index " + str(i))
            curState=q0
        else:
            curState=delta[curState, c]
#        if i>5000:
#             break


def dfa_search_file(dataFilename, dfaFilename):
    (Q, E, delta, q0, F) = load_dfa(dfaFilename)
    file= open(dataFilename,"r")
    fileStr= file.read().replace('\n', '')
    file.close();
    dfa_search_string(fileStr, delta, q0, F)




#dfa_search_file("ecoli.txt", "gene_search.jff")
