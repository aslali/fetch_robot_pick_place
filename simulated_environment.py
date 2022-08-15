# import tkinter
# import tkinter
import tkinter
from tkinter import *
import math

# from mttkinter import mtTkinter


class SHSCPackaging:
    a = 1

    def __init__(self, pattern, fast_run=False):
        self.root = tkinter.Tk()
        self.canvas = None

        self.field_width = 1700
        self.field_length = 900

        self.pattern_table_x = 100
        self.pattern_table_y = 100
        self.pattern_table_cell = 60
        self.pattern = pattern

        self.workspace_table_width = 200
        self.workspace_table_length = 860
        self.workspace_table_x = (self.field_width - self.workspace_table_width) // 2
        self.workspace_table_y = (self.field_length - self.workspace_table_length) // 2

        self.workspaces_r = 75
        self.workspace1_x0 = self.workspace_table_x + self.workspace_table_width // 2 - self.workspaces_r
        self.workspace1_y0 = self.workspace_table_y + 10

        self.workspace2_x0 = self.workspace1_x0
        self.workspace2_y0 = self.workspace_table_y + self.workspace_table_length//5 + 10

        self.workspace3_x0 = self.workspace1_x0
        self.workspace3_y0 = self.workspace_table_y + 2*self.workspace_table_length//5 + 10

        self.workspace4_x0 = self.workspace1_x0
        self.workspace4_y0 = self.workspace_table_y + 3*self.workspace_table_length//5 + 10

        self.workspace5_x0 = self.workspace1_x0
        self.workspace5_y0 = self.workspace_table_y + 4*self.workspace_table_length//5 + 10

        self.boxes_width = 20
        self.compartments = {1: [], 2: [], 3: [], 4: [], 5: []}
        self.w1b_x0, self.w1b_y0 = self.boxes_x_y(self.workspace1_x0, self.workspace1_y0)
        self.ws1_box_pos = []

        self.w2b_x0, self.w2b_y0 = self.boxes_x_y(self.workspace2_x0, self.workspace2_y0)
        self.ws2_box_pos = []

        self.w3b_x0, self.w3b_y0 = self.boxes_x_y(self.workspace3_x0, self.workspace3_y0)
        self.ws3_box_pos = []

        self.w4b_x0, self.w4b_y0 = self.boxes_x_y(self.workspace4_x0, self.workspace4_y0)
        self.ws4_box_pos = []

        self.w5b_x0, self.w5b_y0 = self.boxes_x_y(self.workspace5_x0, self.workspace5_y0)
        self.ws5_box_pos = []

        self.creat_env()
        # self.update = not fast_run

    def boxes_x_y(self, x0, y0):
        ys = []
        xs = []
        for i in range(1, 5):
            ys.append(y0 + self.workspaces_r // 2 + (i%2) * self.workspaces_r - self.boxes_width // 2)
            xs.append(x0 + self.workspaces_r // 2 + math.ceil(i/2) * self.workspaces_r//3 - self.boxes_width // 2)
        ys.append(y0 + self.workspaces_r - self.boxes_width // 2)
        xs.append(x0 + self.workspaces_r // 2 + 3 * self.workspaces_r//3 - self.boxes_width // 2)
        return xs, ys

    def creat_env(self):
        self.root.title('Collaborative Packaging')
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f'{self.field_width}x{self.field_length}')
        self.root.config(bg='#345')
        self.root.resizable(False, True)
        self.canvas = Canvas(
            self.root,
            height=self.field_length,
            width=self.field_width,
            bg="#ccc",
            bd=0,
            highlightthickness=0,
            relief='ridge'
        )


        ###################################################################################
        ###################################################################################
        ################################## Pattern Table ##################################

        for i in range(5):
            for c in range(6):
                if c == 0:
                    col = 'gray'
                else:
                    col = self.pattern[i+1][c-1]
                x = self.pattern_table_x + c * self.pattern_table_cell
                y = self.pattern_table_y + i * self.pattern_table_cell
                self.canvas.create_rectangle(x, y,
                                             x + self.pattern_table_cell,
                                             y + self.pattern_table_cell, width=2,
                                             outline='#000',
                                             fill=col)
                if c == 0:
                    self.canvas.create_text((x + self.pattern_table_cell//2, y + self.pattern_table_cell//2),
                                            text='W{}'.format(i+1), font=("Helvetica", 15))
                else:
                    self.canvas.create_text((x + self.pattern_table_cell//2, y + self.pattern_table_cell//2),
                                            text=str(c), font=("Helvetica", 12))

        ###################################################################################
        ###################################################################################
        ################################# Workspaces' Tables ##############################

        self.canvas.create_rectangle(self.workspace_table_x, self.workspace_table_y,
                                     self.workspace_table_x + self.workspace_table_width,
                                     self.workspace_table_y + self.workspace_table_length, width=2,
                                     outline='#000',
                                     fill='gray')
        # self.root.update_idletasks()

        ###################################################################################
        ###################################################################################
        ################################### Workspace 1 ###################################
        self.canvas.create_oval(self.workspace1_x0, self.workspace1_y0,
                                self.workspace1_x0 + 2 * self.workspaces_r,
                                self.workspace1_y0 + 2 * self.workspaces_r, width=2,
                                outline='#000', fill='orange')
        self.canvas.create_text((self.workspace1_x0 + self.workspaces_r//2, self.workspace1_y0 + self.workspaces_r),
                                text='W1', angle=90, font=("Helvetica", 20))
        for i in range(5):
            self.ws1_box_pos.append([self.w1b_x0[i], self.w1b_y0[i],
                                    self.w1b_x0[i] + self.boxes_width,
                                    self.w1b_y0[i] + self.boxes_width])
            comp = self.canvas.create_rectangle(self.w1b_x0[i], self.w1b_y0[i],
                                         self.w1b_x0[i] + self.boxes_width,
                                         self.w1b_y0[i] + self.boxes_width, width=2,
                                         outline='#000', fill='white')
            self.canvas.create_text((self.w1b_x0[i]+self.boxes_width//2, self.w1b_y0[i]+self.boxes_width//2), text=str(i+1))

        ###################################################################################
        ###################################################################################
        ################################### Workspace 2 ###################################

        self.canvas.create_oval(self.workspace2_x0, self.workspace2_y0,
                                self.workspace2_x0 + 2 * self.workspaces_r,
                                self.workspace2_y0 + 2 * self.workspaces_r, width=2,
                                outline='#000', fill='orange')
        self.canvas.create_text((self.workspace2_x0 + + self.workspaces_r // 2, self.workspace2_y0 + self.workspaces_r),
                                text='W2', angle=90, font=("Helvetica", 20))
        for i in range(5):
            self.ws1_box_pos.append([self.w2b_x0[i], self.w2b_y0[i],
                                    self.w2b_x0[i] + self.boxes_width,
                                    self.w2b_y0[i] + self.boxes_width])
            self.canvas.create_rectangle(self.w2b_x0[i], self.w2b_y0[i],
                                         self.w2b_x0[i] + self.boxes_width,
                                         self.w2b_y0[i] + self.boxes_width, width=2,
                                         outline='#000', fill='white')
            self.canvas.create_text((self.w2b_x0[i] + self.boxes_width // 2, self.w2b_y0[i] + self.boxes_width // 2),
                                    text=str(i + 1))

        ###################################################################################
        ###################################################################################
        ################################### Workspace 3 ###################################

        self.canvas.create_oval(self.workspace3_x0, self.workspace3_y0,
                                self.workspace3_x0 + 2 * self.workspaces_r,
                                self.workspace3_y0 + 2 * self.workspaces_r, width=2,
                                outline='#000', fill='orange')
        self.canvas.create_text((self.workspace3_x0 + + self.workspaces_r // 2, self.workspace3_y0 + self.workspaces_r),
                                text='W3', angle=90, font=("Helvetica", 20))
        for i in range(5):
            self.ws1_box_pos.append([self.w3b_x0[i], self.w3b_y0[i],
                                    self.w3b_x0[i] + self.boxes_width,
                                    self.w3b_y0[i] + self.boxes_width])
            self.canvas.create_rectangle(self.w3b_x0[i], self.w3b_y0[i],
                                         self.w3b_x0[i] + self.boxes_width,
                                         self.w3b_y0[i] + self.boxes_width, width=2,
                                         outline='#000', fill='white')
            self.canvas.create_text((self.w3b_x0[i] + self.boxes_width // 2, self.w3b_y0[i] + self.boxes_width // 2),
                                    text=str(i + 1))

        ###################################################################################
        ###################################################################################
        ################################### Workspace 4 ###################################

        self.canvas.create_oval(self.workspace4_x0, self.workspace4_y0,
                                self.workspace4_x0 + 2 * self.workspaces_r,
                                self.workspace4_y0 + 2 * self.workspaces_r, width=2,
                                outline='#000', fill='orange')
        self.canvas.create_text((self.workspace4_x0 + + self.workspaces_r // 2, self.workspace4_y0 + self.workspaces_r),
                                text='W4', angle=90, font=("Helvetica", 20))
        for i in range(5):
            self.ws1_box_pos.append([self.w4b_x0[i], self.w4b_y0[i],
                                    self.w4b_x0[i] + self.boxes_width,
                                    self.w4b_y0[i] + self.boxes_width])
            self.canvas.create_rectangle(self.w4b_x0[i], self.w4b_y0[i],
                                         self.w4b_x0[i] + self.boxes_width,
                                         self.w4b_y0[i] + self.boxes_width, width=2,
                                         outline='#000', fill='white')
            self.canvas.create_text((self.w4b_x0[i] + self.boxes_width // 2, self.w4b_y0[i] + self.boxes_width // 2),
                                    text=str(i + 1))

        ###################################################################################
        ###################################################################################
        ################################### Workspace 5 ###################################

        self.canvas.create_oval(self.workspace5_x0, self.workspace5_y0,
                                self.workspace5_x0 + 2 * self.workspaces_r,
                                self.workspace5_y0 + 2 * self.workspaces_r, width=2,
                                outline='#000', fill='orange')
        self.canvas.create_text((self.workspace5_x0 + + self.workspaces_r // 2, self.workspace5_y0 + self.workspaces_r),
                                text='W5', angle=90, font=("Helvetica", 20))
        for i in range(5):
            self.ws1_box_pos.append([self.w5b_x0[i], self.w5b_y0[i],
                                    self.w5b_x0[i] + self.boxes_width,
                                    self.w5b_y0[i] + self.boxes_width])
            self.canvas.create_rectangle(self.w5b_x0[i], self.w5b_y0[i],
                                         self.w5b_x0[i] + self.boxes_width,
                                         self.w5b_y0[i] + self.boxes_width, width=2,
                                         outline='#000', fill='white')
            self.canvas.create_text((self.w5b_x0[i] + self.boxes_width // 2, self.w5b_y0[i] + self.boxes_width // 2),
                                    text=str(i + 1))


        self.canvas.pack()
        self.root.update_idletasks()
        input()
        self.canvas.itemconfig(ws1[1], fill='red')
#
#
#
