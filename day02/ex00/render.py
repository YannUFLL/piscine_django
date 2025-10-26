import sys
import re
import settings
import os

string = "coucou je suis un test co.cou {wesh}"

def return_file_text(arg):
    try:
        with open(arg,'r') as file:
            return (file.read())
    except FileNotFoundError: 
        print("Error: file not found")
        sys.exit(1)



if __name__ == '__main__':
    nbr_arg = len(sys.argv)
    if (nbr_arg != 2):
        print("Wrong arguments number")
        sys.exit(1)
    new_file_name, extension = os.path.splitext(sys.argv[1])
    if extension != ".template":
        print("Error: wrong file extension")
        sys.exit(1)
    file_str = return_file_text(sys.argv[1])
    new_string  = re.sub(r"{(\w+)}", lambda m: getattr(settings, m.group(1), m.group(0)), file_str)
    with open(new_file_name + ".html", 'w') as html_file:
        html_file.write(new_string)
    print(f"File '{new_file_name}.html' generated successfully.")




