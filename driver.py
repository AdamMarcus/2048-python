from puzzle import GameGrid
from agent import *
from random import randint

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

def main():
    # runTraining(25, 100, .05)
    # wederunTraining(25, 1000, .05)
    runTraining(25, 100, .01, 4)
    # runTraining(10, 1000, 10, gamegrid, PatternAgentULRD(gamegrid, waitTime=0))
    # runTraining(10, 1000, 10, gamegrid, PatternAgentLURD(gamegrid, waitTime=0))
    # runTraining(10, 1000, 10, gamegrid, ManualAgent(gamegrid, waitTime=0))
    # runTraining(10, 1000, 10, gamegrid, DNNAgent(gamegrid, waitTime=0, trainName="training_epochs/train.pickle"))


# method to run epochs and iterations to train model
# agent codes: 0 = random, 1 = ULRD, 2 = LURD, 3 = Manual, 4 = DNN
def runTraining(_numEpochs, _numItterations, _trainingSetPercent, agentCode):
    trainingRecord = []

    agent = None
    if (agentCode = 4):
        agent = RandomAgent(gamegrid, waitTime=0)
    for epochNum in range(0, _numEpochs):
        for itterNum in range(0, _numItterations):
            gamegrid = GameGrid()
            gamegrid.hide()

            if (agentCode = 0):
                agent = RandomAgent(gamegrid, waitTime=0)
            elif (agentCode = 1):
                agent = PatternAgentULRD(gamegrid, waitTime=0)
            elif (agentCode = 2):
                # agent = PatternAgentLURD(gamegrid, waitTime=0)
            elif (agentCode = 3):
                # agent = ManualAgent(gamegrid, waitTime=0)

            gamegrid.setAgent(agent)

            print("Epoch: ", epochNum, " Iteration: ", itterNum)
            gamegrid.mainloop()

            # print(gamegrid.matrix)
            print("Score: ", gamegrid.scoreMatrix())
            agent.setScore(gamegrid.scoreMatrix())

            # The current code running AI games needs to know the current epochNum for encoding filename
            (boards, moves, score) = agent.getGameRecord()
            trainingRecord.append((epochNum, itterNum, boards, moves, score))
        elif (agentCode = 4):
            bestGames = getNPercentageBestGames(_trainingSetPercent, trainingRecord.copy())
            agent = DNNAgent(gamegrid, waitTime=0, trainData=bestGames)

    with open(('train{}.pickle'.format(randint(10000, 99999))), 'wb') as f:
        pickle.dump(trainingRecord, f)
        print("Train data stored in {}".format(f))

    plotTrainingRecord(trainingRecord)




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