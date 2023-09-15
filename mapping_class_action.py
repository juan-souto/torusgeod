import free_group
import deep_tools

def get_mapping_class():   # gets a mapping class and writes it as a product of L's and R's
    attempt = False
    while not attempt:
        print('')
        print("Enter a mapping class as an element in SL_2N.\n"
              "Enter the entries of the matrix A of the press 'Q' to quit:")
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

    return word


def elementary_map_on_free(letter,word):
    new_word = ''
    for x in word:
        if letter == 'L':
            if x in ['A','a']:
                new_word += x
            elif x == 'B':
                new_word += 'AB'
            else:                   # if x == 'b'
                new_word += 'bA'
        else:                       # if letter == 'R':
            if x in ['B','b']:
                new_word += x
            elif x == 'A':
                new_word += 'BA'
            else:
                new_word += 'aB'
    return new_word


def mapclass_on_free(mapclass,word):
    new_word = word
    for x in mapclass:
        new_word = elementary_map_on_free(x, new_word)
    return new_word
