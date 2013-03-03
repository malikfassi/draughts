# -*- coding: utf8 -*-

from tkinter import Tk, Canvas, Label, Button, IntVar, StringVar
import tkinter.messagebox as box
from config import *
import draughtsFunctionsCorrection2 as dr

class FixedLabel:
    def __init__(self,parent,text,col,row):
        label=Label(parent,text=text,bg="bisque")
        label.grid(column=col,row=row)

class VariableLabel:
    def __init__(self,parent,col,row,genre):
        
        self.val=StringVar()
        self.val.set("RED")
        if (genre=="integer"): 
            self.val=IntVar()
            self.val.set(0)
        label=Label(parent,textvariable=self.val,bg="bisque")
        label.grid(column=col,row=row)

    def getVar(self):
        return(self.val)
    
    def setVar(self,valeur):
        self.val.set(valeur)

class MessageBox:
    def __init__(self,title,message):
        self.body=box.showinfo(title,message)

class VerticalBorder:
    def __init__(self,parent,anchor,borderwidth,width,relief):
        for i in range(1,DIMENSION+1):
            label=Label(parent,text=i,anchor=anchor)
            label.config(borderwidth=0,width=2,height=2,relief=relief,bg="bisque")
            label.grid(row=i,column=3)

class HorizBorder:
    def __init__(self,parent,anchor,borderwidth,width,relief):
        col=4
        for i in map(chr, range(97, 97+DIMENSION)):
            label=Label(parent,text=i,anchor=anchor)
            label.config(borderwidth=0,width=4,height=2,relief=relief,bg="bisque")
            label.grid(row=11,column=col)
            col+=1

def newgame(parent,player,logicBoard):
    if (not(box.askokcancel('New game', "Are you sure ?"))): return
    parent.destroy()
    board = Board(400, 400,cellSize,player=player,logicBoard=logicBoard)
    board.config(bg="bisque")
    borderVert=VerticalBorder(board,"center",1,3,"solid")
    boderHoriz=HorizBorder(board,"center",1,3,"solid")
    board.title("Draughts")
    buttons=Buttons(board)
    board.mainloop()

def guiLoad(parent):
    player,logicBoard=dr.load("sauvegarde.dat")
    newgame(parent,player,logicBoard)

def help(title,text):
    MessageBox(title,text)

class Buttons:

    def __init__(self,parent):
        self.parent=parent
        self.button1=Button(self.parent,text="New game",command=lambda:newgame(parent,None,None))
        self.button1.grid(row=12,column=5,columnspan=2)
        self.button2=Button(self.parent,text="Save game",command=lambda:dr.save("sauvegarde.dat",parent.getBoard(),parent.getPlayer()))
        self.button2.grid(row=12,column=7,columnspan=2)
        self.button3=Button(self.parent,text="Load game",command=lambda:guiLoad(parent))
        self.button3.grid(row=12,column=9,columnspan=2)
        text="Pour bouger un pion le joueur doit d’abord cliquer sur le pion qu’il veut bouger, ensuite il doit cliquer sur l’endroit ou il veut aller (le pion bouge), finalement il doit re-cliquer sur le meme pion pour signaler que son coup est fini ;"
        self.button4=Button(self.parent,text="Help",command=lambda:help("Help",text))
        self.button4.grid(row=12,column=11)


class Board(Tk):
    def __init__(self, width, height, cellSize,player=None,logicBoard=None):
        Tk.__init__(self)
        self.cellSize = cellSize
        self.guiBoard = Canvas(self, width=width, height=height, bg="bisque")
        self.currentFixedLabel = FixedLabel(self,"CURRENT PLAYER : ",16,0)
        self.currentVariableLabel = VariableLabel(self,18,0,"string")
        self.bluePointsFixedLabel = FixedLabel(self,"BLUE CAPTURES : ",16,2)
        self.bluePointsVariableLabel = VariableLabel(self,18,2,"integer")
        self.redPointsFixedLabel = FixedLabel(self,"RED CAPTURES : ",16,4)
        self.redPointsVariableLabel = VariableLabel(self,18,4,"integer")
        self.logicBoard=logicBoard
        if not(logicBoard):
            self.logicBoard=dr.initBoard(DIMENSION)
        self.player=player
        if not(player):
            self.player=1
        self.hasPlayed=False
        self.hasCaptured=False
        self.guiBoard.bind("<Button -1>", self.bindEvent)
        self.initiateBoard()
        self.guiBoard.grid(rowspan=DIMENSION+1,columnspan=DIMENSION+1,row=0,column=4)

    def getBoard(self):
        return(self.logicBoard)

    def getPlayer(self):
        return(self.player)

    def initiateBoard(self):

        for i in range(DIMENSION):
            for j in range(DIMENSION):
                coordX1 = (i * self.cellSize)
                coordY1 = (j * self.cellSize)
                coordX2 = coordX1 + self.cellSize
                coordY2 = coordY1 + self.cellSize
                color = "white" if i%2 == j%2 else "black"
                cell = self.logicBoard[j][i]
                guiCell=self.draw_rectangle(coordX1, coordY1, coordX2, coordY2, color, "r"+str(i)+str(j))
                if cell !=0:
                    pawnColor = "red" if cell > 0 else "blue"
                    pawn=self.draw_circle(coordX1, coordY1, coordX2, coordY2, pawnColor, "c"+str(i)+str(j),pawnColor)

    def draw_rectangle(self,coordX1,coordY1,coordX2,coordY2,color,tags):
        self.guiBoard.create_rectangle(coordX1,coordY1,coordX2,coordY2,fill=color,outline="black",tags=tags)
        return(self.guiBoard.create_rectangle(coordX1,coordY1,coordX2,coordY2,fill=color,outline="black",tags=tags))
    def draw_circle(self, coordX1, coordY1, coordX2,coordY2, color, tags,outline):
        return(self.guiBoard.create_oval(coordX1,coordY1,coordX2,coordY2,fill=color,outline=outline,tags=tags))

    def findLength(self,i,j,ancientSelectedCellTags):

        departJ=int(ancientSelectedCellTags[0][1])
        departI=int(ancientSelectedCellTags[0][2])
        length=None
        if(departI!=i):
            isDiago=abs(j-departJ)/abs(i-departI)

            if(isDiago==1):#la case d'arrivée se trouve sur la diagonale
                length=( ((j-departJ)**2) + ((i-departI)**2) )**(1/2) #recherche de l'hypothenuse
                length/=(2)**(1/2) #divisé par racine de 2 car l'hypothenuse d'un triangle avec 2 coté de longueur 1 = racine de 2 
        return(length)

    def findDirection(self,i,j,ancientSelectedCellTags,player):
        dirI=(i-int(ancientSelectedCellTags[0][2]))/abs(i-int(ancientSelectedCellTags[0][2]))
        dirJ=(j-int(ancientSelectedCellTags[0][1]))/abs(j-int(ancientSelectedCellTags[0][1]))

        direction="L"
        if (dirJ==self.player): direction="R"
        if(dirI==self.player): direction+="B"
        return(direction)

    def enfOfGame(self):
        end=dr.checkEndOfGame(self.logicBoard,self.player) 
        if (end is False): return #le jeu n'est pas fini
        self.guiBoard.unbind("<Button -1>")
        if(end!=0):
            winner="RED PLAYER" if end==1 else "BLUE PLAYER"
            text=winner + " WON"
        else:
            text = "DRAW"
        FixedLabel(self,text,16,6)


    def changePlayer(self,cellId,i,j):
        self.player=-self.player
        val="RED" if self.player ==1 else "BLUE"
        print(val)
        self.currentVariableLabel.setVar(val)
        self.hasPlayed=False
        self.hasCaptured=False
        dr.becomeKing(self.logicBoard,j,i)
        self.enfOfGame()
        if (dr.isKing(self.logicBoard,j,i)): self.guiBoard.itemconfig(cellId,outline="gold",width=2)

    def coordToLetter(self,j):
        return(chr(int(j)+97))


    def moveGuiPiece(self,i,j,ancientSelectedCellTags,ancientSelectedCellCoordI,ancientSelectedCellCoordJ,ancientSelectedCellId,playerColor):
        length=self.findLength(j,i,ancientSelectedCellTags)#chercher la longueur du mouvement

        if (not(length)): return
            #Le mouvement n'est pas autorisé, case d'arrivée n'est pas sur la diagonale

        direction=self.findDirection(j,i,ancientSelectedCellTags,self.player)#chercher la destination
        errCode=dr.checkMove(self.logicBoard,ancientSelectedCellCoordI,ancientSelectedCellCoordJ,direction,self.player,moves=length,hasPlayed=self.hasPlayed,hasCaptured=self.hasCaptured)

        if (errCode==NO_ERROR):
            #Le mouvement est autorisé
            dest,cap=dr.movePiece(self.logicBoard,ancientSelectedCellCoordI,ancientSelectedCellCoordJ,direction,moves=length)
            tag="c"+str(dest[1])+str(dest[0])
            self.guiBoard.delete(ancientSelectedCellId)#supression du pion déplacé
            
            if (cap):
                self.guiBoard.delete("c"+str(cap[1])+str(cap[0]))#supression du pion capturé
                self.hasCaptured=True
                dr.capture(self.logicBoard,cap[0],cap[1])
                if (playerColor=="red"):
                    self.redPointsVariableLabel.setVar(self.redPointsVariableLabel.getVar().get()+1)
                else:
                    self.bluePointsVariableLabel.setVar(self.bluePointsVariableLabel.getVar().get()+1)

            destCoordX1,destCoordY1,destCoordX2,destCoordY2=self.getGuiCoord(dest[1],dest[0])
            currentCellId=self.draw_circle(destCoordX2,destCoordY2,destCoordX1,destCoordY1, playerColor, tag,playerColor)#placement du pion déplacé

            if (cap): self.selectPawn(currentCellId,tag)#Après capture, le pion est toujours sélectionné
            self.hasPlayed=True

            if(not(self.hasCaptured)): self.changePlayer(currentCellId,i,j)#Aucune capture, changement de joueur

        else:
            departA=self.coordToLetter(ancientSelectedCellTags[0][1])
            departB=str(int(ancientSelectedCellTags[0][2])+1)
            destA=self.coordToLetter(i)
            destB=str(j+1)
            message="le coup "+departA+departB+"-"+destA+destB+" n'est pas permis"+"\n"+dr.strerr(errCode)
            MessageBox("ERROR "+str(errCode),message)
                



    def selectPawn(self,currentCellId,tag):
        self.guiBoard.itemconfig(currentCellId,fill="green",tags=(tag,"selected"))

    def deselectPawn(self,ancientSelectedCellId,playerColor,ancientSelectedCellTags):
        self.guiBoard.itemconfig(ancientSelectedCellId,fill=playerColor,tags=ancientSelectedCellTags[0])

    def getGuiCoord(self,i,j):
        coordX1 = (i * self.cellSize)
        coordY1 = (j * self.cellSize)
        coordX2 = coordX1 + self.cellSize
        coordY2 = coordY1 + self.cellSize
        return(coordX1,coordY1,coordX2,coordY2)

    def bindEvent(self,event):
        i = int(event.x / self.cellSize)
        j = int(event.y / self.cellSize)
        if(dr.outside(self.logicBoard,j,i)): return
        playerColor="red" if self.player==1 else "blue"

        if(dr.caseNoire(j,i)):#Si l'on a cliqué sur une case noire

            coordX1,coordY1,coordX2,coordY2=self.getGuiCoord(i,j)
            tag="c"+str(i)+str(j)
            if (dr.isFree(self.logicBoard,j,i)):#Si l'on a cliqué sur une case vide
                currentCellId=self.guiBoard.find_withtag("r"+str(i)+str(j))[0]#recherche de l'ID de la case vide
            else:#Si l'on a cliqué sur un pion
                currentCellId=self.guiBoard.find_withtag(tag)[0]#recherche de l'ID du pion

            ancientSelectedCellId=self.guiBoard.find_withtag("selected")#recherche de l'ancienne case sélectionée

            if (ancientSelectedCellId):#Si une case à déjà été sélectionnée

                ancientSelectedCellId=ancientSelectedCellId[0]#On récupère l'id du tuple
                ancientSelectedCellTags=self.guiBoard.gettags(ancientSelectedCellId)#On récupère les tags de la case qui était selectionée
                ancientSelectedCellCoordI=int(ancientSelectedCellTags[0][1])
                ancientSelectedCellCoordJ=int(ancientSelectedCellTags[0][2])

                if (not(dr.isFree(self.logicBoard,j,i))):#Si on sélectionne une case remplie

                    if (self.hasCaptured==True):#Si l'on a déjà capturé

                        if (ancientSelectedCellCoordJ==j and ancientSelectedCellCoordI==i and dr.playerColor(self.logicBoard[j][i])==self.player):
                            #J'ai cliqué sur moi même : Tour fini
                            self.changePlayer(ancientSelectedCellId,i,j)
                            self.deselectPawn(ancientSelectedCellId,playerColor,ancientSelectedCellTags)
                            return

                    elif (dr.playerColor(self.logicBoard[j][i])==self.player):#Si on selectionne un de nos pions
                        self.deselectPawn(ancientSelectedCellId,playerColor,ancientSelectedCellTags)
                        self.selectPawn(currentCellId,tag)
                        return

                self.moveGuiPiece(i,j,ancientSelectedCellTags,ancientSelectedCellCoordJ,ancientSelectedCellCoordI,ancientSelectedCellId,playerColor)

            else:#Aucune case n'était sélectionnée

                if(not(dr.isFree(self.logicBoard,j,i))):
                    if (dr.playerColor(self.logicBoard[j][i])==self.player):
                        self.selectPawn(currentCellId,tag)

if __name__=="__main__":
    cellSize = 40
    board = Board(400, 400,cellSize)
    board.config(bg="bisque")
    borderVert=VerticalBorder(board,"center",1,3,"solid")
    boderHoriz=HorizBorder(board,"center",1,3,"solid")
    board.title("Draughts")
    buttons=Buttons(board)
    board.mainloop()