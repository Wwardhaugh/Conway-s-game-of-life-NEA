# region imports
import tkinter as tk
import csv

# endregion

# region globals

# width of the grid that is displayed, the real grid has unlimited size
GridWidth = 40  # note that higher values tend to lead to lag when resizing

# colour customization of the cells
AliveCol = "black"
DeadCol = "white"

# rule values used for simulation
DeathByUnderpop = 2  # default 2
DeathByOverpop = 3  # default 3
ParentsRequired = 3  # default 3

# global delay between ticks
Delay = 500

# boolean for if the simulation is running or not
Running = False


# procedure to pause simulation
def pause():
    global Running
    Running = False


# procedure to unpause simulation
def unpause():
    global Running
    Running = True


# Main grid for the simulation cells
SimCells = []

# new cells added by the user editing the grid, this is wiped each "tick"
newCells = []

# same as last list, but for cells scheduled to be deleted
removedCells = []

# Dictionary for the presets of the simulation, in the form PresetName: 2d list of live cell coords
PresetsDict = {
    "Glider": [[18, 18], [17, 19], [18, 19], [18, 17], [16, 18]],
    "Blinker": [[14, 16], [13, 16], [15, 16]],
    "Block": [[16, 18], [16, 19], [17, 19], [17, 18]],
    "Pentadecathlon": [[10, 19], [11, 19], [12, 18], [12, 20], [13, 19], [14, 19], [15, 19], [16, 19], [17, 18],
                       [17, 20], [18, 19], [19, 19]],
    "Gosper Glider Gun": [[8, 2], [8, 3], [9, 3], [9, 2], [8, 12], [9, 12], [10, 12], [7, 13], [11, 13], [12, 14],
                          [12, 15], [6, 14], [6, 15], [9, 16], [9, 18], [8, 18], [10, 18], [11, 17], [7, 17], [9, 19],
                          [8, 22], [8, 23], [7, 23], [7, 22], [6, 22], [6, 23], [5, 24], [9, 24], [9, 26], [10, 26],
                          [5, 26], [4, 26], [6, 36], [6, 37], [7, 37], [7, 36]],
    "Die Hard": [[20, 16], [19, 16], [19, 15], [20, 20], [20, 21], [20, 22], [18, 21]],
    "Big Glider": [[35, 29], [34, 28], [34, 30], [34, 31], [35, 32], [34, 32], [33, 32], [33, 33], [32, 32], [32, 31],
                   [32, 34], [31, 34], [31, 33], [30, 33], [31, 35], [31, 36], [30, 35], [29, 35], [28, 36], [27, 35],
                   [31, 29], [31, 28], [30, 28], [30, 29], [32, 27], [31, 26], [30, 26], [30, 27], [29, 27], [28, 26],
                   [28, 24], [27, 24], [28, 23], [27, 22], [25, 23], [24, 21], [24, 20], [25, 20], [26, 20], [23, 19],
                   [22, 19], [21, 19], [21, 20], [22, 21], [20, 23], [19, 22], [18, 22], [18, 23], [18, 24], [19, 25],
                   [20, 25], [19, 26], [19, 27], [22, 26], [22, 29], [21, 28], [23, 28], [23, 29], [25, 29], [26, 30],
                   [26, 31], [25, 31], [25, 32], [26, 33], [27, 32], [27, 31], [28, 31], [28, 32]],
    "Backrake": [[37, 17], [37, 19], [36, 20], [35, 20], [34, 20], [33, 20], [32, 20], [31, 20], [31, 19], [31, 18],
                 [32, 17], [35, 16], [34, 16], [30, 15], [31, 13], [31, 11], [30, 11], [29, 11], [29, 12], [29, 13],
                 [32, 25], [32, 26], [30, 25], [29, 25], [29, 24], [29, 23], [27, 22], [27, 21], [27, 19], [28, 19],
                 [26, 19], [25, 19], [24, 19], [24, 20], [28, 17], [27, 17], [26, 17], [25, 17], [24, 17], [24, 16],
                 [27, 15], [27, 14], [25, 14], [24, 14], [23, 14], [22, 14], [23, 15], [21, 13], [20, 12], [20, 11],
                 [20, 10], [21, 9], [22, 9], [23, 9], [24, 9], [25, 10], [23, 11], [23, 12], [22, 8], [23, 7], [24, 7],
                 [24, 6], [25, 5], [27, 5], [27, 6], [23, 21], [23, 22], [22, 22], [24, 22], [25, 22], [21, 23],
                 [20, 24], [20, 25], [20, 26], [21, 27], [22, 27], [23, 27], [24, 27], [25, 26], [23, 25], [23, 24],
                 [22, 28], [23, 29], [24, 29], [24, 30], [25, 31], [27, 31], [27, 30]],

}


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


# triggers if a display cell is clicked to update the grid accordingly
def click_frame(event):
    # ony allow the cells to be updated if the simulation is paused
    if not Running:
        event.widget.state = not event.widget.state
        event.widget.update_colour()
        pos = [event.widget.x, event.widget.y]
        # if the cell changed to be live
        if event.widget.state:
            # if the position was going to be deleted, change it to be added
            if pos in removedCells:
                removedCells.remove(pos)

            if pos not in newCells:
                newCells.append(pos)

        # if the cell changed to be dead
        else:
            # if the position was going to be added, change it to be deleted
            if pos in newCells:
                newCells.remove(pos)

            if pos not in removedCells:
                removedCells.append(pos)


# cell used in grid display only, state is bool, True -> alive, False -> dead
class DisplayCell(tk.Frame):
    def __init__(self, x: int, y: int, state: bool, master):
        super().__init__(master=master)
        self.x = x
        self.y = y
        self.state = state
        self.bind("<Button-1>", click_frame)

        # used to set the state to dead by default
        if self.state is None:
            self.state = False

        # set initial colour
        if self.state:
            self.configure(bg=AliveCol)
        else:
            self.configure(bg=DeadCol)

        # set cell size relative to the grid width
        self.configure(width=(400 / GridWidth), height=(400 / GridWidth), highlightbackground="gray",
                       highlightthickness=0.5)

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

    # debug message
    def __del__(self):
        # print(f"cell at {self.x}, {self.y} has died")
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
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                # exclude own position
                if not (x == 0 and y == 0):
                    found = False  # if the position has been found live yet
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

        # return dead neighbour positions found
        return dead_neighbours_pos


# endregion


# region functions


# main rule algorithm, applies one iteration of the rules to the actual grid
# takes in the list of the alive cells (classes) and the rule values (globals)
# also returns the same list of cells when done
def tick_rules(sim_cells):
    # list of the live and dead cell positions
    livePos = []
    # format for dead cells list: x, y, no. appearances
    deadCells = []
    # new dead cells found by a live cell

    for cell in sim_cells:
        livePos.append(cell.get_coords())
    for cell in sim_cells:
        newDeadCells = cell.find_next_state(livePos)
        # add new dead cells to list
        if not deadCells:  # if list is empty
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
    # for i in livePos:
    #    print(i)
    # print("deadCells")
    # for i in deadCells:
    #    print(i)
    # for cell in sim_cells:
    #    print("sim cells")
    #    print(cell.x, cell.y, cell.nextState)

    # update cell states and add in new cells, for some reason this can be weird
    cellsDeleted = False
    while not cellsDeleted:
        for cell in sim_cells:
            if not cell.nextState:
                sim_cells.remove(cell)

        # fixes issue
        cellsDeleted = True
        for cell in sim_cells:
            if not cell.nextState:
                cellsDeleted = False

    # add new cells
    for cell in deadCells:
        if cell[2] == ParentsRequired:
            sim_cells.append(SimCell(cell[0], cell[1], True))

    # return the new cell list

    return sim_cells


# procedure to reset the grid
def grid_reset():
    global SimCells
    global Running
    Running = False
    SimCells = []
    update_display(SimCells)


# exports the current grid state as a csv file
def export_grid():
    if not Running:
        update_sim_cells()
        liveCells = []
        for cell in SimCells:
            liveCells.append([cell.x, cell.y])

        with open("output.csv", 'w', newline='') as f:
            f.truncate()
            writer = csv.writer(f)
            writer.writerows(liveCells)


# imports a grid state from a csv, or via a list input
def import_grid(preset):
    global SimCells
    if not Running:
        # if there are cells input, then a preset is being loaded
        if preset is not None:
            grid_reset()
            # fetch the coords of live cells from preset dictionary
            liveCells = PresetsDict.get(preset)
            for cell in liveCells:
                SimCells.append(SimCell(cell[0], cell[1], True))
            update_display(SimCells)
        # otherwise import via a csv
        else:
            grid_reset()
            with open("output.csv", "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    SimCells.append(SimCell(int(row[0]), int(row[1]), True))
                update_display(SimCells)


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
        displayCells[X].append(DisplayCell(X, Y, False, displayGrid))


# updates the displayed version of the grid, takes in the list of the sim cells
def update_display(sim_cells):
    global displayCells
    # list of live cell positions
    live_pos = []
    for cell in sim_cells:
        live_pos.append([cell.x, cell.y])
    for X in range(GridWidth):
        for Y in range(GridWidth):
            cell = displayCells[X][Y]
            # if the cell has been found in the list of live positions
            found = False
            for pos in live_pos:
                if cell.x == pos[0] and cell.y == pos[1]:
                    found = True
            cell.state = found
            cell.update_colour()


# adds and removes cells from user editing the grid
def update_sim_cells():
    global SimCells
    global newCells
    global removedCells

    # delete removed cells
    for cell in SimCells:
        if [cell.x, cell.y] in removedCells:
            SimCells.remove(cell)
    removedCells = []

    # add new cells
    for cell in newCells:
        SimCells.append(SimCell(cell[0], cell[1], True))
    newCells = []


def button_tick():
    global SimCells
    update_sim_cells()
    SimCells = tick_rules(SimCells)
    update_display(SimCells)


# calculate new delay
def calc_Delay(speed):
    speed = int(speed)
    global Delay
    Delay = 1000 * ((101 - speed) / 100)


# speed slider used for the simulation speed
SimSpeed = tk.DoubleVar()
speedScale = tk.Scale(master=window, orient=tk.HORIZONTAL, label="speed", variable=SimSpeed, from_=1, to=100,
                      command=calc_Delay)

# places the slider underneath the grid
speedScale.place(in_=displayGrid, relx=0.4, rely=1, y=50)

# Images
stepImg = tk.PhotoImage(file="stepForward.png")
playImg = tk.PhotoImage(file="play.png")
pauseImg = tk.PhotoImage(file="pause.png")

# time control widgets to contain the start, stop, and step forward buttons
timeControl = tk.Frame(width=100, height=5, )
timeControl.rowconfigure(0)
timeControl.columnconfigure(4)
timeControl.place(in_=displayGrid, relx=0.35, rely=0, y=-50)

# step forward button to update one generation at a time
tk.Button(master=timeControl, image=stepImg, command=button_tick).grid(row=0, column=2)

# play button for starting the simulation
tk.Button(master=timeControl, image=playImg, command=unpause).grid(row=0, column=0)
# pause button for stopping the simulation
tk.Button(master=timeControl, image=pauseImg, command=pause).grid(row=0, column=1)
# button to reset the grid state
tk.Button(master=timeControl, text="reset grid", command=grid_reset).grid(row=0, column=3)


# function for updating rule values, takes in the widget that updated
def rule_update():
    if not Running:
        global DeathByUnderpop
        global DeathByOverpop
        global ParentsRequired
        DeathByUnderpop = int(minPar.get())
        DeathByOverpop = int(maxPar.get())
        ParentsRequired = int(reqPar.get())


# widget for the rules
rulesWidget = tk.Frame(width=20, height=100)
rulesWidget.columnconfigure(1)
rulesWidget.rowconfigure(3)
rulesWidget.pack(side=tk.LEFT, padx=100)

# variables to set default values of the spin boxes
initUnderpop = tk.StringVar(window)
initUnderpop.set(2)
initOverpop = tk.StringVar(window)
initOverpop.set(3)
initPar = tk.StringVar(window)
initPar.set(3)

tk.Label(master=rulesWidget, text="Minimum neighbours").grid(row=0, column=0)

minPar = tk.Spinbox(master=rulesWidget, from_=1, to=8, command=rule_update, repeatdelay=500, repeatinterval=100,
                    textvariable=initUnderpop)
minPar.grid(row=0, column=1)

tk.Label(master=rulesWidget, text="Maximum neighbours").grid(row=1, column=0)

maxPar = tk.Spinbox(master=rulesWidget, from_=1, to=8, command=rule_update, repeatdelay=500, repeatinterval=100,
                    textvariable=initOverpop)
maxPar.grid(row=1, column=1)

tk.Label(master=rulesWidget, text="Required parents").grid(row=2, column=0)

reqPar = tk.Spinbox(master=rulesWidget, from_=1, to=8, command=rule_update, repeatdelay=500, repeatinterval=100,
                    textvariable=initPar)
reqPar.grid(row=2, column=1)

# widget for the import and export buttons
importExport = tk.Frame()
importExport.columnconfigure(2)
importExport.rowconfigure(0)
importExport.place(in_=rulesWidget, relx=0.5, rely=0, y=-60)

# import button
tk.Button(master=importExport, text="Import grid", command=lambda: import_grid(None)).grid(row=0, column=0)

# export button
tk.Button(master=importExport, text="Export grid", command=export_grid).grid(row=0, column=1)


# listbox function
def preset_update(event):
    preset = presetListbox.get(presetListbox.curselection())
    import_grid(preset)


# dropdown for the preset selection
presetLabel = tk.Label(text="Presets:")
presetLabel.place(in_=importExport, x=200)
presetListbox = tk.Listbox(selectmode=tk.SINGLE)
presetListbox.place(in_=presetLabel, relx=0, y=40)
presetListbox.bind('<<ListboxSelect>>', preset_update)

# insert the names for the presets in the presets dictionary
for key in PresetsDict.keys():
    presetListbox.insert(tk.END, str(key))


# endregion


# update
def update():
    global Delay
    # print("Update")
    if Running:
        button_tick()
    window.after(int(Delay), update)


# continuous updates
update()

# main loop for the simulation
window.mainloop()
