 # -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import json
import os
import fileinput
import shutil
import argparse
from subprocess import Popen, PIPE, STDOUT

config_dict = {}
entered_path = ""
#----------------------------------------------------------------------------------------------------------------------#


class Config_Flow(ttk.Frame):
    """ Configuration Tab. """

    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        with open("config.json", 'r') as f:
            config_dict = json.load(f)
        global entered_path
        entered_path.set(config_dict["entered_path"])

    def createWidgets(self):
        #text variables

        #labels
        self.label1 = ttk.Label(self, text="Please Enter the path:").grid(row=0, column=0, sticky=W)

        #My Photo
        #photo1 = PhotoImage(file="UNCC_FLOW_Image.png")
        #Label(window, image=photo1, bg="black") .grid(row=0, column=30, sticky=W)

        #text boxes
        self.textbox1 = ttk.Entry(self, textvariable=entered_path).grid(row=0, column=1, sticky=E)

        #button
        self.button1 = ttk.Button(self, text="Set Path").grid(row=3, column=1, sticky=E)
        self.button2 = ttk.Button(self, text="Save", command = self.save_config).grid(row=3, column=2, sticky=E)
        self.button2 = ttk.Button(self, text="Exit", command = window.destroy).grid(row=3, column=3, sticky=E)
        self.button2 = ttk.Button(self, text="Browse", command= self.browse_path ).grid(row=3, column=4, sticky=E)

    def browse_path(self):
        f = filedialog.askopenfile(parent=self,mode='rb',title='Choose Project Directory')
        entered_path.set(f.name)
        global config_dict
        config_dict['entered_path'] = entered_path.get()


    def save_config(self):
        with open("config.json", "w") as f:
            json.dump(config_dict, f)

#-------------------------------------------------------------------------------------------------------------------------#

class Automate_Flow(ttk.Frame):
    """ Automation FLow Tab """
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.OPTIONS = [
        "Make a selection",
        "sarlock",
        "fbki"
        ]
        self.method = StringVar(self)
        self.method.set("Make a selection")
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """Create the widgets for the GUI"""

        #text box
        self.label1 = ttk.Label(self, text="Step 1: File Configuration").grid(row=0, column=0, sticky=W)
        self.label1 = ttk.Label(self, text="Step 2: DC Compiler").grid(row=1, column=0, sticky=W)
        #self.label1 = ttk.Label(self, text="Step 3: Preinsertion TB").grid(row=2, column=0, sticky=W)
        #self.label1 = ttk.Label(self, text="Step 4: Run Vivado on Preinnsertionn Tb").grid(row=3, column=0, sticky=W)
        self.label1 = ttk.Label(self, text="Step 5: Choose also then run Logic Lock Algo").grid(row=4, column=0, sticky=W)
        #self.label1 = ttk.Label(self, text="Step 6: Run Post Insertion").grid(row=5, column=0, sticky=W)
        self.label1 = ttk.Label(self, text="Step 7: Run Final Vivado").grid(row=6, column=0, sticky=W)

        #buttons
        self.button1 = ttk.Button(self, text="Configurations", command=self.config_synthesis).grid(row=0, column=1, sticky=W)
        self.button2 = ttk.Button(self, text="DC Shell", command=self.dc_synthesis).grid(row=1, column=1, sticky=W)
    #    self.button3 = ttk.Button(self, text="Preinsert-TB").grid(row=2, column=1, sticky=W)
    #    self.button4 = ttk.Button(self, text="Vivado-Pre-TB").grid(row=3, column=1, sticky=W)
        self.button5 = ttk.Button(self, text="Logic Lock Algo", command = self.logic_insertion).grid(row=4, column=1, sticky=W)
        #self.button6 = ttk.Button(self, text="Postinsert-TB").grid(row=5, column=1, sticky=W)
        self.button7 = ttk.Button(self, text="Final Vivado Run").grid(row=6, column=1, sticky=W)
        self.button8 = ttk.Button(self, text="Clean", command=self.clean_env).grid(row=8, column=1, sticky=W)

        #Drop down
        self.dropdown = ttk.OptionMenu(self, self.method, *self.OPTIONS).grid(row=7, column=1, sticky=W)

    def clean_env(self):
        os.system("python3 automation_new.py -step clean_env -insert_method {} {}".format(self.method.get(), entered_path.get()))
        print("python3 automation_new.py -step clean_env -insert_method {} {}".format(self.method.get(), entered_path.get()))

    def config_synthesis(self):
        os.system("python3 automation_new.py -step config_synthesis -insert_method {} {}".format(self.method.get(), entered_path.get()))
        print("python3 automation_new.py -step config_synthesis -insert_method {} {}".format(self.method.get(), entered_path.get()))

    def dc_synthesis(self):
        os.system("python3 automation_new.py -step dc_synthesis -insert_method {} {}".format(self.method.get(), entered_path.get()))
        print("python3 automation_new.py -step dc_synthesis -insert_method {} {}".format(self.method.get(), entered_path.get()))

    def logic_insertion(self):
        os.system("python3 automation_new.py -step lock_insertion -insert_method {} {}".format(self.method.get(), entered_path.get()))
        print("python3 automation_new.py -step lock_insertion -insert_method {} {}".format(self.method.get(), entered_path.get()))




#---------------------------------------------------------------------------------------------------------------------------------#

class FPGA_Comms(ttk.Frame):
    """ FPGA Communication """
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """Create the widgets for the GUI"""

        #text box
        self.label1 = ttk.Label(self, text="Communication with SQL Database and sending Key to FPGA").grid(row=0, column=0, sticky=W)

        #buttons
        self.button1 = ttk.Button(self, text="Display Key").grid(row=1, column=0, sticky=S)
        self.button2 = ttk.Button(self, text="Request Key").grid(row=2, column=0, sticky=S)
        self.button2 = ttk.Button(self, text="Flash FPGA").grid(row=3, column=0, sticky=S)

#--------------------------------------------------------------------------------------------------------------------------------------------#

class Results_Flow(ttk.Frame):
    """ Results Tab. """
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """Create the widgets for the GUI"""

        #text box
        self.label1 = ttk.Label(self, text="See the Results so far here").grid(row=0, column=0, sticky=W)

        # Buttons for Results
        self.button1 = ttk.Button(self, text="View Key").grid(row=1, column=0, sticky=S)
        self.button2 = ttk.Button(self, text="View Logs").grid(row=2, column=0, sticky=S)
        self.button3 = ttk.Button(self, text="View Output").grid(row=3, column=0, sticky=S)

#--------------------------------------------------------------------------------------------------------------------------------------#

class Hope_Flow(ttk.Frame):
    """ Hope Tab. """
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """Create the widgets for the GUI"""

        #text box
        self.label1 = ttk.Label(self, text="Hope Integration for generating test patterns").grid(row=0, column=0, sticky=W)

        #buttons
        self.button1 = ttk.Button(self, text="Combinational-TB").grid(row=1, column=0, sticky=S)
        self.button2 = ttk.Button(self, text="Sequential-TB").grid(row=2, column=0, sticky=S)
        self.button2 = ttk.Button(self, text="Exit").grid(row=3, column=0, sticky=S)

#--------------------------------------------------------------------------------------------------------------------------------------------#

class Post_Flow(ttk.Frame):
    """ Post Tab. """
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """Create the widgets for the GUI"""

        #text box
        self.label1 = ttk.Label(self, text="Last step. exxit app, save to config file, or clear everything").grid(row=0, column=0, sticky=W)

        #buttons
        self.button1 = ttk.Button(self, text="Exit").grid(row=1, column=0, sticky=S)
        self.button2 = ttk.Button(self, text="Save State").grid(row=2, column=0, sticky=S)
        self.button2 = ttk.Button(self, text="Clear").grid(row=3, column=0, sticky=S)




#----------------------------------------------------------------------------------------------------------------------------------------------------#

def main():
    #Setup Tk()
    global window
    window = Tk()
    window.title("UNCC FLOW App")
    global entered_path
    entered_path = StringVar()
    #Setup the notebook (tabs)
    notebook = ttk.Notebook(window)
    frame1 = ttk.Frame(notebook)
    frame2 = ttk.Frame(notebook)
    frame3 = ttk.Frame(notebook)
    frame4 = ttk.Frame(notebook)
    frame5 = ttk.Frame(notebook)
    frame6 = ttk.Frame(notebook)
    notebook.add(frame1, text="Config")
    notebook.add(frame2, text="Automate")
    notebook.add(frame3, text="FPGA Comm")
    notebook.add(frame4, text="Results")
    notebook.add(frame5, text="Hope")
    notebook.add(frame6, text="Post")
    notebook.grid()

    #Create tab frames
    config_tab = Config_Flow(master=frame1)
    config_tab.grid()

    automate_tab = Automate_Flow(master=frame2)
    automate_tab.grid()

    results_tab = FPGA_Comms(master=frame3)
    results_tab.grid()

    results_tab = Results_Flow(master=frame4)
    results_tab.grid()

    hope_tab = Hope_Flow(master=frame5)
    hope_tab.grid()

    post_tab = Post_Flow(master=frame6)
    post_tab.grid()





    #Main loop
    window.mainloop()

if __name__ == '__main__':
    main()
