from tkinter import*
from tkinter import ttk
import tkinter.filedialog
from threading import Thread
from encoder import Encoder
import settings
import utils
import os


class TkinterWindow(object):

    def __init__(self):
        self.filelist = list()
        self.settings = settings.settings
        self.running = False
        self.aborted = False
        self.encoder = None
        self.master = Tk()
        self.create_window()

    def create_window(self):

        def on_change_destination_clicked(event):
            if not self.running and self.__change_output.get():
                self.destination_text.configure(state = 'normal')
                self.destination_text.delete(1.0, END)
                self.destination_text.insert(INSERT, tkinter.filedialog.askdirectory(
                                        title='Dove vuoi salvere le immagini'))
                self.destination_text.configure(state = 'disabled')

        def on_check_changed():
            if self.__change_output:
                self.change_destination.configure(state='normal')
            else:
                self.change_destination.configure(state='disabled')

        def on_quit_clicked(ev):
            if not self.running:
                self.master.destroy()

        def about():
            if self.running:
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
        self.filepattern = settings.filepattern

        self.master.title('Webp ConverteR')

        ttk.Style().configure("TButton", background='gray50', foreground='white',font=(font,11))
        ttk.Style().configure("TLabel", font=(font,11))

        self.f1 = Frame(self.master)
        self.f2 = Frame(self.master)
        self.f3 = Frame(self.master)

        # Radiobutton variable:
        self.__change_output = IntVar()

        title = Label(self.f1, text='                 WebP ConverteR                 ', bg='#fd4949', font=(font, 26, 'bold'))
        title.grid(row=0, column=0, columnspan='3', sticky='we')

        self.addfile_button = ttk.Button(self.f1,text='Aggiungi file')
        self.addfile_button.bind("<ButtonRelease-1>", self.askfile)
        self.addfile_button.grid(row=1, column=0, padx=15, pady=10, sticky='we')
        self.addfolder_button = ttk.Button(self.f1, text='Aggiungi cartella')
        self.addfolder_button.bind("<ButtonRelease-1>", self.askdir)
        self.addfolder_button.grid(row=1, column=1, padx=15, pady=10, sticky='we')
        self.remove_button = ttk.Button(self.f1, text='Rimuovi')
        self.remove_button.bind("<ButtonRelease-1>", self.remove)
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
        self.run_button = ttk.Button(self.f3,text='Start')
        self.run_button.bind('<ButtonRelease-1>', self.run)
        self.run_button.grid(row=6, column=2, sticky='e', padx=10 ,pady=15)
        self.about = ttk.Button(self.f3,text='About',command=about)
        self.about.grid(row=6,column=0,sticky='W',padx=10,pady=15)
        self.quit = ttk.Button(self.f3, text='Chiudi')
        self.quit.bind('<ButtonRelease-1>', on_quit_clicked)
        self.quit.grid(row=6, column=1,sticky='we',padx=10,pady=15)

        self.f1.grid(row=0, column=0, sticky='we')
        self.f2.grid(row=2, column=0)
        self.f3.grid(row=4, column=0)

        self.master.mainloop()

    def popup(self, txt, errors=None):
        info = tkinter.Toplevel(self.master)
        if errors:
            txt += "I seguenti file hanno generato un'errore:\n"
            for error in errors:
                txt += error+'\n'
        msg = tkinter.Message(info, text=txt, bg="#ff6666", fg="white", aspect=1000)
        msg.grid()
        info.transient(self.master)

    def enable_window(self):
        self.run_button.configure(text='Start')
        self.addfile_button.configure(state = 'normal')
        self.addfolder_button.configure(state = 'normal')
        self.remove_button.configure(state = 'normal')
        self.listbox.configure(state = 'normal')
        self.check.configure(state = 'normal')
        self.change_destination.configure(state = 'normal')
        self.about.configure(state = 'normal')
        self.quit.configure(state = 'normal')

    def disable_window(self):
        self.run_button.configure(text='Stop')
        self.addfile_button.configure(state = 'disabled')
        self.addfolder_button.configure(state = 'disabled')
        self.remove_button.configure(state = 'disabled')
        self.listbox.configure(state = 'disabled')
        self.check.configure(state = 'disabled')
        self.destination_text.configure(state = 'disabled')
        self.about.configure(state = 'disabled')
        self.quit.configure(state = 'disabled')

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
            print(filename, 'added')    #debug

    def remove(self, event):
        t = self.listbox.curselection()
        while len(t) > 0:
            elem = self.filelist.pop(int(t[0]))
            print(elem, 'removed')
            self.listbox.delete(t[0])
            t = self.listbox.curselection()
        self.update_info()

    def clear(self):
        # clear filelist, listbox, initialize progress and files left
        self.listbox.delete(0, END)
        self.filelist = list()
        self.update_progress(0)

    def update_settings(self):
        if self.__change_output.get():
            dest = self.destination_text.get(1.0, END).split('\n')[0] + '/'
            if not os.path.isdir(dest):
                os.mkdir(dest)  # eccezione?
            else:
                dest = ''
            self.settings['dir'] = dest
        print('dir:', self.settings['dir'])

    def run(self, ev = None):
        if self.running:
            print('STOP')
            self.encoder.abort()
            self.aborted = True
            # it is still working
        # START pressed
        elif len(self.filelist) > 0:
            print('START')                
            self.running = True
            self.aborted = False
            self.disable_window()
            self.update_settings()
            self.encoder = Encoder(self.filelist, self.settings, self)
            self.encoder.start()
        else:
            print('Nessun file aggiunto.')

    def update_progress(self, progress=0, index=0):
        print('update_progress:',progress)
        self.progressbar.configure(value = progress)
        self.update_info(index)
        self.progresslabel.configure(text = str(progress) + " %.")

    def update_info(self, completed=0):
        self.infolabel.configure(text = str(len(self.filelist)-completed) + ' file da convertire.')

    def notify_finish(self, errors, new_filelist):
        print('notify finish')
        txt = 'Conversione file completata.\n'
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

