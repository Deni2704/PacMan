# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""
import sys
from inspect import stack

#from Tools.Scripts.findlinksto import visit

import util
from util import Queue, PriorityQueue


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    from util import Stack
    from game import Directions

    # the component of tree is (state, the path to the state)
    stack = util.Stack() #folosita pentru a stoca starile pe care le exploram
    visited = []
    startNode = (problem.getStartState(), [])  # tuplu din starea initiala si cale care ne-a adus pana la aceasta stare
    stack.push(startNode)
    while not stack.isEmpty():
        popped = stack.pop() # extragem din stiva nodul curent
        location = popped[0]
        path = popped[1]
        if location not in visited:  # In each node we see if it is visited,if it's not then we are getting the successors and push
            visited.append(location)  # its elements to the stack and we are building the path in depth-first logic and way
            if problem.isGoalState(location):
                return path
            successors = problem.getSuccessors(location)
            for suc in list(successors):
                if suc[0] not in visited:
                    stack.push((suc[0], path + [suc[1]]))
    return []
    #util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Stack
    from game import Directions

    # the component of tree is (state, the path to the state)
    queue = util.Queue()
    visited = []  # We are doing the same thing like DFS with the difference that here we are using
    startNode = (
    problem.getStartState(), [])  # queue instead of stack to build the path according to breadth-first logic
    queue.push(startNode)
    while not queue.isEmpty():
        popped = queue.pop()
        location = popped[0]
        path = popped[1]
        if location not in visited:
            visited.append(location)
            if problem.isGoalState(location):
                return path
            successors = problem.getSuccessors(location)
            for suc in list(successors):
                if suc[0] not in visited:
                    queue.push((suc[0], path + [suc[1]]))
    return []

    #util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    #uniform cost este un algoritm de cautare care exploreaza nodurile
    #in functie de costul total al drumului catre acel nod
    from util import Queue
    from game import Directions
    tree  = PriorityQueue() # ordinea de explorare e determinata de costul total al drumului de la start la un nod

    visited = []
    succeded = []
    start = problem.getStartState()
    tree.push((problem.getStartState(), [], 0), 0)
    while not tree.isEmpty():
        (state, path, cost) = tree.pop() # scoatem nodul cu costul minim
        visited.append(state)
        if problem.isGoalState(state):
            return path

        for successor in problem.getSuccessors(state):
            if not successor[0] in visited:
                if (not successor[0] in succeded) or (problem.isGoalState(successor[0])):
                    succeded.append(successor[0])
                    succesorActions = list(path)
                    succesorActions.append(successor[1])
                    successorCost = cost + successor[2]
                    tree.push((successor[0], succesorActions, successorCost), successorCost)
        if problem.isGoalState(state):
            return path
    return path

    #util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    prob = None  # Initialize prob variable
    for check in sys.argv:
        if 'Corners' in check:
            prob = 'Corners'
            break

    tree = PriorityQueue()
    closed = []
    actionList = []
    start = problem.getStartState()
    tree.push((start, actionList), heuristic(start, problem))

    while not tree.isEmpty():
        (node, path) = tree.pop()

        if problem.isGoalState(node):
            return path

        if node not in closed:
            closed.append(node)
            succesors = problem.getSuccessors(node)

            if 'Corners' == prob:
                for successor in succesors:
                    (coord, dir, cost) = successor
                    nextActions = path + [dir]  # Adding the direction as an element to the path list
                    nextCost = problem.getCostOfActions(path) + successor[2] + heuristic(coord, problem)
                    tree.push((coord, nextActions), nextCost)
            else:
                for successor in succesors:
                    tree.push((successor[0], path + [successor[1]]),  # Adding successor[1] as a list element
                              problem.getCostOfActions(path) + successor[2] + heuristic(successor[0], problem))

    return []

    #util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
