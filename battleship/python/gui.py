# this file is for the GUI code

from tkinter import*
from random import*


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
    enemys = {}
    s = {}
    
    enemyships = []
    ships = []
    shipsindex = -1

    player = 0
    enemy = 0


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
                t = Ship(3)
                self.enemyships.append(t)
                self.ships.append(t)
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
                self.setbuttons[index] = Button(self.shipsframe, relief = GROOVE, bd = 1, bg="light blue", height = 1, width=2, command = lambda i =index: self.place(i,0))
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

                #setting it so that empty cells equal 0, full cells equal 1
                self.enemys[index] = (0,-1)

        self.enemyplacement()
        return


    def enemyplacement(self):
        #5, 4, 3, 3, 2
        self.shipsindex = -1
        for ship in self.enemyships:
            placed = False
            self.shipsindex += 1
            while placed == False:
                index = randrange(0,110)
                self.place(index, 1)

                placed = self.enemyships[self.shipsindex].isplaced()
        return

    def shot(self, index):
        #blue = water, black = ship, red = hit, white = miss
        if self.enemys[index][0] == 0:
            self.buttons[index].configure(bg = "white")
        else:
            self.buttons[index].configure(bg = "red")
            self.ships[self.enemys[index][1]].hit()
            
            if self.ships[self.enemys[index][1]].issunk():
                #sink a ship
                self.player += 1

                if self.player == 5:
                    self.win()
                
        self.buttons[index].configure(state = DISABLED)

        #######
        ###### Put in logic and stuff for hits and misses
        #####   and sinking ships
        ###      and marking off what ships are sunk
        ##        Also...alternating turns...
        #
        
        return

    def win(self):
        winner = "You Win!"
        if self.player < self.enemy:
            winner = "Enemy Wins!"

        top = Toplevel()
        top.title("Winner")
        msg = Message(top, text = winner,)
        msg.pack()

        button = Button(top, text="ok", command = top.destroy)
        button.pack()

    def place(self, index, eorp):
        whichships = [self.ships[self.shipsindex], self.enemyships[self.shipsindex]]
        
        if self.shipsindex < 0:
            return

        if eorp == 0:
            #if ship already there, return
            if self.setbuttons[index].cget('bg') == "dark gray" and whichships[eorp].getplace() != index:
                return
        else:
            if self.enemys[index][0] == 1 and whichships[eorp].getplace() != index:
                return
        if whichships[eorp].isplaced() and whichships[eorp].getplace() != index:
            return
        elif whichships[eorp].getplace() == index:
            if whichships[eorp].direction() != True:
                for i in range(whichships[eorp].getsize()):
                    if eorp == 0:
                        self.setbuttons[index+10*i].configure(bg = "light blue")
                    else:
                        self.enemys[index+10*i] = (0, -1)
            else:
                for i in range(whichships[eorp].getsize()):
                    if eorp ==0:
                        self.setbuttons[index+i].configure(bg = "light blue")
                    else:
                        self.enemys[index+10*i] = (0, -1)
            whichships[eorp].direction()
            

        #if ship size will make the ship go off the board return
        if whichships[eorp].direction():
            if index + 10*whichships[eorp].getsize() < 110:
                for i in range(whichships[eorp].getsize()):
                    if eorp ==0:
                        if self.setbuttons[index+10*i].cget('bg') == "dark gray":
                            return
                    else:
                        if self.enemys[index+10*i][1] == 1:
                            return
                for i in range(whichships[eorp].getsize()):
                    if eorp == 0:
                        self.setbuttons[index+10*i].configure(bg = "dark gray")
                    else:
                        self.enemys[index+10*i] = (1,self.shipsindex)
            else:
                return
        else:
            if index % 10 + whichships[eorp].getsize() < 11:
                for i in range(whichships[eorp].getsize()):
                    if eorp == 0:
                        if self.setbuttons[index+i].cget('bg') == "dark gray":
                            return
                    else:
                        if self.enemys[index+i][0] == 1:
                            return
                for i in range(whichships[eorp].getsize()):
                    if eorp == 0:
                        self.setbuttons[index+i].configure(bg = "dark gray")
                    else:
                        self.enemys[index+i] = (1, self.shipsindex)
            else:
                return

        whichships[eorp].place(index)
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
    cells = []

    def __init__(self, size):
        self.length = size
        self.sunk = False

    def hit(self):
        self.hits += 1
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
