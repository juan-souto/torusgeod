import parti_tools
from parti_tools import Note

'''
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%     CALCULATING SELF-INTERSECTION NUMBER     %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Most of the work is to calculate "long intersections", meaning those corresponding to lifts which fellow-travel
through at least a whole fundamental domain.
'''


def expand_parti(parti):  # checked
    new_parti = []
    k = 0
    pos = 0
    while k < len(parti):
        n = 1
        tipo = ''
        tipo = parti[k].tipo
        sign = 0
        sign = parti[k].sign
        hand = ''
        hand = parti[k].inst[0]
        parti_tools.append_note(new_parti)
        new_parti[-1].tipo = tipo
        new_parti[-1].sign = sign
        new_parti[-1].inst = [hand, 1]
        while n < parti[k].inst[1]:
            parti_tools.append_note(new_parti)
            [new_tipo, new_sign] = parti_tools.compute_next_tipo([new_parti[-2].tipo, new_parti[-2].sign], [hand, 1])
            new_parti[-1].tipo = new_tipo
            new_parti[-1].sign = new_sign
            new_parti[-1].inst = [hand, 1]
            n += 1
        k += 1
    return new_parti


def is_first_in_common(parti1, parti2, k, n):  # checked
    if parti1[k].tipo != parti2[n].tipo:
        return False
    else:
        pass

    s = parti1[k].sign * parti2[n].sign
    if parti1[(k - 1) % len(parti1)].tipo != parti2[(n - s) % len(parti2)].tipo:
        return True
    else:
        return False


''' assuming that parti1[k] and parti2[n] have the same type, this detects in which direction does parti2 
    branch away from parti1 when running with party1 orientation's'''


def forward_branching(parti1, parti2, k, n):
    s = parti1[k].sign * parti2[n].sign
    step = 0
    while parti1[(k + step) % len(parti1)].tipo == parti2[(n + s * step) % len(parti2)].tipo:
        step += 1
    if s == 1:
        return parti2[(n + step - 1) % len(parti2)].inst[0]
    else:
        if parti2[(n - (step - 1) - 1) % len(parti2)].inst[0] == 'R':
            return 'L'
        else:
            return 'R'


''' decides if parti1[k] and parti2[n] are an intersection point or not'''


def is_intersection_point(parti1, parti2, k, n):
    if is_first_in_common(parti1, parti2, k, n):
        #        print('part1 in at k: ', parti1[(k - 1) % len(parti1)].inst[0])

        if parti1[(k - 1) % len(parti1)].inst[0] == forward_branching(parti1, parti2, k, n):
            return True
        else:
            return False
    else:
        return False


''' calculate the intersection number between two partitures'''


def compute_intersection_number(parti1, parti2):
    new_parti1 = []
    new_parti2 = []
    new_parti1 = expand_parti(parti1)
    new_parti2 = expand_parti(parti2)

    intersection = 0
    for k in range(len(new_parti1)):
        for n in range(len(new_parti2)):
            if is_intersection_point(new_parti1, new_parti2, k, n):
                intersection += 1
            else:
                pass
            n += 1
        k += 1

    return intersection


''' things to be added here '''

def parti_homology(parti):
    new_parti = expand_parti(parti)
    inter_a = 0
    inter_b = 0
    inter_c = 0

    for x in new_parti:
        if x.tipo == 'A':
            inter_a += x.sign
        elif x.tipo == 'B':
            inter_b += x.sign
        elif x.tipo == 'C':
            inter_c += x.sign
        else:
            print('La bomba')

    return [inter_a,inter_b,inter_c]

