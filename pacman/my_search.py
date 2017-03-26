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
    levl     = 0;     # Number of levels to get to the current state from the root node

    # Initialization
    def __init__(self, s, p, a, c, l):
        self.state   = s
        self.parent  = p
        self.action  = a
        self.cost    = c
        self.levl    = l

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
            print('y_root::state:', self.state)
        else:
            print('n_root::state:', self.state, \
                  'p_state:'      , self.parent.state, \
                  'action:'       , self.action, \
                  'level:'        , self.levl)

class GenericSearch:
    '''
    This class implements a generic search algorithm. It can
    then be tailored to DFS, BFS, A* by taking input a parameter
    '''
    def gen_root_node(self, st):
        '''
        This method is used to generate the root node given
        the starting state of a search problem
        '''
        return Node(st, None, None, 0, 0)

    def gen_node(self, p, s):
        '''
        This method is used to generate a node from a successor. The
        successor is a tuple of (state, action/direction, cost). This
        method also takes the parent node as an argument
        '''
        # Calculate the total cost for the new node
        total_cost = p.cost + s[2]
        total_levl = p.levl + 1
        return Node(s[0], p, s[1], total_cost, total_levl)

    def search(self, problem):
        '''
        The input to this function is a search problem, which
        defines a starting state, a goal state and a list of
        possible actions given the current state. Our goal is to
        generate a list of actions that can get us from the start
        state to the goal state
        '''
        # Generate my root node
        root_node = self.gen_root_node(problem.getStartState())
        # Initialize the frontier list to be pointing to the start
        # state where we being our search. Note that typically we will
        # never be asked to search if we are already at the goal state, so
        # no need to perform that check here
        frontier = [root_node]
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
            assert len(frontier)
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
                    frontier.append(self.gen_node(current_node, s))

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
    # Instantiate the search algorithm
    salgo = GenericSearch()
    # Solve the problem and print the solution
    solution = salgo.search(sprob)
    print('Size:', sprob.grid_size, 'Start:', sprob.strt_state, 'Goal:', sprob.goal_state)
    print(solution)
