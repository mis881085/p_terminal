# -*- coding: utf-8 -*-
from tkinter import *
from SmartButton import *
import functools
from UartController import *
TEXT_WIDTH = 200 #word width
BTN_WIDTH = 20 #word width
TEXT_HEIGHT = 60
QUICK_SEND_BTN_NUM = 10

def quick_send_cmd_btn_cb(btn_idx, event):
    #send key
    btn_text = quick_send_cmd_btn_list[btn_idx].cget("text")
    if len(btn_text) is not 0:
        uart.Send(btn_text+"\n")
        smart_button.UpdateButton(btn_text)


def in_text_cb(event):
    print("[]"+in_text.get()+"[]")
    uart.Send(in_text.get()+"\n")

    smart_button.UpdateButton(in_text.get())
    smart_button.Debug()
    for i in range(QUICK_SEND_BTN_NUM):
        btn_text = smart_button.GetButtonInfo(i)
        if btn_text is not None:
            quick_send_cmd_btn_list[i].config(text = btn_text)
    in_text.delete(0, END)

def insert_log_text(data):
    TEXT_LOG_SIZE = 1000.0
    DEL_LOG_SIZE = TEXT_LOG_SIZE / 10;
    log_text.config(state = NORMAL)
    log_text.insert(END, data)

    if (float(log_text.index(END)) > TEXT_LOG_SIZE):
        log_text.delete(1.0, DEL_LOG_SIZE)

    log_text.config(state = DISABLED)
    log_text.yview_moveto(1.0)

root_ui = Tk()
top_frame = Frame(root_ui, bg = "black")
top_frame.pack(side = "top")
btn_frame = Frame(top_frame, height = TEXT_HEIGHT, bg = "black")
btn_frame.pack(side = "left", fill="y", expand = False)

quick_send_cmd_btn_list = []
for i in range(QUICK_SEND_BTN_NUM):
    quick_send_cmd_btn = Button(btn_frame, width = BTN_WIDTH, height = 1, bg = "gray")
    quick_send_cmd_btn.pack(side = "top", fill = "x", expand = False)
    press_quick_send_cmd_btn_with_btn_idx = functools.partial(quick_send_cmd_btn_cb, i)
    quick_send_cmd_btn.bind("<Button-1>", press_quick_send_cmd_btn_with_btn_idx)
    quick_send_cmd_btn.config(text = "{}".format(i))
    quick_send_cmd_btn_list.append(quick_send_cmd_btn)


log_frame = Frame(top_frame, width = TEXT_WIDTH, height = TEXT_HEIGHT)
log_frame.pack(side = "right")

log_text = Text(log_frame, width = TEXT_WIDTH, height = TEXT_HEIGHT, wrap = WORD, bg = "black", fg = "white")
log_text.insert(INSERT, "Hello...\n")
log_text.pack(side = "left", fill="both", expand = True)
log_scrollbar = Scrollbar(log_frame, command = log_text.yview)
log_scrollbar.pack(side = "right", fill="y", expand = False)
log_text.config(state = DISABLED) # 禁止編輯功能

in_text = Entry(root_ui, width = TEXT_WIDTH)

in_text.bind("<Return>", in_text_cb)
in_text.pack(side = "bottom")
in_text.focus()

uart = uart()
uart.SetEchoFunction(insert_log_text)
smart_button = smart_button(QUICK_SEND_BTN_NUM)

root_ui.mainloop()
