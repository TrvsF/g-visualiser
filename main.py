import tkinter as tk
import numpy   as np
import matplotlib.pyplot as plt

from tkinter import filedialog
from ast import literal_eval

class Gui(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # display base elements
        self.display_menu()

    def display_menu(self):
        # set window vars
        self.title   ("SSC")
        self.geometry("600x400")
        self.minsize (600, 400)

        # define fonts
        self.header_font  = ("System", 22, "bold")
        self.default_font = ("System", 12)

        # safe close
        self.protocol("WM_DELETE_WINDOW", self.safe_destroy)

        # menu frame
        self.menu_frame = tk.Frame(self,
            width  = 600,
            height = 400,
            bg     = "lightgrey"
        )

        # menu gui items
        self.title_text = tk.Label(self.menu_frame,
            text = "g-visualiser",
            bg   = "lightgrey",
            fg   = "black",
            font = self.header_font
        )
        self.file_button = tk.Button(self.menu_frame,
            text = "File",
            bg   = "lightgrey",
            fg   = "black",
            font = self.header_font,
            command = self.open_fileselect
        )

        # pack
        self.menu_frame.pack (fill=tk.BOTH, expand=1)
        self.title_text.pack (fill=tk.X, pady=(32, 28))
        self.file_button.pack(fill=tk.X, pady=(40, 28))

    def display_data(self):
        window = tk.Toplevel(self.menu_frame)
        window.title("DATA CHANGE ME")
        # TODO : rest

    def process_logs(self, data) -> list:
        population_data = []
        pop = 0
        for item in data:
            elements = item.split(":")
            event    = elements[0]
            time     = elements[2]

            pop += 1 if event == "BIRTH" else -1
            time = int(time) / 64

            population_data.append((time, pop))

        print(population_data)
        plt.plot(*zip(*population_data))
        plt.show()

        return population_data

    def process_agent(self, data):
        xs = []
        ys = []
        

    def open_fileselect(self):
        print("f")
        ftypes = [("g-sim files", "*.g")]
        dlg = filedialog.askopenfilename(initialdir="./", filetypes = ftypes)
    
        if dlg != "":
            self.read_file(dlg)

    def read_file(self, filename):
        file  = open(filename, "r")
        data  = file.read().splitlines()
        index = data.pop(0)

        if   "AGENT" in index:
            print("AGENT FILE")
        elif "LOGS"  in index:
            self.process_logs(data)

        # self.display_data()

    def safe_destroy(self) -> None:
        # stop any ongoing tasks
        print("deading...")
        self.destroy()

if __name__ == "__main__":
    print("starting g-visualiser")
    root = Gui()
    root.mainloop()