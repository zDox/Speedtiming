from time import time
from tkinter import *
from tkinter.ttk import Treeview

import threading as tr

from network_server import NetworkServer
import constants as const
from writer import write_session


class GUI:
    def __init__(self):
        self.network_server = NetworkServer()
        self.lanes = []
        thread = tr.Thread(target=self.network_server.start, daemon=True)
        thread.start()
        update_time = tr.Thread(target=self.update_time, daemon=True)
        update_time.start()

        self.root = Tk()
        self.root.title("Chat APP")

        self.root.resizable(width=True,
                            height=True)
        self.root.configure(width=470,
                            height=550,
                            bg="#17202A")
        self.setup_root()

        self.update()

        self.root.mainloop()

    def setup_root(self):

        # Create Treeview Frame
        frame = Frame(self.root)
        frame.pack(pady=20)

        # Treview Scrollbar
        table_scroll = Scrollbar(frame)
        table_scroll.pack(side=RIGHT, fill=Y)

        self.table = Treeview(frame, height=35, yscrollcommand=table_scroll.set)
        self.table["columns"] = ("Run ID", "Lane ID", "Time", "Distance")
        self.table.column("#0", width=0, stretch=NO)
        self.table.column("Run ID", minwidth=70)
        self.table.column("Lane ID", minwidth=70)

        self.table.heading("#0", text="")
        self.table.heading("Run ID", text="Run ID")
        self.table.heading("Lane ID", text="Lane ID")
        self.table.heading("Time", text="Time")
        self.table.heading("Distance", text="Distance")

        self.table.pack()

        table_scroll.config(command=self.table.yview)

        label_button = Label(self.root,
                             height=40,
                             width=1,
                             background="#17202A")

        label_button.place(relwidth=1,
                           rely=0.825)

        self.label_time = Label(self.root,
                                text="00.0000",
                                font="Arial 20 bold",
                                bg="#17202A",
                                fg="#f92713"
                                )

        self.label_time.place(relx=0.45,
                              rely=0.75)

        button_start = Button(label_button,
                              text="Start Run",
                              font="Arial 10 bold",
                              width=1,
                              bg="#4BB543",
                              command=self.network_server.start_run)

        button_start.place(relx=0.01,
                           rely=0.01,
                           relheight=0.06,
                           relwidth=0.22)

        button_save = Button(label_button,
                             text="Save Session",
                             font="Arial 10 bold",
                             width=1,
                             bg="#3E5780",
                             command=lambda: write_session(self.table, self.network_server.runs))

        button_save.place(relx=0.32,
                          rely=0.01,
                          relheight=0.06,
                          relwidth=0.22)

        button_stop = Button(label_button,
                             text="Stop Run",
                             font="Arial 10 bold",
                             width=1,
                             bg="#f92713",
                             command=self.stop_current_run)

        button_stop.place(relx=0.01,
                          rely=0.09,
                          relheight=0.06,
                          relwidth=0.22)

    def update(self):
        if self.network_server.runs:
            self.update_table()
        self.root.after(1000, self.update)  # run itself again after 1000 ms

    def update_table(self):
        for run in self.network_server.runs:
            for i, lane in enumerate(run.lanes.items()):
                if lane not in self.lanes:
                    row = run.id * const.LANE_COUNT + lane[0]
                    self.table.insert(parent="", index="end", iid=row, text=row,
                                      values=(run.id, lane[0], lane[1]["total_time"], lane[1]["distance"]))
                    self.table.pack(pady=20)
                    self.lanes.append(lane)

    def update_time(self):
        while True:
            if self.network_server.runs:
                latest_run = self.network_server.runs[-1]
                if latest_run.running:
                    if self.label_time.cget("fg") == "#f92713":
                        self.label_time.configure(fg="#4BB543")
                    self.label_time.configure(text=round(time() - latest_run.start_time, 4))
                    self.label_time.update()
                # Checks if label is not already red
                elif not latest_run.running and self.label_time.cget("fg") != "#f92713":
                    self.label_time.configure(fg="#f92713")
                    self.label_time.update()

    def stop_current_run(self):
        if self.network_server.runs:
            current_run = self.network_server.runs[-1]
            current_run.running = False


if __name__ == '__main__':
    g = GUI()
