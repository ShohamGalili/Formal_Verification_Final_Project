from Model_Smv import *
import time
import run_nuXmv
import re

def extract_lines_between_states(output):
    """
    Extract the lines between the states from the output of nuXmv.
    This is a generator function.
    :param output: the output of nuXmv
    :return: the lines between the states
    """
    # a list to hold the lines between the states
    lines_between_states = []
    # a flag to indicate if we are between states
    start = False

    # iterate over the lines in the output
    for line in output.split('\n'):
        # if we find the 'State' line, we are between states
        if 'State' in line:
            # if we are already between states, yield the lines between the states and reset the list
            # if not, set the flag to True because we are now between states
            if not start:
                lines_between_states = []
                start = True
            else:
                yield lines_between_states
                lines_between_states = []
        # if we are not between states, continue to the next line
        # if we are between states, add the line to the list
        elif start:
            lines_between_states.append(line)

    # if we are between states at the end of the file, yield the lines between the states
    if start:
        yield lines_between_states


def extract_goals_indexes(board):
    """
    Extract the indexes of the goals from the board.
    :param board: the board of the current Sokoban game
    :return: the indexes of the goals and the board text
    """
    goals_indexes = []  # List to store the indexes of the goals
    board_text = read_from_file(board)  # Read the board text from the file

    # Iterate through each row and column of the board
    for i, row in enumerate(board_text):
        for j, cell in enumerate(row):
            # Check if the cell contains a goal ('.'), a box on a goal ('*'), or a player on a goal ('+')
            if cell == '.' or cell == '+' or cell == '*':
                # Add the index of the goal to the list of goals_indexes
                goals_indexes.append((i, j))

    # Return the list of goals_indexes and the board text
    return goals_indexes, board_text

def positions_to_change(lines_between_states):
    """
    Extract the positions to change from the output of nuXmv.
    :param lines_between_states: the lines between the states
    :return: the positions to change
    """
    # list to hold the positions to change
    positions_to_change = []

    for line in lines_between_states:
        # if we find the 'game_board' line, we need to extract the positions to change
        if "game_board" in line:

            if "Wall" in line:
                continue
            else:
                positions_to_change.append(re.findall(r'\[([0-9]+)\]\[([0-9]+)\] = (\w+)', line))

    # return the positions to change
    return positions_to_change


def gen_board_one_goal(goals_of_iteration, board):
    """
    Create the SMV text file that will be used by the nuXmv tool.
    :param board: the board of the current Sokoban game
    :param goals_of_iteration: a list of winning conditions
    :return: the format of given input boards into SMV models
    """

    n = len(board)
    m = len(board[0])

    smv_model = f"""
    MODULE main

    -- Define the puzzle state variables
    VAR
        game_board: array 0..{n - 1} of array 0..{m - 1} of {{Wall, Player, PonGoal, Box, BonGoal, Goal, Floor}};
        movement: {{r, l, u, d}}; --direction is non-determinisic

    -- Define the initial state
    INIT
        {define_initial_states(board, n, m)}

    -- Define transition rules for moving tiles
    ASSIGN
        {define_transitions(board)}

    -- Define a function to check solvability based on the condition that all goals . convert to *
    DEFINE
        is_solvable :=
            {define_solvability_iterative(board, goals_of_iteration)}

    -- Specify properties to check solvability
    LTLSPEC !(F is_solvable);

    """
    return smv_model

def create_initial_state_iterative(board, output_file):
    """
    Create the initial state of the board after an iteration of nuXmv.
    :param board: the board of the current Sokoban game
    :param output_file: the output file from nuXmv
    :return: the updated board
    """

    # save the current directory
    cwd = os.getcwd()

    #### CHANGE HERE TO THE LOCATION OF YOUR nuXmv BIN FOLDER ####
    os.chdir(r'C:\Users\shoham\Documents\ENG_degree\Final Project\nuXmv-2.0.0-win64\bin')
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    with open(output_file, "r") as f:
        final_state = f.read()

    # Change directory back to the original directory
    os.chdir(cwd)

    # remove all lines until the first 'State' line and if there is no 'State' line, end the function
    if 'State' not in final_state:
        return -1
    else:
        output = final_state[final_state.index('State'):]

    # extract the lines between the 'states' in the smv file
    for lines in extract_lines_between_states(output):
        lines_between_states = lines
        pos_to_change = positions_to_change(lines_between_states)
        pos_to_change = [pos[0] for pos in pos_to_change]

    for position in pos_to_change:
        row, col = int(position[0]), int(position[1])

        if position[2] == 'Wall':
            board[row][col] = '#'
        elif position[2] == 'Player':
            board[row][col] = '@'
        elif position[2] == 'PonGoal':
            board[row][col] = '+'
        elif position[2] == 'Box':
            board[row][col] = '$'
        elif position[2] == 'BonGoal':
            board[row][col] = '*'
        elif position[2] == 'Goal':
            board[row][col] = '.'
        elif position[2] == 'Floor':
            board[row][col] = '-'

    return board


def tuple_to_str(tup):
    return "[" + "][".join(str(x) for x in tup) + "]"

def define_solvability_iterative(board, goals_of_iteration):
    """
    Define the solvability of the board iteratively.
    :param board: the board of the current Sokoban game
    :param goals_of_iteration: a list of winning conditions
    :return: the solvability definition
    """

    is_solvable = ''

    for goal in goals_of_iteration:
        index_goal = tuple_to_str(goal)

        # if we are in the last goal, we don't need to add the '&' operator
        if goal == goals_of_iteration[-1]:
            is_solvable += f'game_board{index_goal} = BonGoal ;\n'  # Last '.' in the board
        else:
            is_solvable += f'game_board{index_goal} = BonGoal & \n'  # Not the last '.' in the board

    return is_solvable

def solve_board_iteratively(board_to_read):
    """
    Solve the board iteratively using nuXmv.
    :param board_to_read: the board file to read
    :return: the run times of each iteration
    """

    # extract from board all the goals
    name_of_board =board_to_read.split(".")[0]
    goals, board = extract_goals_indexes(board_to_read)

    run_times_lst = []
    goals_of_iteration = []

    for i, goal in enumerate(goals):
        # pop first goal:
        goals_of_iteration.append(goal)

        # generate the SMV model for the current goals and the current board state
        smv_model = gen_board_one_goal(goals_of_iteration, board)

        # get the current path
        curr_path = os.getcwd()

        #### CHANGE HERE TO THE PATH OF YOUR nuXmv BIN FOLDER ####
        os.chdir(r'C:\Users\shoham\Documents\ENG_degree\Final Project\nuXmv-2.0.0-win64\bin')
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        with open(f"{name_of_board}_goals{goals_of_iteration}.smv", 'w') as f:
            f.write(smv_model)

        # return the path to the previous path
        os.chdir(curr_path)

        # RUN nuXmv:
        k = input("Enter k Value for BMC:")
        start_time = time.time()  # Record start time
        output_file_name = run_nuXmv.run_nuxmv(f"{name_of_board}_goals{goals_of_iteration}.smv", k=k, engine="SAT")
        end_time = time.time()  # Record end time

        # save the run time + iteration number of each iteration
        run_times_lst.append(((end_time - start_time), (i + 1)))

        # create the new initial state
        board = create_initial_state_iterative(board, output_file_name)

        if board == -1:
            print("There is no solution to this board")
            return []

    # print the total run time and the total number of iterations to solve the board:
    print(f"Total run time: {sum([t for t, _ in run_times_lst]):.3f} seconds")
    print(f"Total number of iterations: {len(run_times_lst)}")

    return run_times_lst

