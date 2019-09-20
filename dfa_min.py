# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 18:05:10 2019

@author: Distanta
"""




from dfa_xml import load_dfa
from dfa_xml import save_dfa

def build_table(states, alphabet, delta, accepting):
    table ={}
    for state1 in states:
        for state2 in states:
            if (state1 in accepting) and (state2 not in accepting):
                table[state1, state2] = True
                table[state2, state1] = True
                #print("Marking initial:" + state1 + "  " + state2)
            elif (state1 not in accepting) and (state2 in accepting):
                table[state1, state2] = True
                table[state2, state1] = True
                #print("Marking initial:" + state1 + "  " + state2)

    inserted= True
    i=1
    while(inserted):
        inserted= False
        for state1 in states:
            for state2 in states:
                if(state1, state2) not in table or table[state1, state2]==False:
                    for alpha in alphabet:
                        destin1 = delta[state1, alpha]
                        destin2 = delta[state2, alpha]
                        if (destin1,destin2) in table and table[destin1, destin2]:
                            table[state1, state2]= True
                            table[state2, state1]= True
                            #print("Marking in iteration: " +str(i)+" : " + state1 + "  " + state2)
                            inserted= True
                        else:
                            table[state1, state2]= False
                            table[state2, state1]= False
        i=i+1
    return table


def build_mindfa(states, alphabet, delta, q0, accepting, distinct):
    minStates = set()
    stateCluster = {}
    #alphabets will be same
    minDelta= {}
    minq0= ""
    minAccepting=set()

    for state1 in states:
        for state2 in states:
            if(state1!=state2):
                if(distinct[state1, state2]!= True):
                    if(state1 not in stateCluster):
                        stateCluster[state1]= {state1, state2}
                        stateCluster[state2]= stateCluster[state1]
                    else:
                            stateCluster[state1].add(state2)
                            stateCluster[state2]= stateCluster[state1]

    mergedStates= stateCluster.values()
    for mergedState in mergedStates:
        mergedState= sorted(mergedState)
        joinedMergedState= ",".join(mergedState)

        minStates.add(joinedMergedState)
        if q0 in mergedState:
            minq0= joinedMergedState

        if(not (set(accepting).isdisjoint(set(mergedState)))):
            minAccepting.add(joinedMergedState)

        for ch in alphabet:
            destination= delta[mergedState[0],ch]
            minDelta[joinedMergedState, ch]= ",".join(sorted(stateCluster[destination]))
    return minStates, minDelta, minq0, minAccepting





def minimize_dfa( states, alphabet, delta, q0, accepting ):
    return build_mindfa(states,alphabet,delta,q0,accepting, build_table(states,alphabet,delta,accepting))


def minimize_file( origFilename, minFilename ):
    (states, alphabet, delta, q0, accepting) = load_dfa(origFilename)
    (minStates, minDelta, minq0, minAccepting) = minimize_dfa(states, alphabet, delta, q0, accepting)
    save_dfa(minStates,minDelta,minq0,minAccepting,minFilename)


#delta = {
#        ("A", "0") : "B", ("A", "1") : "E",
#        ("B", "0") : "C", ("B", "1") : "F",
#        ("C", "0") : "D", ("C", "1") : "H",
#        ("D", "0") : "E", ("D", "1") : "H",
#        ("E", "0") : "F", ("E", "1") : "I",
#        ("F", "0") : "G", ("F", "1") : "B",
#        ("G", "0") : "H", ("G", "1") : "B",
#        ("H", "0") : "I", ("H", "1") : "C",
#        ("I", "0") : "A", ("I", "1") : "E"
#}

#minimizeTable = build_table({"A","B","C","D","E","F","G","H","I"},{"0","1"}, delta, {"C","F","I"})
#Q1, delta1, q01, F1 = build_mindfa({"A","B","C","D","E","F","G","H","I"},{"0","1"},delta,"A",{"C","F","I"},minimizeTable)


# print("List of states is: " + str(Q1))
# print("Delta is: " + str(delta1))
# print("Initial state is: " + q01)
# print("List of final states is: " + str(F1))
# minimize_file("hw3mini.jff", "hw3minimized.jff")

