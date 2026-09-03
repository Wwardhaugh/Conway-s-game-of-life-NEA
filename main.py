# region imports
import tkinter as tk

# endregion

# region globals

# width of the grid that is displayed, the real grid has unlimited size
GridWidth = 20  # note that higher values tend to lead to lag when resizing

# colour customization of the cells
AliveCol = "black"
DeadCol = "white"

# rule values used for simulation
DeathByUnderpop = 2 # default 2
DeathByOverpop = 3 # default 3
ParentsRequired = 3 # default 3


# endregion

# region classes

# main window
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("test")
        self.geometry("500x500")
        self.configure(bg="gray")
        self.state("zoomed")


# cell used in grid display only, state is bool, True -> alive, False -> dead
class DisplayCell(tk.Frame):
    def __init__(self, x: int, y: int, state: bool, master):
        super().__init__(master=master)
        self.x = x
        self.y = y
        self.state = state

        # used to set the state to dead by default
        if self.state is None:
            self.state = False

        # set initial colour
        if self.state:
            self.configure(bg=AliveCol)
        else:
            self.configure(bg=DeadCol)

        # set cell size relative to the grid width
        self.configure(width=400 / GridWidth, height=400 / GridWidth)

        # set the position in the displayGrid widget
        self.grid(row=self.x, column=self.y)

    # procedure to update colour based on state
    def update_colour(self):
        if self.state:
            self.configure(bg=AliveCol)
        else:
            self.configure(bg=DeadCol)

# cell class used for the main rule algorithm and calculations
class SimCell:
    def __init__(self, x: int, y: int, nextState: bool):
        self.x = x
        self.y = y
        self.nextState = nextState

    #debug message
    def __del__(self):
        #print(f"cell at {self.x}, {self.y} has died")
        pass

    def update_state(self):
        # if the cell dies, delete itself
        del self

    def get_coords(self):
        return [self.x, self.y]

    # calculates next state based on neighbours and current rules
    def find_next_state(self, live_pos):
        # counts the neighbour's states
        # if a dead neighbor is found it is added to the list of dead cells
        live_neighbours = 0
        dead_neighbours = 0
        dead_neighbours_pos = []
        for x in [-1,0,1]:
            for y in [-1,0,1]:
                # exclude own position
                if not (x == 0 and y == 0):
                    found = False # if the position has been found live yet
                    for pos in live_pos:
                        if pos == [(self.x + x), (self.y + y)]:
                            found = True
                    if found:
                        live_neighbours += 1
                    else:
                        dead_neighbours += 1
                        dead_neighbours_pos.append([(self.x + x), (self.y + y)])
        # compare live neighbours with rules
        self.nextState = True
        # death by underpopulation
        if live_neighbours < DeathByUnderpop:
            self.nextState = False
        # death by overpopulation
        if live_neighbours > DeathByOverpop:
            self.nextState = False

        #debug
        #if self.x == 1 and self.y == 1:
        #    print(f"live neighbours:{live_neighbours}, dead neighbours: {dead_neighbours}")
        #    print(f"state:{self.nextState}")


        #return dead neighbour positions found
        return dead_neighbours_pos


# endregion

# region instantiation and widgets

# Instance of the main window used
window = MainWindow()

# display grid for displaying the main grid used for the program
displayGrid = tk.Frame(background="black", width=2.5 * GridWidth, height=2.5 * GridWidth, master=window, borderwidth=3)
displayGrid.columnconfigure(GridWidth)
displayGrid.rowconfigure(GridWidth)
displayGrid.pack(side=tk.RIGHT, padx=35)

# creation of the 2d array for the display cell objects in the grid
displayCells = []
for X in range(GridWidth):
    displayCells.append([])
    for Y in range(GridWidth):
        displayCells[X].append(DisplayCell(X, Y, ((X + Y) % 2 == 0), displayGrid))

# speed slider used for the simulation speed
SimSpeed = tk.DoubleVar()
speedScale = tk.Scale(master=window, orient=tk.HORIZONTAL, label="speed", variable=SimSpeed, from_=0, to=100)

# places the slider underneath the grid
speedScale.place(in_=displayGrid, relx=0.4, rely=1, y=50)

# time control widgets to contain the start, stop, and step forward buttons
timeControl = tk.Frame(width=100, height=5, )
timeControl.rowconfigure(0)
timeControl.columnconfigure(3)
timeControl.place(in_=displayGrid, relx=0.35, rely=0, y=-50)

# Images
stepImg = tk.PhotoImage(file="stepForward.png")
playImg = tk.PhotoImage(file="play.png")
pauseImg = tk.PhotoImage(file="pause.png")


# step forward button to update one generation at a time
tk.Button(master=timeControl, image=stepImg).grid(row=0, column=2)

# play button for starting the simulation
tk.Button(master=timeControl, image=playImg).grid(row=0, column=0)

# pause button for stopping the simulation
tk.Button(master=timeControl, image=pauseImg).grid(row=0, column=1)


# endregion


# region functions

# updates the displayed version of the grid
def update_display(grid):
    pass

# main rule algorithm, applies one iteration of the rules to the actual grid
# takes in the list of the alive cells (classes) and the rule values (globals)
# also returns the same list of cells when done
def tick_rules(sim_cells):
    # list of the live and dead cell positions
    livePos = []
    # format for dead cells list: x, y, no. appearances
    deadCells = []
    # new dead cells found by a live cell
    newDeadCells = []

    for cell in sim_cells:
        livePos.append(cell.get_coords())
    for cell in sim_cells:
        newDeadCells = cell.find_next_state(livePos)
        # add new dead cells to list
        if deadCells == []:
            for pos in newDeadCells:
                deadCells.append([pos[0], pos[1], 1])
        else:
            for new_pos in newDeadCells:
                id = 0
                # if the position has been found
                found = False
                for old_pos in deadCells:
                    # if the new dead cell already exists, update it's counter
                    if new_pos == [old_pos[0], old_pos[1]]:
                        old_counter = old_pos[2]
                        deadCells[id] = [old_pos[0], old_pos[1], (old_counter + 1)]
                        found = True
                    id += 1
                if not found:
                    deadCells.append([new_pos[0], new_pos[1], 1])


    # debug
    #for i in livePos:
    #    print(i)
    #print("deadCells")
    #for i in deadCells:
    #    print(i)
    #for cell in sim_cells:
    #    print("sim cells")
    #    print(cell.x, cell.y, cell.nextState)

    # update cell states and add in new cells, for some reason this can be weird
    cellsDeleted = False
    while not cellsDeleted:
        for cell in sim_cells:
            if cell.nextState == False:
                sim_cells.remove(cell)

        # fixes issue
        cellsDeleted = True
        for cell in sim_cells:
            if cell.nextState == False:
                cellsDeleted = False



    # add new cells
    for cell in deadCells:
        if cell[2] == ParentsRequired:
            sim_cells.append(SimCell(cell[0], cell[1], True))

    #return the new cell list

    return sim_cells


# endregion

#test
sim_cells = []
for i in range(3):
    sim_cells.append(SimCell(i, 0, True))
for cell in sim_cells:
    print(cell.x, cell.y)
sim_cells = tick_rules(sim_cells)
print("sim")

for cell in sim_cells:
    print(cell.x, cell.y)

sim_cells = tick_rules(sim_cells)
print("sim")

for cell in sim_cells:
    print(cell.x, cell.y)


# main loop for the simulation
#window.mainloop()

