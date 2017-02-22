# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?
A: A naked twin is a situation in an unsolved Sudoku puzzle when more than
   one box in a unit (a column, a row or a square of 9 boxes) has exactly
   the same two digits. Under such a situation, it is a safe assumption that
   no other unsolved box in the same unit can have the same digits as the
   ones in the naked twins box. Therefore once we identify if a column, row
   or a square has naked twins, we need to iterate over all other boxes in
   the same column/row/square to eliminate matching digits of the naked twins.
   The concept is extendable to more than two matches - to triples, quadruples etc.
   In our implementation, we iterate over a column/row/square at a time to find
   _unsolved_ boxes that match exactly with other boxes. These digits _must_ only
   be placed in the exactly matching boxes, therefore any other non-fully matching
   box can exclude matching digits.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?
A: A diagnol sudoku is a sudoku with an additional constraint that a diagnol must
   only have digits 1-9. In an unsolved sudoku, for all boxes which are yet to be
   solved, we start with all possible answers 1-9 and then apply the constraint
   that for any box in the diagnol, if we have a solution, then the digit represented
   by the solved box can be eliminated from the unsolved box. After the first step, if
   unsolved boxes have a digit that is only represented once, then it must be the solution
   for that box as that digit is not represented by any other box in the diagnol. The above
   two constraints can be iteratively used till a solution is found.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged
Python distribution that contains all of the necessary libraries and software for this project.
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed
our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using
the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.