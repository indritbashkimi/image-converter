from tkinter import*
from tkinter import ttk
import tkinter.filedialog
from threading import Thread
from encoder import Encoder
from options_window import OptionsWindow
import settings
import utils
import os


class MainWindow(object):

    def __init__(self):
        self.filelist = list()
        self.settings = settings.settings
        self.running = False
        self.aborted = False
        self.encoder = None
        
        self.font = 'Ubuntu'
        self.filepattern = settings.filepattern
        
        self.master = Tk()
        self.master.protocol('WM_DELETE_WINDOW', self.destroy)
        self.change_output = BooleanVar()
        self.create_window()

    def create_window(self):

        def on_change_destination_clicked(event):
            if self.change_output.get():
                dir = tkinter.filedialog.askdirectory(title='Dove vuoi salvere le immagini')+'/'
                if dir:
                    self.destination_entry.configure(state = 'normal')
                    self.destination_entry.delete(0,END)
                    self.destination_entry.insert(0, dir)
                    self.destination_entry.configure(state = 'disabled')

        def on_check_changed():
            if self.change_output.get():
                self.change_destination.configure(state='normal')
            else:
                self.change_destination.configure(state='disabled')

        def about():
            about_master = tkinter.Toplevel(self.master)
            txt = "WebP Converter permette di convertire file .jpg o .png"+\
                " in .webp.\nPermette anche di convertire file .webp in"+\
                " .png\nPer ulteriori informazioni, potete consultare "+\
                "la self.master.mainloop()pagina ufficiale di Webp."
            msg = tkinter.Message(about_master, text=txt, bg="white", fg="black", aspect=300)
            msg.grid()
            ttk.Button(about_master, text='Chiudi', command=about_master.destroy).grid(sticky='E',padx=5,pady=5)
            about_master.transient(self.master)

        def open_options_window(event):
            OptionsWindow(self.master, self.settings)

        font = self.font

        ttk.Style().configure("TButton", background='gray50', foreground='white',font=(font,11))
        ttk.Style().configure("TLabel", font=(font,11))

        self.master.resizable(False, False)
        self.master.title('Webp ConverteR')
        self.frame = ttk.Frame(self.master, style='TFrame')

        title = Label(self.frame, text='Webp ConverteR', bg='#fd4949', font=(font, 26, 'bold'))
        title.grid(row=0, column=0, columnspan='4', sticky='we')

        self.addfile_button = ttk.Button(self.frame,text='Aggiungi file')
        self.addfile_button.bind("<ButtonRelease-1>", self.askfile)
        self.addfile_button.grid(row=1, column=0,padx=15, pady=10, sticky='we')
        self.addfolder_button = ttk.Button(self.frame,text='Aggiungi cartella')
        self.addfolder_button.bind("<ButtonRelease-1>", self.askdir)
        self.addfolder_button.grid(row=1,column=1,padx=15,pady=10,sticky='we')
        self.remove_button = ttk.Button(self.frame, text='Rimuovi')
        self.remove_button.bind("<ButtonRelease-1>", self.remove_file)
        self.remove_button.grid(row=1,column=3,padx=15,pady=10,sticky='we')

        ttk.Label(self.frame,text='Sorgente',style='TLabel').grid(row=2,column=0,columnspan='4',sticky='w',padx='10',pady='5')

        self.scrollbar = Scrollbar(self.frame, orient="vertical")
        self.listbox = Listbox(self.frame, selectmode=EXTENDED,
                               yscrollcommand = self.scrollbar.set, height=12)
        self.listbox.config(yscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command = self.listbox.yview)
        self.scrollbar.grid(row=3, column=4, sticky=N+S)
        self.listbox.grid(row=3,column=0,columnspan=4,padx=10,pady=5,sticky='we')

        self.options_button = ttk.Button(self.frame, text='Opzioni', style='TButton')
        self.options_button.bind("<ButtonRelease-1>", open_options_window)
        self.options_button.grid(row=4,column=3,padx=10,pady=5)

        ttk.Label(self.frame, text='Destinazione',font=(font,11), style='TLabel').grid(row=5,column=0,columnspan=4,sticky='w',padx=10,pady=5)
        self.check = Checkbutton(self.frame, text='Salva nella cartella:', 
                                 variable = self.change_output,
                                 onvalue = True, offvalue = False,
                                 command = on_check_changed)
        self.check.grid(row=6, column=0, sticky='W', padx=10)
        self.change_destination = ttk.Button(self.frame, text='Cambia')
        self.change_destination.bind("<ButtonRelease-1>", on_change_destination_clicked)
        self.change_destination.grid(row=6, column=1, sticky='WE', padx=10)
        self.change_destination.configure(state = 'disabled')

        self.destination_entry = Entry(self.frame)
        self.destination_entry.configure(state = 'disabled')
        self.destination_entry.grid(row=6,column=2,columnspan=2,sticky='we',padx=10)
        self.infolabel = ttk.Label(self.frame,text='0 file da convertire', style='TLabel')
        self.infolabel.grid(row=7, column=0, sticky='W', columnspan=2, padx=10, pady=10)
        self.progresslabel = ttk.Label(self.frame,text='0 %', style='TLabel')
        self.progresslabel.grid(row=7, column=2, sticky='W', columnspan=2, padx=10, pady=10)
        self.progressbar = ttk.Progressbar(self.frame, mode='determinate', value=0, maximum=100)
        self.progressbar.grid(row=8, column=0, sticky='WE', columnspan=4, padx=10, pady=5)
        self.about = ttk.Button(self.frame,text='Informazioni',command=about)
        self.about.grid(row=9,column=0,sticky='W',padx=10,pady=15)
        self.run_button = ttk.Button(self.frame,text='Start')
        self.run_button.bind('<ButtonRelease-1>', self.run)
        self.run_button.grid(row=9, column=3, sticky='e', padx=10 ,pady=15)

        self.frame.grid(row=0, column=0)
        self.master.mainloop()

    ''' overwrite the default exit method. chiude i thread prima di uscire. '''
    def destroy(self):
        ''' To be implemented '''
        self.master.destroy()

    def popup(self, txt, errors=None):
        info = tkinter.Toplevel(self.master)
        if errors:
            txt += "I seguenti file hanno generato un'errore:\n"
            for error in errors:
                txt += error+'\n'
        msg = tkinter.Message(info, text=txt, bg="#ff6666", fg="white", aspect=1000)
        msg.grid()
        ttk.Button(info, text='Chiudi', command=info.destroy).grid(sticky='E',padx=5,pady=5)
        info.transient(self.master)

    def enable_window(self):
        self.run_button.configure(text='Start')
        self.addfile_button.configure(state = 'normal')
        self.addfolder_button.configure(state = 'normal')
        self.remove_button.configure(state = 'normal')
        self.listbox.configure(state = 'normal')
        self.options_button.configure(state='normal')
        self.check.configure(state = 'normal')
        self.change_destination.configure(state = 'normal')
        self.about.configure(state = 'normal')

    def disable_window(self):
        self.run_button.configure(text='Stop')
        self.addfile_button.configure(state = 'disabled')
        self.addfolder_button.configure(state = 'disabled')
        self.remove_button.configure(state = 'disabled')
        self.listbox.configure(state = 'disabled')
        self.options_button.configure(state='disabled')
        self.check.configure(state = 'disabled')
        self.change_destination.configure(state = 'disabled')
        self.destination_entry.configure(state = 'disabled')
        self.about.configure(state = 'disabled')

    def askfile(self, event):
        if self.running:
            return None
        filename = tkinter.filedialog.askopenfilename(
                                filetypes = self.filepattern,
                                title = 'Scegli il file da convertire')
        if filename:
            self.addfile(filename)
            self.update_info()

    def askdir(self, event):
        if self.running:
            return None
        dirname = tkinter.filedialog.askdirectory(title='Scegli la cartella con le immagini')
        dirname += '/'
        if dirname:
            for filename in os.listdir(dirname):
                self.addfile(dirname+filename)
            self.update_info()

    def addfile(self, filename):
        if utils.isconvertible(filename) and filename not in self.filelist:
            self.filelist.append(filename)
            self.listbox.insert(END, filename)

    def remove_file(self, event):
        t = self.listbox.curselection()
        while len(t) > 0:
            self.filelist.pop(int(t[0]))
            self.listbox.delete(t[0])
            t = self.listbox.curselection()
        self.update_info()

    def update_settings(self):
        if self.change_output.get() and self.destination_entry.get():
            self.settings['dir'] = self.destination_entry.get()+'/'
        else:
            self.settings['dir'] = ''

    def run(self, event):
        if self.running:
            ''' STOP '''
            self.encoder.abort()
            self.aborted = True
            # it is still working
        elif len(self.filelist) > 0:
            ''' START '''             
            self.running = True
            self.aborted = False
            self.disable_window()
            self.update_settings()
            self.encoder = Encoder(self.filelist, self.settings, self)
            self.encoder.start()
        else:
            ''' Nessun file aggiunto '''
            pass

    def update_progress(self, progress=0, index=0):
        self.progressbar.configure(value = progress)
        self.update_info(index)
        self.progresslabel.configure(text = str(progress) + " %.")

    def update_info(self, completed=0):
        self.infolabel.configure(text = str(len(self.filelist)-completed) + ' file da convertire.')

    def notify_finish(self, errors, new_filelist):
        txt = 'Conversione file completata'
        if len(errors):
            txt += '.\n'
        else:
            txt += ' con successo.\n'
        self.enable_window()
        self.listbox.delete(0, END)
        self.filelist = new_filelist
        self.update_progress(0)
        if self.aborted:
            txt = 'Conversione file interrotta.\n'
            for filename in self.filelist:
                self.listbox.insert(END, filename)
        self.running = False
        if errors or not self.aborted:
            self.popup(txt, errors)
