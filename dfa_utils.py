# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 08:37:51 2019

@author: Distanta
"""
from nfa_utils import epsilon_reachable
from nfa_utils import epsilon_reachable_many
from re_to_nfa import re_to_nfa_main
from collections import deque


def nfa_to_dfa(Q, E, delta, q0, F):

    dfaQ= set()
    dfaDelta ={}
    dfaF = set()
    visited={}

    nfaStart= epsilon_reachable(delta, q0)
    dfaStart= ",".join(sorted(nfaStart))
    dfaQ.add(dfaStart)
    # if(len(nfaStart.intersection(F))>=0):
    #     F.add(dfaStart)


    queue = deque()
    queue.append(dfaStart);
    visited[dfaStart] = True

    while(len(queue)!=0):
        state = queue.pop()
        state_constituents = state.split(",")


        if(len(set(state_constituents).intersection(F))>0):
            dfaF.add(state)

        for ch in E:
            #print("Now looking at: " + str(state_constituents) + " and key " + ch)
            destination = set()
            #get what all constituent take you to
            for constituent in state_constituents:
                if (constituent, ch) not in delta:
                    nextStates= {}
                else:
                    nextStates= list(epsilon_reachable_many(Q,delta,delta[constituent,ch]))
                    destination = destination.union(nextStates)

            nextJoinedState= ",".join(sorted(destination))
            #print("Destination is: " + nextJoinedState)
            dfaQ.add(nextJoinedState)
            dfaDelta[state, ch]= nextJoinedState
            if(nextJoinedState not in visited):
                queue.append(nextJoinedState)
                visited[nextJoinedState] = True

    return dfaQ, E, dfaDelta, dfaStart, dfaF


def re_to_dfa( regex ):
    (Q, E, delta, q0, F)=re_to_nfa_main(regex)
    return nfa_to_dfa(Q, E, delta, q0, F)



def dfa_run( w, Q, E, delta, q0, F ):
    currentState=  q0
    for ch in w:
        if ch not in E:
            return False
        else:
            currentState = delta[currentState, ch]
    if(currentState in F):
        return True
    else:
        return False


def dfa_scan( program, Q, E, delta, q0, F ):
    counter= 0
    finalPointIndex = 0
    searchStartIndex=0
    currentState= q0

    while(counter < len(program)):
        ch= program[counter]

        if(ch== " "):
            yield(program[searchStartIndex:finalPointIndex+1], searchStartIndex, finalPointIndex)
            currentState= q0
            searchStartIndex= counter+1
        else:
            currentState= delta[currentState, ch]
            if currentState in F:
                finalPointIndex= counter
            elif(currentState== ''):
                #print("reached crash state at: " + str(counter) +" string " + program[counter])
                yield(program[searchStartIndex:finalPointIndex+1], searchStartIndex, finalPointIndex)
                currentState= q0
                counter= finalPointIndex
                #print("restarting search from: " +  str(counter) +" string " + program[counter])
                searchStartIndex= counter+1
                finalPointIndex= searchStartIndex



        if(counter== len(program)-1):
            if currentState in F:
                yield(program[searchStartIndex:finalPointIndex+1], searchStartIndex, finalPointIndex)

        counter=  counter + 1;

    yield ()

# Q, E, delta, q0, F = re_to_dfa("if|elseif|else|then|while|for|i|e|w|f|=|+|(1|2)(1|2)*")
# program = "ifithenwelseifethen for2w=1212elsewhile fi=i+1212"

# get_token = dfa_scan( program, Q, E, delta, q0, F )     # create generator and get/scan a few tokens

# print( next(get_token) )      # ('if', 0, 1)
# print( next(get_token) )      # ('i', 2, 2)
# print( next(get_token) )      # ('then', 3, 6)

# get_token = dfa_scan( program, Q, E, delta, q0, F )      # rebuild the generator to print all

# for token in get_token:      # for loop will automatically perform:   token = next(get_token)
#     print( token )
