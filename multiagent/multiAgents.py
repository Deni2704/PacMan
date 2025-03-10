# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        Food = newFood.asList()
        gPos = successorGameState.getGhostPositions()  ###We have the position of the food and the ghost positions
        FoodDist = []  ###We have the distance between the pacman,the food and the ghost
        GhostDist = []

        for food in Food:
            FoodDist.append(manhattanDistance(food, newPos))
        for ghost in gPos:
            GhostDist.append(manhattanDistance(ghost, newPos))

        if currentGameState.getPacmanPosition() == newPos: #daca nu se misca
            return (-(float("inf")))

        for dist in GhostDist:  ###If the ghost is too near(next to pacman) we return(-float("inf")) like we have lost
            if dist < 2:
                return (-(float("inf")))  ###When there is no food left we return float("inf") like we have won
        if len(FoodDist) == 0:  ##Finally we return 1000/sum(FoodDist) + 10000/len(FoodDist) as the evaluation of the state
            return float(
                "inf")  ###It is not necessary that we put 1000 or 10000 ,the only need is to be large enough contrary to sum(foodDist)
            ###and len(foodDist) respectively
        return 1000 / sum(FoodDist) + 10000 / len(FoodDist)
    # fololsim 1000/sum(FoodDIST) daca suma distantelor catre mancare este mica si 10000/len da un scor mare daca sunt putine bucati de mancare


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        def minimax(agentIndex, depth, gameState):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState), None
            if agentIndex == 0:  # Pacman
                return max_value(agentIndex, depth, gameState)
            else:  # Ghosts
                return min_value(agentIndex, depth, gameState)

        def max_value(agentIndex, depth, gameState):
            bestScore = float('-inf')
            bestAction = None
            for action in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, action)
                score, _ = minimax(agentIndex + 1, depth, successor)
                if score > bestScore:
                    bestScore, bestAction = score, action
            return bestScore, bestAction

        def min_value(agentIndex, depth, gameState):
            bestScore = float('inf')
            bestAction = None
            nextAgent = agentIndex + 1
            if agentIndex == gameState.getNumAgents() - 1: #daca agentul curent este utlimul vom trece la agentul 0 si vom incrementa adancimea
                nextAgent, depth = 0, depth + 1

            for action in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, action)
                score, _ = minimax(nextAgent, depth, successor)
                if score < bestScore:
                    bestScore, bestAction = score, action
            return bestScore, bestAction

        _, action = minimax(0, 0, gameState)
        return action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        # alpha beta pruning elimina ramurile care nu pot influenta decizia finala
        # daca in orice moment, valoarea unui nod este mai mare decat beta ( in cazul min) sau mai mica decat alpha in cazukl max, ramura nu mai are nevoie sa fie explorata
        def minimax(agentIndex, depth, gameState, alpha, beta):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState), None

            if agentIndex == 0:  # Pacman (Maximizer)
                return max_value(agentIndex, depth, gameState, alpha, beta)
            else:  # Ghosts (Minimizers)
                return min_value(agentIndex, depth, gameState, alpha, beta)

        def max_value(agentIndex, depth, gameState, alpha, beta):
            """
              Compute the maximum value for Pacman and perform alpha-beta pruning.
            """
            bestScore = float('-inf')
            bestAction = None
            legalActions = gameState.getLegalActions(agentIndex)

            if not legalActions:
                return self.evaluationFunction(gameState), None

            for action in legalActions:
                successor = gameState.generateSuccessor(agentIndex, action)
                score, _ = minimax(1, depth, successor, alpha, beta)  # Next agent is the first ghost
                if score > bestScore:
                    bestScore, bestAction = score, action
                if bestScore > beta:
                    return bestScore, bestAction  # Prune
                alpha = max(alpha, bestScore)
          # daca alpha devine mai mare decat beta ramura repsectiva va fi taiata deoarece fantoma nu va permite niciodata ca scorul sa fie mai mare decat beta
            return bestScore, bestAction

        def min_value(agentIndex, depth, gameState, alpha, beta):
            """
              Compute the minimum value for a ghost and perform alpha-beta pruning.
            """
            bestScore = float('inf')
            bestAction = None
            legalActions = gameState.getLegalActions(agentIndex)
            numAgents = gameState.getNumAgents()

            if not legalActions:
                return self.evaluationFunction(gameState), None

            for action in legalActions:
                successor = gameState.generateSuccessor(agentIndex, action)
                if agentIndex == numAgents - 1:  # Last ghost
                    score, _ = minimax(0, depth + 1, successor, alpha, beta)  # Next agent is Pacman
                else:
                    score, _ = minimax(agentIndex + 1, depth, successor, alpha, beta)  # Next ghost
                if score < bestScore:
                    bestScore, bestAction = score, action
                if bestScore < alpha:
                    return bestScore, bestAction  # Prune
                beta = min(beta, bestScore)
           #daca beta devine mai mic decat alpha ramura respectiva e taiata deoarece pacman nu va permite niciodata ca scorul sa fie mai mic decat alpha
            return bestScore, bestAction

        alpha = float('-inf')
        beta = float('inf')


        _, action = minimax(0, 0, gameState, alpha, beta)
        return action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        def expectimax(agentIndex, depth, gameState):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState), None

            if agentIndex == 0:  # Pacman
                return max_value(agentIndex, depth, gameState)
            else:  # Ghosts
                return exp_value(agentIndex, depth, gameState)

        def max_value(agentIndex, depth, gameState):
            bestScore = float('-inf')
            bestAction = None
            for action in gameState.getLegalActions(agentIndex):
                successor = gameState.generateSuccessor(agentIndex, action)
                score, _ = expectimax(1, depth, successor)
                if score > bestScore:
                    bestScore, bestAction = score, action
            return bestScore, bestAction
          #acum fantomele nu mai aleg cea mai mica valoarea, ci aleg pe baza unei distributii de probabilitate
        def exp_value(agentIndex, depth, gameState):
            totalScore = 0
            actions = gameState.getLegalActions(agentIndex)\

            probability = 1.0 / len(actions)
            for action in actions:
                successor = gameState.generateSuccessor(agentIndex, action)
                nextAgent = (agentIndex + 1) % gameState.getNumAgents()
                nextDepth = depth + 1 if agentIndex == gameState.getNumAgents() - 1 else depth
                #determinam urmatorul agent care va juca si daca trebuie sa trecem la un nou nivel de adancime
                score, _ = expectimax(nextAgent, nextDepth, successor)
                totalScore += score * probability
                #scorul ponderat al actiunii curente
            return totalScore, None

        _, action = expectimax(0, 0, gameState)
        return action
def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pacPosition = currentGameState.getPacmanPosition()  ###Now we do not want only the pacman,the food and the ghost positions
    gList = currentGameState.getGhostStates()  ###but also the capsules
    Food = currentGameState.getFood()
    Capsules = currentGameState.getCapsules()

    if currentGameState.isWin():
        return float("inf")
    if currentGameState.isLose():
        return float("-inf")

    foodDistList = []
    for food in Food.asList():
        foodDistList += [util.manhattanDistance(food, pacPosition)]
    minFDist = min(foodDistList)  ###We have a better evaluation function,what it means?
    GhDistList = []  ###It means that we have take into account more parameters in order to have a better evalution function
    ScGhDistList = []  ###Of course every parameter has its own "gravity,importance" like chess the strategical advantages
    for ghost in gList:  ###are less important than the tactical,material ones
        if ghost.scaredTimer == 0:
            GhDistList += [util.manhattanDistance(pacPosition, ghost.getPosition())]
        elif ghost.scaredTimer > 0:
            ScGhDistList += [util.manhattanDistance(pacPosition, ghost.getPosition())]
    minGhDist = -1
    if len(GhDistList) > 0:
        minGhDist = min(
            GhDistList)  # We have the min distance of a ghost,the min distance of a scaredGhost,the amount of the capsules,the food and the min distance of a food.
    minScGhDist = -1  # As we see they do not hve all the same role-importance in the estimation -evaluation of a state
    if len(ScGhDistList) > 0:
        minScGhDist = min(ScGhDistList)
    score = scoreEvaluationFunction(currentGameState)
    score -= 1.5 * minFDist + 2 * (1.0 / minGhDist) + 2 * minScGhDist + 20 * len(Capsules) + 4 * len(Food.asList())
    return score
# Mancarea: Apropierea fata de mancare (minFDist) este importanta pentru ca Pacman trebuie sa o consume.
#Fantome active: Distanta minima catre fantomele active (1.0 / minGhDist) este importanta pentru a evita moartea.Coeficient: 2  foarte important sa evite coliziunea.
#Fantome speriate: Apropierea de fantomele speriate (minScGhDist) este benefica pentru ca le poate manca.
##Capsule: Numarul de capsule ramase (len(Capsules)) are un impact major asupra jocului.Coeficient: 20  foarte important sa le consume pentru a activa starea speriata a fantomelor
#Mancarea ramasa: Numarul total de alimente ramase (len(Food.asList())) determina progresul spre victorie
# Abbreviation
better = betterEvaluationFunction

