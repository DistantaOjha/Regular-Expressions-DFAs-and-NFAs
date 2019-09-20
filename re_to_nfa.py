from re_parse3 import re_parse



def make_state(labels=[-1]):
    labels[0] += 1
    return str(labels[0])

def re_to_nfa(regex, i, j):
    Q = set() #states
    delta= {} #transition function
    q0= ""    # starting state
    F = set() # final states
    E = set() # alphabets
    if (i==j):
        state1= make_state()
        state2 = make_state()
        Q.add(state1)
        Q.add(state2)
        q0 = state1
        F.add(state2)
        E.add(regex[i])
        delta[state1 , regex[i]] =  {state2}
    else:
        (index, operator) = re_parse(regex, i, j)
        if (operator == '|' ):
            (lQ, lE, lDelta, lq0, lF) = re_to_nfa(regex, i, index-1)
            (rQ, rE, rDelta, rq0, rF) = re_to_nfa(regex, index+ 1, j)
            newState= make_state()
            Q= lQ.union(rQ)
            Q.add(newState)
            delta = {**rDelta, **lDelta}
            delta[newState, ""] = {lq0, rq0}
            q0= newState
            F= lF.union(rF)
            E= lE.union(rE)
        elif (operator=="o"):
            (lQ, lE, lDelta, lq0, lF) = re_to_nfa(regex, i, index)
            (rQ, rE, rDelta, rq0, rF) = re_to_nfa(regex, index+ 1, j)
            Q= lQ.union(rQ)
            delta = {**rDelta, **lDelta}

            for finalState in lF:                    # process all elements
                if((finalState, "") in delta):
                    destinations = delta[finalState, ""]
                    destinations.add(rq0)
                    delta[finalState, ""]= destinations
                else:
                    delta[finalState, ""]= {rq0}

            q0 = lq0
            F= rF
            E= lE.union(rE)
        elif (operator== '*'):
            (lQ, lE, lDelta, lq0, lF) = re_to_nfa(regex, i, index-1)
            prevStart = lq0
            newState = make_state()
            q0 = newState
            delta[q0, ""]= {prevStart}

            for finalState in lF:                    # process all elements
                lDelta[finalState, ""]= {prevStart}

            Q = Q.union(lQ)
            Q.add(q0)
            E = E.union(lE)
            delta= {**delta, **lDelta}
            lF.add(q0)
            F= lF
        else:
            #print("Index is: " + str(i) + " "+ str(j)+ " " + str(len(regex)))
            if(i+1 <= j-1):
                return re_to_nfa(regex, i+1, j-1)

    return (Q, E, delta, q0, F)



def re_to_nfa_main(regex):
    return re_to_nfa( regex, 0, len(regex)-1)






