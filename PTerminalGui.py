# -*- coding: utf-8 -*-
from tkinter import *
from SmartButton import *
import functools
from UartController import *
TEXT_WIDTH = 200 #word width
BTN_WIDTH = 20 #word width
BTN_WRAPLENGTH = 160
TEXT_HEIGHT = 60
QUICK_SEND_BTN_NUM = 20
class termanialmodel():
    def __init__(self):
        self.uart = uart()
        self.smart_button = smart_button(QUICK_SEND_BTN_NUM)

class termanialview():
    def __init__(self, master):

        self.top_frame = Frame(master, bg = "#444444")
        self.top_frame.pack(side = "top", fill = 'x', expand = True)
        self.btn_frame = Frame(self.top_frame, height = TEXT_HEIGHT, bg = "#444444")
        self.btn_frame.pack(side = "left", fill = "both", expand = False)
        self.quick_send_cmd_btn_list = []
        for i in range(QUICK_SEND_BTN_NUM):
            quick_send_cmd_btn = Button(self.btn_frame, width = BTN_WIDTH, wraplength = BTN_WRAPLENGTH, justify = LEFT, bg = "blue")
            #quick_send_cmd_btn = Button(self.btn_frame, bg = "#000000", fg = "#4400CC", activebackground = "#CC0000", activeforeground = "#00DD00")
            quick_send_cmd_btn.pack(side = "top", fill = "x", expand = False)
            quick_send_cmd_btn.config(text = "{}".format(i))
            self.quick_send_cmd_btn_list.append(quick_send_cmd_btn)

        self.log_frame = Frame(self.top_frame, width = TEXT_WIDTH, height = TEXT_HEIGHT)
        self.log_frame.pack(side = "right")

        self.log_text = Text(self.log_frame, width = TEXT_WIDTH, height = TEXT_HEIGHT, wrap = WORD, bg = "black", fg = "white")
        #self.log_text.insert(INSERT, "Hello...\n")
        self.log_text.pack(side = "left", fill="both", expand = True)
        self.log_scrollbar = Scrollbar(self.log_frame, command = self.log_text.yview)
        self.log_scrollbar.pack(side = "right", fill="y", expand = False)
        self.log_text.config(state = DISABLED) # 禁止編輯功能

        self.in_text = Entry(master, width = TEXT_WIDTH)

        self.in_text.pack(side = "bottom")
        self.in_text.focus()

class termanialcontroller():
    def __init__(self):
        self.root = Tk()
        self.model = termanialmodel()
        self.view = termanialview(self.root)

        for i in range(QUICK_SEND_BTN_NUM):
            press_quick_send_cmd_btn_with_btn_idx = functools.partial(self.quick_send_cmd_btn_cb, i)
            self.view.quick_send_cmd_btn_list[i].bind("<Button-1>", press_quick_send_cmd_btn_with_btn_idx)

        self.view.in_text.bind("<Return>", self.in_text_cb)
        self.model.uart.SetEchoFunction(self.insert_log_text)
    def run(self):
        self.root.title("P_Terminal")
        self.root.mainloop()

    def quick_send_cmd_btn_cb(self, btn_idx, event):
        #send key
        btn_text = self.view.quick_send_cmd_btn_list[btn_idx].cget("text")
        if len(btn_text) is not 0:
            self.model.uart.Send(btn_text + "\n")
            self.model.smart_button.UpdateButton(btn_text)

    def in_text_cb(self, event):
        self.model.uart.Send(self.view.in_text.get() + "\n")
        self.model.smart_button.UpdateButton(self.view.in_text.get())
        self.model.smart_button.Debug()
        for i in range(QUICK_SEND_BTN_NUM):
            btn_text = self.model.smart_button.GetButtonInfo(i)
            if btn_text is not None:
                self.view.quick_send_cmd_btn_list[i].config(text = btn_text)
        self.view.in_text.delete(0, END)

    def insert_log_text(self, data):
        TEXT_LOG_SIZE = 1000.0
        DEL_LOG_SIZE = TEXT_LOG_SIZE / 10
        self.view.log_text.config(state = NORMAL)
        self.view.log_text.insert(END, data)
        if (float(self.view.log_text.index(END)) > TEXT_LOG_SIZE):
            self.view.log_text.delete(1.0, DEL_LOG_SIZE)
        self.view.log_text.config(state = DISABLED)
        self.view.yview_moveto(1.0)

c = termanialcontroller()
c.run()
