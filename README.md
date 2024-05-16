# Formal Verification Final Project

This repository contains the code for the final project of our Formal Verification course. The project is divided into four parts, each with its own set of codes. Below are the instructions to ensure that each part runs appropriately:

## Part 2

### Files:
1. Model_smv.py
2. LURD_moves.py
3. run_nuXmv.py
4. Main.py

### Instructions:
1. **Model_smv.py**:
   - In the `gen_board()` function, at line 446, change the path saved in the variable `model_file_path` to your nuXmv bin repository path. This change is necessary for saving the smv model in a runnable path. Use an r string.

2. **LURD_moves.py**:
   - In line 14, in the `os.chdir()` command, change the path to your nuXmv bin repository path so that the code can read the .out file to extract the LRUD moves. Use an r string.

3. **run_nuXmv.py**:
   - In line 20, put your bin repository path in the `os.chdir()` command. Use an r string.

4. **Main.py**:
   - Change the following:
     - Line 9: Change the `board_file` variable to the FULL XSB BOARD PATH. The board should be saved in XSB format and as a .txt file.
     - Line 17: Should remain with the value "SAT" if a bmc type run is requested. If a run without a bounded number of steps is requested, change the value to None.
     - Line 61: The input to the `Main()` function should be False.

## Part 3

### Files:
1. Model_smv.py
2. LURD_moves.py
3. run_nuXmv.py
4. Main.py

### Instructions:
1. **Model_smv.py**:
   - In the `gen_board()` function, at line 446, change the path saved in the variable `model_file_path` to your nuXmv bin repository path. Use an r string.

2. **LURD_moves.py**:
   - In line 14, in the `os.chdir()` command, change the path to your nuXmv bin repository path. Use an r string.

3. **run_nuXmv.py**:
   - In line 20, put your bin repository path in the `os.chdir()` command. Use an r string.

4. **Main.py**:
   - Change the following:
     - Line 9: Change the `board_file` variable to the FULL XSB BOARD PATH. The board should be saved in XSB format and as a .txt file.
     - Line 17: Change to "BDD" if running with BDD engine is requested, or "SAT" if running with SAT engine is requested. Using the value None would result in running the model in the SAT engine without a bounded number of steps (k will equal None as well).
     - Line 61: The input to the `Main()` function should be False.

## Part 4

### Files:
1. Model_smv.py
2. LURD_moves.py
3. run_nuXmv.py
4. Main.py
5. solve_iteratively.py

### Instructions:
1. **Model_smv.py**:
   - In the `gen_board()` function, at line 446, change the path saved in the variable `model_file_path` to your nuXmv bin repository path. Use an r string.

2. **LURD_moves.py**:
   - In line 14, in the `os.chdir()` command, change the path to your nuXmv bin repository path. Use an r string.

3. **run_nuXmv.py**:
   - In line 20, put your bin repository path in the `os.chdir()` command. Use an r string.

4. **Main.py**:
   - Change the following:
     - Line 9: Change the `board_file` variable to the FULL XSB BOARD PATH. The board should be saved in XSB format and as a .txt file.
     - Line 17: Should remain with the value "SAT" if a bmc type run is requested. If a run without a bounded number of steps is requested, change the value to None.
     - Line 61: The input to the `Main()` function should be True.

5. **solve_iteratively.py**:
   - In lines 223 and 132, change the input of the `os.chdir()` command to your nuXmv bin repository path. Use an r string.

**Note:** All codes should be run only from the `Main.py` file in all parts.
For all parts, all of the places that need to be changed are marked in the code with comment blocks of the form:
# #### ______ #### #
line needed to be changed
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
