
def attractors(S):

    j = 1
    Att_num = 0
    Atts_syn = set()
    total_set = set()
    total_set.update(S.keys())
    delta_0 = set()

    #print(total_set)

    while len(total_set) != 0:

        delta_j = getElementsJCycle(total_set, S, j)

        #print(delta_j)

        delta_j.difference_update(delta_0)

        if delta_j.union(delta_0) == total_set:
            Att_num += len(delta_j) / j
            Atts_syn.update(delta_j)
            break

        if len(delta_j) != 0:
            Att_num += len(delta_j) / j
            Atts_syn.update(delta_j)
            total_set.difference_update(BR(delta_j, S))
        
        #print(j)
        delta_0.update(delta_j)
        j += 1

    #print(Atts_syn)

    return Atts_syn, Att_num

def BR(delta_j, S):

    States = set(S.keys())
    States.difference_update(delta_j)

    back_reachable = set()
    curr_set = set()
    cond = False

    #print(States)

    for state in States:

        curr_set.add(state)
        s = state

        while s not in delta_j:
            s = S[s]

            if s in delta_j:
                break

            if s in curr_set:
                cond = True
                break

            curr_set.add(s)
        
        if cond != True:
            back_reachable.update(curr_set)
            curr_set = set()
        else:
            curr_set = set()
            cond = False
            #States.difference_update(curr_set)

    return back_reachable

def getElementsJCycle(total_set, S, j):

    states = set()

    for state in total_set:
        s = state
        for i in range(j):
            st = S[s]
            s = st

        if state == st:
            states.add(state)

    return states


'''if __name__ == "__main__":

    BN = {
        '000':'001',
        '001':'000',
        '010':'101',
        '011':'000',
        '100':'101',
        '101':'010',
        '110':'101',
        '111':'011'
    }

    BN1 = {
        '000':'000',
        '001':'100',
        '010':'001',
        '011':'101',
        '100':'001',
        '101':'101',
        '110':'000',
        '111':'100'
    }

    BN2 = {
        '000':'000',
        '001':'100',
        '010':'001',
        '011':'101',
        '100':'000',
        '101':'100',
        '110':'000',
        '111':'100'
    }

    BN3 = {
        '000':'000',
        '001':'000',
        '010':'100',
        '011':'100',
        '100':'011',
        '101':'001',
        '110':'110',
        '111':'100'
    }

    BN4 = {
        '000':'000',
        '001':'100',
        '010':'001',
        '011':'101',
        '100':'010',
        '101':'100',
        '110':'011',
        '111':'101'
    }

    BN5 = {
        '00101':'01100',
        '00001':'01100',
        '10101':'01100',
        '11001':'11000',
        '01100':'10100',
        '11000':'10100',
        '10100':'00000',
        '00000':'00000',

        '10001':'01000',
        '01101':'11100',
        '01001':'11100',
        '11101':'11100',
        '01000':'10000',
        '11100':'10000',
        '10000':'00100',
        '00100':'00100',

        '11011':'10011',
        '10011':'10011',

        '10111':'11111',
        '11111':'11111',

        '01011':'10110',
        '00011':'10110',
        '10110':'11010',
        '01010':'11010',
        '00010':'11010',
        '11010':'11110',
        '11110':'11010',
        '10010':'11110',
        '01111':'11110',
        '01110':'11110',
        '00111':'11110',
        '00110':'11110'
    }

    Atts_syn, Att_num = attractors(BN5)

    print("Attractors:", Atts_syn)
    print("Number of attractors:", Att_num)'''

    