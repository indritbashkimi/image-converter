from tkinter import*
from tkinter import ttk


class OptionsWindow(object):

    def __init__(self, master, settings):
        ttk.Style().configure("TButton")
        self.master = Toplevel(master)
        self.master.resizable(False, False)
        self.master.title('Opzioni')
        self.settings = settings
        self.quality = IntVar()
        self.qfile = BooleanVar()
        self.replace = BooleanVar()
        self.passes = StringVar()

        Label(self.master, text='Default quality:').grid(row=0, column=0, sticky='W', padx=10, pady=5)
        self.scale = Scale(self.master, orient='horizontal',
                                        resolution='1',
                                        length=100,
                                        from_=1, to=100,
                                        variable=self.quality)
        self.scale.set(self.settings['quality'])
        self.scale.grid(row=0, column=1, sticky='WE', padx=10, pady=5)
        check_qfile = Checkbutton(self.master, text='Use the quality specified in the filename (filename[q85].jpg):', 
                                               variable = self.qfile,
                                               onvalue = True, offvalue = False)
        check_qfile.select()
        check_qfile.grid(row=1, column=0, columnspan=2, sticky='W', padx=10, pady=5)

        Label(self.master, text='Size (bytes):').grid(row=4, column=0, padx=10, pady=5, sticky='W')
        self.size_entry = Entry(self.master)
        size_text = self.settings['size']
        if size_text == 0:
            size_text = 'default'
        self.size_entry.insert(0, size_text)
        self.size_entry.grid(row=4, column=1, padx=10, pady=5, sticky='WE')
        Label(self.master, text='Passes (calculate size):').grid(row=5, column=0, sticky='W', padx=10, pady=5)
        pass_combobox = ttk.Combobox(self.master, textvariable=self.passes, state='readonly')
        pass_combobox['values'] = (1,2,3,4,5,6,7,8,9,10)
        pass_combobox.current(settings['pass']-1)
        pass_combobox.grid(row=5, column=1, sticky='WE', padx=10, pady=5)

        check_replace = Checkbutton(self.master,text='Replace existing files?', 
                                                variable = self.replace,
                                                onvalue = True,
                                                offvalue = False)
        if self.settings['replace']:
            check_replace.select()
        check_replace.grid(row=6, column=0, sticky='W',columnspan=2,padx=10,pady=5)

        cancel_button = ttk.Button(self.master, text='Annulla')
        cancel_button.bind("<ButtonRelease-1>", self.exit)
        cancel_button.grid(row=15, column=0, padx=10, pady=10, sticky='W')
        save_button= ttk.Button(self.master, text='Salva')
        save_button.bind("<ButtonRelease-1>", self.save)
        save_button.grid(row=15, column=1, padx=10, pady=10, sticky='E')

        self.master.transient(master)

    def exit(self, event=None):
        self.master.destroy()

    def save(self, event):
        self.settings['replace'] = self.replace.get()
        self.settings['quality'] = self.quality.get()
        self.settings['qfile'] = self.qfile.get()
        try:
            self.settings['size'] = int(self.size_entry.get())
        except:
            pass
        self.settings['pass'] = int(self.passes.get())
        # debug
        print('settings updated:')
        print('\tquality:\t',self.settings['quality'])
        print('\tsize:\t\t',self.settings['size'])
        print('\tpass:\t\t',self.settings['pass'])
        print('\treplace:\t',bool(self.settings['replace']))
        self.exit()
