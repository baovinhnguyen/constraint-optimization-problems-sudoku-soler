import copy
import numpy as np
c3 = [(i, j) for i in range(3) for j in range(3)]
c9 = [(i, j) for i in range(9) for j in range(9)]

easy_puzzle = [[6, 0, 8, 7, 0, 2, 1, 0, 0],
          [4, 0, 0, 0, 1, 0, 0, 0, 2],
          [0, 2, 5, 4, 0, 0, 0, 0, 0],
          [7, 0, 1, 0, 8, 0, 4, 0, 5],
          [0, 8, 0, 0, 0, 0, 0, 7, 0],
          [5, 0, 9, 0, 6, 0, 3, 0, 1],
          [0, 0, 0, 0, 0, 6, 7, 5, 0],
          [2, 0, 0, 0, 9, 0, 0, 0, 8],
          [0, 0, 6, 8, 0, 5, 2, 0, 3]]
hard_puzzle = [[0, 7, 0, 0, 4, 2, 0, 0, 0],
          [0, 0, 0, 0, 0, 8, 6, 1, 0],
          [3, 9, 0, 0, 0, 0, 0, 0, 7],
          [0, 0, 0, 0, 0, 4, 0, 0, 9],
          [0, 0, 3, 0, 0, 0, 7, 0, 0],
          [5, 0, 0, 1, 0, 0, 0, 0, 0],
          [8, 0, 0, 0, 0, 0, 0, 7, 6],
          [0, 5, 4, 8, 0, 0, 0, 0, 0],
          [0, 0, 0, 6, 1, 0, 0, 5, 0]]
trivial = [[1, 2, 3, 4, 5, 6, 7, 8, 9],
            [2, 3, 4, 5, 6, 7, 8, 9, 1],
            [3, 4, 5, 6, 7, 8, 9, 1, 2],
            [4, 5, 6, 7, 8, 9, 1, 2, 3],
            [5, 6, 7, 8, 9, 1, 2, 3, 4],
            [6, 7, 8, 9, 1, 2, 3, 4, 5],
            [7, 8, 9, 1, 2, 3, 4, 5, 6],
            [8, 9, 1, 2, 3, 4, 5, 6, 7],
            [9, 1, 2, 3, 4, 5, 6, 7, 8]]

class Board():

    def __init__(self, board):
        self.board = board
        self.remaining = [(i, j) for i, j in c9 if board[i][j] == 0]
        self.choices = self.find_choices(board)

    def find_choices(self, board):
        self.choices = {(i, j):list(range(1, 10)) for i, j in c9}
        for i, j in c9:
            if board[i][j] > 0:
                self.remove_choices(i, j)
        return self.choices

    def remove_choices(self, i, j):
        num = self.board[i][j]
        for k in range(9):
            if num in self.choices[(i, k)]:
                self.choices[(i, k)].remove(num)
        for k in range(9):
            if num in self.choices[(k, j)]:
                self.choices[(k, j)].remove(num)
        bigi = i // 3
        bigj = j // 3
        for k, l in c3:
            kk = bigi*3 + k
            ll = bigj*3 + l
            if num in self.choices[(kk, ll)]:
                self.choices[(kk, ll)].remove(num)


    def print_board(self):
        board = self.board
        print('-------------------------', end='')
        for i in range(9):
            print('\n|', end=' ')
            for j in range(9):
                if (board[i][j] == 0):
                    print('-', end=' ')
                else:
                    print(board[i][j], end=' ')
                if (j % 3 == 2):
                    print('|', end=' ')
            if (i % 3 == 2):
                print('\n-------------------------', end='')
        print('')

    def is_solved(self):

        board = self.board

        # check rows
        for i in range(9):
            possible_values = list(range(1, 10))
            for j in range(9):
                if board[i][j] == 0:
                    print('Still have blank cells...')
                    return False
                elif board[i][j] not in possible_values:
                    print('Error: Duplicate values.')
                    return False
                else:
                    possible_values.remove(board[i][j])

        # check columns
        for j in range(9):
            possible_values = list(range(1, 10))
            for i in range(9):
                if board[i][j] == 0:
                    print('Still have blank cells...')
                    return False
                elif board[i][j] not in possible_values:
                    print('Error: Duplicate values.')
                    return False
                else:
                    possible_values.remove(board[i][j])

        # check boxes
        for bigi, bigj in c3:
            possible_values = list(range(1, 10))
            for k, l in c3:
                i = bigi*3 + k
                j = bigj*3 + l
                if board[i][j] == 0:
                    print('Still have blank cells...')
                    return False
                elif board[i][j] not in possible_values:
                    print('Error: Duplicate values.')
                    return False
                else:
                    possible_values.remove(board[i][j])

        # if nothing fails, must be solution
        return True

    def total_potential_values(self):
        num_potential_values = [len(self.choices[square]) for square in self.remaining]
        return sum(num_potential_values)

def square_fewest_values(board: Board):
    min = 10
    if len(board.remaining) == 0:
        return((-1, -1))
    for square in board.remaining:
        if len(board.choices[square]) < min:
            min = len(board.choices[square])
            min_square = square
        if min == 1:
            return min_square
    return min_square


# finds the square with the fewest possible values, and
# returns a node with the necessary information to evaluate that square next
# OPTIMIZATION: Minimum Remaining Values (MRV)
def find_next_square(board):
    sq_sols = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    sq_row = 0
    sq_col = 0
    for row in range(9):
        for col in range(9):
            if not board[row][col]:
                next = find_possible_vals(board, row, col)
                if len(next) == 1:
                    return Node(next, row, col, board)
                if not board[row][col] and len(sq_sols) > len(next):
                    sq_sols = next
                    sq_row = row
                    sq_col = col
    return Node(sq_sols, sq_row, sq_col, board)

def recursive_solve(board: Board, level):
    if board.is_solved():
        return board

    square = square_fewest_values(board)
    if len(board.choices[square]) == 0:
        print('Failed because no choices left for a square.')
        return board

    i, j = square
    potential_values = {board.choices[square]: -1}
    for value in board.choices[square]:
        new_board = copy.deepcopy[board]
        new_board.board[i][j] = value
        new_board.remove_choices(i, j)
        potential_values[value] = new_board.total_potential_values()



    tried_first= False
    # we look through possible_value_sums in order of lowest PVS first
    # OPTIMIZATION: Least Constraining Value (LCV)
    for pvs in sorted(possible_value_sums):
        while possible_value_sums[pvs]:
            if tried_first:
                print('Backtracked to square #' + str(level) + ' assigned')
            else:
                tried_first = True
            answer = recursive_solve(possible_value_sums[pvs][0], level + 1)
            possible_value_sums[pvs] = possible_value_sums[pvs][1:]
            if answer != 'FAIL':
                return answer
    return 'FAIL'

def solve_sudoku(puzzle):
    result = recursive_solve(puzzle, 0)
    print('Congratulations! Here is your solution:')
    print_sudoku(result)


# User interface: prompts user to ask if they want to solve easy or hard puzzle, then solves and returns solution
inp = input('Hello! Would you like to solve the easy or hard puzzle? (type h for hard, e for easy)')
if inp == 'h':
    puzzle = hard_puzzle
    diff = 'hard'

elif inp == 'e':
    puzzle = easy_puzzle
    diff = 'easy'
print('You chose to solve the ' + diff + ' puzzle. Here it is:')
print_sudoku(puzzle)
print('Now, let\'s solve it:')
solve_sudoku(puzzle)
