from puzzle import GameGrid

def main():
    for i in range (0, 10):
        for j in range(0, 100):

            gamegrid = GameGrid()
            gamegrid.mainloop()



            print(gamegrid.matrix)
            print("Score: ", gamegrid.scoreMatrix())

            gamegrid.agent.setScore(gamegrid.scoreMatrix())
            gamegrid.agent.pikPakGame()
main()