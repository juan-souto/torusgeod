import hyper_tools
import deep_tools
import random
import math

import parti_tools


def linear_move(given_parti,given_shear,given_vect):
    new_parti = []
    new_shear = []
    new_shear = deep_tools.add_vector(given_shear,given_vect)
    new_parti = hyper_tools.hyper_parti(given_parti,new_shear)
    return new_parti


def line_minimisation(given_parti,given_shear):
    number_of_steps = len(given_parti)

    got_parti=[]
    got_parti = hyper_tools.hyper_parti(given_parti,given_shear)
    got_der = hyper_tools.read_der_parti(got_parti)
    step = deep_tools.scalar_prod(1/number_of_steps,got_der)

    mink =0
    minl = hyper_tools.length_hyper_parti(got_parti)

    new_shear = 0
    last_shear = 0
    new_parti = []
    last_shear = given_shear

    for k in range(number_of_steps):
        new_shear = deep_tools.subtract_vector(last_shear,step)
        new_parti = hyper_tools.hyper_parti(given_parti,new_shear)
        new_length = hyper_tools.length_hyper_parti(new_parti)
        if new_length >= minl:
            return last_shear
        else:
            last_shear = new_shear

    return new_shear


def gradient_descent(given_parti,given_shear):
    got_parti = []
    got_parti = parti_tools.expand_parti(given_parti)
    got_parti = parti_tools.add_affixes(given_parti)
    got_parti = hyper_tools.hyper_parti(got_parti,given_shear)
    old_length = hyper_tools.length_hyper_parti(got_parti)
    print(old_length)
    new_parti = []
    new_shear = [0,0,0]
    old_shear = given_shear
    while True:
        new_shear = line_minimisation(given_parti,new_shear)
        new_parti = hyper_tools.hyper_parti(given_parti,new_shear)
        new_length = hyper_tools.length_hyper_parti(new_parti)
        if new_length < old_length:
            print(new_length)
            old_length = new_length
            old_shear = new_shear
        else:
            return [old_shear,old_length]









def minimize_around(parti,shear,tol,steps=None):
    min_length = 1000000
    back_shear = [0,0,0]
    if steps is None:
        steps = 1000
    for n in range(steps):
        new_shear = deep_tools.add_vector(shear,[math.cos(n*math.pi/steps)*tol,math.sin(n*math.pi/steps)*tol,
                                                 -math.cos(n*math.pi/steps)-math.sin(n*math.pi/steps)*tol])
        parti = hyper_tools.hyper_parti(parti,new_shear)
        new_length = hyper_tools.length_hyper_parti(parti)
        if new_length < min_length:
            min_length = new_length
            back_shear = new_shear
        else:
            pass
    return [min_length,back_shear]



