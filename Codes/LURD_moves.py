import os

def automation_LURD_moves(filename):
    """
    Extract the solution path for solvable boards using automation (the LURD format).
    :param filename: the name of the file containing the Sokoban game solution
    :return: list of player movements (LURD format)
    """

    # get current directory
    cwd = os.getcwd()

    #### CHANGE HERE TO THE PATH OF YOUR nuXmv BIN FOLDER ####
    os.chdir(r'C:\Users\shoham\Documents\ENG_degree\Final Project\nuXmv-2.0.0-win64\bin')
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    # variable storing the last movement in case of no change between states
    last_movement_of_player = None

    # list storing the movements of the player
    player_movements = []

    with open(filename, 'r') as file:
        for line in file:
            if 'State' in line:
                # append the last movement to the player_movements list
                if last_movement_of_player is not None:
                    player_movements.append(last_movement_of_player)
            elif 'movement =' in line:
                # extract the movement from the line and strip whitespace
                last_movement_of_player = line.split('=')[-1].strip()
            elif 'Loop starts here' in line:
                break

    # change directory back to the original directory
    os.chdir(cwd)

    # add the last movement if there is one
    if last_movement_of_player is not None:
        player_movements.append(last_movement_of_player)

    return player_movements[:-1]
