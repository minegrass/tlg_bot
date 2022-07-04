import tkinter.messagebox
from tkinter import *

import main
from main import TlgBot
import time

# https://t.me/MEXCJapan

root = Tk()
root.title('飞机推广')
root.geometry('450x300')
text_list = []

def start_spam(group_name, min, max):
    print(f'spamming to {group_name} min {min} max {max}')
    tkinter.messagebox.showinfo(title="发送中", message='请耐心等待')
    start_btn['state'] = 'disable'

def show_good_bot():
    good_count = main.get_good_bot()
    good_bot_count.config(text=f'{good_count}个未封号')

def show_frame(frame):
    frame.tkraise()

def add_new_text(text):
    print(f'added {text}')
    text_setting_input.delete(0,'end')
    text_list.append(text)

def clear_text():
    print('clear all text')
    text_list.clear()

def check_text():
    print('check all text')
    show_text = ''
    if len(text_list) == 0:
        show_text='库已清空，请添加'
    else :
        for text in text_list:
            show_text += f'{text}\n'
    # print(show_text)

    tkinter.messagebox.showinfo(title="语句库", message=f'当前语句：\n{show_text}')

def scrap_group(group_link):
    print(f'scraping target group >> {group_link}')

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

frame1 = Frame(root, width=450, height=300, bg='grey')
frame2 = Frame(root, width=450, height=300, bg='grey')
frame3 = Frame(root, width=450, height=300, bg='grey')

for frame in (frame1, frame2, frame3):
    frame.grid(row=0, column=0, sticky='nsew')

# ==================Frame 1 code
frame1_title = Label(frame1, text='私信页', font='times 35', bg='grey')
frame1_title.grid(column=0, columnspan=2, row=0, padx=10, pady=10)

frame1_btn = Button(frame1, text='换页', command=lambda: show_frame(frame2))
frame1_btn.grid(column=2, row=0, padx=10, sticky='e')
frame1_btn2 = Button(frame1, text='设定', command=lambda: show_frame(frame3))
frame1_btn2.grid(column=3, row=0, sticky='w')

target_label = Label(frame1, text="目标群名：", bg="grey")
target_label.grid(column=0, row=1, padx=10, pady=10)
target_input = Entry(frame1, width=40)
target_input.grid(column=1, columnspan=2, row=1, padx=10, pady=10)

wait_min_input = Entry(frame1, width=40)
wait_min_label = Label(frame1, text="最低等待时间(秒）：", bg="grey")
wait_min_label.grid(column=0, row=2, padx=10, pady=10)
wait_min_input.grid(column=1, columnspan=2, row=2, padx=10, pady=10)

wait_max_input = Entry(frame1, width=40)
wait_max_label = Label(frame1, text="最高等待时间(秒）：", bg="grey")
wait_max_label.grid(column=0, row=3, padx=10, pady=10)
wait_max_input.grid(column=1, columnspan=2, row=3, padx=10, pady=10)

start_btn = Button(frame1, text="开始推送", width=10,
                   command=lambda: start_spam(target_input.get(), wait_min_input.get(), wait_max_input.get()))
start_btn.grid(column=1, row=4, padx=10, pady=10)
# ==================Frame 2 code
frame2_title = Label(frame2, text='数据收集页', font='times 35', bg='grey')
frame2_title.grid(column=1, row=0, padx=10, pady=10)

frame2_btn = Button(frame2, text='换页', command=lambda: show_frame(frame1))
frame2_btn.grid(column=2, row=0, padx=10)
frame2_btn2 = Button(frame2, text='设定', command=lambda: show_frame(frame3))
frame2_btn2.grid(column=3, row=0)

group_link_input_label = Label(frame2, text="群组链接:", bg='grey')
group_link_input = Entry(frame2, width=50)
group_link_input.grid(columnspan=2, column=1, row=1, padx=10, pady=10)
group_link_input_label.grid(column=0, row=1, padx=10, pady=10)
group_link_btn = Button(frame2, text="获取数据", width=15,command=lambda: scrap_group(group_link_input.get()))
group_link_btn.grid(column=1, row=2)

# ==================Frame 3 code
frame3_title = Label(frame3, text='设置', font='times 35', bg='grey')
frame3_title.grid(column=1, row=0, pady=10, padx=10)

frame3_btn = Button(frame3, text='换页', command=lambda: show_frame(frame1))
frame3_btn.grid(column=4, row=0, padx=10)

text_setting_title = Label(frame3, text='推送语句:', bg='grey')
text_setting_title.grid(column=1, row=1)
text_setting_input = Entry(frame3, width=35)
text_setting_input.grid(column=2,columnspan=2, row=1, padx=10)
text_add_btn = Button(frame3, text='添加',command=lambda: add_new_text(text_setting_input.get()))
text_add_btn.grid(column=2, row=2,sticky='w')
text_clear_btn = Button(frame3, text='清空',command=clear_text)
text_clear_btn.grid(column=2, row=2)
text_check_btn = Button(frame3, text='查看',command=check_text)
text_check_btn.grid(column=2, row=2,pady=10,sticky='e')

good_bot_count_label = Label(frame3,text='可用号数:',bg='grey')
good_bot_count_label.grid(column=1,row=3,pady=10)
good_bot_count = Label(frame3,text='未刷新',bg='grey')
good_bot_count.grid(column=2,row=3)
good_bot_count_btn = Button(frame3,text='刷新',command=show_good_bot)
good_bot_count_btn.grid(column=3,row=3)
show_frame(frame1)

# frame1 = Frame(root)
# frame1.grid(row=0,column=0,sticky='nsew')
# frame2 = Frame(root)
# frame2.grid(row=0,column=0,sticky='nsew')


root.mainloop()
