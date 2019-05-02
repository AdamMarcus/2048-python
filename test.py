from puzzle import GameGrid
import random
from agent import *

def main():
    for i in range (0, 30):
        random.seed(i)

        agentDict = {1: RandomAgent(None, waitTime=0), 2: PatternAgentULRD(None, waitTime=0), 3 : DNNAgent(None, waitTime=0, trainName="ULRD_train.pickle")}
        agentScoreDict = {1:[], 2:[], 3:[]}
        for (agentKey, agent) in agentDict.items():
            gamegrid = GameGrid()
            gamegrid.hide()
            gamegrid.setAgent(agent)
            agent.setGameGrid(gamegrid)
            gamegrid.mainloop()
            agentScoreDict[agentKey].append(sumScoreMatrix(gamegrid.matrix))
            print(agentScoreDict[agentKey])

def sumScoreMatrix(mat):
    sum = 0
    for i in range(4):
        for j in range(4):
            sum += mat[i][j]
    return sum

main()