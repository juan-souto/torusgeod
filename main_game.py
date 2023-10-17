import math
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pysine import sine

import deep_tools
import free_group
import get_parti
import hyper_tools
import combinatorial_parti
import minimisation
import find_systole
import parti_tools


def welcome():
    print('')
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print('%%%% Juan-has-way-too-much-time welcomes you %%%%')
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print('')
    print('   The point of this program is to be able to compute a few things')
    print('about geodesics in punctured tori, and hopefully help "visualize" ')
    print('some general facts. In principle everything could have been done for')
    print('more general surfaces with cusps, but I am not that bored...')
    print('')
    print('The fundamental group of the punctures torus is identified with F_2.')
    print("A,B are the standard generators and a,b are their inverses.")
    print('An element is "admissible" if it does not conjugate of a power of B. ')
    print('')
    query = input('Press "Q" to Quit or anything else to proceed. ')
    deep_tools.wanna_quit(query)
    deep_tools.limpia()


def main_menu():
    times = 0
    print('')
    print('These are your options:')
    print('')
    print('   (1) Go see a few things I can do.')
    print('   (2) Go to use a couple of tools.')
    print('')
    chosen = False
    query = ''
    while not chosen:
        query = input('Press "1", "2", or "Q" to Quit. ')
        deep_tools.wanna_quit(query)
        if query in ['1','2']:
            chosen = True
        else:
            pass

    deep_tools.limpia()

    if query == '1':
        watch_games()
    else:
        play_with_tools()
    exit()

def wanna_out():
    want_out = input("Press 'Q' to quit, 'B' to go back to the main menu, or anything else to do it again. ")
    deep_tools.wanna_quit(want_out)
    deep_tools.limpia()

    if want_out in ['b', 'B']:
        main_menu()
    else:
        pass



#######################################
#######################################

def play_with_tools():
    print('There are only a few things you can do here:')
    print('')
    print("   (1) Calculate intersection number of two curves")
    print('   (2) Calculate length of a curve in a given torus')
    print('   (3) Calculate the systole of a given torus')
    print('   (4) Estimate the torus where a given curve is minimized')
    print('')

    chosen = False
    wanna_do = ''
    while not chosen:
        wanna_do = input("Press '1', '2', '3', '4', 'Q' to quit or 'B' to go back. ")
        deep_tools.wanna_quit(wanna_do)
        if wanna_do in ['1','2','3','4','B','b']:
            chosen = True
        else:
            pass

    if wanna_do == '1':
        while True:
            deep_tools.limpia()

            print('Intersection form')
            print('')
            [word_1, actual_word_1] = free_group.get_element_in_free()
            parti_1 = free_group.free_group_parti(actual_word_1)
            [word_2, actual_word_2] = free_group.get_element_in_free()
            parti_2 = free_group.free_group_parti(actual_word_2)
            intersection = combinatorial_parti.compute_intersection_number(parti_1,parti_2)
            print('')
            print('The geometric intersection number is')
            print('   i(',word_1,',',word_2,') = ',intersection)
            print('')
            wanna_out()
    elif wanna_do == '2':
        while True:
            deep_tools.limpia()
            print('')
            print('Calculate length in some torus')
            print('')
            [word, actual_word] = free_group.get_element_in_free()
            print('')
            calculate_length_elsewhere(word, actual_word, [], 0)

            wanna_out()

    elif wanna_do == '3':
        while True:
            deep_tools.limpia()
            print("    We consider shearing coordinates on the punctured torus. If we think of the punctured torus")
            print('as the square torus punctured at the vertex, then shear_1 is the shearing along the vertical side,')
            print('shear_2 is the shearing along the horizontal side, and shear_3 is the shear only the diagonal')
            print('parallel to y=-x.')
            print('    This convention is so that shear_1, when the others are unchanged, does not change the length of B.')
            print('Similarly, shear_2 by itself does not change the length of A.')
            print('')
            shear_A = input("shear_1 (default is 0) = ")
            if deep_tools.isDigit(shear_A):
                shear_A = float(shear_A)
            else:
                shear_A = 0
            shear_B = input("shear_2 (default is 0) = ")
            if deep_tools.isDigit(shear_B):
                shear_B = float(shear_B)
            else:
                shear_B = 0

            print("shear_3 (default is ", end='')
            print(-shear_A - shear_B, end="")
            shear_C = input(" so that the peripheral curve is parabolic): ")
            if deep_tools.isDigit(shear_C):
                shear_C = float(shear_C)
            else:
                shear_C = -shear_A - shear_B
            shear = [shear_A, shear_B, shear_C]

            print('The systole of the given torus is ')
            print('   syst(',shear,') = ', find_systole.find_systole(shear))

            wanna_out()


    elif wanna_do == '4':
        while True:
            [word, actual_word] = free_group.get_element_in_free()
            parti = free_group.free_group_parti(actual_word)

            routine_length_minimisation(word, actual_word, parti, 0)

            wanna_out()

    else:
        main_menu()








#######################################
#######################################

def watch_games():
    while True:
        print('Here are your options:')
        print('   (1) Watch what gradient descent does (do not expect much).')
        print('   (2) Watch behaviour of size of homology for a sequence of random geodesics.')
        print('   (3) Convexity of length function (summary: you see the graph of a convex function).')
        print('   (4) Estimating lengths via intersections with longer and longer random geodesics.')
        print('   (5) Test if you can hear the difference between different types of randomly chosen geodesics.')
        print('   (6) Heatmap of the length function')
        print('   (7) Heatmap of the systole function')
        print('   (8) Length of a random geodesic in another torus.')
        print('   (9) Calculate things for a given geodesic.')
        print('')

        chosen = False
        wanna_do = ''
        while not chosen:
            wanna_do = input("Press '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Q' to quit or 'B' to go back. ")
            deep_tools.wanna_quit(wanna_do)
            if wanna_do in ['1','2','3','4','5','6','7','8','9','B','b']:
                chosen = True
            else:
                pass
        deep_tools.limpia()
        print('')

        if wanna_do in ['b','B']:
            main_menu()
        elif wanna_do == '1':
            [word, actual_word] = free_group.get_element_in_free('ABAAABababbbbaab')
            parti = free_group.free_group_parti(actual_word)
            minimisation.gradient_descent_plot(parti,[0,0,0],actual_word)
            pass
        elif wanna_do == '2':
            homology_random_walk()
        elif wanna_do == '3':
            convexity_length_function()
        elif wanna_do == '4':
            bonahon_length_random()
        elif wanna_do == '5':
            routine_musica()
        elif wanna_do == '6':
            heat_map_length_function()
        elif wanna_do == '7':
            heat_map_systole_function()
        elif wanna_do == '8':
            compare_in_different_tori()
        elif wanna_do == '9':
            individual_geod()
        else:
            pass
        wanna_out()


##########################
##########################
## The individual games ##
##########################
##########################


#######################################
# 2 = Track homology along a random ray
#######################################
def homology_random_walk():
    print("You will see how does the size of the homology vary over a random ray")
    print("A ray of length 500 takes a couple of seconds, of length 1000 clearly longer,")
    print("and for 2000 get yourself a drink.")
    wanna_length = input("Enter the desired length (>=500) of the ray (default is 1000), or press 'Q' to quit : ")
    deep_tools.wanna_quit(wanna_length)
    if deep_tools.isDigit(wanna_length):
        wanna_length = float(wanna_length)
        wanna_length = max(wanna_length, 500)
    else:
        wanna_length = 1000
    print('')
    print('Patience...')

    parti = get_parti.random_parti(wanna_length+100, [0, 0, 0])
    length = hyper_tools.hyper_parti(parti)
    k=1
    l=[]
    h=[]
    hom_list = []
    while k*10 < len(parti):
        new_parti = parti[:k*10]
        new_parti = parti_tools.close_parti(new_parti)
        hom = combinatorial_parti.parti_homology(new_parti)
        hom_list.append(hom)
        h.append(deep_tools.norm(hom))
        new_parti = parti_tools.add_affixes(new_parti)
        new_parti = hyper_tools.hyper_parti(new_parti,[0,0,0])
        l.append(hyper_tools.length_hyper_parti(new_parti))

        k +=1

    plt.xlabel("length along the ray")
    plt.ylabel('norm of the homology')
    plt.plot(l, h, color='red')

    plt.title('Norm of the homology when we run along the ray.\n '
                  'Note the difference in scale between both axes.')

    plt.show()
    print('')
    want_2dhom = input("Now we track the actual homology classes. Press 'Q' to quit or anything to continue")
    deep_tools.wanna_quit(want_2dhom)
    x = []
    y = []
    for k in range(len(hom_list)):
        x.append(hom_list[k][0])
        y.append(hom_list[k][1])

    plt.plot(x, y, color='red')

    plt.show()

    print('')
    wanna_help = input("Press 'H' if you want an explanation, 'Q' to quit, or anything else to continue.")
    deep_tools.wanna_quit(wanna_help)
    if wanna_help in ['h','H']:
        print("What we are doing is taking a random ray, running along that ray for a bit, closing it up to\n"
              "a curve, calculating its homology class, taking the norm, and then doing all over again for\n"
              "a 10 feet longer piece of ray. The sequence of homology classes is expected to look like a\n"
              "random walk on the homology group. ")
    else:
        pass

    deep_tools.limpia()

##################################
# 3 = convexity of length function
##################################

def convexity_length_function():
    print("This will show the graph of the length function of a given element along a \n"
          "segment in the space of shearing coordinates.")
    [word, actual_word] = free_group.get_element_in_free()

    shear_p1 = input("Initial point shear_1 (default is -10) = ")
    if deep_tools.isDigit(shear_p1):
        shear_p1 = float(shear_p1)
    else:
        shear_p1 = -10
    shear_p2 = input("Initial point shear_2 (default is 3) = ")
    if deep_tools.isDigit(shear_p2):
        shear_p2 = float(shear_p2)
    else:
        shear_p2 = 3
    shear_p = [shear_p1, shear_p2, -shear_p1 - shear_p2]

    shear_q1 = input("Final point shear_1 (default is 8) = ")
    if deep_tools.isDigit(shear_q1):
        shear_q1 = float(shear_q1)
    else:
        shear_q1 = 8
    shear_q2 = input("Final point shear_2 (default is 6) = ")
    if deep_tools.isDigit(shear_q2):
        shear_q2 = float(shear_q2)
    else:
        shear_q2 = 6
    shear_q = [shear_q1, shear_q2, -shear_q1 - shear_q2]

    step = deep_tools.subtract_vector(shear_q, shear_p)
    step = deep_tools.scalar_prod(1 / 500, step)
    x = []
    y = []
    for k in range(501):
        x.append(k / 500)
        y.append(hyper_tools.length_trace_free_group_word(actual_word, shear_p))
        shear_p = deep_tools.add_vector(shear_p, step)

    plt.plot(x, y, color='red')

    plt.title('Hopefully this really looks convex...')
    plt.show()

    print('')
    print('Although in general it is not really illuminating, you can also see a 3d graph')
    wanna_3d = input("Press 'Y' to see a 3d-graph of the length function, 'Q' to Quit or anything else to go back.")
    deep_tools.wanna_quit(wanna_3d)
    if wanna_3d in ['y', 'Y']:
        x = np.outer(np.linspace(-15, 15, 150), np.ones(150))
        y = x.copy().T
        z = x.copy()
        for k in range(len(x)):
            for n in range(len(y)):
                z[k, n] = hyper_tools.length_trace_free_group_word(actual_word,
                                                               [x[k, n], y[k, n], -x[k, n] - y[k, n]])

        fig = plt.figure(figsize=(14, 9))
        ax = plt.axes(projection='3d')

        surf = ax.plot_surface(x, y, z, cmap=cm.coolwarm)
        fig.colorbar(surf, shrink=0.5, aspect=5)

        plt.show()
    else:
        pass

    deep_tools.limpia()


#################################################################
# 4 = estimating lengths by taking intersections along random ray
#################################################################
def bonahon_length_random():

    print('We know that if we take any sequence of geodesics g_i converging to the Liouville measure\n'
          'then for any other geodesic g we have that the quantity i(g,g_i)/(pi^2 l(g_i)) converges\n'              
          'to l(g). What we do here is test this. You choose the geodesic g and then we take a random\n'
          'sequence g_i obtained from a randomly chosen ray.')
    print('')
    [word, actual_word] = free_group.get_element_in_free('AB')
    parti = free_group.free_group_parti(actual_word)
    act_length = hyper_tools.length_trace_free_group_word(word,[0,0,0])
    print('')
    print("Now you choose the length of the ray. A ray of length 500 takes a few of seconds, of\n"
              "length 1000 takes the time of pouring yourself a cup of coffee, and for length 2000\n"
              "you can maybe make yourself some tea. ")
    print('')
    wanna_length = input("Enter the desired length (>=500) of the ray (default is 1000), or press 'Q' to quit : ")
    deep_tools.wanna_quit(wanna_length)
    print('Patience...')
    if deep_tools.isDigit(wanna_length):
        wanna_length = float(wanna_length)
        wanna_length = max(wanna_length, 500)
    else:
        wanna_length =500

    parti2 = get_parti.random_parti(wanna_length+100, [0, 0, 0])
    k=1
    l=[]
    p=[]
    while k*10 < len(parti2):
        new_parti = parti2[:k*10]
        new_parti = parti_tools.close_parti(new_parti)
        new_parti = parti_tools.add_affixes(new_parti)
        new_parti = hyper_tools.hyper_parti(new_parti,[0,0,0])
        len2 = hyper_tools.length_hyper_parti(new_parti)
        inter = combinatorial_parti.compute_intersection_number(parti,new_parti)
        pred = inter * (math.pi ** 2) / len2
        error = 100*(pred-act_length)/act_length
        p.append(error)
        l.append(len2)
        k +=1

    plt.plot(l, p, color='red')
    plt.axhline(0)
    plt.ylabel('% error when estimating the length of g\n'
                   'by counting intersections with random geodesics g_i')
    plt.xlabel('Length of random geodesic g_i')

    title_text = '% error when estimating length of\n'+str(word)
    plt.title(title_text)
    plt.show()

    deep_tools.limpia()


#######################
# 5 = singing geodesics
#######################

def routine_musica():
    print("This is supposed to make clear how different are random geodesics, geodesics arising from\n"
          "random elements in pi_1, and random simple geodesics. To do that we play some music\n"
          "as follows: every time that the geodesic hits the arc corresponding to the vertical side of the square torus\n"
          "we play 'la' and when it hits the horizontal side we play 'fa', both times with direction equal to the next\n"
          "hit. The result is a hit!!! OK, basically we get the following:\n"
          "   (1) 'random geodesics' sound most of the time plainly awful\n"
          "   (2) 'random element in pi_1' sound like me playing the recorder (If there were any doubts, I don't know how to play)\n"
          "   (3) 'random simple geodesics' sound vaguely like one could be having a joint while listening to it.\n"
          "\n")
    done_listening = False
    while not done_listening:
        choice = input("Do you want to listen? (for 20 sec at most)\n "
                       "Press '1', '2' or '3' to pick the type, "
                       "'Q' to quit on anything else to continue.")
        if choice in ['1','2','3']:
            pass_choice = int(choice)-1
            if choice == '1':
                pass_chosen = 'random geodesic.'
            elif choice == '2':
                pass_chosen = 'random element in \pi_1.'
            else:
                pass_chosen = 'random simple geodesic.'
            play_music(pass_choice,pass_chosen)

        else:
            done_listening = True
    played = False
    wanna_play = True
    while wanna_play:
        if not played:
            print( "Do you want to see if you can recognize each type?")
        else:
            print("Do you want to try again?")
        wanna_listen = input("   Press 'Y' to listen or anything else to continue. ")
        if wanna_listen in ['y', 'Y']:
            choice = random.randint(0, 2)

            play_music(choice)
            print("")
            input('Do you know what this was? Press anything to continue. ')
            print('')
            if choice == 0:
                print('   It was a '+'\033[92m random geodesic\033[00m')
            elif choice == 1:
                print('   It was a '+'\033[92m random element in pi_1\033[00m')
            else:
                print('   It was a '+'\033[92m random simple geodesic\033[00m')
            played = True
        else:
            wanna_play = False
            deep_tools.limpia()
            watch_games()


def play_music(choice,chosen=None):
    print('')
    print('Preparing the music...')

    if choice == 0:
        parti = get_parti.random_parti(100, [0, 0, 0])
        parti = parti_tools.expand_parti(parti)
        parti = parti_tools.add_affixes(parti)
        parti = hyper_tools.hyper_parti(parti, [0, 0, 0])
        length = hyper_tools.length_hyper_parti(parti)

        scale = 0.5
        musik = get_music(parti, 20, scale)

    elif choice == 1:
        parti = get_parti.random_free_group_parti(100, [0, 0, 0])
        parti = parti_tools.expand_parti(parti)
        parti = parti_tools.add_affixes(parti)
        parti = hyper_tools.hyper_parti(parti, [0, 0, 0])
        length = hyper_tools.length_hyper_parti(parti)

        scale = 0.5
        musik = get_music(parti, 20, scale)

    else:
        parti = get_parti.random_simple_kette(100, [0, 0, 0])
        parti = parti_tools.expand_parti(parti)
        parti = parti_tools.add_affixes(parti)
        parti = hyper_tools.hyper_parti(parti, [0, 0, 0])
        length = hyper_tools.length_hyper_parti(parti)

        scale = 0.5
        musik = get_music(parti, 20, scale)

    print('')
    if chosen is None:
        input("Ready? Press anything to listen. ")
    else:
        input("Ready? Press anything to listen to a "+chosen)

    FA = 349.228
    LA = 440.000

    for x in musik:
        if x[0] == 'A':
            sine(frequency=LA, duration=x[1] * scale)
        else:
            sine(frequency=FA, duration=x[1] * scale)


def get_music(parti,cuanto_dura,scale):
    total_time = 0
    k = 0
    pre_musica = []
    while total_time < cuanto_dura and k < len(parti):
        pre_musica.append([parti[k].tipo,parti[k].length])
        total_time += parti[k].length * scale
        k += 1
    musica = []
    while len(pre_musica)>0:
        if pre_musica[0][0] == 'A':
            tiempo = 0
            while len(pre_musica)>0 and pre_musica[0][0] != 'B':
                tiempo += pre_musica[0][1]
                pre_musica = pre_musica[1:]
            musica.append(['A',tiempo])
        elif pre_musica[0][0] == 'B':
            tiempo = 0
            while len(pre_musica)>0 and pre_musica[0][0] != 'A':
                tiempo += pre_musica[0][1]
                pre_musica = pre_musica[1:]
            musica.append(['B',tiempo])
        else:
            print('Boom')
    return musica


#################################
# 6 = heat map of length function
################################
def heat_map_length_function():
    print('This produces a heat map of the log of the length function of a chosen element as you\n'
              'move around using shear coordinates. The reason for the log is that log highlights when\n'
              'the length is small. This is important for simple curves.\n'
              '\n'
              'If the element is not simple, then in the map you also see what the gradient descent\n'
              'suggests a location of the minimum of the length function.')
    print('')
    [word, actual_word] = free_group.get_element_in_free()
    parti = free_group.free_group_parti(actual_word)
    simple = True
    if combinatorial_parti.compute_intersection_number(parti, parti) > 0:
        simple = False

    else:
        pass

    while True:
        if simple:
            print('Your curve is simple. If you take a large radius, you might find a divition by 0 error.')
            radius = input("What radius around [0,0] do you want to see? (default is 10) = ")
        else:
            radius = input("What radius around [0,0] do you want to see? (default is 50) = ")
        if deep_tools.isDigit(radius):
            radius = 2 * float(radius)
        else:
            if simple:
                radius = 2 * 10
            else:
                radius = 2 * 50

        steps = 100
        center = [0, 0]
        data = np.empty((steps, steps))
        for k in range(steps):
            for n in range(steps):
                shear = [radius * (k - steps / 2) / steps + center[0], radius * (n - steps / 2) / steps + center[1],
                             radius * (steps - k - n) / steps - center[0] - center[1]]
                data[k, n] = math.log(hyper_tools.length_trace_free_group_word(word, shear))
        plt.imshow(data, extent=(center[0] - radius / 2,center[0] + radius / 2, center[1] - radius / 2,center[1] + radius / 2),
                   cmap='autumn', interpolation='nearest')
        plt.colorbar()
        if not simple:
            [min_shear, length, loops, steps] = minimisation.gradient_descent(parti, [0, 0, 0])
            plt.plot(min_shear[0], min_shear[1], marker='v', color="white")

        added_title = "Heatmap of the log of the length function of\n" + word
        plt.title(added_title)
        plt.show()

        print("Do you want to see what happens if you take a different radius?")
        wanna_out()


##################################
# 7 = heat map of systole function
##################################
def heat_map_systole_function():
    while True:
        print('This gives you a heatmap of the systole function.\n'
                  '\n'
                  'You can choose the center and the radius, however your map is forced to\n'
                  'be contained in a 18x18 square centered at [0,0], just to prevent\n'
                  'the program crashing.')
        print('')
        print('Enter the shear coordinates of the center:')
        shear_A = input("   shear_1 (default is 0) = ")
        if deep_tools.isDigit(shear_A):
            shear_A = float(shear_A)
        else:
            shear_A = 0
        shear_B = input("   shear_2 (default is 0) = ")
        if deep_tools.isDigit(shear_B):
            shear_B = float(shear_B)
        else:
            shear_B = 0
        print('')
        radius = input('Enter the radius (default=5): ')
        if deep_tools.isDigit(radius):
            radius = min(18.5, 2*float(radius))
            radius = min(radius - shear_A, radius - shear_B)
        else:
            radius = min(10 - shear_A, 10 - shear_B)
        if radius == 0:
            print('The center was outside of the allowed region')
        else:
            pass
        print('')
        print('Patience...')

        steps = 500
        center = [shear_A, shear_B]
        data = np.empty((steps, steps))
        for k in range(steps):
            for n in range(steps):
                shear = [radius * (k - steps / 2) / steps + center[0], radius * (n - steps / 2) / steps + center[1],
                             radius * (steps - k - n) / steps - center[0] - center[1]]
                data[k, n] = find_systole.find_systole(shear)

        plt.imshow(data, cmap='autumn', interpolation='nearest')

        plt.colorbar()

        plt.title("Heatmap of th systole function")
        plt.show()

        deep_tools.limpia()
        print("Do you want to do it again?")
        wanna_out()


#####################################################
# 8 = compare length of random geodesic in other tori
#####################################################

def compare_in_different_tori():
    have_done = False
    print('The length of the Liouville current (or measure, as you wish) is minimized\n'
          'in the surface whose Liovulle current you are taking. It follows that if you\n'
          'take a random geodesic in the square torus and you calculate its length \n'
          'there and elsewhere, then the elsewhere length should be larger...\n'
          'Do you want to check this?')
    print('')
    shear = [0,0,0]
    while True:
        if have_done:
            print("Do you want to try it again?")
        else:
            pass
        want_quit = input("Press 'Q' to quit, 'B' to go to the main menu, or anything else to continue. ")
        deep_tools.wanna_quit(want_quit)
        if want_quit in ['b','B']:
            main_menu()
        else:
            pass
        if have_done:
            default1 = str(shear[0])
            default2 = str(shear[1])
        else:
            default1 = '-5'
            default2 = '2'

        print('Enter the shear coordinates of the new torus:')
        shear_A = input("   shear_1 (default is "+default1+") = ")
        if deep_tools.isDigit(shear_A):
            shear_A = float(shear_A)
        else:
            shear_A = -5
        shear_B = input("   shear_2 (default is "+default2+") = ")
        if deep_tools.isDigit(shear_B):
            shear_B = float(shear_B)
        else:
            shear_B = 2
        print('')

        shear = [shear_A, shear_B, -shear_A-shear_B]
        wanted_length = input('How long (Default = 200) should the random geodesic be? ')
        if deep_tools.isDigit(wanted_length):
            wanted_length = float(wanted_length)
        else:
            wanted_length = 200

        parti = get_parti.random_parti(wanted_length,[0,0,0])
        length_square = hyper_tools.length_hyper_parti(parti)
#        parti = parti_tools.add_affixes(parti)

        parti2 = hyper_tools.hyper_parti(parti,shear)
        length_new = hyper_tools.length_hyper_parti(parti2)
        deep_tools.limpia()

        print('')
        print('New torus has shear coordinates (',shear[0],',',shear[1],')')
        print('   Length in the square torus = ',length_square)
        print('   Length in the new torus    = ',length_new)
        print('')
        if length_new>length_square:
            print('As expected, the random curve was longer in the new torus.')
        else:
            print('Well... this is not what was expected... maybe your torus is too close\n'
                  'to the square torus, or maybe it was just a fluke. Try again!')
        print('')


        have_done = True



#####################################################
# 9 = look at individual geodesics
#####################################################

def individual_geod(old_word=None,old_actual_word=None):
    word = ''
    actual_word = ''
    length = 0
    if old_word is None:
        [word,actual_word] = free_group.get_element_in_free('ABBAAbbbAbAba')
    else:
        deep_tools.limpia()

        print('')
        change = input("Do you want to change your element? If you do, enter 'Y'. ")
        if change in ['y','Y']:
            [word,actual_word] = free_group.get_element_in_free()
        else:
            word = old_word
            actual_word = old_actual_word

    parti = free_group.free_group_parti(actual_word)
    self_intersection = combinatorial_parti.compute_intersection_number(parti,parti)
    homology_class = combinatorial_parti.parti_homology(parti)[:2]
    if word != actual_word:
        homology_class = deep_tools.scalar_prod(-1,homology_class)
    else:
        pass
    parti = hyper_tools.hyper_parti(parti,[0,0,0])

    deep_tools.limpia()

    print('')
    print("Element = ",word)
    print('   Homology class             : ',homology_class)
    print('   Self-intersection number   : ',self_intersection)
    real_length = hyper_tools.length_trace_free_group_word(word,[0,0,0])
    print('   Length in the square torus : ',real_length)
    print('')
    if self_intersection == 0:
        print('   The element ',word,' is simple and hence its infimum length over Teichmueller space is equal to 0')
        print('')
        input('Press any key to continue. ')

    else:
        routine_length_minimisation(word, actual_word, parti, real_length)

    deep_tools.limpia()

    after_basic_options(word,actual_word,parti,real_length)


def routine_length_minimisation(word,actual_word,parti,real_length):
    [min_shear, length, loops, steps] = minimisation.gradient_descent(parti, [0, 0, 0])

    print('')
    print('   It seems that the length of the given element is minimised for a torus with ')
    print('      shear coordinates more or less equal to')
    print('           ', min_shear)
    print('      There, the length function takes the value ', length)
    print('      Moreover, the systole in that torus is ', find_systole.find_systole(min_shear))
    print('')
    print('   How accurate is the minimisation proces?')
    radius = len(parti) / 200
    print('      For a word of your length, most of the time gradient descend seems to give a result')
    print('      within distance ', radius, ' of the actual minimiser, but sometimes the error')
    print('      is larger.')
    print(' ')
    wanna_check = input('   Press "Y" if want to check? (It might take a while.) ')
    if wanna_check in ['y', 'Y']:
        powers = minimisation.check_minimisation_radius(parti, min_shear, length, radius)
        print('')
        adjective = ''
        if powers == 1:
            adjective = 'indeed is'
        else:
            adjective = 'is rather'
        print('      I am done checking: It seems to me that the actual minimum '+adjective+' within ', powers * radius)
        print('         of the estimated point.')
        print('')

        wanna_do = input("Press 'H' for a minimal description of how did the distance get bounded,\n"
                         "or any other key to continue. ")

        if wanna_do in ['h','H']:
            print('')
            print('The length function is convex in shear coordinates. It thus follows that to decide if the minimum \n'
                  'is inside some closed convex set K it suffices to prove that the minimum of the length function on \n'
                  'on K is taken in the interior. In this case I am interested in round balls B(x,r) around the \n'
                  'minimizer x. To "check" whether the minimum of the length function is taken in the interior of the \n'
                  'ball I calculate the length function at a bunch of points in the boundary. More specifically, \n'
                  'starting with k=1, I calculate for the length at 200 * k points at distance "R = k times the estimated\n'
                  'radius". If I do not find any point where the length is smaller than at x, then I infer that the \n'
                  'minimum is indeed achieved within "R" of x. Otherwise I increase k to 2k, 4k, 8k,...')
            print('')
            input('Press any key to continue.')
    else:
        print('')

    return [word,actual_word,parti,real_length]


def after_basic_options(word,actual_word,parti,given_length):
    deep_tools.limpia()

    print('')
    print('Here are your current options:')
    print('')
    print('   (1) Calculate the intersection number with another element')
    print('   (2) Calculate the length of the given element in another torus')
    print('   (3) Use a random curve in the square torus to estimate the length ')
    print('       and see how this compares to the actual value.')
    print('   (4) Enter a new element altogether.')
    print('')
    chosen = False
    wanna_do = ''
    while not chosen:
        wanna_do = input("Enter '1', '2', '3', '4', 'B' to go back to the main menu or 'Q' to quit. ")
        deep_tools.wanna_quit(wanna_do)
        if wanna_do in ['1','2','3','4','b','B']:
            chosen = True
        else:
            pass
    deep_tools.limpia()

    if wanna_do == '1':
        intersection_with_curve(word,actual_word,parti,given_length)
    elif wanna_do == '2':
        bla = calculate_length_elsewhere(word, actual_word, parti,given_length)
        print('')
        input('Press any key to continue')
        deep_tools.limpia()
        after_basic_options(bla[0],bla[1],bla[2],bla[3])
    elif wanna_do == '3':
        calculate_bonahon_length(word, actual_word, parti,given_length)
    elif wanna_do == '4':
        print('')
        individual_geod()
    else:
        main_menu()


def intersection_with_curve(word, actual_word, parti,given_length):
    print('')
    print('Please enter the second element in \pi_1.')
    print("Recall that A,B are the standard generators and a,b are their inverses, and that")
    print("and that we only admit elements which are not conjugated to a power of B.")
    print('')
    [word2, actual_word2] = free_group.get_element_in_free('ABBA')
    parti2 = free_group.free_group_parti(actual_word2)
    intersection = combinatorial_parti.compute_intersection_number(parti, parti2)
    print('')
    print('Geometric intersection number:')
    print('    i(',word,',',word2,') = ',intersection)
    print('')
    input('Press any key to continue.')

    after_basic_options(word, actual_word, parti,given_length)

def calculate_length_elsewhere(word, actual_word, parti,given_length):
    print("   We consider shearing coordinates on the punctured torus. If we think of the punctured torus")
    print('as the square torus punctured at the vertex, then shear_1 is the shearing along the vertical side,')
    print('shear_2 is the shearing along the horizontal side, and shear_3 is the shear only the diagonal')
    print('parallel to y=-x.')
    print('   This convention is so that shear_1, when the others are unchanged, does not change the length of B.')
    print('Similarly, shear_2 by itself does not change the length of A.')
    print('')
    shear_A = input("shear_1 (default is 0) = ")
    if deep_tools.isDigit(shear_A):
        shear_A = float(shear_A)
    else:
        shear_A = 0
    shear_B = input("shear_2 (default is 0) = ")
    if deep_tools.isDigit(shear_B):
        shear_B = float(shear_B)
    else:
        shear_B = 0

    print("shear_3 (default is ", end='')
    print(-shear_A - shear_B, end="")
    shear_C = input(" so that the peripheral curve is parabolic): ")
    if deep_tools.isDigit(shear_C):
        shear_C = float(shear_C)
    else:
        shear_C = -shear_A - shear_B
    shear = [shear_A, shear_B, shear_C]
    print('')

    new_length = hyper_tools.length_trace_free_group_word(word,shear)
    print('The element ',word,' has length ',new_length,' at the torus ',shear)

    return [word,actual_word,parti,given_length]


def calculate_bonahon_length(word, actual_word, parti,given_length):
    print("   We estimate the length of the given element via computing the intersection number with a")
    print('random geodesic, that is one which approaches the Liouville measure.')
    print('You can choose about how long you want that random geodesic to be. To avoid silly issues I force it to have')
    print('at least length 50. If you choose the length of the random geodesic to be about 1000 it takes seconds,')
    print('if you want it to be about 5000 it takes minutes.')
    print('')
    wanna_length = input("Enter the desired length (default 500) got the random geodesic, or press 'Q' to quit : ")
    deep_tools.wanna_quit(wanna_length)
    if deep_tools.isDigit(wanna_length):
        chosen = True
        wanna_length = float(wanna_length)
        wanna_length = max(wanna_length, 50)
    else:
        wanna_length = 500

    parti2 = get_parti.random_parti(wanna_length,[0,0,0])
    length2 = hyper_tools.length_hyper_parti(parti2)
    print('')
    print('We will be working with a random geodesic of')
    print('length(random) = ',length2)
    print('Geometric intersection number:')
    intersection = combinatorial_parti.compute_intersection_number(parti, parti2)
    print('    i(',word,', random ) = ',intersection)
    print('Estimated length of ',word)
    est_length = intersection*(math.pi**2)/length2
    error = int(10000*((est_length/given_length)-1))/100
    print('    Estimated length = ',intersection*(math.pi**2)/length2)
    print('    Actual length    = ',given_length)
    print('    Error            = ',error,'%')
    print('')
    wanna_do = input("Press 'Q' to quit or anything else to continue. ")
    deep_tools.wanna_quit(wanna_do)

    after_basic_options(word, actual_word, parti,given_length)


