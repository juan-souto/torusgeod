import math
import parti_tools

MobL = [[1, 0], [1, 1]]
MobR = [[1, 1], [0, 1]]
MobLInv = [[1, 0], [-1, 1]]
MobRInv = [[1, -1], [0, 1]]

# eta attracting fixed point
# bareta is repelling fixed point


''' This gives the shear mob for every edge'''


def read_shear(tipo, shear, direction):  # checked
    if tipo == 'A':
        if direction:
            mob = [[math.exp(shear[0] / 2), 0], [0, math.exp(-shear[0] / 2)]]
        else:
            mob = [[math.exp(-shear[0] / 2), 0], [0, math.exp(shear[0] / 2)]]
    elif tipo == 'B':
        if direction:
            mob = [[math.exp(shear[1] / 2), 0], [0, math.exp(-shear[1] / 2)]]
        else:
            mob = [[math.exp(-shear[1] / 2), 0], [0, math.exp(shear[1] / 2)]]
    else:
        if direction:
            mob = [[math.exp(shear[2] / 2), 0], [0, math.exp(-shear[2] / 2)]]
        else:
            mob = [[math.exp(-shear[2] / 2), 0], [0, math.exp(shear[2] / 2)]]
    return mob


''' 
The next functions deal with elements in SL_2R as linear maps. The point is to be able to 
 compute the trace and hence the length in a different way.
 '''


def mob_linear(mob, given_point):   # checked
    new0 = mob[0][0]*given_point[0]+mob[1][0]*given_point[1]
    new1 = mob[0][1]*given_point[0]+mob[1][1]*given_point[1]

    return [new0, new1]


def mob_parti_linear(parti, point, shear=None):  # checked
    new_parti = parti_tools.expand_parti(parti)
    if shear is None:
        shear = [0,0,0]
    else:
        pass

    new_point = point

    k = 0
    while k < len(new_parti):
        pos = len(new_parti) - k -1
        inst = new_parti[pos].inst
        if inst[0] == 'L':
            new_point=mob_linear(MobL, new_point)
        else:
            new_point=mob_linear(MobR, new_point)
        mob = read_shear(new_parti[pos].tipo,shear,True)
        new_point = mob_linear(mob,new_point)
        k += 1

    return new_point


def computed_translation_length(parti,shear): # checked
    new_parti = parti_tools.expand_parti(parti)

    a = mob_parti_linear(new_parti, [1,0], shear)[0]
    b = mob_parti_linear(new_parti, [0,1], shear)[1]
    trace = a+b
    if trace == 2:
        return 0
    else:
        return 2*math.acosh(trace/2)


'''
The following functions deal with elements in SL_2R from with the hyperbolic point of view
'''

def mob_hyp(given_mob, given_point):  # checked
    a = given_mob[0][0]
    b = given_mob[1][0]
    c = given_mob[0][1]
    d = given_mob[1][1]
    x = given_point[0]
    y = given_point[1]
    new_point = [1, 1]

    den = (c * x + d) ** 2 + (c * y) ** 2
    new_point[0] = (((a * x + b) * (c * x + d)) + a * c * (y ** 2)) / den
    new_point[1] = y * (a * d - b * c) / den

    return new_point


def mob_parti_hyp(parti, point, direction, shear=None):  # checked
    #######################################
    # PARTI IS BEING EXPANDED
    #######################################
    new_parti = parti_tools.expand_parti(parti)
    if shear is None:
        shear = [0, 0, 0]

    k = 0
    if direction:
        while k < len(new_parti):
            pos = len(new_parti) - (k + 1)
            inst = new_parti[pos].inst
            if inst[0] == 'L':
                point = mob_hyp(MobL, point)
            else:
                point = mob_hyp(MobR, point)
            point = mob_hyp(read_shear(new_parti[pos].tipo, shear, True), point)
            k += 1
    else:
        while k < len(new_parti):
            pos = k
            point = mob_hyp(read_shear(new_parti[pos].tipo, shear, False), point)
            inst = new_parti[pos].inst
            if inst[0] == 'L':
                point = mob_hyp(MobLInv, point)
            else:
                point = mob_hyp(MobRInv, point)
            k += 1

    return point


def compute_fixed_points(parti, direction, shear=None):  # checked
    ##############################
    # parti does not need to have been expanded
    ##############################
    if shear is None:
        shear = [0, 0, 0]
    if direction:
        fixed_point = mob_parti_hyp(parti, [0, 1], True, shear)
    else:
        fixed_point = mob_parti_hyp(parti, [0, 1], False, shear)

    return fixed_point


''' compute the point where the vertical axis meets the geodesic joining the attracting point of suffix
and the repelling point of prefix'''


def compute_point(given_suffix, given_prefix, shear=None):  # checked
    ##############################
    # given_suffix and given_prefix do not need to have been expanded
    ##############################
    if shear is None:
        shear = [0, 0, 0]
    eta = compute_fixed_points(given_suffix, True, shear)[0]
    bareta = compute_fixed_points(given_prefix, False, shear)[0]

    center = (eta + bareta) / 2
    radius = (eta - bareta) / 2

    point = [0, math.sqrt(radius ** 2 - center ** 2)]

    return point


def pull_point(parti, pos, point,shear=None):  # checked
    ##############################
    # done so that the underlying parti did not need to be expanded
    ##############################

    if shear is None:
        shear = [0, 0, 0]

    mini_parti = parti_tools.expand_parti([parti[pos]])
    new_point = mob_parti_hyp(mini_parti,point,False,shear)

    return new_point


def hyp_distance(x, y):  # checked
    dist = math.acosh(1 + ((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2) / (2 * x[1] * y[1]))
    return dist



def hyper_parti(parti, shear=None):  # checked
    ###########################################
    # parti does not need to be expanded
    ###########################################
    if shear is None:
        shear = [0, 0, 0]
    else:
        pass
    if parti_tools.parti_is_periodic(parti):
        pass
    else:
        print('parti is not periodic')
        exit()

    for k in range(len(parti)):
#        [suffix, prefix] = parti_tools.get_affixes(parti, k)
        parti[k].point = compute_point(parti[k].suffix, parti[k].prefix, shear)

    for k in range(len(parti)):
        parti[k].length = hyp_distance(pull_point(parti,k, parti[k].point, shear), parti[(k + 1) % len(parti)].point)

    return parti


def length_hyper_parti(parti):  # checked
    length = 0
    for x in parti:
        length += x.length

    return length



#
# Still to be done
#

def calculate_angle(parti, pos, shear=None):
    pass


def highest_point(parti, pos, shear=None):
    pass






def time_in_cusp(parti, pos, height, shear=None):
    pass
