#!/usr/bin/python

"""
%(scriptName_cl)s Script Description:

The %(scriptName_cl)s module allows you to have a command list for each Python script you create.  A command list is like a command stack except a command list is static and thus only changes when you want it to change

Why is a command list useful?--

   - Shell command history can get lost, aged/expired, especially if you are switching between multiple projects.
   - You can re-execute long command lines without retyping them.
   - You can remember and re-execute a script's common invocations.
   - You can remember what you or someone else was last working on.

This %(scriptName_cl)s module has 2 modes:

   - Standalone mode:  A general command list tool by itself.
   - Embedded mode:    Can be called from inside another Python script to provide a command list for the script.


if invocation_mode == standalone:

   You can use the %(scriptName_cl)s script directly as a general command list tool by itself (standalone):

   Runstrings--

      %(scriptName_cl)s h
          Displays this help screen.

      %(scriptName_cl)s
      or
      %(scriptName_cl)s l
          Displays command list interactive loop menu.

      %(scriptName_cl)s 1..N
          Executes command list entry directly without displaying the command list.

      %(scriptName_cl)s ag runstring_with_no_enclosing_quotes
          Add command to global list.

   Note that you can alias the %(scriptName_cl)s name to make it easier to bring up:

      $ alias cl=%(scriptName_cl)s
      $ cl

You can also embed this command list functionality in another script so that this other script will have a command list.  See the embedded mode section below for details.

else:  # invocation_mode == embedded mode

   This script: %(scriptName_parent_help)s

   has a built-in command list.

   Runstrings--

      %(scriptName_parent_help)s --cl h
          Displays this help screen.

      %(scriptName_parent_help)s --cl
      or
      %(scriptName_parent_help)s --cl l
          Displays command list interactive main loop.

      %(scriptName_parent_help)s --cl 7
          Executes the #7 command list entry directly without displaying the command list main loop.

      %(scriptName_parent_help)s --cl 7 --debug 1
          Executes the #7 command list entry directly without displaying the command list main loop.  Temporarily include the extra params in the #7 command's runstring.

      %(scriptName_parent_help)s --cl ag runstring_with_no_enclosing_quotes
          Add command to global list.

   Installation:

      If you want to add this command_list feature to your Python script, put the command_list import and function call at the top of your script's main program:

         if __name__ == '__main__':
            import command_list
            command_list.command_list(sys.argv)

      Then run your script using the --cl option.

      If your script has a help screen that you want to make available in the commannd list interactive main loop (as command 's'), add this to your script:

         if __name__ == '__main__':
            import command_list
            command_list.command_list(argv=sys.argv, your_scripts_help_function=[my_scripts_usage,'return'])

      where
          my_scripts_usage is the name of your script's function that displays your script's help screen when the 's' interactive mode option is used.
          'return' is an optional flag to pass to my_scripts_usage().  In this example, after your function my_scripts_usage() displays its help screen, 'return' tells my_scripts_usage() to return when finished, not exit.  You can have another flag value 'exit'.  Since you create my_scripts_usage(), you are free to code it any way you like and have it recognize any flag values you want.

      You'll need to define your function as:

          def my_scripts_usage(param_list):
              param_list[0] is 'return'.


invocation_mode == either:

   In the command list file, you can include comments.  You can also include more than just single commands:

       # You can include comments
       ls; who; ps    # Multiple commands per entry
       ls | grep foo  # Piped commands
       vi foo         # Interactive commands

   If the command in the command list does not contain a hardcoded directory path, this script will:

       A. Attempt to find the command's file using the PATH variable.
       B. Attempt to find the command's file using the directory path used to call this command list script (Standalone mode) or the parent script (Embedded mode).


====================================================
Standalone mode global command list file = %(command_list_file_global_cl)s
Embedded mode global command list file = %(command_list_file_global)s
====================================================

The following rules are used for determining which command list file you'll use:

1. In embedded mode, the command list file name will have the same first part of its name as the name of the script it is being used in.  Example: 

   %(scriptName_parent_help)s is using this command_list module, so the name of the command_list file being used by %(scriptName_parent_help)s is:
   %(scriptName_parent_help)s_cl_file

   The command list file will be in the same directory as the %(scriptName_parent_help)s script.

2. Similar to embedded mode, in standalone mode, the command list file name will have the same first part of its name as the name of this script:

      %(scriptName_cl)s_cl_file

   The command list file will be in the same directory as the %(scriptName_cl)s script.

   This global command list file will be shared by all users on the system.

3. But each user may want their own command list file.  So if the global command list file does not exist, this script will create a command list file for each user using the user's getpass() user name in the file name:

      Embedded mode:

         %(scriptName_parent_help)s_cl_file_jsmith
         %(scriptName_parent_help)s_cl_file_tjones

         These command list files will be in the same directory as the script %(scriptName_parent_help)s .

      Standalone mode:

         %(scriptName_cl)s_cl_file_jsmith
         %(scriptName_cl)s_cl_file_tjones

         These command list files will be in the same directory as the %(scriptName_cl)s script.

4. You can override these default settings and have the script use a particular username or identifying string for you.  For example, for script %(scriptName_parent_help)s, set the following environment variable to:

       export %(cl_file_env_var)s=dev_user1
       export %(cl_file_env_var)s=project4

    or any unique value.

    A command list file will be created:

        %(scriptName_parent_help)s_cl_file_dev_user1
        %(scriptName_parent_help)s_cl_file_project4

   This command list file will be in the same directory as the script %(scriptName_parent_help)s .

   You MUST make sure your environment variable is set before you run this command list script or else it won't be able to access your custom-named command list file.

"""

import sys
import os,re
import re
import readline
import getopt

scriptDir = os.path.dirname(os.path.realpath(sys.argv[0]))
libDir = scriptDir + '/lib'

sys.path.append(scriptDir)
sys.path.append(libDir)

from   logging_wrappers import reportError, user_input
from   run_command import run_command

#==========================================

'''
cwd = os.getcwd()
scriptDir = os.path.dirname(sys.argv[0])
if scriptDir[0] != '/':
   scriptDir = cwd + '/' + scriptDir
'''

if sys.version_info[0] == 3: xrange = range

scriptName_cl = os.path.basename(__file__).replace('.pyc', '.py')

# print 175, scriptName_cl

# scriptName_parent = os.path.basename(os.path.realpath(__file__))
scriptName_parent = os.path.basename(os.path.abspath(sys.argv[0])).replace('.pyc', '.py')
# print 171, scriptName_parent
if scriptName_cl == scriptName_parent:
    scriptName_parent_help = 'xyz.py'
else:
    scriptName_parent_help = scriptName_parent

scriptName_sh = scriptName_parent.split('.')[0] + '.sh'

cl_file_env_var = scriptName_parent.split('.')[0]+"_cl_file" # bash doesn't like periods in env vars
username_env = os.getenv(cl_file_env_var)

if username_env != None:
    command_list_file_basename_cl = scriptName_cl + "_cl_file_" + username_env
else:
    command_list_file_basename_cl = scriptName_cl + "_cl_file"
command_list_file_global_cl = scriptDir + "/" + command_list_file_basename_cl

if username_env != None:
   command_list_file_basename = scriptName_parent + "_cl_file_" + username_env
   command_list_file_global = scriptDir + "/" + command_list_file_basename
   command_list_readline_history_file = scriptDir + "/" + scriptName_parent + "_history_file_" + username_env
else:
   command_list_file_basename = scriptName_parent + "_cl_file"
   command_list_file_global = scriptDir + "/" + command_list_file_basename
   command_list_readline_history_file = scriptDir + "/" + scriptName_parent + "_history_file"
   if not os.path.isfile(command_list_file_global):
      import getpass
      username_env = getpass.getuser()
      command_list_file_basename = scriptName_parent + "_cl_file_" + username_env
      command_list_file_global = scriptDir + "/" + command_list_file_basename
      command_list_readline_history_file = scriptDir + "/" + scriptName_parent + "_history_file_" + username_env


global not_set_yet
not_set_yet = 0
global standalone
standalone = 1
global embedded
embedded = 2
global invocation_mode
invocation_mode = not_set_yet


#-------------------------------------------------

from subprocess import call

#-------------------------------------------------

def is_duplicate_command(command_list=[], command_str=''):
    for index in range(len(command_list)):
        if command_str == command_list[index]['command']:
            return index
    return -1

#-------------------------------------------------

def remove_duplicate_commands(command_list):
    dupes_removed = False
    index_going_backwards = len(command_list)
    while True:
        index_going_backwards -= 1
        if index_going_backwards < 0:
            break
        index_going_forwards = is_duplicate_command(command_list=command_list, command_str=command_list[index_going_backwards]['command'])
        if index_going_forwards > -1:
            if index_going_forwards == index_going_backwards:
                continue
            else:
                del command_list[index_going_forwards]
                dupes_removed = True
    return dupes_removed, command_list

#-------------------------------------------------

def assemble_command_lists_from_files(last_command=''):
    command_list_global = []

    last_command_added = False
    count = 0
    if os.path.exists(command_list_file_global):
        with open(command_list_file_global, 'r') as fd:
            for command_str in list(fd.read().splitlines()):
                if re.search("^ *#", command_str):
                    command_list_global.append({'count': -1, 'type': 'Comment', 'filename': '', 'command': command_str})
                    continue

                # if invocation_mode == embedded:
                #     outer_script_dir = os.path.dirname(sys.argv[0])
                #     # print(210, outer_script_dir)
                #
                #     # python2 but no split for python3
                #     # import string
                #     # command_only, command_remainder = string.split(command_str.replace('  ', ' '), ' ', 1)
                #
                #     command_only, command_remainder = command_str.replace('  ', ' ').split(' ', 1)
                #
                #     # command_only, command_remainder = command_str.replace('  ', ' ').split(' ',1)
                #     # command_remainder = command_str.replace('  ', ' ').split(' ')[1:]
                #     # command_dirname = os.path.dirname(command_only)
                #     command_basename = os.path.basename(command_only)
                #     if outer_script_dir == '':
                #         command_only = command_basename
                #     else:
                #         command_only = outer_script_dir + '/' + command_basename
                #     command_str  = command_only + ' ' + command_remainder

                if "Last:" in command_str:
                    count += 1
                    if last_command == '':
                        command_list_global.append({'count': count, 'type': 'Last:', 'filename': '', 'command': command_str})
                    elif scriptName_parent not in last_command and scriptName_parent_sh not in last_command:
                        command_list_global.append({'count': count, 'type': 'Last:', 'filename': '', 'command': 'Last: ' + last_command})
                    last_command_added = True
                else:
                    index = is_duplicate_command(command_list=command_list_global, command_str=command_str)
                    if index > 0:
                        del command_list_global[index]
                    count += 1
                    command_list_global.append({'count': count, 'type': 'global', 'filename': command_list_file_global, 'command': command_str})

    if last_command != '' and scriptName_parent not in last_command and scriptName_parent_sh not in last_command and last_command_added == False:
        count += 1
        command_list_global.append({'count': count, 'type': 'Last:', 'filename': '', 'command': 'Last: ' + last_command})

    return command_list_global

#-------------------------------------------------

def add_to_command_list(new_command, command_list_global):
    # print(329, new_command)
    command_list_global.append({'count': -1, 'type': 'global', 'filename': command_list_file_global, 'command': new_command})

    # print(332, command_list_global)
    save_command_list(command_list_global)

    return command_list_global

#-------------------------------------------------

'''

This function does not work.  Can't update the user's in-memory bash history list.  User would need to run:

. cs.sh  Portfolio.py --cl 1  # Note '.' in front of cs.sh to "source" it
   cs.sh runs:
      command_list.py inside Portfolio.py # User chooses command to run
      echo user_runstring >> ~/.bash_history
      history -n ~/.bash_history

But one of the main goals of the embedded command list was to make it invisible unless the user wants to use it.


def save_command_to_bash_history(command):
   homedir = os.getenv("HOME")
   fd = open(homedir + "/.bash_history", "a")
   fd.write(command + '\n')
   fd.close()

   # bash_history_command = 'history -a "' + command + '" ~/.bash_history'
   # bash_history_command = 'history -a '
   # bash_history_command = 'history -a ~/.bash_history'
   # rc, results = run_command(bash_history_command)
   # if rc != 0:
   #    reportError("rc = " + str(rc) + ", results = " + results)
   # rc, results = run_command('set')
   # print rc, results
   # print os.getenv("HISTFILE")

   # bash_history_command = 'bash -c "history -n ~/.bash_history"'
   # bash_history_command = 'history -n ~/.bash_history'
   # bash_history_command = '. ./temp.sh'
   # os.execl('history', 'history', '-n', '~/.bash_history')
   # os.execl('. ./temp.sh', '. ./temp.sh')
   os.execl('./temp.sh', './temp.sh')
   # rc, results = run_command(bash_history_command)
   # if rc != 0:
   #    reportError("rc = " + str(rc) + ", results = " + results)
   # rc, results = run_command('set')
   # print rc, results
   # print os.getenv("HISTFILE")
'''

#-------------------------------------------------

'''
def update_last_command_in_command_list(last_command='', command_list_global=None):
   if last_command == '':
      return

   if (command_list_local != None and command_list_global == None) or (command_list_local == None and command_list_global == None):
      if command_list_local == None:
         command_list_local = []
      match = False
      for index in xrange(len(command_list_local)):
         if command_list_local[index]['type'] == 'Last:':
            command_list_local[index]['command'] = last_command
            match = True
      if match == False:
         command_list_local.append({'count': count, 'type': 'Last:', 'filename': '', 'command': 'Last: ' + last_command})
   else:
      if command_list_global == None:
         command_list_global = []
      match = False
      for index in xrange(len(command_list_global)):
         if command_list_global[index]['type'] == 'Last:':
            command_list_global[index]['command'] = last_command
            match = True
      if match == False:
         command_list_global.append({'count': -1, 'type': 'Last:', 'filename': '', 'command': 'Last: ' + last_command})

   return command_list_global, command_list_local
'''

#-------------------------------------------------

def save_command_list(command_list_global):
    # Save Last: commands including their "Last:" prefix.

    if len(command_list_global) > 0:
        dupes_removed, command_list_global = remove_duplicate_commands(command_list_global)
        fd = open(command_list_file_global, "w")
        for command in command_list_global:
            fd.write(command['command'] + '\n')
        fd.close()

    return

#-------------------------------------------------

def renumber_command_list(command_list_global):

    count = 0
    for command in command_list_global:
        if command['type'] == "Comment":
            continue

        count += 1
        command['count'] = count

    return command_list_global

#-------------------------------------------------

def show_command_list(command_list_global):

    dupes_removed, command_list_global = remove_duplicate_commands(command_list_global)

    command_list_global = renumber_command_list(command_list_global)

    if len(command_list_global) == 0:
        print("No global commands")
    else:
        for command in command_list_global:
            if command['type'] == "Comment":
                print(str(command['command']))
            else:
                print(str(command['count']) + ' ' + command['command'] + ' :' + str(command['count']))

#-------------------------------------------------

def delete_command(position, command_list_global):
    del_done = False
    if len(command_list_global) > 0:
        for index in xrange(len(command_list_global)):
            if command_list_global[index]['count'] == position:
                show_command_list(command_list_global)
                answer = user_input('Confirmation: Deleting entry ' + str(position) + '? (y/n): ')
                if answer != 'y':
                    print("Delete cancelled.")
                    break
                del command_list_global[index]
                del_done = True
                save_command_list(command_list_global)
                break

    if del_done == True:
        command_list_global = renumber_command_list(command_list_global)

    return command_list_global

#-------------------------------------------------

def move_command(source_position_int, dest_position_int, command_list_global):
    command_list_global.insert(dest_position_int+1, source_list[source_position_int])
    del (source_list[source_position_int])

    save_command_list(command_list_global)

    return command_list_global

#-------------------------------------------------

'''
Does not work!

def get_last_command_from_history():
   # results = call('bash -i -c "history -r; history"')
   rc, results = run_command('bash -i -c "history -a; history"')
   # rc, results = run_command('bash -i -c "history -r; history"')
   # rc, results = run_command('bash -i -c "history"')
   # rc, results = run_command('echo $_')
   # print "rc: ", rc, "results: ", results
   print "results: ", results
   last_command = re.sub('^  *[0-9]+ +', '', results.split('\n')[-2])
   return last_command
'''

#-------------------------------------------------

def get_command_from_list(id_num, command_list_global):
    for command in command_list_global:
        if command['count'] == id_num:
            return 0, command['command']

    msg = "id_num " + str(id_num) + " not found."
    reportError(msg)
    return 1, msg

#-------------------------------------------------

def command_list_main_loop(which_command = '', extra_params=[], last_command=''):

    if not os.path.exists(command_list_file_global):
        fd = open(command_list_file_global, "w")
        fd.close()

    try:
        readline.read_history_file(command_list_readline_history_file)
    except:
        pass

    if invocation_mode == embedded:
        last_command = ''
    # else:
        # last_command = get_last_command_from_history()
    command_list_global = assemble_command_lists_from_files(last_command=last_command)

    if which_command != '':
        which_command_source = 'runstring'
    else:
        which_command_source = 'interactive'

    while True:
        # print 482, which_command, which_command_source
        if which_command_source == 'interactive':
            which_command = user_input('Enter number, command to run, history arrow keys, or h for help: ', defaultText=defaultText)
            # last_command = readline.get_history_item(readline.get_current_history_length())

        # if which_command_source == 'runstring':
        #     which_command_source = 'interactive'  # After processing runstring command, immediately go into interactive mode.

        defaultText = ''
        if which_command == 'l':
            show_command_list(command_list_global)
            which_command_source = 'interactive'
            # if which_command_source == 'runstring':
            #    sys.exit(1)
            continue

        if which_command == '':
            continue
        if which_command == 'q':
            sys.exit(1)
        if which_command == 'h' or which_command == '?':
            print("#   = Run entry number #.  For easier reading for longer entries, entry numbers show up at the end of entries also, e.g., 3 long_entry :3")
            print("#e  = Edit and run entry #.")
            print("l   = Show the command list.")
            print("key = Use arrow keys to access this script's bash-type command stack history.")
            print("al  = Add the last command executed to the command list.")
            print("d N = Delete command N.")
            print("m N1,N2 = Move N1 command to N2 position.")
            print("e   = Edit your command list file using $EDITOR.  Manually add/delete entries as well.")
            print("h   = Show this help.")
            print("r   = Show runstring help.")
            if your_help_function != None:
                print("s   = Show your script " + scriptName_parent + " help screen.")
            print("q   = Quit.")
            print("cmd = Type in any os command (e.g., ls) or program runstring with no enclosing quotes.")
            if invocation_mode == embedded:
                print("Embedded global command list file = " + command_list_file_global)
            else:
                print("Standalone global command list file = " + command_list_file_global_cl)
            continue
        if which_command == 's':
            if your_help_function != None:
                if your_help_function_params != None:
                    your_help_function(your_help_function_params) 
                else:
                    your_help_function() 
            continue
        if which_command == 'r':
            cl_usage()
            continue
        if which_command == 'e':
            EDITOR = os.environ.get('EDITOR','vim')
            if EDITOR == '':
                EDITOR = 'vi'
            if os.path.exists(command_list_file_global):
                call([EDITOR, command_list_file_global])
            # Show refreshed list.
            command_list_global = assemble_command_lists_from_files()
            show_command_list(command_list_global)
            continue

        if re.search('^m ', which_command):
            source_position, dest_position = which_command.replace('  ', ' ').split(' ')[1].replace(' ','').split(',')
            source_position_int = int(source_position) - 1
            dest_position_int   = int(dest_position) - 1
            command_list_global = move_command(source_position_int, dest_position_int, command_list_global)
            show_command_list(command_list_global)
            continue

        if re.search('^d [0-9]+$', str(which_command)):
            position = int(which_command.replace('  ', ' ').split(' ')[1])
            command_list_global = delete_command(position, command_list_global)
            show_command_list(command_list_global)
            continue

        if re.search('^al', which_command):
            if last_command == '':
                print("No last_command available.")
                continue
            command_list_global = assemble_command_lists_from_files()
            # new_command = ' '.join(which_command.replace('  ', ' ').split(' ')[1:])
            command_list_global.append({'count': -1, 'type': 'global', 'filename': command_list_file_global, 'command': last_command})
            save_command_list(command_list_global)
            show_command_list(command_list_global)
            continue

        if re.search('^[0-9]+e$', str(which_command)):
            rc, command_from_list = get_command_from_list(int(which_command.split('e')[0]), command_list_global)
            if rc != 0:
                reportError("Error getting command from list.")
                continue
            defaultText = command_from_list
            continue

        if re.search('^[0-9]+$', str(which_command)):
            which_command_int = int(which_command)
            if which_command_int > len(command_list_global):
                reportError("Number too big = " + which_command)
                continue
            elif which_command_int <= 0:
                reportError("Number is too small = " + which_command)
                continue

            rc, command_from_list = get_command_from_list(which_command_int, command_list_global)
            if rc != 0:
                reportError("Error getting command from list.")
                continue

            command_to_run = re.sub('^Last: ', '', command_from_list)
            # print scriptName_parent, re.sub('  ', ' ', command_to_run).split(' ')
            # os.execv(scriptName_parent, re.sub('  ', ' ', command_to_run).split(' '))

        else:
            command_to_run = which_command

        if re.search("^ *#", command_to_run):   # Ignore comment lines in the command_list.
            continue

        command_before_env_var_expansion = ''

        # Works for interactive commands such as vi
        command_edited = re.sub('  ', ' ', command_to_run).split(' ')
        for index in xrange(len(extra_params)):
            command_edited.insert(index+1, extra_params[index])
        command_before_env_var_expansion = ' '.join(command_edited)
        error_flag = False
        for index in xrange(len(command_edited)):  # look for environment variables and get their values
            if re.search("^\$", command_edited[index]):
                env_var = re.sub('^\$', '', command_edited[index])
                env_var_value = os.environ.get(env_var)
                if env_var_value == None:
                    reportError("Environment variable " + command_edited[index] + " is not set for command:  " + command_to_run)
                    error_flag = True
                    break
                command_edited[index] = env_var_value

        # Command does not specify a directory path?
        get_first_command_list = command_edited
        if get_first_command_list[0] != 'cd':
            scriptDir_get_first_command = os.path.dirname(get_first_command_list[0])
            if scriptDir_get_first_command == '':  # No directory path, so...
                if not os.path.isfile(scriptDir_get_first_command):  # can we access it?  No, so...
                    get_first_command_list[0] = scriptDir + '/' + get_first_command_list[0]  # Use the scriptDir ussed to call this command_list script.
                    if os.path.isfile(get_first_command_list[0]):  # can we access it?  Yes, so...
                        command_edited = get_first_command_list
                    # else:  Let the command go through to try it as is.

        if error_flag == True:
            continue

        # print(589, command_edited)
        '''
        rc = call(command_edited)

            reportError("call() rc = " + str(rc) + ".  command_edited = " + str(command_edited))
        '''

        try:
            command_edited_string = ' '.join(command_edited)
            rc, output, error = run_command(command_edited_string)
            results = str(output) + str(error)
            if rc != 0:
                # results2 = reportError("run_command() error: Problem launching or running command or program.", mode='return_msg_only')
                for line in results.split('\n'):
                   print(line)
                   if 'run_command' in line:
                       print("    run_command() rc = " + str(rc) + ".  command_edited_string = " + str(command_edited_string))

                # print(results)

                if which_command_source == 'runstring':
                    # break
                    return 1, results
            else:
                if output != None and error != 'None':
                    print(results)

        except KeyboardInterrupt:
            print
        except Exception as e:
            # reportError("Command cannot be executed: " + str(command_edited_string) + ".  Exception e.message = " + str(e.message) + ".  e.args = " + str(e.args))
            reportError("Command cannot be executed: " + str(command_edited_string) + ".  Exception e = " + str(e))
            continue

        # command_list_global, command_list_local = update_last_command_in_command_list(command_to_run, command_list_global, command_list_local)
        # save_command_list(command_list_global)
        if command_before_env_var_expansion != '':
            if command_before_env_var_expansion != last_command:   # avoid saving duplicate last commands
                readline.add_history(command_before_env_var_expansion)
                readline.write_history_file(command_list_readline_history_file)
                last_command = command_before_env_var_expansion

        if which_command_source == 'runstring':
            break

        # save_command_to_bash_history(command_to_run)

    # reportError("Unrecognized command = " + which_command)


    # return rc, ""

#-------------------------------------------------

def command_list(argv=[], your_scripts_help_function=None):

    global invocation_mode
    global your_help_function
    global your_help_function_params

    if your_scripts_help_function == None:
        your_help_function = None
    else:
        if len(your_scripts_help_function) > 1:
            your_help_function = your_scripts_help_function[0]
            your_help_function_params = your_scripts_help_function[1:]
        else:
            your_help_function = your_scripts_help_function[0]
            your_help_function_params = None

    # How can we tell whether we are getting called in embedded mode vs. standalone mode?
    # print "realpath: ", os.path.realpath(sys.argv[0])
    # print "argv: ", sys.argv[0]
    import inspect
    # callerframerecord = inspect.list()[1]    # 0 represents this line
    # frame = callerframerecord[0]
    # info = inspect.getframeinfo(frame)
    # print "inspect:", info.filename
    # print "inspect getfile:", os.path.basename(inspect.getfile(command_list))
    # print "__main__", os.path.basename(sys.modules['__main__'].__file__)
    if os.path.basename(inspect.getfile(command_list)) == os.path.basename(sys.modules['__main__'].__file__):
        invocation_mode = standalone
    else:
        invocation_mode = embedded

    # print(743, invocation_mode)

    last_command = ''

    extra_params = []

    which_command = 'l'
    if invocation_mode == embedded:
        if len(argv) <= 1:  # User specified no params
            print()
            print("=======================================")
            print("For command list help, enter:")
            print()
            print(scriptName_parent_help + " --cl h")
            print("=======================================")
            print()
            return
        else:  # User specified some params
            if argv[1] != '--cl':  # But if the first one is not --cl, we'll ignore them and pass them on to the script we're embedded in.
                return
            if len(argv) == 2:
                which_command = 'l'  # --cl with no params
            else: 
                which_command = argv[2]
                if which_command == 'h':
                    print("=======================================")
                    print()
                    print(scriptName_parent_help + " uses the " + scriptName_cl + " feature.")
                    print()
                    print("=======================================")
                    cl_usage()
                    sys.exit(1)
                if len(argv) > 3:
                    extra_params = sys.argv[3:]
                if which_command == 'ag':
                    command_list_global = assemble_command_lists_from_files(last_command='')
                    add_to_command_list(' '.join(extra_params), command_list_global)
                    which_command = 'l'

    else:  # standalone mode
        try:
            opts, args = getopt.getopt(sys.argv[1:], "h", ["ag", "h", "help", "cl=", "cl_file="])
        except getopt.GetoptError as err:
            reportError("Unrecognized runstring " + str(err))
            cl_usage()
            return

        for opt, arg in opts:
            if opt == '--h' or opt == '--help' or opt == '-h':
                cl_usage()
                return
    
            if opt == '--cl_file':
                global command_list_file_global_cl
                command_list_file_global_cl = arg
                global command_list_file_global
                command_list_file_global = command_list_file_global_cl
            elif opt == '--cl':
                # if arg == 'last_command':
                #     last_command = argv[2]
                #     del argv[1:2]
                # elif arg == 'ag':
                #     which_command = ' '.join(argv[1:])

                if arg == 'l':
                    which_command = 'l'
                elif arg == 'h':
                    cl_usage()
                    return
                elif re.search('[0-9]+', arg):
                    which_command = arg
                else:
                    reportError("Unrecognized command = " + arg)
                    sys.exit(1)

        if len(args) > 1:
            if args[0] == 'h':
                cl_usage()
                return
            elif args[0] == 'ag':
                extra_params = []
                if len(argv) > 3:
                    extra_params = sys.argv[2:]
                command_list_global = assemble_command_lists_from_files(last_command='')
                add_to_command_list(' '.join(extra_params), command_list_global)
                which_command = 'l'
            else:
                reportError("Unrecognized command = " + args[0]) 

    command_list_main_loop(which_command, extra_params, last_command=last_command)

    sys.exit(1)


#-------------------------------------------------

def cl_usage():
    print(__doc__ % {'scriptName_cl': scriptName_cl, 'scriptName_parent_help' : scriptName_parent_help, 'command_list_file_global': command_list_file_global, 'command_list_file_global_cl': command_list_file_global_cl, 'cl_file_env_var': cl_file_env_var})


#==========================================


if __name__ == '__main__':

    command_list(sys.argv)



