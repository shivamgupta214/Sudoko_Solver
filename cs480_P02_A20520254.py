import csv
import sys
import time
import os


def load_puzzle(input_filename):        # Load the puzzle data from the filename, return: puzzle 2D array of data
    puzzle = []

    with open(input_filename) as csvinput:
        row_reader = csv.reader(csvinput)
        for row in row_reader:
            puzzle.append(row)

    return puzzle

def display_puzzle(puzzle):   # Display the puzzle for sudoku

    for i in range(9):
        print(",".join(puzzle[i]))

def get_next_open_position(puzzle, type="linear"):  # Fetch the next position in the puzzle, return: (row, col) Coordinates of next position to fill
  
    result = None
    if type == "linear":
        for row in range(9):
            for col in range(9):
                if(puzzle[row][col] == "X"):
                    return (row, col)

    elif type == "mrv":
        mrv = 10
        for row in range(9):
            for col in range(9):
                if (puzzle[row][col] == "X"):
                    possible_values = get_possible_values(puzzle,row, col)
                    if len(possible_values) < mrv:
                        mrv = len(possible_values)
                        result = (row, col, possible_values)

    return result

def validate_element(puzzle, row, col, element):   # Validate element fits in row, col of the sudoku grid
    #Validate Row
    for x in range(9):
        if puzzle[row][x] == element:
            #print("Failure Row: ", element)
            #display_puzzle(puzzle)
            return False

    #Validate Column
    for x in range(9):
        if puzzle[x][col] == element:
            #print("Failed Col: ", element)
            return False

    #Validate Box
    boxRow = row - row % 3
    boxCol = col - col % 3
    for i in range(3):
        for j in range(3):
            if puzzle[i + boxRow][j + boxCol] == element:
                #print("Failed Box: ", element)
                return False

    return True

def brute_force_solution(puzzle):  #Brute force
    global nodes
    pos = get_next_open_position(puzzle)
    if pos is None:
        return True

    row = pos[0]
    col = pos[1]

    for element in [str(i) for i in range(1, 10)]:
        nodes += 1
        if validate_element(puzzle, row, col, element):
            puzzle[row][col] = element

            if brute_force_solution(puzzle):
                return True

        puzzle[row][col] = "X"
    return False

def get_possible_values(puzzle, row, col): #possible values to be assigned 
    constraints = set()  # constraints for the variable (row, col)

    if puzzle[row][col] != "X":
        return [puzzle[row][col]]
    else:
        row_constraints = []
        col_constraints = []
        box_constraints = []
        for i in range(9):
            if puzzle[row][i] != "X":
                row_constraints.append(puzzle[row][i])

        for i in range(9):
            if (puzzle[i][col] != "X"):
                col_constraints.append(puzzle[i][col])

        box_row = row - row % 3
        box_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if (puzzle[i + box_row][j + box_col] != "X"):
                    box_constraints.append(puzzle[i + box_row][j + box_col])

        constraints = set(row_constraints + col_constraints + box_constraints)
        result = [str(i) for i in range(1,10) if str(i) not in constraints]

        return result

def  backtracking_solution(puzzle):     # CSPback-tracking search
    global nodes
    pos = get_next_open_position(puzzle)
    if pos is None:
        return True

    row = pos[0]
    col = pos[1]

    available_values = get_possible_values(puzzle, row, col)
    if len(available_values) == 0:
        return False

    for element in available_values:
        nodes += 1
        if validate_element(puzzle, row, col, element):
            puzzle[row][col] = element

            if backtracking_solution(puzzle):
                return True

        puzzle[row][col] = "X"
    return False


def csp_mrv_solution(puzzle):           # CSP with forward-checking and MRV heuristics
    global nodes
    pos = get_next_open_position(puzzle, "mrv")
    if pos is None:
        return True

    row = pos[0]
    col = pos[1]
    available_values = pos[2]

    if len(available_values) == 0:
        return False

    for element in available_values:
        nodes += 1
        if validate_element(puzzle, row, col, element):
            puzzle[row][col] = element

            if csp_mrv_solution(puzzle):
                return True

        puzzle[row][col] = "X"
    return False

def test_puzzle(puzzle):        #check input puzzle if empty or filled
    is_valid = True

    #Row Validation
    for row in range(9):
        row_elements = set(puzzle[row])
        if len(row_elements) != 9:
            is_valid = False
            break
        for e in row_elements:
            if e == 'X':
                is_valid = False
                break

    #Col Validation
    if is_valid:
        #Col Validation
        for col in range(9):
            col_elements = set([puzzle[i][col] for i in range(9)])
            if len(col_elements) != 9:
                is_valid = False
                break
            for e in col_elements:
                if e == 'X':
                    is_valid = False
                    break

    #Box Validation
    if is_valid:
        for base_row in range(3):
            for base_col in range(3):
                box_elements = []
                for i in range(3):
                    for j in range(3):
                        box_elements.append(puzzle[base_row*3+i][base_col+3+j])
                if len(box_elements) != 9:
                    is_valid = False
                    break
                for e in box_elements:
                    if e == 'X':
                        is_valid = False
                        break
    if is_valid:
        print("This is a valid, solved, Sudoku puzzle.")
    else:
        print("ERROR: This is NOT a solved Sudoku puzzle.")

def save_result(sudoku_grid, Filename):
    """
    Save the Grid values into the file, Filename
    :param sudoku_grid:
    :param Filename:
    :return: None
    """
    with open(Filename, "w+") as f:
        for i in range(9):
            f.write(",".join(sudoku_grid[i])+"\n")


#Program Begins here
if __name__ == "__main__":
    args = sys.argv
    input_csv = ''
    algo_mode = ''
    firstName = "Shivam"
    lastName = "Gupta"
    a_number = "A20520254"
    list = ('1', '2', '3', '4')
    if len(args) == 3 and args[2] in list and os.path.isfile(args[1]):
        input_csv = args[1]
        algo_mode = args[2]
    else: 
        print("ERROR: Not enough/too many/illegal input arguments.")
        quit()

    puzzle = load_puzzle(input_csv)

    global nodes
    if algo_mode == list[0]:

        nodes = 0
        print("{}, {}, {} Solution".format(lastName, firstName, a_number))
        print("Input File: {}".format(input_csv))
        print("Algorithm:", "BruteForce")

        print("\nInput Puzzle:")
        display_puzzle(puzzle)

        print("")
        start_time = time.time()
        brute_force_solution(puzzle)
        end_time = time.time()

        print("Number of search tree nodes generated: {}".format(nodes))
        print("Search time: {} seconds".format(round(end_time - start_time, 3)))
        print("")
        print("Solved Puzzle:")
        display_puzzle(puzzle)
        save_result(puzzle, os.path.splitext(input_csv)[0] + "_SOLUTION.csv")
        print("Result is saved")

    elif algo_mode == list[1]:
        nodes = 0
        print("{}, {}, {} Solution".format(lastName, firstName, a_number))
        print("Input File: {}".format(input_csv))
        print("Algorithm: CSP BackTracking")

        print("\nInput Puzzle:")
        display_puzzle(puzzle)

        print("")

        start_time = time.time()
        backtracking_solution(puzzle)
        end_time = time.time()

        print("Number of search tree nodes generated: {}".format(nodes))
        print("Search time: {} seconds".format(round(end_time - start_time, 3)))
        print("")
        print("Solved Puzzle:")
        display_puzzle(puzzle)
        save_result(puzzle, os.path.splitext(input_csv)[0] + "_SOLUTION.csv")
        print("Result is saved")

    elif algo_mode == list[2]:
        nodes = 0
        print("{}, {}, {} Solution".format(lastName, firstName, a_number))
        print("Input File: {}".format(input_csv))
        print("Algorithm: CSP with forward-checking and MRV heuristics")

        print("\nInput Puzzle:")
        display_puzzle(puzzle)

        print("")

        start_time = time.time()
        csp_mrv_solution(puzzle)
        end_time = time.time()

        print("Number of search tree nodes generated: {}".format(nodes))
        print("Search time: {} seconds".format(round(end_time - start_time, 3)))
        print("")
        print("Solved Puzzle:")
        display_puzzle(puzzle)
        save_result(puzzle, os.path.splitext(input_csv)[0] + "_SOLUTION.csv")
        print("Result is saved")

    elif algo_mode == list[3]:
        print("{}, {}, {} Solution".format(lastName, firstName, a_number))
        print("Input File: {}".format(input_csv))
        print("Algorithm: Test")

        print("\nInput Puzzle:")
        display_puzzle(puzzle)

        print("")
        print("Number of search tree nodes generated: 0")
        print("Search time: 0 seconds")
        test_puzzle(puzzle)
