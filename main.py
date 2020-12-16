import os
import sys
import actionFunctions

from color import Color
from variable import Variable


def list_env():
    if os.listdir(Variable.env_path):
        max_width_name = max(len(row) for row in os.listdir(Variable.env_path)) + 1
        print(Color.BLUE + Color.BOLD + "Name" + (' ' * (
                max_width_name - 4)) + Color.DEFAULT + ' | ' + Color.BLUE + Color.BOLD + "Location" + Color.DEFAULT)
        for row in os.listdir(Variable.env_path):
            print(row + (' ' * (max_width_name - len(row))) + ' | ' + Variable.env_path + row)
    else:
        print(
            Color.BLUE + Color.BOLD + "Name" + Color.DEFAULT + ' | ' + Color.BLUE + Color.BOLD + "Location" + Color.DEFAULT)


def print_information():
    print("Information")


def env_box_process():
    if len(sys.argv) > 2:
        # Possible choices
        choices = {
            # processing option
            'list': list_env,
            'remove': actionFunctions.remove_env
        }

        # Check the first argument
        func = choices.get(sys.argv[2], 'error')

        if func == 'error':
            exit(Color.ERROR + "Invalid syntax, use --info" + Color.DEFAULT)
        elif sys.argv[2] == 'remove':
            if len(sys.argv) > 3:
                return func(sys.argv[3])
            else:
                print(Color.ERROR + "You need to specify a name." + Color.DEFAULT)
        else:
            return func()
    else:
        exit(Color.ERROR + "Invalid syntax, use --info" + Color.DEFAULT)


def check_arguments():
    if len(sys.argv) > 1:
        # Possible choices
        choices = {
            # Processing environments
            'run': actionFunctions.run_box_process,
            'build': actionFunctions.build_box_process,
            'env': env_box_process,

            # Information option
            '-i': print_information,
            '--information': print_information
        }

        # Check the first argument
        func = choices.get(sys.argv[1], 'error')

        # Error handling
        if func == 'error':
            exit(Color.ERROR + "Invalid syntax, use --info" + Color.DEFAULT)
        else:
            if sys.argv[1] == 'run' and len(sys.argv) > 2:
                return func(sys.argv[2])
            elif sys.argv[1] == 'build' and len(sys.argv) > 2:
                return func(sys.argv[2])
            elif sys.argv[1] == 'build' and len(sys.argv) < 2:
                exit(Color.ERROR + "Invalid syntax, use --info" + Color.DEFAULT)
            else:
                return func()
    else:
        print_information()
        exit(0)


def main():
    check_arguments()


if __name__ == "__main__":
    main()
