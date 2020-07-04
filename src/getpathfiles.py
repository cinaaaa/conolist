"""
 Getting all files in current path
"""
import os
from os import listdir
from os.path import isfile, join, isdir

def get_files(dir):

    # get files in directory
    files  = [f'{f}' for f in listdir(dir) if isfile(join(dir, f))]
    # get folders in directory
    folders = [f'$ {f}' for f in listdir(dir) if isdir(join(dir, f))]

    return ['..'] + folders + files