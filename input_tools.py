import free_group
import hyper_tools
import math
import time
import get_parti
import combinatorial_parti
import deep_tools
import random
import minimisation

import mapping_class_action
import parti_tools


def what_shear():
    print("Enter the shearing coordinates of the torus you want to work with:")
    shear_A = input("Shear at arc 'A': ")
    if deep_tools.isDigit(shear_A):
        shear_A = float(shear_A)
    else:
        shear_A = 0
    shear_B = input("Shear at arc 'B': ")
    if deep_tools.isDigit(shear_B):
        shear_B = float(shear_B)
    else:
        shear_B = 0

    print("Shear at arc C (default is ", end='')
    print(-shear_A - shear_B, end="")
    shear_C = input(" so that the peripheral curve is parabolic): ")
    if deep_tools.isDigit(shear_C):
        shear_C = float(shear_C)
    else:
        shear_C = -shear_A - shear_B
    return [shear_A, shear_B, shear_C]


def what_geodesic():
    attempt = False

    while not attempt:
        decide = input("Choose      '1' random geodesic,\n"
                       "            '2' farey geodesic, \n"
                       "            '3' random simple geodesic, \n"
                       "            '4' custom sequence of Ls and Rs,\n"
                       "            '5' custom element in pi_1,\n"
                       "            '6' matrix,\n"
                       "            'Q' quit.\n"
                       "    "
                       "Choice:  ")
        deep_tools.wanna_quit(decide)
        if decide in ['1', '2', '3', '4', '5', '6']:
            print('')
            attempt = True
        else:
            pass

    return decide

def what_length():
    wished_length = input("About which length you want the geodesic? "
                              "(Default 500 --- might take a few sec) ")
    if wished_length.isdigit():
        desired_length = int(wished_length)
    else:
        desired_length = 500
    return desired_length


def get_desired_parti(shear):
    decide = what_geodesic()
    if decide in ['1', '2', '3']:
        desired_length = what_length()
        start = time.time()
        if decide == '1':
            parti = get_parti.random_parti(desired_length,shear)
        elif decide == '2':
            parti = get_parti.farey_parti(desired_length,shear)
        else:
            print("The curve will have roughly the desired length in the square punctured torus")
            parti = get_parti.random_simple_kette(desired_length,shear)
    elif decide == '4':
        parti = get_parti.custom_parti()
        start = None
        desired_length = 1000
    elif decide == '5':
        parti = get_parti.free_group_parti()
        start = None
        desired_length = 1000
    else:
        parti = get_parti.matrix_parti()
        start = None
        desired_length = 1000

    return [parti,start,decide,desired_length]


def global_get_parti():
    while True:
        shear = what_shear()

        [parti,start_time,decide,desired_length] = get_desired_parti(shear)
        if desired_length < 1200:
            computed_length = hyper_tools.computed_translation_length(parti,shear)
            print('')
            print("Length via trace        : ", computed_length)
        else:
            print('The desired length is too big for it to be computed via the trace')
        if decide not in ['1','2','3']:
            parti = parti_tools.add_affixes(parti)
            parti = hyper_tools.hyper_parti(parti,shear)
        else:
            pass
        actual_length = hyper_tools.length_hyper_parti(parti)
        der = hyper_tools.read_der_parti(parti)
        length_time = time.time()
        intersection_number = combinatorial_parti.compute_intersection_number(parti, parti)
        inter_time = time.time()
        homology = combinatorial_parti.parti_homology(parti)
        if len(parti)<10:
            parti_tools.print_parti(parti)

        mat1 = hyper_tools.mob_parti_linear(parti, [1, 0], shear)
        mat2 = hyper_tools.mob_parti_linear(parti, [0, 1], shear)

        print('')
        print("Shear                   : ",shear)
        print("Length                  : ", actual_length)
        print("Derivative              : ", der)
        print("Matrix                  : ",mat1[0],"  ",mat2[0])
        print("                          ",mat1[1],"  ",mat2[1])

        print('Self-Intersection number: ', intersection_number)
        print('Homology class          : ', homology)
        if decide == '1':
            print("The quotient i(gamma,gamma)/l(gamma)^2 is ", intersection_number / (actual_length ** 2),
                  ' (asymptotic value is ', 1 / math.pi ** 2, ')')
        else:
            pass
        if decide in ['1','2','3']:
            print('')
            print('        time to get length             : ', length_time - start_time)
            print('        time to get intersection number: ', inter_time - length_time)
        else:
            pass
        print('')


def length_intersection():
    while True:
        shear=[0,0,0]
        desired_length = what_length()

        random_parti = get_parti.random_parti(desired_length,shear)
        custom_parti = get_parti.custom_parti()
        custom_parti = parti_tools.add_affixes(custom_parti)

        custom_parti = hyper_tools.hyper_parti(custom_parti, shear)

        intersection_number1 = combinatorial_parti.compute_intersection_number(random_parti, custom_parti)
        length1 = hyper_tools.length_hyper_parti(custom_parti)
        intersection_number2 = combinatorial_parti.compute_intersection_number(random_parti, random_parti)
        length2 = hyper_tools.length_hyper_parti(random_parti)
        print("Custom length : ",length1)
        print("Random length : ",length2)
        print("Bonahon random length: ",intersection_number2*(math.pi**2)/length2)
        print("Bonahon custom length: ",intersection_number1*(math.pi**2)/length2)
        print("Random error :",100*(intersection_number2*(math.pi**2)/length2-length2)/length2," %")
        print("Custom error :",100*(intersection_number1*(math.pi**2)/length2-length1)/length1," %")

def check_intersection():
    while True:
        parti1 = get_parti.custom_parti()
        parti2 = get_parti.custom_parti()
        print(combinatorial_parti.compute_intersection_number(parti1, parti2))


#------------------------------------------
#------------------------------------------
#------------------------------------------

def track_random_walk_map():
    shear=[0,0,0]
    baseword = "AB"
    mapclass = ''
    hand = ''
    while True:
        flip = random.randint(0,1)
        if flip == 0:
            hand += 'L'
        else:
            hand += 'R'
        mapclass = mapclass + hand
        word = mapping_class_action.mapclass_on_free(mapclass,baseword)
        directions = free_group.translate_free_word_to_directions(word)
        kette = parti_tools.word_to_kette(directions)
        parti = parti_tools.kette_to_parti(kette)
        homology = combinatorial_parti.parti_homology(parti)
        homology_size = abs(homology[0])+abs(homology[1])
        lamination = [homology[0]/homology_size,homology[1]/homology_size]
        parti = parti_tools.add_affixes(parti)

        parti = hyper_tools.hyper_parti(parti,shear)
        length = hyper_tools.length_hyper_parti(parti)

        print('l = ',length,' size of homology = ',homology_size,' looks like lamination = ',lamination)
        time.sleep(1)


def track_powers_of_map():
    shear=[0,0,0]
    word = "AB"
    mapclass=mapping_class_action.get_mapping_class()
    while True:
        for x in mapclass:
            word = mapping_class_action.elementary_map_on_free(x,word)
        directions = free_group.translate_free_word_to_directions(word)
        kette = parti_tools.word_to_kette(directions)
        parti = parti_tools.kette_to_parti(kette)
        homology = combinatorial_parti.parti_homology(parti)
        homology_size = abs(homology[0])+abs(homology[1])
        lamination = [homology[0]/homology_size,homology[1]/homology_size]
        parti = parti_tools.add_affixes(parti)

        parti = hyper_tools.hyper_parti(parti,shear)
        length = hyper_tools.length_hyper_parti(parti)

        print('l = ',length,' size of homology = ',homology_size,' looks like lamination = ',lamination)
        time.sleep(1)


def compare_in_different_tori():
    shear = [-5, 2, 3]
    parti = get_parti.random_parti(200,[0,0,0])
    print(hyper_tools.length_hyper_parti(parti))
    parti = parti_tools.add_affixes(parti)

    parti2 = hyper_tools.hyper_parti(parti,shear)
    print(hyper_tools.length_hyper_parti(parti))


def total_minimisation(parti,shear):
    parti = parti_tools.expand_parti(parti)
    parti = parti_tools.add_affixes(parti)

    [new_shear,length] = minimisation.gradient_descent(parti,shear)

    print('')
    print('It seems that the length is minimised around ',new_shear)
    print('   The length function takes there the value ',length)
    print('')
    radius = len(parti)/10000
    print('I am checking 5000 points at distance ',radius,' from that point...')

    [min_length,min_shear]=minimisation.minimize_around(parti,new_shear,radius,5000)

    if min_length>length:
        print("Indeed, I didn't find any better point")
    else:
        print("CELHP!!! I found a better point... The value of the length there is ",min_length)
        print('Let me look a bit further...')
        print('I am checking 5000 points at distance ', 10*radius, ' from that point...')

        [min_length, min_shear] = minimisation.minimize_around(parti, new_shear, 10*radius, 5000)
        if min_length > length:
            print("Ok, now I didn't find any better point")
        else:
            print("FFS!!! Again a better point... The value of the length there is ", min_length)
            print("I give up!")



