'''
instances of Note should eventually have the following attributes
Note.tipo = type of geodesic it is on (Values are 'A','B','C')
Note.sign = sign of the intersection (Values are 1,-1)
Note.inst = bundled instructions to go to the next one (Values are things like ['L',5] or ['R',1])
'''

TURNS = 10

class Note:

    def __init__(self):
        self.tipo = None
        self.sign = None
        self.inst = None
        pass


def append_note(parti):  # checked
    new_note = Note()
    parti.append(new_note)

def parti_is_periodic(parti):
    virtual_tipo_sign = compute_next_tipo([parti[-1].tipo, parti[-1].sign], parti[-1].inst)
    if virtual_tipo_sign == [parti[0].tipo, parti[0].sign]:
        return True
    else:
        return False


def close_parti(parti):
    if parti[-1].inst[0] == 'L':
        virtual = compute_next_tipo([parti[-1].tipo, parti[-1].sign], parti[-1].inst)
        while virtual != [parti[0].tipo, parti[0].sign]:
            parti_tail = []
            append_note(parti_tail)
            parti_tail[0].tipo = virtual[0]
            parti_tail[0].sign = virtual[1]
            parti_tail[0].inst = ['R', 1]
            parti = join_partis(parti, parti_tail)
            del parti_tail
            virtual = compute_next_tipo([parti[-1].tipo, parti[-1].sign], parti[-1].inst)

    else:
        virtual = compute_next_tipo([parti[-1].tipo, parti[-1].sign], parti[-1].inst)
        while virtual != [parti[0].tipo, parti[0].sign]:
            parti_tail = []
            append_note(parti_tail)
            parti_tail[0].tipo = virtual[0]
            parti_tail[0].sign = virtual[1]
            parti_tail[0].inst = ['L', 1]
            parti = join_partis(parti, parti_tail)
            del parti_tail
            virtual = compute_next_tipo([parti[-1].tipo, parti[-1].sign], parti[-1].inst)

    return parti

def print_parti(parti):  # checked
    for x in parti:
        print(parti.index(x), "  tipo ", x.tipo, ", sign ", x.sign, ", inst ", x.inst)


def compute_next_tipo(signed_tipo, inst):  # checked

    go_right = [['A', 1], ['B', -1], ['C', -1], ['A', -1], ['B', 1], ['C', 1]]
    go_left = [['A', 1], ['C', 1], ['B', 1], ['A', -1], ['C', -1], ['B', -1]]

    hand = inst[0]
    clicks = inst[1]
    if hand == 'R':
        pos = go_right.index(signed_tipo)
        return go_right[(pos + clicks) % 6]
    else:
        pos = go_left.index(signed_tipo)
        return go_left[(pos + clicks) % 6]


def word_to_kette(given_word):
    kette = []
    word = ''
    word = given_word
    while len(word) > 0:
        n = ''
        if word[0] == 'L':
            if 'R' in word:
                n = word.find('R')
            else:
                n = len(word)
            kette += [['L', n]]
        else:
            if 'L' in word:
                n = word.find('L')
            else:
                n = len(word)
            kette += [['R', n]]
        word = word[n:]

    return kette


def join_ketten(kette1, kette2):  # checked
    new_kette = ''
    if kette1[-1][0] != kette2[0][0]:
        new_kette = kette1 + kette2
    else:
        k = 0
        new_kette = [0] * (len(kette1) + len(kette2) - 1)
        while k < len(kette1) - 1:
            new_kette[k] = kette1[k]
            k += 1
        k = 0
        while k < len(kette2) - 1:
            new_kette[len(kette1) + k] = [kette2[k + 1][0], kette2[k + 1][1]]
            k += 1
        new_kette[len(kette1) - 1] = [kette1[-1][0], kette1[-1][1] + kette2[0][1]]

    return new_kette


def extract_kette(parti):  # checkec
    kette = []
    for x in parti:
        kette += [x.inst]
    return kette


def kette_to_parti(kette, tipo=None, sign=None):  # checked
    parti = []
    append_note(parti)
    if tipo == None:
        parti[0].tipo = 'A'
    else:
        parti[0].tipo = tipo
    if sign == None:
        parti[0].sign = 1
    else:
        parti[0].sign = sign
    parti[0].inst = kette[0]
    k = 1
    while k < len(kette):
        append_note(parti)
        tipo_sign = compute_next_tipo([parti[k - 1].tipo, parti[k - 1].sign], kette[k - 1])
        parti[k].tipo = tipo_sign[0]
        parti[k].sign = tipo_sign[1]
        parti[k].inst = kette[k]
        k += 1

    return parti

def join_partis(parti1, parti2):  # check
    virtual_tipo_sign = compute_next_tipo([parti1[-1].tipo, parti1[-1].sign], parti1[-1].inst)
    if virtual_tipo_sign == [parti2[0].tipo, parti2[0].sign]:
        pass
    else:
        print("parties cannot be joined because their endpoints don't match")
        exit()

    tipo = ''
    tipo = parti1[0].tipo
    sign = 0
    sign = parti1[0].sign
    kette1 = []
    kette2 = []
    new_kette = []
    new_parti = []
    kette1 = extract_kette(parti1)
    kette2 = extract_kette(parti2)
    new_kette = join_ketten(kette1, kette2)
    new_parti = kette_to_parti(new_kette, tipo, sign)

    return new_parti


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
        append_note(new_parti)
        new_parti[-1].tipo = tipo
        new_parti[-1].sign = sign
        new_parti[-1].inst = [hand, 1]
        while n < parti[k].inst[1]:
            append_note(new_parti)
            [new_tipo, new_sign] = compute_next_tipo([new_parti[-2].tipo, new_parti[-2].sign], [hand, 1])
            new_parti[-1].tipo = new_tipo
            new_parti[-1].sign = new_sign
            new_parti[-1].inst = [hand, 1]
            n += 1
        k += 1
    return new_parti


def longer_parti(parti):  # checked
    if len(parti) == 1:
        print('way too short')
        exit()
    else:
        pass

    kette = []
    kette = extract_kette(parti)
    kette_long = []
    kette_long = kette
    while len(kette_long) < TURNS + 4:
        kette_long = join_ketten(kette, kette_long)

    longer_parti = kette_to_parti(kette_long)

    return longer_parti


def get_affixes(parti, pos):  # checked
    if parti_is_periodic(parti):
        pass
    else:
        print("this will make no sense because the given partiture is not periodic")
        exit()

    new_parti = []
    head = []
    tail = []
    new_parti = longer_parti(parti)
    if pos + TURNS <= len(new_parti):
        suffix = new_parti[pos:pos + TURNS]
    else:
        head = new_parti[pos:]
        tail = new_parti[:(TURNS + pos) - len(new_parti)]
        suffix = join_partis(head, tail)  # this one is ok
    if pos >= TURNS:
        prefix = new_parti[pos - TURNS:pos]
    else:
        head = new_parti[len(new_parti) + pos - TURNS - 1:]
        if pos == 0:
            prefix = head
        else:
            tail = new_parti[:pos]
            prefix = join_partis(head, tail)

    return [suffix, prefix]










