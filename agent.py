import random
import constants as c
import time
from sklearn.neural_network import MLPClassifier

# Pickle for serielizing data and re-adding
# Save and plot average fittness over generations? (Get an A)

class Agent:
    def __init__(self, gGrid, waitTime=0.1):
        self.waitTime = waitTime
        self.myGrid = gGrid
        print("__init__ not defined for abstract Agent")

    # This function is to be populated with code for the agent to respond to a new board being given after an update and will trigger a command.
    def promptAgent(self, currentMatrix):
        print("__init__ not defined for promptAgent method in abstract Agent")

    def getCurrMat(self):
        return self.myGrid.matrix

    def pressKey(self, key):
        time.sleep(self.waitTime)
        self.myGrid.key_down_str(key)

    def checkMoveValid(self, move):
        _, done = self.myGrid.getCommand(move)(self.getCurrMat())
        return done


class RandomAgent(Agent):
    def __init__(self, gGrid, waitTime=0.1):
        #super(RandomAgent, self)._init__(self, waitTime=waitTime)
        self.waitTime = waitTime
        self.myGrid = gGrid
        # self.keyboard = Controller()

    def promptAgent(self):
        done = False
        count = 0
        while not done:
            choice = random.choices([c.KEY_UP_AGENT, c.KEY_DOWN_AGENT, c.KEY_LEFT_AGENT, c.KEY_RIGHT_AGENT], weights=[0.25, 0.25, 0.25, 0.25])[0]
            # print("Temp choice: ", choice)
            count += 1
            done = self.checkMoveValid(choice)

            # If I have lost
            if count > 4:
                # do something
                # print("I've lost")
                #############################
                print("########Last Resort!!!!!!")
                self.myGrid.after(20, self.myGrid.task)
                # time.sleep(1)
                #############################
                break

        # print("Random agent choice: ", choice)
        self.pressKey(choice)



class PatternAgentULRD(Agent):
    def __init__(self, gGrid, waitTime=0.1):
        #super(RandomAgent, self)._init__(self, waitTime=waitTime)
        self.waitTime = waitTime
        self.myGrid = gGrid
        # self.keyboard = Controller()

    def promptAgent(self):

        done = False
        # Always try up first
        choice = c.KEY_UP_AGENT
        if not self.checkMoveValid(choice):
            # Always try left second
            choice = c.KEY_LEFT_AGENT
            if not self.checkMoveValid(choice):
                # Always try right third
                choice = c.KEY_RIGHT_AGENT
                if not self.checkMoveValid(choice):
                    # Always try left last
                    choice = c.KEY_DOWN_AGENT
        # print("Random agent choice: ", choice)
        self.pressKey(choice)

class PatternAgentLURD(Agent):
    def __init__(self, gGrid, waitTime=0.1):
        #super(RandomAgent, self)._init__(self, waitTime=waitTime)
        self.waitTime = waitTime
        self.myGrid = gGrid
        # self.keyboard = Controller()

    def promptAgent(self):

        done = False
        # Always try up first
        choice = c.KEY_LEFT_AGENT
        if not self.checkMoveValid(choice):
            # Always try left second
            choice = c.KEY_UP_AGENT
            if not self.checkMoveValid(choice):
                # Always try right third
                choice = c.KEY_RIGHT_AGENT
                if not self.checkMoveValid(choice):
                    # Always try left last
                    choice = c.KEY_DOWN_AGENT
        # print("Random agent choice: ", choice)
        self.pressKey(choice)

class ManualAgent(Agent):
    def __init__(self, gGrid, waitTime=0.1):
        #super(RandomAgent, self)._init__(self, waitTime=waitTime)
        self.waitTime = waitTime
        self.myGrid = gGrid

    def promptAgent(self):
        print("Wait for user input")


class DNNAgent(Agent):
    def __init__(self, gGrid, waitTime=0.1, trainName=None):
        self.waitTime = waitTime
        self.myGrid = gGrid

        # Init neural net
        # Number and size of hidden layers
        self.size = [32]
        # Using "relu" activation function, a standard in the industry
        self.mlp = MLPClassifier(hidden_layer_sizes=self.size, activation='relu')
        self.xTrain, self.yTrain = self.getTrains(trainName)
        self.mlp.fit(self.xTrain, self.yTrain)


    def promptAgent(self):
        # Get list form of matrix
        inMat = self.convMat1x16(self.getCurrMat())
        # Input matrix into mlp
        choice = self.convDirCode(self.mlp.predict(inMat))

        while self.checkMoveValid(choice):
            choice = random.choices([c.KEY_UP_AGENT, c.KEY_DOWN_AGENT, c.KEY_LEFT_AGENT, c.KEY_RIGHT_AGENT], weights=[0.25, 0.25, 0.25, 0.25])[0]
        print(choice)
        self.pressKey(choice)


    def getTrains(self, trainName):
        if trainName == None:
            print("Use Default Train Data")
            # A non-working base xTrain set
            xTrain = [[0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0], [0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0]]
            # The yTrain dataset and all of the possible output's it contains is the only source for output labels
            yTrain = [3, 0, 1, 2]
            return(xTrain, yTrain)
        else:
            print("Have Train Data")

    def convMat1x16(self, mat):
        outMat1x16 = []
        for i in range(4):
            for j in range(4):
                outMat1x16.append(mat[i][j])
        print(outMat1x16)
        # Weird thing, need to return the single list in a list of lists
        return [outMat1x16]

    def convDirCode(self, code):
        if code == c.UP_CODE:
            return c.KEY_UP_AGENT
        elif code == c.RIGHT_CODE:
            return c.KEY_RIGHT_AGENT
        elif code == c.DOWN_CODE:
            return c.KEY_DOWN_AGENT
        elif code == c.LEFT_CODE:
            return c.KEY_LEFT_AGENT


