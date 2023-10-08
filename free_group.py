import deep_tools
import parti_tools


def get_element_in_free(default_word=None):
    attempt = False
    word=''
    actual_word = ''
    while not attempt:
        if default_word is None:
            input_text ="   Enter an admissible element or press 'Q' to quit:  "
        else:
            input_text ="    Enter an admissible element (default is '"+default_word+"') or press 'Q' to quit:  "
        word = input(input_text)
        deep_tools.wanna_quit(word)
        maybe_admissible = check_admissible(word,default_word)
        if maybe_admissible[0]:
            attempt = True
            word = maybe_admissible[1]
            actual_word = maybe_admissible[2]
        else:
            pass
    return [word,actual_word]


def check_admissible(word,default_word=None):
    clean = False
    while not clean:
        if len(word)<2:
            clean = True
        else:
            k=0
            while k<len(word)-1:
                clean = True
                if word[-1]+word[0] in ['Aa','aA','Bb','bB']:
                    word = word[1:-1]
                    clean = False
                    break
                elif word[k:k+2] in ['Aa','aA','Bb','bB']:
                    word=word[:k]+word[k+2:]
                    clean = False
                    break
                else:
                    pass
                k += 1
    if len(word)==0:
        if default_word is None:
            print('Tontolaba, that was the identity')
            input()
            return [False,'tontolaba','tontolaba']
        else:
            return [True,default_word,default_word]
    else:
        pass

    if 'A' in word:
        new_word = word
        return [True,word,new_word]
    elif 'a' in word:
        new_word = ''
        for x in word:
            if x == 'a':
                new_word = 'A' + new_word
            elif x == 'A':
                new_word = 'a' + new_word
            elif x == 'b':
                new_word = 'B' + new_word
            elif x == 'B':
                new_word = 'B' + new_word
            else:
                return [False,'letter different than abAB']
        return [True,word,new_word]
    else:
        return [False,'tontolaba','power_of_B']



def free_word_to_tree_path(word):   # translates a cyclically reduces an element into a sequence of edge crossings
    new_word = ''
    for x in word:
        if x == 'A':
            new_word += 'AC'
        if x == 'a':
            new_word += 'ca'
        if x == 'B':
            new_word += 'ACBa'
        if x == 'b':
            new_word += 'Abca'

    clean = False
    while not clean:
        if len(new_word)<2:
            clean = True
        else:
            k=0
            while k<len(new_word)-1:
                clean = True
                if new_word[-1]+new_word[0] in ['Aa','aA','Bb','bB','cC','Cc']:
                    new_word = new_word[1:-1]
                    clean = False
                    break
                elif new_word[k:k+2] in ['Aa','aA','Bb','bB','cC','Cc']:
                    new_word=new_word[:k]+new_word[k+2:]
                    clean = False
                    break
                else:
                    pass
                k += 1
    if len(new_word)==0:
        print('Tontolaba, that was the identity')
        exit()
    else:
        pass

    return new_word


def conjugate_tree_path(word):   #if possible, conjugates a word so that it starts with 'A'
    k = 0
    while k < len(word):
        if word[k] == 'A':
            word = word[k:]+word[0:k]
            return word
        else:
            pass
        k += 1
    print('The word was not admissible. Invert it!')
    exit()


def local_direction(word):
    if word[:2] =='AC':
        return 'L'
    elif word[:2] =='Ab':
        return 'R'
    elif word[:2] =='ac':
        return 'L'
    elif word[:2] =='aB':
        return 'R'
    elif word[:2] =='Ba':
        return 'L'
    elif word[:2] =='BC':
        return 'R'
    elif word[:2] =='bA':
        return 'L'
    elif word[:2] =='bc':
        return 'R'
    elif word[:2] =='CA':
        return 'R'
    elif word[:2] =='CB':
        return 'L'
    elif word[:2] =='ca':
        return 'R'
    elif word[:2] =='cb':
        return 'L'


def tree_path_directions(word):    # translates an admissible sequence of edge crossings into a sequence of moves L,R
    word = word + 'A'
    directions = ''
    while len(word)>1:
        directions += local_direction(word)
        word = word[1:]
    return directions


def translate_free_word_to_directions(word):
    new_word = free_word_to_tree_path(word)
    new_word = conjugate_tree_path(new_word)
    new_word = tree_path_directions(new_word)

    return new_word


def free_group_parti(word):
    word = translate_free_word_to_directions(word)

    parti = []
    kette = parti_tools.word_to_kette(word)
    parti = parti_tools.kette_to_parti(kette)
    parti = parti_tools.add_affixes(parti)

    return parti



