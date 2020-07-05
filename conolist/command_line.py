#!/usr/bin/env python3
import conolist

# use to create command line access to conolist
def execute_from_command_line():
    """
    Given the command-line arguments, figure out which subcommand is being
    run, create a parser appropriate to that command, and run it.
    """
    conolist.menu_initilizer()