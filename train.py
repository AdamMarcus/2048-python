from puzzle import GameGrid
from agent import *

def main():
    gamegrid = GameGrid()
    gamegrid.hide()
    agent = DNNAgent(None, waitTime=0, trainDataPickle="ULRD_train_2000_20.pickle")
    gamegrid.setAgent(agent)

    with open(('ULRD_trained_model_20_game_layers_64.pickle'), 'wb') as f:
        pickle.dump(agent, f)
        print("Train data stored in {}".format(f))

main()