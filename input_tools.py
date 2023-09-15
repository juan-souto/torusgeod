import hyper_tools
import math
import time
import get_parti
import combinatorial_parti



def what_shear():
    print("Enter the shearing coordinates of the torus you want to work with:")
    shear_A = float(input("Shear at arc 'A': "))
    shear_B = float(input("Shear at arc 'B': "))
    print("Shear at arc C (default is ", end='')
    print(-shear_A - shear_B, end="")
    shear_C = input(" so that the peripheral curve is parabolic): ")
    if shear_C.isdigit():
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
                       "            '5' matrix,\n"
                       "            'Q' quit.\n"
                       "    "
                       "Choice:  ")
        get_parti.wanna_quit(decide)
        if decide in ['1', '2', '3', '4', '5']:
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
    else:
        parti = get_parti.matrix_parti()
        start = None
        desired_length = 1000

    return [parti,start,decide,desired_length]


def global_get_parti():
    shear = what_shear()
    while True:
        [parti,start_time,decide,desired_length] = get_desired_parti(shear)
        if desired_length < 1200:
            computed_length = hyper_tools.computed_translation_length(parti,shear)
            print('')
            print("Length via trace        : ", computed_length)
        else:
            print('The desired length is too big for it to be computed via the trace')
        if decide in ['4','5']:
            parti = hyper_tools.hyper_parti(parti,shear)
        else:
            pass
        actual_length = hyper_tools.length_hyper_parti(parti)
        length_time = time.time()
        intersection_number = combinatorial_parti.compute_intersection_number(parti, parti)
        inter_time = time.time()
        homology = combinatorial_parti.parti_homology(parti)

        print('')
        print("Length                  : ", actual_length)
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
