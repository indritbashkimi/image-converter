from tkinter import*
from tkinter import ttk


class OptionsWindow(object):

    def __init__(self, master, settings):
        ttk.Style().configure("TButton", background='gray50', foreground='white',font=('Ubuntu',11))
        self.master = Toplevel(master)
        self.master.resizable(False, False)
        self.master.title('Opzioni')
        self.settings = settings
        self.quality = IntVar()
        self.qfile = BooleanVar()

        Label(self.master, text='Qualità predefinita:').grid(row=0,column=0,sticky='W',padx=10,pady=5)
        self.scale = Scale(self.master,orient='horizontal',resolution='1',length=100,from_=1,to=100, variable=self.quality)
        self.scale.set(self.settings['quality'])
        self.scale.grid(row=0,column=1,sticky='WE',padx=10,pady=5)
        check_qfile = Checkbutton(self.master, text='Usa la qualità specificata nel nome del file (filename[q85].jpg):', 
                                 variable = self.qfile,
                                 onvalue = True, offvalue = False)
        check_qfile.select()
        check_qfile.grid(row=1, column=0, columnspan=2,sticky='W',padx=10,pady=5)
        Label(self.master, text='Dimensione (bytes):').grid(row=4,column=0,padx=10,pady=5,sticky='W')
        self.size_entry = Entry(self.master)
        self.size_entry.insert(0, self.settings['size'])
        self.size_entry.grid(row=4,column=1,padx=10,pady=5,sticky='WE')
        Label(self.master, text='Passi (calcolo dimensione):').grid(row=5,column=0,sticky='W',padx=10,pady=5)
        self.pass_entry = Entry(self.master)
        self.pass_entry.insert(0, str(self.settings['pass']))
        self.pass_entry.grid(row=5, column=1, sticky='WE',padx=10,pady=5)
        cancel_button = ttk.Button(self.master, text='Annulla', style='TButton')
        cancel_button.bind("<ButtonRelease-1>", self.exit)
        cancel_button.grid(row=15, column=0, padx=10, pady=10, sticky='W')
        save_button= ttk.Button(self.master, text='Salva', style='TButton')
        save_button.bind("<ButtonRelease-1>", self.save)
        save_button.grid(row=15, column=1, padx=10, pady=10, sticky='E')

        self.master.transient(master)

    def exit(self, event=None):
        self.master.destroy()

    def save(self, event):
        self.settings['quality'] = self.quality.get()
        self.settings['qfile'] = self.qfile.get()
        try:
            self.settings['size'] = int(self.size_entry.get())
        except:
            pass
        try:
            self.settings['pass'] = int(self.pass_entry.get())
        except:
            pass
        self.exit()