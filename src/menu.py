from selector import pick
from getpathfiles import get_files
from os.path import isfile, join
from commands import exitcommand, runcommand, gotodir
import os

def menu_initilizer():
    
    # Current directory as title
    title = os.getcwd()

    # options are the files and folders in cr path
    options = get_files(os.getcwd())

    try:
        # Choosed an option now
        option, index = pick(options, title, indicator="->")

    except:
        menu_initilizer()

    # User selects a option
    if option:
        # its file or folder
        if option and index and option[0] != '@' and option != '..':
            # Get type of selected item
            if isfile(join(os.getcwd(), option.replace(' ','').replace('$',''))):
                menu_initilizer()
            else:
                gotodir(join(os.getcwd(), option.replace(' ','').replace('$','')))
                menu_initilizer()

        # its back command
        if option == '..':
            pfc = os.getcwd().split('/')
            gotodir('/'.join(pfc[:-1]))
            menu_initilizer()

        # its command
        if option == '@exit':
            exitcommand()

        if option == '@command':
            # clear console
            os.system('cls' if os.name=='nt' else 'clear')
            # Print path
            print(os.getcwd())
            # get command from user
            command = str(input('command >> '))
            # run the command
            runcommand(command)

