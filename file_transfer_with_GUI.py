import tkinter as tk
from tkinter import *
import tkinter.filedialog
import os
from os.path import join
import shutil
import time
from datetime import datetime

import schedule
import time
import threading

class ParentWindow(Frame):
    def __init__(self, master):
        Frame.__init__(self)
        # sets title of GUI
        self.master.title("File Transer")

        #Creates button to select files from source directory
        self.sourceDir_btn = Button(text="Select Source", width=20, command=self.sourceDir)

        #Positions source button in GUI using tkinter grid()
        self.sourceDir_btn.grid(row=0, column=0, padx=(20, 10), pady= (30, 0))

        #Creates entry for source directory selection
        self.source_dir = Entry(width=75)

        #Positions entry in GUI using tkinter grid() padx and pady are the same as
        #the button to ensure they will line up
        self.source_dir.grid(row=0, column=1, columnspan=2, padx= (20, 10), pady=(30, 0))

        #Creates button to select destination of files from destination directory
        self.destDir_btn = Button(text="Select Destination", width=20, command=self.destDir)

        #Positions destination button in GUI using tkinter grid()
        #on the next row under the source button
        self.destDir_btn.grid(row=1, column=0, padx=(20, 10), pady= (15, 10))

        #Creates entry for destination directory selection
        self. destination_dir = Entry(width=75)

        #Positions entry in GUI using tkinter grid() padx and pady are the same as #the button to ensure they will line up
        self.destination_dir.grid(row=1, column=1, columnspan=2, padx=(20, 10), pady= (15, 10))

        #Creates button to transfer files
        self.transfer_btn = Button(text="Transfer Files", width=20, command=self.transferFiles)
        #Positons transfer files button
        self.transfer_btn.grid(row=2, column=1, padx= (200, 0), pady= (0, 15))

        #Creates an Exit button
        self.exit_btn = Button(text="Exit", width=20, command=self.exit_program)
        #Positions the Exit button
        self.exit_btn.grid(row=2, column=2, padx=(10, 40), pady= (0, 15))

    #Creates function to select source directory.
    def sourceDir (self) :
        selectSourceDir = tkinter.filedialog.askdirectory()
        #The •delete(0, END) will clear the the content that is inserted in the Entry widget,
        #this allows the path to be inserted into the Entry widget properly.
        self.source_dir.delete(0, END)
        #The insert method will insert the user selection to the source_dir Entry
        self.source_dir.insert(0, selectSourceDir)

    #Creates function to select desitnation directory.
    def destDir (self):
        selectDestDir= tkinter.filedialog.askdirectory ()
        #The delete(0, END) will clear the the content that is inserted in the Entry widget,
        #this allows the path to be inserted into the Entry widget properly.
        self.destination_dir.delete(0, END)
        #The insert method will insert the user selection to the destination_dir Entry widget
        self.destination_dir.insert(0, selectDestDir)

    # Creates function to transfer files from one directory to another
    def transferFiles (self):
        #Gets source directory
        source = self.source_dir.get()
        print(type(source))
        #Gets destination directory
        destination = self.destination_dir.get()
        #Gets a list of files in the source directory
        source_files = os.listdir(source)
        #Runs through each file in the source directory
        for i in source_files:
            #moves each file from the source to the destination
            shutil.move(source + '/' + i, destination)
            print (i + ' was successfully transferred.')

    #Creates function to exit program
    def exit_program (self) :
        #root is the main GUI window, the Tkinter destroy method
        #tells python to terminate root.mainloop and all widgets inside the GUI window
        root. destroy ()

def runContinuously(interval=1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run

def autoTransferFiles(source, destination):
    for file in os.listdir(source):
        # check if file is hidden
        if not file.startswith('.'):
            # get time in seconds and convert to datetime object
            modification_time = datetime.fromtimestamp(os.path.getmtime(join(source, file)))
            current_time = datetime.fromtimestamp(time.time())

            # get time difference in seconds
            delta = current_time - modification_time
            sec = delta.total_seconds()

            # get time difference in hours
            hours = sec / (60 * 60)

            # add file if new or modified in the last 24 hours
            if hours < 24:
                shutil.move(source + '/' + file, destination)
                print (file + ' was successfully transferred.')


if __name__ == "__main__":
    root = tk.Tk()
    App = ParentWindow(root)

    # run auto transfer of files in the background
    stop_run_continuously = runContinuously()

    # run job AFTER and every 24 hours since the program started
    schedule.every(24).hours.do(autoTransferFiles, source="/Users/jonahmarc/Desktop/Customer Source", destination="/Users/jonahmarc/Desktop/Customer Destination")

    # run scheduled job right away when program is started regardless of the schedule
    schedule.run_all()

    root.mainloop()

    # stop auto transfer of files in the background
    stop_run_continuously.set()