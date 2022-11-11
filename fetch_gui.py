import ui
from objc_util import ObjCClass, ObjCInstance
import time
import socket
import threading

PORT = 5051
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
# SERVER = "10.32.22.145"
# SERVER = "129.97.71.122" robo
SERVER = "192.168.1.255"
SERVER = "192.168.1.8"
SERVER = "192.168.0.49"
ADDR = (SERVER, PORT)


class Box(object):
    def __init__(self, workspace, box_number):
        self.workspace = workspace
        self.number = box_number
        self.previous_state = None
        self.current_state = 'Free'
        self.choosable = False
        self.previous_color = None
        self.color = ''


class Userinterface(object):
    def __init__(self):
        self.__blue = 'blue'
        self.__green = 'green'
        self.__orange = 'orange'
        self.__pink = 'pink'
        self.__human_icon = 'iob:man_256'
        self.__robot_icon = 'iob:social_android_256'
        self.flashing_boxes = {}  # {'w1b1': self.__blue, 'w1b2': self.__green}
        self.selected_color = None
        self.selected_agent = None
        self.all_boxes = [[] for i in range(5)]
        self.generate_boxes()
        self.btn_workspace = None
        self.btn_box = None
        self.box_name = ''
        self.color_names = {
            self.__green: 'green',
            self.__blue: 'blue',
            self.__pink: 'pink',
            self.__orange: 'orange'
        }

        self.all_action_type = {'Human': 0, 'Assigned_to_Human': 1, 'Assigned_to_Robot': 2, 'Done': 3, 'Return': 4,
                                'Free': 5}

        self.color_list = {
            0: self.__green,
            1: self.__blue,
            2: self.__orange,
            3: self.__pink,
            self.__green: 0,
            self.__blue: 1,
            self.__orange: 2,
            self.__pink: 3
        }

        w, h = ui.get_screen_size()
        self.v = ui.load_view()
        self.create_workspaces()
        self.create_question_colors()
        self.create_question_agent()
        self.create_question_yesno()
        self.create_msg_error()
        self.create_finish_task()
        self.v.height = h
        self.v.width = w
        self.assign_actions()
        self.hide_question_colors()
        self.hide_question_agent()
        self.hide_question_yesno()
        self.hide_msg_error()
        self.v.present('sheet')

        self.client = None
        self.start_socket()
        time.sleep(1)
        col_chng = threading.Thread(target=self.color_flasher)
        col_chng.start()

    def create_workspaces(self):
        button = []
        btn_width = 70
        btn_height = 70
        buttons_gaps = 15
        view_padding = 15

        view_width = 2 * btn_width + 2 * view_padding + buttons_gaps
        view_height = 3 * btn_height + 2 * view_padding + 2 * buttons_gaps
        views_gaps = 25
        view1_x = 80
        view1_y = 70
        btn_pos = [[0, 0], [btn_width + buttons_gaps, 0],
                   [btn_width + buttons_gaps, btn_height + buttons_gaps],
                   [0, btn_height + buttons_gaps],
                   [btn_width // 2 + buttons_gaps // 2, 2 * btn_height + 2 * buttons_gaps]]

        for i in range(1, 6):
            view_name = 'view_w' + str(i)
            view = ui.View(name=view_name)
            view.x = view1_x + (i - 1) * view_width + (i - 1) * views_gaps
            view.y = view1_y
            view.width = view_width
            view.height = view_height
            view.background_color = 'orange'
            view.alpha = 0.3
            self.v.add_subview(view)

            wlabel_name = 'label_w' + str(i)
            wlabel = ui.Label(name=wlabel_name)
            wlabel.width = 60
            wlabel.height = 34
            wlabel.font = ('.SFUI-Semibold', 30.0)
            wlabel.text = 'W ' + str(i)
            wlabel.x = view.x + view.width // 2 - wlabel.width // 2
            wlabel.y = view.y - wlabel.height
            wlabel.alignment = 1
            self.v.add_subview(wlabel)

            for ii in range(1, 6):
                btn_name = 'w' + str(i) + 'b' + str(ii)
                label_name = 'label' + str(i) + str(ii)
                button = ui.Button(name=btn_name)
                button.x = self.v[view_name].x + view_padding + btn_pos[ii - 1][0]
                button.y = self.v[view_name].y + view_padding + btn_pos[ii - 1][1]
                button.width = btn_width
                button.height = btn_height
                button.background_color = 'white'
                button.border_width = 2
                button.corner_radius = 5
                self.v.add_subview(button)

                label = ui.Label(name=label_name)
                label.font = ('.SFUI-Semibold', 30.0)
                label.text = str(ii)
                label.x = button.x
                label.y = button.y
                label.width = 34
                label.height = 34
                label.alignment = 1
                self.v.add_subview(label)

    def create_question_agent(self):
        view_agent = ui.View(name='view_agent')
        view_agent.width = 425
        view_agent.height = 285
        view_agent.x = self.v.width // 2 - view_agent.width // 3
        view_agent.y = self.v['view_w1'].y + self.v['view_w1'].height
        view_agent.background_color = '#a8a8a8'
        self.v.add_subview(view_agent)

        label_agent = ui.Label(name='label_agent')
        label_agent.text = 'Who do you want to assign this task?'
        label_agent.x = view_agent.x + 30
        label_agent.y = view_agent.y + 10
        label_agent.width = view_agent.width - 30
        label_agent.height = 35
        label_agent.font = ('.SFUI-Semibold', 25)
        self.v.add_subview(label_agent)

        btn_agent_select = ui.SegmentedControl(name='btn_agent_select')
        btn_agent_select.segments = ['Me', 'Fetch']
        btn_agent_select.width = 160
        btn_agent_select.height = 80
        btn_agent_select.x = view_agent.x + view_agent.width // 2 - btn_agent_select.width // 2
        btn_agent_select.y = label_agent.y + label_agent.height + 30
        btn_agent_select.background_color = ''
        btn_agent_select.border_width = 4
        btn_agent_select.corner_radius = 10
        btn_agent_select.selected_index = 0
        UIFont = ObjCClass('UIFont').fontWithName_size_('Arial Rounded MT Bold', 22)
        attributes = {'NSFont': UIFont}
        vo = ObjCInstance(btn_agent_select).segmentedControl()
        vo.setTitleTextAttributes_forState_(attributes, 0)
        self.v.add_subview(btn_agent_select)

        btn_agent_ok = ui.Button(name='btn_agent_ok')
        btn_agent_ok.title = 'OK'
        btn_agent_ok.width = 80
        btn_agent_ok.height = 60
        btn_agent_ok.x = view_agent.x + view_agent.width // 2 - btn_agent_ok.width - 20
        btn_agent_ok.y = btn_agent_select.y + btn_agent_select.height + 30
        btn_agent_ok.background_color = 'white'
        btn_agent_ok.tint_color = 'black'
        btn_agent_ok.font = ('.SFUI-Semibold', 20)
        self.v.add_subview(btn_agent_ok)

        btn_agent_cancel = ui.Button(name='btn_agent_cancel')
        btn_agent_cancel.title = 'Cancel'
        btn_agent_cancel.width = 80
        btn_agent_cancel.height = 60
        btn_agent_cancel.x = btn_agent_ok.x + btn_agent_ok.width + 20
        btn_agent_cancel.y = btn_agent_select.y + btn_agent_select.height + 30
        btn_agent_cancel.background_color = 'white'
        btn_agent_cancel.tint_color = 'black'
        btn_agent_cancel.font = ('.SFUI-Semibold', 20)
        self.v.add_subview(btn_agent_cancel)

    def create_question_colors(self):
        btn_color_gap = 20
        btn_y = 85
        btn_w = 80
        btn_h = 80
        view_color = ui.View(name='view_color')
        view_color.width = 425
        view_color.height = 285
        view_color.x = self.v.width // 2 - view_color.width // 3
        view_color.y = self.v['view_w1'].y + self.v['view_w1'].height
        view_color.background_color = '#a8a8a8'
        self.v.add_subview(view_color)

        btn_green = ui.Button(name='btn_green')
        btn_green.title = 'Green'
        btn_green.width = btn_w
        btn_green.height = btn_h
        btn_green.x = view_color.x + btn_color_gap
        btn_green.y = view_color.y + btn_y
        btn_green.background_color = self.__green
        btn_green.tint_color = 'white'
        btn_green.font = ('.SFUI-Semibold', 20)
        self.v.add_subview(btn_green)

        btn_blue = ui.Button(name='btn_blue')
        btn_blue.title = 'Blue'
        btn_blue.width = btn_w
        btn_blue.height = btn_h
        btn_blue.x = btn_green.x + btn_w + btn_color_gap
        btn_blue.y = view_color.y + btn_y
        btn_blue.background_color = self.__blue
        btn_blue.tint_color = 'white'
        btn_blue.font = ('.SFUI-Semibold', 20)
        self.v.add_subview(btn_blue)

        btn_orange = ui.Button(name='btn_orange')
        btn_orange.title = 'Orange'
        btn_orange.width = btn_w
        btn_orange.height = btn_h
        btn_orange.x = btn_blue.x + btn_w + btn_color_gap
        btn_orange.y = view_color.y + btn_y
        btn_orange.background_color = self.__orange
        btn_orange.tint_color = 'white'
        btn_orange.font = ('.SFUI-Semibold', 20)
        self.v.add_subview(btn_orange)

        btn_pink = ui.Button(name='btn_pink')
        btn_pink.title = 'Pink'
        btn_pink.width = btn_w
        btn_pink.height = btn_h
        btn_pink.x = btn_orange.x + btn_w + btn_color_gap
        btn_pink.y = view_color.y + btn_y
        btn_pink.background_color = self.__pink
        btn_pink.tint_color = 'white'
        btn_pink.font = ('.SFUI-Semibold', 20)
        self.v.add_subview(btn_pink)

        btn_color_ok = ui.Button(name='btn_color_ok')
        btn_color_ok.title = 'OK'
        btn_color_ok.width = 80
        btn_color_ok.height = 60
        btn_color_ok.x = view_color.x + view_color.width // 2 - btn_color_ok.width - 20
        btn_color_ok.y = btn_blue.y + btn_blue.height + 30
        btn_color_ok.background_color = 'white'
        btn_color_ok.tint_color = 'black'
        btn_color_ok.font = ('.SFUI-Semibold', 20)
        self.v.add_subview(btn_color_ok)

        btn_color_cancel = ui.Button(name='btn_color_cancel')
        btn_color_cancel.title = 'Cancel'
        btn_color_cancel.width = 80
        btn_color_cancel.height = 60
        btn_color_cancel.x = view_color.x + view_color.width // 2 + 20
        btn_color_cancel.y = btn_blue.y + btn_blue.height + 30
        btn_color_cancel.background_color = 'white'
        btn_color_cancel.tint_color = 'black'
        btn_color_cancel.font = ('.SFUI-Semibold', 20)
        self.v.add_subview(btn_color_cancel)

        label_color = ui.Label(name='label_color')
        label_color.text = 'Select the color for this spot.'
        label_color.x = view_color.x + 30
        label_color.y = view_color.y + 10
        label_color.width = view_color.width - 30
        label_color.height = 35
        label_color.font = ('.SFUI-Semibold', 25)
        self.v.add_subview(label_color)

    def create_question_yesno(self):
        view_yesno = ui.View(name='view_yesno')
        view_yesno.width = 425
        view_yesno.height = 200
        view_yesno.x = self.v.width - view_yesno.width + 50
        view_yesno.y = self.v['view_w1'].y + self.v['view_w1'].height + 70
        view_yesno.background_color = '#a8a8a8'
        self.v.add_subview(view_yesno)

        label_yesno = ui.Label(name='label_yesno')
        label_yesno.text = ''
        label_yesno.x = view_yesno.x + 30
        label_yesno.y = view_yesno.y + 10
        label_yesno.width = view_yesno.width - 30
        label_yesno.height = 70
        label_yesno.number_of_lines = 2
        self.v.add_subview(label_yesno)

        btn_dialog_yes = ui.Button(name='btn_dialog_yes')
        btn_dialog_yes.title = 'Yes'
        btn_dialog_yes.width = 80
        btn_dialog_yes.height = 60
        btn_dialog_yes.x = view_yesno.x + view_yesno.width // 2 - btn_dialog_yes.width - 30
        btn_dialog_yes.y = label_yesno.y + label_yesno.height + 20
        btn_dialog_yes.background_color = 'white'
        btn_dialog_yes.tint_color = 'black'
        btn_dialog_yes.font = ('.SFUI-Semibold', 20)
        self.v.add_subview(btn_dialog_yes)

        btn_dialog_no = ui.Button(name='btn_dialog_no')
        btn_dialog_no.title = 'No'
        btn_dialog_no.width = 80
        btn_dialog_no.height = 60
        btn_dialog_no.x = btn_dialog_yes.x + btn_dialog_yes.width + 40
        btn_dialog_no.y = label_yesno.y + label_yesno.height + 20
        btn_dialog_no.background_color = 'white'
        btn_dialog_no.tint_color = 'black'
        btn_dialog_no.font = ('.SFUI-Semibold', 20)
        self.v.add_subview(btn_dialog_no)

    def create_msg_error(self):
        view_error = ui.View(name='view_error')
        view_error.width = 425
        view_error.height = 285
        view_error.x = self.v.width // 2 - view_error.width // 2
        view_error.y = self.v['view_w1'].y + self.v['view_w1'].height
        view_error.background_color = '#a8a8a8'
        self.v.add_subview(view_error)

        label_error = ui.Label(name='label_error')
        label_error.text = ''
        label_error.x = view_error.x + 30
        label_error.y = view_error.y + 10
        label_error.width = view_error.width - 40
        label_error.height = 35
        label_error.font = ('.SFUI-Semibold', 25)
        self.v.add_subview(label_error)

        btn_error = ui.Button(name='btn_error')
        btn_error.title = 'Ok'
        btn_error.width = 80
        btn_error.height = 60
        btn_error.x = view_error.x + view_error.width // 2 - btn_error.width
        btn_error.y = label_error.y + label_error.height + 20
        btn_error.background_color = 'white'
        btn_error.tint_color = 'black'
        btn_error.font = ('.SFUI-Semibold', 20)
        self.v.add_subview(btn_error)

    def create_finish_task(self):
        btn_finish = ui.Button(name='btn_finish')
        btn_finish.title = 'Finished'
        btn_finish.width = 100
        btn_finish.height = 60
        btn_finish.x = 100
        btn_finish.y = self.v.height - btn_finish.height - 200
        btn_finish.background_color = '#96ffff'
        btn_finish.border_width = 2
        btn_finish.corner_radius = 5
        btn_finish.border_color = 'black'
        btn_finish.tint_color = 'black'
        btn_finish.font = ('.SFUI-Semibold', 25)
        btn_finish.enabled = False
        btn_finish.hidden = True
        self.v.add_subview(btn_finish)

        btn_cancel_action = ui.Button(name='btn_cancel_action')
        btn_cancel_action.title = 'Cancel'
        btn_cancel_action.width = 100
        btn_cancel_action.height = 60
        btn_cancel_action.x = btn_finish.x + btn_finish.width + 30
        btn_cancel_action.y = self.v.height - btn_finish.height - 200
        btn_cancel_action.background_color = '#96ffff'
        btn_cancel_action.border_width = 2
        btn_cancel_action.corner_radius = 5
        btn_cancel_action.border_color = 'black'
        btn_cancel_action.tint_color = 'black'
        btn_cancel_action.font = ('.SFUI-Semibold', 25)
        btn_cancel_action.enabled = False
        btn_cancel_action.hidden = True
        self.v.add_subview(btn_cancel_action)

        label_finish = ui.Label(name='label_finish')
        label_finish.text = ''
        label_finish.width = 800
        label_finish.height = 35
        label_finish.x = btn_finish.x
        label_finish.y = btn_finish.y - label_finish.height - 10
        label_finish.font = ('.SFUI-Semibold', 25)
        self.v.add_subview(label_finish)

    def start_socket(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(100000)
        self.client.connect(ADDR)
        self.client.settimeout(None)
        socket_thread = threading.Thread(target=self.receive)
        socket_thread.start()

    def receive(self):
        # client.settimeout(10000)
        connected = True
        while connected:
            msg_length = self.client.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = self.client.recv(msg_length).decode(FORMAT)
                print(msg)
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                else:
                    self.read_msg(msg)

        self.client.close()

    def generate_message(self, previous_action=None, action=None, workspace=None, box_number=None, color=None):
        if previous_action is None:
            previous_action = self.all_action_type[
                self.all_boxes[self.btn_workspace - 1][self.btn_box - 1].previous_state]
        if action is None:
            action = self.all_action_type[self.all_boxes[self.btn_workspace - 1][self.btn_box - 1].current_state]
        if workspace is None:
            workspace = self.btn_workspace
        if box_number is None:
            box_number = self.btn_box
        if color is None:
            color = self.all_boxes[self.btn_workspace - 1][self.btn_box - 1].color

        msg = str(previous_action) + str(action) + str(workspace) + str(box_number) + str(color)
        return msg

    def send(self, msg=None):
        if msg is None:
            msg = self.generate_message()
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)

    def read_msg(self, msg):
        # message: action_type + workspace + box + color
        action_list = {0: 'Robot', 1: 'Done', 2: 'Assigned_to_Human'}
        action_type = action_list[int(msg[0])]
        ws = int(msg[1])
        box = int(msg[2])
        msg_box_name = 'w' + str(ws) + 'b' + str(box)
        color = self.color_list[int(msg[3])]
        tmp_curstate = self.all_boxes[ws][box].current_state
        if action_type == 'Robot':
            self.all_boxes[ws - 1][box - 1].current_state = 'Robot'
            self.flashing_boxes[msg_box_name] = color
            self.all_boxes[ws - 1][box - 1].color = color
            self.icon_changer(msg_box_name, 'iob:load_a_256')
        elif action_type == 'Done':
            self.all_boxes[ws - 1][box - 1].current_state = 'Done'
            self.flashing_boxes.pop(msg_box_name)
            self.icon_changer(msg_box_name, '')
        elif action_type == 'Assigned_to_Human':
            self.all_boxes[ws - 1][box - 1].current_state = 'Assigned_to_Human'
            self.flashing_boxes[msg_box_name] = color
            self.all_boxes[ws - 1][box - 1].color = color
            self.icon_changer(msg_box_name, self.__human_icon)
        self.all_boxes[ws - 1][box - 1].previous_state = tmp_curstate

    def generate_boxes(self):
        for i in range(0, 5):
            for j in range(0, 5):
                self.all_boxes[i].append(Box(workspace=i + 1, box_number=j + 1))

    def assign_actions(self):
        for i in range(1, 6):
            for j in range(1, 6):
                btn_name = 'w' + str(i) + 'b' + str(j)
                self.v[btn_name].action = self.btn_box_click

        self.v['btn_green'].action = self.btn_green_click
        self.v['btn_orange'].action = self.btn_orange_click
        self.v['btn_blue'].action = self.btn_blue_click
        self.v['btn_pink'].action = self.btn_pink_click
        self.v['btn_color_ok'].action = self.btn_color_ok_click
        self.v['btn_color_cancel'].action = self.btn_color_cancel_click
        self.v['btn_agent_ok'].action = self.btn_agent_ok_click
        self.v['btn_agent_cancel'].action = self.btn_agent_cancel_click
        self.v['btn_dialog_yes'].action = self.btn_yesno_yes
        self.v['btn_dialog_no'].action = self.btn_yesno_no
        self.v['btn_error'].action = self.btn_error_ok
        self.v['btn_finish'].action = self.btn_finish
        self.v['btn_cancel_action'].action = self.btn_cancel_action

    def disable_enable_buttons(self, action='disable', excepted_buttons=[]):
        if action == 'disable':
            tf = False
        else:
            tf = True

        for i in range(1, 6):
            for ii in range(1, 6):
                btn_name = 'w' + str(i) + 'b' + str(ii)
                if btn_name not in excepted_buttons:
                    self.v[btn_name].enabled = tf

    def show_question_colors(self):

        self.v['view_color'].hidden = False
        self.v['btn_green'].hidden = False
        self.v['btn_orange'].hidden = False
        self.v['btn_blue'].hidden = False
        self.v['btn_pink'].hidden = False
        self.v['btn_color_ok'].hidden = False
        self.v['btn_color_cancel'].hidden = False
        self.v['label_color'].hidden = False

        self.v['view_color'].enabled = True
        self.v['btn_green'].enabled = True
        self.v['btn_orange'].enabled = True
        self.v['btn_blue'].enabled = True
        self.v['btn_pink'].enabled = True
        self.v['btn_color_ok'].enabled = False
        self.v['btn_color_cancel'].enabled = True
        self.v['label_color'].enabled = True

    def hide_question_colors(self):
        self.v['label_color'].hidden = True
        self.v['view_color'].hidden = True
        self.v['btn_green'].hidden = True
        self.v['btn_orange'].hidden = True
        self.v['btn_blue'].hidden = True
        self.v['btn_pink'].hidden = True
        self.v['btn_color_ok'].hidden = True
        self.v['btn_color_cancel'].hidden = True

        self.v['label_color'].enabled = False
        self.v['view_color'].enabled = False
        self.v['btn_green'].enabled = False
        self.v['btn_orange'].enabled = False
        self.v['btn_blue'].enabled = False
        self.v['btn_pink'].enabled = False
        self.v['btn_color_ok'].enabled = False
        self.v['btn_color_cancel'].enabled = False

    def show_question_agent(self):
        self.v['label_agent'].hidden = False
        self.v['view_agent'].hidden = False
        self.v['btn_agent_select'].hidden = False
        self.v['btn_agent_ok'].hidden = False
        self.v['btn_agent_cancel'].hidden = False

        self.v['label_agent'].enabled = True
        self.v['view_agent'].enabled = True
        self.v['btn_agent_select'].enabled = True
        self.v['btn_agent_ok'].enabled = True
        self.v['btn_agent_cancel'].enabled = True

    def hide_question_agent(self):
        self.v['label_agent'].hidden = True
        self.v['view_agent'].hidden = True
        self.v['btn_agent_select'].hidden = True
        self.v['btn_agent_ok'].hidden = True
        self.v['btn_agent_cancel'].hidden = True

        self.v['label_agent'].enabled = False
        self.v['view_agent'].enabled = False
        self.v['btn_agent_select'].enabled = False
        self.v['btn_agent_ok'].enabled = False
        self.v['btn_agent_cancel'].enabled = False

    def show_question_yesno(self, btn_state):
        if btn_state == 'Assigned_to_Robot':
            self.v['label_yesno'].text = 'Do you want to cancel this assignment?'
        elif btn_state == 'Assigned_to_Human':
            self.v[
                'label_yesno'].text = 'Do you want to do this task assigned by Fetch?'
        elif btn_state == 'Human':
            self.v['label_yesno'].text = 'Do you want to select another box?'
        elif btn_state == 'Done':
            self.v['label_yesno'].text = 'Do you want to return this block?'

        self.v['view_yesno'].hidden = False
        self.v['btn_dialog_yes'].hidden = False
        self.v['btn_dialog_no'].hidden = False
        self.v['label_yesno'].hidden = False

        self.v['view_yesno'].enabled = True
        self.v['btn_dialog_yes'].enabled = True
        self.v['btn_dialog_no'].enabled = True
        self.v['label_yesno'].enabled = True

    def hide_question_yesno(self):
        self.v['view_yesno'].hidden = True
        self.v['btn_dialog_yes'].hidden = True
        self.v['btn_dialog_no'].hidden = True
        self.v['label_yesno'].hidden = True

        self.v['view_yesno'].enabled = False
        self.v['btn_dialog_yes'].enabled = False
        self.v['btn_dialog_no'].enabled = False
        self.v['label_yesno'].enabled = False

    def hide_msg_error(self):
        self.v['view_error'].hidden = True
        self.v['btn_error'].hidden = True
        self.v['label_error'].hidden = True

        self.v['view_error'].enabled = False
        self.v['btn_error'].enabled = False
        self.v['label_error'].enabled = False

    def show_msg_error(self, type, precedence=None):
        if type == 'precedence':
            lb_txt = ''
            for i in precedence:
                lb_txt += str(i) + ', '
            self.v['label_error'].text = 'ِYou need to do first task(s) ' + lb_txt[0:-2] + '.'
        else:
            self.v['label_error'].text = 'Fetch is currently doing this action. Please select another spot.'
        self.v['view_error'].hidden = False
        self.v['btn_error'].hidden = False
        self.v['label_error'].hidden = False

        self.v['view_error'].enabled = True
        self.v['btn_error'].enabled = True
        self.v['label_error'].enabled = True

    def show_finish_cancel(self, text):
        self.v['btn_finish'].enabled = True
        self.v['btn_finish'].hidden = False
        self.v['btn_cancel_action'].enabled = True
        self.v['btn_cancel_action'].hidden = False
        self.v['label_finish'].enabled = True
        self.v['label_finish'].hidden = False
        self.v['label_finish'].text = text

    def hide_finish_cancel(self):
        self.v['btn_finish'].enabled = False
        self.v['btn_finish'].hidden = True
        self.v['btn_cancel_action'].enabled = False
        self.v['btn_cancel_action'].hidden = True
        self.v['label_finish'].text = ''
        self.v['label_finish'].enabled = False
        self.v['label_finish'].hidden = True

    def is_precedence_constraint(self, box):
        ws = box.workspace
        bn = box.number
        done = True
        precedence = []

        if bn > 1:
            for i in range(0, bn - 1):
                done = done and (self.all_boxes[ws - 1][i].current_state == 'Done')
                if self.all_boxes[ws - 1][i].current_state != 'Done':
                    precedence.append(i + 1)
        return done, precedence

    def btn_box_click(self, sender):
        self.btn_workspace = int(sender.name[1])
        self.btn_box = int(sender.name[3])
        ww = self.btn_workspace - 1
        bb = self.btn_box - 1
        self.box_name = 'w' + str(self.btn_workspace) + 'b' + str(self.btn_box)
        self.disable_enable_buttons()
        cr_state = self.all_boxes[ww][bb].current_state
        if cr_state == 'Free':
            done, precedence = self.is_precedence_constraint(self.all_boxes[ww][bb])
            if done:
                self.show_question_colors()
            else:
                self.show_msg_error(type='precedence', precedence=precedence)
        elif cr_state == 'Assigned_to_Robot':
            self.show_question_yesno('Assigned_to_Robot')
        elif cr_state == 'Assigned_to_Human':
            self.show_question_yesno('Assigned_to_Human')
        elif cr_state == 'Human':
            self.show_question_yesno('Human')
        elif cr_state == 'Done':
            self.show_question_yesno('Done')
        elif cr_state == 'Robot':
            self.show_msg_error(type='robot')

    def btn_green_click(self, sender):
        self.selected_color = self.__green
        self.v['btn_color_ok'].enabled = True
        self.v['btn_green'].enabled = False
        self.v['btn_orange'].enabled = True
        self.v['btn_blue'].enabled = True
        self.v['btn_pink'].enabled = True

    def btn_blue_click(self, sender):
        self.selected_color = self.__blue
        self.v['btn_color_ok'].enabled = True
        self.v['btn_green'].enabled = True
        self.v['btn_orange'].enabled = True
        self.v['btn_blue'].enabled = False
        self.v['btn_pink'].enabled = True

    def btn_pink_click(self, sender):
        self.selected_color = self.__pink
        self.v['btn_color_ok'].enabled = True
        self.v['btn_green'].enabled = True
        self.v['btn_orange'].enabled = True
        self.v['btn_blue'].enabled = True
        self.v['btn_pink'].enabled = False

    def btn_orange_click(self, sender):
        self.selected_color = self.__orange
        self.v['btn_color_ok'].enabled = True
        self.v['btn_green'].enabled = True
        self.v['btn_orange'].enabled = False
        self.v['btn_blue'].enabled = True
        self.v['btn_pink'].enabled = True

    def btn_color_ok_click(self, sender):
        self.hide_question_colors()
        self.show_question_agent()

    def btn_color_cancel_click(self, sender):
        self.hide_question_colors()
        self.disable_enable_buttons(action='enable')
        self.selected_color = None

    def btn_agent_ok_click(self, sender):
        agent_ind = self.v['btn_agent_select'].selected_index
        ww = self.btn_workspace - 1
        bb = self.btn_box - 1
        if agent_ind == 0:
            self.selected_agent = 'Human'
            self.all_boxes[ww][bb].previous_state = self.all_boxes[ww][bb].current_state
            self.all_boxes[ww][bb].current_state = 'Human'
            self.color_changer(self.box_name, self.selected_color)
            block_color = self.color_names[self.selected_color]
            label_text = 'Placing a ' + block_color + ' block on workspace #' + str(
                self.btn_workspace) + ' and spot #' + str(self.btn_box)
            self.show_finish_cancel(label_text)


        else:
            self.selected_agent = 'Fetch'
            self.all_boxes[ww][bb].previous_state = self.all_boxes[ww][bb].current_state
            self.all_boxes[ww][bb].current_state = 'Assigned_to_Robot'
            self.color_changer(self.box_name, self.selected_color)
            self.icon_changer(self.box_name, self.__robot_icon)
            self.disable_enable_buttons(action='enable')

        self.send()
        self.hide_question_agent()

    def btn_agent_cancel_click(self, sender):
        self.selected_color = None
        self.selected_agent = None
        self.hide_question_agent()
        self.disable_enable_buttons(action='enable')

    def btn_yesno_yes(self, sender):
        ww = self.btn_workspace - 1
        bb = self.btn_box - 1
        cr_state = self.all_boxes[ww][bb].current_state
        if cr_state == 'Assigned_to_Robot':
            self.all_boxes[ww][bb].current_state = 'Free'
            self.color_changer(self.box_name, 'white')
            self.icon_changer(self.box_name, '')
            self.disable_enable_buttons(action='enable')
        elif cr_state == 'Assigned_to_Human':
            self.all_boxes[ww][bb].current_state = 'Human'
            self.flashing_boxes.pop(self.box_name)
            self.icon_changer(self.box_name, '')
            block_color = self.color_names[self.all_boxes[ww][bb].color]
            label_text = 'Placing a ' + block_color + ' block on workspace #' + str(
                self.btn_workspace) + ' and spot #' + str(self.btn_box)
            self.show_finish_cancel(label_text)

        elif cr_state == 'Human':
            if self.all_boxes[ww][bb].previous_state == 'Assigned_to_Human':
                self.all_boxes[ww][bb].current_state = 'Assigned_to_Human'
                self.icon_changer(self.box_name, self.__human_icon)
                self.flashing_boxes[self.box_name] = self.all_boxes[ww][bb].color
                msg = str(self.all_action_type['cancel_human_assigned']) + str(self.btn_workspace) + str(
                    self.btn_box) + str(self.color_list[self.selected_color])
            else:
                self.all_boxes[ww][bb].current_state = 'Free'
                self.color_changer(self.box_name, 'white')
                msg = str(self.all_action_type['cancel_human']) + str(self.btn_workspace) + str(self.btn_box) + str(
                    self.color_list[self.selected_color])
            self.disable_enable_buttons(action='enable')
            self.hide_finish_cancel()

        elif cr_state == 'Done':
            self.all_boxes[ww][bb].current_state = 'Return'
            block_color = self.all_boxes[ww][bb].color
            label_text = 'Returning the ' + block_color + ' block on workspace #' + str(
                self.btn_workspace) + ' and spot #' + str(self.btn_box)
            self.all_boxes[ww][bb].previous_color = self.all_boxes[ww][bb].color
            self.show_finish_cancel(label_text)
            self.color_changer(self.box_name, 'white')

        self.send()
        self.all_boxes[ww][bb].previous_state = cr_state
        self.hide_question_yesno()

    def btn_yesno_no(self, sender):
        self.hide_question_yesno()
        self.disable_enable_buttons(action='enable')

    def btn_error_ok(self, sender):
        self.hide_msg_error()
        self.disable_enable_buttons(action='enable')

    def btn_finish(self, sender):
        ww = self.btn_workspace - 1
        bb = self.btn_box - 1
        cr_state = self.all_boxes[ww][bb].current_state
        if cr_state == 'Return':
            self.all_boxes[ww][bb].previou_state = cr_state
            self.all_boxes[ww][bb].current_state = 'Free'

        elif cr_state == 'Human':
            self.all_boxes[ww][bb].previou_state = cr_state
            self.all_boxes[ww][bb].current_state = 'Done'

        self.send()
        self.hide_finish_cancel()
        self.disable_enable_buttons(action='enable')

    def btn_cancel_action(self, sender):
        ww = self.btn_workspace - 1
        bb = self.btn_box - 1
        cr_state = self.all_boxes[ww][bb].current_state
        if cr_state == 'Human':
            if self.all_boxes[ww][bb].previous_state == 'Assigned_to_Human':
                self.all_boxes[ww][bb].current_state = 'Assigned_to_Human'
                self.all_boxes[ww][bb].previous_state = 'Human'
                self.icon_changer(self.box_name, self.__human_icon)
                self.flashing_boxes[self.box_name] = self.all_boxes[ww][bb].color

            else:
                self.all_boxes[ww][bb].current_state = 'Free'
                self.color_changer(self.box_name, 'white')
        elif cr_state == 'Return':
            self.all_boxes[ww][bb].current_state = self.all_boxes[ww][bb].previous_state
            self.all_boxes[ww][bb].previous_state = 'Return'
            self.color_changer(self.box_name, self.all_boxes[ww][bb].previous_color)

        self.send()
        self.hide_finish_cancel()
        self.disable_enable_buttons(action='enable')

    def color_flasher(self):
        while True:
            if self.flashing_boxes:
                fl_bx = dict(self.flashing_boxes)
                for box in fl_bx:
                    self.v[box].background_color = fl_bx[box]
                time.sleep(0.8)
                fl_bx = dict(self.flashing_boxes)
                for box in fl_bx:
                    self.v[box].background_color = 'white'
                    self.v[box].tint_color = 'black'
                time.sleep(0.8)
                for box in fl_bx:
                    self.v[box].background_color = fl_bx[box]
                    self.v[box].tint_color = 'ffffff'

    def icon_changer(self, box_name, icon):
        self.v[box_name].image = ui.Image.named(icon)
        if icon == '' or icon is None:
            self.v[box_name].tint_color = ''
        else:
            self.v[box_name].tint_color = '#ffffff'

    def color_changer(self, box_name, color):
        self.v[box_name].background_color = color
        self.all_boxes[self.btn_workspace - 1][self.btn_box - 1].color = color


gui = Userinterface()
# time.sleep(8)
# gui.flashing_boxes.pop('w1b1')

gui.read_msg('0110')
time.sleep(3)
gui.read_msg('2121')
time.sleep(3)
gui.read_msg('1110')
