import random
import constants as c
import time
from sklearn.neural_network import MLPClassifier
import pickle
import numpy as np

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

    def reset(self):
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
        if (self.checkMoveValid(move)):
            self._matRecord.append(self.convMat1x16(self.getCurrMat()))
            self._moveRecord.append(self.convDirToDirCode(move))
            self.incrementMoveID()

    # Method packages the game data with pickle
    def pikPakGame(self):
        print("PIKPAK")
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
        print(self._moveID)
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
    def __init__(self, gGrid, waitTime=0.1, gameSessionFile=None, trainName=None, trainData=None, trainDataPickle=None):
        super().__init__(gGrid, waitTime=waitTime, gameSessionFile=gameSessionFile)

        # Init neural net
        # Number and size of hidden layers
        self.size = [64]
        # Using "relu" activation function, a standard in the industry
        # self.mlp = MLPClassifier(hidden_layer_sizes=self.size, activation='relu', max_iter=700)
        self.mlp = MLPClassifier(hidden_layer_sizes=self.size, activation='relu', max_iter=700)
        print("Start Training")
        if trainData == None and trainName == None and trainDataPickle == None:
            self.xTrain, self.yTrain = self.getTrainsFromFile("random_train.pickle")
            print("Fitting Model")
            self.fitModel(self.xTrain, self.yTrain)
        elif trainName != None and trainData == None:
            self.xTrain, self.yTrain = self.getTrainsFromFile(trainName)
            print("Fitting Model")
            self.fitModel(self.xTrain, self.yTrain)
        elif trainName == None and trainData != None:
            self.xTrain, self.yTrain = self.getTrainsFromDataSet(trainData)
            self.fitModel(self.xTrain, self.yTrain)
        elif trainDataPickle != None:
            self.xTrain, self.yTrain = self.getTrainsFromPickleData(trainDataPickle, 20)
            self.fitModel(self.xTrain, self.yTrain)
            #########################
            # with open('ULRD_trained_model_20_game_layers_16.pickle', 'wb') as f:
            #     pickle.dump(self.mlp, f)
            #########################
        else:
            print("Specified both train data file and data set, please only pass one of the two")

        print("Training Finished")

    def fitModel(self, xTrain, yTrain):
        self.mlp.fit(xTrain, yTrain)

    def promptAgent(self):
        # Get list form of matrix
        inMat = [self.convMat1x16(self.getCurrMat())]
        # Input matrix into mlp
        pred = self.mlp.predict(inMat)
        probs = np.asarray(self.mlp.predict_proba(inMat))
        opts = np.asarray(self.mlp.classes_)
        predInd = np.where(opts==pred)[0][0]

        # print("Opts before:", opts)
        opts = np.delete(opts, predInd)
        # print("Opts after:", opts)

        # print("Probs before:", probs)
        probs = np.delete(probs, predInd)
        # print("Probs after:", probs)

        choice = self.convDirCodeToDir(pred)
        while not self.checkMoveValid(choice) and not probs.size == 0 and not opts.size == 0:
            # print("Move ", choice, " was not valid. Getting new choice")
            maxProb = np.argmax(probs)
            # print("Max Prob: ", maxProb)
            pred = opts[maxProb]
            choice = self.convDirCodeToDir(pred)
            # print("New Choice: ", choice)

            # print("Opts before:", opts)
            opts = np.delete(opts, maxProb)
            # print("Opts after:", opts)

            # print("Probs before:", probs)
            probs = np.delete(probs, maxProb)
            # print("Probs after:", probs)

        # print("Choice Confirmed: ", choice)
        self.appendMove(choice)
        self.pressKey(choice)


    def getTrainsFromFile(self, trainName):
        if trainName != None:
            # xTrain, yTrain = []
            with open(trainName, 'rb') as f:
                (xTrain, yTrain, score) = pickle.load(f)
            # print("Have Train Data")
            xTrain.append([0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            xTrain.append([0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            xTrain.append([0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            xTrain.append([0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0])

            yTrain.append(0)
            yTrain.append(1)
            yTrain.append(2)
            yTrain.append(3)
            # print(xTrain)
            # print(yTrain)
            return (xTrain, yTrain)
        else:
            print("No train file")

    # Data is in the form: (epochNum, itterNum, boards, moves, score)
    def getTrainsFromPickleData(self, trainName, limit):
        if trainName != None:
            # xTrain, yTrain = []
            with open(trainName, 'rb') as f:
                dataFromPickle = pickle.load(f)
            # print("Have Train Data")
            xTrain = [[2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2], [2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2], [2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2], [2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2]]
            yTrain = [0, 1, 2, 3]

            limit = min(limit, len(dataFromPickle))
            # limit = min(1, len(dataFromPickle))
            print("Training on ", limit, " games")
            for i in range(0, limit):
                (_, _, xArr, yArr, score) = dataFromPickle[i]
                print("Game has ", len(yArr), " moves to achive score ", score)
                # print(xArr)
                print(yArr)
                for xData in xArr:
                    xTrain.append(xData)
                    # print("Putting X: ", xData)
                for yData in yArr:
                    yTrain.append(yData)
                    # print("Putting Y: ", yData)
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
            xTrain = [[0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
            yTrain = [0, 1, 2, 3]
            # xTrain = []
            # yTrain = []
            # print(trainData)
            # print(len(trainData))
            for i in range(0, len(trainData)):
                (_, _, xArr, yArr, _) = trainData[i]
                for xData in xArr:
                    xTrain.append(xData)
                    # print("Putting X: ", xData)
                for yData in yArr:
                    yTrain.append(yData)
                    # print("Putting Y: ", yData)
            # print("Have Train Data")
            # print(xTrain)
            # print(yTrain)
            return (xTrain, yTrain)
        else:
            print("No train dataset")


# class ExistingAgent(Agent):
#     def __init__(self, gGrid, existingModelPickle, waitTime=0.1, gameSessionFile=None):
#         self.agent = None
#         with open(existingModelPickle, 'rb') as f:
#             self.agent = pickle.load(f)
#         self.agent.setGameGrid(gGrid)
#         self.agent.waitTime = waitTime
#         self.agent.gameSessionFile = gameSessionFile
#
#     def promptAgent(self):
#         self.agent.promptAgent()
#
#     # Retrieve the current game board
#     def getCurrMat(self):
#         return self.agent.myGrid.matrix
#
#     def setGameGrid(self, gameGrid):
#         self.agent.setGameGrid(gameGrid)