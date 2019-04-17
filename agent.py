# import util
import random
import constants as c
from pynput.keyboard import Key, Controller
import time
import logic
# import numpy as np
# import np.random

class Agent:
    def __init__(self, gGrid, waitTime=0.1):
        self.waitTime = waitTime
        self.myGrid = gGrid
        print("__init__ not defined for abstract Agent")

    # This function is to be populated with code for the agent to respond to a new board being given after an update and will trigger a command.
    def promptAgent(self, currentMatrix):
        print("__init__ not defined for promptAgent method in abstract Agent")

    def getCurrMat(self):
        return self.myGrid.matrix

class RandomAgent(Agent):
    def __init__(self, gGrid, waitTime=0.1):
        #super(RandomAgent, self)._init__(self, waitTime=waitTime)
        self.waitTime = waitTime
        self.myGrid = gGrid
        self.keyboard = Controller()

    def promptAgent(self):
        done = False
        count = 0
        while not done:
            choice = random.choices([c.KEY_UP_AGENT, c.KEY_DOWN_AGENT, c.KEY_LEFT_AGENT, c.KEY_RIGHT_AGENT], weights=[0.25, 0.25, 0.25, 0.25])[0]
            print("Temp choice: ", choice)
            count += 1
            _, done = self.myGrid.getCommand(choice)(self.getCurrMat())

            # If I have lost
            if count > 4:
                # do something
                print("I've lost")
                break

        print("Random agent choice: ", choice)
        time.sleep(self.waitTime)
        self.keyboard.press(choice)
        self.keyboard.release(choice)


class PatternAgentULRD(Agent):
    def __init__(self, gGrid, waitTime=0.1):
        #super(RandomAgent, self)._init__(self, waitTime=waitTime)
        self.waitTime = waitTime
        self.myGrid = gGrid
        self.keyboard = Controller()

    def promptAgent(self):

        done = False
        # Always try up first
        choice = c.KEY_UP_AGENT
        _, done = self.myGrid.getCommand(choice)(self.getCurrMat())
        if not done:
            # Always try left second
            choice = c.KEY_LEFT_AGENT
            _, done = self.myGrid.getCommand(choice)(self.getCurrMat())
            if not done:
                # Always try right third
                choice = c.KEY_RIGHT_AGENT
                _, done = self.myGrid.getCommand(choice)(self.getCurrMat())
                if not done:
                    # Always try left last
                    choice = c.KEY_DOWN_AGENT
                    _, done = self.myGrid.getCommand(choice)(self.getCurrMat())
        print("Random agent choice: ", choice)
        time.sleep(self.waitTime)
        self.keyboard.press(choice)
        self.keyboard.release(choice)



