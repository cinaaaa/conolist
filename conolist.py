#!/usr/bin/python3

from src.menu import menu_initilizer
import os
import sys, getopt

def init():
    menu_initilizer()

def handle_args(args):
    
    if args[0] == '-h' or args[0] == '--help':
        print('''
        Thanks for using conolist.

        this is commands you can use with conolist:

            q = exit conolist and back to first path
            c = enter command in path you are
        ''')

if __name__ == '__main__':
    
    # check for args else init menu
    handle_args(sys.argv[1:]) if sys.argv[1:] else init()