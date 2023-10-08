import parti_tools
import hyper_tools
import math
import random
import free_group
import deep_tools




def custom_parti():
    attempt = False
    while not attempt:
        word = input("    Enter a sequence of 'L's and 'R's as in LRRRLRRLLRL or press 'Q' to quit:  ")
        deep_tools.wanna_quit(word)

        problem = False
        if len(word) == 0:
            problem = True
        else:
            pass
        for x in word:
            if x not in ['L','R','l','r']:
                problem = True
            else:
                pass
        if problem:
            pass
        else:
            word=word.upper()
            attempt = True

    parti = []
    kette = parti_tools.word_to_kette(word)
    parti = parti_tools.kette_to_parti(kette)
    if parti_tools.parti_is_periodic(parti):
        pass
    else:
        print("The word you gave me was not closed --- I closed it up")
        parti = parti_tools.close_parti(parti)

    parti = parti_tools.expand_parti(parti)
    parti = parti_tools.add_affixes(parti)

    return parti


''' enter a word in F_2 '''

def free_group_parti():
    attempt = False
    word = free_group.get_element_in_free()
    word = free_group.translate_free_word_to_directions(word)

    parti = []
    kette = parti_tools.word_to_kette(word)
    parti = parti_tools.kette_to_parti(kette)
    if parti_tools.parti_is_periodic(parti):
        pass
    else:
        print("Problem: The parti seems to be not closed --- I closed it up")
        parti = parti_tools.close_parti(parti)

    parti = parti_tools.add_affixes(parti)

    return parti


''' enter an element in SL_2N'''

def matrix_parti():
    attempt = False
    while not attempt:
        print('')
        print("Enter the entries of the matrix A of the press 'Q' to quit:")
        print('')
        A = [[0, 0], [0, 0]]

        A[0][0] = input('A_{1,1} = ')
        deep_tools.wanna_quit(A[0][0])
        A[1][0] = input('A_{1,2} = ')
        deep_tools.wanna_quit(A[1][0])
        A[0][1] = input('A_{2,1} = ')
        deep_tools.wanna_quit(A[0][1])
        A[1][1] = input('A_{2,2} = ')
        deep_tools.wanna_quit(A[1][1])

        if not A[0][0].isdigit() or not A[0][1].isdigit() or not A[1][0].isdigit() or not A[1][1].isdigit():
            print("Entries have to be numbers")
            attempt = False
        else:
            A[0][0] = int(A[0][0])
            A[0][1] = int(A[0][1])
            A[1][0] = int(A[1][0])
            A[1][1] = int(A[1][1])
            if A[0][0] * A[1][1] - A[1][0] * A[0][1] != 1:
                print("Determinant should be 1")
                attempt = False
            else:
                attempt = True

    word = ''
    while A[0][1] != 0:
        if A[0][0] > A[0][1]:
            A[0][0] = A[0][0] - A[0][1]
            A[1][0] = A[1][0] - A[1][1]
            word += 'L'
        if A[0][0] <= A[0][1]:
            A[0][1] = A[0][1] - A[0][0]
            A[1][1] = A[1][1] - A[1][0]
            word += 'R'
    word += 'L' * A[1][0]

    parti = []
    kette = parti_tools.word_to_kette(word)
    parti = parti_tools.kette_to_parti(kette)
    if parti_tools.parti_is_periodic(parti):
        pass
    else:
        print("The element you gave me is not the desired subgroup --- I closed it up")
        parti = parti_tools.close_parti(parti)

    parti = parti_tools.add_affixes(parti)


    return parti


def find_right_estimated(coef, length, shear, n=None):
    if n is None:
        k = 0
    else:
        k = n
    estimated = 0
    while estimated < length:
        estimated += hyper_tools.hyp_distance([0, 1], [coef[k], 1])+5*max(shear)
        k += 1
    return k


def random_parti(desired_length,shear):
    desired_length=int(desired_length)
    den = 10 ** desired_length
    num = random.randint(1, den)
    eta = [num, den]

    GAP = 10

    coef = []
    eta.reverse()
    while eta[1] > 0:
        coef.append(int(eta[0] / eta[1]))
        eta[0] = eta[0] % eta[1]
        eta.reverse()

    length = 0
    estimated_length = 0
    kette = []
    help_coef = []
    new_parti = []
    k = 0
    pos = 0
    while length < desired_length - GAP:
        #        print('Aim for ',desired_length-length)
        del new_parti
        new_parti = []
        pos = find_right_estimated(coef, desired_length - length, shear, pos)
        while k < pos:
            if k % 2 == 0:
                kette.append(['R', coef[k]])
            else:
                kette.append(['L', coef[k]])
            k += 1
        new_parti = parti_tools.kette_to_parti(kette)
        new_parti = parti_tools.close_parti(new_parti)
        new_parti = parti_tools.add_affixes(new_parti)

        new_parti = hyper_tools.hyper_parti(new_parti,shear)
        length = hyper_tools.length_hyper_parti(new_parti)

    return new_parti


def farey_parti(desired_length,shear):
    word = ''
    while len(word) < 2 * desired_length:
        new_term = random.randint(0, 1)
        if new_term == 0:
            word += 'L'
        else:
            word += 'R'

    kette = parti_tools.word_to_kette(word)
    coef = []
    for x in kette:
        coef.append(x[1])

    gap = 10

    length = 0
    estimated_length = 0
    kette = []
    help_coef = []
    new_parti = []
    k = 0
    pos = 0
    while length < desired_length - gap:
        #        print('Aim for ',desired_length-length)
        del new_parti
        new_parti = []
        pos = find_right_estimated(coef, desired_length - length, shear,pos)
        while k < pos:
            if k % 2 == 0:
                kette.append(['R', coef[k]])
            else:
                kette.append(['L', coef[k]])
            k += 1
        new_parti = parti_tools.kette_to_parti(kette)
        new_parti = parti_tools.close_parti(new_parti)
        new_parti = parti_tools.add_affixes(new_parti)

        new_parti = hyper_tools.hyper_parti(new_parti,shear)
        length = hyper_tools.length_hyper_parti(new_parti)

    return new_parti



def random_free_group_parti(desired_length,shear):
    attempt = False
    word=''
    while not attempt:
        while len(word) < 1.5*desired_length:
            new_term = random.randint(0, 3)
            if new_term == 0:
                word += 'A'
            elif new_term == 1:
                word += 'a'
            elif new_term == 2:
                word += 'B'
            else:
                word += 'b'

        maybe_admissible = free_group.check_admissible(word)
        if maybe_admissible[0]:
            attempt = True
            if maybe_admissible[1] != maybe_admissible[2]:
                word = maybe_admissible[2]
            else:
                pass
        else:
            pass

    parti = free_group.free_group_parti(word)
    parti = hyper_tools.hyper_parti(parti,shear)

    return parti



def random_simple_kette(length,shear):


    done = False
    while not done:
        #       print("trying...",end='')
        word = ''
        found = False
        while not found:
            a = random.randint(int(0.2 * length), int(0.37 * length))
            b = random.randint(int(0.2 * length), int(0.37 * length))
            if math.gcd(a, b) == 1:
                found = True
            else:
                pass

        k = 0
        x = 0
        while k < a + b:
            if x < a:
                word += 'LR'
            else:
                word += 'RL'

            x = (x + b) % (a + b)
            k += 1
        kette = parti_tools.word_to_kette(word)

        short_kette = []
        if len(kette) > 100:
            short_kette = kette[:100]
        else:
            short_kette = kette

        short_parti = parti_tools.kette_to_parti(short_kette)
        short_parti = parti_tools.close_parti(short_parti)
        short_parti = parti_tools.add_affixes(short_parti)

        short_parti = hyper_tools.hyper_parti(short_parti)
        short_length = hyper_tools.length_hyper_parti(short_parti)

        if 0.99 * length * len(short_kette) < short_length * len(kette) < 1.01 * length * len(short_kette):
            done = True
        else:
            pass

    parti = parti_tools.kette_to_parti(kette)
    parti = parti_tools.close_parti(parti)
    parti = parti_tools.add_affixes(parti)

    parti = hyper_tools.hyper_parti(parti,shear)

    return parti


