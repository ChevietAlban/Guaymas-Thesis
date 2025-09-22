# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 09:34:23 2022

@author: Alban
"""

from tkinter import END
import numpy as np
import csv
import pandas as pd
import os
import tkinter as tk
import matplotlib.pyplot as plt 
# from math import sqrt
import plotly.express as px
import plotly.io as io 
# from matplotlib import image
from tkinter import Tk, Label,Scrollbar, Frame,messagebox,Listbox, Entry, Button,Toplevel,Canvas, StringVar, CENTER,Checkbutton, IntVar,RIDGE, NSEW, filedialog
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter.filedialog import askopenfilename
# import tkinter.font as font
# from skimage.transform import resize
# from tifffile import TiffFile
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from ternary_diagram import TernaryDiagram #conda install -c conda-forge ternary-diagram
from PIL import Image, ImageTk
import tkinter.messagebox
import tkinter.filedialog
import kaleido
import shutil
import re

Image.MAX_IMAGE_PIXELS = None
io.renderers.default='browser'
# io.kaleido.scope.default_format = "svg"
# io.kaleido.scope.mathjax = None
path ='tab_minerals.csv'

def on_frame_configure(canvas):
    """Reset the scroll region to encompass the inner frame."""
    canvas.configure(scrollregion=canvas.bbox("all"))


"""Ouverture des fichiers de paramètres"""
with open(path, 'r') as reader_tab_minerals :
    reader_tab_minerals  = csv.reader(reader_tab_minerals, delimiter = ',')
    convert_tab_minerals = list(reader_tab_minerals)
    tab_minerals         = np.array(convert_tab_minerals)
option_minerals_list = tab_minerals[0,1:]
option_minerals_list = option_minerals_list.tolist() 

control_formule_strcutrale_exist = 0

info_bases_MEB="""User :   
    
Sample :

Dates of analysis :

Conditions of analysis (Voltage, Current, time acquisition):
    
Detector :
    
Instrument : MEB ApreoS Thermofisher

Standards :
    
Comments :
    
File path : """

info_bases_MIC="""User :   
    
Sample :  

Dates of analysis :   

Conditions of analysis (Voltage, Current):  
    
Standards :  
    
Instrument : EPMA Jeol Lausanne
    
Comments :  
    
File path : """



"Microsonde"
def show_files_MIC_project():
    global listbox_files_project_MIC
    listbox_files_project_MIC = Listbox(tab_menu_MIC)
    listbox_files_project_MIC.bind('<ButtonRelease-1>',selection_files_MIC)
    listbox_files_project_MIC.grid(row=0,column=0,columnspan=2,rowspan=5,sticky="NS"+"EW")

    k=0
    l=1
    while k<len(files_project_mic):
        listbox_files_project_MIC.insert(k,files_project_mic[k])
        k=k+1
        l=l+1
def selection_files_MIC(e):
    #global extension_mic
    listbox_selection = listbox_files_project_MIC.curselection()
    fichier = listbox_files_project_MIC.get(listbox_selection)
    extension = os.path.splitext(fichier)
    extension = extension[1]
    print(extension,fichier)
    os.startfile(project_name_mic+'/'+fichier)
def create_MIC_path():
    global new_project_path
    new_project_path = tkinter.filedialog.askdirectory(title='Select a folder')
    w_MIC_create.configure(background="green")  
def create_MIC_project():
    global files_project_mic,project_name_mic,info_bases_MIC
    project_name_mic = project_MIC_name.get()
    project_name_mic = new_project_path+"/"+project_name_mic
    os.makedirs(project_name_mic)
    if os.path.exists(project_name_mic):
        w_MIC_create.destroy()
    files_project_mic = os.listdir(project_name_mic)
    info_bases_MIC=info_bases_MIC+project_name_mic
    w_MIC()
    show_files_MIC_project() 
def w_MIC_create():
    global w_MIC_create,import_MIC_data,create_MIC_project,project_MIC_name,MIC_entry_label
    eval_ = main_w.nametowidget('.').eval
    eval_('tk::PlaceWindow %s center' % main_w)
    w_MIC_create = Toplevel(main_w, bg = "white") 
    w_MIC_create.focus_set()
    w_MIC_create.title("Project")
    w_MIC_create.geometry("%dx%d" % (300,175))
    w_MIC_create.columnconfigure(0,weight=1)
    w_MIC_create.rowconfigure(0,weight=1)
    w_MIC_create.rowconfigure(1,weight=1)
    w_MIC_create.rowconfigure(2,weight=1)
    w_MIC_create.rowconfigure(3,weight=1)
    #Boutons
    import_MIC_path = ttk.Button(w_MIC_create, text="Project Path", command = create_MIC_path,width = 26)
    import_MIC_path.grid(row=2, column=0,columnspan=1, sticky='nsew')
    import_MIC_path.grid(pady=2,padx=2,ipady=2)
    create_MIC_project = ttk.Button(w_MIC_create, text="Create Project", command = create_MIC_project,width = 26)
    create_MIC_project.grid(row=3, column=0,columnspan=1, sticky='nsew')
    create_MIC_project.grid(pady=2,padx=2,ipady=2)
    #Entry
    project_MIC_name = ttk.Entry(w_MIC_create,width = 26,justify='center',font=20)
    project_MIC_name.grid(row=1, column=0,ipady=4,pady=2,padx=2)
    MIC_entry_label = ttk.Label(w_MIC_create,text="Project Name",background="white",font=20)
    MIC_entry_label.grid(row=0, column=0,ipady=4,pady=1,padx=2)
def w_MIC_open():
    global project_name_mic, files_project_mic
    project_name_mic = tkinter.filedialog.askdirectory(title='Select a folder')
    files_project_mic = os.listdir(project_name_mic)
    w_MIC() 
    show_files_MIC_project()
def show_main_w_MIC():
    save_data = (metadata_mic.get(1.0,END))
    automatic_data_save = project_name_mic+'/Metadata.txt'
    txt_write_data = open(automatic_data_save, 'w')
    txt_write_data.write(save_data)
    txt_write_data.close()
    MIC_win.destroy()
    main_w.deiconify() 
def w_MIC():                                                       #main Microprobe windows
    global MIC_win,tab_menu_MIC,metadata_mic
    print('MIC')
    MIC_win = Toplevel(main_w)
    MIC_win.title("Microprobe analysis")
    MIC_win.geometry("%dx%d" % (1300, 700))
    MIC_win.configure(bg="white")
    MIC_win.focus_set()
    MIC_win.update()
    main_w.withdraw()
    MIC_win.protocol("WM_DELETE_WINDOW",  show_main_w_MIC)
    tab_menu_MIC      = Frame(MIC_win,bg="white",highlightbackground='white')
    tab_menu_MIC.grid(row=1, column=0,columnspan=6,sticky="NS"+"EW")
    tab_calculate_MIC = Frame(MIC_win,bg="blue",highlightbackground='white')
    tab_plot_MIC      = Frame(MIC_win,bg="red",highlightbackground='white') 
    #configure les colonnes et lignes pour que tout reste en place si il y a changement de taille de la fenetre
    k=0
    while k<6 :
        MIC_win.columnconfigure(k, weight=1)
        tab_menu_MIC.columnconfigure(k, weight=1)   
        k=k+1  
    MIC_win.rowconfigure(0, weight=1)
    MIC_win.rowconfigure(1, weight=10)
    tab_menu_MIC.rowconfigure(0, weight=1)
    tab_menu_MIC.rowconfigure(1, weight=1)
    tab_menu_MIC.rowconfigure(2, weight=1)
    tab_menu_MIC.rowconfigure(3, weight=1)
    tab_menu_MIC.rowconfigure(4, weight=100)
    tab_calculate_MIC.rowconfigure(0, weight=1)
    tab_calculate_MIC.rowconfigure(1, weight=4)
    
    tab_calculate_MIC.columnconfigure(0, weight=1)
    tab_calculate_MIC.columnconfigure(1, weight=1)
    tab_calculate_MIC.columnconfigure(2, weight=1)
    tab_calculate_MIC.columnconfigure(3, weight=1)
    def show_menu_MIC():
        tab_calculate_MIC.grid_remove()
        tab_plot_MIC.grid_remove()
        tab_menu_MIC.grid()
    def show_calculate_MIC():
        tab_calculate_MIC.grid(row=1, column=0,columnspan=6,sticky="NS"+"EW")
        tab_plot_MIC.grid_remove()
        tab_menu_MIC.grid_remove()
    def show_plot_MIC():
        tab_calculate_MIC.grid_remove()
        tab_plot_MIC.grid(row=1, column=0,columnspan=6,sticky="NS"+"EW")
        tab_menu_MIC.grid_remove()
    def save_MIC_project():
        a=1
    def save_formule_structurale():
        SAVE_formule=tkinter.filedialog.asksaveasfile(title="Save as...",filetypes=[('CSV files','.csv')],defaultextension = ".txt") 
        save_formule_structurale = pd.DataFrame(formule_structurale[1:,1:], index = formule_structurale[1:,0], columns = formule_structurale[0,1:])
        save_formule_structurale.to_csv(SAVE_formule)
    def import_MIC_data():
        global files_project_mic
        dossier_a_importer=tkinter.filedialog.askdirectory(title='Select a folder')
        files_dossier_source = os.listdir(dossier_a_importer)
        shutil.copytree(dossier_a_importer,project_name_mic+"/"+"Folder 1")
        for i in files_dossier_source :
             os.rename(project_name_mic+"/"+"Folder 1"+"/"+ i, project_name_mic +"/"+ i)  
        shutil.rmtree(project_name_mic+"/"+"Folder 1")
        files_project_mic = os.listdir(project_name_mic)
        show_files_MIC_project()
    bouton_main_show1 = ttk.Button(MIC_win, text="HOME", command = show_main_w_MIC)
    bouton_main_show1.grid(row=0, column=0,ipady=0,sticky="news")
    bouton_save_MIC   = ttk.Button(MIC_win, text="Save Project", command = save_MIC_project)
    bouton_save_MIC.grid(row=0, column=1,ipady=0,sticky="news")
    bouton_import_MIC   = ttk.Button(MIC_win, text="Import data", command = import_MIC_data)
    bouton_import_MIC.grid(row=0, column=2,ipady=0,sticky="news")
    bouton_menu_MIC   = ttk.Button(MIC_win, text="Meta-data", command = show_menu_MIC)
    bouton_menu_MIC.grid(row=0, column=3,ipady=0,sticky="news")
    bouton_calculate_MIC = ttk.Button(MIC_win, text="APFU", command = show_calculate_MIC)
    bouton_calculate_MIC.grid(row=0, column=4,ipady=0,sticky="news")
    bouton_plot_MIC = ttk.Button(MIC_win, text="Plots", command = show_plot_MIC)
    bouton_plot_MIC.grid(row=0, column=5,ipady=0,sticky="news")
    metadata_mic = tk.Text(tab_menu_MIC, wrap='word')
    metadata_mic.grid(row=1, column=2,rowspan=1,columnspan=5,sticky="ew"+"ns")
    label_MIC_date = ttk.Label(tab_menu_MIC, text = 'Metadata (automatically saved in the parent folder)',justify='center',anchor='s',background="white")
    label_MIC_date.grid(row=0, column=2,rowspan=1,columnspan=4,sticky="ew"+"ns")
    #Créer le fichier de métadonnées .txt dans le dossier parent si il n'existe pas.
    name_of_metadata_mic = project_name_mic + '/Metadata.txt'
    print(os.path.exists(name_of_metadata_mic))
    if  os.path.exists(name_of_metadata_mic)  is True :
        reader_acces = open(name_of_metadata_mic, 'r')
        liste = reader_acces.read()
        metadata_mic.insert(tk.END,liste)
    else : 
        
        metadata_mic.insert(tk.END,info_bases_MIC)

    def onopen_mic():
        global access,affichage_chemical_data,chemical_data_size, chemical_data,Sum_Total_recalc, chemical_data_num,chemical_data_brut, tab_ref_red, tab_ref_size, Oxy_architecture, option_minerals_list, tab_minerals,formule_structurale_shape
        FILE = askopenfilename(title="Select a file",filetypes=[('CSV FILES','*.csv')])    
        data = FILE
        def remove_whitespace(x):
            try:
                #remove spaces inside and outside of string
                x = "".join(x.split())

            except:
                pass
            return x
        data = data.applymap(remove_whitespace)

        data.to_csv('chemical_data_cor.csv', sep = ',')

        with open('chemical_data_cor.csv', 'r') as reader_chemical_data :
            reader_chemical_data = csv.reader(reader_chemical_data, delimiter = ',')
            convert_chemical_data = list(reader_chemical_data)
            chemical_data = np.array(convert_chemical_data)

        chemical_data[chemical_data == ''] = 0
        chemical_data = np.delete(chemical_data, 1, axis = 0)
        top_position  = np.where(chemical_data=='No.')
        top_position  = int(top_position[0])
        bot_position  = np.where(chemical_data=='Minimum')
        bot_position  = int(bot_position[0]-1)
        chemical_data_brut = chemical_data[2:-6,1:]
        chemical_data = chemical_data[top_position:bot_position,3:-2]
        """Choix du minéral"""
        with open('tab_minerals.csv', 'r') as reader_tab_minerals :
            reader_tab_minerals  = csv.reader(reader_tab_minerals, delimiter = ';')
            convert_tab_minerals = list(reader_tab_minerals)
            tab_minerals         = np.array(convert_tab_minerals)

        option_minerals_list = tab_minerals[0,1:]   


        """Importation et réduction du tableau périodique"""

        tab_ref = pd.read_csv('table_ref_chemical_elements_microprobe.csv', sep = ';', engine = 'python')

        for i in tab_ref :                                                                   #pour tous les élements dans tab_ref                                                           
            index_chemical_data_tab_ref = tab_ref.columns.searchsorted(chemical_data[0,:])   #rechercher les valeurs qui correspondent à la première ligne de chemical_data
        tab_ref_red   = tab_ref.iloc[:,index_chemical_data_tab_ref]                          #selectionne seulement les colonnes utiles
        tab_ref_red   = np.array(tab_ref_red)                                                #transforme en format numpy
        tab_ref_size  = tab_ref_red.shape                                                    #prend la dimension de tab_ref_red
        tab_ref_size  = tab_ref_size[1]                                                      #prend le  nombre de colonnes de tab_ref_red
        tab_ref_num   = tab_ref_red.astype(float)                                            #prend que les valeurs numériques

        chemical_data_num = (chemical_data[1:,:]).astype(float)
        chemical_data_size = chemical_data.shape                                     #donne la taille de chemical_data
        chemical_data_size_index = chemical_data_size[0]
        chemical_data_size_cols  = chemical_data_size[1]                              #prends le nombre de colonnes de chemical_data
   
    
    def check_min():
        global mineral, mineral_pos, mineral_choice,Oxy_architecture, tab_minerals, Mineral_type
        check=mb.askquestion(title='Selection', message=f'Do you want select {select_mineral.get()} ? ')
        if check=='yes' :
            mineral               = select_mineral.get()
            mineral_choice        = option_minerals_list.index(mineral)
            Oxy_architecture      = np.empty((chemical_data_size[0]-1,1), dtype = int)
            Oxy_architecture[:,0] = int(tab_minerals[1,mineral_choice+1])
            Mineral_type          = np.empty((chemical_data_size[0]-1,1),dtype = int)
            k=0
            while k < chemical_data_size[0]-1 :
                Mineral_type[k,0]          = tab_minerals[2,mineral_choice+1]
                k=k+1
        else : 
            mb.showinfo(title='Choice', message='Please select an other mineral !')  


    
    frame_button = Frame(tab_calculate_MIC,bg="green",highlightbackground='white')
    frame_button.grid(row=0, column = 0,columnspan=4,sticky="NS"+"EW")
    frame_button.columnconfigure(0,weight=1)
    frame_button.rowconfigure(0,weight=1)
    frame_button.rowconfigure(1,weight=1)
    frame_button.rowconfigure(2,weight=1)
    frame_button.rowconfigure(3,weight=1)
    frame_button.rowconfigure(4,weight=1)
    frame_results = Frame(tab_calculate_MIC,bg="red",highlightbackground='white')
    frame_results.grid(row=1, column = 0,columnspan=4,sticky="NS"+"EW")
    
    select_mineral=ttk.Combobox(frame_button, textvariable=option_minerals_list,font=16)
    select_mineral['values']=option_minerals_list
    select_mineral.grid(column=0, row=1, sticky='news')
    # #Monomineral
    button_open=ttk.Button(frame_button,text="Open SEM file...", command=onopen_mic)
    button_open.grid(row=0, column=0, sticky='news')
    #bouton lancer le calcul
    button_calcul=ttk.Button(frame_button,text="Calcul structural formula", command=onopen_mic)
    button_calcul.grid(row=3, column=0, sticky='news')
    #bouton valider la sélection    
    button_check=ttk.Button(frame_button, text='Confirm selection', command=onopen_mic)
    button_check.grid(row=2, column=0, sticky='news')
    #bouton lancer le calcul
    button_show_data=ttk.Button(frame_button, text="Show results", command=onopen_mic)
    button_show_data.grid(row=4, column=0, sticky='news')


"""Menu SEM"""

def show_files_project():     #crée une liste déroulante avec tous les fichiers disponibles dans le dossier de travail [create_SEM_project,w_SEM_open]()
    global listbox_files_project
    listbox_files_project = Listbox(tab_menu_SEM)
    listbox_files_project.bind('<ButtonRelease-1>',selection_files)
    listbox_files_project.grid(row=0,column=0,columnspan=2,rowspan=2,sticky="NS"+"EW")

    k=0
    l=1
    while k<len(files_project):
        listbox_files_project.insert(k,files_project[k])
        k=k+1
        l=l+1
def selection_files(e):       #ouvre le fichier dans le dossier parent 
    global extension
    listbox_selection = listbox_files_project.curselection()
    fichier = listbox_files_project.get(listbox_selection)
    extension = os.path.splitext(fichier)
    extension = extension[1]
    os.startfile(project_name+'/'+fichier)
def create_SEM_path():
    global new_project_path
    new_project_path = tkinter.filedialog.askdirectory(title='Select a folder')
    w_SEM_create.configure(background="green")    
def create_SEM_project():
    global files_project,project_name,info_bases_MEB
    project_name = project_SEM_name.get()
    project_name = new_project_path+"/"+project_name
    os.makedirs(project_name)
    if os.path.exists(project_name):
        w_SEM_create.destroy()
    files_project = os.listdir(project_name)
    info_bases_MEB = info_bases_MEB+project_name
    w_SEM()
    show_files_project() 
def w_SEM_create():
    global w_SEM_create,import_SEM_data,create_SEM_project,project_SEM_name,SEM_entry_label
    eval_ = main_w.nametowidget('.').eval
    eval_('tk::PlaceWindow %s center' % main_w)
    w_SEM_create = Toplevel(main_w, bg = "white") 
    w_SEM_create.focus_set()
    w_SEM_create.title("Project")
    w_SEM_create.geometry("%dx%d" % (300,175))
    w_SEM_create.columnconfigure(0,weight=1)
    w_SEM_create.rowconfigure(0,weight=1)
    w_SEM_create.rowconfigure(1,weight=1)
    w_SEM_create.rowconfigure(2,weight=1)
    w_SEM_create.rowconfigure(3,weight=1)
    #Boutons
    import_SEM_path = ttk.Button(w_SEM_create, text="Project Path", command = create_SEM_path,width = 26)
    import_SEM_path.grid(row=2, column=0,columnspan=1, sticky='news')
    import_SEM_path.grid(pady=2,padx=2,ipady=2)
    create_SEM_project = ttk.Button(w_SEM_create, text="Create Project", command = create_SEM_project,width = 26)
    create_SEM_project.grid(row=3, column=0,columnspan=1, sticky='news')
    create_SEM_project.grid(pady=2,padx=2,ipady=2)
    #Entry
    project_SEM_name = ttk.Entry(w_SEM_create,width = 26,justify='center',font=20)
    project_SEM_name.grid(row=1, column=0,ipady=4,pady=2,padx=2,sticky ='news')
    SEM_entry_label = ttk.Label(w_SEM_create,text="Project Name",background="white",font=20)
    SEM_entry_label.grid(row=0, column=0,ipady=4,pady=1,padx=2)
def w_SEM_open():
    global project_name, files_project
    project_name = tkinter.filedialog.askdirectory(title='Select a folder')
    files_project = os.listdir(project_name)
    w_SEM() 
    show_files_project()
def show_main_w_SEM():
    save_data = (metadata.get(1.0,END))
    automatic_data_save = project_name+'/Metadata.txt'
    txt_write_data = open(automatic_data_save, 'w')
    txt_write_data.write(save_data)
    txt_write_data.close()
    SEM_win.destroy()
    main_w.deiconify()   
def w_SEM():
    global SEM_win,tab_menu_SEM,metadata,liste
    print('SEM')
    SEM_win = Toplevel(main_w)
    SEM_win.title("SEM analysis")
    SEM_win.geometry("%dx%d" % (1300, 700))
    SEM_win.configure(bg="white")
    SEM_win.focus_set()
    SEM_win.update()
    main_w.withdraw()
    SEM_win.protocol("WM_DELETE_WINDOW",  show_main_w_SEM)
    SEM_win.rowconfigure(0, weight=0)
    SEM_win.rowconfigure(1, weight=0)
    #Frames
    tab_menu_SEM      = Frame(SEM_win,bg="white",highlightbackground='white')
    tab_menu_SEM.grid(row=1, column=0,columnspan=6,sticky="news")
    tab_georef_SEM    = Frame(SEM_win,bg="white",highlightbackground='white')
    tab_calculate_SEM = Frame(SEM_win,bg="white",highlightbackground='white')
    tab_plot_SEM      = Frame(SEM_win,bg="white",highlightbackground='white') 
    #configure les colonnes et lignes pour que tout reste en place si il y a changement de taille de la fenetre
    
    SEM_win.columnconfigure(0, weight=1)
    SEM_win.columnconfigure(1, weight=1)
    SEM_win.columnconfigure(2, weight=1)
    SEM_win.columnconfigure(3, weight=1)
    SEM_win.columnconfigure(4, weight=1)
    SEM_win.columnconfigure(5, weight=1)
    tab_menu_SEM.columnconfigure(0, weight=1)
    tab_menu_SEM.columnconfigure(1, weight=1)
    tab_menu_SEM.columnconfigure(2, weight=1)
    tab_menu_SEM.columnconfigure(3, weight=1)
    tab_menu_SEM.columnconfigure(4, weight=1)
    tab_menu_SEM.columnconfigure(5, weight=1)
    tab_menu_SEM.rowconfigure(0, weight=0)
    tab_menu_SEM.rowconfigure(1, weight=0)

    def show_menu_SEM():
        tab_calculate_SEM.lower()
        tab_plot_SEM.lower()
        tab_georef_SEM.lower()
        tab_menu_SEM.grid(row=1, column=0,columnspan=6,sticky="news")
    def show_calculate_SEM():
        tab_plot_SEM.lower()
        tab_menu_SEM.lower()
        tab_georef_SEM.lower()
        tab_calculate_SEM.grid(row=1, column=0,columnspan=6,sticky="news")
        tab_calculate_SEM.rowconfigure(0, weight=1)
        tab_calculate_SEM.rowconfigure(1, weight=1)
        tab_calculate_SEM.columnconfigure(0, weight=0)
        tab_calculate_SEM.columnconfigure(1, weight=1)
        tab_calculate_SEM.columnconfigure(2, weight=1)
        tab_calculate_SEM.columnconfigure(3, weight=1)


      
    def show_georef():
        tab_calculate_SEM.lower()
        tab_plot_SEM.lower()
        tab_menu_SEM.lower()
        tab_georef_SEM.grid(row=1, column=0,columnspan=6,sticky="news")
        tab_georef_SEM.rowconfigure(0, weight=1)
        tab_georef_SEM.rowconfigure(1, weight=1)
        tab_georef_SEM.columnconfigure(0, weight=1)
        tab_georef_SEM.columnconfigure(1, weight=8)
        tab_georef_SEM.columnconfigure(2, weight=8)
    
    Frame_bouton_georef=Frame(tab_georef_SEM,background='green',highlightbackground="white")
    Frame_bouton_georef.columnconfigure(0, weight=1)
    Frame_bouton_georef.rowconfigure(0, weight=1)
    Frame_bouton_georef.grid(row=0, column=0,rowspan=2, sticky="news")
    Frame_scan=Frame(tab_georef_SEM,background='red',highlightbackground="white")
    Frame_scan.grid(row=0, column=1,rowspan=2, sticky="news")
    Frame_image1=Frame(tab_georef_SEM,background='blue',highlightbackground="white")
    Frame_image1.grid(row=0, column=2,rowspan=2, sticky="news")
    Frame_image1.columnconfigure(0, weight=1)
    Frame_image1.rowconfigure(0, weight=1)
    Frame_image2=Frame(tab_georef_SEM,background='yellow',highlightbackground="white")
    Frame_image2.grid(row=1, column=2,rowspan=2, sticky="news")
    Frame_scan.rowconfigure(0, weight=1)
    Frame_scan.columnconfigure(0, weight=1)

    def import_scan():            
        def on_canvas_click(event):
    # Clic gauche pour dessiner un point
            if event.num == 1:
                print(f"Point ajouté à la position ({event.x}, {event.y})")
                point_id = canvas1.create_oval(event.x - radius, event.y - radius, event.x + radius, event.y + radius, fill='red')
                points.append(point_id)  # Ajouter l'ID du point à la liste
    # Clic droit pour effacer le point le plus proche
            elif event.num == 3:
                effacer_point_proche(event.x, event.y)

        def effacer_point_proche(x, y):
            for point_id in points:
                # Obtenir les coordonnées du point
                x1, y1, x2, y2 = canvas1.coords(point_id)
                centre_x = (x1 + x2) / 2
                centre_y = (y1 + y2) / 2
                # Vérifier si le clic est à l'intérieur du rayon du point
                if (centre_x - radius <= x <= centre_x + radius) and (centre_y - radius <= y <= centre_y + radius):
                    print(f"Point effacé à la position ({centre_x}, {centre_y})")
                    canvas1.delete(point_id)  # Effacer le point du Canvas
                    points.remove(point_id)  # Enlever le point de la liste
                    break  # Arrêter après avoir effacé le premier point trouvé
            
            
        def ajuster_image(event):
            global photo_image_scan
            if not original_image:  # Vérifier si une image a été chargée
                return
    
            cadre_largeur = Frame_scan.winfo_width()
            cadre_hauteur = Frame_scan.winfo_height()
            img_ratio = original_image.width / original_image.height
            cadre_ratio = cadre_largeur / cadre_hauteur
            if img_ratio > cadre_ratio:
                nouvelle_largeur = cadre_largeur
                nouvelle_hauteur = int(nouvelle_largeur / img_ratio)
            else:
                nouvelle_hauteur = cadre_hauteur
                nouvelle_largeur = int(nouvelle_hauteur * img_ratio)
            nouvelle_image = original_image.resize((nouvelle_largeur, nouvelle_hauteur), Image.Resampling.LANCZOS)
            photo_image_scan = ImageTk.PhotoImage(nouvelle_image)
            x = (cadre_largeur - nouvelle_largeur) // 2
            y = (cadre_hauteur - nouvelle_hauteur) // 2
            canvas1.coords(image_on_canvas, x, y)
            canvas1.itemconfig(image_on_canvas, image=photo_image_scan)
        
        import_scan= filedialog.askopenfilename(title="Ouvrir une image", filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tif *.tiff")])
        original_image = Image.open(import_scan)
        canvas1 = tk.Canvas(Frame_scan)
        canvas1.grid(row=0, column=0, sticky="nsew")
        photo_image = ImageTk.PhotoImage(original_image)
        image_on_canvas = canvas1.create_image(0, 0, anchor='nw', image=photo_image)

        # Associer un gestionnaire d'événement de clic à canvas
        canvas1.bind("<Button-1>", on_canvas_click)  # Bouton gauche
        canvas1.bind("<Button-3>", on_canvas_click)  # Bouton droit

        radius = 5  # Rayon des points dessinés sur le canvas
        points = []  # Liste pour stocker les IDs des points sur le canvas

        Frame_scan.bind("<Configure>", ajuster_image)
        
    def ouvrir_image():
        
        def ajuster_image1(event):
            global photo_image1
            if not original_image1:
                return

            Frame_image1.update_idletasks()  # S'assurer que les mises à jour du Frame sont traitées
            cadre_largeur = Frame_image1.winfo_width()
            cadre_hauteur = Frame_image1.winfo_height()
            
            img_ratio = original_image1.width / original_image1.height
            cadre_ratio = cadre_largeur / cadre_hauteur

            if img_ratio > cadre_ratio:
                nouvelle_largeur = cadre_largeur
                nouvelle_hauteur = int(nouvelle_largeur / img_ratio)
            else:
                nouvelle_hauteur = cadre_hauteur
                nouvelle_largeur = int(nouvelle_hauteur * img_ratio)

            nouvelle_image = original_image1.resize((nouvelle_largeur, nouvelle_hauteur), Image.Resampling.LANCZOS)
            photo_image1 = ImageTk.PhotoImage(nouvelle_image)
            
            x = (cadre_largeur - nouvelle_largeur) // 2
            y = (cadre_hauteur - nouvelle_hauteur) // 2

            canvas_image.coords(image_on_canvas1, x, y)
            canvas_image.itemconfig(image_on_canvas1, image=photo_image1)
            
        import_scan= filedialog.askopenfilename(title="Ouvrir une image", filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tif *.tiff")])
        original_image1 = Image.open(import_scan)
        canvas_image = tk.Canvas(Frame_image1)
        canvas_image.grid(row=0, column=0, sticky="nsew")
        photo_image1 = ImageTk.PhotoImage(original_image1)
        image_on_canvas1 = canvas_image.create_image(0, 0, anchor='nw', image=photo_image1)

        
        Frame_image1.bind("<Configure>", ajuster_image1)

            
    def on_canvas_click2(event):
        print(f"Vous avez cliqué sur la position ({event.x}, {event.y})")
    
    button_import_scan=ttk.Button(Frame_bouton_georef, text="Import Microscope \nScan", command=import_scan)
    button_import_scan.grid(row=0, column=0, sticky='new')
    button_images=ttk.Button(Frame_bouton_georef, text="Import SEM \nImages", command=ouvrir_image)
    button_images.grid(row=1, column=0, sticky='new')



    
    def show_plot_SEM():
        tab_georef_SEM.lower()
        tab_calculate_SEM.lower()
        tab_menu_SEM.lower()
        tab_plot_SEM.grid(row=1, column=0,columnspan=6,sticky="news")
        tab_plot_SEM.rowconfigure(0,weight=1)
        tab_plot_SEM.columnconfigure(0,weight=1)
        tab_plot_SEM.columnconfigure(1,weight=2)
        tab_plot_SEM.columnconfigure(2,weight=2)
        
        
        if control_formule_strcutrale_exist == 1 :
            global ternary_diag,list_poles_topapex,e,e2,ternary_diag_shape,list_poles_bottomleft,index_plot,list_poles_bottomright,select_topapex,select_bottomleft,select_bottomright
            ternary_diag = pd.DataFrame(formule_structurale[1:,1:], index = formule_structurale[1:,0], columns = formule_structurale[0,1:])
            index_plot = formule_structurale[1:,0]
            #liste déroulante Top Apex
            select_topapex=ttk.Combobox(frame_button_plot, values=list_poles_topapex)
            select_topapex.grid(row=1, column=1,sticky='news')
            labeltopapex=ttk.Label(frame_button_plot, text='X or Top apex :',background="white")
            labeltopapex.grid(row=1, column=0,sticky='news')
            
            #liste déroulante bottom left
            select_bottomleft=ttk.Combobox(frame_button_plot, width=16,values=list_poles_bottomleft)
            select_bottomleft.grid(row=2, column=1,sticky='news')
            labelbottomleft=ttk.Label(frame_button_plot, text='Y or Bottom left :',background="white")
            labelbottomleft.grid(row=2, column=0,sticky='news')
            
            #liste déroulante bottom right
            select_bottomright=ttk.Combobox(frame_button_plot, width=16,values=list_poles_bottomright)
            select_bottomright.grid(row=3, column=1,sticky='news')
            labelbottomright=ttk.Label(frame_button_plot, text='Bottom right :',background="white")
            labelbottomright.grid(row=3, column=0,sticky='news')
            
            
            Frame_canvas_plot=Frame(tab_plot_SEM,background='white',highlightbackground="white")
            Frame_canvas_plot.grid(row=0, column=1,columnspan=2, sticky="news")
            Frame_canvas_plot.columnconfigure(0,weight=1)
            Frame_canvas_plot.rowconfigure(0,weight=1)
            canvas = tk.Canvas(Frame_canvas_plot, bg="white")
            canvas.grid(row=0,rowspan=4, column=0,sticky="news")

            # Link a scrollbar to the canvas
            vsb = tk.Scrollbar(Frame_canvas_plot, orient="vertical", command=canvas.yview)
            vsb.grid(row=0,rowspan=4, column=1, sticky='ns')
            hsb = tk.Scrollbar(Frame_canvas_plot, orient="horizontal", command=canvas.xview)
            hsb.grid(row=2, column=0, sticky='we')
            canvas.configure(yscrollcommand=vsb.set)
            canvas.configure(xscrollcommand=hsb.set)

            frame_entry = Frame(canvas, bg="white")
            frame_entry.grid(row=0, column=0, sticky='news')
            frame_entry.columnconfigure(0,weight=1)
            frame_entry.columnconfigure(1,weight=1)
            frame_entry.columnconfigure(2,weight=1)
            canvas.create_window((0, 0), window=frame_entry, anchor='center')
            ternary_diag_shape = ternary_diag.shape
            
            k=0
            l=1
            label_e = np.empty((ternary_diag_shape[0],1))
            label_e_text = (np.arange((ternary_diag_shape[0])))
            e       = np.empty((ternary_diag_shape[0],1),dtype=object)
            e2      = np.empty((ternary_diag_shape[0],1),dtype=object)
            while k < ternary_diag_shape[0]:
                value_l = str(l)
                e2[k,0]="e2"+value_l
                e[k,0]="e"+value_l
                l=l+1
                k=k+1
            k=0   
            while k < ternary_diag_shape[0]:
                label_e = ttk.Label(frame_entry,text = index_plot[k],background="white",font=20)
                label_e.grid(row=1+k,column = 0)
                e[k,0] = ttk.Entry(frame_entry,justify='center')
                e[k,0].grid(row=1+k,column = 1,sticky="ew")
                e2[k,0] = ttk.Entry(frame_entry,justify='center')
                e2[k,0].grid(row=1+k,column = 2,sticky="ew")
                k=k+1
            label_e_title = ttk.Label(frame_entry,text = 'Colour',background="white",justify='center',font=20)
            label_e_title.grid(row=0,column = 1)
            label_e_title2 = ttk.Label(frame_entry,text = 'Symbol',background="white",justify='center',font=20)
            label_e_title2.grid(row=0,column = 2)
            frame_entry.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))
            
            fenetre3_legend = Frame(Frame_canvas_plot,bg="white",highlightbackground='white')
            fenetre3_legend.grid(row=0,column=2,sticky='news')
            label_colour_legend = ttk.Label(fenetre3_legend, text = 'Colour',justify='left',anchor='nw',width=20,font=20,background="white")
            label_colour_legend.grid(row = 0, column = 0)
            label_colour_legend = ttk.Label(fenetre3_legend, text = 'Marker',justify='left',anchor='nw',width=20,font=20,background="white")
            label_colour_legend.grid(row = 0, column = 1)
            label_blue = ttk.Label(fenetre3_legend, text = '1 : Blue',justify='left',anchor='nw',width=20,font=20,background="white")
            label_blue.grid(row = 1, column = 0)
            label_red = ttk.Label(fenetre3_legend, text = '2 : Red',justify='left',anchor='nw',width=20,font=20,background="white")
            label_red.grid(row = 2, column = 0)
            label_green = ttk.Label(fenetre3_legend, text = '3 : Green',justify='left',anchor='nw',width=20,font=20,background="white")
            label_green.grid(row = 3, column = 0)
            label_yellow = ttk.Label(fenetre3_legend, text = '4 : Yellow',justify='left',anchor='nw',width=20,font=20,background="white")
            label_yellow.grid(row = 4, column = 0)
            label_orange = ttk.Label(fenetre3_legend, text = '5 : orange',justify='left',anchor='nw',width=20,font=20,background="white")
            label_orange.grid(row = 5, column = 0)
            label_magenta = ttk.Label(fenetre3_legend, text = '6 : Magenta',justify='left',anchor='nw',width=20,font=20,background="white")
            label_magenta.grid(row = 6, column = 0)
            label_black = ttk.Label(fenetre3_legend, text = '7 : Black',justify='left',anchor='nw',width=20,font=20)
            label_black.grid(row = 7, column = 0)
    
    
            label_circle = ttk.Label(fenetre3_legend, text = '1 : Circle',justify='left',anchor='nw',width=20,font=20,background="white")
            label_circle.grid(row = 1, column = 1)
            label_square = ttk.Label(fenetre3_legend, text = '2 : Square',justify='left',anchor='nw',width=20,font=20,background="white")
            label_square.grid(row = 2, column = 1)
            label_diamond = ttk.Label(fenetre3_legend, text = '3 : Diamond',justify='left',anchor='nw',width=20,font=20,background="white")
            label_diamond.grid(row = 3, column = 1)
            label_cross = ttk.Label(fenetre3_legend, text = '4 : Cross',justify='left',anchor='nw',width=20,font=20,background="white")
            label_cross.grid(row = 4, column = 1)
            label_x = ttk.Label(fenetre3_legend, text = '5 : X',justify='left',anchor='nw',width=20,font=20,background="white")
            label_x.grid(row = 5, column = 1)
            label_triangle_up = ttk.Label(fenetre3_legend, text = '6 : Triangle',justify='left',anchor='nw',width=20,font=20,background="white")
            label_triangle_up.grid(row = 6, column = 1)
            label_star = ttk.Label(fenetre3_legend, text = '7 : Star',justify='left',anchor='nw',width=20,font=20,background="white")
            label_star.grid(row = 7, column = 1)
        

    def save_formule_structurale():
        SAVE_formule=tkinter.filedialog.asksaveasfile(title="Save as...",filetypes=[('CSV files','.csv')],defaultextension = ".txt") 
        save_formule_structurale = pd.DataFrame(formule_structurale[1:,1:], index = formule_structurale[1:,0], columns = formule_structurale[0,1:])
        save_formule_structurale.to_csv(SAVE_formule)
    def import_SEM_data():
        global dossier_a_importer,files_project
        dossier_a_importer=tkinter.filedialog.askdirectory(title='Select a folder')
        files_dossier_source = os.listdir(dossier_a_importer)
        shutil.copytree(dossier_a_importer,project_name+"/"+"Folder 1")
        for i in files_dossier_source :
            os.rename(project_name+"/"+"Folder 1"+"/"+ i, project_name +"/"+ i)  
        shutil.rmtree(project_name+"/"+"Folder 1")
        files_project = os.listdir(project_name)
        show_files_project()
    
    bouton_main_show1 = ttk.Button(SEM_win, text="HOME", command = show_main_w_SEM)
    bouton_main_show1.grid(row=0, column=0,ipady=0,sticky="news")
    bouton_georef_SEM   = ttk.Button(SEM_win, text="Georeferencement", command = show_georef)
    bouton_georef_SEM.grid(row=0, column=3,ipady=0,sticky="news")
    bouton_import_SEM   = ttk.Button(SEM_win, text="Import data", command = import_SEM_data)
    bouton_import_SEM.grid(row=0, column=1,ipady=0,sticky="news")
    bouton_menu_SEM   = ttk.Button(SEM_win, text="Meta-data", command = show_menu_SEM)
    bouton_menu_SEM.grid(row=0, column=2,ipady=0,sticky="news")
    bouton_calculate_SEM = ttk.Button(SEM_win, text="APFU", command = show_calculate_SEM)
    bouton_calculate_SEM.grid(row=0, column=4,ipady=0,sticky="news")
    bouton_plot_SEM = ttk.Button(SEM_win, text="Plots", command = show_plot_SEM)
    bouton_plot_SEM.grid(row=0, column=5,ipady=0,sticky="news")
    metadata = tk.Text(tab_menu_SEM, wrap='word')
    metadata.grid(row=1, column=2,rowspan=1,columnspan=4,sticky="ew"+"ns")
    label_SEM_date = ttk.Label(tab_menu_SEM, text = 'Metadata (automatically saved in the parent folder)',justify='center',anchor='s',background="white")
    label_SEM_date.grid(row=0, column=2,rowspan=1,columnspan=4,sticky="ew"+"ns")
    #Images EDS
    fig2_frame = Frame(tab_calculate_SEM,bg="white",highlightbackground='white')
    fig2_frame.grid(row=0,column=1,sticky='news')
    figure2 = plt.Figure( facecolor='white')
    canvas2 = FigureCanvasTkAgg(figure2, fig2_frame)
    canvas2.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
    ax2 = figure2.add_subplot(1,1,1) 
    ax2.axes.get_xaxis().set_visible(False) #supprime les axes
    ax2.axes.get_yaxis().set_visible(False)
    # creating the Matplotlib toolbar
    toolbar2 = NavigationToolbar2Tk(canvas2,fig2_frame)
    toolbar2.update()
    
    
    
    
    #Créer le fichier de métadonnées .txt dans le dossier parent si il n'existe pas.
    name_of_metadata = project_name + '/Metadata.txt'
    print(os.path.exists(name_of_metadata))
    if  os.path.exists(name_of_metadata)  is True :
        reader_acces = open(name_of_metadata, 'r')
        liste = reader_acces.read()
        metadata.insert(tk.END,liste)
    else : 
        
        metadata.insert(tk.END,info_bases_MEB)
             
    def points_images_EDS():     
        global name_fichier_base,fichier_coord_points,fichier_image_points,Check_button,var                      
        dossier_EDS =tkinter.filedialog.askdirectory(title='Select a folder') 
        files_os = os.listdir(dossier_EDS)    
        button_open_eds_folder.destroy()
        
        def adjust_canvas(event):
            canvas_width = frame_entry.winfo_reqwidth()
            canvas.itemconfig(frame_id, width=canvas_width)
            canvas.configure(scrollregion=canvas.bbox("all"), width=canvas_width)
        frame_listbox = tk.Frame(tab_calculate_SEM, bg="white", highlightbackground='white')
        frame_listbox.grid(row=0, column=0, sticky='nsew')
        frame_listbox.grid_rowconfigure(0, weight=1)
        frame_listbox.grid_columnconfigure(0, weight=1)
        canvas = tk.Canvas(frame_listbox, bg="white", highlightthickness=0)
        canvas.grid(row=0, column=0, sticky="nsew")
    
        vsb = tk.Scrollbar(frame_listbox, orient="vertical", command=canvas.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        canvas.configure(yscrollcommand=vsb.set)

        frame_entry = tk.Frame(canvas, bg="white")
        frame_id = canvas.create_window((0, 0), window=frame_entry, anchor='nw')

        frame_entry.bind("<Configure>", adjust_canvas)

        button_open_folder_EDS = ttk.Button(frame_entry, text="Folder")
        button_open_folder_EDS.grid(row=0, column=0, sticky='nsew')

        #cette partie récupère les dossiers de sortie EDS_MEB
        matches_P_S       = np.array([match for match in files_os if ".PS.EDS" in match])        #donne tous les fichiers d'analyses disponibles dans le dossier EDS du MEB
        k=0
        name_fichier_base    = np.empty(len(matches_P_S), dtype=object)
        fichier_coord_points = np.empty(len(matches_P_S), dtype=object)
        fichier_image_points = np.empty(len(matches_P_S), dtype=object)
        name_check_box       = np.empty(len(matches_P_S), dtype=object)
        extension_coord_points = '.p_s'
        extension_image_points = '.psref'
        while k < len(matches_P_S):
            name_fichier_base[k] = dossier_EDS+'/'+matches_P_S[k]
            split_func = matches_P_S[k].split('.')
            name_check_box[k] = split_func[0]
            fichier_coord_points[k] = '/' +split_func[0] + extension_coord_points
            fichier_image_points[k] = '/' +split_func[0] + extension_image_points
            k=k+1
        var= IntVar()
        Check_button = np.empty(len(matches_P_S), dtype=object)
        k=0
        while k < len(matches_P_S):
            Check_button= ttk.Checkbutton(frame_entry,text=name_check_box[k],variable=var,onvalue=[k],command=show_EDS_image,style='white.TCheckbutton')
            Check_button.grid(row=k+1, column=0)
            k=k+1   
        frame_entry.update_idletasks()

        
    #permet d'afficher l'image EDS + points
    def show_EDS_image():    
        global coord_points, choice_base,img_EDS, user_base_choice
        user_base_choice = var.get()   #index de name_fichier_base
        choice_base = np.where(name_fichier_base==name_fichier_base[user_base_choice]) #renvois l'index de la base qu'on veut
        choice_base = int(choice_base[0])
        directory   = name_fichier_base[user_base_choice]
        ax2.clear()  
        image_file_directory = directory+fichier_coord_points[choice_base]
        img_file_directory = directory+fichier_image_points[choice_base]
        with open (image_file_directory) as f :
            image_reader         = csv.reader(f, delimiter = ',')
            convert_image_reader = list(image_reader)
        numb_of_points = int(np.array(convert_image_reader[2])) #récupère le nombre de points d'analyses sur une image
        k = 0
        coord_points= np.zeros((numb_of_points, 4))
        while k < numb_of_points :                                  #récupère les coordonnées des points d'analyse EDS
            l = 5+3*k                                               #index 
            coord_points[k] = convert_image_reader[l]
            k = k+1
        coord_points = np.delete(coord_points, [2,3], axis = 1)
        img_EDS = plt.imread(img_file_directory)                    #Lecture de l'image
        ax2.scatter(coord_points[:,0],coord_points[:,1], c='red')   # ajoute les points d'analyses
        k = 0
        while k < numb_of_points :     #ajoute les nombres des points
            l = 1+k
            ax2.text(coord_points[k,0]+8,coord_points[k,1],l, c='red')
            k = k+1
        ax2.imshow(img_EDS)
        canvas2.draw()
    button_open_eds_folder=ttk.Button(tab_calculate_SEM,text="Open EDS folder", command=points_images_EDS)
    button_open_eds_folder.grid(row=0, column=0,sticky='news')
    
    canvas2.toolbar = toolbar2
        
    def on_canvas_click(event):
        global index_point
        if event.inaxes is not None:  # Ensure the click is within the axes of the plot
            click_x, click_y = event.xdata, event.ydata
            tolerance = 20  # Set the tolerance level here

            # Check if coord_points is defined and accessible
            if 'coord_points' in globals():
                for index, (px, py) in enumerate(coord_points):
                    if abs(click_x - px) <= tolerance and abs(click_y - py) <= tolerance:
                        print(f"Point {index + 1} clicked!")
                        index_point = index
                        open_eds_file()
                        break
                    
    
    canvas2.mpl_connect('button_press_event', on_canvas_click)

    def open_eds_file():
        def read_psmas_file(filepath):
            global metadata
            metadata = {}
            spectrum = []

            with open(filepath, 'r') as file:
                data_section = False
                for line in file:
                    line = line.strip()
                    if line.startswith('#'):
                        if line.startswith('#SPECTRUM'):
                            data_section = True
                            continue
                        if data_section:
                            continue
                        key_value = line[1:].split(':')
                        if len(key_value) > 1:
                            key, value = key_value[0].strip(), key_value[1].strip()
                            if key in metadata:
                                if isinstance(metadata[key], list):
                                    metadata[key].append(value)
                                else:
                                    metadata[key] = [metadata[key], value]
                            else:
                                metadata[key] = value
                    else:
                        if data_section:
                            parts = line.split(',')
                            if len(parts) == 3:
                                energy, intensity = float(parts[0].strip()), float(parts[1].strip())
                                spectrum.append((energy, intensity))
            
            return metadata, spectrum

        def extract_peak_elements(metadata):
            peak_elements = []
            if '#PEAKLAB' in metadata:
                for item in metadata['#PEAKLAB']:
                    parts = item.split()
                    if len(parts) >= 2:
                        number = parts[0]
                        element = parts[1]
                        peak_elements.append((float(number), element))
            return peak_elements

        def extract_quant_data(metadata):
            quant_data = {}
            if '#QUANT_WTCON' in metadata and '#QUANT_ATCON' in metadata:
                for wt, at in zip(metadata['#QUANT_WTCON'], metadata['#QUANT_ATCON']):
                    parts_wt = wt.split()
                    parts_at = at.split()
                    element = parts_wt[0]
                    wt_percent = parts_wt[1]
                    atom_conc = parts_at[1]
                    quant_data[element] = (wt_percent, atom_conc)
            return quant_data

        def plot_spectrum_with_table(spectrum, peak_elements, quant_data):
            energies, intensities = zip(*spectrum)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            fig.canvas.manager.set_window_title(f'Point {index_point + 1}')
            ax.plot(energies, intensities, linestyle='-')
            ax.set_title('Spectrum Energy vs Intensity')
            ax.set_xlabel('Energy (keV)')
            ax.set_ylabel('Intensity (Counts)')
            ax.grid(True)
            
            # Ajouter des barres verticales et annoter avec le nom des éléments
            for number, element in peak_elements:
                ax.axvline(x=number, color='r', linestyle='--')
                ax.text(number, max(intensities) * 0.9, element, rotation=45, verticalalignment='bottom', horizontalalignment='right')

            # Créer un tableau à côté du graphique
            cell_text = []
            columns = ['Elements', 'Wt %', 'Atom Conc']
            for element, (wt, at) in quant_data.items():
                cell_text.append([element, wt, at])

            table = plt.table(cellText=cell_text, colLabels=columns, loc='right', cellLoc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(8)
            table.scale(0.55, 1.0)

            plt.subplots_adjust(right=0.7)  # Ajuster pour donner de l'espace au tableau
            plt.show()


        match = re.search(r'\((\d+)\)', name_fichier_base[choice_base])
        numero = match.group(1)
        metadata, spectrum = read_psmas_file(name_fichier_base[choice_base]+"/Base("+str(numero)+")_pt"+str(index_point+1)+".psmsa")
        peak_elements = extract_peak_elements(metadata)
        quant_data = extract_quant_data(metadata)
        
        plot_spectrum_with_table(spectrum, peak_elements, quant_data)





    
    
    
    # fonctions d'ouverture de csv EDS_MEB (monomineral)
    def onopen():
        global access,affichage_chemical_data,chemical_data_size, chemical_data,Sum_Total_recalc, chemical_data_num,chemical_data_brut, tab_ref_red, tab_ref_size, Oxy_architecture, option_minerals_list, tab_minerals,formule_structurale_shape
        FILE = askopenfilename(title="Select a file",filetypes=[('CSV FILES','*.csv')])    
        access = FILE
        with open(access, 'r') as reader_access :
            reader_access  = csv.reader(reader_access, delimiter = ',')
            convert_access = list(reader_access)
            chemical_data  = np.array(reader_access)
        liste = convert_access
        n = len(max(liste, key=len))
        liste_2 = [x + [None]*(n-len(x)) for x in liste]
        chemical_data = np.array(liste_2)
        pos_weight = np.where(chemical_data=='Weight Concentration %')
        pos_weight = int(pos_weight[0])
        pos_atom   = np.where(chemical_data=='Atom Concentration %')
        pos_atom   = int(pos_atom[0])
        chemical_data = chemical_data[(pos_weight+1):(pos_atom-2),:-1]
        chemical_data[chemical_data == '  '] = 0                                           #remplace les valeurs vides par des 0
        chemical_data2 = pd.DataFrame(chemical_data[:,:],columns=chemical_data[0,:])
        chemical_data2 = chemical_data2[sorted(chemical_data2.columns)] 
        chemical_data2.to_csv('chemical_data.csv',sep = ';')
        with open('chemical_data.csv', 'r') as reader_chemical_data :
            reader_chemical_data  = csv.reader(reader_chemical_data, delimiter = ';')
            convert_chemical_data = list(reader_chemical_data)
            chemical_data  = np.array(convert_chemical_data)
        chemical_data = chemical_data[1:,1:]
        column_shape = np.shape(chemical_data)
        column_shape = column_shape[1]
        k=0
        while k < column_shape :
            chemical_data[0,k] = chemical_data[0,k][2:]
            k=k+1
        for i in chemical_data :
            if 'C' in chemical_data :                                                    #lance le recalcule des wght% si il y a un carbone dans le tableau
                 del_carbon         = np.where(chemical_data=='C')                       #cherche la position de la colonne du carbonne
                 chemical_data      = np.delete(chemical_data, del_carbon[1], axis = 1)  #supprime la colonne du carbone
                 chemical_data_num  = chemical_data[1::,1:-1]                            #prends que les données numériques du chemical_data
                 chemical_data_num  = np.array(chemical_data_num).astype(float)          #transforme les données en float
                 Sum_Total_recalc   = chemical_data_num.sum(axis = 1)                    #fait la somme des colonnes 
                 Sum_Total_recalc   = np.reshape(Sum_Total_recalc,(len(Sum_Total_recalc),1))
                 chemical_data_num  = chemical_data_num*100/Sum_Total_recalc             #recalcul la proportion d'élements sans le carbone
            if 'C' not in chemical_data :
                chemical_data_num = (chemical_data[1:,1:-1]).astype(float)              #si il n'y a pas de C remet juste en forme le tableau
        chemical_data_brut = chemical_data[:,:-1]                                        #garde un fichier brut non modifié
        chemical_data_size=np.shape(chemical_data)
        #Importation et réduction du tableau périodique
        tab_ref = pd.read_csv('table_ref_chemical_elements.csv', sep = ';', engine = 'python')
        for i in tab_ref :                                                                   #pour tous les élements dans tab_ref                                                           
            index_chemical_data_tab_ref = tab_ref.columns.searchsorted(chemical_data[0,:])   #rechercher les valeurs qui correspondent à la première ligne de chemical_data
        tab_ref_red   = tab_ref.iloc[:,index_chemical_data_tab_ref]                          #selectionne seulement les colonnes utiles
        tab_ref_red   = np.array(tab_ref_red)                                                #transforme en format numpy
        tab_ref_size  = tab_ref_red.shape                                                    #prend la dimension de tab_ref_red
        tab_ref_size  = tab_ref_size[1]                                                      #prend le  nombre de colonnes de tab_ref_red

    #fonctions d'ouverture de csv EDS_MEB (polymineral)
    def onopen_choice_minerals():
        global access,affichage_chemical_data,Saisie,chemical_data_size, chemical_data,Sum_Total_recalc, chemical_data_num,chemical_data_brut, tab_ref_red, tab_ref_size, Oxy_architecture, option_minerals_list, tab_minerals
        FILE = askopenfilename(title="Select a file",filetypes=[('CSV FILES','*.csv')])    
        access = FILE
        def adjust_canvas(event):
    
            canvas_width = frame_entry_fen1.winfo_reqwidth()
            canvas_fen1.itemconfig(frame_id, width=canvas_width)  # Adjust width of canvas window
            canvas_fen1.configure(scrollregion=canvas_fen1.bbox("all"), width=canvas_width)



        canvas_fen1 = tk.Canvas(fenetre1_1, bg="white", highlightthickness=0)
        canvas_fen1.grid(row=0, column=0, rowspan=2, sticky="nsew")

        vsb_fen1 = tk.Scrollbar(fenetre1_1, orient="vertical", command=canvas_fen1.yview)
        vsb_fen1.grid(row=0, column=1, sticky='ns')
        canvas_fen1.configure(yscrollcommand=vsb_fen1.set)

        frame_entry_fen1 = tk.Frame(canvas_fen1, bg="white")
        frame_id = canvas_fen1.create_window((0, 0), window=frame_entry_fen1, anchor='nw')

        frame_entry_fen1.bind("<Configure>", lambda event, canvas=canvas_fen1: adjust_canvas(event))

        frame_entry_fen1.grid_columnconfigure(0, weight=0)
        frame_entry_fen1.grid_columnconfigure(1, weight=0)



        with open(access, 'r') as reader_access :
            reader_access  = csv.reader(reader_access, delimiter = ',')
            convert_access = list(reader_access)
            chemical_data  = np.array(reader_access)
        liste = convert_access
        n = len(max(liste, key=len))
        liste_2 = [x + [None]*(n-len(x)) for x in liste]
        chemical_data = np.array(liste_2)
        pos_weight = np.where(chemical_data=='Weight Concentration %')
        pos_weight = int(pos_weight[0])
        pos_atom   = np.where(chemical_data=='Atom Concentration %')
        pos_atom   = int(pos_atom[0])
        chemical_data = chemical_data[(pos_weight+1):(pos_atom-2),:-1]
        chemical_data[chemical_data == '  '] = 0                                           #remplace les valeurs vides par des 0
        chemical_data2 = pd.DataFrame(chemical_data[:,:],columns=chemical_data[0,:])
        chemical_data2 = chemical_data2[sorted(chemical_data2.columns)] 
        chemical_data2.to_csv('chemical_data.csv',sep = ';')
        with open('chemical_data.csv', 'r') as reader_chemical_data :
            reader_chemical_data  = csv.reader(reader_chemical_data, delimiter = ';')
            convert_chemical_data = list(reader_chemical_data)
            chemical_data  = np.array(convert_chemical_data)
        chemical_data = chemical_data[1:,1:]
        column_shape = np.shape(chemical_data)
        column_shape = column_shape[1]
        k=0
        while k < column_shape :
            chemical_data[0,k] = chemical_data[0,k][2:]
            k=k+1
        for i in chemical_data :
            if 'C' in chemical_data :                                                    #lance le recalcule des wght% si il y a un carbone dans le tableau
                 del_carbon         = np.where(chemical_data=='C')                       #cherche la position de la colonne du carbonne
                 chemical_data      = np.delete(chemical_data, del_carbon[1], axis = 1)  #supprime la colonne du carbone
                 chemical_data_num  = chemical_data[1::,1:-1]                            #prends que les données numériques du chemical_data
                 chemical_data_num  = np.array(chemical_data_num).astype(float)          #transforme les données en float
                 Sum_Total_recalc   = chemical_data_num.sum(axis = 1)                    #fait la somme des colonnes 
                 Sum_Total_recalc   = np.reshape(Sum_Total_recalc,(len(Sum_Total_recalc),1))
                 chemical_data_num  = chemical_data_num*100/Sum_Total_recalc             #recalcul la proportion d'élements sans le carbone
            if 'C' not in chemical_data :
                chemical_data_num = (chemical_data[1:,1:-1]).astype(float)              #si il n'y a pas de C remet juste en forme le tableau
        chemical_data_brut = chemical_data[:,:-1]                                        #garde un fichier brut non modifié
        chemical_data_size=np.shape(chemical_data)
        temp_var=str
        list_points = chemical_data[:,0]
        list_finale = np.empty((chemical_data_size[0],1),dtype='U25')
        k=0
        while k <chemical_data_size[0]:
            if k==0 : 
                list_finale[k,0]=" "
            else :
                temp_var = list_points[k]
                base_num_temp = temp_var[6]
                pt_temp = temp_var[9:]
                list_finale[k,0] = 'b' + base_num_temp + pt_temp
            k=k+1
        #Importation et réduction du tableau périodique
        tab_ref = pd.read_csv('table_ref_chemical_elements.csv', sep = ';', engine = 'python')
        for i in tab_ref :                                                                   #pour tous les élements dans tab_ref                                                           
            index_chemical_data_tab_ref = tab_ref.columns.searchsorted(chemical_data[0,:])   #rechercher les valeurs qui correspondent à la première ligne de chemical_data
        tab_ref_red   = tab_ref.iloc[:,index_chemical_data_tab_ref]                          #selectionne seulement les colonnes utiles
        tab_ref_red   = np.array(tab_ref_red)                                                #transforme en format numpy
        tab_ref_size  = tab_ref_red.shape                                                    #prend la dimension de tab_ref_red
        tab_ref_size  = tab_ref_size[1]                                                      #prend le  nombre de colonnes de tab_ref_red
        #crée des possibilités de selection pour chaque point d'analyse
        Saisie = np.full((2,chemical_data_size[0]),"            ", dtype = object)
        mineral_list2=option_minerals_list
        for i in range (2):
            ttk.Label(frame_entry_fen1,text="Minerals",borderwidth=1,relief="solid",width=10,font=("Arial, 12"),background="white").grid(column=1,row=0,sticky="news")
            Saisie[i][0]=" Mineral%s "%i
            for i in range (chemical_data_size[0]):
                frame_entry_fen1.grid_rowconfigure(i, weight=1)
                ttk.Label(frame_entry_fen1,text=list_finale[i,0],borderwidth=1,relief="solid",font=("Arial, 12"),background="white").grid(column=0,row=i,sticky="news")
                Saisie[0][i]=list_finale[i,0]
                for i in range (1,2):
                    for j in range (1, chemical_data_size[0]):
                        Saisie[i][j]=StringVar()
                        Saisie[i][j]=ttk.Combobox(frame_entry_fen1,values=mineral_list2)
                        Saisie[i][j].grid(column=1,row=j,sticky="news")
        frame_entry_fen1.update_idletasks()
        canvas_fen1.config(scrollregion=canvas_fen1.bbox("all"))
    #recupère le nombre d'oxygène (polymineral)
    def Selected_elem():
         global Saisie,Oxy_architecture,mineral,Mineral_type
         for i in range (1,2):
             for j in range (1,chemical_data_size[0]):
                 Saisie[i][j]=Saisie[i][j].get()
         minerals2 = Saisie[1,1:chemical_data_size[0]]   
         minerals2 = minerals2.tolist()
         Oxy_architecture = np.empty((chemical_data_size[0]-1,1), dtype = int)
         Mineral_type     = np.empty((chemical_data_size[0]-1,1), dtype = int)
         k=0
         index_min_list=np.empty((chemical_data_size[0]-1,1), dtype = int)
         while k<len(minerals2) :
             index_min_list[k,0]= option_minerals_list.index(minerals2[k])
             Oxy_architecture[k,0] = int(tab_minerals[1,index_min_list[k,0]+1])
             Mineral_type[k,0]     = (tab_minerals[2,index_min_list[k,0]+1])
             k=k+1
         mineral ="No mineral" #nécessaire pour bloquer un if dans le calcul des formules structurales
         
    #recupère le nombre d'oxygène (monomineral)
    def check_min():
        global mineral, mineral_pos, mineral_choice,Oxy_architecture, tab_minerals, Mineral_type
        check=mb.askquestion(title='Selection', message=f'Do you want select {select_mineral.get()} ? ')
        if check=='yes' :
            mineral               = select_mineral.get()
            mineral_choice        = option_minerals_list.index(mineral)
            Oxy_architecture      = np.empty((chemical_data_size[0]-1,1), dtype = int)
            Oxy_architecture[:,0] = int(tab_minerals[1,mineral_choice+1])
            Mineral_type          = np.empty((chemical_data_size[0]-1,1),dtype = int)
            k=0
            while k < chemical_data_size[0]-1 :
                Mineral_type[k,0]          = tab_minerals[2,mineral_choice+1]
                k=k+1
        else : 
            mb.showinfo(title='Choice', message='Please select an other mineral !')  
    
    #fonction pour calculer les formules strucurales MEB (monomineral)
    def calcul_MEB_silicates():
            global formule_structurale,M_elements,formule_structurale_shape,control_formule_strcutrale_exist,list_poles_topapex,list_poles_bottomleft,list_poles_bottomright
            #Calcul APFU silicates
            if Mineral_type[0,0] == 1 :
                M_elements       = np.reshape(tab_ref_red[0,1:-1],(1,tab_ref_size-2))              #masse molaire des élements
                pos_O            = np.where(chemical_data=='O')                               #cherche la posititon de 'O'
                pos_O            = pos_O[1]-1
                for i in chemical_data_num :
                    chemical_data_num_atom = chemical_data_num/M_elements                               #calcul la proportion de cations n =m/M
                oxygene          = chemical_data_num_atom[:,pos_O]                                      #copie la colonne O
                chemical_data_num_atom_size      = chemical_data_num_atom.shape
                chemical_data_num_atom_size_index = chemical_data_num_atom_size[0]
                nb_cations = np.zeros((chemical_data_num_atom_size[0],chemical_data_num_atom_size[1]))  #prépare une matrice de même taille que chemical_data_num
                k = 0                                                                                   #initialisation boucle
                while k < chemical_data_num_atom_size_index :                                           #pour toutes les lignes k
                    for i in chemical_data_num_atom[k,:] :                                              #lit pour i tous les élements de la ligne k
                        nb_cations[k,:] = chemical_data_num_atom[k,:]*(Oxy_architecture[k,0]/oxygene[k,0])   #calcul final
                    k = k+1                                                                             #pas de la boucle
                nb_cations = np.round(nb_cations,decimals=2)
                chemical_data_brut_size = chemical_data_brut.shape
                size_headers_cols  = chemical_data_brut_size[1]
                size_headers_index = chemical_data_brut_size[0]
                headers_cols  = np.reshape((chemical_data_brut[0,1:]), (1,size_headers_cols-1))
                headers_index = np.reshape((chemical_data_brut[:,0]), (size_headers_index,1))
                formule_structurale = np.concatenate((headers_cols,nb_cations), axis = 0)               #restructure le fichier final
                formule_structurale = np.concatenate((headers_index,formule_structurale), axis = 1)
                #calcul de l'éléctoneutralité
                # nb_charges = nb_cations*tab_ref_red[1,1:-1]
                # charges_positives = np.delete(nb_charges, pos_O, axis = 1)
                # charges_positives = np.sum(charges_positives, axis = 1)
                # charges_positives = np.reshape(charges_positives,(chemical_data_num_atom_size_index,1))
                # charges_negatives = nb_charges[:,pos_O]
                # deficit_charges   = charges_negatives - charges_positives
                # k = 0
                # while k < chemical_data_num_atom_size_index :
                #     if deficit_charges[k,:] > 0 :
                #         pos_Fe     = np.where(chemical_data=='Fe')
                #         pos_Fe     = pos_Fe[1]-1
                #         nb_cations[k,pos_Fe] = nb_cations[k,pos_Fe] - deficit_charges[k,:]
                #         if nb_cations[k,pos_Fe] < 0 :
                #             nb_cations[k,pos_Fe] = 0
                #     else :
                #         pos_Fe     = np.where(chemical_data=='Fe')
                #         pos_Fe     = pos_Fe[1]-1
                #         deficit_charges[k,:]=0
                #     k = k+1
                # nb_cations      = np.insert(nb_cations,pos_Fe+1,deficit_charges,axis = 1)
                # k = 0
                # while k < chemical_data_num_atom_size_index :
                #     if nb_cations[k,pos_Fe+1] <= 0 :
                #         nb_cations[k,pos_Fe+1] = 0
                #     k = k+1
                # nb_cations = np.round(nb_cations,decimals=3)
                # headers_cols = np.insert(headers_cols,pos_Fe+1,'Fe3+',axis = 1)
                # formule_structurale = np.concatenate((headers_cols,nb_cations), axis = 0)               #restructure le fichier final
                # formule_structurale = np.concatenate((headers_index,formule_structurale), axis = 1)
                #écriture des formules structurales
                #cas des plagioclases 
                # if mineral == "Plagioclase" :
                #     nb_cations_round = np.around(nb_cations, decimals = 2)
                #     pos_Si = np.where(formule_structurale=='Si')
                #     pos_Si = pos_Si[1]-1   
                #     pos_O  = np.where(formule_structurale=='O')
                #     pos_O  = pos_O[1]-1
                #     pos_Al = np.where(formule_structurale=='Al')
                #     pos_Al = pos_Al[1]-1
                #     pos_Na = np.where(formule_structurale=='Na')
                #     pos_Na = pos_Na[1]-1
                #     pos_Ca = np.where(formule_structurale=='Ca')
                #     pos_Ca = pos_Ca[1]-1
                #     pos_K  = np.where(formule_structurale=='K')
                #     pos_K  = pos_K[1]-1
                #     k = 0
                #     formule = np.empty((chemical_data_num_atom_size_index,1), dtype=object)
                #     while k < chemical_data_num_atom_size_index :
                #         ValueSi = str(nb_cations_round[k,pos_Si])
                #         ValueSi = ValueSi[1:-1]
                #         ValueO  = str(nb_cations_round[k,pos_O])
                #         ValueO = ValueO[1:-1]
                #         ValueAl = str(nb_cations_round[k,pos_Al])
                #         ValueAl = ValueAl[1:-1]
                #         ValueNa = str(nb_cations_round[k,pos_Na])
                #         ValueNa = ValueNa[1:-1]
                #         ValueCa = str(nb_cations_round[k,pos_Ca])
                #         ValueCa = ValueCa[1:-1]
                #         ValueK  = str(nb_cations_round[k,pos_K])
                #         ValueK = ValueK[1:-1]
                #         formule[k,:] = "K"+ValueK+"Na"+ValueNa+"Ca"+ValueCa+"Al"+ValueAl+"[Si"+ValueSi+"O"+ValueO+"]"
                #         k = k+1
                #     header_formule = np.empty((1,1), dtype=object)
                #     header_formule[0,0] = "Formule_structurale"
                #     formule = np.concatenate((header_formule,formule), axis = 0)
                #     formule_structurale = np.concatenate((formule_structurale,formule), axis = 1)
                #     if pos_Si.size == 0 :
                #         formule_structurale = np.delete(formule_structurale, (-1), axis = 1)
                #     if pos_O.size == 0 :
                #         formule_structurale = np.delete(formule_structurale, (-1), axis = 1)
                #     if pos_Al.size == 0 :
                #         formule_structurale = np.delete(formule_structurale, (-1), axis = 1)
                #     if pos_Na.size == 0 :
                #         formule_structurale = np.delete(formule_structurale, (-1), axis = 1)
                #     if pos_Ca.size == 0 :
                #         formule_structurale = np.delete(formule_structurale, (-1), axis = 1)
                #     if pos_K.size == 0 :
                #         formule_structurale = np.delete(formule_structurale, (-1), axis = 1)
                formule_structurale_shape = np.shape(formule_structurale)
                control_formule_strcutrale_exist = 1
                #pour les diagrammes ternaires
                list_poles = formule_structurale[0,:]
                list_poles = list_poles.tolist()   
                if ('Formule_structurale' in formule_structurale) == True :
                    del list_poles[-1]
                if ('' in formule_structurale) == True :
                    del list_poles[0] 
                list_poles_topapex     = list_poles
                list_poles_bottomright = list_poles
                list_poles_bottomleft  = list_poles
                #Enregistrement des données de sortie dans le dossier du projet 
                automatic_save = project_name+'/formule_structurale.csv'
                save_formule_structurale = pd.DataFrame(formule_structurale[1:,1:], index = formule_structurale[1:,0], columns = formule_structurale[0,1:])
                save_formule_structurale.to_csv(automatic_save) #enregistre les données
            #calcul APFU pour carbonates
            if Mineral_type[0,0] == 2 :
                Carbone_architecture = Oxy_architecture/3 
                chemical_data_num_size = chemical_data_num.shape
                chemical_data_num_size_cols = chemical_data_num_size[1]
                chemical_data_num_size = chemical_data_num_size[0]
                M_elements       = np.reshape(tab_ref_red[0,1:-1],(1,tab_ref_size-2))              #masse molaire des élements
                pos_O            = np.where(chemical_data=='O')                               #cherche la posititon de 'O'
                pos_O            = pos_O[1]
                chemical_data_num_atom = np.empty((chemical_data_num_size,chemical_data_num_size_cols), dtype = object)
                k=0
                while k < chemical_data_num_size :
                    chemical_data_num_atom[k,:] = chemical_data_num[k,:]/M_elements[0,:]                                #calcul la proportion de cations n =m/M
                    k=k+1
                oxygene          = chemical_data_num_atom[:,pos_O-1]
                chemical_data_num_atom_size      = chemical_data_num_atom.shape
                chemical_data_num_atom_size_index = chemical_data_num_atom_size[0]
                nb_cations = np.zeros((chemical_data_num_atom_size[0],chemical_data_num_atom_size[1]))  #prépare une matrice de même taille que chemical_data_num
                k = 0                                                                                   #initialisation boucle
                while k < chemical_data_num_atom_size_index :                                           #pour toutes les lignes k
                    for i in chemical_data_num_atom[k,:] :                                              #lit pour i tous les élements de la ligne k
                        nb_cations[k,:] = chemical_data_num_atom[k,:]*(Oxy_architecture[k,0]/oxygene[k,0])   #calcul final
                    k = k+1                                                                             #pas de la boucle
                chemical_data_brut_size = chemical_data_brut.shape
                size_headers_cols  = chemical_data_brut_size[1]
                size_headers_index = chemical_data_brut_size[0]
                headers_cols  = np.reshape((chemical_data_brut[0,1:]), (1,size_headers_cols-1))
                headers_index = np.reshape((chemical_data_brut[:,0]), (size_headers_index,1))
                colonne_carbone = np.empty((chemical_data_num_size+1,1),dtype=object)
                colonne_carbone[0,0]='C'
                colonne_carbone[1:,0]=Carbone_architecture[:,0]
                formule_structurale = np.concatenate((headers_cols,nb_cations), axis = 0)               #restructure le fichier final
                formule_structurale = np.concatenate((colonne_carbone,formule_structurale), axis = 1)
                formule_structurale = np.concatenate((headers_index,formule_structurale), axis = 1)
                formule_structurale_shape = np.shape(formule_structurale)
                control_formule_strcutrale_exist = 1
                #préparation diagrammes ternaires
                list_poles = formule_structurale[0,:]
                list_poles = list_poles.tolist()   
                if ('Formule_structurale' in formule_structurale) == True :
                    del list_poles[-1]
                if ('' in formule_structurale) == True :
                    del list_poles[0]
                list_poles_topapex     = list_poles
                list_poles_bottomright = list_poles
                list_poles_bottomleft  = list_poles
                #enregistrement automatique dans le projet
                automatic_save = project_name+'/formule_structurale.csv'
                save_formule_structurale = pd.DataFrame(formule_structurale[1:,1:], index = formule_structurale[1:,0], columns = formule_structurale[0,1:])
                save_formule_structurale.to_csv(automatic_save) #enregistre les données
    
    
    def calcul_MEB_silicates_poly():
            global formule_structurale,M_elements,Carbone_architecture,formule_structurale_shape,control_formule_strcutrale_exist,list_poles_topapex,list_poles_bottomleft,list_poles_bottomright
            #Calcul APFU silicates
            M_elements       = np.reshape(tab_ref_red[0,1:-1],(1,tab_ref_size-2))
            pos_O            = np.where(chemical_data=='O')                               
            pos_O            = pos_O[1]-1
            Carbone_architecture = np.zeros((len(Mineral_type),1),dtype=int)
            
            
            k=0 
            while k < len(Mineral_type) : 
                if Mineral_type[k]==2:
                    Carbone_architecture[k,0] = Oxy_architecture[k]/3 
                else :
                    Carbone_architecture[k,0] = 0
                k=k+1
            
            chemical_data_num_size = chemical_data_num.shape
            chemical_data_num_size_cols = chemical_data_num_size[1]
            chemical_data_num_size = chemical_data_num_size[0]
            colonne_carbone = np.empty((chemical_data_num_size+1,1),dtype=object)
            colonne_carbone[0,0]='C'
            colonne_carbone[1:,0]=Carbone_architecture[:,0]

            

            for i in chemical_data_num :
                    chemical_data_num_atom = chemical_data_num/M_elements                               #calcul la proportion de cations n =m/M
            oxygene          = chemical_data_num_atom[:,pos_O]                                      #copie la colonne O
            chemical_data_num_atom_size      = chemical_data_num_atom.shape
            chemical_data_num_atom_size_index = chemical_data_num_atom_size[0]
            nb_cations = np.zeros((chemical_data_num_atom_size[0],chemical_data_num_atom_size[1]))  #prépare une matrice de même taille que chemical_data_num
            k = 0                                                                                   #initialisation boucle
            while k < chemical_data_num_atom_size_index :                                           #pour toutes les lignes k
                for i in chemical_data_num_atom[k,:] :                                              #lit pour i tous les élements de la ligne k
                    nb_cations[k,:] = chemical_data_num_atom[k,:]*(Oxy_architecture[k,0]/oxygene[k,0])   #calcul final
                k = k+1                                                                             #pas de la boucle
            nb_cations = np.round(nb_cations,decimals=2)
            chemical_data_brut_size = chemical_data_brut.shape
            size_headers_cols  = chemical_data_brut_size[1]
            size_headers_index = chemical_data_brut_size[0]
            headers_cols  = np.reshape((chemical_data_brut[0,1:]), (1,size_headers_cols-1))
            headers_index = np.reshape((chemical_data_brut[:,0]), (size_headers_index,1))
            
            formule_structurale = np.concatenate((headers_cols,nb_cations), axis = 0)               #restructure le fichier final
            formule_structurale = np.concatenate((headers_index,formule_structurale), axis = 1)
            formule_structurale = np.concatenate((formule_structurale,colonne_carbone), axis = 1)
            formule_structurale_shape = np.shape(formule_structurale)
            
            
            control_formule_strcutrale_exist = 1
                
                
            #pour les diagrammes ternaires
            list_poles = formule_structurale[0,:]
            list_poles = list_poles.tolist()   
            if ('Formule_structurale' in formule_structurale) == True :
                    del list_poles[-1]
            if ('' in formule_structurale) == True :
                    del list_poles[0] 
            list_poles_topapex     = list_poles
            list_poles_bottomright = list_poles
            list_poles_bottomleft  = list_poles
            #Enregistrement des données de sortie dans le dossier du projet 
            automatic_save = project_name+'/formule_structurale.csv'
            save_formule_structurale = pd.DataFrame(formule_structurale[1:,1:], index = formule_structurale[1:,0], columns = formule_structurale[0,1:])
            save_formule_structurale.to_csv(automatic_save) #enregistre les données
            #calcul APFU pour carbonates
            #if Mineral_type[0,0] == 2 :
                
               
               
                
               
    #crée l'onglet avec mono ou polymineral
    tabControl = ttk.Notebook(tab_calculate_SEM)
    tabControl.grid(row=0,column=2,rowspan=1,sticky="news")
    tab1 = Frame(tabControl,bg="white",highlightbackground='white')
    tab2 = Frame(tabControl,bg="white",highlightbackground='white')
    tabControl.add(tab1, text ='Mono mineral')
    tabControl.add(tab2, text ='Poly mineral')
    tab1.grid_rowconfigure(0, weight=1)
    tab1.grid_rowconfigure(1, weight=1)
    tab1.grid_rowconfigure(2, weight=1)
    tab1.grid_rowconfigure(3, weight=1)
    tab1.grid_rowconfigure(4, weight=1)
    tab1.grid_rowconfigure(5, weight=1)
    tab1.grid_rowconfigure(6, weight=1)
    tab1.grid_columnconfigure(0, weight=1)
    tab2.grid_columnconfigure(0, weight=1)
    tab2.grid_rowconfigure(0, weight=1)
    tab2.grid_rowconfigure(1, weight=1)
    tab2.grid_rowconfigure(2, weight=1)
    tab2.grid_rowconfigure(3, weight=1)
    tab2.grid_rowconfigure(4, weight=1)
    #fenetre pour choisir le minéral pour poly
    fenetre1_1 = Frame(tab_calculate_SEM,bg="white",highlightbackground='white')
    fenetre1_1.grid(row=0,column=3,rowspan=1,sticky="news")
    fenetre1_1.grid_rowconfigure(0, weight=1)
    fenetre1_1.grid_columnconfigure(0, weight=1)
    fenetre1_1.grid_columnconfigure(1, weight=0)

    select_mineral=ttk.Combobox(tab1, textvariable=option_minerals_list,font=16)
    select_mineral['values']=option_minerals_list
    select_mineral.grid(column=0, row=2, sticky='news')
    label=ttk.Label(tab1, text='Please select a mineral :',background="white",font=16)
    label.grid(column=0, row=1, sticky='ew')  
    button_save = ttk.Button(tab1,text="Save as", command=save_formule_structurale, width = 10)
    button_save.grid(row=6, column=0,sticky="news")
    button_save2 = ttk.Button(tab2,text="Save as", command=save_formule_structurale, width = 10)
    button_save2.grid(row=4, column=0,sticky="news")
    #fenetre pour visualiser le résultat du calcul
    fenetre2 = Frame(tab_calculate_SEM,bg="white",highlightbackground='white')
    fenetre2.grid(row=3,column=0,columnspan=4,rowspan=3,sticky="news")
    fenetre2.grid_rowconfigure(0, weight=1)
    fenetre2.grid_columnconfigure(0, weight=1)
    #ouverture d'un tableau numpy dans Tk 
    def show_formule_structurale():
        canvas = tk.Canvas(fenetre2, bg="white",highlightbackground='white')
        canvas.grid(row=0, column=0, sticky="news")
        # Link a scrollbar to the canvas
        vsb = tk.Scrollbar(fenetre2, orient="vertical", command=canvas.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        hsb = tk.Scrollbar(fenetre2, orient="horizontal", command=canvas.xview)
        hsb.grid(row=1, column=0, sticky='we')
        canvas.configure(yscrollcommand=vsb.set)
        canvas.configure(xscrollcommand=hsb.set)
        frame_entry = Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=frame_entry, anchor='nw')
        formule_structurale_shape_index = formule_structurale_shape[0]
        formule_structurale_shape_col = formule_structurale_shape[1]
        rows = []
        for i in range(formule_structurale_shape_index):
            cols = []
            for j in range(formule_structurale_shape_col):
                e = ttk.Entry(frame_entry,justify='center')
                e.grid(row=i, column=j)
                e.insert(0, formule_structurale[i][j])
                e.configure(state="readonly")
                cols.append(e)
            rows.append(cols)
        frame_entry.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        
    #Monomineral
    button_open=ttk.Button(tab1,text="Open SEM file...", command=onopen)
    button_open.grid(row=0, column=0, sticky='news')
    #bouton lancer le calcul
    button_calcul=ttk.Button(tab1,text="Calcul structural formula", command=calcul_MEB_silicates)
    button_calcul.grid(row=4, column=0, sticky='news')
    #bouton valider la sélection    
    button_check=ttk.Button(tab1, text='Confirm selection', command=check_min)
    button_check.grid(row=3, column=0, sticky='news')
    #polymineral
    button_open_poly=ttk.Button(tab2,text="Open EDS file...", command=onopen_choice_minerals)
    button_open_poly.grid(row=0, column=0, sticky='news')
    #bouton lancer le calcul
    button_calcul_poly=ttk.Button(tab2,text="Calcul structural formula", command=calcul_MEB_silicates_poly)
    button_calcul_poly.grid(row=2, column=0, sticky='news')
    button_check_poly=ttk.Button(tab2, text='Confirm selection', command=Selected_elem)
    button_check_poly.grid(row=1, column=0, sticky='news')    
    button_show_data_poly=ttk.Button(tab2, text="Show results", command=show_formule_structurale)
    button_show_data_poly.grid(row=3, column=0, sticky='news')
    button_show_data=ttk.Button(tab1, text="Show results", command=show_formule_structurale)
    button_show_data.grid(row=5, column=0, sticky='news')

    #Ternary plots 
    #importation des données
    
    frame_button_plot = Frame(tab_plot_SEM,background='white')
    frame_button_plot.columnconfigure(0,weight=1)
    frame_button_plot.columnconfigure(1,weight=1)
    frame_button_plot.grid(row=0,column=0, sticky='news')

    
    def import_data():
        global ternary_diag,list_poles_topapex,convert_import_data,e,e2,ternary_diag_shape,list_poles_bottomleft,index_plot,list_poles_bottomright,select_topapex,select_bottomleft,select_bottomright,control_formule_strcutrale_exist
        import_data_ternary = askopenfilename(title="Select a file",filetypes=[('CSV FILES','*.csv')])    
        import_data = import_data_ternary
        with open(import_data, 'r') as reader_import_data :
            reader_import_data = csv.reader(reader_import_data, delimiter = ',')
            convert_import_data = list(reader_import_data)
            import_formule_data = np.asarray(convert_import_data)
        list_poles = import_formule_data[0,:]
        list_poles = list_poles.tolist()   
        if ('Formule_structurale' in import_formule_data) == True :
            del list_poles[-1]
            import_formule_data = import_formule_data[:,:-1] 
        if ('' in import_formule_data) == True :
            del list_poles[0]
        index_plot = import_formule_data[1:,0]    
        ternary_diag = pd.DataFrame(import_formule_data[1:,1:], index = import_formule_data[1:,0], columns = import_formule_data[0,1:])   #met en format pandas avec la première ligne et colonne de formule_structural en header
        
        list_poles_topapex     = list_poles[:]
        list_poles_bottomright = list_poles[:]
        list_poles_bottomleft  = list_poles[:]
        #liste déroulante Top Apex
        select_topapex=ttk.Combobox(frame_button_plot, values=list_poles_topapex)
        select_topapex.grid(row=1, column=1,sticky='news')
        labeltopapex=ttk.Label(frame_button_plot, text='X or Top apex :',background="white",font=20)
        labeltopapex.grid(row=1, column=0,sticky='news')
        
        #liste déroulante bottom left
        select_bottomleft=ttk.Combobox(frame_button_plot, width=16,values=list_poles_bottomleft)
        select_bottomleft.grid(row=2, column=1,sticky='news')
        labelbottomleft=ttk.Label(frame_button_plot, text='Y or Bottom left :',background="white",font=20)
        labelbottomleft.grid(row=2, column=0,sticky='news')
        
        #liste déroulante bottom right
        select_bottomright=ttk.Combobox(frame_button_plot, width=16,values=list_poles_bottomright)
        select_bottomright.grid(row=3, column=1,sticky='news')
        labelbottomright=ttk.Label(frame_button_plot, text='Bottom right :',background="white",font=20)
        labelbottomright.grid(row=3, column=0,sticky='news')
        
        
        Frame_canvas_plot=Frame(tab_plot_SEM,background='white',highlightbackground="white")
        Frame_canvas_plot.grid(row=0, column=1,columnspan=2, sticky="news")
        Frame_canvas_plot.columnconfigure(0,weight=1)
        Frame_canvas_plot.rowconfigure(0,weight=1)
        canvas = tk.Canvas(Frame_canvas_plot, bg="white")
        canvas.grid(row=0,rowspan=4, column=0,sticky="news")

        # Link a scrollbar to the canvas
        vsb = tk.Scrollbar(Frame_canvas_plot, orient="vertical", command=canvas.yview)
        vsb.grid(row=0,rowspan=4, column=1, sticky='ns')
        hsb = tk.Scrollbar(Frame_canvas_plot, orient="horizontal", command=canvas.xview)
        hsb.grid(row=2, column=0, sticky='we')
        canvas.configure(yscrollcommand=vsb.set)
        canvas.configure(xscrollcommand=hsb.set)

        frame_entry = Frame(canvas, bg="white")
        frame_entry.grid(row=0, column=0, sticky='news')
        frame_entry.columnconfigure(0,weight=1)
        frame_entry.columnconfigure(1,weight=1)
        frame_entry.columnconfigure(2,weight=1)
        canvas.create_window((0, 0), window=frame_entry, anchor='center')
        ternary_diag_shape = ternary_diag.shape
        
        k=0
        l=1
        label_e = np.empty((ternary_diag_shape[0],1))
        label_e_text = (np.arange((ternary_diag_shape[0])))
        e       = np.empty((ternary_diag_shape[0],1),dtype=object)
        e2      = np.empty((ternary_diag_shape[0],1),dtype=object)
        while k < ternary_diag_shape[0]:
            value_l = str(l)
            e2[k,0]="e2"+value_l
            e[k,0]="e"+value_l
            l=l+1
            k=k+1
        k=0   
        while k < ternary_diag_shape[0]:
            label_e = ttk.Label(frame_entry,text = index_plot[k],background="white",font=20)
            label_e.grid(row=1+k,column = 0)
            e[k,0] = ttk.Entry(frame_entry,justify='center')
            e[k,0].grid(row=1+k,column = 1,sticky="ew")
            e2[k,0] = ttk.Entry(frame_entry,justify='center')
            e2[k,0].grid(row=1+k,column = 2,sticky="ew")
            k=k+1
        label_e_title = ttk.Label(frame_entry,text = 'Colour',background="white",justify='center',font=20)
        label_e_title.grid(row=0,column = 1)
        label_e_title2 = ttk.Label(frame_entry,text = 'Symbol',background="white",justify='center',font=20)
        label_e_title2.grid(row=0,column = 2)
        frame_entry.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        
        fenetre3_legend = Frame(Frame_canvas_plot,bg="white",highlightbackground='white')
        fenetre3_legend.grid(row=0,column=2,sticky='news')
        label_colour_legend = ttk.Label(fenetre3_legend, text = 'Colour',justify='left',anchor='nw',width=20,font=20,background="white")
        label_colour_legend.grid(row = 0, column = 0)
        label_colour_legend = ttk.Label(fenetre3_legend, text = 'Marker',justify='left',anchor='nw',width=20,font=20,background="white")
        label_colour_legend.grid(row = 0, column = 1)
        label_blue = ttk.Label(fenetre3_legend, text = '1 : Blue',justify='left',anchor='nw',width=20,font=20,background="white")
        label_blue.grid(row = 1, column = 0)
        label_red = ttk.Label(fenetre3_legend, text = '2 : Red',justify='left',anchor='nw',width=20,font=20,background="white")
        label_red.grid(row = 2, column = 0)
        label_green = ttk.Label(fenetre3_legend, text = '3 : Green',justify='left',anchor='nw',width=20,font=20,background="white")
        label_green.grid(row = 3, column = 0)
        label_yellow = ttk.Label(fenetre3_legend, text = '4 : Yellow',justify='left',anchor='nw',width=20,font=20,background="white")
        label_yellow.grid(row = 4, column = 0)
        label_orange = ttk.Label(fenetre3_legend, text = '5 : orange',justify='left',anchor='nw',width=20,font=20,background="white")
        label_orange.grid(row = 5, column = 0)
        label_magenta = ttk.Label(fenetre3_legend, text = '6 : Magenta',justify='left',anchor='nw',width=20,font=20,background="white")
        label_magenta.grid(row = 6, column = 0)
        label_black = ttk.Label(fenetre3_legend, text = '7 : Black',justify='left',anchor='nw',width=20,font=20)
        label_black.grid(row = 7, column = 0)


        label_circle = ttk.Label(fenetre3_legend, text = '1 : Circle',justify='left',anchor='nw',width=20,font=20,background="white")
        label_circle.grid(row = 1, column = 1)
        label_square = ttk.Label(fenetre3_legend, text = '2 : Square',justify='left',anchor='nw',width=20,font=20,background="white")
        label_square.grid(row = 2, column = 1)
        label_diamond = ttk.Label(fenetre3_legend, text = '3 : Diamond',justify='left',anchor='nw',width=20,font=20,background="white")
        label_diamond.grid(row = 3, column = 1)
        label_cross = ttk.Label(fenetre3_legend, text = '4 : Cross',justify='left',anchor='nw',width=20,font=20,background="white")
        label_cross.grid(row = 4, column = 1)
        label_x = ttk.Label(fenetre3_legend, text = '5 : X',justify='left',anchor='nw',width=20,font=20,background="white")
        label_x.grid(row = 5, column = 1)
        label_triangle_up = ttk.Label(fenetre3_legend, text = '6 : Triangle',justify='left',anchor='nw',width=20,font=20,background="white")
        label_triangle_up.grid(row = 6, column = 1)
        label_star = ttk.Label(fenetre3_legend, text = '7 : Star',justify='left',anchor='nw',width=20,font=20,background="white")
        label_star.grid(row = 7, column = 1)
        
        
        
        control_formule_strcutrale_exist = 1
    
    def plot_ternary():
        global Top_apex,Bottom_left,Bottom_right
        
        if control_formule_strcutrale_exist != 1 : 
            mb.showinfo(title='Warning', message='No data imported') 
            
        list_marker = []
        list_color = []
        list_marker = [1]*ternary_diag_shape[0]
        list_color = [1]*ternary_diag_shape[0]
        k=0
        while k < ternary_diag_shape[0]:
            list_marker[k] = e2[k,0].get()
            list_color[k] = e[k,0].get()
            k= k+1
        if list_marker[0] == "" :
            list_marker = [1]*ternary_diag_shape[0]
            list_color = [1]*ternary_diag_shape[0]
        
        Top_apex     = select_topapex.get()       #pôle haut du dT
        Bottom_left  = select_bottomleft.get()       #bas gauche
        Bottom_right = select_bottomright.get()       #bas droite
        
        symbols = ['circle', 'square', 'diamond', 'cross',"x","triangle-up","star",]
        colors = ['blue','red','green','yellow','orange','magenta','black']
        ternary_diag['Marker']=list_marker
        ternary_diag['Color'] =list_color
        if Bottom_right != "" :
            fig_ternary  = px.scatter_ternary(ternary_diag, a = Top_apex, b = Bottom_left, c = Bottom_right,hover_data = ["Color", "Marker"],
                    symbol = ternary_diag['Marker'],symbol_sequence=symbols, color_discrete_sequence = colors,color =  ternary_diag['Color'])                                  #crée le diagramme ternaire avec les 3 pôles 
            fig_ternary.write_html('tmp.html', auto_open=True)
            filename_svg = project_name+'/Ternary_Diagram.svg'   
            fig_ternary.write_image(filename_svg,format="svg", engine="kaleido")
        else :
            fig_binary = px.scatter(ternary_diag,x=Top_apex,y=Bottom_left,hover_data = ["Color", "Marker"],
                    symbol = ternary_diag['Marker'],symbol_sequence=symbols, color_discrete_sequence = colors,color =  ternary_diag['Color'])
            fig_binary.write_html('tmp.html', auto_open=True)
            filename_svg_bi = project_name+'/Binary_Diagram.svg'   
            fig_binary.write_image(filename_svg_bi,format="svg", engine="kaleido")
             
        
    
    
    
    
    #plots
    button_import_SEM_APFU = ttk.Button(frame_button_plot,text="Import APFU file",command=import_data)
    button_import_SEM_APFU.grid(row=0,column=0,columnspan=2, sticky="ew")
    button_import_SEM_APFU = ttk.Button(frame_button_plot,text="Plot",command=plot_ternary)
    button_import_SEM_APFU.grid(row=4,column=0,columnspan=2, sticky="ew")
    
"""Menu transferts de masse"""   

def w_massbalance():
    main_w.destroy()
    mass_w = Tk()
    mass_w.title("HOME")
    mass_w.geometry("%dx%d" % (400, 300))
    mass_w.configure(bg="white")
    mass_w.focus_set()
    mass_w.update()
    print('mass')

"""Menu ACP"""

def w_PCA():
    main_w.destroy()
    stable_w = Tk()
    stable_w.title("HOME")
    stable_w.geometry("%dx%d" % (400, 300))
    stable_w.configure(bg="white")
    stable_w.focus_set()
    stable_w.update()
    print('PCA')

"""Création des différents boutons amenant aux différents menus"""    

def destroy_boutton():
    global bouton_main_w1_1,bouton_main_w1_2,bouton_main_w2,bouton_main_w3,bouton_main_w4
    bouton_main_w1.destroy()
    bouton_main_w2.destroy()
    bouton_main_w3.destroy()
    bouton_main_w4.destroy()
def main_w1():
    global bouton_main_w1_1,bouton_main_w1_2,bouton_main_w2,bouton_main_w3,bouton_main_w4,bouton_main_w2_1,bouton_main_w2_2
    destroy_boutton()
    if "bouton_main_w2_1"in locals():
        bouton_main_w2_1.destroy()
        bouton_main_w2_2.destroy()
    bouton_main_w1_1 = ttk.Button(main_w, text="New SEM Project", command = w_SEM_create,style='small_font.TButton',width = 17)
    bouton_main_w1_1.grid(row=0, column=0,sticky='nsew')
    bouton_main_w1_2 = ttk.Button(main_w, text="Existing SEM Project", command = w_SEM_open,style='small_font.TButton',width = 17)
    bouton_main_w1_2.grid(row=0, column=1,sticky='nsew')
    bouton_main_w2 = ttk.Button(main_w, text="Microprobe", command = main_w2,style='Custom.TButton',width = 35)
    bouton_main_w2.grid(row=1, column=0,columnspan=2, sticky='nsew',pady=1,padx=2)
    bouton_main_w3 = ttk.Button(main_w, text="Mass Balance", command = main_w3,style='Custom.TButton',width = 35)
    bouton_main_w3.grid(row=2, column=0,columnspan=2, sticky='nsew',pady=1,padx=2)
    bouton_main_w4 = ttk.Button(main_w, text="PCA", command = main_w4,style='Custom.TButton',width = 35)
    bouton_main_w4.grid(row=3, column=0,columnspan=2, sticky='nsew',pady=1,padx=2)
    main_w.update()
def main_w2():
    global bouton_main_w1_1,bouton_main_w1_2,bouton_main_w2,bouton_main_w3,bouton_main_w4,bouton_main_w2_1,bouton_main_w2_2
    destroy_boutton()
    if "bouton_main_w1_1"in locals():
        bouton_main_w1_1.destroy()
        bouton_main_w1_2.destroy()
    bouton_main_w1 = ttk.Button(main_w, text="SEM", command = main_w1,style='Custom.TButton',width = 35)
    bouton_main_w1.grid(row=0, column=0,columnspan=2, sticky='nsew')
    bouton_main_w2_1 = ttk.Button(main_w, text="New EPMA Project", command = w_MIC_create,style='small_font.TButton',width = 17)
    bouton_main_w2_1.grid(row=1, column=0,sticky='nsew')
    bouton_main_w2_2 = ttk.Button(main_w, text="Existing EPMA Project", command = w_MIC_open,style='small_font.TButton',width = 17)
    bouton_main_w2_2.grid(row=1, column=1,sticky='nsew')
    bouton_main_w3 = ttk.Button(main_w, text="Mass Balance", command = main_w3,style='Custom.TButton',width = 35)
    bouton_main_w3.grid(row=2, column=0,columnspan=2, sticky='nsew',pady=1,padx=2)
    bouton_main_w4 = ttk.Button(main_w, text="PCA", command = main_w4,style='Custom.TButton',width = 35)
    bouton_main_w4.grid(row=3, column=0,columnspan=2, sticky='nsew',pady=1,padx=2)
    main_w.update()
def main_w3():
    global bouton_main_w1_1,bouton_main_w1_2,bouton_main_w2,bouton_main_w3,bouton_main_w4
    destroy_boutton()
    if "bouton_main_w1_1"in globals():
        bouton_main_w1_1.destroy()
        bouton_main_w1_2.destroy()
    if "bouton_main_w2_1"in globals():
        bouton_main_w2_1.destroy()
        bouton_main_w2_2.destroy()
    bouton_main_w1 = ttk.Button(main_w, text="SEM", command = main_w1,style='Custom.TButton',width = 35)
    bouton_main_w1.grid(row=0, column=0,columnspan=2, sticky='nsew',pady=1,padx=2)
    bouton_main_w2 = ttk.Button(main_w, text="Microprobe", command = main_w2,style='Custom.TButton',width = 35)
    bouton_main_w2.grid(row=1, column=0,columnspan=2, sticky='nsew',pady=1,padx=2)
    bouton_main_w3 = ttk.Button(main_w, text="Mass Balance", command = w_massbalance,width = 35)
    bouton_main_w3.grid(row=2, column=0,columnspan=2, sticky='nsew',pady=1,padx=2)
    bouton_main_w4 = ttk.Button(main_w, text="PCA-", command = w_PCA,style='Custom.TButton',width = 35)
    bouton_main_w4.grid(row=3, column=0,columnspan=2, sticky='nsew',pady=1,padx=2)
    main_w.update()
def main_w4():
    global bouton_main_w1_1,bouton_main_w1_2,bouton_main_w2,bouton_main_w3,bouton_main_w4
    destroy_boutton()
    if "bouton_main_w1_1"in globals():
        bouton_main_w1_1.destroy()
        bouton_main_w1_2.destroy()
    if "bouton_main_w2_1"in globals():
        bouton_main_w2_1.destroy()
        bouton_main_w2_2.destroy()
    bouton_main_w1 = ttk.Button(main_w, text="SEM", command = main_w1,style='Custom.TButton',width = 35)
    bouton_main_w1.grid(row=0, column=0,columnspan=2, sticky='nsew',pady=1,padx=2)
    bouton_main_w2 = ttk.Button(main_w, text="Microprobe", command = main_w2,style='Custom.TButton',width = 35)
    bouton_main_w2.grid(row=1, column=0,columnspan=2, sticky='nsew',pady=1,padx=2)
    bouton_main_w3 = ttk.Button(main_w, text="Mass Balance", command = w_massbalance,style='Custom.TButton',width = 35)
    bouton_main_w3.grid(row=2, column=0,columnspan=2, sticky='nsew',pady=1,padx=2)
    bouton_main_w4 = ttk.Button(main_w, text="PCA", command = w_PCA,width = 35)
    bouton_main_w4.grid(row=3, column=0,columnspan=2, sticky='nsew',pady=1,padx=2)
    main_w.update()

"""création de la fenetre principale"""
#fenetre
main_w = Tk()
main_w.title("HOME")
main_w.geometry("%dx%d" % (500, 400))
main_w.configure(bg="white")
main_w.focus_set()
main_w.columnconfigure(0, weight=1)
main_w.columnconfigure(1, weight=1)
main_w.rowconfigure(0, weight=1)
main_w.rowconfigure(1, weight=1)
main_w.rowconfigure(2, weight=1)
main_w.rowconfigure(3, weight=1)
main_w.update()
eval_ = main_w.nametowidget('.').eval
eval_('tk::PlaceWindow %s center' % main_w)

#boutons
bouton_main_w1 = ttk.Button(main_w, text="SEM", command = main_w1)
bouton_main_w1.grid(row=0, column=0,columnspan=2, sticky='nsew',pady=1,padx=2,ipady=18)
bouton_main_w2 = ttk.Button(main_w, text="Microprobe", command = main_w2)
bouton_main_w2.grid(row=1, column=0,columnspan=2, sticky='nsew',pady=1,padx=2,ipady=18)
bouton_main_w3 = ttk.Button(main_w, text="Mass Balance", command = w_massbalance)
bouton_main_w3.grid(row=2, column=0,columnspan=2, sticky='nsew',pady=1,padx=2,ipady=18)
bouton_main_w4 = ttk.Button(main_w, text="PCA", command = w_PCA)
bouton_main_w4.grid(row=3, column=0,columnspan=2, sticky='nsew',pady=1,padx=2,ipady=18)
main_w.update()
#création des styles
style = ttk.Style()
#style.theme_use('xpnative')
style.configure('TButton', background = 'white', foreground = 'black', borderwidth=2, focusthickness=3, focuscolor='none',font=(None, 16),justify='center',anchor='center')
style.configure('TLabel', background = 'white', foreground = 'black')
style.configure('white.TCheckbutton', foreground='black', background = 'white')
style2 = ttk.Style()
style2.configure('Custom.TButton', background = 'grey', foreground = 'grey', borderwidth=2, focusthickness=3, focuscolor='none',font=(None, 16))
style3 = ttk.Style()
style3.configure('small_font.TButton', background = 'white', foreground = 'black', borderwidth=2, focusthickness=3, focuscolor='none',font=(None, 12))

    
def on_close():
     close = messagebox.askokcancel("Close", "Would you like to close the program?")
     if close:
          main_w.destroy()
main_w.protocol("WM_DELETE_WINDOW",  on_close)
main_w.mainloop()






















