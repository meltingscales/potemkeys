## Running code

    gcc -o myexecutable myfile1.c myfile2.c myfile3.c
    ./myexecutable

or

    watch "gcc myfile.c; ./a.out"

or open the `Makefile` and see what tasks can be run.

Example: Run `cd pointers; make strings2; ./strings_clobbering_null_terminators.exe`

Also, you can use VS Code, open this folder as a project, and use `CTRL-SHIFT-B` to show the tasks defined in `./.vscode/tasks.json`.