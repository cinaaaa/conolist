from selector import pick
from getpathfiles import get_files
from os.path import isfile, join
import os

def cono_menu():
    
    title = os.getcwd()
    options = get_files(os.getcwd())
    option, index = pick(options, title, indicator="->")

    print(option)
    # User selects a option
    # if option:
    #     # Get type of selected item
    #     if isfile(join(os.getcwd(), option.replace(' ','').replace('#','').replace('#',''))):
    #         print('file')
    #     else:
    #         print('folder')

    #     print(option)

    # cono_menu()