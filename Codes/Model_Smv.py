import os

def create_smv_model (board):
    """
    Create an SMV text file to be used with the nuXmv tool.
    :param board: the board of the current Sokoban game
    :return: the SMV model as a string
    """

    n = len(board)
    m = len(board[0])

    smv_model = f"""
MODULE main

-- Define the puzzle state variables
VAR
    game_board: array 0..{n-1} of array 0..{m-1} of {{Wall, Player, PonGoal, Box, BonGoal, Goal, Floor}};
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
        {define_solvability(board)}
        
-- Specify properties to check solvability
LTLSPEC !(F is_solvable);

"""

    return smv_model

def write_to_file(path, smv_model):
    """
    Write SMV model to a file.
    :param path: the path to write the SMV model file
    :param smv_model: the SMV model as a string
    """
    smv_model_file = open(path, "w")
    smv_model_file.write(smv_model)
    smv_model_file.close()


def read_from_file(path):
    """
    Read board from an SMV model file.
    :param path: the path to the SMV model file
    :return: the board as a 2D list
    """
    with open(path, "r") as smv_model_file:
        # Read each line from the file, convert it to a list of characters, and remove the '\n' character
        board = [list(line.strip()) for line in smv_model_file if line.strip()]

        # Iterate through each list (row) in the board
    for lst in board:
        # Iterate through each element (character) in the list
        for i in range(len(lst)):
            # Check if the character is not a valid Sokoban character
            if lst[i] not in ['#', '@', '$', '.', '+', '*', '-']:
                # Create a new list that contains only the correct characters
                new_lst = []
                for char in lst:
                    if char in ['#', '@', '$', '.', '+', '*', '-']:
                        new_lst.append(char)
                # Replace the old list with the new list
                board.insert(board.index(lst), new_lst)
                # Remove the old list
                board.remove(lst)
                break

    return board

def define_initial_states(board, n, m):
    """
    Define the string of the initial states of the current board.
    :param board: the board of the current Sokoban game
    :param n: number of rows of the board
    :param m: number of columns of the board
    :return: the initial state as a string
    """
    str_initial = ''

    for r in range(n):
        for c in range(m):
            if r == n - 1 and c == m - 1:
                # Convert XSB symbols to char format in SMV model
                if board[r][c] == '@': #warehouse keeper
                    str_initial += f'game_board[{r}][{c}] = Player;\n'
                    str_initial += '\t'

                elif board[r][c] == '+': #warehouse keeper on goal
                    str_initial += f'game_board[{r}][{c}] = PonGoal;\n'
                    str_initial += '\t'

                elif board[r][c] == '$': #box
                    str_initial += f'game_board[{r}][{c}] = Box;\n'
                    str_initial += '\t'

                elif board[r][c] == '*': #box on goal
                    str_initial += f'game_board[{r}][{c}] = BonGoal;\n'
                    str_initial += '\t'

                elif board[r][c] == '#': #wall
                    str_initial += f'game_board[{r}][{c}] = Wall;\n'
                    str_initial += '\t'

                elif board[r][c] == '.': #goal
                    str_initial += f'game_board[{r}][{c}] = Goal;\n'
                    str_initial += '\t'

                elif board[r][c] == '-': #floor
                    str_initial += f'game_board[{r}][{c}] = Floor;\n'
                    str_initial += '\t'
            else:
                # Convert XSB symbols to char format in SMV model
                if board[r][c] == '@':  # warehouse keeper
                    str_initial += f'game_board[{r}][{c}] = Player &\n'
                    str_initial += '\t'

                elif board[r][c] == '+':  # warehouse keeper on goal
                    str_initial += f'game_board[{r}][{c}] = PonGoal &\n'
                    str_initial += '\t'

                elif board[r][c] == '$':  # box
                    str_initial += f'game_board[{r}][{c}] = Box &\n'
                    str_initial += '\t'

                elif board[r][c] == '*':  # box on goal
                    str_initial += f'game_board[{r}][{c}] = BonGoal &\n'
                    str_initial += '\t'

                elif board[r][c] == '#':  # wall
                    str_initial += f'game_board[{r}][{c}] = Wall &\n'
                    str_initial += '\t'

                elif board[r][c] == '.':  # goal
                    str_initial += f'game_board[{r}][{c}] = Goal &\n'
                    str_initial += '\t'

                elif board[r][c] == '-':  # floor
                    str_initial += f'game_board[{r}][{c}] = Floor &\n'
                    str_initial += '\t'

    return str_initial


def define_transitions(board):
    """
    Define the transition rules of the SMV model.
    :param board: the board of the current Sokoban game
    :return: the transition rules as a string
    """
    transitions = ''
    num_rows = len(board)
    num_cols = len(board[0])

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == '#':
                transitions += f'next(game_board[{i}][{j}]) := Wall;\n\t'
            else:
                transitions += f'next(game_board[{i}][{j}]) := \n\t\tcase\n'
                # MAYBE IN DEFAULT CASE
                transitions += f'\t\t\t--Current @ V + next cell #\n'
                transitions += f'\t\t\t(game_board[{i}][{j}] = Player | game_board[{i}][{j}] = PonGoal) & movement = l & game_board[{i}][{j - 1}] = Wall: game_board[{i}][{j}];\n'
                transitions += f'\t\t\t(game_board[{i}][{j}] = Player | game_board[{i}][{j}] = PonGoal) & movement = r & game_board[{i}][{j + 1}] = Wall: game_board[{i}][{j}];\n'
                transitions += f'\t\t\t(game_board[{i}][{j}] = Player | game_board[{i}][{j}] = PonGoal) & movement = u & game_board[{i - 1}][{j}] = Wall: game_board[{i}][{j}];\n'
                transitions += f'\t\t\t(game_board[{i}][{j}] = Player | game_board[{i}][{j}] = PonGoal) & movement = d & game_board[{i + 1}][{j}] = Wall: game_board[{i}][{j}];\n\n'

                # -----------------------------------------------------------------------------------------------
                transitions += f'\t\t\t--Current @ next cell .\n'
                transitions += f'\t\t\tgame_board[{i}][{j}] = Player & movement = l & game_board[{i}][{j - 1}] = Goal: Floor;\n'
                transitions += f'\t\t\tgame_board[{i}][{j}] = Player & movement = r & game_board[{i}][{j + 1}] = Goal: Floor;\n'
                transitions += f'\t\t\tgame_board[{i}][{j}] = Player & movement = u & game_board[{i - 1}][{j}] = Goal: Floor;\n'
                transitions += f'\t\t\tgame_board[{i}][{j}] = Player & movement = d & game_board[{i + 1}][{j}] = Goal: Floor;\n\n'

                transitions += '\t\t\t-- other tiles cases for Current @ next cell .\n'
                transitions += f'\t\t\tgame_board[{i}][{j + 1}] = Player & movement = l & game_board[{i}][{j}] = Goal: PonGoal;\n'
                transitions += f'\t\t\tgame_board[{i}][{j - 1}] = Player & movement = r & game_board[{i}][{j}] = Goal: PonGoal;\n'
                transitions += f'\t\t\tgame_board[{i + 1}][{j}] = Player & movement = u & game_board[{i}][{j}] = Goal: PonGoal;\n'
                transitions += f'\t\t\tgame_board[{i - 1}][{j}] = Player & movement = d & game_board[{i}][{j}] = Goal: PonGoal;\n\n'

                # -----------------------------------------------------------------------------------------------
                transitions += f'\t\t\t--Current @ next cell -\n'
                transitions += f'\t\t\tgame_board[{i}][{j}] = Player & movement = l & game_board[{i}][{j - 1}] = Floor: Floor;\n'
                transitions += f'\t\t\tgame_board[{i}][{j}] = Player & movement = r & game_board[{i}][{j + 1}] = Floor: Floor;\n'
                transitions += f'\t\t\tgame_board[{i}][{j}] = Player & movement = u & game_board[{i - 1}][{j}] = Floor: Floor;\n'
                transitions += f'\t\t\tgame_board[{i}][{j}] = Player & movement = d & game_board[{i + 1}][{j}] = Floor: Floor;\n\n'

                transitions += '\t\t\t-- other tiles cases for Current @ next cell -\n'
                transitions += f'\t\t\tgame_board[{i}][{j + 1}] = Player & movement = l & game_board[{i}][{j}] = Floor: Player;\n'
                transitions += f'\t\t\tgame_board[{i}][{j - 1}] = Player & movement = r & game_board[{i}][{j}] = Floor: Player;\n'
                transitions += f'\t\t\tgame_board[{i + 1}][{j}] = Player & movement = u & game_board[{i}][{j}] = Floor: Player;\n'
                transitions += f'\t\t\tgame_board[{i - 1}][{j}] = Player & movement = d & game_board[{i}][{j}] = Floor: Player;\n\n'

                # -----------------------------------------------------------------------------------------------
                # MAYBE IN DEFAULT CASE
                transitions += f'\t\t\t--Current @ V + next cell $ V * next next cell $ V # V *\n'
                if j - 2 >= 0:
                    transitions += (
                        f'\t\t\t(game_board[{i}][{j}] = Player | game_board[{i}][{j}] = PonGoal) & movement = l & (game_board[{i}][{j - 1}] = Box | game_board[{i}][{j - 1}] = BonGoal) & '
                        f'(game_board[{i}][{j - 2}] = Box | game_board[{i}][{j - 2}] = Wall | game_board[{i}][{j - 2}] = BonGoal) : game_board[{i}][{j}];\n')
                if j + 2 < num_cols:
                    transitions += (
                        f'\t\t\t(game_board[{i}][{j}] = Player | game_board[{i}][{j}] = PonGoal) & movement = r & (game_board[{i}][{j + 1}] = Box | game_board[{i}][{j + 1}] = BonGoal) & '
                        f'(game_board[{i}][{j + 2}] = Box | game_board[{i}][{j + 2}] = Wall | game_board[{i}][{j + 2}] = BonGoal) : game_board[{i}][{j}];\n')
                if i - 2 >= 0:
                    transitions += (
                        f'\t\t\t(game_board[{i}][{j}] = Player | game_board[{i}][{j}] = PonGoal) & movement = u & (game_board[{i - 1}][{j}] = Box | game_board[{i - 1}][{j}] = BonGoal) & '
                        f'(game_board[{i - 2}][{j}] = Box | game_board[{i - 2}][{j}] = Wall | game_board[{i - 2}][{j}] = BonGoal) : game_board[{i}][{j}];\n')
                if i + 2 < num_rows:
                    transitions += (
                        f'\t\t\t(game_board[{i}][{j}] = Player | game_board[{i}][{j}] = PonGoal) & movement = d & (game_board[{i + 1}][{j}] = Box | game_board[{i + 1}][{j}] = BonGoal) & '
                        f'(game_board[{i + 2}][{j}] = Box | game_board[{i + 2}][{j}] = Wall | game_board[{i + 2}][{j}] = BonGoal) : game_board[{i}][{j}];\n\n')
                # -----------------------------------------------------------------------------------------------
                transitions += f'\t\t\t--Current @ next cell $ V * next next cell - V .\n'
                if j - 2 >= 0:
                    transitions += (
                        f'\t\t\tgame_board[{i}][{j}] = Player & movement = l & (game_board[{i}][{j - 1}] = Box | game_board[{i}][{j - 1}] = BonGoal) & '
                        f'(game_board[{i}][{j - 2}] = Floor | game_board[{i}][{j - 2}] = Goal): Floor;\n')
                if j + 2 < num_cols:
                    transitions += (
                        f'\t\t\tgame_board[{i}][{j}] = Player & movement = r & (game_board[{i}][{j + 1}] = Box | game_board[{i}][{j + 1}] = BonGoal) & '
                        f'(game_board[{i}][{j + 2}] = Floor | game_board[{i}][{j + 2}] = Goal): Floor;\n')
                if i - 2 >= 0:
                    transitions += (
                        f'\t\t\tgame_board[{i}][{j}] = Player & movement = u & (game_board[{i - 1}][{j}] = Box | game_board[{i - 1}][{j}] = BonGoal) & '
                        f'(game_board[{i - 2}][{j}] = Floor | game_board[{i - 2}][{j}] = Goal): Floor;\n')
                if i + 2 < num_rows:
                    transitions += (
                        f'\t\t\tgame_board[{i}][{j}] = Player & movement = d & (game_board[{i + 1}][{j}] = Box | game_board[{i + 1}][{j}] = BonGoal) & '
                        f'(game_board[{i + 2}][{j}] = Floor | game_board[{i + 2}][{j}] = Goal): Floor;\n\n')

                transitions += '\t\t\t-- other tiles cases\n'
                if j + 2 < num_cols:
                    transitions += (
                        f'\t\t\t(game_board[{i}][{j + 2}] = Player | game_board[{i}][{j + 2}] = PonGoal) & movement = l & (game_board[{i}][{j + 1}] = Box | game_board[{i}][{j + 1}] = BonGoal) & '
                        f'game_board[{i}][{j}] = Floor: Box;\n')
                if j - 2 >= 0:
                    transitions += (
                        f'\t\t\t(game_board[{i}][{j - 2}] = Player | game_board[{i}][{j - 2}] = PonGoal) & movement = r & (game_board[{i}][{j - 1}] = Box | game_board[{i}][{j - 1}] = BonGoal) & '
                        f'game_board[{i}][{j}] = Floor: Box;\n')
                if i + 2 < num_rows:
                    transitions += (
                        f'\t\t\t(game_board[{i + 2}][{j}] = Player | game_board[{i + 2}][{j}] = PonGoal) & movement = u & (game_board[{i + 1}][{j}] = Box | game_board[{i + 1}][{j}] = BonGoal) & '
                        f'game_board[{i}][{j}] = Floor: Box;\n')
                if i - 2 >= 0:
                    transitions += (
                        f'\t\t\t(game_board[{i - 2}][{j}] = Player | game_board[{i - 2}][{j}] = PonGoal) & movement = d & (game_board[{i - 1}][{j}] = Box | game_board[{i - 1}][{j}] = BonGoal) & '
                        f'game_board[{i}][{j}] = Floor: Box;\n\n')

                # -----------------------------------------------------------------------------------------------
                transitions += (
                    f'\t\t\t(game_board[{i}][{j + 1}] = Player | game_board[{i}][{j + 1}] = PonGoal) & movement = l & game_board[{i}][{j}] = Box & '
                    f'(game_board[{i}][{j - 1}] = Floor | game_board[{i}][{j - 1}] = Goal): Player;\n')
                transitions += (
                    f'\t\t\t(game_board[{i}][{j - 1}] = Player | game_board[{i}][{j - 1}] = PonGoal) & movement = r & game_board[{i}][{j}] = Box & '
                    f'(game_board[{i}][{j + 1}] = Floor | game_board[{i}][{j + 1}] = Goal): Player;\n')
                transitions += (
                    f'\t\t\t(game_board[{i + 1}][{j}] = Player | game_board[{i + 1}][{j}] = PonGoal) & movement = u & game_board[{i}][{j}] = Box & '
                    f'(game_board[{i - 1}][{j}] = Floor | game_board[{i - 1}][{j}] = Goal): Player;\n')
                transitions += (
                    f'\t\t\t(game_board[{i - 1}][{j}] = Player | game_board[{i - 1}][{j}] = PonGoal) & movement = d & game_board[{i}][{j}] = Box & '
                    f'(game_board[{i + 1}][{j}] = Floor | game_board[{i + 1}][{j}] = Goal): Player;\n\n')
                # -----------------------------------------------------------------------------------------------
                transitions += (
                    f'\t\t\t(game_board[{i}][{j + 1}] = Player | game_board[{i}][{j + 1}] = PonGoal) & movement = l & game_board[{i}][{j}] = BonGoal & '
                    f'(game_board[{i}][{j - 1}] = Floor | game_board[{i}][{j - 1}] = Goal): PonGoal;\n')
                transitions += (
                    f'\t\t\t(game_board[{i}][{j - 1}] = Player | game_board[{i}][{j - 1}] = PonGoal) & movement = r & game_board[{i}][{j}] = BonGoal & '
                    f'(game_board[{i}][{j + 1}] = Floor | game_board[{i}][{j + 1}] = Goal): PonGoal;\n')
                transitions += (
                    f'\t\t\t(game_board[{i + 1}][{j}] = Player | game_board[{i + 1}][{j}] = PonGoal) & movement = u & game_board[{i}][{j}] = BonGoal & '
                    f'(game_board[{i - 1}][{j}] = Floor | game_board[{i - 1}][{j}] = Goal): PonGoal;\n')
                transitions += (
                    f'\t\t\t(game_board[{i - 1}][{j}] = Player | game_board[{i - 1}][{j}] = PonGoal) & movement = d & game_board[{i}][{j}] = BonGoal & '
                    f'(game_board[{i + 1}][{j}] = Floor | game_board[{i + 1}][{j}] = Goal): PonGoal;\n\n')
                # -----------------------------------------------------------------------------------------------

                transitions += '\t\t\t-- other tiles cases\n'
                if j + 2 < num_cols:
                    transitions += (
                        f'\t\t\t(game_board[{i}][{j + 2}] = Player | game_board[{i}][{j + 2}] = PonGoal) & movement = l & (game_board[{i}][{j + 1}] = Box | game_board[{i}][{j + 1}] = BonGoal) & '
                        f'game_board[{i}][{j}] = Goal: BonGoal;\n')
                if j - 2 >= 0:
                    transitions += (
                        f'\t\t\t(game_board[{i}][{j - 2}] = Player | game_board[{i}][{j - 2}] = PonGoal) & movement = r & (game_board[{i}][{j - 1}] = Box | game_board[{i}][{j - 1}] = BonGoal) & '
                        f'game_board[{i}][{j}] = Goal: BonGoal;\n')
                if i + 2 < num_rows:
                    transitions += (
                        f'\t\t\t(game_board[{i + 2}][{j}] = Player | game_board[{i + 2}][{j}] = PonGoal) & movement = u & (game_board[{i + 1}][{j}] = Box | game_board[{i + 1}][{j}] = BonGoal) & '
                        f'game_board[{i}][{j}] = Goal: BonGoal;\n')
                if i - 2 >= 0:
                    transitions += (
                        f'\t\t\t(game_board[{i - 2}][{j}] = Player | game_board[{i - 2}][{j}] = PonGoal) & movement = d & (game_board[{i - 1}][{j}] = Box | game_board[{i - 1}][{j}] = BonGoal) & '
                        f'game_board[{i}][{j}] = Goal: BonGoal;\n\n')

                transitions += '\t\t\t-- other tiles cases\n'
                if j + 2 < num_cols:
                    transitions += (
                        f'\t\t\tgame_board[{i}][{j + 2}] = Player & movement = l & game_board[{i}][{j + 1}] = BonGoal & '
                        f'game_board[{i}][{j}] = Floor: PonGoal;\n')
                if j - 2 >= 0:
                    transitions += (
                        f'\t\t\tgame_board[{i}][{j - 2}] = Player & movement = r & game_board[{i}][{j - 1}] = BonGoal & '
                        f'game_board[{i}][{j}] = Floor: PonGoal;\n')
                if i + 2 < num_rows:
                    transitions += (
                        f'\t\t\tgame_board[{i + 2}][{j}] = Player & movement = u & game_board[{i + 1}][{j}] = BonGoal & '
                        f'game_board[{i}][{j}] = Floor: PonGoal;\n')
                if i - 2 >= 0:
                    transitions += (
                        f'\t\t\tgame_board[{i - 2}][{j}] = Player & movement = d & game_board[{i - 1}][{j}] = BonGoal & '
                        f'game_board[{i}][{j}] = Floor: PonGoal;\n\n')
                # -----------------------------------------------------------------------------------------------

                # EXAMIN THE CASE OF THE MAN ON GOAL
                transitions += f'\t\t\t--Current + next cell .\n'
                transitions += f'\t\t\tgame_board[{i}][{j}] = PonGoal & movement = l & game_board[{i}][{j - 1}] = Goal: Goal;\n'
                transitions += f'\t\t\tgame_board[{i}][{j}] = PonGoal & movement = r & game_board[{i}][{j + 1}] = Goal: Goal;\n'
                transitions += f'\t\t\tgame_board[{i}][{j}] = PonGoal & movement = u & game_board[{i - 1}][{j}] = Goal: Goal;\n'
                transitions += f'\t\t\tgame_board[{i}][{j}] = PonGoal & movement = d & game_board[{i + 1}][{j}] = Goal: Goal;\n\n'

                transitions += '\t\t\t-- other tiles cases\n'
                transitions += f'\t\t\tgame_board[{i}][{j + 1}] = PonGoal & movement = l & game_board[{i}][{j}] = Goal: PonGoal;\n'
                transitions += f'\t\t\tgame_board[{i}][{j - 1}] = PonGoal & movement = r & game_board[{i}][{j}] = Goal: PonGoal;\n'
                transitions += f'\t\t\tgame_board[{i + 1}][{j}] = PonGoal & movement = u & game_board[{i}][{j}] = Goal: PonGoal;\n'
                transitions += f'\t\t\tgame_board[{i - 1}][{j}] = PonGoal & movement = d & game_board[{i}][{j}] = Goal: PonGoal;\n\n'

                # -----------------------------------------------------------------------------------------------
                transitions += f'\t\t\t--Current + next cell -\n'
                transitions += f'\t\t\tgame_board[{i}][{j}] = PonGoal & movement = l & game_board[{i}][{j - 1}] = Floor: Goal;\n'
                transitions += f'\t\t\tgame_board[{i}][{j}] = PonGoal & movement = r & game_board[{i}][{j + 1}] = Floor: Goal;\n'
                transitions += f'\t\t\tgame_board[{i}][{j}] = PonGoal & movement = u & game_board[{i - 1}][{j}] = Floor: Goal;\n'
                transitions += f'\t\t\tgame_board[{i}][{j}] = PonGoal & movement = d & game_board[{i + 1}][{j}] = Floor: Goal;\n\n'

                transitions += '\t\t\t-- other tiles cases\n'
                transitions += f'\t\t\tgame_board[{i}][{j + 1}] = PonGoal & movement = l & game_board[{i}][{j}] = Floor: Player;\n'
                transitions += f'\t\t\tgame_board[{i}][{j - 1}] = PonGoal & movement = r & game_board[{i}][{j}] = Floor: Player;\n'
                transitions += f'\t\t\tgame_board[{i + 1}][{j}] = PonGoal & movement = u & game_board[{i}][{j}] = Floor: Player;\n'
                transitions += f'\t\t\tgame_board[{i - 1}][{j}] = PonGoal & movement = d & game_board[{i}][{j}] = Floor: Player;\n\n'

                # -----------------------------------------------------------------------------------------------
                transitions += f'\t\t\t--Current + V next cell $ next next cell - V .\n'
                if j - 2 >= 0:
                    transitions += (
                        f'\t\t\tgame_board[{i}][{j}] = PonGoal & movement = l & (game_board[{i}][{j - 1}] = Box | game_board[{i}][{j - 1}] = BonGoal) & '
                        f'(game_board[{i}][{j - 2}] = Floor | game_board[{i}][{j - 2}] = Goal): Goal;\n')
                if j + 2 < num_cols:
                    transitions += (
                        f'\t\t\tgame_board[{i}][{j}] = PonGoal & movement = r & (game_board[{i}][{j + 1}] = Box | game_board[{i}][{j + 1}] = BonGoal) & '
                        f'(game_board[{i}][{j + 2}] = Floor | game_board[{i}][{j + 2}] = Goal): Goal;\n')
                if i - 2 >= 0:
                    transitions += (
                        f'\t\t\tgame_board[{i}][{j}] = PonGoal & movement = u & (game_board[{i - 1}][{j}] = Box | game_board[{i - 1}][{j}] = BonGoal) & '
                        f'(game_board[{i - 2}][{j}] = Floor | game_board[{i - 2}][{j}] = Goal): Goal;\n')
                if i + 2 < num_rows:
                    transitions += (
                        f'\t\t\tgame_board[{i}][{j}] = PonGoal & movement = d & (game_board[{i + 1}][{j}] = Box | game_board[{i + 1}][{j}] = BonGoal) & '
                        f'(game_board[{i + 2}][{j}] = Floor | game_board[{i + 2}][{j}] = Goal): Goal;\n\n')

                # -----------------------------------------------------------------------------------------------
                # DEFAULT CASE
                transitions += f'\n\t\t\t-- Default case\n'
                transitions += f'\t\t\tTRUE: game_board[{i}][{j}];\n'
                transitions += f'\t\tesac;\n'
                transitions += '\n\t\t'

    return transitions

def define_solvability(board):
    """
    Define the solvability condition for the Sokoban game.
    :param board: the board of the current Sokoban game
    :return: the solvability condition as a string
    """

    # get the locations of the targets
    targets = [(y, x) for y in range(len(board))
               for x in range(len(board[0]))
               if board[y][x] == '.' or board[y][x] == '+' or board[y][x] == '*']

    # Generate the winning conditions
    win_conditions = f''
    for target in targets:
        # if we are in the last target then we don't need to add the '&' operator
        if target == targets[-1]:
            win_conditions += f'(game_board[{target[0]}][{target[1]}] = BonGoal) ;'
        else:
            win_conditions += f'(game_board[{target[0]}][{target[1]}] = BonGoal) & '

    return win_conditions


# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^ MAIN FUNCTION OF SCRIPT ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
##### CHANGE HERE TO THE FULL BOARD PATH #####
def gen_board(board_file= 'board10.txt'):
    """
    Generate the SMV model file for the given Sokoban board.
    :param board_file: the file containing the Sokoban board
    :return: the name of the generated SMV model file
    """
    # read board from file
    board = read_from_file(board_file)

    # create SMV model and win conditions
    smv_model = create_smv_model(board)

    # save the SMV model to a file with a meaningful name
    model_file_name = 'sokoban_model.smv'

    # save the current path
    current_path = os.getcwd()

    #### CHANGE THE PATH TO THE PATH OF YOUR nuXmv BIN FOLDER ####
    model_file_path = r'C:\Users\shoham\Documents\ENG_degree\Final Project\nuXmv-2.0.0-win64\bin'
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    os.chdir(model_file_path)

    with open(model_file_name, 'w') as file:
        file.write(smv_model)

    # change the directory back to the original directory
    os.chdir(current_path)

    return model_file_name

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

