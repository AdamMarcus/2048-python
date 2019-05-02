from puzzle import GameGrid
import random
from agent import *
import matplotlib.pyplot as plt
import numpy as np

def main():
    gamegrid = GameGrid()
    gamegrid.hide()
    agent = DNNAgent(None, waitTime=0, trainDataPickle="ULRD_train_2000_20.pickle")
    gamegrid.setAgent(agent)

    with open(('ULRD_trained_model_20_game_layers_64_16.pickle'), 'wb') as f:
        pickle.dump(agent, f)
        print("Train data stored in {}".format(f))

main()