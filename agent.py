import random
import constants as c
import time
from sklearn.neural_network import MLPClassifier
import pickle

# Pickle for serielizing data and re-adding
# Save and plot average fittness over generations? (Get an A)

class Agent:
    def __init__(self, gGrid, waitTime=0.1, gameSessionFile=None):
        self.waitTime = waitTime
        self.myGrid = gGrid
        self.gameSessionFile = gameSessionFile
        # print("__init__ not defined for abstract Agent")

        self._moveID = 0
        self._matRecord = []
        self._moveRecord = []
        self._score = None

    def setGameGrid(self, gameGrid):
        self.myGrid = gameGrid


    # This function is to be populated with code for the agent to respond to a new board being given after an update and will trigger a command.
    def promptAgent(self, currentMatrix):
        print("__init__ not defined for promptAgent method in abstract Agent")

    # Retrieve the current game board
    def getCurrMat(self):
        return self.myGrid.matrix

    # Simulate a key press
    def pressKey(self, key):
        time.sleep(self.waitTime)
        self.myGrid.key_down_str(key)

    # Check if the desired move is a valid move that cam be made
    def checkMoveValid(self, move):
        _, done = self.myGrid.getCommand(move)(self.getCurrMat())
        return done

    # Increment the move ID
    def incrementMoveID(self):
        self._moveID += 1

    # Add a move to the move record
    def appendMove(self, move):
        self._matRecord.append(self.convMat1x16(self.getCurrMat()))
        self._moveRecord.append(self.convDirToDirCode(move))
        self.incrementMoveID()

    # Method packages the game data with pickle
    def pikPakGame(self):
        xAll = self._matRecord
        yAll = self._moveRecord
        # print("write data")
        # print(xAll)
        # print(yAll)
        # print(self._score)
        with open('train.pickle', 'wb') as f:
            pickle.dump((xAll, yAll, self._score), f)

    # Set the game score (to be included in pickle file)
    def setScore(self, score):
        self._score = score

    def getScore(self):
        return self._score

    def getGameRecord(self):
        return (self._matRecord, self._moveRecord, self._score)

    # Convert a 4x4 board matrix into a 1X16 matrix
    def convMat1x16(self, mat):
        outMat1x16 = []
        for i in range(4):
            for j in range(4):
                outMat1x16.append(mat[i][j])
        # print(outMat1x16)
        # Weird thing, need to return the single list in a list of lists
        return outMat1x16

    # Convert a direction code (0 -3) to a key direction
    def convDirCodeToDir(self, code):
        if code == c.UP_CODE:
            return c.KEY_UP_AGENT
        elif code == c.RIGHT_CODE:
            return c.KEY_RIGHT_AGENT
        elif code == c.DOWN_CODE:
            return c.KEY_DOWN_AGENT
        elif code == c.LEFT_CODE:
            return c.KEY_LEFT_AGENT

    def convDirToDirCode(self, dir):
        if dir == c.KEY_UP_AGENT:
            return c.UP_CODE
        elif dir == c.KEY_RIGHT_AGENT:
            return c.RIGHT_CODE
        elif dir == c.KEY_DOWN_AGENT:
            return c.DOWN_CODE
        elif dir == c.KEY_LEFT_AGENT:
            return c.LEFT_CODE




class RandomAgent(Agent):
    def __init__(self, gGrid, waitTime=0.1, gameSessionFile=None):
        super().__init__(gGrid, waitTime=waitTime, gameSessionFile=gameSessionFile)


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
                # print("########Last Resort!!!!!!")
                self.myGrid.after(20, self.myGrid.task)
                # time.sleep(1)
                #############################
                break

        # print("Random agent choice: ", choice)
        self.appendMove(choice)
        self.pressKey(choice)



class PatternAgentULRD(Agent):
    def __init__(self, gGrid, waitTime=0.1, gameSessionFile=None):
        super().__init__(gGrid, waitTime=waitTime, gameSessionFile=gameSessionFile)

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
        self.appendMove(choice)
        self.pressKey(choice)

class PatternAgentLURD(Agent):
    def __init__(self, gGrid, waitTime=0.1, gameSessionFile=None):
        super().__init__(gGrid, waitTime=waitTime, gameSessionFile=gameSessionFile)

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
        self.appendMove(choice)
        self.pressKey(choice)

class ManualAgent(Agent):
    def __init__(self, gGrid, waitTime=0.1, gameSessionFile=None):
        super().__init__(gGrid, waitTime=waitTime, gameSessionFile=gameSessionFile)

    def promptAgent(self):
        print("Wait for user input")


class DNNAgent(Agent):
    def __init__(self, gGrid, waitTime=0.1, gameSessionFile=None, trainName=None, trainData=None):
        super().__init__(gGrid, waitTime=waitTime, gameSessionFile=gameSessionFile)

        # Init neural net
        # Number and size of hidden layers
        self.size = [32, 8]
        # Using "relu" activation function, a standard in the industry
        self.mlp = MLPClassifier(hidden_layer_sizes=self.size, activation='relu')
        if trainName != None and trainData == None:
            self.xTrain, self.yTrain = self.getTrainsFromFile(trainName)
            self.fitModel(self.xTrain, self.yTrain)
        elif trainName == None and trainData != None:
            self.xTrain, self.yTrain = self.getTrainsFromDataSet(trainData)
            self.fitModel(self.xTrain, self.yTrain)
        else:
            print("Specified both train data file and data set, please only pass one of the two")

    def fitModel(self, xTrain, yTrain):
        self.mlp.fit(xTrain, yTrain)

    def promptAgent(self):
        # Get list form of matrix
        inMat = [self.convMat1x16(self.getCurrMat())]
        # Input matrix into mlp
        pred = self.mlp.predict(inMat)
        # print(pred)
        choice = self.convDirCodeToDir(pred)
        # print(choice)

        while not self.checkMoveValid(choice):
            # print("Move ", choice, " was not valid. Getting new choice")
            choice = random.choices([c.KEY_UP_AGENT, c.KEY_DOWN_AGENT, c.KEY_LEFT_AGENT, c.KEY_RIGHT_AGENT], weights=[0.25, 0.25, 0.25, 0.25])[0]

        # print(choice)
        self.appendMove(choice)
        self.pressKey(choice)


    def getTrainsFromFile(self, trainName):
        if trainName != None:
            # xTrain, yTrain = []
            with open(trainName, 'rb') as f:
                (xTrain, yTrain, score) = pickle.load(f)
            # print("Have Train Data")
            # print(xTrain)
            # print(yTrain)
            return (xTrain, yTrain)
        else:
            print("No train file")

    def getTrainsFromDataSet(self, trainData):
        if trainData != None:
            # xTrain, yTrain = []
            # Data is in the form: (epochNum, itterNum, boards, moves, score)
            xTrain = []
            yTrain = []
            for i in range(0, len(trainData)):
                (_, _, xArr, yArr, _) = trainData[i]
                xTrain.append(xArr[0])
                yTrain.append(yArr[0])
            # print("Have Train Data")
            # print(xTrain)
            # print(yTrain)
            return (xTrain, yTrain)
        else:
            print("No train dataset")