# this file is for the GUI code

from tkinter import*


class GameBoard():
    #create root window for game
    root = Tk()
    buttons = {}


    def __init__(self):
        self.root.geometry("500x600")

        #self.makegridships()
        self.makegridshot()

        #run gui
        self.root.mainloop()




    def makegridships(self):
        #create 10x10 grid for placing ships
        #below grid there is list of possible ships to place
                #after placement, it's a way to show what ships you've sunk
        return



    #create 10x10 grid of buttons for taking shots
    def makegridshot(self):
        #clicking button is taking a shot
        for r in range(10):
            for c in range(10):
                index = r*10+c
                self.buttons[index] = Button(self.root, relief = GROOVE, bd = 1, bg="light blue", height = 1, width=2, command = lambda i =index: self.shot(i))
                self.buttons[index].grid(row=r,column=c)
        return



    def shot(self, index):
        #blue = water, black = ship, red = hit, white = miss
        self.buttons[index].configure(bg = "red")        
        return


#game = GameBoard()
