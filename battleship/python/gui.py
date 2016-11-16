# this file is for the GUI code

from tkinter import*


class GameBoard():
    #create root window for game
    root = Tk()
    shipsframe = LabelFrame(root, text="Your Ships", labelanchor = N, bd=0, padx = 10, width = 10)
    enemyframe = LabelFrame(root, text="Enemy Ships", labelanchor = N, bd = 0, padx = 10, width = 10)
    checks = LabelFrame(root, text="Ships", labelanchor = N, bd=0, padx = 30)
    instructions = LabelFrame(root, bd = 0)
    info = Label(instructions, text = "Pick a Ship to Place on Your Ships", bd = 0, justify = CENTER)
    buttons = {}
    setbuttons = {}
    s = {}
    
    enemyships = []
    ships = []
    shipsindex = -1


    def __init__(self):
        #set window
        self.root.title("Battleship")
        self.root.geometry("480x500")

        #set frames
        self.shipsframe.place(anchor = NW, y = 10)
        self.enemyframe.pack(side = RIGHT, anchor = NE, pady = 10)
        self.checks.place(relx = .29, rely = .66)
        self.instructions.place(relx = .3, rely = .58)
        self.info.pack()

        #create ships
        self.createships()
        
        #make a checklist of ships to place
        self.listships()

        #make playing grids
        self.makegridships()
        self.makegridshot()

        #run gui
        self.root.mainloop()


    def createships(self):
        for i in range(4):
            s = Ship(i+2)
            if i + 2 == 3:
                self.enemyships.append(s)
                self.ships.append(s)
            self.enemyships.append(s)
            self.ships.append(s)


    def listships(self):
        #create a checklist of ships to place
        #1-5length, 1-4length, 2-3length, 1-2length
        i = 5
        for r in range(5):
            i -= 1
            if r == 3:
                i+=1
            self.s[r] = Checkbutton(self.checks, onvalue = 1, offvalue = 0, width =0, padx= 0, command = lambda j=i+1: self.shipsize(j))
            self.s[r].grid(row = r, column = 0)
            for c in range(i+1):
                button = Button(self.checks, relief = GROOVE, bd = 1, bg="dark gray")
                button.configure(state = DISABLED, height = 1, width = 2)
                button.grid(row = r, column = c+1)


        return


    def makegridships(self):
        #create 10x10 grid for placing ships
        for r in range(10):
            for c in range(10):
                index = r*10+c
                self.setbuttons[index] = Button(self.shipsframe, relief = GROOVE, bd = 1, bg="light blue", height = 1, width=2, command = lambda i =index: self.place(i))
                self.setbuttons[index].grid(row=r,column=c)
        return



    #create 10x10 grid of buttons for taking shots
    def makegridshot(self):
        #clicking button is taking a shot
        for r in range(10):
            for c in range(10):
                index = r*10+c
                self.buttons[index] = Button(self.enemyframe, relief = GROOVE, bd = 1, bg="light blue", height = 1, width=2, command = lambda i =index: self.shot(i))
                self.buttons[index].grid(row=r,column=c)
        return



    def shot(self, index):
        #blue = water, black = ship, red = hit, white = miss
        if self.buttons[index].cget('bg') == "light blue":
            self.buttons[index].configure(bg = "white")
        else:
            self.buttons[index].configure(bg = "red")
        self.buttons[index].configure(state = DISABLED)

        #######
        ###### Put in logic and stuff for hits and misses
        #####   and sinking ships
        ###      and marking off what ships are sunk
        ##        Also...alternating turns...
        #
        
        return

    def place(self, index):
        if self.shipsindex < 0:
            return
        
        #if ship already there, return
        if self.setbuttons[index].cget('bg') == "dark gray" and self.ships[self.shipsindex].getplace() != index:
            return
        elif self.ships[self.shipsindex].isplaced() and self.ships[self.shipsindex].getplace() != index:
            return
        elif self.ships[self.shipsindex].getplace() == index:
            if self.ships[self.shipsindex].direction() != True:
                for i in range(self.ships[self.shipsindex].getsize()):
                    self.setbuttons[index+10*i].configure(bg = "light blue")
            else:
                for i in range(self.ships[self.shipsindex].getsize()):
                    self.setbuttons[index+i].configure(bg = "light blue")
            self.ships[self.shipsindex].direction()
            

        #if ship size will make the ship go off the board return
        if self.ships[self.shipsindex].direction():
            if index + 10*self.ships[self.shipsindex].getsize() < 110:
                for i in range(self.ships[self.shipsindex].getsize()):
                    if self.setbuttons[index+10*i].cget('bg') == "dark gray":
                        return
                for i in range(self.ships[self.shipsindex].getsize()):
                    self.setbuttons[index+10*i].configure(bg = "dark gray")
            else:
                return
        else:
            if index % 10 + self.ships[self.shipsindex].getsize() < 11:
                for i in range(self.ships[self.shipsindex].getsize()):
                    if self.setbuttons[index+i].cget('bg') == "dark gray":
                        return
                for i in range(self.ships[self.shipsindex].getsize()):
                    self.setbuttons[index+i].configure(bg = "dark gray")
            else:
                return

        self.ships[self.shipsindex].place(index)
        return

    def shipsize(self, size):
        i = size-1
        if i == 1:
            i = 0
        elif i == 2:
            if self.ships[2].isplaced() == True:
                i = 1
        self.shipsindex = i
        return

class Ship():
    length = 0
    hits = 0
    sunk = None
    vertical = True
    startindex = -1

    def __init__(self, size):
        self.length = size
        self.sunk = False

    def shot(self):
        return

    def issunk(self):
        if self.hits == self.length:
            self.sunk = True
        return self.sunk

    def direction(self):
        if self.vertical == True:
            self.vertical = False
        else:
            self.vertical = True
        return self.vertical

    def place(self, index):
        self.startindex = index
        return

    def getplace(self):
        return self.startindex

    def isplaced(self):
        if self.startindex == -1:
            return False
        return True

    def getsize(self):
        return self.length
    
game = GameBoard()
