from puzzle import GameGrid
from agent import *
from random import randint

# import matplotlib.pyplot as plt; plt.rcdefaults()
# import numpy as np

def main():
    # runner = TrainingPartialCountRunner(20, 50, 4, 2)
    runner = TrainingWholeCountRunner(1, 2000, 1, 20)
    # runner = TrainingPartialCountRunner(10, 100, 4, 20)
    # runner = TrainWholePercentRunner(20, 20, 4, 1)
    # runner = TrainWholePercentRunner(1, 2, 4, .01)
    # runner = TrainPartialPercentRunner(10, 100, 4, .01)

    runner.runTraining()

    # runTraining(25, 100, .05)
    # wederunTraining(25, 1000, .05)
    # runTraining_perc(2, 5000, .01, 4)
    # runTraining(10, 1000, 10, gamegrid, PatternAgentULRD(gamegrid, waitTime=0))
    # runTraining(10, 1000, 10, gamegrid, PatternAgentLURD(gamegrid, waitTime=0))
    # runTraining(10, 1000, 10, gamegrid, ManualAgent(gamegrid, waitTime=0))
    # runTraining(10, 1000, 10, gamegrid, DNNAgent(gamegrid, waitTime=0, trainName="training_epochs/train.pickle"))

# This is an abstract implementation of a class to run training. This class handles how many epochs and itterations to run, and how to re-train.
class Runner:
    def __init__(self, numEpochs, numItterations, agentCode):
        self._numEpochs = numEpochs
        self._numItterations = numItterations
        self._agentCode = agentCode

        self._gamegrid = GameGrid()
        self._gamegrid.hide()

        if (agentCode == 0):
            self._agent = RandomAgent(None, waitTime=0)
        elif (agentCode == 1):
            self._agent = PatternAgentULRD(None, waitTime=0)
        elif (agentCode == 2):
            self._agent = PatternAgentLURD(None, waitTime=0)
        elif (agentCode == 3):
            self._agent = ManualAgent(None, waitTime=0)
        elif (agentCode == 4):
            self._agent = DNNAgent(None, waitTime=0, trainName="ULRD_train.pickle")

        self._agent.setGameGrid(self._gamegrid)
        self._gamegrid.setAgent(self._agent)
        self._trainingRecord = []

    def refreshGameGrid(self):
        self._gamegrid = GameGrid()
        # self._gamegrid.hide()
        self._gamegrid.setAgent(self._agent)
        self._agent.setGameGrid(self._gamegrid)

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
        for epochNum in range(0, self._numEpochs):
            for itterNum in range(0, self._numItterations):
                self.refreshGameGrid()

                print("Epoch: ", epochNum, " Iteration: ", itterNum)
                self._gamegrid.mainloop()

                # print(gamegrid.matrix)
                print("Score: ", self._gamegrid.scoreMatrix())
                self._agent.setScore(self._gamegrid.scoreMatrix())

                # The current code running AI games needs to know the current epochNum for encoding filename
                (boards, moves, score) = self._agent.getGameRecord()
                self._trainingRecord.append((epochNum, itterNum, boards, moves, score))

            if (self._agentCode == 4):
                # print(self._trainingRecord)
                bestGames = getNPercentageBestGames(self._percent, self._trainingRecord.copy())
                # print("BEST:", bestGames)
                # print("Retrain agent")
                self._agent = DNNAgent(None, waitTime=0, trainData=bestGames)
                 #print("Done retraining")
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
        for epochNum in range(0, self._numEpochs):
            epochTrainSet = []
            for itterNum in range(0, self._numItterations):

                self.refreshGameGrid()

                print("Epoch: ", epochNum, " Iteration: ", itterNum)
                self._gamegrid.mainloop()

                # print(gamegrid.matrix)
                print("Score: ", self._gamegrid.scoreMatrix())
                self._agent.setScore(self._gamegrid.scoreMatrix())

                # The current code running AI games needs to know the current epochNum for encoding filename
                (boards, moves, score) = self._agent.getGameRecord()
                self._trainingRecord.append((epochNum, itterNum, boards, moves, score))
                epochTrainSet.append((epochNum, itterNum, boards, moves, score))

            if (self._agentCode == 4):
                bestGames = getNPercentageBestGames(self._percent, epochTrainSet.copy())
                self._agent = DNNAgent(None, waitTime=0, trainData=bestGames)
        with open(('train{}.pickle'.format(randint(10000, 99999))), 'wb') as f:
            pickle.dump(self._trainingRecord, f)
            print("Train data stored in {}".format(f))

        plotTrainingRecord(self._trainingRecord)

        return self._trainingRecord

# Runner implementation that will use a fixed number of games stored in _trainingRecord to train the next epoch
class TrainingWholeCountRunner(Runner):
    def __init__(self, numEpochs, numItterations, agentCode, trainingCount):
        super().__init__(numEpochs, numItterations, agentCode)
        self._trainingCount = trainingCount

    def runTraining(self):
        for epochNum in range(0, self._numEpochs):
            for itterNum in range(0, self._numItterations):
                self.refreshGameGrid()

                print("Epoch: ", epochNum, " Iteration: ", itterNum)
                self._gamegrid.mainloop()

                # print(gamegrid.matrix)
                print("Score: ", self._gamegrid.scoreMatrix())
                self._agent.setScore(self._gamegrid.scoreMatrix())

                # The current code running AI games needs to know the current epochNum for encoding filename
                (boards, moves, score) = self._agent.getGameRecord()
                self._trainingRecord.append((epochNum, itterNum, boards, moves, score))

            #########################
            with open('ULRD_train_2000_20.pickle', 'wb') as f:
                bestGames = getNBestGames(self._trainingCount, self._trainingRecord.copy())
                pickle.dump(bestGames, f)
                print("Train data stored in {}".format(f))

            with open('ULRD_train_2000.pickle', 'wb') as f:
                pickle.dump(self._trainingRecord, f)
                print("Train data stored in {}".format(f))
            #########################
            if (self._agentCode == 4):
                bestGames = getNBestGames(self._trainingCount, self._trainingRecord.copy())
                self._agent = DNNAgent(None, waitTime=0, trainData=bestGames)
        with open(('train{}.pickle'.format(randint(10000, 99999))), 'wb') as f:
            pickle.dump(self._trainingRecord, f)
            print("Train data stored in {}".format(f))

        plotTrainingRecord(self._trainingRecord)

        return self._trainingRecord

# Runner implementation that will use a fixed number of games from the last epoch to train the next epoch
class TrainingPartialCountRunner(Runner):
    def __init__(self, numEpochs, numItterations, agentCode, trainingCount):
        super().__init__(numEpochs, numItterations, agentCode)
        self._trainingCount = trainingCount

    def runTraining(self):
        for epochNum in range(0, self._numEpochs):
            for itterNum in range(0, self._numItterations):
                self.refreshGameGrid()

                print("Epoch: ", epochNum, " Iteration: ", itterNum)
                self._gamegrid.mainloop()

                # print(gamegrid.matrix)
                print("Score: ", self._gamegrid.scoreMatrix())
                self._agent.setScore(self._gamegrid.scoreMatrix())

                # The current code running AI games needs to know the current epochNum for encoding filename
                (boards, moves, score) = self._agent.getGameRecord()
                self._trainingRecord.append((epochNum, itterNum, boards, moves, score))

            if (self._agentCode == 4):
                bestGames = getNBestGames(self._trainingCount, self._trainingRecord.copy())
                self._agent = DNNAgent(None, waitTime=0, trainData=bestGames)
        with open(('train{}.pickle'.format(randint(10000, 99999))), 'wb') as f:
            pickle.dump(self._trainingRecord, f)
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
    # fig, ax = plt.subplots()
    # x = []
    # y = []
    # for i in range(0, len(data)):
    #     x.append(i)
    #     y.append(data[i][4])
    # plt.bar(x, y)
    # plt.show()
    print("no")

main()