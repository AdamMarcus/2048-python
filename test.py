from puzzle import GameGrid
import random
from agent import *
import matplotlib.pyplot as plt
import numpy as np

def main():
    agentDict = {1: RandomAgent(None, waitTime=0), 2: PatternAgentULRD(None, waitTime=0), 3: DNNAgent(None, waitTime=0, trainName="ULRD_train.pickle")}
    agentDescription = {1: "Random", 2: "Up-Left-Right-Down", 3: []}
    agentScoreDict = {1: [], 2: [], 3: []}
    agentColors = {1: "b", 2: "r", 3: "g"}

    gameIDs = []
    for i in range (0, 5):
        gameIDs.append(i)
        random.seed(i)
        for (agentKey, agent) in agentDict.items():
            gamegrid = GameGrid()
            gamegrid.hide()
            gamegrid.setAgent(agent)
            agent.setGameGrid(gamegrid)
            gamegrid.mainloop()
            agentScoreDict[agentKey].append(sumScoreMatrix(gamegrid.matrix))
            print(agentScoreDict[agentKey])

    plotTrainingRecord(gameIDs, agentDict, agentDescription, agentScoreDict, agentColors)



def sumScoreMatrix(mat):
    sum = 0
    for i in range(4):
        for j in range(4):
            sum += mat[i][j]
    return sum

def plotTrainingRecord(gameIDs, agentDict, agentSummarys, agentScoreDict, agentColors):
    ind = np.arange(len(gameIDs))
    fig, ax = plt.subplots()
    x = agentDict.keys()

    offset = 0
    for key in x:
        ax.bar(ind + offset, agentScoreDict[key], width=0.2,color=agentColors[key])
        offset += 0.21

    ax.legend(agentColors.values(), agentSummarys.values())

    plt.show()

main()