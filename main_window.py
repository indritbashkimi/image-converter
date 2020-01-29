from pathlib import Path
from tkinter import *
from tkinter import ttk
import tkinter.filedialog
import tkinter.messagebox
from manager import ManagerListener, Manager
from options_window import OptionsWindow
import settings
import os


class MyListbox(Listbox):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf)

    def clear(self):
        self.delete(0, END)

    def delete_elem(self, path: Path):
        index = 0
        for elem in self.get(0, END):
            if elem == path.absolute().__str__():
                break
            index += 1
        self.delete(index)


class MainWindow(ManagerListener):
    def __init__(self):
        super().__init__()
        self.default_base = '/home/'
        self.running = False
        self.encoder = None
        self.manager = Manager()
        self.manager.add_listener(self)

        self.encoding_started = False

        self.master = Tk()
        self.master.protocol('WM_DELETE_WINDOW', self.destroy)
        # self.master.resizable(False, False)
        self.master.title('Webp Converter')
        self.change_output = BooleanVar()

        """ style """
        ttk.Style().configure("TButton")
        ttk.Style().configure("TLabel")
        ttk.Style().configure("TProgressbar")

        ''' menu '''
        self.menu = Menu(self.master, relief=FLAT)
        menu_file = Menu(self.menu, tearoff=0)
        menu_file.add_command(label='Add File', command=self.ask_file)
        menu_file.add_command(label='Add Folder', command=self.ask_dir)
        menu_file.add_separator()
        menu_file.add_command(label='Exit', command=self.destroy)
        self.menu.add_cascade(label='File', menu=menu_file)
        menu_edit = Menu(self.menu, tearoff=0)
        menu_edit.add_command(label='Select All', command=self.remove_file)
        menu_edit.add_command(label='Remove', command=self.remove_file)
        menu_edit.add_separator()
        menu_edit.add_command(label='Options', command=self.open_options_window)
        self.menu.add_cascade(label='Edit', menu=menu_edit)
        menu_help = Menu(self.menu, tearoff=0)
        menu_help.add_command(label='About', command=self.about)
        self.menu.add_cascade(label='Help', menu=menu_help)
        self.master.config(menu=self.menu)

        ''' frames '''
        toolbar = Frame(self.master)
        input_frame = ttk.Frame(self.master)
        output_format_frame = ttk.Frame(self.master)
        dest_frame = Frame(self.master)
        bottom_frame = Frame(self.master)

        ''' toolbar '''
        self.addfile_button = ttk.Button(toolbar, text='Add File')
        self.addfile_button.bind("<ButtonRelease-1>", self.ask_file)
        self.addfile_button.pack(side='left', padx=10, pady=10)
        self.add_folder_button = ttk.Button(toolbar, text='Add Folder')
        self.add_folder_button.bind("<ButtonRelease-1>", self.ask_dir)
        self.add_folder_button.pack(side='left', padx=10, pady=10)
        self.remove_button = ttk.Button(toolbar, text='Remove')
        self.remove_button.bind("<ButtonRelease-1>", self.remove_file)
        self.remove_button.pack(side='left', padx=10, pady=10)
        self.options_button = ttk.Button(toolbar, text='Options', style='TButton')
        self.options_button.bind("<ButtonRelease-1>", self.open_options_window)
        self.options_button.pack(side='right', padx=10, pady=10)
        ttk.separator = ttk.Separator(toolbar, orient='vertical').pack(side='right', fill='y', padx=10, pady=10)

        ''' input frame '''
        ttk.Label(input_frame, text='Source', style='TLabel').pack(anchor='nw', padx='10', pady='10')
        self.scrollbar = Scrollbar(input_frame, orient="vertical")
        self.listbox = MyListbox(input_frame, selectmode=EXTENDED,
                               yscrollcommand=self.scrollbar.set, height=15)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side='right', fill='y')
        self.listbox.pack(side='left', fill='both', expand=1, padx=10, pady=10)

        ''' destination frame '''
        ttk.Label(dest_frame, text='Destination', style='TLabel').pack(anchor='nw', padx=10)

        self.check = Checkbutton(dest_frame, text='Save in:',
                                 variable=self.change_output,
                                 onvalue=True, offvalue=False,
                                 command=self.on_check_changed)
        self.check.pack(side='left', padx=10, pady=10)
        self.destination_entry = Entry(dest_frame)
        self.destination_entry.insert(0, self.default_base)
        self.destination_entry.pack(side='left', expand=1, fill='x', padx=10)
        self.change_destination = ttk.Button(dest_frame, text='Change')
        self.change_destination.bind("<ButtonRelease-1>", self.set_destination)
        self.change_destination.pack(side='right', padx=10, pady=10)
        self.change_destination.configure(state='disabled')

        ''' bottom frame '''
        self.info_label = ttk.Label(bottom_frame, style='TLabel')
        self.update_status_bar(0)
        self.info_label.pack(anchor='nw', padx=10)
        self.progressbar = ttk.Progressbar(bottom_frame, mode='determinate', value=0, maximum=100)
        self.progressbar.pack(side='left', expand=1, fill='x', padx=10, pady=10)
        self.progress_label = ttk.Label(bottom_frame, text='0 %', style='TLabel')
        self.progress_label.pack(side='left', padx=10, pady=10)
        self.run_button = Button(bottom_frame, text='Start')
        self.run_button.bind('<ButtonRelease-1>', self.do_job)
        self.run_button.pack(side='right', padx=10)

        ''' packing frames '''
        ttk.separator = ttk.Separator(self.master, orient='horizontal').pack(expand=1, fill='x')
        toolbar.pack(expand=1, fill='both')
        ttk.separator = ttk.Separator(self.master, orient='horizontal').pack(expand=1, fill='x')
        input_frame.pack(expand=1, fill='both')

        self.output_format = StringVar()
        Label(output_format_frame, text='Output format:').pack(side='left', padx=10, pady=10)
        pass_combobox = ttk.Combobox(output_format_frame, textvariable=self.output_format, state='readonly')
        pass_combobox['values'] = settings.supported_formats
        pass_combobox.current(2)
        pass_combobox.pack(side='left', expand=1, fill='x', padx=10)

        output_format_frame.pack(expand=1, fill='both')
        dest_frame.pack(expand=1, fill='both')
        bottom_frame.pack(expand=1, fill='both', pady=5)
        self.master.mainloop()

    def set_destination(self, event=None):
        if not self.running and self.change_output.get():
            dirname = tkinter.filedialog.askdirectory(title='Where do you want to save the images?')
            if dirname:
                # dir += '/'
                self.destination_entry.delete(0, END)
                self.destination_entry.insert(0, dirname)

    def on_check_changed(self):
        # print('change output: '+str(self.change_output.get()))
        if self.change_output.get():
            self.change_destination.configure(state='normal')
        else:
            self.change_destination.configure(state='disabled')

    def open_options_window(self, event=None):
        if not self.running:
            OptionsWindow(self.master, self.manager.get_parameters())

    def destroy(self):
        do_exit = True
        if self.running:
            if tkinter.messagebox.askyesno("Stai per uscire", "Interrompere la conversione e uscire?"):
                self.encoder.abort()
                self.encoder.join()
            else:
                do_exit = False
        if do_exit:
            self.master.destroy()

    def about(self):
        master = tkinter.Toplevel(self.master)
        txt = "WebPConverter permette di convertire file .jpg e .png" + \
              " in .webp e viceversa.\n" + \
              "Per ulteriori informazioni, potete consultare " + \
              "la pagina ufficiale di Webp."
        msg = tkinter.Message(master, text=txt, aspect=300)
        msg.grid()
        ttk.Button(master, text='Chiudi', command=master.destroy).grid(sticky='E', padx=5, pady=5)
        master.transient(self.master)

    def show_info(self, txt, errors=None):
        master = tkinter.Toplevel(self.master)
        if errors:
            txt += "I seguenti file hanno generato un'errore:\n"
            for error in errors:
                txt += error + '\n'
        msg = tkinter.Message(master, text=txt, aspect=1000)
        msg.grid()
        ttk.Button(master, text='Close', command=master.destroy).grid(sticky='E', padx=5, pady=5)
        master.transient(self.master)

    def enable_window(self):
        self.run_button.configure(text='Start')
        self.addfile_button.configure(state='normal')
        self.add_folder_button.configure(state='normal')
        self.remove_button.configure(state='normal')
        self.listbox.configure(state='normal')
        self.options_button.configure(state='normal')
        self.check.configure(state='normal')
        self.destination_entry.configure(state='normal')
        self.change_destination.configure(state='normal')

    def disable_window(self):
        self.run_button.configure(text='Stop')
        self.addfile_button.configure(state='disabled')
        self.add_folder_button.configure(state='disabled')
        self.remove_button.configure(state='disabled')
        self.listbox.configure(state='disabled')
        self.options_button.configure(state='disabled')
        self.check.configure(state='disabled')
        self.destination_entry.configure(state='disabled')
        self.change_destination.configure(state='disabled')

    def ask_file(self, event=None):
        if not self.running:
            uri = tkinter.filedialog.askopenfilename(filetypes=settings.file_pattern,
                                                     title='Scegli il file da convertire')
            if uri:
                self.manager.add_file(Path(uri))

    def ask_dir(self, event=None):
        if not self.running:
            dirname = tkinter.filedialog.askdirectory(title='Scegli la cartella con le immagini')
            print(type(dirname))
            print(dirname)
            if dirname:
                dirname += '/'
                for filename in os.listdir(dirname):
                    self.manager.add_file(Path(dirname + filename))

    def remove_file(self, event=None):
        t = self.listbox.curselection()
        while len(t) > 0:
            self.manager.remove_file_at(int(t[0]))
            self.listbox.delete(t[0])
            t = self.listbox.curselection()

    def update_parameters(self):
        parameters = self.manager.get_parameters()
        if self.change_output.get() and self.destination_entry.get():
            parameters['dir'] = self.destination_entry.get() + '/'
        else:
            parameters['dir'] = ''
        parameters['output_format'] = str(self.output_format.get())
        print(parameters['output_format'])

    def do_job(self, event=None):
        if self.encoding_started:
            self.manager.stop_job()
        else:
            self.update_parameters()
            self.manager.start_job()

    def update_status_bar(self, total):
        self.info_label.configure(text=str(total) + ' ' + ('file' if total == 1 else 'files') + ' to convert.')

    def on_encoding_start(self):
        self.encoding_started = True
        self.disable_window()

    def on_file_add(self, path: Path, total: int):
        self.listbox.insert(END, path.absolute())
        self.update_status_bar(total)
        print(path.absolute(), ' added')

    def on_file_remove(self, path: Path, total: int):
        self.update_status_bar(total)
        print(path.absolute(), ' removed')

    def on_encoding_finish(self, stopped=False, errors=None):
        self.encoding_started = False
        tkinter.messagebox.showinfo("Conversione finita", " con successo")

    def on_progress(self, progress: float):
        print('update_progress:', progress)
        self.progressbar.configure(value=progress)
        self.progress_label.configure(text=str(progress) + " %")

    def on_file_encode(self, path: Path, success: bool, files_left: int):
        self.listbox.delete_elem(path)
        self.update_status_bar(files_left)

    def on_encoding_stop(self):
        self.encoding_started = False
        tkinter.messagebox.showinfo("Conversione file", " interrotta")
