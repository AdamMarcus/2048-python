import random
import constants as c
import time

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

    def pressKey(self, key):
        time.sleep(self.waitTime)
        self.myGrid.key_down_str(key)

    def checkMoveValid(self, move):
        _, done = self.myGrid.getCommand(move)(self.getCurrMat())
        return done


class RandomAgent(Agent):
    def __init__(self, gGrid, waitTime=0.1):
        #super(RandomAgent, self)._init__(self, waitTime=waitTime)
        self.waitTime = waitTime
        self.myGrid = gGrid
        # self.keyboard = Controller()

    def promptAgent(self):
        done = False
        count = 0
        while not done:
            choice = random.choices([c.KEY_UP_AGENT, c.KEY_DOWN_AGENT, c.KEY_LEFT_AGENT, c.KEY_RIGHT_AGENT], weights=[0.25, 0.25, 0.25, 0.25])[0]
            print("Temp choice: ", choice)
            count += 1
            done = self.checkMoveValid(choice)

            # If I have lost
            if count > 4:
                # do something
                print("I've lost")
                #############################
                print("########Last Resort!!!!!!")
                self.myGrid.after(20, self.myGrid.task)
                #############################
                break

        print("Random agent choice: ", choice)
        self.pressKey(choice)



class PatternAgentULRD(Agent):
    def __init__(self, gGrid, waitTime=0.1):
        #super(RandomAgent, self)._init__(self, waitTime=waitTime)
        self.waitTime = waitTime
        self.myGrid = gGrid
        # self.keyboard = Controller()

    def promptAgent(self):

        done = False
        # Always try up first
        choice = c.KEY_UP_AGENT
        if not self.checkMoveValid(choice):
            # Always try left second
            choice = c.KEY_LEFT_AGENT
            if not self.checkMoveValid(choice):
                # Always try right third
                choice = c.KEY_RIGHT_AGENT
                if not self.checkMoveValid(choice):
                    # Always try left last
                    choice = c.KEY_DOWN_AGENT
        print("Random agent choice: ", choice)
        self.pressKey(choice)

class PatternAgentLURD(Agent):
    def __init__(self, gGrid, waitTime=0.1):
        #super(RandomAgent, self)._init__(self, waitTime=waitTime)
        self.waitTime = waitTime
        self.myGrid = gGrid
        # self.keyboard = Controller()

    def promptAgent(self):

        done = False
        # Always try up first
        choice = c.KEY_LEFT_AGENT
        if not self.checkMoveValid(choice):
            # Always try left second
            choice = c.KEY_UP_AGENT
            if not self.checkMoveValid(choice):
                # Always try right third
                choice = c.KEY_RIGHT_AGENT
                if not self.checkMoveValid(choice):
                    # Always try left last
                    choice = c.KEY_DOWN_AGENT
        print("Random agent choice: ", choice)
        self.pressKey(choice)



