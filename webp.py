#! /usr/bin/env python3
# -*- coding: iso8859-15 -*-
# (C) Indrit Bashkimi indrit.bashkimi@gmail.com
# Version 0.5.0 apha
# ultima modifica: 16 marzo 2012

from tkinter import ttk
import tkinter.messagebox, tkinter.filedialog, tkinter.simpledialog
import os, platform
        
class style:
    def __init__(self,character,size,extra):
        self.character = character
        self.size = size
        self.extra = extra
    def getCharacter():
        return self.character
    def getSize():
        return self.size
    def getExtra():
        return self.extra
        
class ProgressBar:
    def __init__(self):
        self.Value=0
                        
class finestra:
    def quality(self,file):
        if not self.check2:
            return str(self.scale.get())
        i = len(file)-1
        while i>=0 and len(file)>8:
            if file[i-4:i-2]=="[q" and file[i] == "]" and str.isnumeric(file[i-2:i]):
                if file[i-2:i] == '00':
                    return '100'
                return file[i-2:i]
            i-=1
        q = tkinter.simpledialog.askstring('Qualità', os.path.split(file)[1]+'\nScegli la qualità q')
        if len(q)==0:
            q='85'
        return q

    def errore(self,d,l): #(dir, file[])
        if not os.path.isfile(d+l[1]) or os.path.getsize(d+l[1])==0:
                return 1
                
    def cwebp(self,src,dst,q):  
        size=os.path.getsize(src)/1024
        print('\tElaborando',os.path.split(src)[1], end='\t[ '+str(int(size))+' kb]\tq='+q+' --> ')
        os.system('cwebp -q '+q+' \"'+src+'\" -o \"'+dst+'\"') # cwebp -quality 80 image.png -o image.webp
        if os.path.exists(dst):
            print(os.path.split(dst)[1])
        else:
            print('ERRORE')

    def dwebp(self,src,dst):
        print('\tElaborando',os.path.split(src)[1],end='\t--> ')
        os.system('dwebp "'+src+'" -o "'+dst+'"') # dwebp image.webp -o image.png
        if os.path.exists(dst):
            print(os.path.split(dst)[1])
        else:
            print('ERRORE')
    def choseSaveDir(self):
        if self.check4==0:
            self.saveDir=tkinter.filedialog.askdirectory(title='Dove vuoi salvare le immagini?')+'/'
        else:
            self.saveDir=self.originalDir
    
    def elabora_file(self):
    
        myFormats=[
        ('File supportati','*.jpg'),('File supportati','*.JPG'),
        ('File supportati','*.png'),('File supportati','*.PNG'),
        ('File supportati','*.jpeg'),('File supportati','*.JPEG'),
        ('File supportati','*.webp'),('File supportati','*.WEBP'),
        ('Portable Network Graphics','*.png'),('Portable Network Graphics','*.PNG'),
        ('JPEG','*.jpg'),('JPEG','*.JPG'),
        ('JPEG','*.jpeg'),('JPEG','*.JPEG'),
        ('WebP','*.webp'),('WebP','*.WEBP'),]

        image_file = tkinter.filedialog.askopenfilename(filetypes=myFormats,title='Scegli il file da convertire')
        if len(image_file)==0: #evita di sovrascrivere toWebp e toPng
            return 0
            
        self.toWebp = []
        self.toPng = []
        self.originalDir=os.path.split(image_file)[0]+'/'
        self.saveDir=self.choseSaveDir()
        #self.toConvert=1
        self.l2.configure(text='1 file da convertire...')
        print('Sto lavorando in',os.path.split(image_file)[0],'\n1 file da convertire\n\n')
        
        self.createList(os.path.split(image_file)[1])
        self.readyToConvert=1
        
    def createList(self,file):
        if file[len(file)-3:] in ['jpg','JPG','png','PNG']:
            self.toWebp.append([file, file[:len(file)-3]+'webp', self.quality(file)])
        elif file[len(file)-4] in ['webp']:
            self.toPng.append([file, file[:len(file)-4]])
        elif file[len(file)-4] in ['jpeg','JPEG']:
            self.toWebp.append([file, file[:len(file)-4]+'webp', self.quality(file)])
                    
    def elabora_cartella(self):
    
        self.originalDir=tkinter.filedialog.askdirectory(title='Scegli la cartella con le immagini')+'/'
        self.choseSaveDir()
        self.toWebp = []
        self.toPng = []
        files=os.listdir(self.originalDir)
        if len(files)>0:
            #print('Elaborando',len(files),'files in',self.dir,'...\n')
            for file in files:
                self.createList(file)
        self.l2.configure(text=str(len(self.toWebp)+len(self.toPng))+' file da convertire...')        
        self.readyToConvert=1
        print(len(self.toWebp)+len(self.toPng),'file da convertire...')
        
    def convert(self):
        self.SetProgress(0)
        self.ERRORE=[]
    
        for file in self.toWebp:
            self.cwebp(self.originalDir+file[0], self.saveDir+file[1], file[2])
            if self.errore(self.saveDir, file):
                self.ERRORE.append(self.originalDir+file[1])
            self.IncrementProgress()
        for file in self.toPng:
            self.dwebp(self.originalDir+file[0], self.saveDir+file[1])
            if self.errore(self.saveDir, file):
                self.ERRORE.append(self.originalDir+file[1])
            self.IncrementProgress()
            
        if not len(ERRORE):   
            print('\n\nPROCESSO TERMINATO\n\n')
            tkinter.messagebox.showinfo("Fine","Processo terminato")
        else:
            print('Processo terminato, ma',len(ERRORE),'files hanno generato ERRORE durante la conversione!\n')
            for file in ERRORE:
                print(file)
            
    def information(self):
        info = tkinter.Toplevel(root)
        msg = tkinter.Message(info, text="WebP Converter è un programma realizzato da Indrit Bashkimi."
        "\nQuesto programma permette di convertire file .jpg o .png in .webp, un nuovo formato sviluppato da Google."
        "Permette anche di convertire file .webp in .png"
        "\nPer ulteriori informazioni, potete consultare la pagina ufficiale di Webp", bg="white", fg="black",font=('Ubuntu',10))
        msg.grid()
        info.transient(root)
        
    def __init__(self,root):
        self.readyToConvert=0 #quando finisce di elaborare la cartella o file, imposta lo status 1, così CONVERTI controlla se status è 1 per procedere
        #self.toConvert=0
        self.defaultfont='Ubuntu'
        self.color=['#FF6000','#ffe100','#f2f1f0','#000000'] #e0ff94 #titolo,descrizione,pulsanti
        
        self.originalDir=''
        self.saveDir=''
        
        self.checkVar1 = 0 # 0,1 (off, on)
        self.checkVar2 = 3 # 2,3
        self.checkVar3 = 5 # 4,5
        self.checkVar4 = 7 # 6,7
        self.radioVar1 = 1 # 8,9 (deve essere unico)
        self.progressStatus = 0
        
        self.createWidget()
        
    def createWidget(self):
        self.f1 = tkinter.Frame(root).grid(row='0',column='0')
        
        self.title = tkinter.Label(self.f1,text='WebP ConverteR', bg=self.color[0], font =(self.defaultfont,26,'bold')).\
            grid(row='0',column='0',columnspan='2',sticky='we')
        tkinter.Label(self.f1,text='WebP è un nuovo formato per le foto digitali, sviluppato da Google',bg=self.color[1],font=('Ubuntu',10)).\
            grid(row='1', column='0', columnspan='2',sticky='we')
        
        self.button1 = tkinter.Button(self.f1,text='Singolo file',bg=self.color[2],fg='#000000',\
            font=(self.defaultfont,12,'bold') ,command=self.elabora_file).grid(row='2', column='0',padx='10',pady='10',sticky='WE')
        self.button2 = tkinter.Button(self.f1,text='Cartella immagini', bg=self.color[2],fg='#000000',font=(self.defaultfont,12,'bold'),\
            command=self.elabora_cartella).grid(row='2', column='1',padx='10',pady='10',sticky='WE')
        
        ttk.Separator(self.f1).grid(row='3',column='0',columnspan='2',sticky='WE',padx='10',pady='5')
        
        tkinter.Label(self.f1,text='Qualità predefinita:',font=(self.defaultfont,11)).grid(row='4',column='0',sticky='E',padx='10')
        self.scale = tkinter.Scale(self.f1,fg=self.color[3], orient='horizontal', troughcolor=self.color[0],resolution='1',length=100,\
            from_=0,to=100,font=(self.defaultfont,10))
        self.scale.set(85)
        self.scale.grid(row='4',column='1',sticky='WE',padx='10')
        
        self.checkButton1 = tkinter.Checkbutton(self.f1,text='Applica la stessa qualità a tutti i file', variable=self.checkVar1,onvalue=1,\
            offvalue=0,state='normal',font=(self.defaultfont,10))
        self.checkButton1.grid(row='5',column='1',sticky='W',padx='10')
        
        tkinter.Label(self.f1,text='Opzioni generali:',font=(self.defaultfont,11)).grid(row=6,column='0',sticky='E',padx='10')
        self.checkButton2 = tkinter.Checkbutton(self.f1,text='Usa la qualità specificata del file',variable=self.checkVar2,\
            onvalue=3,offvalue=0,font=(self.defaultfont,10))
        self.checkButton2.select()
        self.checkButton2.grid(row='6',column='1',sticky='W',padx='10')
        
        self.checkButton3 = tkinter.Checkbutton(self.f1,text='Converti tutti i file',variable=self.checkVar3,onvalue=5,offvalue=4,\
            font=(self.defaultfont,10),command=self.check3Pressed)
        self.checkButton3.select()
        self.checkButton3.grid(row=7,column='1',sticky='W',padx='10')
        
        self.radioButton1 = tkinter.Radiobutton(self.f1,text='Non convertire file .webp', variable=self.radioVar1,value=1,\
            font=(self.defaultfont,10),state='disabled')
        self.radioButton1.grid(row=8,column='1',sticky='W',padx='10')
        self.radioButton2 = tkinter.Radiobutton(self.f1,text='Converti solo file .webp',state='disabled', variable=self.radioVar1, value=0,\
            font=(self.defaultfont,10))
        self.radioButton2.grid(row=9,column='1',sticky='W',padx='10')
        
        tkinter.Label(self.f1,text='Opzioni di salvataggio:',font=(self.defaultfont,11)).grid(row=10,column='0',sticky='E',padx='10')
        self.checkButton4 = tkinter.Checkbutton(self.f1,text='Stessa cartella dei file originali',variable=self.checkVar4,onvalue=7,offvalue=6,\
            font=(self.defaultfont,10),command=self.checkPressed4)
        self.checkButton4.select()
        self.checkButton4.grid(row='10',column='1',sticky='W',padx='10')
        
        self.text1 = tkinter.Text(self.f1,width=38, height=4)
        #self.text1.insert(end,'/home/indrit')
        self.text1.grid(row='11',column='0',padx='10',pady='10',sticky='WE')
        
        self.ChoseDirButton = tkinter.Button(self.f1,text='Cambia cartella',bg=self.color[2],fg='#000000',state='disabled',\
            font=(self.defaultfont,12,'bold'),command=self.choseSaveDir)
        self.ChoseDirButton.grid(row='11', column='1',padx='10',pady='10',sticky='WE')
        
        ttk.Separator(self.f1).grid(row='12',column='0',columnspan='2',sticky='WE',padx='10')
        
        self.infoLabel=tkinter.Label(self.f1,text='0 file da convertire',font=(self.defaultfont,12))
        self.infoLabel.grid(row='13',column='0',sticky='WE',padx='10')
        
        self.startConversion = tkinter.Button(self.f1,text='Converti',bg=self.color[0],height='1',font=(self.defaultfont,12))
        self.startConversion.bind("<Button-1>",self.startConversionPressed)
        self.startConversion.grid(row='13',column='1',pady='10')
        
        self.progressBar=ttk.Progressbar(self.f1,mode='determinate',value='0',maximum='100')
        self.progressBar.grid(row='14',column='0',sticky='WE',columnspan='2',padx='10')
        
        ttk.Separator(self.f1,orient='horizontal').grid(row='16',column='0',sticky='WE',columnspan='2',padx='10',pady='5')
        self.information = tkinter.Button(self.f1,text='Information',bg=self.color[2],font=(self.defaultfont,12),command=self.information).\
            grid(row='17',column='0',sticky='W',padx='10',pady='10')
        self.close = tkinter.Button(self.f1,text='Chiudi',bg=self.color[2],font=(self.defaultfont,12),command=root.destroy).\
            grid(row='17',column='1',sticky='E',padx='10',pady='10')
    def choseSaveDir(self):
        self.saveDir = self.saveDir=tkinter.filedialog.askdirectory(title='Dove vuoi salvare le immagini?')+'/'
        
    def startConversionPressed(self,event):
        print("Avvia conversione.")
        self.startConversion.configure(text='Ferma processo')
        if self.readyToConvert:
            self.convert()
        else:
            print("Scegli file")
        #print('Il nome del pulsante: '+self.start["text"]) #self.start.config()
        #print('Il suo colore è: '+self.start['bg'])
        #print('il valore di q è: '+str(self.scale.get()))
        #print('il valore di check: '+str(self.check1))
        #self.progress.config(value='1')
        #self.ask_same_q.select()
        #self.IncrementProgress()
    def check3Pressed(self):
        print(str(self.checkButton3))
        if self.checkVar4 == 7:
            self.checkVar4=6
            self.radioButton1.config(state='normal')
            self.radioButton2.config(state='normal')
        else:
            self.checkVar4=7
            self.radioButton1.config(state='disabled')
            self.radioButton2.config(state='disabled')
                       
    def checkPressed4(self):
        if self.checkVar4==6:
            self.checkVar4=7
            self.ChoseDirButton.config(state='normal')
        else:
            self.checkVar4=6
            self.ChoseDirButton.config(state='disabled')
                        
    def SetProgress(self,valore):
        self.progressStatus=valore
        self.progressBar.config(value=str(valore))
              
    def IncrementProgress(self,value):
        pass
    def SimpelIncrementProgress(self):
        self.progressStatus+=1
        self.progressBar.config(value=str(self.progress_var))
        
    def AzzeraProgress(self):
        self.progressStatus=0
        self.SetProgress(0)
            
    def getDefaultFonf(self):
        return self.defaultfont
        
if platform.python_version()[0]=='3' and platform.system()=='Linux':
    root=tkinter.Tk()
    root.title('WebP ConverteR')
    finestra(root)
    root.mainloop()
else:
    print('Per eseguire questo script serve Python 3 e un sistema operativo Linux')
    input()
