import input_tools
import random
import parti_tools

#input_tools.track_random_walk_map()

#input_tools.track_powers_of_map()


#input_tools.global_get_parti()

#input_tools.length_intersection()


longi = 100

word = ''
for k in range(longi):
    if random.randint(0, 1) == 0:
        word += 'L'
    else:
        word += 'R'

kette = parti_tools.word_to_kette(word)
parti = parti_tools.kette_to_parti(kette)
if parti_tools.parti_is_periodic(parti):
    pass
else:
    parti = parti_tools.close_parti(parti)

A = 4 * random.random() - 2
B = 4 * random.random() - 2
shear = [A, B, -A - B]


input_tools.total_minimisation(parti,shear)
