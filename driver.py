from puzzle import GameGrid
from agent import *
from random import randint

import matplotlib.pyplot as plt

def main():
    # Run itterative learning/training using a defined number of games output from the last epoch
    runner = TrainingPartialCountRunner(5, 5, 4, 5)

    # Run itterative learning/training using a defined number of games output from all epochs
    # Had a bug here right before turning in! This one doesnt work now
    # runner = TrainingWholeCountRunner(5, 5, 4, 4)

    # Run itterative learning/training using an upper percentile of games output from the last epoch
    # runner = TrainPartialPercentRunner(10, 100, 4, .01)

    # Run itterative learning/training using an upper percentile of games output from all epochs
    # runner = TrainWholePercentRunner(10, 10, 4, .01)
    runner.runTraining()

# This is an abstract implementation of a class to run training. This class handles how many epochs and itterations to run, and how to re-train.
class Runner:
    def __init__(self, numEpochs, numItterations, agentCode):
        self._numEpochs = numEpochs
        self._numItterations = numItterations
        self._agentCode = agentCode

        self._gamegrid = GameGrid()
        self._gamegrid.hide()

        self._trainingRecord = []

    def createAgent(self, gameSessionFile=None, trainName=None, trainData=None, trainDataPickle=None, existingAgent=None):
        if (self._agentCode == 0):
            self._gamegrid.setAgent(RandomAgent(None, waitTime=0))
        elif (self._agentCode == 1):
            self._gamegrid.setAgent(PatternAgentULRD(None, waitTime=0))
        elif (self._agentCode == 2):
            self._gamegrid.setAgent(PatternAgentLURD(None, waitTime=0))
        elif (self._agentCode == 3):
            self._gamegrid.setAgent(ManualAgent(None, waitTime=0))
        elif (self._agentCode == 4):
            self._gamegrid.setAgent(DNNAgent(None, waitTime=0, gameSessionFile=gameSessionFile, trainName=trainName, trainData=trainData, trainDataPickle=trainDataPickle))

        self._gamegrid.getAgent().setGameGrid(self._gamegrid)

    def refreshGameGrid(self):
        agent = self._gamegrid.getAgent()
        self._gamegrid = GameGrid()
        self._gamegrid.hide()

        agent.reset()

        self._gamegrid.setAgent(agent)
        self._gamegrid.getAgent().setGameGrid(self._gamegrid)

    def runTraining(self):
        for epochNum in range(0, self._numEpochs):
            for itterNum in range(0, self._numItterations):
                self.refreshGameGrid()
                self._gamegrid.setAgent(self._agent)

                print("Epoch: ", epochNum, " Iteration: ", itterNum)
                self._gamegrid.mainloop()

                # print(gamegrid.matrix)
                print("Score: ", self._gamegrid.scoreMatrix())
                self._agent.setScore(self._gamegrid.scoreMatrix())

                # The current code running AI games needs to know the current epochNum for encoding filename
                (boards, moves, score) = self._agent.getGameRecord()
#                 self._agent.pikPakGame()
                self._trainingRecord.append((epochNum, itterNum, boards, moves, score))
        return self._trainingRecord


# Runner implementation that will use a top percentile of all games stored in _trainingRecord to train the next epoch
class TrainWholePercentRunner(Runner):
    def __init__(self, numEpochs, numItterations, agentCode, percent):
        super().__init__(numEpochs, numItterations, agentCode)
        self._percent = percent


    def runTraining(self):
        currData = None
        for epochNum in range(0, self._numEpochs):
            self.createAgent(trainData=currData)
            for itterNum in range(0, self._numItterations):
                self.refreshGameGrid()
                self._gamegrid.getAgent().reset()

                print("Epoch: ", epochNum, " Iteration: ", itterNum)
                self._gamegrid.mainloop()

                # print(gamegrid.matrix)
                print("Score: ", self._gamegrid.scoreMatrix())
                self._gamegrid.getAgent().setScore(self._gamegrid.scoreMatrix())

                # The current code running AI games needs to know the current epochNum for encoding filename
                (boards, moves, score) = self._gamegrid.getAgent().getGameRecord()
                self._trainingRecord.append((epochNum, itterNum, boards, moves, score))

                currData = getNPercentageBestGames(self._percent, self._trainingRecord.copy())
        with open(('train{}.pickle'.format(randint(10000, 99999))), 'wb') as f:
            pickle.dump(self._trainingRecord, f)
            print("Train data stored in {}".format(f))

        plotTrainingRecord(self._trainingRecord)

        return self._trainingRecord

# Runner implementation that will use a top percentile of games from the last epoch to train the next epoch
class TrainPartialPercentRunner(Runner):
    def __init__(self, numEpochs, numItterations, agentCode, percent):
        super().__init__(numEpochs, numItterations, agentCode)
        self._percent = percent


    def runTraining(self):
        currData = None
        for epochNum in range(0, self._numEpochs):
            epochTrainSet = []
            self.createAgent(trainData=currData)
            for itterNum in range(0, self._numItterations):
                self.refreshGameGrid()

                print("Epoch: ", epochNum, " Iteration: ", itterNum)
                self._gamegrid.mainloop()

                # print(gamegrid.matrix)
                print("Score: ", self._gamegrid.scoreMatrix())
                self._gamegrid.getAgent().setScore(self._gamegrid.scoreMatrix())

                # The current code running AI games needs to know the current epochNum for encoding filename
                (boards, moves, score) = self._gamegrid.getAgent().getGameRecord()
                self._trainingRecord.append((epochNum, itterNum, boards, moves, score))
                epochTrainSet.append((epochNum, itterNum, boards, moves, score))

                currData = getNPercentageBestGames(self._percent, epochTrainSet)
        plotTrainingRecord(self._trainingRecord)
        return self._trainingRecord

# Runner implementation that will use a fixed number of games stored in _trainingRecord to train the next epoch
class TrainingWholeCountRunner(Runner):
    def __init__(self, numEpochs, numItterations, agentCode, trainingCount):
        super().__init__(numEpochs, numItterations, agentCode)
        self._trainingCount = trainingCount

    def runTraining(self):
        currData = None
        for epochNum in range(0, self._numEpochs):
            self.createAgent(trainData=currData)
            for itterNum in range(0, self._numItterations):
                self.refreshGameGrid()

                print("Epoch: ", epochNum, " Iteration: ", itterNum)
                self._gamegrid.mainloop()

                # print(gamegrid.matrix)
                print("Score: ", self._gamegrid.scoreMatrix())
                self._gamegrid.getAgent().setScore(self._gamegrid.scoreMatrix())

                # The current code running AI games needs to know the current epochNum for encoding filename
                (boards, moves, score) = self._gamegrid.getAgent().getGameRecord()
                self._trainingRecord.append((epochNum, itterNum, boards, moves, score))

                currData = getNBestGames(self._trainingCount, self._trainingRecord)
        plotTrainingRecord(self._trainingRecord)

        return self._trainingRecord

# Runner implementation that will use a fixed number of games from the last epoch to train the next epoch
class TrainingPartialCountRunner(Runner):
    def __init__(self, numEpochs, numItterations, agentCode, trainingCount):
        super().__init__(numEpochs, numItterations, agentCode)
        self._trainingCount = trainingCount

    def runTraining(self):
        currData = None
        for epochNum in range(0, self._numEpochs):
            self.createAgent(trainData=currData)
            epochTrainSet = []
            for itterNum in range(0, self._numItterations):
                self.refreshGameGrid()

                print("Epoch: ", epochNum, " Iteration: ", itterNum)
                self._gamegrid.mainloop()

                # print(gamegrid.matrix)
                print("Score: ", self._gamegrid.scoreMatrix())
                self._gamegrid.getAgent().setScore(self._gamegrid.scoreMatrix())

                # The current code running AI games needs to know the current epochNum for encoding filename
                (boards, moves, score) = self._gamegrid.getAgent().getGameRecord()
                self._trainingRecord.append((epochNum, itterNum, boards, moves, score))
                epochTrainSet.append((epochNum, itterNum, boards, moves, score))

            currData = getNBestGames(self._trainingCount, epochTrainSet.copy())

        with open("TrainingPartialCountRunner_100_20_4_5.pickle", 'wb') as f:
            agent = DNNAgent(None, waitTime=0, trainData=currData)
            pickle.dump(agent, f)
            print("Train data stored in {}".format(f))

        plotTrainingRecord(self._trainingRecord)

        return self._trainingRecord

# Data is in the form: (epochNum, itterNum, boards, moves, score)
def getNPercentageBestGames(nPerc, gameData):
    bestGames = []
    n = int(len(gameData) * nPerc + 1)
    for i in range(0, n):
        maxVal = float("-inf")
        maxGameInd = -1
        for j in range(0, len(gameData)):
            currGame = gameData[j]
            if currGame[4] >= maxVal:
                maxVal = currGame[4]
                maxGameInd = j
        # print("Next top score: ", gameData[maxGameInd][4])
        bestGames.append(gameData[maxGameInd])
        _ = gameData.pop(maxGameInd)
    # print(bestGames)
    return bestGames

# Data is in the form: (epochNum, itterNum, boards, moves, score)
def getNBestGames(n, gameData):
    bestGames = []
    for i in range(0, n):
        maxVal = float("-inf")
        maxGameInd = -1
        for j in range(0, len(gameData)):
            currGame = gameData[j]
            if currGame[4] >= maxVal:
                maxVal = currGame[4]
                maxGameInd = j
        # print("Next top score: ", gameData[maxGameInd][4])
        bestGames.append(gameData[maxGameInd])
        _ = gameData.pop(maxGameInd)

    # print(bestGames)
    return bestGames

# Data is in the form: (epochNum, itterNum, boards, moves, score)
def plotTrainingRecord(data):
    fig, ax = plt.subplots()
    x = []
    y = []
    for i in range(0, len(data)):
        x.append(i)
        y.append(data[i][4])
    plt.bar(x, y)
    plt.show()

main()