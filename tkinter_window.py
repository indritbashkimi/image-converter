from tkinter import*
from tkinter import ttk
import tkinter.filedialog
from encoder import Encode
from mylist import MyList
from threading import Lock
import utility
import os


settings = {
    'q':        85,     # default quality
    'dir':      '',     # output dir
    'qfile':    True,   # use the quality specified on the file name
    'replace':  True,   # replace existing files
    'pass':     0,      # <int> analysis pass number (1..10)
    'size':     0,      # target size (in bytes)
    'strong':   False,  # use strong filter instead of simple
    'af':       False,  # auto-adjust filter strength.
    'pre':      0,      # pre-processing filter
    'quiet':    True,   #

    'ppm':      False,  # save the raw RGB samples as color PPM
    'pgm':      False,  #
    'mt':       True    # use multithreading, only for dwebp (non usarlo)
}


class TkinterWindow(object):

    def __init__(self):
        self.filelist = MyList()
        self.working = False
        self.encoding_thread = None
        self.lock = Lock()
        self.settings = settings
        self.master = Tk()
        self.create_window()

    def create_window(self):

        def on_addfile_clicked(event):
            if self.working:
                return None
            filename = tkinter.filedialog.askopenfilename(
                                    filetypes = self.filepattern,
                                    title = 'Scegli il file da convertire')
            if filename:
                self.add_file(filename)

        def on_addfolder_clicked(event):
            if self.working:
                return None
            dirname = tkinter.filedialog.askdirectory(title='Scegli la cartella con le immagini')
            if dirname:
                self.add_dir(dirname)

        def on_remove_clicked(event):
            if not self.working:
                t = self.listbox.curselection()
                while len(t) > 0:
                    self.filelist.remove(int(t[0]))
                    self.remove_file_from_window(t[0])
                    t = self.listbox.curselection()
            else:
                pass

        def on_options_clicked(event):
            if not self.working:
                print('Options window. It does nothing yet.')

        def on_change_destination_clicked(event):
            if not self.working and self.__change_output.get():
                self.destination_text.configure(state = 'normal')
                self.destination_text.delete(1.0, END)
                self.destination_text.insert(INSERT, tkinter.filedialog.askdirectory(
                                        title='Dove vuoi salvere le immagini'))
                self.destination_text.configure(state = 'disabled')
            else:
                pass

        def on_check_changed():
            if self.__change_output:
                self.change_destination.configure(state='normal')
            else:
                self.change_destination.configure(state='disabled')

        def on_quit_clicked(ev):
            if not self.working:
                self.master.destroy()

        def about():
            if self.working:
                return None
            info = tkinter.Toplevel(self.master)
            txt = "WebP Converter permette di convertire file .jpg o .png"+\
                " in .webp.\nPermette anche di convertire file .webp in"+\
                " .png\nPer ulteriori informazioni, potete consultare "+\
                "la self.master.mainloop()pagina ufficiale di Webp."
            msg = tkinter.Message(info, text=txt, bg="white", fg="black", aspect=300)
            msg.grid()
            info.transient(self.master)


        self.font = font = 'Ubuntu'
        self.filepattern = ((('All files'),'*.*'),
                            ('JPEG','*.jpg;*.jpeg'),
                            ('PNG','*.png'),
                            ('WEBP','*.webp'))

        self.master.title('Webp ConverteR')

        ttk.Style().configure("TButton", background='gray50', foreground='white', font=(font,11))
        ttk.Style().configure("TLabel", font=(font,11))

        self.f1 = Frame(self.master)
        self.f2 = Frame(self.master)
        self.f3 = Frame(self.master)

        # Radiobutton variable:
        self.__change_output = IntVar()

        title = Label(self.f1, text='                 WebP ConverteR                 ', bg='#FF6000', font=(font, 26, 'bold'))
        title.grid(row=0, column=0, columnspan='3', sticky='we')

        self.addfile_button = ttk.Button(self.f1,text='Aggiungi file')
        self.addfile_button.bind("<ButtonRelease-1>", on_addfile_clicked)
        self.addfile_button.grid(row=1, column=0, padx=15, pady=10, sticky='we')

        self.addfolder_button = ttk.Button(self.f1, text='Aggiungi cartella')
        self.addfolder_button.bind("<ButtonRelease-1>", on_addfolder_clicked)
        self.addfolder_button.grid(row=1, column=1, padx=15, pady=10, sticky='we')

        self.remove_button = ttk.Button(self.f1, text='Rimuovi')
        self.remove_button.bind("<ButtonRelease-1>", on_remove_clicked)
        self.remove_button.grid(row=1,column=2,padx=15, pady=10, sticky='we')

        ttk.Label(self.f2, text='Sorgente', style='TLabel').grid(row=2, column=0, columnspan='3',sticky='w',padx='10',pady='5')

        self.scrollbar = Scrollbar(self.f2, orient="vertical")
        self.listbox = Listbox(self.f2, selectmode=EXTENDED,
                               yscrollcommand = self.scrollbar.set,
                               width=64, height=10)
        # attach scrollbar to listbox
        self.listbox.config(yscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command = self.listbox.yview)
        self.scrollbar.grid(row=3, column=3, sticky=N+S)
        self.listbox.grid(row=3,column=0,columnspan=3,padx=10,pady=5,sticky='we')

        '''
        self.options_button = ttk.Button(self.f2,text='Opzioni')
        self.options_button.bind("<ButtonRelease-1>", on_options_clicked)
        self.options_button.grid(row=5,column=2,padx=10,pady=5, sticky='we')
        '''

        Label(self.f3, text='Destinazione',font=(font,11)).grid(row=0,column=0,sticky='w',padx=10,pady=5)

        self.check = Checkbutton(self.f3, text='Salva nella cartella:', 
                                 variable = self.__change_output,
                                 onvalue = 1, offvalue = 0,
                                 command = on_check_changed)
        self.check.grid(row=2, column=0, sticky='W', padx=10)

        self.change_destination = ttk.Button(self.f3, text='Cambia')
        self.change_destination.bind("<ButtonRelease-1>", on_change_destination_clicked)
        self.change_destination.grid(row=2, column=1, sticky='WE', padx=10)
        self.change_destination.configure(state = 'disabled')

        self.destination_text = Text(self.f3, width=34,height=1)
        # must be always disabled
        self.destination_text.configure(state = 'disabled')
        self.destination_text.grid(row=2,column=2,sticky='we',padx=10)

        self.infolabel = ttk.Label(self.f3,text='0 file da convertire', style='TLabel')
        self.infolabel.grid(row=4, column=0, sticky='W', columnspan=2, padx=10, pady=10)

        self.progresslabel = ttk.Label(self.f3,text='0 %', style='TLabel')
        self.progresslabel.grid(row=4, column=2, sticky='W', columnspan=1, padx=10, pady=10)
        self.progressbar = ttk.Progressbar(self.f3, mode='determinate', value=0, maximum=100)
        self.progressbar.grid(row=5, column=0, sticky='WE', columnspan=3, padx=10, pady=5)
        self.start_button = ttk.Button(self.f3,text='Start')
        self.start_button.bind('<ButtonRelease-1>', self.action)
        self.start_button.grid(row=6, column=2, sticky='e', padx=10 ,pady=15)

        self.about = ttk.Button(self.f3,text='About',command=about)
        self.about.grid(row=6,column=0,sticky='W',padx=10,pady=15)

        self.quit = ttk.Button(self.f3, text='Chiudi')
        self.quit.bind('<ButtonRelease-1>', on_quit_clicked)
        self.quit.grid(row=6, column=1,sticky='we',padx=10,pady=15)

        self.f1.grid(row=0, column=0, sticky='we')
        self.f2.grid(row=2, column=0)
        self.f3.grid(row=4, column=0)

        self.master.mainloop()

    def popup(self, errors):
        info = tkinter.Toplevel(self.master)
        txt = "I seguenti file hanno generato un'errore:\n"
        for error in errors:
            txt += error+'\n'
        msg = tkinter.Message(info, text=txt, bg="#ff6666", fg="white", aspect=1000)
        msg.grid()
        info.transient(self.master)

    def enable_window(self):
        self.start_button.configure(text='Start')
        self.addfile_button.configure(state = 'normal')
        self.addfolder_button.configure(state = 'normal')
        self.remove_button.configure(state = 'normal')
        self.listbox.configure(state = 'normal')
        #self.options_button.configure(state = 'normal')
        self.r1.configure(state = 'normal')
        self.r2.configure(state = 'normal')
        self.change_destination.configure(state = 'normal')
        self.about.configure(state = 'normal')
        self.quit.configure(state = 'normal')

    def disable_window(self):
        self.start_button.configure(text='Stop')
        self.addfile_button.configure(state = 'disabled')
        self.addfolder_button.configure(state = 'disabled')
        self.remove_button.configure(state = 'disabled')
        self.listbox.configure(state = 'disabled')
        #self.options_button.configure(state = 'disabled')
        self.r1.configure(state = 'disabled')
        self.r2.configure(state = 'disabled')
        self.destination_text.configure(state = 'disabled')
        self.about.configure(state = 'disabled')
        self.quit.configure(state = 'disabled')

    def update_settings(self):
        if self.__change_output.get():
            self.settings['dir'] = self.destination_text.get(1.0, END).split('\n')[0] + '/'
        if not os.path.isdir(self.settings['dir']):
            self.settings['dir'] = ''
        print('dir:',self.settings['dir'])

    def add_file_to_window(self, filename):
        self.listbox.insert(END, filename)

    def remove_file_from_window(self, i):
        self.listbox.delete(i)

    def refresh_window(self):
        self.lock.acquire()
        self.clear_window()
        for filename in self.filelist:
            self.add_file_to_window(filename)
        self.lock.release()

    def clear_window(self):
        self.listbox.delete(0, END)

    def add_file(self, filename):
        if utility.isconvertible(filename) and self.filelist.add(filename):
            self.add_file_to_window(filename)
            self.update_info()
        else:
            pass

    def add_dir(self, dirname):
        for name in os.listdir(dirname):
            self.add_file(dirname+'/'+name)

    def remove_files(self, indices):
        self.filelist.remove_from_list(indices)
        self.update_info()

    def clear(self):
        self.clear_window()
        self.filelist.clear()

    def action(self, ev = None):
        # START pressed
        if not self.working:
            print('START')
            self.working = True
            self.disable_window()
            self.update_settings()
            self.encoding_thread = Encode(self.filelist, self.settings, self)
            self.encoding_thread.start()
        # STOP pressed
        else:
            print('STOP')
            self.encoding_thread.force_stop()

    def update_progress(self, progress):
        self.progressbar.configure(value = progress)
        self.update_info()
        self.progresslabel.configure(text = str(progress)+" %.")

    def update_info(self):
        self.infolabel.configure(text = str(len(self.filelist))+' file da convertire.')

    def notify_finish(self, errors):
        print('end')
        if len(errors):
            self.popup(errors)
        self.update_progress(0)
        self.enable_window()
        self.refresh_window()
        self.update_info()
        self.working = False
