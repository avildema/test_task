# Instruction

## test 1

Detect local mounted disk (make sure it is local) with at least X MB free space, create Z files of size Y, run Z “dd” processes which where each process will fill the selected file with Data and print time took to complete the work.

* How to use:
 ```bash
 python3.exe test.py -p /x -X 100 -Z 4 -Y 3
 ```

## test 2

Run user-selected command on many servers (user provided as param) with ssh in parallel, collect output from all nodes. Script should print collected output from all nodes on stdout, w/o using temp files.

* How to use:
 ```bash
python.exe C:/GIT/test_task/test.py -p . -X 100 -Z 4 -Y 3
 ```
 