#!/usr/bin/python3
"""
    Conolist all codes here.
    i put the all code here to prevent releative imports
    error in python.
    @2020 
    Author Sina Farhadi <E-RROR>
"""
from os.path import isfile, join, isdir
import os
import platform
from os import listdir
import subprocess
import curses

KEYS_ENTER = (curses.KEY_ENTER, ord('\n'), ord('\r'))
KEYS_UP = (curses.KEY_UP, ord('k'))
KEYS_DOWN = (curses.KEY_DOWN, ord('j'))
KEYS_SELECT = (curses.KEY_RIGHT, ord(' '))
KEYS_COMMAND = (curses.KEY_COPY, 67)

COPY = None

class Picker(object):
    """The :class:`Picker <Picker>` object
    :param options: a list of options to choose from
    :param title: (optional) a title above options list
    :param multiselect: (optional) if true its possible to select multiple values by hitting SPACE, defaults to False
    :param indicator: (optional) custom the selection indicator
    :param default_index: (optional) set this if the default selected option is not the first one
    :param options_map_func: (optional) a mapping function to pass each option through before displaying
    """

    def __init__(self, options, title=None, indicator='*', default_index=0, multiselect=False, multi_select=False, min_selection_count=0, options_map_func=None):

        if len(options) == 0:
            raise ValueError('options should not be an empty list')

        self.options = options
        self.title = title
        self.indicator = indicator
        self.multiselect = multiselect or multi_select
        self.min_selection_count = min_selection_count
        self.options_map_func = options_map_func
        self.all_selected = []

        if default_index >= len(options):
            raise ValueError('default_index should be less than the length of options')

        if multiselect and min_selection_count > len(options):
            raise ValueError('min_selection_count is bigger than the available options, you will not be able to make any selection')

        if options_map_func is not None and not callable(options_map_func):
            raise ValueError('options_map_func must be a callable function')

        self.index = default_index
        self.custom_handlers = {}

    def register_custom_handler(self, key, func):
        self.custom_handlers[key] = func

    def move_up(self):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.options) - 1

    def move_down(self):
        self.index += 1
        if self.index >= len(self.options):
            self.index = 0

    def mark_index(self):
        if self.multiselect:
            if self.index in self.all_selected:
                self.all_selected.remove(self.index)
            else:
                self.all_selected.append(self.index)

    def get_selected(self):
        """return the current selected option as a tuple: (option, index)
           or as a list of tuples (in case multiselect==True)
        """
        if self.multiselect:
            return_tuples = []
            for selected in self.all_selected:
                return_tuples.append((self.options[selected], selected))
            return return_tuples
        else:
            return self.options[self.index], self.index

    def get_title_lines(self):
        if self.title:
            return self.title.split('\n') + ['']
        return []

    def get_option_lines(self):
        lines = []
        for index, option in enumerate(self.options):
            # pass the option through the options map of one was passed in
            if self.options_map_func:
                option = self.options_map_func(option)

            if index == self.index:
                prefix = self.indicator
            else:
                prefix = len(self.indicator) * ' '

            if self.multiselect and index in self.all_selected:
                format = curses.color_pair(1)
                line = ('{0} {1}'.format(prefix, option), format)
            else:
                line = '{0} {1}'.format(prefix, option)
            lines.append(line)

        return lines

    def get_lines(self):
        title_lines = self.get_title_lines()
        option_lines = self.get_option_lines()
        lines = title_lines + option_lines
        current_line = self.index + len(title_lines) + 1
        return lines, current_line

    def draw(self):
        """draw the curses ui on the screen, handle scroll if needed"""
        self.screen.clear()

        x, y = 1, 1  # start point
        max_y, max_x = self.screen.getmaxyx()
        max_rows = max_y - y  # the max rows we can draw

        lines, current_line = self.get_lines()

        # calculate how many lines we should scroll, relative to the top
        scroll_top = getattr(self, 'scroll_top', 0)
        if current_line <= scroll_top:
            scroll_top = 0
        elif current_line - scroll_top > max_rows:
            scroll_top = current_line - max_rows
        self.scroll_top = scroll_top

        lines_to_draw = lines[scroll_top:scroll_top+max_rows]

        for line in lines_to_draw:
            if type(line) is tuple:
                self.screen.addnstr(y, x, line[0], max_x-2, line[1])
            else:
                self.screen.addnstr(y, x, line, max_x-2)
            y += 1

        self.screen.refresh()

    def run_loop(self):
        while True:
            self.draw()
            c = self.screen.getch()
            if c in KEYS_UP:
                self.move_up()
            if c == 99:
                return ('@command','@command')
            if c == 113:
                return ('@exit','@exit')
            if c == 105:
                return ('@folderoption', self.get_selected())
            elif c in KEYS_DOWN:
                self.move_down()
            elif c in KEYS_ENTER:
                if self.multiselect and len(self.all_selected) < self.min_selection_count:
                    continue
                return self.get_selected()
            elif c in KEYS_SELECT and self.multiselect:
                self.mark_index()
            elif c in self.custom_handlers:
                ret = self.custom_handlers[c](self)
                if ret:
                    return ret

    def config_curses(self):
        try:
            # use the default colors of the terminal
            curses.use_default_colors()
            # hide the cursor
            curses.curs_set(0)
            # add some color for multi_select
            # @todo make colors configurable
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_WHITE)
        except:
            # Curses failed to initialize color support, eg. when TERM=vt100
            curses.initscr()

    def _start(self, screen):
        self.screen = screen
        self.config_curses()
        return self.run_loop()

    def start(self):
        return curses.wrapper(self._start)


def pick(*args, **kwargs):
    picker = Picker(*args, **kwargs)
    return picker.start()


def get_files(dir):

    # get files in directory
    files  = [f'{f}' for f in listdir(dir) if isfile(join(dir, f))]
    # get folders in directory
    folders = [f'$ {f}' for f in listdir(dir) if isdir(join(dir, f))]

    if COPY:
        filename = COPY.split('/')[len(COPY.split('/')) - 1]
        return [f'Paste {filename} here'] + ['..'] + folders + files
    else:
        return ['..'] + folders + files

def gotodir(path):

    splitted_path = path.replace(' ','').replace('$','')
    os.chdir(splitted_path) if path != '' else None

def exitcommand():

    return exit()

def runcommand(command):

    if command != '':
        os.system(f'GREPDB="{command}"; /bin/bash -c "$GREPDB"')
        get_question = str(input('Do you want to continue? [y,n] >>> '))
        
        if get_question == 'y':
            menu_initilizer()
        if get_question == 'n':
            exit()
        else:
            menu_initilizer()

def getcopy(pathname):

    global COPY

    COPY = pathname
    menu_initilizer()

def getrename(current_name):
    # clear console
    os.system('cls' if os.name=='nt' else 'clear')
    # get name of new name
    target_name = str(input(f'Rename {current_name} to >> '))
    # do rename
    os.system(f'mv {current_name} {target_name}')
    menu_initilizer()

def deletefile(filename):

    os.system(f'rm -rf {os.getcwd()}/{filename}')

def question_menu(title, options, task):

    title = title
    options = options

    try:
        # Choosed an option now
        option, index = pick(options, title, indicator="=>")

    except:
        menu_initilizer()

    # we have option
    if option:
        # index of select option in tasks
        task[index]()
        
    return menu_initilizer()


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
        if option and index and option[0] != '@' and option != '..' and 'Paste ' not in option:
            # Get type of selected item
            if isfile(join(os.getcwd(), option.replace(' ','').replace('$',''))):
                question_menu(
                    options[index].replace(' ','').replace('$',''),
                    [
                        'Delete',
                        'Copy',
                        'Rename',
                        'Go back'
                    ],
                    [
                        lambda: deletefile(options[index].replace(' ','').replace('$','')),
                        lambda: getcopy(os.getcwd()+'/'+options[index].replace(' ','').replace('$','')),
                        lambda: getrename(options[index].replace(' ','').replace('$','')),
                        menu_initilizer,
                    ]
                )
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

        # its paste
        if 'Paste ' in option:

            # Make copy global
            global COPY
            # copy file in current path
            os.system(f'cp -r {COPY} {os.getcwd()}')
            # Make copy empty
            COPY = None
            # Initial Menu again
            menu_initilizer()

        if option == '@command':
            # clear console
            os.system('cls' if os.name=='nt' else 'clear')
            # Print path
            print(os.getcwd())
            # get command from user
            command = str(input('command >> '))
            # run the command
            runcommand(command)

        # its option on folder
        if option == '@folderoption':
            
            # check select item is folder
            if isdir(join(os.getcwd(), index[0].replace(' ','').replace('$','').replace(' ','').replace('$',''))):
                folder_name = index[0].replace(' ','').replace('$','')
                question_menu(
                    f'What to do with {folder_name} ?',
                    [
                        'Delete Folder',
                        'Copy',
                        'Exit',
                    ],
                    [
                        lambda: deletefile(folder_name),
                        lambda: getcopy(os.getcwd() + '/' + folder_name.replace(' ','').replace('$','')),
                        menu_initilizer,
                    ]
                )

            # not a folder initial menu again
            else:
                menu_initilizer()


if __name__ == '__main__':
    menu_initilizer()