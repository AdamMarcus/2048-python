from puzzle import GameGrid
from agent import *
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

def main():
    existingAgent1 = None
    with open("TrainingPartialCountRunner_100_20_4_5.pickle", 'rb') as f:
        existingAgent0 = pickle.load(f)

    with open("ULRD_trained_model_20_game_layers_32_16.pickle", 'rb') as f:
        existingAgent1 = pickle.load(f)

    with open("ULRD_trained_model_20_game_layers_64_16.pickle", 'rb') as f:
        existingAgent2 = pickle.load(f)

    with open("ULRD_trained_model_20_game_layers_64_16_8.pickle", 'rb') as f:
        existingAgent3 = pickle.load(f)

    with open("ULRD_trained_model_20_game_layers_64_32_8.pickle", 'rb') as f:
        existingAgent4 = pickle.load(f)

    with open("ULRD_trained_model_20_game_layers_64.pickle", 'rb') as f:
        existingAgent5 = pickle.load(f)


    agentDict = {1: RandomAgent(None, waitTime=0), 2: PatternAgentULRD(None, waitTime=0), 0: existingAgent0, 3: DNNAgent(None, waitTime=0, trainName="ULRD_train.pickle"), 4 : existingAgent1, 5 : existingAgent2, 6 : existingAgent2, 7 : existingAgent2, 8 : existingAgent2}
    agentDescription = {1: "Random", 2: "Up-Left-Right-Down", 0: "Online learning NN", 3: "DNN Agent", 4: "DNN Agent with layers [32, 16]", 5: "DNN Agent with layers [64, 16]", 6: "DNN Agent with layers [64, 16, 8]", 7: "DNN Agent with layers [64, 32, 8]", 8: "DNN Agent with layers [64]"}
    agentScoreDict = {1: [], 2: [], 0: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []}
    agentColors = {1: "b", 2: "r", 0: "#1f004d", 3: "g", 4: "c", 5: "m", 6: "y",7: "k",8: "#3CFE6E"}

    gameIDs = []
    for i in range (0, 15):
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

    custom_lines = [Line2D([0], [0], color=agentColors[1], lw=4),
                    Line2D([0], [0], color=agentColors[2], lw=4),
                    Line2D([0], [0], color=agentColors[0], lw=4),
                    Line2D([0], [0], color=agentColors[3], lw=4),
                    Line2D([0], [0], color=agentColors[4], lw=4),
                    Line2D([0], [0], color=agentColors[5], lw=4),
                    Line2D([0], [0], color=agentColors[6], lw=4),
                    Line2D([0], [0], color=agentColors[7], lw=4),
                    Line2D([0], [0], color=agentColors[8], lw=4)]

    fig, ax = plt.subplots()
    ax.legend(custom_lines, agentSummarys.values())

    plt.show()

main()