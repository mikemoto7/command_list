# command_list
Add a command list to any Python script.

The command_list.py module allows you to have a command list for each Python script you create.  A command list is like a command stack except a command list is static and thus only changes when you want it to change

Why is a command list useful?--

   - Shell command history can get lost, aged/expired, especially if you are switching between multiple projects.
   - You can re-execute long command lines without retyping them.
   - You can remember and re-execute a script's common invocations.
   - You can remember what you or someone else was last working on.

This command_list.py module has 2 modes:

   - Standalone mode:  A general command list tool by itself.
   - Embedded mode:    Can be called from inside another Python script to provide a command list for the script.


