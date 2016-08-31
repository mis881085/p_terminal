from tkinter import *
from UartController import *

root_ui = Tk()
TEXT_WIDTH = 200 #word width
BTN_WIDTH = 20 #word width
TEXT_HEIGHT = 60
top_frame = Frame(root_ui, bg = "black")
top_frame.pack(side = "top")
btn_frame = Frame(top_frame, height = TEXT_HEIGHT, bg = "black")
btn_frame.pack(side = "left", fill="y", expand = False)

quick_send_cmd_btn_list = []
for i in range(10):
    quick_send_cmd_btn = Button(btn_frame, width = BTN_WIDTH, height = 1, bg = "gray")
    quick_send_cmd_btn.pack(side = "top", fill = "x", expand = False)
    quick_send_cmd_btn_list.append(quick_send_cmd_btn)

log_frame = Frame(top_frame, width = TEXT_WIDTH, height = TEXT_HEIGHT)
log_frame.pack(side = "right")

log_text = Text(log_frame, width = TEXT_WIDTH, height = TEXT_HEIGHT, wrap = WORD, bg = "black", fg = "white")
log_text.insert(INSERT, "Hello...\n")
log_text.pack(side = "left", fill="both", expand = True)
log_scrollbar = Scrollbar(log_frame, command = log_text.yview)
log_scrollbar.pack(side = "right", fill="y", expand = False)
#for i in range(200):
#    log_text.insert(INSERT, "World...{}\n".format(i))
log_text.config(state = DISABLED) # 禁止編輯功能

in_text = Entry(root_ui, width = TEXT_WIDTH)
def in_text_cb(event):
    print("[]"+in_text.get()+"[]")
    uart.Send(in_text.get()+"\n")
    in_text.delete(0, END)

in_text.bind("<Return>", in_text_cb)
in_text.pack(side = "bottom")
in_text.focus()

def insert_log_text(data):
    TEXT_LOG_SIZE = 1000.0
    DEL_LOG_SIZE = TEXT_LOG_SIZE / 10;
    log_text.config(state = NORMAL)
    log_text.insert(END, data)

    if (float(log_text.index(END)) > TEXT_LOG_SIZE):
        log_text.delete(1.0, DEL_LOG_SIZE)

    log_text.config(state = DISABLED)
    log_text.yview_moveto(1.0)

uart = uart()
uart.SetEchoFunction(insert_log_text)
root_ui.mainloop()
