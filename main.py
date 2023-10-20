import os
import glob
import subprocess
import platform
import re
import time


internal_lst = ["dir", "cd", "cls", "help", "mkdir", "rename", "exit", "set"]
original_dir = os.getcwd()
ENVIRONMENT_VALUES = []


def setup_enviroment_vars():
    """
    Objective: declare a gloal variables that will store all of the environment variables.
    Parameters: Nothing.
    Returns: Nothing.
    """
    
    global ENVIRONMENT_VALUES
    # get all Windows environment variables
    for key, value in  os.environ.items():
        ENVIRONMENT_VALUES.append(f"{key}={value}")
    # our own environment variables
    ENVIRONMENT_VALUES.append("CMDNEO_VERSION=V7.10")
    ENVIRONMENT_VALUES.append("CODE_NAME=TYRANUS")
    ENVIRONMENT_VALUES.append("MEGA_NEO=TRUE")
    ENVIRONMENT_VALUES.append("INGANEU=ORLOGIN1")

    ENVIRONMENT_VALUES.sort(key=str.casefold)


def print_credits():
    """
    Objective: print fancy credits.
    Parameters: Nothing.
    Returns: Nothing.
    """
    
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


def dir_neo(parameter: str=""):
    if parameter == "":
        parameter = os.getcwd()
        
    parameter = parameter.lstrip().rstrip()
    
    if not parameter.lower().startswith("c:\\"):
        parameter = f"{os.getcwd()}\{parameter}"
    
    if os.path.isdir(parameter):
        path = parameter
        pattern = "*"
    else:
        parameter_lst = parameter.rsplit("\\", 1)
        path = parameter_lst[0]
        pattern = parameter_lst[1]

    os.chdir(path)
    in_dir_lst = glob.glob(pattern)
    
    for item in in_dir_lst:
        full_name = os.path.join(path,item)
        if os.path.isfile(full_name):
            print("%s\t\t%s \t%s" %(time.ctime(os.path.getmtime(full_name)), str(os.path.getsize(full_name)), item))
        else:
            print("%s\t<Dir>\t\t%s" %(time.ctime(os.path.getmtime(full_name)), item))


def remove_suffix_until_flag(word, flag):
    """
    Objective: remove all chars from the end of the string until the flag is met.
    Parameters: word (str), flag (string).
    Returns: string of all files and sub-directories matching a pattern in cwd.
    """
    
    new_word = []
    last_slash_pos = word.rindex(flag)
    for i in range(0, last_slash_pos):
        new_word.append(word[i])
    return "".join(new_word)


def cd_neo(directory=""):
    """
    Objective: change cwd to the requested directory (if exists).
    Parameters: directory (str).
    Returns: Nothing.
    """
    
    global original_dir

    if directory == "":
        print(original_dir)
        return
    
    try:
        directory = directory.lstrip().rstrip()
        
        
        if directory == "..":
            os.chdir(remove_suffix_until_flag(os.getcwd(), "\\"))
        else:
            try:
                os.chdir(directory)
            except OSError:
                print("Invalid Path!")
    except IndexError:
        print("Invalid Command!")
    finally:
        original_dir = os.getcwd()


def filter_lst(lst, filt):
    """
    Objective: change cwd to the requested directory (if exists).
    Parameters: lst (list), filt (string).
    Returns: string with all environment variables seperated by new lines.
    """
    
    temp_lst = []

    for i in range(0, len(lst)):
        if lst[i].lower().startswith(filt):
            temp_lst.append(lst[i])
    return "\n".join(temp_lst)


def set_neo(filt=""):
    """
    OBJECTIVE: The set_cmd function manages environment variables by either
        displaying all environment variables, adding new ones, or filtering them based on user input.

    PARAMETERS: filt (str): A string parameter representing the user's command or request related to environment variables.
                    It can be empty (for displaying all variables), contain an equal sign (for adding a new variable), 
                    or serve as a filter string (for filtering variables).

    RETURNS: If filt is empty: Returns a string containing all environment variables joined with line breaks ("\n").
                If filt contains an equal sign: Returns a message indicating successful variable addition.
                If filt is neither empty nor contains an equal sign: Returns a filtered list of environment variables as a string.
    """
    
    
    global ENVIRONMENT_VALUES
    try:
        # Print the output of the 'set' command
        filt = filt.lstrip().rstrip()
        if filt == "":
            print("\n".join(ENVIRONMENT_VALUES))
        elif filt.__contains__("="):
            ENVIRONMENT_VALUES.append(filt)
            ENVIRONMENT_VALUES.sort(key=str.casefold)
            print("Added variable to environment")
        else:
            print(filter_lst(ENVIRONMENT_VALUES, filt))

    except Exception as e:
        print("An error occurred:", str(e))


def cls_neo():
    """
    Objective: clears the entire terminal.
    Parameters: Nothing.
    Returns: Nothing.
    """
    
    if platform.system().lower() == 'windows':
        os.system('cls')
    else:
        os.system('clear')


def exit_neo():
    """
    Objective: terminate the program.
    Parameters: Nothing.
    Returns: Nothing.
    """
    
    exit(0)


def help_neo(help):
    """
    Objective: print help texts for supported internal command.
    Parameters: help (str): specify specific helps.
    Returns: Nothing.
    """
    
    if help == "help1":
        print(r'''For more information on a specific command, type HELP command-name
        
            CD             Displays the name of or changes the current directory.
            CLS            Clears the screen.
            EXIT           Quits the CMD.EXE program (command interpreter).
            HELP           Provides Help information for Windows/ Shell NEO commands.
            DIR             Displays a list of files and subdirectories in a directory.
            MKDIR          Creates a directory.
            RENAME         Renames a file or files.
            SET            Displays, sets, or removes Windows/ Shell NEO environment variables.

        ''')
    elif help == "cd":
        print(r'''Displays the name of or changes the current directory.

    CHDIR [/D] [drive:][path]
    CHDIR [..]
    CD [/D] [drive:][path]
    CD [..]
    
    ..   Specifies that you want to change to the parent directory.

    Type CD drive: to display the current directory in the specified drive.
    Type CD without parameters to display the current drive and directory.

    Use the /D switch to change current drive in addition to changing current
    directory for a drive.

    If Command Extensions are enabled CHDIR changes as follows:

    The current directory string is converted to use the same case as
    the on disk names.  So CD C:\TEMP would actually set the current
    directory to C:\Temp if that is the case on disk.

    CHDIR command does not treat spaces as delimiters, so it is possible to
    CD into a subdirectory name that contains a space without surrounding
    the name with quotes.  For example:

    cd \winnt\profiles\\username\programs\start menu

    is the same as:

    cd "\winnt\profiles\\username\programs\start menu"

    which is what you would have to type if extensions were disabled.
    ''')

    elif help == "cls":
        print("Clears the screen.")
    elif help == "exit":
        print(r'''Quits the CMD.EXE program (command interpreter) or the current batch script.

                EXIT [/B] [exitCode]

                /B          specifies to exit the current batch script instead of
                            CMD.EXE.  If executed from outside a batch script, 
                            it will quit CMD.EXE

                exitCode    specifies a numeric number.  if /B is specified, sets
                            ERRORLEVEL that number.  If quitting CMD.EXE, sets the process
                             exit code with that number.''')
    elif help == "help":
        print(r'''Provides help information for Windows commands.

                HELP [command]

                command - displays help information on that command.''')
    elif help == "dir":
        print(r'''Displays a list of files and subdirectories in a directory.

                DIR [drive:][path][filename] [/A[[:]attributes]] [/B] [/C] [/D] [/L] [/N]
                [/O[[:]sortorder]] [/P] [/Q] [/R] [/S] [/T[[:]timefield]] [/W] [/X] [/4]

                [drive:][path][filename]
                specifies drive, directory, and/or files to list.

                /A          Displays files with specified attributes.
                attributes   D  Directories                R  Read-only files
                             H  Hidden files               A  Files ready for archiving
                             S  System files               I  Not content indexed files
                             L  Reparse Points             O  Offline files
                             -  Prefix meaning not
                /B          Uses bare format (no heading information or summary).
                /C          Display the thousand separator in file sizes.  This is the
                            default.  Use /-C to disable display of separator.
                /D          Same as wide but files are list sorted by column.
                /L          Uses lowercase.
                /N          New long list format where filenames are on the far right.
                /O          List by files in sorted order.
                            sortorder    N  By name (alphabetic)       S  By size (smallest first)
                                         E  By extension (alphabetic)  D  By date/time (oldest first)
                                         G  Group directories first    -  Prefix to reverse order
                /P          Pauses after each screenful of information.
                /Q          Display the owner of the file.
                /R          Display alternate data streams of the file.
                /S          Displays files in specified directory and all subdirectories.
                /T          Controls which time field displayed or used for sorting
                            timefield   C  Creation
                            A  Last Access
                            W  Last Written
                /W          Uses wide list format.
                /X          This displays the short names generated for non-8dot3 file
                            names.  The format is that of /N with the short name inserted
                            before the long name. If no short name is present, blanks are
                            displayed in its place.
                /4          Displays four-digit years

                Switches may be preset in the DIRCMD environment variable.  Override
                preset switches by prefixing any switch with - (hyphen)--for example, /-W.''')
    elif help == "mkdir":
        print(r'''Creates a directory.

                MKDIR [drive:]path
                MD [drive:]path

                If Command Extensions are enabled MKDIR changes as follows:

                MKDIR creates any intermediate directories in the path, if needed.
                For example, assume \a does not exist then:

                mkdir \a\b\c\d

                is the same as:

                mkdir \a
                chdir \a
                mkdir b
                chdir b
                mkdir c
                chdir c
                mkdir d

                which is what you would have to type if extensions were disabled.''')
    elif help == "rename":
        print(r'''Renames a file or files.

                RENAME [drive:][path]filename1 filename2.
                REN [drive:][path]filename1 filename2.

                Note that you cannot specify a new drive or path for your destination file.''')
    elif help == "set":
        print(r'''Displays, sets, or removes cmd.exe environment variables.

SET [variable=[string]]

  variable  Specifies the environment-variable name.
  string    Specifies a series of characters to assign to the variable.

Type SET without parameters to display the current environment variables.

If Command Extensions are enabled SET changes as follows:

SET command invoked with just a variable name, no equal sign or value
will display the value of all variables whose prefix matches the name
given to the SET command.  For example:

    SET P

would display all variables that begin with the letter 'P'

SET command will set the ERRORLEVEL to 1 if the variable name is not
found in the current environment.

SET command will not allow an equal sign to be part of the name of
a variable.

Two new switches have been added to the SET command:

    SET /A expression
    SET /P variable=[promptString]

The /A switch specifies that the string to the right of the equal sign
is a numerical expression that is evaluated.  The expression evaluator
is pretty simple and supports the following operations, in decreasing
order of precedence:

    ()                  - grouping
    ! ~ -               - unary operators
    * / %               - arithmetic operators
    + -                 - arithmetic operators
    << >>               - logical shift
    &                   - bitwise and
    ^                   - bitwise exclusive or
    |                   - bitwise or
    = *= /= %= += -=    - assignment
      &= ^= |= <<= >>=
    ,                   - expression separator

If you use any of the logical or modulus operators, you will need to
enclose the expression string in quotes.  Any non-numeric strings in the
expression are treated as environment variable names whose values are
converted to numbers before using them.  If an environment variable name
is specified but is not defined in the current environment, then a value
of zero is used.  This allows you to do arithmetic with environment
variable values without having to type all those % signs to get their
values.  If SET /A is executed from the command line outside of a
command script, then it displays the final value of the expression.  The
assignment operator requires an environment variable name to the left of
the assignment operator.  Numeric values are decimal numbers, unless
prefixed by 0x for hexadecimal numbers, and 0 for octal numbers.
So 0x12 is the same as 18 is the same as 022. Please note that the octal
notation can be confusing: 08 and 09 are not valid numbers because 8 and
9 are not valid octal digits.

The /P switch allows you to set the value of a variable to a line of input
entered by the user.  Displays the specified promptString before reading
the line of input.  The promptString can be empty.

Environment variable substitution has been enhanced as follows:

    %PATH:str1=str2%

would expand the PATH environment variable, substituting each occurrence
of "str1" in the expanded result with "str2".  "str2" can be the empty
string to effectively delete all occurrences of "str1" from the expanded
output.  "str1" can begin with an asterisk, in which case it will match
everything from the beginning of the expanded output to the first
occurrence of the remaining portion of str1.

May also specify substrings for an expansion.

    %PATH:~10,5%

would expand the PATH environment variable, and then use only the 5
characters that begin at the 11th (offset 10) character of the expanded
result.  If the length is not specified, then it defaults to the
remainder of the variable value.  If either number (offset or length) is
negative, then the number used is the length of the environment variable
value added to the offset or length specified.

    %PATH:~-10%

would extract the last 10 characters of the PATH variable.

    %PATH:~0,-2%

would extract all but the last 2 characters of the PATH variable.

Finally, support for delayed environment variable expansion has been
added.  This support is always disabled by default, but may be
enabled/disabled via the /V command line switch to CMD.EXE.  See CMD /?

Delayed environment variable expansion is useful for getting around
the limitations of the current expansion which happens when a line
of text is read, not when it is executed.  The following example
demonstrates the problem with immediate variable expansion:

    set VAR=before
    if "%VAR%" == "before" (
        set VAR=after
        if "%VAR%" == "after" @echo If you see this, it worked
    )

would never display the message, since the %VAR% in BOTH IF statements
is substituted when the first IF statement is read, since it logically
includes the body of the IF, which is a compound statement.  So the
IF inside the compound statement is really comparing "before" with
"after" which will never be equal.  Similarly, the following example
will not work as expected:

    set LIST=
    for %i in (*) do set LIST=%LIST% %i
    echo %LIST%

in that it will NOT build up a list of files in the current directory,
but instead will just set the LIST variable to the last file found.
Again, this is because the %LIST% is expanded just once when the
FOR statement is read, and at that time the LIST variable is empty.
So the actual FOR loop we are executing is:

    for %i in (*) do set LIST= %i

which just keeps setting LIST to the last file found.

Delayed environment variable expansion allows you to use a different
character (the exclamation mark) to expand environment variables at
execution time.  If delayed variable expansion is enabled, the above
examples could be written as follows to work as intended:

    set VAR=before
    if "%VAR%" == "before" (
        set VAR=after
        if "!VAR!" == "after" @echo If you see this, it worked
    )

    set LIST=
    for %i in (*) do set LIST=!LIST! %i
    echo %LIST%

If Command Extensions are enabled, then there are several dynamic
environment variables that can be expanded but which don't show up in
the list of variables displayed by SET.  These variable values are
computed dynamically each time the value of the variable is expanded.
If the user explicitly defines a variable with one of these names, then
that definition will override the dynamic one described below:

%CD% - expands to the current directory string.

%DATE% - expands to current date using same format as DATE command.

%TIME% - expands to current time using same format as TIME command.

%RANDOM% - expands to a random decimal number between 0 and 32767.

%ERRORLEVEL% - expands to the current ERRORLEVEL value

%CMDEXTVERSION% - expands to the current Command Processor Extensions
    version number.

%CMDCMDLINE% - expands to the original command line that invoked the
    Command Processor.

%HIGHESTNUMANODENUMBER% - expands to the highest NUMA node number
    on this machine.''')
    else:
        print("commend not active")


def pwd():
    """
    Objective: print cwd and collect data from user.
    Parameters: Nothing.
    Returns: Nothing.
    """
    
    return input(f"{os.getcwd()}~> ")


def mkdir_neo(path_and_name):
    """  
    OBJECTIVE: This function, 'mkdir', is designed to create a directory based on the provided 'path_and_name' argument
    or check if the directory already exists. It aims to handle directory creation and validation.
    
    PARAMETERS:
    - path_and_name (str): A string representing a directory path and name. It can be either a directory name or a full path.
                            If it's a directory name, the function assumes the current working directory.
                            If it's a full path, the function uses that path for directory operations.
                            
    RETURNS: Nothing.
    """
    
    path = None
    parts = path_and_name.split()

    for part in parts:
        # If only one part is found, treat it as the directory name and use the default path
        if not '\\' in part:
            directory_name = part
            path = os.getcwd()  # Get the current working directory as the default
            # Check if the directory already exists
            full_path = os.path.join(path, directory_name)
        else:
            path = part
            full_path = part
            directory_name = part.rsplit("\\", 1)[1]

        try:
            if not os.path.exists(full_path):
                # Create the directory
                os.mkdir(full_path)
                print(f"Directory '{directory_name}' created successfully at '{full_path}'.")
            else:
                print(f"Directory '{directory_name}' already exists at '{full_path}'.")
        except OSError:
            print("Directory path wasn't found!")
            pass


def clean_filename(filename):
    """
    Objective: remove special characters from the filename
    Parameters: filename (str).
    Returns: pure filename.
    """
    
    cleaned_name = re.sub(r'', '', filename)
    return cleaned_name


def rename_neo(inp):
    """
        OBJECTIVE: This function gets a file path and name and new name and rename the file.

        PARAMETERS:
            command (str): The shell command to execute.
            input_filename (str): The path of the file, the name of the current file, the name that the user wants to change to.

        RETURNS: nothing.
    """
    
    # Split the input string into a list of strings
    inputs = inp.split(" ")

    # Check if the first input is an absolute path (starts with 'c:\')
    if inputs[0].lower().startswith("c:\\"):
        original_file_path = inputs[0]
    else:
        # If not an absolute path, assume it's a file in the current working directory
        original_file_path = f"{os.getcwd()}\{inputs[0]}"

    # Split the original file path into parts using backslashes
    path = original_file_path.split("\\")
    file_path = path[0]

    # Reconstruct the file path up to the parent directory (excluding the file name)
    for i in path[1:-1]:
        file_path += "\\" + i

    # Create the full path for the old and new file names
    old_names = file_path + "\\" + path[-1]
    new_names = file_path + "\\" + inputs[1]

    old_path = clean_filename(old_names.strip())
    new_path = clean_filename(new_names.strip())

    try:
        # Attempt to rename the old file to the new file name
        os.rename(old_path, new_path)
        print(f"Renamed '{old_path}' to '{new_path}' successfully.")
    except OSError as e:
        print(f"Error renaming '{old_path}': {e}")


def execute_python_file(script_name):
    """ 
        OBJECTIVE: This function executes a Python script specified by 'script_name' using the 'python' command.

        PARAMETERS:
        - script_name (str): The name of the Python script file to be executed.

        RETURNS: nothing.
    """
    
    try:
        # Run the Python script using subprocess
        subprocess.run(['python', script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")


def execute_external(command):
    """ 
        OBJECTIVE: This function executes an external shell command specified in 'command' and captures its output and error messages.

        PARAMETERS:
	        - command (str): The shell command to execute along with its parameters, provided as a single string.

        RETURNS: nothing. 
     """
     
    try:
        # user input will be turned to list that will be run by the subprocess
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Check if the command was successful (exit code 0)
        if result.returncode == 0:
            print("Command output:")
            print(result.stdout)
        else:
            print("Command failed:")
            print(result.stderr)
    except Exception as e:
        print(f"'{command}' is not recognized as an internal or external command, operable program or batch file.")


def redirect_output_to_file(command, output_filename):
    """ 
    OBJECTIVE: This function redirects output from specified shell command to a file.

    PARAMETERS:
        - command (str): The shell command to execute.
        - output_filename (str): The name of the output file from which output will be redirected to from the command.

    RETURNS: nothing.
    """
    
    try:
        with open(output_filename, "w+") as output_file:
            subprocess.run(command, shell=True, stdout=output_file)
    except Exception as e:
        print(f"Error: {e}")


def redirect_input_from_file(command, input_filename):
    """ 
        OBJECTIVE: This function redirects input from a file to a specified shell command.

        PARAMETERS:
            - command (str): The shell command to execute.
            - input_filename (str): The name of the input file from which input will be redirected to the command.

        RETURNS: nothing.
    """
    
    try:
        with open(input_filename, "r") as input_file:
            subprocess.run(command, shell=True, stdin=input_file)
    except Exception as e:
        print(f"Error: {e}")
        

def pipe_commands(command1: str, command2: str):
    """
        OBJECTIVE: This function pipes the output of 'command1' into 'command2' and returns the result as a decoded string.

        PARAMETERS:
            - command1 (str): The first shell command to execute.
            - command2 (str): The second shell command to execute, with 'command1' as its input.

        RETURNS: The decoded output of 'command2' after piping 'command1' into it. If an error occurs, it prints an error message.
    """
    
    
    #try:
    #    process1 = subprocess.Popen(command1, stdout=subprocess.PIPE, shell=True)
    #    process2 = subprocess.Popen(command2, stdin=process1.stdout, stdout=subprocess.PIPE, shell=True)
    #    process1.stdout.close()  # Close the output of the first command to prevent deadlocks
    #    output = process2.communicate()[0]
    #    return output.decode("utf-8")
    #except Exception as e:
    #    print(f"Error: {e}")
    command_param1 = command1.split()
    command_param2 = command2.split()
    
    comm1 = command_param1[0]
    params1 = " ".join(command_param1[1:])
    
    
    comm2 = command_param2[0]
    params2 = " ".join(command_param2[1:])
    
    
    try:
        if comm1 in internal_lst:
            if params1 != "":
                process1 = subprocess.Popen(['python', '-c', f'import main; main.{comm1}_neo("{params1}")'], stdout=subprocess.PIPE)
            else:
                process1 = subprocess.Popen(['python', '-c', f'import main; main.{comm1}_neo()'], stdout=subprocess.PIPE)
        else:
            process1 = subprocess.Popen(command1, stdout=subprocess.PIPE, shell=True)
            
            
        if comm2 in internal_lst:
            if params2 != "":
                process2 = subprocess.Popen(['python', '-c', f'import main; main.{comm2}_neo("{params2}")'], stdin=process1.stdout, stdout=subprocess.PIPE)
            else:
                process2 = subprocess.Popen(['python', '-c', f'import main; main.{comm2}_neo()'], stdin=process1.stdout, stdout=subprocess.PIPE)
        else:
            process2 = subprocess.Popen(command2, stdin=process1.stdout, stdout=subprocess.PIPE, shell=True)
            
            
        process1.stdout.close()  # Close the output of the first command to prevent deadlocks
        output = process2.communicate()[0]
        
        return output.decode("utf-8")
    except Exception as e:
        print(f"Error: {e}")


def redirect_input_output(prompt):
    """ 
        OBJECTIVE: This function redirects input from a file to a specified shell command, then the output will be redirected to another file.

        PARAMETERS:
            - prompt (str): the inserted user input.

        RETURNS: nothing.
    """
    
    # Command with both input and output redirection
    parts = prompt.split("<")
    command_and_input = parts[0].strip()
    output_file = parts[1].split(">")[1].strip()
    input_file = parts[1].split(">")[0].strip()

    # Read input from the input file
    try:
        with open(input_file, "r") as input_file:
            input_data = input_file.read()
        
        # Execute the command with input data and redirect output to the output file
        with open(output_file, "w+") as output_file:
            process = subprocess.Popen(command_and_input, shell=True, stdout=output_file, stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True)
            process.communicate(input=input_data)

        print("Command executed with input and output redirection.")
    except FileNotFoundError:
        print(f"Input file '{input_file}' not found.")


def main():
    global original_dir
    print_credits()
    run = True
    while run:
        prompt = pwd()
        prompt = prompt.lower().lstrip().rstrip()
        
        if ">" in prompt or "<" in prompt or "|" in prompt:
            redirections = []
            commands = []
            
            if not (str(prompt[0])).isalpha() or not (str(prompt[-1])).isalpha():
                print("Invalid syntax")
                continue
            
            # Define a regular expression pattern with capturing groups
            pattern = r"([^<|>]+)|([<|>])"

            # Use re.findall to find all matches
            matches = re.findall(pattern, prompt)

            # Extract and print the matched substrings
            for match in matches:
                matched_string = match[0]
                if matched_string:
                    commands.append(matched_string.rstrip().lstrip()) 
                
                
            # Define a regular expression pattern with capturing groups
            pattern = r"([<|>])"

            # Use re.findall to find all matches
            matches = re.findall(pattern, prompt)

            # Extract and print the matched substrings
            for match in matches:
                matched_string = match[0]
                if matched_string:
                    redirections.append(matched_string.rstrip().lstrip())
            
            if redirections[0] == "|":
                print(pipe_commands(commands[0], commands[1]))
            
            #for i in range(len(redirections)):
            #    run_process(commands[i], redirections[i], commands[i+1]) 
            
            #
            #thread_lst = []
            #
            #for i in range(len(commands)):
            #    thread_lst.append(threading.Thread(target=run_process, args=(commands[i],)))
        
            
        elif prompt.endswith(".py"):
            if prompt.removesuffix(".py") == "":
                continue
            execute_python_file(prompt)                
            
        # works with spaces
        elif prompt.startswith("dir"):
            try:
                if prompt == "dir":
                    dir_neo("")
                else:
                    parameters = prompt[4:]
                    dir_neo(parameters)
            except OSError:
                print("Invalid Syntax!")
            finally:
                os.chdir(original_dir)
        # works with spaces
        elif prompt.startswith("exit"):
            exit_neo()
        # works with spaces
        elif prompt.startswith("cd"):
            if prompt == "cd":
                cd_neo()
            else:
                parameters = prompt[3:]
                cd_neo(parameters)
                #try:
                #    cd_neo(parameters)
                #    original_dir = os.getcwd()
                #except IndexError:
                #    print("Invalid Command!")
        # works with spaces
        elif prompt.startswith("set"):
            if prompt == "set":
                set_neo()
            else:
                parameters = prompt[4:]
                set_neo(parameters)
        # works with spaces 
        elif prompt.startswith("cls"):
            cls_neo()
        # works with spaces, but function is unfinished!
        elif prompt.startswith("help"):
            if prompt == "help":
                help_neo("help1")
            else:
                comment_to_help = prompt[5:]
                help_neo(comment_to_help)
                pass
        elif prompt.startswith("mkdir"):
            if prompt == "mkdir":
                print("The syntax of the command is incorrect.")
            elif prompt[5] != " ":
                print("Invalid Syntax!")
            else:
                parameters = prompt[6:].lstrip().rstrip()
                mkdir_neo(prompt[6:])
        elif prompt.startswith("rename"):
            if prompt.startswith("rename"):
                inp = prompt[7:]
                rename_neo(inp)
        
        elif prompt.endswith(".py"):
            if prompt.removesuffix(".py") == "":
                continue
            execute_python_file(prompt)
        
        # if input is only whitespaces or nothing
        elif prompt == "":
            continue
        
        else:
            execute_external(prompt)

if __name__ == "__main__":
    setup_enviroment_vars()
    main()
