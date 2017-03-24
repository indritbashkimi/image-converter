#! /usr/bin/env python3
# -*- coding: iso8859-15 -*-
# (C) Indrit Bashkimi indrit.bashkimi@gmail.com
# Version 0.4 beta
# ultima modifica: 2 novembre 2011

from tkinter import ttk
import tkinter.messagebox, tkinter.filedialog, tkinter.simpledialog
import os, platform

def quality(file):
    def q():
        q=tkinter.simpledialog.askstring('Qualità', os.path.split(file)[1]+'\nScegli la qualità q')
        if len(q)==0:
            q='100'
        return q
    
    i = len(file)-1
    while i>=0:
        if file[i] == "]":
            if file[i-4:i-2]=="[q": # i-2 è escluso
                try:
                    return str(int(file[i-2:i])) # se non è un numero da errore
                except:
                    return q()
        i-=1
    return q()
        
def webp(src,dst,q,i):
    size=os.path.getsize(src)/1024
    print(str(i)+'\tElaborando',os.path.split(src)[1], end='\t[ '+str(int(size))+' kb]\tq='+q+' --> ')
    os.system('cwebp -q '+q+' "'+src+'" -o "'+dst+'"') # cwebp -quality 80 image.png -o image.webp
    if os.path.exists(dst):
        print(os.path.split(dst)[1])
    else:
        print('ERRORE')

def dwebp(src,dst,i):
    print(str(i)+'\tElaborando',os.path.split(src)[1],end='\t--> ')
    os.system('dwebp "'+src+'" -o "'+dst+'"') # dwebp image.webp -o image.png
    if os.path.exists(dst):
        print(os.path.split(dst)[1])
    else:
        print('ERRORE')

def file():
    myFormats=[
    ('File supportati','*.jpg'),
    ('File supportati','*.JPG'),
    ('File supportati','*.png'),
    ('File supportati','*.PNG'),
    ('File supportati','*.jpeg'),
    ('File supportati','*.JPEG'),
    ('File supportati','*.webp'),
    ('File supportati','*.WEBP'),
    ('Portable Network Graphics','*.png'),
    ('Portable Network Graphics','*.PNG'),
    ('JPEG','*.jpg'),
    ('JPEG','*.JPG'),
    ('JPEG','*.jpeg'),
    ('JPEG','*.JPEG'),
    ('WebP','*.webp'),
    ('WebP','*.WEBP'),
    ]
    File=tkinter.filedialog.askopenfilename(filetypes=myFormats,title='Scegli il file da convertire')
    print('Sto lavorando in',os.path.split(File)[0],'\n1 file da convertire\n\n')
    if File[len(File)-3:] in ['jpg','JPG','png','PNG']:       # se gli ultimi 3 caratteri sono..
        webp(File,File[:len(File)-3]+'webp',quality(os.path.split(File)[1]),1)
    elif File[len(File)-4:] in ['webp']:
        dwebp(File,File[:len(File)-4]+'png',1)
    else:   #elif File[len(File)-4:] in ['jpeg','JPEG']:
        webp(File,File[:len(File)-4]+'webp',quality(os.path.split(File)[1]),1)
    print('\n\nPROCESSO TERMINATO\n\n')
    tkinter.messagebox.showinfo("Success","Processo terminato")
    
def cartella():
    dir=tkinter.filedialog.askdirectory(title='Scegli la cartella con le immagini')+'/'
    files=os.listdir(dir)
    print(type(files))
    if len(files)>0:
        print('Sto lavorando in',dir,'\n',len(files),'file da elaborare\n\n')
        i=0
        for file in files:
            if file[len(file)-3:] in ['jpg','JPG','png','PNG']:
                webp(dir+file,dir+file[:len(file)-3]+'webp',quality(file),i)
            elif file[len(file)-4] in ['webp']:
                dwebp(dir+file,dir+file[:len(file)-4],i)
            elif file[len(file)-4] in ['jpeg','JPEG']:
                webp(dir+file,dir+file[:len(file)-4]+'webp',quality(file),i)
            else:
                print(os.path.split(file)[1],'non è un file supportato')
            i+=1
    else:
        print ('Cartella vuota!')
        tkinter.messagebox.showerror("Errore","Cartella vuota!")
    print('\n\nPROCESSO TERMINATO\n\n')
    tkinter.messagebox.showinfo("Fine","Processo terminato")
        
def main():
    color=('#FF6000','#e0ff94','#009FFF','#ffffff')
    titolo='WebP ConverteR v. 0.3'
    root=tkinter.Tk()
    root.title('WebP ConverteR')
    tkinter.Label(root,text=titolo, bg=color[0], font =('Arial',18)).grid(row='0', column='0', columnspan='2', sticky='we')
    testo='Il programma converte i file .jpeg o .png in .webp e i file .webp in .png\ne li riconosce in modo automatico.'
    tkinter.Label(root,text=testo,bg=color[1], font=('Arial',10)).grid(row='1', column='0', columnspan='2',sticky='we')
    tkinter.Button(root,text='     Singolo file     ', bg=color[2],fg=color[3],font=('Arial',12),command=file).grid(row='2', column='0',pady='10')
    tkinter.Button(root,text='Cartella immagini', bg='#009FFF',fg='#ffffff',font=('Arial',12), command=cartella).grid(row='2', column='1',pady='10')
    root.mainloop()

if platform.python_version()[0]=='3' and platform.system()=='Linux':
    main()
else:
    print('Per eseguire questo script serve Python 3 e un sistema operativo Linux')
    input()
