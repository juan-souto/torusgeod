import hyper_tools
import deep_tools
import math
import numpy as np

import parti_tools
from matplotlib import pyplot as plt
import os


def line_minimisation(given_parti,given_shear):
    number_of_steps = int(len(given_parti)/2)+1

    got_parti=[]
    got_parti = hyper_tools.hyper_parti(given_parti,given_shear)
    got_der = hyper_tools.read_der_parti(got_parti)
    step = deep_tools.scalar_prod(1/number_of_steps,got_der)

    mink =0
    minl = hyper_tools.length_hyper_parti(got_parti)

    new_shear = 0
    last_shear = 0
    new_parti = []
    steps = 0
    last_shear = given_shear

    for k in range(number_of_steps):
        steps = k
        new_shear = deep_tools.subtract_vector(last_shear,step)
        new_parti = hyper_tools.hyper_parti(given_parti,new_shear)
        new_length = hyper_tools.length_hyper_parti(new_parti)
        if new_length >= minl:
            return [last_shear,steps]
        else:
            last_shear = new_shear

    return [new_shear,steps]


def gradient_descent(given_parti,given_shear):
    loops = 0
    steps = 0
    got_parti = []
    got_parti = parti_tools.expand_parti(given_parti)
    got_parti = parti_tools.add_affixes(given_parti)
    got_parti = hyper_tools.hyper_parti(got_parti,given_shear)
    old_length = hyper_tools.length_hyper_parti(got_parti)
    new_parti = []
    new_shear = [0,0,0]
    old_shear = given_shear
    while True:
        loops +=1
        line_min = line_minimisation(given_parti,new_shear)
        new_shear = line_min[0]
        new_steps = line_min[1]
        steps += new_steps
        new_parti = hyper_tools.hyper_parti(given_parti,new_shear)
        new_length = hyper_tools.length_hyper_parti(new_parti)
        if new_length < old_length:
            old_length = new_length
            old_shear = new_shear
        else:
            return [old_shear,old_length,loops,steps]



def gradient_descent_plot(given_parti,given_shear,word):
    plt.ion()
    got_parti = []
    got_parti = parti_tools.expand_parti(given_parti)
    got_parti = parti_tools.add_affixes(given_parti)
    got_parti = hyper_tools.hyper_parti(got_parti,given_shear)
    old_length = hyper_tools.length_hyper_parti(got_parti)
    new_parti = []
    new_shear = [0,0,0]
    old_shear = given_shear
    n=[]
    x=[]
    y=[]
    count = 0
    while True:
        count += 1
        n.append(count)
        x.append(new_shear[0])
        y.append(new_shear[1])

        line_min = line_minimisation(given_parti,new_shear)
        new_shear = line_min[0]
        new_steps = line_min[1]
        new_parti = hyper_tools.hyper_parti(given_parti,new_shear)
        new_length = hyper_tools.length_hyper_parti(new_parti)
        if new_length < old_length:
            old_length = new_length
            old_shear = new_shear
            if new_length < 0.0001:
                break
            else:
                pass
        else:
            break

    fig, ax = plt.subplots()
    ax.scatter(x[:-1], y[:-1], color='red')
    ax.scatter(x[-1], y[-1], color='blue', marker="x")

    for i, txt in enumerate(n[:-1]):
        ax.annotate(txt, (x[i], y[i]))

    ax.set_title('The descent started at "1" and then followed the dots.\n '
                 'The blue cross indicates the estimated minimum')
    plt.show()

    print('')
    wanna_heat = input('It is possible that this was underwhelming... it might get (although it might not)\n'
                       'to see it on a heat map.This was maybe underwhelming... Press "Q" to quit, "H" to get\n'
                       'the heat map, an anything else to go back to the main menu. ')
    deep_tools.wanna_quit(wanna_heat)
    os.system('cls')
    if wanna_heat in ['h', 'H']:
        max_x = max(x)+2
        min_x = min(x)-2
        max_y = max(y)+2
        min_y = min(y)-2

        steps = 100
        step_x = (max_x-min_x)/steps
        step_y = (max_y-min_y)/steps

        center = [0, 0]
        data = np.empty((steps, steps))
        for k in range(steps):
            for n in range(steps):
                shear = [(min_x+k*step_x), (min_y+n*step_y),(-min_x-k*step_x-min_y-n*step_y)]
                data[steps-1-n, k] = math.log(hyper_tools.length_trace_free_group_word(word, shear))

        plt.imshow(data, cmap='autumn', interpolation='nearest')
        plt.colorbar()


        for k in range(len(x)-1):
            plt.plot(int((x[k]-min_x)/step_x), steps-1-int((y[k]-min_y)/step_y), color='blue', marker=".", markersize=10)
            kstr = str(k+1)
            plt.text(int((x[k]-min_x)/step_x), steps-1-int((y[k]-min_y)/step_y), kstr)

        plt.plot(int((x[-1]-min_x)/step_x), steps-1-int((y[-1]-min_y)/step_y), color='blue', marker="x", markersize=10)


        plt.title('The descent started at "1" and then followed the dots.\n '
                     'The blue cross indicates the estimated minimum')
        plt.show()
    else:
        pass

    os.system('cls')


def check_minimisation_radius(parti,shear,length,radius):
    k = 1
    minimal = False
    while not minimal:
        [min_length, min_shear] = minimize_around(parti, shear, k*radius, 200*k)
        if min_length < length:
            k = 2*k
        else:
            minimal = True

    return k


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



