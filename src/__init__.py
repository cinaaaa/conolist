from conolist import init

# use to create command line access to conolist
def execute_from_command_line():
    """
    Given the command-line arguments, figure out which subcommand is being
    run, create a parser appropriate to that command, and run it.
    """
    init()