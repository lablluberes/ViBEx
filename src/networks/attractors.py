##############################################
#
# This file contains function to compute attractors of BN.
# Algorithm implemented was proposed by Desheng Zheng in paper:
#
# Zheng D, Yang G, Li X, Wang Z, Liu F, et al. (2013) An Efficient 
# Algorithm for Computing Attractors of Synchronous And Asynchronous Boolean
# Networks. PLoS ONE 8(4): e60593. doi:10.1371/journal.pone.0060593
#
##############################################
def attractors(S):
    """
        attractors - computes attractors of BN

        S: dictionary representing state transitions example: {000: 010, 001: 111, ...}
    """

    j = 1 # times of iteration
    Att_num = 0 # number of attractors
    Atts_syn = set() # set of attractors
    total_set = set() # set of unvisited states
    total_set.update(S.keys())
    delta_0 = set() # empty set 

    #print(total_set)

    # Main resolving part (continue until all states are visited)
    while len(total_set) != 0:

        # verifies if remaining states are attractors based on j-sized forward step
        delta_j = getElementsJCycle(total_set, S, j)

        #print(delta_j)

        # delete visited attractor 
        delta_j.difference_update(delta_0)

        # verifies if states are periodic attractors
        if delta_j.union(delta_0) == total_set:
            Att_num += len(delta_j) / j # increase number of attractors
            Atts_syn.update(delta_j) # add attractors
            break # end loop
        
        # verifies if new attractor will be generated after one iteration
        if len(delta_j) != 0:
            Att_num += len(delta_j) / j # increase number of attractors
            Atts_syn.update(delta_j) # add new attractors
            total_set.difference_update(BR(delta_j, S)) # deletes states that reach attractor 
        
        #print(j)

        # adds attractors 
        delta_0.update(delta_j)
        j += 1

    #print(Atts_syn)

    # returns number of attractors and attractors states
    return Atts_syn, Att_num

def BR(delta_j, S):
    """
        BR - finds states that reach attractor (back reachable)

        delta_j: attractor
        S: BN state transition
    """

    # get all states
    States = set(S.keys())

    # delete states that are attractors
    States.difference_update(delta_j)

    # set to save states that reach attractor
    back_reachable = set()

    # adds state path (non attractors)
    curr_set = set()
    cond = False

    #print(States)

    # iterate non attractor states
    for state in States:
        
        # add current state in the path 
        curr_set.add(state)
        s = state

        # while the states have not reached an attractor
        while s not in delta_j:

            # extract new transition
            s = S[s]

            # if state reaches attractor exit while
            if s in delta_j:
                break

            # if curr state is an attractor
            if s in curr_set:
                cond = True
                break
            
            # add new transition to path (has not reached an attractor)
            curr_set.add(s)
        
        # if curr state is not an attractor
        if cond != True:
            # adds back reachable states (states that reach attractor)
            back_reachable.update(curr_set)
            curr_set = set()

        # in case state is an attractor start again another path
        else:
            curr_set = set()
            cond = False
            #States.difference_update(curr_set)

    # returns states that reach attractor 
    return back_reachable

def getElementsJCycle(total_set, S, j):
    """
        getElementsJCycle - searches if unvisited states are attractors based on j steps forward in state transitions

        total_set: unvisited states
        S: Boolean network state transitions (dictionary)
        j: number of time steps forward in state transition 
    """

    # to save attractors
    states = set()

    # iterate unvisited states
    for state in total_set:
        # unvisited state
        s = state

        # go forward in transition j times
        for i in range(j):
            # save new state transition
            st = S[s]
            s = st

        # verifies if after forward j times i end up in starting state (it means its an attractor)
        if state == st:
            # add attractor
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

    BN6 = {
        '00':'01',
        '01':'10',
        '10':'11',
        '11':'00'
    }

    Atts_syn, Att_num = attractors(BN6)

    print("Attractors:", Atts_syn)
    print("Number of attractors:", Att_num)'''

    