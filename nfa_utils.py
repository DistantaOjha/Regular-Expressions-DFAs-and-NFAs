# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 17:47:27 2019

@author: Distanta
"""
from collections import deque



def epsilon_reachable( delta, q ):
    queue = deque()
    reachable = set()
    visited ={}
    queue.append(q);
    visited[q] = True
    reachable.add(q)
    while(len(queue)!=0):
        state = queue.pop()
        if (state, "") in delta:
            newStates= delta[state,""]
            reachable= reachable.union(newStates)
            for newState in newStates:
                if(newState not in visited):
                    queue.append(newState)
                    visited[newState] = True
    return reachable


def epsilon_reachable_many(Q, delta, q_set ):
    reachables = set()
    for q in q_set:
        reachables= reachables.union(epsilon_reachable( delta, q ))
    return reachables



def nfa_run( w, Q, E, delta, q0, F ):
    currentStates= set()
    currentStates= epsilon_reachable(delta, q0)
    # print("Starting index is: " + str(currentStates))
    for ch in w:                    # process all elements
        #print("Coin is: " + ch)
        newStates= set()
        for curState in currentStates:
           # delta [ch , curState] will give each currentState
           if((curState, ch) in delta):
               newStates= newStates.union(epsilon_reachable_many(Q, delta, delta[curState, ch]))
        currentStates= newStates
    if(len (currentStates.intersection(F)) >= 1):
        return True
    else:
        return False

