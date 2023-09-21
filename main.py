import os
import sys
import glob
import subprocess

PATH = [r"c:\temp", r"c:\windows\..."]




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
        os.chdir(directory)


def exit_cmd():
    exit(0)


def help_cmd():
    print()


def pwd():
    return input(f"{os.getcwd()}~> ")


def main():
    original_dir = os.getcwd()
    print_credits()
    run = True
    while run:
        prompt = pwd()
        if prompt.lower().__contains__("ls"):
            if prompt.lower() == "ls":
                print(ls(r"*"))
            else:
                # needs fixing
                split_data = prompt.lower().split(" ")
                os.chdir(split_data[1])
                print(ls(r"*"))
                os.chdir(original_dir)
        elif prompt.lower() == "exit":
            exit_cmd()
        elif prompt.lower().__contains__("cd"):
            if prompt.lower() == "cd":
                print(os.getcwd())
            else:
                split_data = prompt.lower().split(" ")
                cd(split_data[1])


        #if prompt.lower() in internal_dict:
        #    if prompt.lower() == "ls":
        #        print(internal_dict[prompt.lower()]("*"))
        #    else:
        #        internal_dict[prompt.lower()]()
        #if prompt.lower().__contains__(" "):
        #    splitted = prompt.lower().split(" ")
        #    if splitted[0] not in internal_dict:
        #        continue



if __name__ == "__main__":
    internal_dict = {"ls": ls, "help": help_cmd, "exit": exit_cmd}
    main()
