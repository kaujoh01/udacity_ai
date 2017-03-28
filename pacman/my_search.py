# Imports
from util import Stack
from util import Queue
from util import PriorityQueue

class Node:
    '''
    This class is used to hold the key information about a node. The node
    contains a current status which indicates the coordinates of the current
    location. It contains the cost of getting from the starting state to
    the current state. It will hold a pointer to the parent node. The idea
    is that by traversing all the way back to the root node via the parent
    nodes, we can get the direction from the root node to the current node
    '''
    # Variables
    state    = ();    # Uninitialized tuple which holds the current state
    parent   = None;  # A pointer to the parent node
    action   = None;  # The action it took to get to this state
    cost     = 0;     # Total cost to get to the current status from the root node
    heur     = 0;     # Total cost plus a heuristic to goal state

    # Initialization
    def __init__(self, s, p, a, c, h):
        self.state   = s
        self.parent  = p
        self.action  = a
        self.cost    = c
        self.heur    = h

    # Check if this is a root node
    def is_root(self):
        return self.parent==None

    # Get path from root to the current node
    def get_path_from_root(self):
        # Check that a parent exists, otherwise we can never
        # generate a path from root
        assert self.parent
        # Recursively call all parents to start generating
        # a list of all actions
        if self.parent.is_root():
            return [self.action]
        else:
            return self.parent.get_path_from_root() + [self.action]

    # Print properties of a node
    def print_props(self):
        if self.is_root():
            print('y_root::state:', self.state,        \
                  'cost:'         , self.cost,         \
                  'heur:'         , self.heur,         \
                  '::')
        else:
            print('n_root::state:', self.state,        \
                  'p_state:'      , self.parent.state, \
                  'action:'       , self.action,       \
                  'cost:'         , self.cost,         \
                  'heur:'         , self.heur,         \
                  '::')
class GenericSearch:
    '''
    This class implements a generic search algorithm. It can
    then be tailored to DFS, BFS, A* by taking input a parameter
    '''

    # Variables
    search_type = 'DFS'

    def __init__(self, s_type='DFS'):
        '''
        Initialize the type of search that is needed. The options are:
          o DFS - Depth first search
          o BFS - Breath first search
          o Astar
        '''
        self.search_type = s_type

    def get_hypotenuse(self, curr_st, goal_st):
        '''
        This method is used to get a hypotenuse distance between
        the current state and the goal
        '''
        c_x, c_y = curr_st
        g_x, g_y = goal_st
        hyp = ( ((c_x-g_x)**2) + ((c_y-g_y)**2) )**0.5
        # REVISIT: Add a correction to avoid same priorities
        if (c_x-g_x)==0:
            hyp = hyp - 0.5
        return hyp

    def gen_root_node(self, st, g_st):
        '''
        This method is used to generate the root node given
        the starting state of a search problem
        '''
        hyp = self.get_hypotenuse(st, g_st)
        return Node(st, None, None, 0, hyp)

    def gen_node(self, p, s, g_st):
        '''
        This method is used to generate a node from a successor. The
        successor is a tuple of (state, action/direction, cost). This
        method also takes the parent node as an argument
        '''
        # Calculate the total cost for the new node
        total_cost = p.cost + s[2]
        total_heur = p.cost + s[2] + self.get_hypotenuse(s[0], g_st)
        return Node(s[0], p, s[1], total_cost, total_heur)

    def search(self, problem):
        '''
        The input to this function is a search problem, which
        defines a starting state, a goal state and a list of
        possible actions given the current state. Our goal is to
        generate a list of actions that can get us from the start
        state to the goal state
        '''
        # Generate the root node
        root_node = self.gen_root_node(problem.getStartState(), problem.goal)

        # Check that the search type is from a list of supported
        # ones
        assert                         \
            self.search_type=='DFS' or \
            self.search_type=='BFS' or \
            self.search_type=='Astar'

        # Initialize the frontier depending on the search type
        frontier = None
        if self.search_type == 'DFS':
            frontier = Stack()
        if self.search_type == 'BFS':
            frontier = Queue()
        if self.search_type == 'Astar':
            frontier = PriorityQueue()

        # Initialize the frontier list to be pointing to the start
        # state where we being our search. Note that typically we will
        # never be asked to search if we are already at the goal state, so
        # no need to perform that check here
        frontier.push(root_node, root_node.cost)
        search_iter = 0
        # Initialize the explored states to null, which is a dictionary. The
        # reason why we choose a dictionary is to be able to do a hash lookup
        # of a state to see if it exists or not
        explored_states = {}
        # Run an infinite loop till we solve our problem.
        while 1:
            # In order to not get genuinely stuck in an
            # infinite loop, terminate if the search has iterated for
            # too long
            search_iter +=1
            assert search_iter<1000
            # Catch illegal draining of frontiers before we have
            # found a solution
            assert not frontier.isEmpty()
            # Extract the current node based on search parameter
            # from the frontier to determine if we have found our
            # goal
            current_node  = frontier.pop()
            current_state = current_node.state
            # Push this frontier to the explored state
            explored_states[current_state] = 1
            # Check if the current node is our goal, if so, then
            # return the path from root to the goal.
            if problem.isGoalState(current_state):
                return current_node.get_path_from_root()
            # If we haven't reached our goal, then generate all
            # the successors for my frontier
            for s in problem.getSuccessors(current_state):
                if s[0] not in explored_states.keys():
                    new_node = self.gen_node(current_node, s, problem.goal)
                    frontier.push(new_node, new_node.heur)

class LazySearchProblem:
    '''
    This class is used to create a search problem to check that our
    search algorithm can find a goal given a reasonable problem construction.
    '''

    # Imports
    #from random import randint

    # Variables
    strt_state = None
    goal_state = None
    grid_size  = None
    goal       = None # Alias to goal_state

    # Initialization
    def __init__(self):
        # Imports
        from random import randint
        # Always generate a square grid
        self.grid_size  = randint(2,10)
        self.strt_state = (randint(0,self.grid_size-1),randint(0,self.grid_size-1))
        # Note that we can in rare occasions generate a goal that
        # is also the starting state. This is useful to check our search
        # doesn't die horribly
        self.goal_state = (randint(0,self.grid_size-1),randint(0,self.grid_size-1))
        self.goal = self.goal_state

    def getStartState(self):
        '''
        Returns the start state for the search problem
        '''
        return self.strt_state

    def isGoalState(self, s):
        '''
        state: Search state
        Returns True if and only if the state is a valid goal state
        '''
        return s==self.goal_state

    def getSuccessors(self, s):
        '''
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        '''
        # We generate successors in all four directions as long as
        # we don't go outside of the grid. The definition of outside
        # of the grid is if one of the axis turns negative
        x, y = s
        successors = []
        for i in ['N', 'S', 'E', 'W']:
            if i=='N' and y+1<=self.grid_size-1:
                successors.append([(x,y+1), 'N', 1])
            if i=='S' and y-1>=0:
                successors.append([(x,y-1), 'S', 1])
            if i=='E' and x+1<=self.grid_size-1:
                successors.append([(x+1,y), 'E', 1])
            if i=='W' and x-1>=0:
                successors.append([(x-1,y), 'W', 1])
        return successors

# Main
if __name__ == '__main__':
    # Instantiate a new search problem
    sprob = LazySearchProblem()
    print('Size:', sprob.grid_size, 'Start:', sprob.strt_state, 'Goal:', sprob.goal_state)
    # Instantiate the search algorithm
    salgo = GenericSearch('BFS')
    # Solve the problem and print the solution
    solution = salgo.search(sprob)
    print(solution)
