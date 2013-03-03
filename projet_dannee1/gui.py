import Tkinter as tk
from draughtsFunctions import *
import tkMessageBox
from config import *


class Root:
  def __init__(self):
    """Creation de la fenetre principale."""
    self.body=tk.Tk()

  def setTitle(self,title):
    """ Ajout du titre dans la fenetre"""
    self.body.title(title)


class Label:
  def __init__(self,parent,text,anchor,variable=True,int=False):
    if(variable):
        self.label=tk.Label(parent,textvariable=text,anchor=anchor)
    else:
        self.label=tk.Label(parent,text=text,anchor=anchor)

  def configLabel(self,borderwidth,width,relief):
    self.label.config(borderwidth=borderwidth,width=width,relief=relief)

  def gridLabel(self,column,row):
    self.label.grid(column=column,row=row)


class Frame:
  
  def __init__(self,root):
    """Cree une fenetre secondaire.

    Arguments:
       root(instance):la fenetre principale.   
    """
    self.frame=tk.Frame(root)#creation d'une petite fenetre dans root

  def gridFrame(self,column,row,columnspan,rowspan):
    self.frame.grid(column=column,row=row,columnspan=columnspan,rowspan=rowspan)


  
  def createGrid(self,val_plateau,col,row,columnspan,rowspan,anchor,relief,borderwidth,width):
    """ Cree un plateau de jeu en fonction des valeurs presentes dans val_plateau
       val_plateau(list):la liste de listes de StringVar.
       col(int):la colonne dans root, entre 0 et 14.
       row(int):la ligne dans root, entre 0 et 14.
       columnspan(int):le nombre de colonnes que prend l'objet.
       rowspan(int):le nombre de lignes que prend l'objet.
    """
    for i in range(DIMENSION):
      for j in range(DIMENSION):
        label=Label(self.frame,val_plateau[i][j],anchor)
        label.configLabel(borderwidth,width,relief)
        label.gridLabel(j,i)

class ValBoard:

  def __init__(self,board):
    """ Cree le plateau logique pour l'interface
        Arguments:
       plateau(list):la liste contenant 15 listes de 15 elements."""
    self.body=[]
    for i in range(DIMENSION):
        self.body.append([])
        for j in range(DIMENSION):
            val=tk.StringVar()
            self.body[i].append(val)
            self.body[i][j].set(board[i][j])
            #attribue une valeur au StringVar

class Button:
    def __init__(self):
        self.body=



def create_variabletext_intlabel(root,col,row):
    """Cree un label a texte variable en IntVar.

    Arguments:
       root(instance):la fenetre principale.
       col(int):la colonne dans root, entre 0 et 14.
       row(int):la ligne dans root, entre 0 et 14.

    Valeurs de retour:
       instance. Retourne un IntVar associe a un label.
       instance. Retourne un label a texte variable.
    """   
    val=tk.IntVar()
    label=tk.Label(root,textvariable=val)#cree un label
    label.grid(column=col,row=row)#place le label dans le fenetre root
    return val, label

def creation_button(root,text,command,col,row):
    """Cree les boutons.

    Arguments:
       root(instance):la fenetre principale.
       text(str):le texte sur le bouton.
       command(function):la commande du bouton.
       col(int):la colonne dans root, entre 0 et 14.
       row(int):la ligne dans root, entre 0 et 14.

    Valeurs de retour:
       instance. Retourne un bouton.
    """
    button=ttk.Button(root,text=text,command=command)
    #cree un button et lui assigne une commande
    button.grid(column=col,row=row)#place le button dans la fenetre root
    return button

def intialisation_text_label(root):
    """Initialise les labels a texte.

    Argument:
       root(instance):la fenetre principale.

    Valeurs de retour:
       instance. Retourne neuf labels a texte.
    """
    label_text1=create_text_label(root,'Ce mot vaut :',0,2,1,1,tk.W)
    #cree un label a texte fixe
    label_text2=create_text_label(root,'points',2,2,1,1,tk.W)
    #cree un label a texte fixe
    label_text3=create_text_label(root,'Veuillez introduire les coordonees \
de la premiere lettre :',0,3,3,1,None)#cree un label a texte fixe
    label_text4=create_text_label(root,'Colonne :',0,4,1,1,tk.W)
    #cree un label a texte fixe
    label_text5=create_text_label(root,'Ligne :',0,5,1,1,tk.W)
    #cree un label a texte fixe
    label_text6=create_text_label(root,'Veuillez introduire le mot\
 : ',0,1,1,1,tk.W)#cree un label a texte fixe
    label_text7=create_text_label(root,'Veuillez choisir l\'orientation du\
 mot : ',0,6,1,1,tk.W)#cree un label a texte fixe
    label_text8=create_text_label(root,'Votre score : ',0,11,1,1,tk.W)
    #cree un label a texte fixe
    label_text8=create_text_label(root,'Votre chevalet : ',0,12,1,1,tk.W)
    #cree un label a texte fixe
    label_text9=create_text_label(root,'Pour changer des lettres de votre\
 chevalet, \nveuillez entrer /!\\sans espace/!\\ les lettres a \
 changer. \nAppuyer ensuite sur changer ',0,13,1,1,tk.W)
 #cree un label a texte fixe
    return label_text1,label_text2,label_text3,label_text4,label_text5,\
label_text6,label_text7,label_text8,label_text9

def changer_lettre_gui(val_lettres,chevalet,val_chevalet,sac):
    """Change les lettres du chevalet.

    Arguments:
       val_lettres(instance):StringVar qui contient la valeur des lettres 
       entrees dans une Entry
       chevalet(list):le chevalet contenant 7 lettres.
       val_chevalet(list):le chevalet en liste de ValString.
       sac(list):le sac contenant les lettres.

    Valeurs de retour:
       list. Retourne le sac, le chevalet et la valeur du chevalet.
    """
    sac,chevalet=l.changer_lettre(val_lettres,chevalet,sac)
    val_chevalet=set_val_chevalet(val_chevalet,chevalet)
    return sac,chevalet,val_chevalet

def jouer(val_entry_mot,plateau,val_plateau,sac,chevalet,val_col,val_ligne,\
val_radiobutton,score,val_chevalet,nbre_tours,val_score):
    """Assure le deroulement du jeu lorsqu on appuie sur le bouton play.

    Arguments:
       val_entry_mot(instance):le StringVar contenant la valeur du mot entre.
       plateau(list):le plateau du Scrabble.
       val_plateau(list):la liste de listes de StringVar.
       sac(list):le sac contenant les lettres.
       chevalet(list):le chevalet contenant 7 lettres.
       val_col(instance):le IntVar contenant la colonne du plateau, entre 
       0 et 14.
       val_ligne(instance):le IntVar contenant la ligne du plateau, entre 
       0 et 14.
       val_radiobuttons(instance):le IntVar contenant la valeur 
       des radiobuttons.
       score(int):le score
       val_chevalet(list):le score et la valeur du chevalet.
       nbre_tours(int):le nombre de tours.
       val_score(instance):le IntVar contenant la valeur du score.        
    """
    if messageBox_check_mot_valide(val_entry_mot) and \
messageBox_check_mot_in_chevalet(val_entry_mot,chevalet,val_radiobutton,\
val_col,val_ligne,plateau) and messageBox_check_premier_tour(nbre_tours,\
val_col,val_ligne):
        plateau,chevalet,sac,nbre_tours,score=l.deroulement_jouer(\
val_entry_mot,val_ligne,val_col,plateau,val_radiobutton,chevalet,\
sac,nbre_tours,score)
        val_plateau=set_val_plateau(val_plateau,plateau)
        val_chevalet=set_val_chevalet(val_chevalet,chevalet)
        val_score=set_val_score(val_score,score)
		
def set_val_score(val_score,score):
    """Attribue une valeur au score.

     Arguments:
        val_score(instance):le StrinVar contenant valeur du score.
        score(int):le score.

     Valeurs de retour:
        instance. Retourne le IntVar du score.
    """
    val_score.set(score[0])
    return val_score

def set_val_chevalet(val_chevalet,chevalet):
    """Attribue une valeur au chevalet.

    Arguments:
       val_chevalet(list):la liste de StringVar.
       chevalet(list):le chevalet contenant 7 lettres.

    Valeurs de retour:
       list. Retourne le chevalet avec sa valeur.
    """
    for i in range(len(chevalet)):
        val_chevalet[i].set(chevalet[i])
    return val_chevalet

def set_val_plateau(val_plateau,plateau):
    """Attribue une valeur au plateau.

    Arguments:
       val_plateau(list):la liste de listes de StringVar
       plateau(list):le plateau du scrabble.

    Valeurs de retour:
       instance. Retourne la valeur du plateau.
    """    
    for i in range(len(plateau)):
        for j in range(len(plateau[i])):
            val_plateau[i][j].set(plateau[i][j])
    return val_plateau

def messageBox_check_mot_valide(mot):
    """Affiche un message d'erreur si le mot n'est pas valide.

    Argument:
       mot(str):le mot considere.

    Valeurs de retour:
       str. Retourne 'True' si le mot est valide.
    """ 
    validite=l.check_mot_valide(mot)
    if not validite:
        create_messagebox_error('ERROR : Mot invalide','Le mot que vous\
 avez choisi n\'existe pas.')
    return validite

def messageBox_check_mot_in_chevalet(mot,chevalet,direction,col,ligne,plateau):
    """Affiche un message d'erreur si le mot du chevalet est valide.

    Argument:
       mot(str):le mot considere.
       chevalet(list):le chevalet contenant 7 lettres.
       direction(int):la direction du mot(1='Horizontal' ou 2='Vertical')
       col(int):la colonne du plateau.
       ligne(int):la ligne du plateau.
       plateau(list):le plateau du Scrabble.

    Valeurs de retour:
       instance. Retourne un message d'erreur si le mot du chevalet n'est pas 
       valide.
       str. Retourne 'True' si le mot du chevalet est valide.
    """ 
    validite=l.check_mot_in_chevalet(mot,chevalet,direction,col,ligne,plateau)
    if not validite:
        create_messagebox_error('ERROR : Mot invalide','Le mot que vous avez \
choisi n\'est pas dans votre chevalet.')
    return validite

def messageBox_check_premier_tour(nbre_tours,col,ligne):
    """Affiche un message d'erreur si l'utilisateur ne place pas son mot sur 
    la case 7x7 pour le premier tour.

    Argument:
       nbre_tours(int):le nombre de tours.
       col(int):la colonne du plateau.
       ligne(int)la ligne du plateau.
       
    Valeurs de retour:
       str. Retourne 'VRAI' si c'est le premier tour.
    """ 
    validite=l.check_premier_tour(nbre_tours,col,ligne)
    if not validite:
        create_messagebox_error('ERROR : Premier tour','Pour votre premier \
tour veuillez placer votre mot en 7x7.')
    return validite

def help():
    """Affiche un message d'aide.
    """   
    tkMessageBox.showinfo("Help", "Vous pouvez trouver les regles officielles\
 du Scrabble sur : \nhttp://scrabble.fr.ubi.com/regles.php")

def about():
    """Affiche un message d'information.
    """   
    tkMessageBox.showinfo("About...",
	"Scrabble 1.0.0 \nAuteurs : \nMalik Fassi Fihri \nMatricule : 00364845\
	 \nAn Trinh \nMatricule : 000361085 \nDate : Lundi 30 avril 2012 \nLieu : \
  Bruxelles, Belgique \nFait dans le cadre du deuxieme projet du cours \
  d'informatique")

def create_messagebox_error(nom,message):
    """Permet d'afficher un message d'erreur.

    Arguments:
      nom(str):titre du message.
      message(str):message a afficher.
    """
    tkMessageBox.showerror(nom,message)

def create_messagebox_info(nom,message):
    """Permet d'afficher un message d'info.

    Arguments:
      nom(str):titre du message.
      message(str):message a afficher.
    """   
    tkMessageBox.showinfo(nom,message)

def change_list_to_string(li):
    """Change une liste en string.

    Argument:
       li(list):une liste.

    Valeurs de retour:
       str. Retourne le string contenant les valeur de la liste
    Exemple:
      >>>x=change_list_to_string(['A','B','C'])
      >>>x
     A,B,C, 
    """    
    string=''
    for i in li:
        for j in i:
            string+=j
        string+=', '
    return string

def triche_gui(chevalet,nom):
    """Affiche une fenetre contenant tout les mots qu'il est possible 
    de cree avec les lettres du chevalet.

    Arguments:
       chevalet(list):le chevalet contenant 7 lettres.
       nom(str):le nom du message.
    """    
    ana=l.recherche_anagramme(chevalet)
    ana_string=change_list_to_string(ana)
    create_messagebox_info(nom,ana_string)

def initialisation_valeurs_logiques():
    """Initialise les valeurs logiques (le plateau, le sac, le chevalet, 
      le score et le nombre de tours).

    Valeurs de retour:
      list. Retourne le plateau, le sac et le chevalet.
      int. Retourne le score, le nombre de tours.
    """
    plateau = l.creation_plateau()
    sac=l.creation_sac()
    chevalet=l.creation_chevalet()
    score=l.initialisation_score()
    nbre_tours=l.initialisation_nbre_tours()
    return plateau,sac,chevalet,score,nbre_tours

def initialisation_buttons(root,chevalet,plateau,val_entry_mot,val_plateau,\
  val_chevalet,sac,val_col,val_ligne,val_radiobutton,score,nbre_tours,\
  val_score,val_lettres):
    """Initialise les boutons du jeu (bouton triche, bouton jouer,
      bouton quitter, bouton help, bouton about)
    
    Arguments:
      root(instance):la fenetre principale.
      chevalet(list):le chevalet sous forme de liste de 7 string.
      plateau(list):le plateau sous forme d'une liste de 15 listes de 15 string.
      val_entry_mot(instance):le StringVar qui recupere la valeur d'une entry.
      val_plateau(list):le plateau sous forme d'une liste de 15 listes 
      de 15 StringVar.
      val_chevalet(list):le chevalet sous forme de liste de 7 StringVar.
      sac(list):le sac sous forme de liste.
      val_col(instance):IntVar qui recupere la valeur de la colonne.
      val_ligne(instance):IntVar qui recupere la valeur de la ligne.
      val_radiobutton(instance):IntVar qui recupere la valeur des radiobutton 
      (1='Horizontal' ou 2='Vertical')
      score(int):le score.
      nbre_tours(int):le nombre de tours.
      val_score(instance):IntVar qui contient la score.

    Valeurs de retour:
      instance. Retourne le bouton triche, le bouton jouer, le bouton quitter, 
      le bouton help et le bouton about.
    """
    button_triche=creation_button(root,'Tricher',lambda:triche_gui(chevalet,\
'Un peu d\'aide...'),None,None)
    button_changer=creation_button(root,'Changer',lambda:changer_lettre_gui(\
val_lettres.get().upper(),chevalet,val_chevalet,sac),2,13)
    button_jouer=creation_button(root,'Play !',lambda:jouer(\
val_entry_mot.get().upper(),plateau,val_plateau,sac,chevalet,val_col.get()\
,val_ligne.get(),val_radiobutton.get(),score,val_chevalet,nbre_tours,\
val_score),0,10)
    button_quit=creation_button(root,'Quit',root.quit,4,10)
    button_help=creation_button(root,'Help',help,2,10)
    button_about=creation_button(root,'About...',about,3,10)
    return button_triche,button_changer,button_jouer,button_quit,button_help,\
    button_about

def initialisation_val_chevalet_plateau(chevalet,plateau):
    """Initialise le plateau et le chevalet sous forme de liste de StringVar.

    Arguments:
      chevalet(list):le chevalet sous forme de liste de 7 string.
      plateau(list):le plateau sous forme d'une liste de 15 listes de 15 
      string.

    Valeurs de retour:
      instance. Retourne le plateau sous forme d'une liste de 15 listes de
      15 StringVar et le chevalet sous forme de liste de 7 StringVar.

    """
    val_chevalet=create_gui_val_chevalet(chevalet)
    val_plateau=create_gui_val_plateau(plateau)
    return val_plateau,val_chevalet

def initialisation_plateau_gui_chevalet(root,val_chevalet,val_plateau):
    """Initialise le plateau et le chevalet sous forme graphique.

    Arguments:
      root(instance):la fenetre principale.
      chevalet(list):le chevalet sous forme de liste de 7 string.
      plateau(list):le plateau sous forme d'une liste de 15 listes de 
      15 string.

    Valeurs de retour:
      instance. Retourne le plateau_gui et le gui_chevalet.
    """
    gui_chevalet=create_gui_chevalet(root,val_chevalet,1,12)
    plateau_gui=creation_plateau_gui(root, val_plateau)
    return plateau_gui,gui_chevalet

def initialisation_entry(root,val_points):
    """Initialise les Entry.

    Argument:
      root(instance):la fenetre principale.
      val_points(instance):le IntVar qui contient les points du mot inscrit.

    Valeurs de retour:
      instance. Retourne l'Entry ou le mot doit etre inscrit ainsi que son 
      StringVar, l'Entry ou la colonne est inscrit ainsi que son IntVar, 
      l'Entry ou la ligne est inscrite ainsi que sont IntVar.
    """
    val_entry_mot, entry_mot =create_entry_string(root,15,1,1,1,1)
    create_bind(entry_mot,val_entry_mot,val_points)
    val_lettres, entry_lettres=create_entry_string(root,7,1,13,1,1)
    val_col,entry_col=create_entry_int(root,2,1,4,3,1)
    val_ligne, entry_ligne=create_entry_int(root,2,1,5,3,1)
    return val_entry_mot, entry_mot,val_lettres, entry_lettres,val_col,\
entry_col,val_ligne, entry_ligne

def intialisation_variable_text_label(root):
    """Initialise les labels a texte variable.

    Argument:
      root(instance):la fenetre principale.

    Valeurs de retour:
      instance. Retourne le label ou le score est affiche et son IntVar, 
      le label ou les points du mot sont affiches et son IntVar.
    """
    val_points,label_points=create_variabletext_intlabel(root,1,2)
    val_score, label_score=create_variabletext_intlabel(root,1,11)
    return val_score, label_score, val_points,label_points

________________________________________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________________________________________
________________________________________________________________________________________________________________________________________________________


def creation_plateau_gui(root,val_plateau):
    """Cree le plateau.

    Arguments:
        root(instance):la fenetre principale.
        val_plateau(list):la liste de listes de StringVar.

    Valeurs de retour:
        instance. Retourne le plateau.
    """
    plateau_gui = create_gui_grid(root, val_plateau,5,0,16,16)  
    create_nombre_border_vert(plateau_gui,3,1,'solid')
    create_nombre_border_horiz(plateau_gui,3,1,'solid')
    create_case_vide(plateau_gui,3,1,'solid')
    return plateau_gui

def create_nombre_border_vert(frame,width,borderwidth,relief):
    """Cree les nombres sur le bord vertical du plateau.
  
    Arguments:
       frame(instance):la fenetre enfant.
       width(int):l'epaisseur de la case du plateau.
       borderwidth(int):l'epaisseur du bord de la case.
       relief(str):le style de la case.

    Valeurs de retour:
       instance. Retourne le plateau avec le bord vertical numerote de 0 a 14.
    """

    for i in range(15):
        label=ttk.Label(frame,text=i,anchor='center')#cree un label
        label.config(borderwidth=borderwidth,width=width,relief=relief)
        #configure un label
        label.grid(column=0,row=i+1)#place le label dans la fenetre frame
    return frame

def create_nombre_border_horiz(frame,width,borderwidth,relief):
    """Cree les nombres sur le bord horizontal du plateau.

    Arguments:
       frame(instance):la fenetre enfant.
       width(int):l'epaisseur de la case du plateau.
       borderwidth(int):l'epaisseur du bord de la case.
       relief(str):le stye de la case.

    Valeurs de retour:
       instance. Retourne le plateau avec le bord horizontal numerote de 0 a 14.
    """
    for i in range(15):
        label=tk.Label(frame,text=i,anchor='center')#cree un label
        label.config(borderwidth=borderwidth,width=width,relief=relief)
        #configure un label
        label.grid(column=i+1,row=0)#place le label dans la fenetre frame
    return frame

def create_case_vide(frame,width,borderwidth,relief):
    """Cree une case vide situee entre le bord horizontal et vertical.

    Arguments:
       frame(instance):la fenetre enfant.
       width(int):l'epaisseur de la case du plateau.
       borderwidth(int):l'epaisseur du bord de la case.
       relief(str):le stye de la case.

    Valeurs de retour:
       instance. Retourne le plateau avec la case vide.
    """
    case_vide=ttk.Label(frame,text='')#cree un label
    case_vide.config(borderwidth=borderwidth,width=width,relief=relief)
    #configure un label
    case_vide.grid(column=0,row=0)#place la grille a la case 0x0
    return frame

def create_gui_val_chevalet(chevalet):
    """Cree l'interface du chevalet.

    Argument: 
       chevalet(list):le chevalet contenant 7 lettres.

    Valeurs de retour:
       instance. Retourne le chevalet sous forme de liste de StringVar
    """
    val_chevalet=[]
    for i in range(len(chevalet)):#i allant de 0 a 6
        val=tk.StringVar()
        val_chevalet.append(val)#ajoute 7 StringVar dans la liste val_chevalet
        val_chevalet[i].set(chevalet[i])#attribue une valeur au StringVar
    return val_chevalet



def create_gui_chevalet(root,val_chevalet,column,row):
    """Cree l'interface du chevalet.

    Arguments:
       root(instance):la fenetre principale.
       val_chevalet(list):la liste de listes de StringVar du chevalet.
       column(int):la colonne dans root, entre 0 et 14.
       row(int):la ligne dans root, entre 0 et 14.
    Valeurs de retour:
       instance. Retourne le plateau avec le chevalet.
    """
    frame=tk.Frame(root)#cree une fenetre dans root
    for i in range(len(val_chevalet)):#i allant de 0 a 6
        label=ttk.Label(frame,textvariable=val_chevalet[i],anchor='center')
        #cree un label
        label.config(borderwidth=1,width=2,relief='sunken')#configure un label
        label.grid(column=i,row=0)#place le label dans la fenetre frame
    frame.grid(column=column,row=row)
    #place la fenetre frame dans la fenetre root
    return frame

def creation_radiobutton(root,text1,text2,value1,value2, col1, row1, col2, row2):
    """Cree les radiobuttons.

    Arguments:
       root(instance):la fenetre principale.
       text1(str):le texte sur le radiobutton 1.
       text2(str):le texte sur le radiobutton 2.
       value1(str):la valeur du radiobutton 1.
       value2(str):la valeur du radiobutton 2.
       col1(int):la colonne du radiobutton 1 dans root.
       row1(int):la ligne du radiobutton 1 dans root.
       col2(int):la colonne du radiobutton 2 dans root.
       row2(int):la ligne du radiobutton 2 dans root.

    Valeurs de retour:
       instance. Retourne les radiobuttons 1 et 2 et le IntVar du radiobutton.
    """  
    val_radiobutton=tk.IntVar()
    R1=tk.Radiobutton(root,text=text1,variable=val_radiobutton, value=value1)
    #cree un radiobutton
    R2=tk.Radiobutton(root,text=text2,variable=val_radiobutton, value=value2)
    #cree un radiobutton
    R1.grid(column=col1,row=row1)#place le radiobutton dans la fenetre root
    R2.grid(column=col2,row=row2)#place le radiobutton dans la fenetre root
    return R1, R2,val_radiobutton

def create_entry_string(root,width,col,row,columnspan,rowspan):
    """Cree une entree sous forme de string.

    Arguments:
       root(instance):la fenetre principale.
       width(int):l'epaisseur de la case du plateau.
       col(int):la colonne dans root.
       row(int):la ligne dans root.
       columnspan(int):le nombre de colonnes que prend l'objet.
       rowspan(int):le nombre de lignes que prend l'objet.

    Valeurs de retour:
       str. Retourne un StringVar associe a une Entry.
       instance. Retourne une entree.
    """    
    val=tk.StringVar()
    entry=ttk.Entry(root,width=width,textvariable=val)# cree une Entry
    entry.grid(column=col,row=row,columnspan=columnspan,rowspan=rowspan)
    #place l'entry dans la fenetre root
    return val, entry

def bind_entry(entry,val_entry_mot,val_point):
    """Appelle la fonction comptabilisation_points et assigne sa \
valeur de retour a val_point.

    Arguments:
      entry(instance):Entrey en consideration.
      val_entry_mot(instance):Stringvar dont il faut calculer les points.
      val_points(instance):IntVar qui va recuperer la valeur des points.
    """
    def f(event):
        val_point.set(l.comptabilisation_points(val_entry_mot.get()))
        #calcul les points du mot entre dans un entry
    return f

def create_bind(entry,val_entry_mot,val_point):
    """Permet d'appeler la fonction bind_entry a chaque fois que \
l'utilisateur 'relache' une touche.

    Arguments:
      entry(instance):Entrey en consideration.
      val_entry_mot(instance):Stringvar dont il faut calculer les points.
      val_points(instance):IntVar qui va recuperer la valeur des points.
    """
    entry.bind("<Any-KeyRelease>",bind_entry(entry,val_entry_mot,val_point))
    #permet de calculer les points du mot a chaque fois que 
    #l'utilisateur entre une lettre

def create_entry_int(root,width,col,row,columnspan,rowspan):
    """Cree une entree sous forme de int.

    Arguments:
       root(instance):la fenetre principale.
       width(int):l'epaisseur de la case du plateau.
       col(int):la colonne dans root.
       row(int):la ligne dans root.
       columnspan(int):le nombre de colonnes que prend l'objet.
       rowspan(int):le nombre de lignes que prend l'objet.

    Valeurs de retour:
       instance. Retourne un IntVar associe a une Entry.
       instance. Retourne une entree.
    """     
    val=tk.IntVar()
    entry=ttk.Entry(root,width=width,textvariable=val)#cree une Entry
    entry.grid(column=col,row=row,columnspan=columnspan,rowspan=rowspan)
    #place l'entry dans la fenetre root
    return val, entry
