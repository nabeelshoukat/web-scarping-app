from tkinter import *
from tkinter import filedialog
import requests
from bs4 import BeautifulSoup
import sqlite3
import os
from tkinter import ttk
from pathlib import Path
from tkinter import messagebox

# list for storing file path
filepath = []

root = Tk()
root.config(bg='yellow')
root.geometry(str(root.winfo_screenwidth()) + "x" + str(root.winfo_screenheight()))

with sqlite3.connect('SCDB.db') as db:
    cursor = db.cursor()
dirpath = os.path.join('C:/', 'web scraping')
if not dirpath:
    os.mkdir(dirpath)

# TABLE OF FILE PATH
cursor.execute("CREATE TABLE IF NOT EXISTS filepath(path TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS theme(bg TEXT , fg TEXT,font TEXT)")
db.commit()
# FETCHING RECORD FROM TABLE
rowcount = cursor.execute('SELECT COUNT(*) FROM filepath')
for i in rowcount:
    if i[0] == 0:
        query = (f"INSERT INTO filepath(path) VALUES (?)")
        cursor.execute(query, ([dirpath]))
        db.commit()

    else:
        pass

themecount = cursor.execute('SELECT COUNT(*) FROM theme')

for i in rowcount:
    if i[0] == 0:
        query = (f"INSERT INTO theme(bg,fg,font) VALUES (?,?,?)")
        cursor.execute(query, ('#e52165', '#3b4d61', 'Arial'))
        db.commit()
    else:
        x = cursor.execute("SELECT * FROM theme")
        for i in x:
            pass
    bgcol = str(i[0])
    fgcol = str(i[1])

    font = str(i[2])


class Scrap:
    def __init__(self):


        menubar = Menu(root)
        filemenu = Menu(menubar)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save_file)
        filemenu.add_command(label="Save as", command=self.save_as)
        filemenu.add_separator()

        # filemenu.add_command(label="Set Path", command=self.filepath)
        filemenu.add_command(label="Exit", command=root.quit)
        # settings
        settingsmenu = Menu(menubar)

        menubar.add_cascade(label="Settings", menu=settingsmenu)
        settingsmenu.add_command(label="Theme", command=self.theme)

        root.config(menu=menubar)
# creating a frame scrollable
        container = Frame(root)
        self.file_frame = LabelFrame(text='Files',  bg=bgcol, fg=fgcol, width=300,height=root.winfo_screenheight() - 200)
        self.file_frame.pack(side=LEFT, ipadx=100, ipady=root.winfo_screenheight())
        canvas = Canvas(self.file_frame)
        scrollbar = ttk.Scrollbar(self.file_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # scroll frame

        self.setting_frame = LabelFrame(bg=bgcol, width=300, height=root.winfo_screenheight() - 150)
        self.setting_frame.pack(side=RIGHT, ipadx=0, ipady=root.winfo_screenheight(), fill=X, expand=True)

        self.scrollframe = LabelFrame(bg=bgcol, width=20, height=root.winfo_screenheight() - 300)
        self.scrollframe.pack(side=RIGHT, ipadx=0, ipady=root.winfo_screenheight(), fill=X, expand=True)

        self.link_frame = LabelFrame(bg=bgcol, width=root.winfo_screenwidth(), height=100)
        self.link_frame.pack(side=TOP, ipadx=root.winfo_screenwidth() - 200, ipady=20)
        self.text_area = Text(root,wrap=WORD,font=("arial",13))
        self.text_area.pack(side=BOTTOM, ipadx=root.winfo_screenwidth() - 200, ipady=185)
        # create a Scrollbar and associate it with txt

        scrollbar = Scrollbar(self.scrollframe)
        scrollbar.pack(fill=Y,expand=True,side=RIGHT,)
        self.text_area.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text_area.yview)
        self.text_area.see(END)

        # scrollbar.config(undo=True, wrap='word')
        scrollbar.config(borderwidth=3, relief="sunken")

        style = ttk.Style()
        style.theme_use('clam')

        # self.gui_files()
        self.gui_link()
        self.gui_main_settings()

    def gui_files(self):

        self.min_btn = Button(self.scrollable_frame, text="_ minimize", font=(font, 15), bd=0, bg=bgcol, fg=fgcol,
                              command=self.destroy_fileframe)
        self.min_btn.grid(row=0, column=1)
        self.path_files()
        try:
            self.plusbtn.destroy()
        except:
            pass
    # def destroy_fileframe(self):
        for widget in self.file_frame.winfo_children():
            widget.destroy()
        self.file_frame.config(width=0)
        self.plusbtn=Button(self.file_frame,text='+ maximize',font=(font, 15), bd=0, bg=bgcol, fg=fgcol,command=self.gui_files)
        self.plusbtn.grid(row=0,column=1 )

        button=Button(self.file_frame,text="+",bg=bgcol,fg=fgcol,bd=0)
        button.pack(side=RIGHT,anchor=NW)





    def gui_link(self):
        self.link_label = Label(self.link_frame, text="Enter URL", font=(font, 15), bg=bgcol, fg=fgcol)
        self.link_label.grid(row=0, column=0, padx=100, pady=25)
        self.link_entery = Entry(self.link_frame, width=30, font=(font, 15))
        self.link_entery.grid(row=0, column=1)
        self.link_entery.focus()


    def gui_main_settings(self):
        self.h1var = IntVar()
        self.h2var = IntVar()
        self.h3var = IntVar()
        self.h4var = IntVar()
        self.h5var = IntVar()
        self.h6var = IntVar()
        headingLabel = Label(self.setting_frame, text="Headings", font=(font, 15, 'bold'), bg=bgcol, fg=fgcol)
        headingLabel.grid(row=0, column=0, pady=5, columnspan=2)
        self.h1label = Label(self.setting_frame, text='h1', font=(font, 12), bg=bgcol, fg=fgcol)
        self.h1label.grid(row=1, column=0, ipadx=5, ipady=5, rowspan=1)
        self.h1check = Checkbutton(self.setting_frame, onvalue=1, offvalue=0, variable=self.h1var, bg=bgcol)
        self.h1check.grid(row=1, column=1, padx=5, columnspan=1)
        self.h2label = Label(self.setting_frame, text='h2', font=(font, 12), bg=bgcol, fg=fgcol)
        self.h2label.grid(row=1, column=2, ipadx=5, ipady=5)
        self.h2check = Checkbutton(self.setting_frame, onvalue=1, offvalue=0, variable=self.h2var, bg=bgcol)
        self.h2check.grid(row=1, column=3, padx=5)
        self.h3label = Label(self.setting_frame, text='h3', font=(font, 12), bg=bgcol, fg=fgcol)
        self.h3label.grid(row=1, column=4, ipadx=5, ipady=5)
        self.h3check = Checkbutton(self.setting_frame, onvalue=1, offvalue=0, variable=self.h3var, bg=bgcol, )
        self.h3check.grid(row=1, column=5, padx=5)
        # 2nd row
        self.h4label = Label(self.setting_frame, text='h4', font=(font, 12), bg=bgcol, fg=fgcol)
        self.h4label.grid(row=2, column=0, ipadx=5, ipady=5, rowspan=1)
        self.h4check = Checkbutton(self.setting_frame, onvalue=1, offvalue=0, variable=self.h4var, bg=bgcol, )
        self.h4check.grid(row=2, column=1, padx=5)
        self.h5label = Label(self.setting_frame, text='h5', font=(font, 12), bg=bgcol, fg=fgcol)
        self.h5label.grid(row=2, column=2, ipadx=5, ipady=5)
        self.h5check = Checkbutton(self.setting_frame, onvalue=1, offvalue=0, variable=self.h5var, bg=bgcol)
        self.h5check.grid(row=2, column=3, padx=5)
        self.h6label = Label(self.setting_frame, text='h6', font=(font, 12), bg=bgcol, fg=fgcol)
        self.h6label.grid(row=2, column=4, ipadx=5, ipady=5)
        self.h6check = Checkbutton(self.setting_frame, onvalue=1, offvalue=0, variable=self.h6var, bg=bgcol, )
        self.h6check.grid(row=2, column=5, padx=5)
        # Title
        self.titlelabel1 = Label(self.setting_frame, text="Add Title", font=(font, 15, 'bold'), bg=bgcol, fg=fgcol)
        self.titlelabel1.grid(row=3, column=0, pady=10, padx=1, columnspan=2, rowspan=1)

        self.titlelabel2 = Label(self.setting_frame, text='title', font=(font, 12), bg=bgcol, fg=fgcol)
        self.titlelabel2.grid(row=4, column=0, ipadx=5, ipady=5)
        self.titlvar = IntVar()
        self.titlecheck = Checkbutton(self.setting_frame, onvalue=1, offvalue=0, variable=self.titlvar, bg=bgcol, )
        self.titlecheck.grid(row=4, column=1, padx=5)
        # paragraphs
        self.p1var = IntVar()
        self.p2var = IntVar()
        self.p3var = IntVar()
        self.p4var = IntVar()
        self.p5var = IntVar()
        self.p6var = IntVar()
        headingLabel = Label(self.setting_frame, text="Paragraphs", font=("arial", 15, 'bold'), bg=bgcol, fg=fgcol)
        headingLabel.grid(row=5, column=0, pady=10, columnspan=2)

        self.p1label = Label(self.setting_frame, text='p1', font=(font, 12), bg=bgcol, fg=fgcol)
        self.p1label.grid(row=6, column=0, ipadx=5, ipady=5, rowspan=1)
        self.p1check = Checkbutton(self.setting_frame, onvalue=1, offvalue=0, variable=self.p1var, bg=bgcol, )
        self.p1check.grid(row=6, column=1, padx=5, columnspan=1)
        self.p2label = Label(self.setting_frame, text='p2', font=(font, 12), bg=bgcol, fg=fgcol)
        self.p2label.grid(row=6, column=2, ipadx=5, ipady=5)
        self.p2check = Checkbutton(self.setting_frame, onvalue=1, offvalue=0, variable=self.p2var, bg=bgcol, )
        self.p2check.grid(row=6, column=3, padx=5)
        self.p3label = Label(self.setting_frame, text='p3', font=(font, 12), bg=bgcol, fg=fgcol)
        self.p3label.grid(row=6, column=4, ipadx=5, ipady=5)
        self.p3check = Checkbutton(self.setting_frame, onvalue=1, offvalue=0, variable=self.p3var, bg=bgcol, )
        self.p3check.grid(row=6, column=5, padx=5)
        # 2nd row
        self.p4label = Label(self.setting_frame, text='p4', font=(font, 12), bg=bgcol, fg=fgcol)
        self.p4label.grid(row=7, column=0, ipadx=5, ipady=5, rowspan=1)
        self.p4check = Checkbutton(self.setting_frame, onvalue=1, offvalue=0, variable=self.p4var, bg=bgcol, )
        self.p4check.grid(row=7, column=1, padx=5)
        self.p5label = Label(self.setting_frame, text='p5', font=(font, 12), bg=bgcol, fg=fgcol)
        self.p5label.grid(row=7, column=2, ipadx=5, ipady=5)
        self.p5check = Checkbutton(self.setting_frame, onvalue=1, offvalue=0, variable=self.p5var, bg=bgcol, )
        self.p5check.grid(row=7, column=3, padx=5)
        self.p6label = Label(self.setting_frame, text='p6', font=(font, 12), bg=bgcol, fg=fgcol)
        self.p6label.grid(row=7, column=4, ipadx=5, ipady=5)
        self.p6check = Checkbutton(self.setting_frame, onvalue=1, offvalue=0, variable=self.p6var, bg=bgcol, )
        self.p6check.grid(row=7, column=5, padx=5)
        # define the entery
        self.p6label = Label(self.setting_frame, text='Specific No:', font=(font, 12), width=10, bg=bgcol, fg=fgcol)
        self.p6label.grid(row=8, column=0, pady=5, padx=0, ipadx=5, columnspan=2)
        self.pera_entery = Entry(self.setting_frame, font=("arial", 13))
        self.pera_entery.grid(row=8, column=2, pady=5, columnspan=3)
        # select all peragraphs
        self.al_peras_var = IntVar()
        self.selectal_pera_label1 = Label(self.setting_frame, text='Select all Paras', font=(font, 12, 'bold'),
                                          bg=bgcol, fg=fgcol)
        self.selectal_pera_label1.grid(row=10, column=0, pady=10, padx=0, columnspan=2)
        self.selectal_pera_label2 = Label(self.setting_frame, text='Select', font=(font, 12,), width=10, bg=bgcol,
                                          fg=fgcol)
        self.selectal_pera_label2.grid(row=11, column=0, pady=10, padx=0, ipadx=5, columnspan=2)
        self.selectal_pera_check = Checkbutton(self.setting_frame, onvalue=1, offvalue=0, variable=self.al_peras_var,
                                               bg=bgcol, )
        self.selectal_pera_check.grid(row=11, column=2, padx=5)

        # select  everything
        self.whole_webdata = IntVar()
        self.everyt_label1 = Label(self.setting_frame, text='Select Everything(Text + HTMl...)',
                                   font=(font, 12, 'bold'), bg=bgcol, fg=fgcol)
        self.everyt_label1.grid(row=12, column=0, pady=10, padx=0, columnspan=4)
        self.everyt_label2 = Label(self.setting_frame, text='Select', font=(font, 12,), width=10, bg=bgcol, fg=fgcol)
        self.everyt_label2.grid(row=13, column=0, pady=10, padx=0, ipadx=5, columnspan=2)
        self.everyt_check = Checkbutton(self.setting_frame, onvalue=1, offvalue=0, variable=self.whole_webdata,
                                        bg=bgcol, )
        self.everyt_check.grid(row=13, column=2, padx=5)

        # all links in website
        self.links_var = IntVar()
        self.linklabel1 = Label(self.setting_frame, text='Select Links',
                                font=(font, 12, 'bold'), bg=bgcol, fg=fgcol)
        self.linklabel1.grid(row=14, column=0, pady=10, padx=0, columnspan=2)
        self.linklabel2 = Label(self.setting_frame, text='Select', font=(font, 12,), width=10, bg=bgcol, fg=fgcol)
        self.linklabel2.grid(row=15, column=0, pady=10, padx=0, ipadx=5, columnspan=2)
        self.link_check = Checkbutton(self.setting_frame, onvalue=1, offvalue=0, variable=self.links_var, bg=bgcol, )
        self.link_check.grid(row=15, column=2, padx=5)

        self.search_button1 = Button(self.setting_frame, text='search', font=(font, 12, 'bold'), bg='yellow', fg='red',
                                     command=self.check_values)
        self.search_button1.grid(row=16, column=3, columnspan=3, ipadx=15)

    def check_values(self):
        x = self.h1var.get()
        # print(x)
        weburl = self.link_entery.get()
        r = requests.get(weburl)
        htmlcontent = r.content
        # parsing the html
        sop = BeautifulSoup(htmlcontent, "html.parser")
        # for one para

        h1val = self.h1var.get()
        h2val = self.h2var.get()
        h3val = self.h3var.get()
        h4val = self.h4var.get()
        h5val = self.h5var.get()
        h6val = self.h6var.get()
        if h1val == 1:
            h1 = (sop.find('h1')).getText()
            self.text_area.insert('end', str("Heading 1\n" + h1 + "\n"))

        if h2val == 1:
            h2 = (sop.find('h2')).getText()
            self.text_area.insert('end', str("Heading 2\n" + h2 + "\n"))
        if h3val == 1:
            h3 = (sop.find('h3')).getText()
            self.text_area.insert('end', str("Heading 3\n" + h3 + "\n"))
        if h4val == 1:
            h4 = (sop.find('h4')).getText()
            self.text_area.insert('end', str("Heading 4\n" + h4 + "\n"))
        if h5val == 1:
            h5 = (sop.find('h5')).getText()
            self.text_area.insert('end', str("Heading 5\n" + h5 + "\n"))
        if h6val == 1:
            h6 = (sop.find('h6')).getText()
            self.text_area.insert('end', str("Heading 6\n" + h6 + "\n"))
        # inserting title
        title = self.titlvar.get()
        if title == 1:
            title_text = (sop.find('title')).getText()
            self.text_area.insert('end', str("Title\n" + title_text + "\n"))
        # inserting paragraphs
        p1val = self.p1var.get()
        p2val = self.p2var.get()
        p3val = self.p3var.get()
        p4val = self.p4var.get()
        p5val = self.p5var.get()
        p6val = self.p6var.get()
        if p1val == 1:
            p1 = (sop.find_all('p')[0]).get_text()
            self.text_area.insert('end', str("paragraph 1\n" + p1 + "\n"))
        if p2val == 1:
            p2 = (sop.find_all('p')[1]).get_text()
            self.text_area.insert('end', str("paragraph 2\n" + p2 + "\n"))
        if p3val == 1:
            p3 = (sop.find_all('p')[2]).get_text()
            self.text_area.insert('end', str("paragraph 3\n" + p3 + "\n"))
        if p4val == 1:
            p4 = (sop.find_all('p')[3]).get_text()
            self.text_area.insert('end', str("paragraph 4\n" + p4 + "\n"))
        if p5val == 1:
            p5 = (sop.find_all('p')[4]).get_text()
            self.text_area.insert('end', str("paragraph 5\n" + p5 + "\n"))
        if p6val == 1:
            p6 = (sop.find_all('p')[5]).get_text()
            self.text_area.insert('end', str("paragraph 6\n" + p6 + "\n"))

        # for all paras
        if self.al_peras_var.get() == 1:
            all_peras = sop.find_all('p')
            #
            for parse in all_peras:
                wholedata = ("{}{}".format(parse.text, parse.find_next_sibling(text=True)))

                self.text_area.insert('end', str("\nAll Peragrphs\n\n\n" + wholedata))

        if self.whole_webdata.get() == 1:
            # print('i am access')
            complte_web = sop.find_all()
            self.text_area.insert('end', str("\nAll Complete WebSite with Code\n\n\n" + str(complte_web)))

        if self.links_var.get() == 1:
            link_list_1 = []

            for link in sop.find_all('a'):
                link_list_1.append(link.get('href'))
            for i, j in enumerate(link_list_1):
                self.text_area.insert('end', str(f"\n\nLink {i}:\n" + str(j)))

    def open_file(self):
        # this section is used to read a file

        file_path = filedialog.askopenfilename(title="Select A File", )
        # file_path = "C:/web scraping"
        with open(f"{file_path}", "r") as file:
            print(file.readlines())
            # self.text_area.insert('end',file.read())

    def save_file(self):

        files_types = [
            ('Text Document', '*.txt'), ('Word Document', '*.docx'), ('Python File', '*.py'), ('All Files', '*.*')]
        file_path = filedialog.asksaveasfilename(title='Save File', filetypes=files_types, defaultextension=".txt")
        with open(file_path, 'w') as file:
            file.write(self.text_area.get('1.0', END))

    def save_as(self):
        f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return
        text2save = str(self.text_area.get(1.0, END))  # starts from `1.0`, not `0.0`
        f.write(text2save)
        f.close()

    def path_files(self):
        file = cursor.execute("SELECT * FROM filepath")

        for i in file:
            filepath.append(i[0])

        y = os.listdir(filepath[0])
        for i, j in enumerate(y):
            try:
                button = Button(self.file_frame, text=str(j), font=('arial', 12), bd=0,
                        command=lambda x=j: self.file_function(x))

                button.grid(row=i + 1, column=0, sticky=EW, pady=2)
                self.file_frame.grid_columnconfigure(0, weight=1)
            except:
                pass
    def file_function(self, filename):

        data =self.text_area.get('1.0',END)
        if len(data.strip())>=1:
            x=messagebox.askyesnocancel('Alert?',"Do you want to save your file?")
            if x==1:
                self.save_file()
            elif x==0:
                self.text_area.delete('1.0',END)
                with open(f"{filepath[0]}/{filename}", 'r') as file:
                    self.text_area.delete('1.0', END)
                    self.text_area.insert('end', file.read())
            else:
                pass

        if len(data.strip())==0:
            with open(f"{filepath[0]}/{filename}", 'r') as file:
                self.text_area.delete('1.0', END)
                self.text_area.insert('end', file.read())


    def get_key(self, val):
        for key, value in self.colors_dictionary.items():
            if val == value:
                return key


    def theme(self):
        self.colors_dictionary = {'Pink': '#e52165', 'raisin': "#0d1137", "Red": "#d72631", "sea-foam": "#a2d5c6",
                                  "jade": "#077b8a", 'violet': "#5c3c92", "Yellow": "#e2d810", "magenta": "#d9138a",
                                  "cyan": "#12a4d9", 'Black':"#322e2f","Mustard": "#f3ca20"
            , "goldenrod": "#e8d21d", "turquoise": "#039fbe", "brick": "#b20238", "Gold": "#ef9d10f", }

        fonts = ['Agency Fb', "Algerian Regular", "Arial", "Arial Rounded Bold", "Bauhas 93 Regular", "Bell MT",
                 "OPEN SANS", "ALTERNATE GOTHIC", "TISA"]
        bgfgcolor = [i for i in self.colors_dictionary.keys()]

        self.root1 = Toplevel(root)
        self.color_frame = Frame(self.root1)

        self.color_frame.grid(row=0, column=0, ipadx=100, ipady=300)
        self.root1.grab_set()

        # background color

        self.bgcollabel = Label(self.color_frame, text='Select a background color  ', font=("arial", 15))
        self.bgcollabel.grid(row=0, column=0, padx=10, pady=5)
        self.value = StringVar()

        bgoptoins = bgfgcolor

        self.bg_optmenu = ttk.Combobox(self.color_frame, values=bgoptoins)
        y = self.get_key(bgcol)
        self.bg_optmenu.set(y)
        self.bg_optmenu.grid(row=0, column=1)

        # foreground color
        self.fgcollabel = Label(self.color_frame, text='Select a foreground color  ', font=("arial", 15))
        self.fgcollabel.grid(row=0, column=2, padx=10, pady=5)
        self.value = StringVar()
        fgoptoins = bgfgcolor
        self.fg_optmenu = ttk.Combobox(self.color_frame, values=fgoptoins)

        x = (fgcol)

        self.bg_optmenu.set(x)
        self.bg_optmenu.grid(row=0, column=3)

        # font
        self.fontcollabel = Label(self.color_frame, text='Select a Font   ', font=("arial", 15))
        self.fontcollabel.grid(row=0, column=4, padx=10, pady=5)
        self.fontvalue = StringVar()
        fontoptoins = fonts
        self.font_optmenu = ttk.Combobox(self.color_frame, values=fontoptoins)
        self.font_optmenu.grid(row=0, column=5)
        self.font_optmenu.set(font)
        self.applybtn = Button(self.color_frame, text="Apply", bd=2, bg='purple', command=self.change_theme)
        self.applybtn.grid(row=0, column=6, padx=15)

    def change_theme(self):

        bgcolr = self.bg_optmenu.get()
        fgcolor = self.fg_optmenu.get()
        fonts = self.font_optmenu.get()

        background = self.colors_dictionary.get(str(bgcolr))
        foreground = self.colors_dictionary.get(str(fgcolor))

        # foreground=(self.colors_dictionary.get(str(fgcolor)))

        # print(background)
        # fnt=(self.colors_dictionary[f'{fonts}'])
        query = "UPDATE theme SET bg=?,fg=?,font=?"
        cursor.execute(query, (background, foreground, fonts))
        db.commit()
        # Scrap()


obj = Scrap()
root.mainloop()
