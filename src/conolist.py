from selector import pick
from getpathfiles import get_files
import os

def start():
    title = os.getcwd()
    options = get_files(os.getcwd())
    option, index = pick(options, title, indicator=">>")
    print(index)
    

if __name__ == '__main__':
    start()