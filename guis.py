# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
import time
import os
import shutil
import subprocess
import socket

try:
    import pymysql
except:
    p = subprocess.Popen(["pip","install","pymysql"], stdout=subprocess.PIPE, universal_newlines=True, stderr=subprocess.STDOUT)
    print("*** cmd : pip install paramiko ***")
    for out in iter(p.stdout.readline,""):
        print(out)
    import pymysql

try:
    import image
except:
    q = subprocess.Popen(["pip","install","image"], stdout=subprocess.PIPE, universal_newlines=True, stderr=subprocess.STDOUT)
    print("*** cmd : pip install image ***")
    for out in iter(q.stdout.readline,""):
        print(out)

# text scroller
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog as fd
from os import path
from urllib.request import urlopen


def layout():
    #main 객체
    global win
    win = tk.Tk()


    #title - step1
    win.title("python gui cheatsheet(step1)")


    #프로그램 실행시 처음 나타날 gui 가운데로 위치 조정
    w = 600
    h = 400
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    x = (sw - w) / 2
    y = (sh - h) / 2
    win.geometry('%dx%d+%d+%d' % (w, h, x, y))


    # 메뉴바 생성
    menu_bar = tk.Menu(win)
    win.config(menu=menu_bar)


    # label -> 이름, command -> 콜백함수 이름(def _quit 함수) - step2
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="New") 
    file_menu.add_command(label="Exit", command=_quit)
    # new, exit를 File이라는 메뉴에 종속
    menu_bar.add_cascade(label="step2", menu=file_menu)


    # example 2
    file_menu2 = tk.Menu(menu_bar, tearoff=0)
    file_menu2.add_command(label="?") 
    file_menu2.add_command(label="about PGC", command=_about)
    menu_bar.add_cascade(label="Help", menu=file_menu2)


    # notebook - step3
    tabControl = tk.ttk.Notebook(win)
    tab1 = tk.ttk.Frame(tabControl)
    tabControl.add(tab1, text='step3')
    tab2 = tk.ttk.Frame(tabControl)
    tabControl.add(tab2, text='step3_1')
    tab3 = tk.ttk.Frame(tabControl)
    tabControl.add(tab3, text='step3_2')
    tab4 = tk.ttk.Frame(tabControl)
    tabControl.add(tab4, text='step3_4')
    tabControl.pack(expand=1, fill="both")


    # 정렬로 위치 설정(column -> x축, row -> y축), 간격은 자동으로 설정됨 - step4
    blank_label1 = tk.Label(tab1, text="step4(0,0)")
    blank_label1.grid(column=0, row=0)
    blank_label2 = tk.Label(tab1, text="step4(1,0)aaaa")
    blank_label2.grid(column=1, row=0)
    blank_label3 = tk.Label(tab1, text="step4(0,1)bbbb")
    blank_label3.grid(column=0, row=1)
    blank_label4 = tk.Label(tab1, text="step4(1,1)")
    blank_label4.grid(column=1, row=1)


    #button - step5
    tkbutton = tk.Button(tab1, text="step5", command=_button, height=3, width=8, font=("맑은고딕", 10), relief="ridge", bg='white')
    tkbutton.grid(column=0, row=2)


    #text area - step6
    string1 = tk.StringVar()
    string1.set("step6")
    textboxes = tk.Entry(tab1, width=20, text='step6', textvariable=string1)
    textboxes.grid(column=0, row=3)


    #scrollbar - step7
    step7string = 'step7_1,step7_1\nstep7_2,step7_1\nstep7_3,step7_1\nstep7_4,step7_1\nstep7_5\nstep7_6,step7_1\n'
    srlbar = scrolledtext.ScrolledText(tab1, width=20, height=3, wrap=tk.WORD)
    srlbar.grid(column=0, row=4)
    srlbar.insert(tk.INSERT,step7string)


    #frame - step8
    frame1 = tk.LabelFrame(tab1, text='step8')
    frame1.grid(column=0, row=5)
    tk.Label(frame1, text="step8_1").grid(column=0, row=0, sticky=tk.W)
    tk.Label(frame1, text="step8_2").grid(column=1, row=0, sticky=tk.W)
    tk.Label(frame1, text="step8_3").grid(column=2, row=0, sticky=tk.W)


    #choice - step9
    choice_number = tk.StringVar()
    number_chosen = ttk.Combobox(tab1, width=12, textvariable=choice_number, state='readonly')
    number_chosen['values'] = ('step9','step9_1','step9_2','step9_3','step9_4')
    number_chosen.grid(column=0, row=6)
    number_chosen.current(0)


    #checkbutton - step10
    frame2 = tk.LabelFrame(tab1, text='step10')
    frame2.grid(column=0, row=7)
    
    chVarDis = tk.IntVar()
    check1 = tk.Checkbutton(frame2, text='disabled', variable=chVarDis, state='disabled')
    check1.select()
    check1.grid(column=0, row=0, sticky=tk.W)

    chVarUn = tk.IntVar()
    check2 = tk.Checkbutton(frame2, text='unchecked', variable=chVarUn)
    check2.deselect()
    check2.grid(column=1, row=0, sticky=tk.W)

    chVarEn = tk.IntVar()
    check3 = tk.Checkbutton(frame2, text='enabled', variable=chVarEn)
    check3.select()
    check3.grid(column=2, row=0, sticky=tk.W)


    #radio - step11
    frame3 = tk.LabelFrame(tab1, text='step11')
    frame3.grid(column=0, row=8)
    global radVar
    radVar = tk.IntVar()
    
    rad1 = tk.Radiobutton(frame3, text="red", variable=radVar, value=1, command=radCall)
    rad1.grid(column=0, row=0, sticky=tk.W)
    rad2 = tk.Radiobutton(frame3, text="blue", variable=radVar, value=2, command=radCall)
    rad2.grid(column=1, row=0, sticky=tk.W)
    rad3 = tk.Radiobutton(frame3, text="green", variable=radVar, value=3, command=radCall)
    rad3.grid(column=2, row=0, sticky=tk.W)


    #padx : 좌우 여유 픽셀(margin-left, margin-right), pady : 상하(margin-top, margin-bottom) - step12
    frame_margin = tk.LabelFrame(tab1, text='step12')
    frame_margin.grid(column=1, row=2, padx=5, pady=10)
    tk.Label(frame_margin, text="step12_1").grid(column=0, row=0, sticky=tk.W)
    tk.Label(frame_margin, text="step12_2").grid(column=1, row=0, sticky=tk.W)
    tk.Label(frame_margin, text="step12_3").grid(column=2, row=0, sticky=tk.W)
    

    #spin - step13
    spin = tk.Spinbox(tab1, from_=0, to=10, bd=5)
    spin.grid(column=1, row=4)

    #picture - step14
    img = tk.PhotoImage(file="picture.png").subsample(5) #subsample -> 1/x중 x값
    imglabel = tk.Label(tab1, image=img)
    imglabel.grid(column=1, row=5)


    #prograssbar - step15
    frame6 = tk.LabelFrame(tab2, text='step15')
    frame6.grid(column=0, row=0)
    runbutton = tk.Button(frame6, text='Run Progressbar', command=run_progressbar).grid(column=0, row=0, sticky='w')
    startbutton = tk.Button(frame6, text='Start Progressbar', command=start_progressbar).grid(column=0, row=1, sticky='w')
    stopbutton = tk.Button(frame6, text='Stop Progressbar', command=stop_progressbar).grid(column=0, row=2, sticky='w')
    sapbutton = tk.Button(frame6, text='Stop after second', command=progressbar_stop_after).grid(column=0, row=3, sticky='w')

    global progress_bar
    progress_bar = ttk.Progressbar(tab2, orient='horizontal', length=286, mode='determinate')
    progress_bar.grid(column=0, row=1, pady=2)


    #file upload, download - step16
    mngFileFrame = tk.LabelFrame(tab2, text=' Manage Files: ')
    mngFileFrame.grid(column=0, row=2, sticky='WE', padx=10, pady=5)

    lb = tk.Button(mngFileFrame, text='Browse to File...', command=getFileName)
    lb.grid(column=0, row=0, sticky=tk.W)

    filename = tk.StringVar()
    entryLen = 40
    global fileEntry
    fileEntry = tk.Entry(mngFileFrame, width=entryLen, textvariable=filename)
    fileEntry.grid(column=1, row=0, sticky=tk.W)

    logDir = tk.StringVar()
    global netwEntry
    netwEntry = tk.Entry(mngFileFrame, width=entryLen, textvariable=logDir)
    netwEntry.grid(column=1, row=1, sticky=tk.W)

    cb = tk.Button(mngFileFrame, text='Copy File To : ', command=copyFile)
    cb.grid(column=0, row=1, sticky=tk.E)

    
    #string find - step17
    global stringfind, teststrings, stringtext
    stringfind = tk.StringVar()
    findentry = tk.Entry(tab3, width=20, textvariable=stringfind).grid(column=0, row=0)

    stringbutton = tk.Button(tab3, text='Find', command=findstring).place(x=400, y=0)

    link = 'http://portal.woosuk.ac.kr'
    try:
        teststrings = 'link = http://portal.woosuk.ac.kr\n'+urlopen(link).read().decode()
    except Exception as ex:
        print(ex)
        messagebox.showerror('step3_2', '인터넷에 연결돼있지 않습니다.')
    stringtext = scrolledtext.ScrolledText(tab3, width=80, height=25, wrap=tk.WORD)
    stringtext.grid(column=0, row=1)
    stringtext.insert(tk.INSERT, teststrings)


    #use mysql - step18
    global connecthost, username, password, connectdb, mysqltext
    connecthost = tk.StringVar()
    username = tk.StringVar()
    password = tk.StringVar()
    connectdb = tk.StringVar()

    tk.Label(tab4, text="host ip : ").grid(column=0, row=0, padx=10, pady=5, sticky=tk.W)
    tk.Label(tab4, text="username : ").grid(column=0, row=1, padx=10, pady=5, sticky=tk.W)
    tk.Label(tab4, text="password : ").grid(column=0, row=2, padx=10, pady=5, sticky=tk.W)
    tk.Label(tab4, text="db name : ").grid(column=0, row=3, padx=10, pady=5, sticky=tk.W)

    connecthost_entry = tk.Entry(tab4, width=20, textvariable=connecthost).grid(column=1,row=0)
    username_entry = tk.Entry(tab4, width=20, textvariable=username).grid(column=1,row=1)
    password_entry = tk.Entry(tab4, width=20, textvariable=password).grid(column=1,row=2)
    connectdb_entry = tk.Entry(tab4, width=20, textvariable=connectdb).grid(column=1,row=3)

    mysqlogin = tk.Button(tab4, text='logintest', command=logintest).grid(column=1,row=4, pady=10)

    mysqltext = scrolledtext.ScrolledText(tab4, width=70, height=12, wrap=tk.WORD)
    mysqltext.grid(column=1,row=5)

    #프로그램 종료 방지
    win.mainloop()

#콜백 함수
def _quit():
    win.quit()
    win.destroy()
    exit()

def _about():
    messagebox.showinfo('!!','info\n우석대학교 정보보안학과 120191099 임태희')
    

def _button():
    messagebox.showinfo('step5_1','step5_2')

def radCall():
    radSel = radVar.get()
    if radSel == 1: print("red!!")
    elif radSel == 2: print("blue!!")
    elif radSel == 3: print("green!!")

def run_progressbar():
    progress_bar["maximum"] = 100
    for i in range(101):
        time.sleep(0.05)
        progress_bar["value"] = i
        progress_bar.update()
    progress_bar["value"] = 0

def start_progressbar():
    pass

def stop_progressbar():
    progress_bar.stop()

def progressbar_stop_after(wait_ms=1000):
    pass

def getFileName():
    print('hello from getFileName')
    global fDir, fName
    fDir = path.dirname(__file__)
    fName = fd.askopenfilename(parent=win, initialdir=fDir)
    fileEntry.insert(0, fName)
    netwEntry.insert(0, fDir)
    

def copyFile():
    src = fileEntry.get()
    file = src.split('/')[-1]
    dst = netwEntry.get() + '\_'+file

    print(src)
    print(file)
    print(dst)
    try:
        shutil.copy(src,dst)
        messagebox.showinfo('Copy File to Network', 'success:File copied.')

    except FileNotFoundError as err:
        messagebox.showerror('Copy File to Network', '*** Failed to copy file! ***\n\n'+str(err))

    except Exception as ex:
        messagebox.showerror('Copy File to Network', '*** Failed to copy file! ***\n\n'+str(ex))

def findstring():
    stringtext.tag_delete("highlight")
    
    if teststrings.find(stringfind.get()) == -1:
        messagebox.showerror("can't find", "nope")

    start = 1.0
    while 1:
        pos = stringtext.search(stringfind.get(), start, "end")
        if not pos:
            break
        end = f"{pos}+{len(stringfind.get())}c"
        stringtext.tag_add("highlight", pos, end)
        start = end
    
    stringtext.tag_config("highlight", background="yellow", foreground="red")
        
def logintest():
    '''connecthost.get()
    username.get()
    password.get()
    connectdb.get()'''

    try:
        conn = pymysql.connect(host=connecthost.get(), user=username.get(), password=password.get(), db=connectdb.get(), charset='utf8')
        cur = conn.cursor()
        cur.execute("show processlist")
        mysqltext.insert(tk.INSERT, cur.fetchall())
    except Exception as ex:
        print(ex)

if __name__ == '__main__':  
    layout()
