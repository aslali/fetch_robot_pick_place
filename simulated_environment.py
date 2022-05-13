# import tkinter
# import tkinter
import tkinter
from tkinter import *


# from mttkinter import mtTkinter


class SHSCPackaging:
    a = 1

    def __init__(self, pattern, fast_run=False):
        self.root = tkinter.Tk()
        self.canvas = None

        self.field_width = 1700
        self.field_length = 900

        self.dh1 = 1
        self.dh2 = 1
        self.dr1 = 1
        self.dr2 = 1

        self.workspace_table_width = 200
        self.workspace_table_length = 800
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

        # self.tray_num = []
        # self.tray_status = []
        # self.tray_col = []
        # self.h_tray_pos = []
        # self.r_tray_pos = []
        # self.block_number = []
        # self.block_status = []
        # self.block_handle = []
        # self.block_pos = []
        # self.block_colors = []
        # self.ws3_pos = []
        # self.ws3_status = []
        # self.ws2_pos = []
        # self.ws2_status = []
        # self.ws4_pos = []
        # self.ws4_status = []
        # self.ws1_pos = []
        # self.ws1_status = []
        # self.human_pos = []
        # self.human_handle = []
        # self.robot_handle = []
        # self.robot_pos = []
        # self.hpoints = {}
        # self.rpoints = {}
        # self.table_blocks = {}
        # self.table_h = 200
        # self.table_w = 350
        # self.pattern_col = pattern
        self.creat_env()
        # self.update = not fast_run

    def boxes_x_y(self, x0, y0):
        ys = []
        xs = []
        for i in range(1, 6):
            ys.append(y0 + i * self.workspaces_r // 3 - self.boxes_width // 2)
            xs.append(x0 + self.workspaces_r - self.boxes_width // 2)
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
        h_workspace = 90
        w_workspace = 200
        x14 = 50
        y23 = 100
        db = 35

        ###################################################################################
        ###################################################################################
        ################################# Workspaces' Tables #################################

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
        for i in range(5):
            self.ws1_box_pos.append([self.w1b_x0[i], self.w1b_y0[i],
                                    self.w1b_x0[i] + self.boxes_width,
                                    self.w1b_y0[i] + self.boxes_width])
            self.canvas.create_rectangle(self.w1b_x0[i], self.w1b_y0[i],
                                         self.w1b_x0[i] + self.boxes_width,
                                         self.w1b_y0[i] + self.boxes_width, width=2,
                                         outline='#000', fill='white')

        ###################################################################################
        ###################################################################################
        ################################### Workspace 2 ###################################

        self.canvas.create_oval(self.workspace2_x0, self.workspace2_y0,
                                self.workspace2_x0 + 2 * self.workspaces_r,
                                self.workspace2_y0 + 2 * self.workspaces_r, width=2,
                                outline='#000', fill='orange')
        for i in range(5):
            self.ws1_box_pos.append([self.w2b_x0[i], self.w2b_y0[i],
                                    self.w2b_x0[i] + self.boxes_width,
                                    self.w2b_y0[i] + self.boxes_width])
            self.canvas.create_rectangle(self.w2b_x0[i], self.w2b_y0[i],
                                         self.w2b_x0[i] + self.boxes_width,
                                         self.w2b_y0[i] + self.boxes_width, width=2,
                                         outline='#000', fill='white')

        ###################################################################################
        ###################################################################################
        ################################### Workspace 3 ###################################

        self.canvas.create_oval(self.workspace3_x0, self.workspace3_y0,
                                self.workspace3_x0 + 2 * self.workspaces_r,
                                self.workspace3_y0 + 2 * self.workspaces_r, width=2,
                                outline='#000', fill='orange')
        for i in range(5):
            self.ws1_box_pos.append([self.w3b_x0[i], self.w3b_y0[i],
                                    self.w3b_x0[i] + self.boxes_width,
                                    self.w3b_y0[i] + self.boxes_width])
            self.canvas.create_rectangle(self.w3b_x0[i], self.w3b_y0[i],
                                         self.w3b_x0[i] + self.boxes_width,
                                         self.w3b_y0[i] + self.boxes_width, width=2,
                                         outline='#000', fill='white')

        ###################################################################################
        ###################################################################################
        ################################### Workspace 4 ###################################

        self.canvas.create_oval(self.workspace4_x0, self.workspace4_y0,
                                self.workspace4_x0 + 2 * self.workspaces_r,
                                self.workspace4_y0 + 2 * self.workspaces_r, width=2,
                                outline='#000', fill='orange')
        for i in range(5):
            self.ws1_box_pos.append([self.w4b_x0[i], self.w4b_y0[i],
                                    self.w4b_x0[i] + self.boxes_width,
                                    self.w4b_y0[i] + self.boxes_width])
            self.canvas.create_rectangle(self.w4b_x0[i], self.w4b_y0[i],
                                         self.w4b_x0[i] + self.boxes_width,
                                         self.w4b_y0[i] + self.boxes_width, width=2,
                                         outline='#000', fill='white')

        ###################################################################################
        ###################################################################################
        ################################### Workspace 5 ###################################

        self.canvas.create_oval(self.workspace5_x0, self.workspace5_y0,
                                self.workspace5_x0 + 2 * self.workspaces_r,
                                self.workspace5_y0 + 2 * self.workspaces_r, width=2,
                                outline='#000', fill='orange')
        for i in range(5):
            self.ws1_box_pos.append([self.w5b_x0[i], self.w5b_y0[i],
                                    self.w5b_x0[i] + self.boxes_width,
                                    self.w5b_y0[i] + self.boxes_width])
            self.canvas.create_rectangle(self.w5b_x0[i], self.w5b_y0[i],
                                         self.w5b_x0[i] + self.boxes_width,
                                         self.w5b_y0[i] + self.boxes_width, width=2,
                                         outline='#000', fill='white')

        # for i in range(5):
        #     self.ws1_pos.append([bx14, d2, bx14 + db, 0 + d2 + db])
        #     self.canvas.create_rectangle(self.w1b1_x0, self.w1b1_y0,
        #                         self.w1b1_x0 + self.boxes_width,
        #                         self.w1b1_y0 + self.boxes_width, width=2,
        #                         outline='#000', fill='white')
        #     self.canvas.create_text((bx14 + db // 2, d2 + db // 2), text=f'{i + 1}')
        #     self.ws1_status.append('empty')
        #     bx14 += db
        self.canvas.pack()
        self.root.update_idletasks()
#         d1 = (w_workspace - 5 * db) // 2
#         d11 = (w_workspace - 5 * db // 2) // 2
#         d2 = 22
#         self.canvas.create_rectangle(self.field_width // 2 - w_workspace // 2 - x14, 0,
#                                      self.field_width // 2 + w_workspace // 2 - x14, 0 + h_workspace, width=2,
#                                      outline='#000',
#                                      fill='gray')
#
#         self.canvas.create_text((self.field_width // 2 - x14, h_workspace - 10), text='W1', font=('Helvetica', '15'))
#
#         bx14 = self.field_width // 2 - w_workspace // 2 - x14 + d1
#         for i in range(5):
#             self.ws1_pos.append([bx14, d2, bx14 + db, 0 + d2 + db])
#             self.canvas.create_rectangle(bx14, d2, bx14 + db, 0 + d2 + db, width=2, outline='#000', fill='#fff')
#             self.canvas.create_text((bx14 + db // 2, d2 + db // 2), text=f'{i + 1}')
#             self.ws1_status.append('empty')
#             bx14 += db
#
#         bx14 = self.field_width // 2 - w_workspace // 2 - x14 + d11
#         for i in range(5):
#             self.canvas.create_rectangle(bx14, h_workspace, bx14 + db // 2, 0 + h_workspace + db // 2, width=2,
#                                          outline='#000', fill=self.pattern_col[(1, i + 1)])
#             bx14 += db // 2
#
#         ################################### Workspace 4 ###################################
#         self.canvas.create_rectangle(self.field_width // 2 - w_workspace // 2 - x14,
#                                      self.field_length - h_workspace - 1,
#                                      self.field_width // 2 + w_workspace // 2 - x14, self.field_length - 1, width=2,
#                                      outline='#000',
#                                      fill='gray')
#         self.canvas.create_text((self.field_width // 2 - x14, self.field_length - h_workspace + 15), text='W4',
#                                 font=('Helvetica', '15'), angle=0)
#
#         bx14 = self.field_width // 2 - w_workspace // 2 - x14 + d1
#         for i in range(5):
#             self.ws4_pos.append([bx14, self.field_length - 1 - d2 - db, bx14 + db, self.field_length - 1 - d2])
#             self.canvas.create_rectangle(bx14, self.field_length - 1 - d2 - db, bx14 + db, self.field_length - 1 - d2,
#                                          width=2,
#                                          outline='#000',
#                                          fill='#fff')
#             self.canvas.create_text((bx14 + db // 2, self.field_length - 1 - d2 - db // 2), text=f'{i + 1}')
#             self.ws4_status.append('empty')
#             bx14 += db
#
#         bx14 = self.field_width // 2 - w_workspace // 2 - x14 + d11
#         for i in range(5):
#             self.canvas.create_rectangle(bx14, self.field_length - h_workspace - db // 2, bx14 + db // 2,
#                                          self.field_length - 1 - h_workspace,
#                                          width=2,
#                                          outline='#000',
#                                          fill=self.pattern_col[(4, i + 1)])
#             bx14 += db // 2
#
#         ################################### Workspace 2 ###################################
#         self.canvas.create_rectangle(self.field_width - h_workspace - 1, y23,
#                                      self.field_width - 1, y23 + w_workspace, width=2, outline='#000', fill='gray')
#         self.canvas.create_text((self.field_width - h_workspace + 10, y23 + w_workspace // 2), text='W2',
#                                 font=('Helvetica', '15'), angle=-90)
#         by23 = y23 + d1
#         for i in range(5):
#             self.ws2_pos.append([self.field_width - db - d2 - 1, by23, self.field_width - 1 - d2, by23 + db])
#             self.canvas.create_rectangle(self.field_width - db - d2 - 1, by23, self.field_width - 1 - d2, by23 + db,
#                                          width=2,
#                                          outline='#000', fill='#fff')
#             self.canvas.create_text((self.field_width - db // 2 - d2 - 1, by23 + db // 2), text=f'{i + 1}')
#             self.ws2_status.append('empty')
#             by23 += db
#
#         by23 = y23 + 50 + d1
#         for i in range(5):
#             self.canvas.create_rectangle(self.field_width - db // 2 - h_workspace - 1, by23,
#                                          self.field_width - 1 - h_workspace, by23 + db // 2,
#                                          width=2, outline='#000', fill=self.pattern_col[(2, i + 1)])
#             by23 += db // 2
#
#         ################################### Workspace 3 ###################################
#         self.canvas.create_rectangle(self.field_width - h_workspace - 1, self.field_length - y23 - w_workspace,
#                                      self.field_width - 1, self.field_length - y23, width=2, outline='#000',
#                                      fill='gray')
#         self.canvas.create_text((self.field_width - h_workspace + 10, self.field_length - y23 - w_workspace // 2),
#                                 text='W3', font=('Helvetica', '15'), angle=-90)
#         by23 = self.field_length - y23 - w_workspace + d1
#         for i in range(5):
#             self.ws3_pos.append([self.field_width - db - d2 - 1, by23, self.field_width - 1 - d2, by23 + db])
#             self.canvas.create_rectangle(self.field_width - db - d2 - 1, by23, self.field_width - 1 - d2, by23 + db,
#                                          width=2,
#                                          outline='#000', fill='#fff')
#             self.canvas.create_text((self.field_width - db // 2 - d2 - 1, by23 + db // 2), text=f'{i + 1}')
#             self.ws3_status.append('empty')
#             by23 += db
#
#         by23 = self.field_length - y23 - w_workspace + d1 + 50
#         for i in range(5):
#             self.canvas.create_rectangle(self.field_width - db // 2 - 1 - h_workspace, by23,
#                                          self.field_width - 1 - h_workspace, by23 + db // 2,
#                                          width=2,
#                                          outline='#000', fill=self.pattern_col[(3, i + 1)])
#             by23 += db // 2
#
#         ###################################################################################
#         ###################################################################################
#         ################################# Objects' Tables #################################
#
#         self.canvas.create_rectangle(1, self.field_length // 2 - self.table_w // 2,
#                                      self.table_h + 1, self.field_length // 2 + self.table_w // 2, width=2,
#                                      outline='#000',
#                                      fill='gray')
#
#         ###################################################################################
#         ###################################################################################
#         ###################################### R_Tray #####################################
#         xot = 10
#         wtray = 35
#         htray = 35
#         yoc = self.field_length // 2 - wtray // 2 - 100
#         for j in range(0, 4):
#             self.canvas.create_rectangle(xot, yoc,
#                                          xot + wtray, yoc + htray, width=2, outline='#000', fill='#fff')
#             self.canvas.create_text((xot + wtray // 2, yoc - 10), text=f'W{j + 1}', font=('TkDefaultFont', 10))
#             self.h_tray_pos.append([xot, yoc, xot + wtray, yoc + htray])
#             # self.tray_col.append(tcol[j])
#             # self.tray_status.append('empty')
#             # self.tray_num.append(j)
#             xot += wtray + 5
#         aaaa = self.canvas.create_text((xot + wtray // 3, yoc + htray // 2), text='H', font=('TkDefaultFont', 15))
#         ##################################### H_Tray #####################################
#         xot = 10
#         wtray = 35
#         htray = 35
#         yoc = self.field_length // 2 + wtray // 2 - 100
#         for j in range(0, 4):
#             self.canvas.create_rectangle(xot, yoc,
#                                          xot + wtray, yoc + htray, width=2, outline='#000', fill='#fff')
#             self.r_tray_pos.append([xot, yoc, xot + wtray, yoc + htray])
#             xot += wtray + 5
#         self.canvas.create_text((xot + wtray // 3, yoc + htray // 2), text='R', font=('TkDefaultFont', 15))
#
# ###################################################################################
# ###################################################################################
# ###################################### Human ######################################
#         rhuman = 25
#         self.human_handle = self.canvas.create_oval(self.table_h + 100, self.field_length // 2 - 110,
#                                                     self.table_h + 100 + 2 * rhuman,
#                                                     self.field_length // 2 - 110 + 2 * rhuman, width=0,
#                                                     outline='#000', fill='orange')
#         self.human_handle_text = self.canvas.create_text((self.table_h + 100 + rhuman, self.field_length // 2 - 110 + rhuman)
#                                                          , text='H', font=('TkDefaultFont', 15))
#         self.human_pos_table = [self.table_h + 10, self.field_length // 2 - 110]
#         self.human_pos = [self.table_h + 100, self.field_length // 2 - 110]
#         self.human_pos_text = [self.table_h + 100 + rhuman, self.field_length // 2 - 110 + rhuman]
#         # self.human_handle = self.canvas.create_oval(self.field_width // 2 - w_workspace // 1.5, h_workspace + 20,
#         #                                             self.field_width // 2 - w_workspace // 1.5 + 2 * rhuman,
#         #                                             h_workspace + 20 + 2 * rhuman, width=0.01,
#         #                                             outline='#000', fill='green')
#         # self.human_handle = self.canvas.create_oval(self.field_width // 2,
#         #                                             self.field_length - h_workspace - 20 - 2 * rhuman,
#         #                                             self.field_width // 2 + 2 * rhuman,
#         #                                             self.field_length - h_workspace - 20, width=0.01,
#         #                                             outline='#000', fill='green')
#         # self.human_handle = self.canvas.create_oval(self.field_width - h_workspace - 20 - 2 * rhuman,
#         #                                             y23,
#         #                                             self.field_width - h_workspace - 20,
#         #                                             y23 + 2 * rhuman, width=0.01,
#         #                                             outline='#000', fill='green')
#         # self.human_handle = self.canvas.create_oval(self.field_width - h_workspace - 20 - 2 * rhuman,
#         #                                             self.field_length - y23 - w_workspace,
#         #                                             self.field_width - h_workspace - 20,
#         #                                             self.field_length - y23 - w_workspace + 2 * rhuman, width=0.01,
#         #                                             outline='#000', fill='green')
#
#         self.hpoints = {'T': [self.table_h + 10, self.field_length // 2 - 110],
#                         'W1': [self.field_width // 2 - w_workspace // 1.5, h_workspace + 20],
#                         'W4': [self.field_width // 2, self.field_length - h_workspace - 20 - 2 * rhuman],
#                         'W2': [self.field_width - h_workspace - 20 - 2 * rhuman, y23],
#                         'W3': [self.field_width - h_workspace - 20 - 2 * rhuman, self.field_length - y23 - w_workspace]
#                         }
#
# ###################################### robot ######################################
#         rrobot = 25
#         self.robot_handle = self.canvas.create_oval(self.table_h + 10, self.field_length // 2 + 50,
#                                                     self.table_h + 10 + 2 * rrobot,
#                                                     self.field_length // 2 + 50 + 2 * rrobot, width=0,
#                                                     outline='#000', fill='blue')
#         self.robot_handle_text = self.canvas.create_text((self.table_h + 10 + rrobot, self.field_length // 2 + 50 + rrobot),
#                                                          text='R', font=('TkDefaultFont', 15))
#         self.robot_pos = [self.table_h + 10, self.field_length // 2 + 50]
#         self.robot_pos_text = [self.table_h + 10 + rrobot, self.field_length // 2 + 50 + rrobot]
#         # self.robot_handle = self.canvas.create_oval(self.field_width // 2 - w_workspace // 100.5, h_workspace + 20,
#         #                                             self.field_width // 2 - w_workspace // 100.5 + 2 * rrobot,
#         #                                             h_workspace + 20 + 2 * rrobot, width=0.01,
#         #                                             outline='#000', fill='blue')
#         # self.robot_handle = self.canvas.create_oval(self.field_width // 2 - w_workspace // 1.5,
#         #                                             self.field_length - h_workspace - 20 - 2 * rrobot,
#         #                                             self.field_width // 2 - w_workspace // 1.5 + 2 * rrobot,
#         #                                             self.field_length - h_workspace - 20, width=0.01,
#         #                                             outline='#000', fill='blue')
#         # self.robot_handle = self.canvas.create_oval(self.field_width - h_workspace - 20 - 2 * rrobot,
#         #                                             y23+w_workspace // 1.5,
#         #                                             self.field_width - h_workspace - 20,
#         #                                             y23 + w_workspace // 1.5+2 * rrobot, width=0.01,
#         #                                             outline='#000', fill='blue')
#         # self.robot_handle = self.canvas.create_oval(self.field_width - h_workspace - 20 - 2 * rrobot,
#         #                                             self.field_length - y23 - w_workspace / 4,
#         #                                             self.field_width - h_workspace - 20,
#         #                                             self.field_length - y23 - w_workspace / 4 + 2 * rrobot, width=0.01,
#         #                                             outline='#000', fill='blue')
#
#         self.rpoints = {'T': [self.table_h + 10, self.field_length // 2 + 50],
#                         'W1': [self.field_width // 2 - w_workspace // 100.5, h_workspace + 20],
#                         'W4': [self.field_width // 2 - w_workspace // 1.5,
#                                self.field_length - h_workspace - 20 - 2 * rrobot],
#                         'W2': [self.field_width - h_workspace - 20 - 2 * rrobot, y23 + w_workspace // 1.5],
#                         'W3': [self.field_width - h_workspace - 20 - 2 * rrobot,
#                                self.field_length - y23 - w_workspace / 4]
#                         }
# ###################################################################################
# ###################################################################################
# ##################################### Objects #####################################
#         obj_color = ['#00a933', '#ffff00', '#2a6099', '#ff0000']
#         color_name = ['g', 'y', 'b', 'r']
#         # random.seed(4)
#         # random.shuffle(obj_color)
#         robjects = 10
#         yoc = self.field_length // 2 - robjects
#         for i in range(0, 4):
#             xoc = 10
#             self.table_blocks[color_name[i]] = {'pos': [], 'status': [], 'number': []}
#             for j in range(0, 7):
#                 tmpcan = self.canvas.create_oval(xoc, yoc - robjects,
#                                                  xoc + 2 * robjects, yoc + robjects, width=0.00, outline='#000',
#                                                  fill=obj_color[i])
#                 self.block_handle.append(tmpcan)
#                 # canvas.move(tmpcan, 300,300)
#                 self.block_pos.append([xoc, yoc - robjects])
#                 self.block_colors.append(obj_color[i])
#                 self.block_status.append('table')
#                 # self.block_number.append(7 * i + j)
#                 self.table_blocks[color_name[i]]['pos'].append([xoc, yoc - robjects])
#                 self.table_blocks[color_name[i]]['status'].append(1)
#                 self.table_blocks[color_name[i]]['number'].append(7 * i + j)
#                 xoc += 2 * robjects + 5
#
#             yoc += 2 * robjects + 5
#
#         self.canvas.pack()
#         self.root.update_idletasks()
#
#     def move_object(self, object_num, destination_name=None, destination_num=None, goal=None):
#         sp = self.block_pos[object_num]
#         if (goal is not None) and (destination_name is None) and (destination_num is None):
#             gp = goal
#         elif (destination_name is not None) and (destination_num is not None):
#             if destination_name == 'W1':
#                 gp = self.ws1_pos[destination_num - 1][:]
#             elif destination_name == 'W2':
#                 gp = self.ws2_pos[destination_num - 1][:]
#             elif destination_name == 'W3':
#                 gp = self.ws3_pos[destination_num - 1][:]
#             elif destination_name == 'W4':
#                 gp = self.ws4_pos[destination_num - 1][:]
#             elif destination_name == 'hTray':
#                 gp = self.h_tray_pos[destination_num - 1][:]
#             elif destination_name == 'rTray':
#                 gp = self.r_tray_pos[destination_num - 1][:]
#             else:
#                 # gp = 0
#                 raise ValueError('destination is not correct')
#             gp[0] += 5
#             gp[1] += 5
#         else:
#             raise ValueError('function inputs are not correct')
#
#         dpx = gp[0] - sp[0]
#         dpy = gp[1] - sp[1]
#         # self.canvas.move(self.block_handle[object_num], dpx, dpy)
#         self.block_pos[object_num][0] = gp[0]
#         self.block_pos[object_num][1] = gp[1]
#         if self.update:
#             self.canvas.move(self.block_handle[object_num], dpx, dpy)
#             self.root.update_idletasks()
#     def move_human_robot(self, new_pos, agent):
#         if agent == 'human':
#             dhx = new_pos[0] - self.human_pos[0]
#             dhy = new_pos[1] - self.human_pos[1]
#             # self.canvas.move(self.human_handle, dhx, dhy)
#             # self.canvas.move(self.human_handle_text, dhx, dhy)
#             if self.update:
#                 self.canvas.move(self.human_handle, dhx, dhy)
#                 self.canvas.move(self.human_handle_text, dhx, dhy)
#                 self.root.update_idletasks()
#             self.human_pos[0] = new_pos[0]
#             self.human_pos[1] = new_pos[1]
#             self.human_pos_text[0] += dhx
#             self.human_pos_text[1] += dhy
#         else:
#             dhx = new_pos[0] - self.robot_pos[0]
#             dhy = new_pos[1] - self.robot_pos[1]
#             # self.canvas.move(self.robot_handle, dhx, dhy)
#             # self.canvas.move(self.robot_handle_text, dhx, dhy)
#             if self.update:
#                 self.canvas.move(self.robot_handle, dhx, dhy)
#                 self.canvas.move(self.robot_handle_text, dhx, dhy)
#                 self.root.update_idletasks()
#             self.robot_pos[0] = new_pos[0]
#             self.robot_pos[1] = new_pos[1]
#             self.robot_pos_text[0] += dhx
#             self.robot_pos_text[1] += dhy
#         if self.update:
#             self.root.update_idletasks()
