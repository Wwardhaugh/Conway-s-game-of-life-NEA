# region imports

import tkinter as tk

# endregion


# region globals

# width of the grid that is displayed, the real grid has unlimited size
GridWidth = 20

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

        # set cell size
        self.configure(width=10, height=10)

        # set the position in the displayGrid widget
        self.grid(row=self.x, column=self.y)

    # procedure to update colour based on state
    def update_colour(self):
        if self.state:
            self.configure(bg=AliveCol)
        else:
            self.configure(bg=DeadCol)


# endregion


# region instantiation

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

# endregion


# main loop for the simulation
window.mainloop()
