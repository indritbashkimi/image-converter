import os
from settings import supported_files


import multiprocessing


def cpu_count():
    try:
        NPROCS = multiprocessing.cpu_count()
    except:
        NPROCS = 1
    return NPROCS


def getbase(path):
    ''' /home/indrit/image.jpg -> /home/indrit/ '''
    return os.path.split(path)[0]


def filename(path):
    ''' /home/indrit/image.jpg -> image.jpg '''
    return os.path.split(path)[1]


def getroot(path):
    ''' /home/indrit/image.jpg -> /home/indrit/image '''
    return os.path.splitext(path)[0]


def getext(path):
    ''' /home/indrit/image.jpg -> .jpg '''
    return os.path.splitext(path)[1]


def getname(path):
    ''' /home/indrit/image.jpg -> image '''
    return os.path.splitext(filename(path))[0]


def isconvertible(uri):
    return getext(uri) in supported_files
