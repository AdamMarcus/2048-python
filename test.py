from puzzle import GameGrid
import random
from agent import *
import matplotlib.pyplot as plt
import numpy as np

def main():
    existingAgent1 = None
    with open("ULRD_trained_model_20_game_layers_32_16.pickle", 'rb') as f:
        existingAgent1 = pickle.load(f)

    with open("ULRD_trained_model_20_game_layers_64_16.pickle", 'rb') as f:
        existingAgent2 = pickle.load(f)

    agentDict = {1: RandomAgent(None, waitTime=0), 2: PatternAgentULRD(None, waitTime=0), 3: DNNAgent(None, waitTime=0, trainName="ULRD_train.pickle"), 4 : existingAgent1, 5 : existingAgent2}
    agentDescription = {1: "Random", 2: "Up-Left-Right-Down", 3: "DNN Agent", 4: "DNN Agent with layers [32, 16]", 5: "DNN Agent with layers [32, 16]"}
    agentScoreDict = {1: [], 2: [], 3: [], 4: [], 5: []}
    agentColors = {1: "b", 2: "r", 3: "g", 4: "c", 5: "m"}

    gameIDs = []
    for i in range (0, 10):
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
            agent.reset()

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
        ax.bar(ind + offset, agentScoreDict[key], width=0.1,color=agentColors[key])
        offset += 0.11

    ax.legend(agentColors.values(), agentSummarys.values())

    ax.autoscale_view()

    plt.show()

main()