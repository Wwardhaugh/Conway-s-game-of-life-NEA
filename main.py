# region imports

import tkinter as tk


# endregion

# region globals

# width of the grid that is displayed, the real grid has unlimited size
GridWidth = 20  # note that higher values tend to lead to lag when resizing

# colour customization of the cells
AliveCol = "black"
DeadCol = "white"


# endregion


# region classes

# main window
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("test")
        self.geometry("500x500")
        self.configure(bg="gray")
        # self.attributes("-fullscreen", True)


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
        self.configure(width=400/GridWidth, height=400/GridWidth)

        # set the position in the displayGrid widget
        self.grid(row=self.x, column=self.y)

    # procedure to update colour based on state
    def update_colour(self):
        if self.state:
            self.configure(bg=AliveCol)
        else:
            self.configure(bg=DeadCol)


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
        displayCells[X].append(DisplayCell(X, Y, ((X+Y) % 2 == 0), displayGrid))


# speed slider used for the simulation speed
SimSpeed = tk.DoubleVar()
speedScale = tk.Scale(master=window, orient=tk.HORIZONTAL, label="speed", variable=SimSpeed, from_=0, to=100)

# places the slider underneath the grid
speedScale.place(in_=displayGrid, relx=0.4, rely=1, y=50)

# time control widgets to contain the start, stop, and step forward buttons
timeControl = tk.Frame(width=100, height=5, )
timeControl.rowconfigure(0)
timeControl.columnconfigure(3)
timeControl.place(in_=displayGrid, relx=0.5, rely=0, y=-50)


stepForward = tk.Button(master=timeControl, width=4, height=2, image=tk.PhotoImage(file="stepForward.png"))
stepForward.grid(row=0, column=0)



# endregion


# main loop for the simulation
window.mainloop()
