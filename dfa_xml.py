# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 16:54:19 2019

@author: Distanta
"""
from math import sin
from math import cos
from math import pi



def load_dfa(filename):
    states= list()
    alphabet = list()
    delta ={}
    accepting = list()
    stateIDMap ={}

    file= open(filename,"r")
    filelines= file.readlines()

    for line in filelines:
        #print(line)
        stripedLine = line.strip().replace("&#13;", "");

        if(stripedLine.startswith("<state")):
            stateTagSplit = line.split('"')
            stateID= stateTagSplit[1]
            state =  stateTagSplit[len(stateTagSplit)-2]
            stateIDMap[stateID] = state
            states.append(state)

        elif(stripedLine.startswith("<initial/>")):
            #last state added will be the initial state
            q0 = states[len(states)-1]

        elif(stripedLine.startswith("<final/>")):
            #last state added will be in the list of final state
            accepting.append(states[len(states)-1])

        elif(stripedLine.startswith("<from>")):
            locationID = stripedLine.replace("<from>", "").replace("</from>", "")

        elif(stripedLine.startswith("<to>")):
            destinationID = stripedLine.replace("<to>", "").replace("</to>", "")

        elif(stripedLine.startswith("<read>")):
            coin = stripedLine.replace("<read>", "").replace("</read>", "")
            delta[stateIDMap[locationID], coin]= stateIDMap[destinationID]
            if coin not in alphabet:
                alphabet.append(coin)
            #just being cautious here
            locationID= None
            coin= None
            destinationID= None


    file.close();
    return (states, alphabet, delta, q0, accepting)

def save_dfa(states, delta, q0, accepting, filename):
    idStateMap = {}
    jffFile = open(filename, "w+")
    print('<?xml version="1.0" encoding="UTF-8" standalone="no"?><!--Created with JFLAP 7.1.--><structure>', file=jffFile)
    print("<type>fa</type>", file=jffFile)
    print("<automaton>", file=jffFile)
    print("<!--The list of states.-->", file=jffFile)

    #insert states
        #check if in inital
        #check if in final
    state_id = 0
    alpha = (2*pi) / len(states)
    for state in states:
        idStateMap[state] = state_id
        print('<state id="'+str(state_id)+'" name="'+ state+ '">', file=jffFile)
        x = 100 + 50*cos(state_id*alpha) # center is at (100, 100), radius is 50
        y = 100 + 50*sin(state_id*alpha) # alpha is the angle between states (pizza pie)
        print("<x>" + str(x) + "</x>", file=jffFile)
        print("<y>" + str(y) + "</y>", file=jffFile)
        if state==q0:
            print("<initial/>", file=jffFile)
        if state in accepting:
            print("<final/>", file=jffFile)
        state_id= state_id +1;
        print("</state>", file=jffFile)


    #print("</state>", file=jffFile)
    print("<!--The list of transitions.-->", file=jffFile)


    
    for k,v in delta.items():  # process all (key, value) pairs
         print("<transition>", file=jffFile)
         (state, coin) = k
         print("<from>" + str(idStateMap[state]) + "</from>", file=jffFile)
         print("<to>" + str(idStateMap[v]) + "</to>", file=jffFile)
         print("<read>" + coin + "</read>", file=jffFile)
         print("</transition>", file=jffFile)


    print("</automaton>", file=jffFile)
    print("</structure>", file=jffFile)

    jffFile.close()

#save_dfa("0","0","0","0","odd_zeros.jff")

##Test Load DFA
# (Q, E, delta, q0, F) = load_dfa("as.txt")
# print("List of states is: " + str(Q))
# print("Delta is: " + str(delta))
# print("Initial state is: " + q0)
# print("List of final states is: " + str(F))
# print("Alphabet is: " + str(E))


##Test Load DFA
# delta = {}
# delta["A", "0"] = "B"
# delta["A", "1"] = "A"
# delta["B", "0"] = "A"
# delta["B", "1"] = "B"

# save_dfa( {"A", "B"}, delta, "A", {"B"}, "odd_zeros.jff")
