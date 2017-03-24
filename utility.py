import os
import multiprocessing


def cpu_count():
    try:
        NPROCS = multiprocessing.cpu_count()
    except:
        NPROCS = 1
    return NPROCS

def __lastindex(name, char = '.'):
    for i in range(1, len(name)):
        if name[-i] == char:
            return len(name) - i
    return -1

def getname(filename):
    return filename[:__lastindex(filename)]

def getextension(filename):
    return filename[__lastindex(filename):].lower()

def split_name(filename):
    # image.jpg -> 'image', '.jpg'
    i = __lastindex(filename)
    return filename[:i], filename[i:]

def isconvertible(path):
    return getextension(os.path.split(path)[1]) in ('.jpg', 'jpeg', '.png', '.webp')