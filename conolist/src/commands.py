"""
    Operators runs on user selections on items
"""
import os
import platform

def gotodir(path):

    return os.chdir(path) if path != '' else None

def exitcommand():

    return exit()

def runcommand(command):

    os.system(command) if command != '' else None