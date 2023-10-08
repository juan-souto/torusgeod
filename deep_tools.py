import math
import os

def wanna_quit(x):
    if x in ['q', 'Q']:
        exit()
    else:
        pass


def limpia():
    if (os.name == 'posix'):
        os.system('clear')
    else:
        os.system('cls')


def add_vector(x,y):
    if len(x) != len(y):
        print('It makes no sense to add this')
        exit()
    else:
        suma = [0]*len(x)
        for k in range(len(x)):
            suma[k] = x[k] + y[k]
    return suma


def subtract_vector(x,y):
    if len(x) != len(y):
        print('It makes no sense to subtract this')
        exit()
    else:
        suma = [0]*len(x)
        for k in range(len(x)):
            suma[k] = x[k] - y[k]
    return suma

def dot_product(x,y):
    if len(x) != len(y):
        print('It makes no sense to take this dot product')
        exit()
    else:
        suma = 0
        for k in range(len(x)):
            suma += x[k] * y[k]
    return suma


def scalar_prod(t,x):
    y = [0]*len(x)
    for k in range(len(x)):
        y[k] = t* x[k]
    return y

def norm(x):
    return math.sqrt(dot_product(x,x))




def isDigit(x):
    try:
        float(x)
        return True
    except ValueError:
        return False


def project_to_simplex(x):
    suma = 0
    for k in range(len(x)):
        suma += x[k]
    y = [0]*len(x)
    for k in range(len(x)):
        y[k] = x[k] - suma/len(x)
    return y


def get_binary(k):
    done = False
    result =[]
    while not done:
        result.append(k%2)
        if k == 0:
            done = True
        else:
            k = int(k/2)
    return result[:-1]
