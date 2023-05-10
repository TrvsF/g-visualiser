import re
import os
import tkinter as tk
import matplotlib.pyplot as plt

from tkinter import filedialog
from ast import literal_eval

class Gui(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.current_dir = ""

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
        colour_data     = []
        colour_dict     = {}
        pop = 0
        for item in data:
            elements = item.split(":")
            event    = elements[0]
            agentid  = elements[1]
            time     = elements[2]
            time     = int(time) / 64
            
            colour = self.get_colour_from_id(agentid)

            if event == "BIRTH":
                pop += 1
                if colour is not None:
                    colour_dict[colour] = colour_dict.get(colour, 0) + 1
            else:
                if colour is not None:
                    colour_dict[colour] = colour_dict.get(colour, 0) - 1
                pop -= 1

            colour_data.append((time, colour_dict.copy()))
            population_data.append((time, pop))


        # plot graph
        plt.close("population")
        plt.figure("population")
        plt.plot(*zip(*population_data))
        plt.xlabel("time (seconds)")
        plt.ylabel("agent population")
        # plot foreach colour
        currentcolour = []
        for key in colour_dict.keys():
            for time, d in colour_data:
                if key in d:
                    currentcolour.append((time, d[key]))
            ctuple   = literal_eval(key)
            cutple_n = tuple(c/255 for c in ctuple)
            plt.plot(*zip(*currentcolour), color=cutple_n)
            currentcolour.clear()
        # show charts
        plt.show()

        return population_data
    
    def get_colour_from_id(self, id):
        filename = f"{self.current_dir}/agents/{id}.g"
        file  = open(filename, "r")

        data  = file.read().splitlines()
        index = data.pop(0)

        if len(data) == 0:
            return
        
        datapoints = data[0].split(":")
        colour = datapoints[1]
        
        return colour
    
    def display_agent_data(self, name, colour, shapes, age=0, children=0, damage=0):
        shapelist = re.split("(\([^)]*\))", shapes)[1::2]
        tuplelist = []
        xs = []
        ys = []
        for shape in shapelist:
            tup = literal_eval(shape)
            tuplelist.append(tup)

            xs.append(tup[0])
            ys.append(tup[1])

        xs.append(xs[0])
        ys.append(ys[0])

        ctuple   = literal_eval(colour)
        cutple_n = tuple(c/255 for c in ctuple)

        print(f"age={age}(s)\nchildren={children}\ndamage={damage}")

        plt.close()
        plt.figure(name)
        plt.axis('off')
        plt.plot(xs, ys, color=cutple_n)
        plt.show()

    def process_agent(self, data, display=False):
        datapoints = data.split(":")
        
        name   = datapoints[0]
        colour = datapoints[1]
        shapes = datapoints[2]
        age    = 0
        kids   = 0
        damage = 0

        isdead = len(datapoints) > 4
        if isdead:
            age    = round(int(datapoints[3]) / 64, 1)
            kids   = datapoints[4]
            damage = datapoints[5]

        if display:
            self.display_agent_data(name, colour, shapes, age, kids, damage) if isdead else self.display_agent_data(name, colour, shapes)

        return (name, colour, shapes, age, kids, damage)

    def open_fileselect(self):
        ftypes = [("g-sim files", "*.g")]
        dlg = filedialog.askopenfilename(initialdir="./", filetypes = ftypes)
    
        if dlg != "":
            self.read_file(dlg)

    def read_file(self, filename):
        file  = open(filename, "r")
        data  = file.read().splitlines()
        index = data.pop(0)

        self.current_dir = os.path.dirname(filename)

        if   "AGENT" in index:
            self.process_agent(data[0], display=True)
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