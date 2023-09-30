import os
import sys
import glob
import subprocess
import platform
import argparse
import re

#PATH = [r"c:\temp", r"c:\windows\..."]
#
#ENVIRONMENT_VALUES = subprocess.run("set", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,
#                                    text=True).stdout.splitlines()

def setup_enviroment_vars():
    global ENVIRONMENT_VALUES
    ENVIRONMENT_VALUES = []
    for key, value in  os.environ.items():
        ENVIRONMENT_VALUES.append(f"{key}={value}")
    ENVIRONMENT_VALUES.append("CMDNEO_VERSION=V7.10")
    ENVIRONMENT_VALUES.sort(key=str.casefold)


def print_credits():
    print(r'''  ____  _          _ _   _   _ _____ ___                                             
 / ___|| |__   ___| | | | \ | | ____/ _ \                                            
 \___ \| '_ \ / _ \ | | |  \| |  _|| | | |                                           
  ___) | | | |  __/ | | | |\  | |__| |_| |                                           
 |____/|_| |_|\___|_|_| |_| \_|_____\___/                      _   _                 
  _ __  _ __ ___   __ _ _ __ __ _ _ __ ___  _ __ ___   ___  __| | | |__  _   _ _     
 | '_ \| '__/ _ \ / _` | '__/ _` | '_ ` _ \| '_ ` _ \ / _ \/ _` | | '_ \| | | (_)    
 | |_) | | | (_) | (_| | | | (_| | | | | | | | | | | |  __/ (_| | | |_) | |_| |_     
 | .__/|_|  \___/ \__, |_|  \__,_|_| |_| |_|_| |_| |_|\___|\__,_| |_.__/ \__, (_)    
 |_|              |___/                                                  |___/       
  ___    _               ____             _    _                                     
 |_ _|__| | __ _ _ __   | __ )  __ _ _ __| | _(_)_ __                                
  | |/ _` |/ _` | '_ \  |  _ \ / _` | '__| |/ / | '_ \                               
  | | (_| | (_| | | | | | |_) | (_| | |  |   <| | | | |                              
 |___\__,_|\__,_|_| |_| |____/ \__,_|_|  |_|\_\_|_| |_|                              
   ___                        ____  _                                      _ _       
  / _ \ _ __ ___   ___ _ __  / ___|| |__  _ __ ___   __ _ _   _  _____   _(_) |_ ____
 | | | | '_ ` _ \ / _ \ '__| \___ \| '_ \| '_ ` _ \ / _` | | | |/ _ \ \ / / | __|_  /
 | |_| | | | | | |  __/ |     ___) | | | | | | | | | (_| | |_| | (_) \ V /| | |_ / / 
  \___/|_| |_| |_|\___|_|    |____/|_| |_|_| |_| |_|\__,_|\__, |\___/ \_/ |_|\__/___|
  __  __       _                 ___                 _ _  |___/                      
 |  \/  | __ _| |_ __ _ _ __    / _ \__   ____ _  __| (_) __ _                       
 | |\/| |/ _` | __/ _` | '_ \  | | | \ \ / / _` |/ _` | |/ _` |                      
 | |  | | (_| | || (_| | | | | | |_| |\ V / (_| | (_| | | (_| |                      
 |_|  |_|\__,_|\__\__,_|_| |_|  \___/  \_/ \__,_|\__,_|_|\__,_|  ''')
    for i in range(3):
        print("\n")


def ls(pattern):
    try:
        res = glob.glob(pattern)
    except TypeError:
        res = []
    return '\n'.join(res)


def remove_suffix_until_char(word, char_flag):
    new_word = []
    last_slash_pos = word.rindex(char_flag)
    for i in range(0, last_slash_pos):
        new_word.append(word[i])
    return "".join(new_word)


def cd(directory):
    if directory == "..":
        os.chdir(remove_suffix_until_char(os.getcwd(), "\\"))
    else:
        try:
            os.chdir(directory)
        except OSError:
            print("Invalid Path!")


def filter_lst(lst, filt):
    temp_lst = []

    for i in range(0, len(lst)):
        if lst[i].lower().startswith(filt):
            temp_lst.append(lst[i])
    return "\n".join(temp_lst)


# def set_cmd(filt):
#    command = 'set'
#
#    try:
#        # Run the 'set' command and capture the output
#        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
#
#        # Check if the command was successful
#        if result.returncode == 0:
#            # Print the output of the 'set' command
#            if filt == "":
#                return result.stdout
#            elif filt.__contains__("="):
#                result.stdout.splitlines().append(filt.strip())
#                return ""
#            else:
#                return filter_big_str(result.stdout.splitlines(), filt)
#        else:
#            # Print any error messages
#            print("Error:", result.stderr)
#
#    except Exception as e:
#        print("An error occurred:", str(e))

def set_cmd(filt):
    global ENVIRONMENT_VALUES
    try:
        # Print the output of the 'set' command
        if filt == "":
            return "\n".join(ENVIRONMENT_VALUES)
        elif filt.__contains__("="):
            #ENVIRONMENT_VALUES.append(filt.strip())
            ENVIRONMENT_VALUES.append(filt)
            ENVIRONMENT_VALUES.sort(key=str.casefold)
            return "Added variable to environment"
        else:
            return filter_lst(ENVIRONMENT_VALUES, filt)

    except Exception as e:
        print("An error occurred:", str(e))


def cls():
    if platform.system().lower() == 'windows':
        os.system('cls')
    else:
        os.system('clear')


def exit_cmd():
    exit(0)


def help_cmd():
    print('''For more information on a specific command, type HELP command-name
          
          CD             Displays the name of or changes the current directory.
          CLS            Clears the screen.
          DIR            Displays a list of files and subdirectories in a directory.
          EXIT           Quits the CMD.EXE program (command interpreter).
          SET            Displays, sets, or removes Windows environment variables.
          
          ''')


def pwd():
    return input(f"{os.getcwd()}~> ")


def mkdir(path_and_name):
    path = None
    parts = path_and_name.rsplit(' ', 1)
    
    # If only one part is found, treat it as the directory name and use the default path
    if len(parts) == 1:
        directory_name = parts[0]
        path = os.getcwd()  # Get the current working directory as the default
    else:
        path = parts[0]
        directory_name = parts[1]
    
    # Check if the directory already exists
    full_path = os.path.join(path, directory_name)
    if not os.path.exists(full_path):
        # Create the directory
        os.mkdir(full_path)
        print(f"Directory '{directory_name}' created successfully at '{full_path}'.")
    else:
        return (f"Directory '{directory_name}' already exists at '{full_path}'.")


def clean_filename(filename):
    # Remove special characters from the filename
    cleaned_name = re.sub(r'', '', filename)
    return cleaned_name


def rename_files():
    old_names = input("Enter old file paths (comma-separated): ").split(",")
    new_names = input("Enter new file paths (comma-separated): ").split(",")

    if len(old_names) != len(new_names):
        print("Error: Number of old paths must match the number of new paths.")
    else:
        for old_path, new_path in zip(old_names, new_names):
            old_path = clean_filename(old_path.strip())
            new_path = clean_filename(new_path.strip())

            try:
                os.rename(old_path, new_path)
                print(f"Renamed '{old_path}' to '{new_path}' successfully.")
            except OSError as e:
                print(f"Error renaming '{old_path}': {e}")


def execute_python_file(script_name):
    try:
        # Run the Python script using subprocess
        subprocess.run(['python', script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")


def execute_external(command):
    try:
        command_and_param = command.split()
        if command_and_param[0] == command:
            result = subprocess.run([command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        else:
            command, param = command_and_param[0], command_and_param[1]
            result = subprocess.run([command, param], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Check if the command was successful (exit code 0)
        if result.returncode == 0:
            print("Command output:")
            print(result.stdout)
        else:
            print("Command failed:")
            print(result.stderr)
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    original_dir = os.getcwd()
    print_credits()
    run = True
    while run:
        prompt = pwd()
        prompt = prompt.lower().lstrip().rstrip()
        
        if prompt.endswith(".py"):
            if prompt.removesuffix(".py") == "":
                continue
            execute_python_file(prompt)                
            
        # works with spaces
        elif prompt.startswith("ls"):
            try:
                if prompt == "ls":
                    print(ls(r"*"))
                else:
                    parameters = prompt[3:]
                    os.chdir(parameters.lstrip())
                    print(ls(r"*"))
                    os.chdir(original_dir)
            except OSError:
                print("Invalid Syntax!")
        # works with spaces
        elif prompt.startswith("exit"):
            exit_cmd()
        # works with spaces
        elif prompt.startswith("cd"):
            if prompt == "cd":
                print(os.getcwd())
            else:
                parameters = prompt[3:].lstrip()
                try:
                    cd(parameters)
                except IndexError:
                    print("Invalid Command!")
        # works with spaces
        elif prompt.startswith("set"):
            if prompt == "set":
                print(set_cmd(""))
            else:
                #split_data = prompt.lower().split(" ")
                #print(set_cmd(split_data[1]))
                parameters = prompt[4:].lstrip()
                print(set_cmd(parameters))
        # works with spaces
        elif prompt.startswith("cls"):
            cls()
        # works with spaces, but function is unfinished!
        elif prompt.startswith("help"):
            if prompt == "help":
                help_cmd()
            else:
                # support for spesific helps
                pass
        elif prompt.startswith("mkdir"):
            if prompt == "mkdir":
                print("The syntax of the command is incorrect.")
            elif prompt[5] != " ":
                print("Invalid Syntax!")
            else:
                parameters = prompt[6:].lstrip().rstrip()
                mkdir(prompt[6:])
        
        else:
            execute_external(prompt)
            pass

        # if prompt.lower() in internal_dict:
        #    if prompt.lower() == "ls":
        #        print(internal_dict[prompt.lower()]("*"))
        #    else:
        #        internal_dict[prompt.lower()]()
        # if prompt.lower().__contains__(" "):
        #    splitted = prompt.lower().split(" ")
        #    if splitted[0] not in internal_dict:
        #        continue


if __name__ == "__main__":
    internal_dict = {"ls": ls, "help": help_cmd, "exit": exit_cmd, "mkdir": mkdir}
    setup_enviroment_vars()
    main()
