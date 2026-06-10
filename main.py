import tkinter as tk

# main window
class mainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("test")
        self.geometry("500x500")
        self.configure( bg= "gray")



window = mainWindow()



# display grid for displaying the main grid used for the program
displayGrid = tk.Frame(background="blue", width=100, height=100, master=window)
displayGrid.columnconfigure(10, minsize=10)
displayGrid.rowconfigure(10, minsize=10)
displayGrid.pack()



# classes

# cell used in grid display only, state is bool, True -> alive, False -> dead
class DisplayCell(tk.Frame):
    def __init__(self, x: int, y: int, state):
        super().__init__()
        self.x = x
        self.y = y
        self.state = state

        if self.state is None:
            self.state = False


        self.configure(width= 10, height= 10)


        # problem
        self.master(displayGrid)
        self.grid(row= self.x, column=self.y)

    # proceedure to update colour based on state
    def updateColour(self):
        if self.state:
            self.configure(bg= "black")
        else:
            self.configure(bg= "white")







#label1 = tk.Frame(bg= "black", master= displayGrid, width= 10, height= 10)
#label1.grid(row= 1, column= 2)
cell1 = DisplayCell(1,2,False)


window.mainloop()
