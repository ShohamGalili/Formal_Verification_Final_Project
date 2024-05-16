import run_nuXmv
from Model_Smv import *
import time
from LURD_moves import automation_LURD_moves
from solve_iteratively import solve_board_iteratively
import scapy
def main(is_iterative=False):
    ##### CHANGE HERE TO THE FULL BOARD PATH #####
    board_file = "board10.txt"
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    if not is_iterative:
        # Generate the board from the file
        board_file_name = gen_board(board_file)

        #### CHANGE HERE TO THE NAME OF THE ENGINE YOU WANT TO USE ####
        engine = "SAT"
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        # If the engine is SAT, prompt the user to enter k value for BMC
        if engine == 'SAT':
            k = input("Enter k Value for BMC:")
        else:
            k = None

        # Record start time of running the model
        start_time = time.time()
        # Run nuXmv with specified parameters and get the output file name
        output_file_name = run_nuXmv.run_nuxmv(board_file_name, k, engine)
        # Record end time
        end_time = time.time()

        # Calculate running time and print it
        total_time = end_time - start_time
        print(f"Running time for {engine} engine on {board_file} is:", total_time, "seconds\n")

        # Extract the LURD moves from the output sokoban file
        player_movements = automation_LURD_moves(r'C:\Users\shoham\Documents\ENG_degree\Final Project\nuXmv-2.0.0-win64\bin\sokoban_model.out')

        # If there's no path to winning, print a message:
        if len(player_movements) == 0 and engine == 'SAT':
            print(f"************ There is no path to win for {board_file} at this k value! ************")
        elif len(player_movements) == 0 and engine == 'BDD':
            print(f"************ There is no path to win - the {board_file} is not solvable! ************")
        # If there are player movements, print the path for winning:
        else:
            print("************ The Path for Win is: ************")
            for move in player_movements:
                print(move)
            print('Win :)')

    # if iterative running
    else:
        # Solve the Sokoban game iteratively
        run_times = solve_board_iteratively(board_file)
        for run_time, iteration in run_times:
            print(f"Time to run iteration {iteration} is: {run_time:.3f} seconds")

if __name__ == '__main__':
    #### CHANGE HERE TO True TO RUN THE ITERATIVE SOLVING OR False IF REGULAR SOLVING IS REQUESTED ####
    main(False)
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

