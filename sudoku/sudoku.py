class Sudoku:
    '''A set of functions to solve a Sudoku puzzle. Optionally
       it can also solve a diagnol sudoku - but this requires the class
       to  be initialized with is_diag=1
    '''
    def __init__(self, is_diag=0):
        self.boxes     = self.cross(self.rows,self.cols)
        self.row_units = [self.cross(r,self.cols) for r in self.rows]
        self.col_units = [self.cross(self.rows,c) for c in self.cols]
        self.sqr_units = [self.cross(r,c)                \
                          for r in ['ABC', 'DEF', 'GHI'] \
                          for c in ['123', '456', '789']]
        # Diagnol units are boxes that are in a diagnol in the sudoku - in mathematical
        # terms these are boxes for which the column and row number is the same
        self.dia_units = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'],
                          ['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']]
        # All units (include diagnol units if is_diag=1)
        self.lst_units = self.row_units + self.col_units + self.sqr_units + (self.dia_units if is_diag==1 else [])
        self.units     = dict((s, [u for u in self.lst_units if s in u]) for s in self.boxes)
        self.peers     = dict((s, set(sum(self.units[s],[]))-set([s])) for s in self.boxes)

        # Variables
    rows      = 'ABCDEFGHI'
    cols      = '123456789'
    boxes     = []
    row_units = []
    col_units = []
    sqr_units = []
    lst_units = []
    units     = {}
    peers     = {}

    # function: cross
    def cross(self, a,b):
        # Return a cross of every element in the two
        # strings
        return [s+t for s in a for t in b]

    # function: grid_values()
    def grid_values(self, s, con=0):
        # A function to convert a string representation of
        # grid values into a dictionary. Create a dictionary
        # for a string of upto 81 characters only
        d = {}
        i = 0
        for r in self.rows:
            for c in self.cols:
                d[r+c] = ('123456789' if s[i]=='.' and con==0 else s[i])
                i+=1
        return d

    # function: eliminate()
    def eliminate(self, d):
        # A function that reads a dictionary, if it finds
        # that a box has only one number, then it eliminates
        # that number from all its peers

        # First extract all of the boxes that aleady have
        # a solution
        solved = {}
        for b in self.boxes:
            if len(d[b])==1:
                solved[b] = d[b]
        # Now that I have a dictionary of all solved boxes, I need
        # to iterate over their peers and delete the matching values
        for b in solved:
            v = d[b]
            for p in self.peers[b]:
                d[p] = d[p].replace(v,'')
        # Return back the updated dictionary
        return d

    # function: only_choice()
    def only_choice(self, d):
        # A function that reads a dictionary and checks in a square
        # if there is only one choice available, then replaces that
        # choice with the digit in the box

        # Iterate over all squares, rows and columns
        for sqr in self.lst_units:
            # Generate a dictionary of boxes that are part of
            # a square, row or column
            mult_values = {}
            for i in range(0,9):
                mult_values[sqr[i]] = d[sqr[i]]
            # Iterate over these multiple values from 1-9
            for i in '123456789':
                mult_values_found = []
                for m_key in mult_values.keys():
                    if i in mult_values[m_key]:
                        mult_values_found.append(m_key)
                # If only one match is found, then use the key
                # that is stored in mult_values_found to then
                # replace the digit in that key
                if len(mult_values_found) == 1:
                    key = mult_values_found[0]
                    d[key] = i
        return d

    # function: only_choice()
    def reduce_puzzle(self, d):
        # A function that reads a dictionary of values which are
        # represented in digits and dots
        stalled = False
        while not stalled:
            # Check how many boxes have a determined value
            solved_d_before = len([box for box in d.keys() if len(d[box]) == 1])

            # Your code here: Use the Eliminate Strategy
            d = self.eliminate(d)
            # Your code here: Use the Only Choice Strategy
            d = self.only_choice(d)

            # Check how many boxes have a determined value, to compare
            solved_d_after = len([box for box in d.keys() if len(d[box]) == 1])
            # If no new values were added, stop the loop.
            stalled = solved_d_before == solved_d_after

            # Sanity check, return False if there is a box with zero available values:
            if len([box for box in d.keys() if len(d[box]) == 0]):
                return False
        return d

    def naked_twins(self, d):
        """This function called naked_twins looks for pair of numbers that appear
           exactly again in its peers. This implies that those numbers can only be
           placed in one of the two boxes, which also implies that they can be removed
           from all other boxes in its units"""
        # First find duplicates in columns
        for i in range(9):
            for j in range(9):
                curr_box_j_key = self.col_units[i][j]
                if len(d[curr_box_j_key])==2:
                    match = 0
                    for k in range(j+1,9):
                        if d[curr_box_j_key] == d[self.col_units[i][k]]:
                            match = 1
                    if match == 1:
                        for k in range(9):
                            curr_box_k_key = self.col_units[i][k]
                            if d[curr_box_j_key] != d[curr_box_k_key]:
                                for digit in d[curr_box_j_key]:
                                    if digit in d[curr_box_k_key]:
                                        d[curr_box_k_key] = d[curr_box_k_key].replace(digit,'')
        # Second find duplicates in rows
        for i in range(9):
            for j in range(9):
                curr_box_j_key = self.row_units[i][j]
                if len(d[curr_box_j_key])==2:
                    match = 0
                    for k in range(j+1,9):
                        if d[curr_box_j_key] == d[self.row_units[i][k]]:
                            match = 1
                    if match == 1:
                        for k in range(9):
                            curr_box_k_key = self.row_units[i][k]
                            if d[curr_box_j_key] != d[curr_box_k_key]:
                                for digit in d[curr_box_j_key]:
                                    if digit in d[curr_box_k_key]:
                                        d[curr_box_k_key] = d[curr_box_k_key].replace(digit,'')
        # Third find duplicates in squares
        for i in range(9):
            for j in range(9):
                curr_box_j_key = self.sqr_units[i][j]
                if len(d[curr_box_j_key])==2:
                    match = 0
                    for k in range(j+1,9):
                        if d[curr_box_j_key] == d[self.sqr_units[i][k]]:
                            match = 1
                    if match == 1:
                        for k in range(9):
                            curr_box_k_key = self.sqr_units[i][k]
                            if d[curr_box_j_key] != d[curr_box_k_key]:
                                for digit in d[curr_box_j_key]:
                                    if digit in d[curr_box_k_key]:
                                        d[curr_box_k_key] = d[curr_box_k_key].replace(digit,'')
        return d
    def search(self, d):
        """Using depth-first search and propagation, create
           a search tree and solve the sudoku."""
        # First, reduce the puzzle using the previous function
        # Choose one of the unfilled squares with the fewest possibilities
        # Now use recursion to solve each one of the resulting sudokus, and if one returns
        # a value (not False), return that answer!

        # Input is a sudoku puzzle dictionary. A solution is found using
        # the reduce_puzzle function. If it returns false, a solution was not found, then
        # traverse the next possible outcome in the tree. In order to traverse the tree
        # using DFS, we traverse column by column from top to bottom. First create a tree
        # with two possible values, then tree possible values and so on.

        # 1. Find a solution by reducing the puzzle
        d = self.reduce_puzzle(d)
        if d == False:
            return False

        d_num = len([box for box in d.keys() if len(d[box]) == 1])

        # 2. Return if a solution is found
        if d_num >= 81:
            return d

        # 3. Find all boxes that dont have a solution. As we are implementing a DFS
        #    search, we want to generate all keys on a column by column basis
        for i in [2,3,4,5]:
            d_keys = [box for col in self.col_units for box in col if len(d[box]) == i]

            # Early terminate if no keys found
            if len(d_keys) == 0:
                return d

            # 4. If a solution isn't found, then iterate on a column basis on
            #    possible solutions, by modifying the dictionary to correct the
            #    first occurence of multiple values
            c_key = d_keys[0] # Take the first occurence
            for j in d[c_key]: # Iterate over all possible values
                d_temp        = d.copy()
                d_temp[c_key] = j # Pick the jth possible value
                d_temp        = self.search(d_temp)
                # Check for error condition. If a solution is not found then
                # continue to a different iteration
                if d_temp == False:
                    continue
                else:
                    return d_temp

            # If I haven't found a solution at all after iterating over all columns
            # then return impossible solution - i.e False
            return False

    # function: solve
    def solve(self, grid):
        """
           Find the solution to a Sudoku grid.
           Args:
              grid(string): a string representing a sudoku grid.
              Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
           Returns:
             The dictionary representation of the final sudoku grid. False if no solution exists.
        """

        # Note that the input to the solve function is a string rather and a dictionary. First
        # convert the string into a dictionary
        d = self.grid_values(grid)
        # We use the eliminate and only_choice functions to solve the diagnol
        # sudoku problem. The class must be initialized with diagnol sudoku enabled
        return self.reduce_puzzle(d)

    # function: display
    def display(self, d):
        """
        Display the values as a 2-D grid.
        Input: The sudoku in dictionary form
        Output: None
        """
        width = 1 + max(len(d[s]) for s in self.boxes)
        line  = '+'.join(['-'*(width*3)]*3)
        for r in self.rows:
            print(''.join(d[r+c].center(width) + ('|' if c in '36' else '') for c in self.cols))
            if r in 'CF': print(line)
        return

# Main
if __name__ == '__main__':
    s = Sudoku(1)
    g1 = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'
    g2 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    g3 = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    d4 = {'I6': '4', 'H9': '3', 'I2': '6', 'E8': '1', 'H3': '5', 'H7': '8', 'I7': '1', 'I4': '8',
          'H5': '6', 'F9': '7', 'G7': '6', 'G6': '3', 'G5': '2', 'E1': '8', 'G3': '1', 'G2': '8',
          'G1': '7', 'I1': '23', 'C8': '5', 'I3': '23', 'E5': '347', 'I5': '5', 'C9': '1', 'G9': '5',
          'G8': '4', 'A1': '1', 'A3': '4', 'A2': '237', 'A5': '9', 'A4': '2357', 'A7': '27',
          'A6': '257', 'C3': '8', 'C2': '237', 'C1': '23', 'E6': '579', 'C7': '9', 'C6': '6',
          'C5': '37', 'C4': '4', 'I9': '9', 'D8': '8', 'I8': '7', 'E4': '6', 'D9': '6', 'H8': '2',
          'F6': '125', 'A9': '8', 'G4': '9', 'A8': '6', 'E7': '345', 'E3': '379', 'F1': '6',
          'F2': '4', 'F3': '23', 'F4': '1235', 'F5': '8', 'E2': '37', 'F7': '35', 'F8': '9',
          'D2': '1', 'H1': '4', 'H6': '17', 'H2': '9', 'H4': '17', 'D3': '2379', 'B4': '27',
          'B5': '1', 'B6': '8', 'B7': '27', 'E9': '2', 'B1': '9', 'B2': '5', 'B3': '6', 'D6': '279',
          'D7': '34', 'D4': '237', 'D5': '347', 'B8': '3', 'B9': '4', 'D1': '5'}

    d5 = {'A1': '23', 'A2': '4', 'A3': '7', 'A4': '6', 'A5': '8', 'A6': '5', 'A7': '23', 'A8': '9',
          'A9': '1', 'B1': '6', 'B2': '9', 'B3': '8', 'B4': '4', 'B5': '37', 'B6': '1', 'B7': '237',
          'B8': '5', 'B9': '237', 'C1': '23', 'C2': '5', 'C3': '1', 'C4': '23', 'C5': '379',
          'C6': '2379', 'C7': '8', 'C8': '6', 'C9': '4', 'D1': '8', 'D2': '17', 'D3': '9',
          'D4': '1235', 'D5': '6', 'D6': '237', 'D7': '4', 'D8': '27', 'D9': '2357', 'E1': '5',
          'E2': '6', 'E3': '2', 'E4': '8', 'E5': '347', 'E6': '347', 'E7': '37', 'E8': '1', 'E9': '9',
          'F1': '4', 'F2': '17', 'F3': '3', 'F4': '125', 'F5': '579', 'F6': '279', 'F7': '6',
          'F8': '8', 'F9': '257', 'G1': '1', 'G2': '8', 'G3': '6', 'G4': '35', 'G5': '345',
          'G6': '34', 'G7': '9', 'G8': '27', 'G9': '27', 'H1': '7', 'H2': '2', 'H3': '4', 'H4': '9',
          'H5': '1', 'H6': '8', 'H7': '5', 'H8': '3', 'H9': '6', 'I1': '9', 'I2': '3', 'I3': '5',
          'I4': '7', 'I5': '2', 'I6': '6', 'I7': '1', 'I8': '4', 'I9': '8'}
    g6 = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    solved_diag_sudoku = {'G7': '8', 'G6': '9', 'G5': '7', 'G4': '3', 'G3': '2', 'G2': '4', 'G1': '6', 'G9': '5',
                          'G8': '1', 'C9': '6', 'C8': '7', 'C3': '1', 'C2': '9', 'C1': '4', 'C7': '5', 'C6': '3',
                          'C5': '2', 'C4': '8', 'E5': '9', 'E4': '1', 'F1': '1', 'F2': '2', 'F3': '9', 'F4': '6',
                          'F5': '5', 'F6': '7', 'F7': '4', 'F8': '3', 'F9': '8', 'B4': '7', 'B5': '1', 'B6': '6',
                          'B7': '2', 'B1': '8', 'B2': '5', 'B3': '3', 'B8': '4', 'B9': '9', 'I9': '3', 'I8': '2',
                          'I1': '7', 'I3': '8', 'I2': '1', 'I5': '6', 'I4': '5', 'I7': '9', 'I6': '4', 'A1': '2',
                          'A3': '7', 'A2': '6', 'E9': '7', 'A4': '9', 'A7': '3', 'A6': '5', 'A9': '1', 'A8': '8',
                          'E7': '6', 'E6': '2', 'E1': '3', 'E3': '4', 'E2': '8', 'E8': '5', 'A5': '4', 'H8': '6',
                          'H9': '4', 'H2': '3', 'H3': '5', 'H1': '9', 'H6': '1', 'H7': '7', 'H4': '2', 'H5': '8',
                          'D8': '9', 'D9': '2', 'D6': '8', 'D7': '1', 'D4': '4', 'D5': '3', 'D2': '7', 'D3': '6',
                          'D1': '5'}

    print(s.__doc__)
    d = s.grid_values(g6)
    d_solved = s.solve(g6)
    print('--')
    print('--Before')
    s.display(s.grid_values(g6,1))
    print('--')
    print('--My solution')
    s.display(d_solved)
    print('--')
    print('--Test solution')
    s.display(solved_diag_sudoku)
    #s.display(s.search(d))
    nt1 = s.naked_twins(d4)
    nt2 = s.naked_twins(d5)
    #print('--After Naked Twins')
    #s.display(nt1)
    #s.display(nt1)
