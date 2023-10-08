import hyper_tools
import math

def markov_move(given_tuple):   # (A,B,AB)
    [x,y,z] = given_tuple
    if x*y-z < z:
        return [x,y,x*y-z]
    elif y*z-x < x:
        return [y,z,y*z-x]
    elif z*x-y < y:
        return [z,x,y]
    else:
        return [x,y,z]


def markov_search_move(shear):
    x = hyper_tools.trace_free_group_word('A',shear)
    y = hyper_tools.trace_free_group_word('B',shear)
    z = hyper_tools.trace_free_group_word('AB',shear)

    new_tuple = [x,y,z]
    old_tuple = ['','','']

    while new_tuple != old_tuple:
        old_tuple = new_tuple
        new_tuple = markov_move(old_tuple)

    return new_tuple


def find_systole(shear):
    min_tuple = markov_search_move(shear)
    trace_syst = min(min_tuple)
    length_syst = 2*math.acosh(trace_syst/2)

    return(length_syst)


