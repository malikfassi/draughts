"""
INFO-F106 : Projets d’Informatique 1
Fichier : draughtsFunctions.py

Malik Fassi Fihri 
Matricule : 000364845

"""
# -*- coding: utf-8 -*-

from config import *
from math import *
import pdb

def caseNoire(row,col):
	"""Retourne True si la case d'indice row,col est une case noire.
		Arguments:

		row (int) : indice de la ligne qui se trouve dans le plateau
		col (int) : indice de la colonne qui se trouve dans le plateau

		Valeurs de retour:

		bool. Retourne True si la case d'indice row,col est une case noire.
		
		Exemples:
		>>> print(caseNoire(0,0))
		False
		>>> print(caseNoire(0,1))
		True
	"""
	return(not(row%2==col%2))

def appendPion(myboard,couleur,nbreLigne,rangeDimension,begin):
	"""Ajoute une valeur(couleur) dans myboard
		Arguments:

		myboard (list) : plateau du jeu de dame
		couleur (str/int) : element a rajouter dans le plateau (case/pion)
		nbreLigne (int) : nombre de lignes que l'element couleur doit remplir
		rangeDimension (range) : objet range equivalent a range(DIMENSION)
		begin (int) : index de la ligne a laquelle l'element couleur doit 
		remplir le plateau

	"""
	for row in range(begin,begin+nbreLigne):
		for col in rangeDimension:	
			if(caseNoire(row,col)):
				myboard[row].append(couleur)
			else:
				myboard[row].append(FREE_SPACE)

def tranform(myboard,row,col):
	"""Transforme les cases en pions noirs ou blancs ou case noire ou blanche 
		Arguments:

		myboard (list) : plateau du jeu de dame
		row (int) : indice de la ligne qui se trouve dans le plateau
		col (int) : indice de la colonne qui se trouve dans le plateau

		Valeurs de retour:

		response (str) : pions blancs ou noirs ou case blanches ou noires

	"""
	response=""
	case=myboard[row][col]
	if(case==FREE_SPACE):
		if (caseNoire(row,col)):
			response=BLACK_SQUARE
		else:
			response=WHITE_SQUARE
	elif(case<0):
		if (case==BLACK_PLAYER):
			response=BLACK_PAWN
		else:
			response=BLACK_KING
	else:
		if (case==WHITE_PLAYER):
			response=WHITE_PAWN
		else:
			response=WHITE_KING
	return(response)

def printBoard(myboard,player):
	"""imprime le plateau proprement 
		Arguments:

		myboard (list) : plateau du jeu de dame
		player (int) : 1 ou -1 en fonction du joueur

		Exemples:
		>>> printBoard(myboard,WHITE_PLAYER)

		▇ ○ ▇ ○ ▇ ○ ▇ ○ ▇ ○  |1
		○ ▇ ○ ▇ ○ ▇ ○ ▇ ○ ▇  |2
		▇ ○ ▇ ○ ▇ ○ ▇ ○ ▇ ○  |3
		○ ▇ ○ ▇ ○ ▇ ○ ▇ ○ ▇  |4
		▇   ▇   ▇   ▇   ▇    |5
		  ▇   ▇   ▇   ▇   ▇  |6
		▇ ● ▇ ● ▇ ● ▇ ● ▇ ●  |7
		● ▇ ● ▇ ● ▇ ● ▇ ● ▇  |8
		▇ ● ▇ ● ▇ ● ▇ ● ▇ ●  |9
		● ▇ ● ▇ ● ▇ ● ▇ ● ▇  |10
		_ _ _ _ _ _ _ _ _ _ 
		a b c d e f g h i j
	"""
	rangeDimension1=range(len(myboard))
	rangeDimension2=list(rangeDimension1)
	alphaArray=[chr(i) for i in range(ord('a'), ord('a')+len(myboard))]

	if (player==-1):
		rangeDimension2.reverse()
		alphaArray.reverse()
	for row in rangeDimension2:
		for col in rangeDimension2:
			print(tranform(myboard,row,col),end=" ")
		print(" |"+str(rangeDimension1[row]+1))
	print(("_ ")*len(myboard))
	print(" ".join(alphaArray))



def initBoard(dimension):
	"""Initialise le plateau.
		Arguments:

		dimension (int) : dimension du plateau

		Valeurs de retour:

		myboard (list): liste representant le plateau
		
		Exemples:
		>>> print(initBoard(dimension))
		[[0, -1, 0, -1, 0, -1, 0, -1, 0, -1], 
		[-1, 0, -1, 0, -1, 0, -1, 0, -1, 0], 
		[0, -1, 0, -1, 0, -1, 0, -1, 0, -1], 
		[-1, 0, -1, 0, -1, 0, -1, 0, -1, 0], 
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
		[0, 1, 0, 1, 0, 1, 0, 1, 0, 1], 
		[1, 0, 1, 0, 1, 0, 1, 0, 1, 0], 
		[0, 1, 0, 1, 0, 1, 0, 1, 0, 1], 
		[1, 0, 1, 0, 1, 0, 1, 0, 1, 0]]

	"""
	myboard=[]
	rangeDimension=range(dimension)
	for i in rangeDimension:
		myboard.append([])
	nbreLigneVide=2+dimension%2
	nbreLigne=(dimension-nbreLigneVide)//2
	appendPion(myboard,BLACK_PLAYER,nbreLigne,rangeDimension,0)
	appendPion(myboard,FREE_SPACE,nbreLigneVide,rangeDimension,nbreLigne)
	appendPion(myboard,WHITE_PLAYER,nbreLigne,rangeDimension,nbreLigne+\
	nbreLigneVide)
	return(myboard)


def findDest(board,rowIndex,colIndex,direction,length,step=None):
	""" Trouve la destination de la pion.

		Arguments :

			board (list) : plateau du jeu
			rowIndex (int) : index de la ligne ou se trouve le pion
			colIndex (int) : index de la colonne ou se trouve le pion
			direction (str) : "R", "L", "LB" ou "RB" 
			length (int) = longueur du deplacement
			step (int) = (default=None) defini la destination a "step" case

		Valeur de retour : 

			destI (int) : ligne de destination
			destJ (int) : colonne de destination
			dirI (int) : direction du mouvement dans les lignes
			dir J (int) : direction du mouvement des les colonnes
			player (int) : le joueur
			length (int) : taille du deplacement


	"""
	#print ( "Je suis dans findDest")
	#print (rowIndex,colIndex,direction,length)
	player=board[rowIndex][colIndex]
	if (abs(player)>1):
		player//=abs(player)
	elif(player==FREE_SPACE):
		player=WHITE_PLAYER
	if(step):
		length=step
	else:
		#print("je rentre dans countFree dans FindDest")
		#print("avec les parametres "+str((rowIndex,colIndex,direction)))
		newLength=countFree(board,rowIndex,colIndex,direction,player=player)
		#print("je sors de countFree dans FindDest")
		if (newLength<length):
			length=newLength+1
		
	destI=int(rowIndex-(player*length))
	destJ=int(colIndex+(player*length))
	dirI=int(-player)
	dirJ=int(player)

	if (len(direction)==2):
		destI=int(rowIndex+(player*length))
		dirI=int(player)
	if(direction[0]=="L"):
		destJ=int(colIndex-(player*length))
		dirJ=int(-player)

	return(destI,destJ,dirI,dirJ,player,length)

def movePiece(board,rowIndex,colIndex,direction,length=1):
	"""Deplace une piece.

		Arguments:

			board (list) : plateau du jeu
			rowIndex (int) : index de la ligne ou se trouve le pion
			colIndex (int) : index de la colonne ou se trouve le pion
			direction (str) : "R", "L", "LB" ou "RB" 

		Valeur de retour :

			(destI,destJ) (tuple) : tuple de la destination
			capt : tuple de la capture sinon None


		Exemples:
		>>> movePiece(myboard,6,3,"L",WHITE_PLAYER)
		>>> print(myboard)
		▇ ○ ▇ ○ ▇ ○ ▇ ○ ▇ ○  |1
		○ ▇ ○ ▇ ○ ▇ ○ ▇ ○ ▇  |2
		▇ ○ ▇ ○ ▇ ○ ▇ ○ ▇ ○  |3
		○ ▇ ○ ▇ ○ ▇ ○ ▇ ○ ▇  |4
		▇   ▇   ▇   ▇   ▇    |5
		  ▇ ● ▇   ▇   ▇   ▇  |6
		▇ ● ▇   ▇ ● ▇ ● ▇ ●  |7
		● ▇ ● ▇ ● ▇ ● ▇ ● ▇  |8
		▇ ● ▇ ● ▇ ● ▇ ● ▇ ●  |9
		● ▇ ● ▇ ● ▇ ● ▇ ● ▇  |10
		_ _ _ _ _ _ _ _ _ _ 
		a b c d e f g h i j

	"""
	pawn=board[rowIndex][colIndex]
	player=colorOfPawn(pawn)
	destI,destJ,dirI,dirJ,player,length=findDest(board,rowIndex,\
	colIndex,direction,length)
	#print('findDest '+'destI = '+str(destI)+' destJ = '+str(destJ)+ " dirI = "+str(dirI)+' dirJ = '+str(dirJ)+" player = "+ str(player) +" length = "+str(length))
	capt=findCapture(board,rowIndex,colIndex,length,dirI,dirJ,player)
	#print(capt)
	if capt:
		destI+=dirI
		destJ+=dirJ
		board[destI][destJ]=pawn
		board[capt[0]][capt[1]]=FREE_SPACE
	else:
		board[destI][destJ]=pawn
	board[rowIndex][colIndex]=FREE_SPACE
	return((destI,destJ),capt)

def countFree(board,rowIndex,colIndex,direction,player=None,length=0):
	""" Calcule la longueur de mouvements a effectuer avant de capturer\
	 une piece adverse.

		Arguments :

			board (list) : plateau du jeu
			rowIndex (int) : index de la ligne ou se trouve le pion
			colIndex (int) : index de la colonne ou se trouve le pion
			direction (str) : "R", "L", "LB" ou "RB" 
			player (int) : (default=None) le joueur (1 ou -1)
			length (int) : (default=0) le nombre de cases vides

		Valeur de retour :

			length (int) : le nombre de cases vides

	"""
	#print("Je suis dans countFree")
	if (player==None):
		player=colorOfPawn(board[rowIndex][colIndex])
	#print("je rentre dqns findDest a l'interieur de countFree")
	#print("Avec les parametres "+ str((rowIndex,colIndex,direction,length)))
	destI,destJ=findDest(board,rowIndex,colIndex,direction,length,step=1)[:2]
	#print("Je suis sorti de FindDest dans countFree")
	#print(destI,destJ)
	if (0<=destI<=9 and 0<=destJ<=9):
		if (board[destI][destJ]==FREE_SPACE):
			length+=1
			length=countFree(board,destI,destJ,direction,player=player,\
			length=length)
	return(length)

def findCapture(board,rowIndex,colIndex,length,dirI,dirJ,player,step=None):
	"""
			Arguments :

			board (list) : plateau du jeu
			rowIndex (int) : index de la ligne ou se trouve le pion
			colIndex (int) : index de la colonne ou se trouve le pion
			length (int) : taille du deplacement
			dirI (int) : direction du mouvement dans les lignes
			dir J (int) : direction du mouvement des les colonnes
			step (int) ; (default=None) si il y a un parametre step la \
			fonction cherchera autant de capture
	"""
	capt=None
	li=[]
	res=capt
	for i in range(1,length+1):
		nextRow=rowIndex+dirI*i
		nextCol=colIndex+dirJ*i
		if (0<=nextRow<=9 and 0<=nextCol<=9):
			if (board[nextRow][nextCol]!=FREE_SPACE):
				#print("YEAAAAAHHHH")
				if (colorOfPawn(board[nextRow][nextCol])!=player):
					if(step):
						if(len(li)<step):
							li.append((nextRow,nextCol))
							res=li
					else:
						capt=(nextRow,nextCol)
						res=capt
						break
				else:
					break
	return(res)

def becomeKing(board,rowIndex,colIndex):
	""" Transforme les pions qui le peuvent en Dame.

		Arguments :

			board (list) : plateau du jeu
			rowIndex (int) : index de la ligne ou se trouve le pion
			colIndex (int) : index de la colonne ou se trouve le pion

	"""
	player=colorOfPawn(board[rowIndex][colIndex])
	if (player==BLACK_PLAYER and rowIndex==DIMENSION-1):
		board[rowIndex][colIndex]-=1
	elif(player==WHITE_PLAYER and rowIndex==0):
		board[rowIndex][colIndex]+=1

def capture(board,rowIndex,colIndex):
	""" Supprime un pion capture du plateau.

		Arguments :
			
			board (list) : plateau du jeu
			rowIndex (int) : index de la ligne ou se trouve le pion
			colIndex (int) : index de la colonne ou se trouve le pion

	"""
	board[rowIndex][colIndex]=FREE_SPACE


def checkOpponentPiece(board,rowIndex,colIndex,player):
	"""Verifie si le joueur a selectionne un de ses pions

		Arguments:

			board (list) : plateau du jeu
			rowIndex (int) : index de la ligne ou se trouve le pion
			colIndex (int) : index de la colonne ou se trouve le pion
			player (int) : 1 ou -1 en fonction du joueur

		Valeurs de retour:

			errCode (int) : Valeur du message d'erreur

		"""
	errCode=NO_ERROR
	if ((board[rowIndex][colIndex]>0 and player<0) or (board[rowIndex]\
	[colIndex]<0 and player>0)) :
		errCode=OPPONENT_PIECE
	return(errCode)

def checkCannotGoJumpOutside(board,destI,destJ,length,rowIndex,colIndex\
,dirI,dirJ,player):
	"""Verifie si le joueur se deplace en dehors du plateau ou s'il saute\
	 en dehors du plateau apres une capture.
		
		Arguments:

			board (list) : plateau du jeu
			destI (int) : ligne de destination
			destJ (int) : colonne de destination
			length (int) : taille du deplacement
			rowIndex (int) : index de la ligne ou se trouve le pion
			colIndex (int) : index de la colonne ou se trouve le pion
			dirI (int) : direction du mouvement dans les lignes
			dir J (int) : direction du mouvement des les colonnes

		Valeurs de retour:

			errCode (int) : Valeur du message d'erreur

		"""
	errCode=NO_ERROR
	#print('Cannot '+'destI = '+str(destI)+' destJ = '+str(destJ)+ " dirI = "+str(dirI)+' dirJ = '+str(dirJ)+" player = "+ str(player) +" length = "+str(length))
	if((not(0<=destI<=9) or not(0<=destJ<=9))):
	#	print("ME AMOR")
		if (rowIndex+(dirI*length)-9==1 or colIndex+(dirJ*length)-9==1):
			#print("YOUPIEEE")
			capt=findCapture(board,rowIndex,colIndex,length,dirI,dirJ,player)
			if(capt):
				errCode=CANNOT_JUMP_OUTSIDE
			else:
				errCode=CANNOT_GO_OUTSIDE
	#print("Cannot " + str(errCode))
	return(errCode)

def checkCannotJumpOutside(board,rowIndex,colIndex,length,dirI,dirJ,player):
	errCode=NO_ERROR
	capt=findCapture(board,rowIndex,colIndex,length,dirI,dirJ,player)
	if (capt):
		if (capt[0]==9 or capt[1]==9):
			errCode=CANNOT_JUMP_OUTSIDE
	return(errCode)

def checkNoPiece(board,destI,destJ):
	"""Verifie si le joueur a selectionne une case vide
		
		Arguments:

			board (list) : plateau du jeu
			destI (int) : ligne de destination
			destJ (int) : colonne de destination	

		Valeurs de retour:
		
			errCode (int) : Valeur du message d'erreur

		"""
	errCode=NO_ERROR
	if (board[destI][destJ]==FREE_SPACE):
		errCode=NO_PIECE
	return(errCode)

def checkMustCapture(board,rowIndex,colIndex,length,dirI,dirJ,player,capt,hasPlayed,hasCaptured):
	errCode=NO_ERROR
	if(hasPlayed and hasCaptured):
		if(not capt):
			errCode=MUST_CAPTURE
	return(errCode)



def checkTooLongJump(board,rowIndex,colIndex,length,dirI,dirJ,player,capt):
	""" Verifie si le joeur essaie de se deplacer au dessus de plusieurs 
	piece

		Arguments :

			board (list) : plateau du jeu
			rowIndex (int) : index de la ligne ou se trouve le pion
			colIndex (int) : index de la colonne ou se trouve le pion
			length (int) : taille du deplacement
			dirI (int) : direction du mouvement dans les lignes
			dir J (int) : direction du mouvement des les colonnes

		Valeurs de retour:
		
			errCode (int) : Valeur du message d'erreur
	"""
	errCode=NO_ERROR
	if(capt):
		if (colorOfPawn(board[capt[0]+dirI][capt[1]+dirJ])==-player):
			errCode=TOO_LONG_JUMP
	return(errCode)


def checkPawnOnlyOneMove(board,rowIndex,colIndex,length):
	""" Verifie que seulement les dames bougent de plus de 2 cases.

		Arguments:

			board (list) : plateau du jeu
			rowIndex (int) : index de la ligne ou se trouve le pion
			colIndex (int) : index de la colonne ou se trouve le pion
			length (int) : taille du deplacement

		Valeur de retour : 

			 errCode (int) : Valeur du message d'erreur

	"""
	errCode=NO_ERROR
	if(abs(board[rowIndex][colIndex])==1 and length!=1):
		errCode=PAWN_ONLY_ONE_MOVE
	return (errCode)

def checkBadDirectionFormat(direction):
	""" Verifie si le joueur a entre une direction valide

		Argument:

			direction (str) : direction du mouvement ("L","R","LB" ou "RB")

		Valeur de retour : 
			 errCode (int) : Valeur du message d'erreur
	"""
	errCode=NO_ERROR
	if (direction not in ["L","R","LB","RB"]):
		errCode=BAD_DIRECTION_FORMAT
	return(errCode)

def checkOnlyKingGoBack(board,rowIndex,colIndex,direction,dirI,dirJ,length,player,capt):
	""" Verifie que seulement les dames peuvent aller en arriere sans capturer

		Arguments :

			board (list) : plateau du jeu
			rowIndex (int) : index de la ligne ou se trouve le pion
			colIndex (int) : index de la colonne ou se trouve le pion
			direction (str) : direction du mouvement ("L","R","LB" ou "RB")
			dirI (int) : direction du mouvement dans les lignes
			dir J (int) : direction du mouvement des les colonnes
			length (int) : taille du deplacement


		Valeur de retour : 

			 errCode (int) : Valeur du message d'erreur
	"""
	errCode=NO_ERROR
	if(abs(board[rowIndex][colIndex])==1 and len(direction)==2 and \
	not(capt)):
		errCode=ONLY_KING_GO_BACK
	return(errCode)

def checkSpaceOccupied(board,destI,destJ,rowIndex,colIndex,length,dirI,dirJ,player,capt):
	""" Verifie que la case choisie n'est pas deja prise.

		Arguments :

			board (list) : plateau du jeu
			destI (int) : ligne de destination
			destJ (int) : colonne de destination

		Valeur de retour : 

			errCode (int) : Valeur du message d'erreur

	"""
	errCode=NO_ERROR
	if ((capt and colorOfPawn(board[destI+dirI][destJ+dirJ])==player) or (board[destI][destJ]!=FREE_SPACE and colorOfPawn(board[destI][destJ])!=-player)):
		errCode=SPACE_OCCUPIED
	return(errCode)

def checkNoFreeWay(board,rowIndex,colIndex,destI,destJ,length,dirI,dirJ,player,capt):
	errCode=NO_ERROR
	if (abs(board[rowIndex][colIndex])>1):
		if(capt and destI+(dirI*length)!=capt[0] and destJ+(dirJ*length)!=capt[1]):
			errCode=NO_FREE_WAY
	return(errCode)

def colorOfPawn(pawn):
	if (pawn!=FREE_SPACE):
		pawn//=abs(pawn)
	return(pawn)


def checkMove(board,rowIndex,colIndex,direction,player,length=1,hasPlayed=False,hasCaptured=False):
	"""Verifie si le joueur fait un deplacement autorise
		
		Arguments:

			board (list) : plateau du jeu
			rowIndex (int) : index de la ligne ou se trouve le pion
			colIndex (int) : index de la colonne ou se trouve le pion
			direction (str) : "R", "L", "LB" ou "RB" 
			player (int) : 1 ou -1 en fonction du joueur
			length (int) : (default=1) longueur du deplacement
			hasPlayed (bool) : (default=False) True si le joueur a deja joue
			hasCaptured (bool) : (default=False) True si le joueur a deja capture 
		
		Valeurs de retour:

			errCode (int) : Valeur du message d'erreur

		"""
	errCode=checkBadDirectionFormat(direction)
	if(errCode==NO_ERROR):
		errCode=checkPawnOnlyOneMove(board,rowIndex,colIndex,length)
		if(errCode==NO_ERROR):
			errCode=checkOpponentPiece(board,rowIndex,colIndex,player)
			if(errCode==NO_ERROR):
				destI,destJ,dirI,dirJ,player,length=findDest(board,rowIndex,colIndex,direction,length)
				#print("(rowIndex,colIndex) "+str((rowIndex,colIndex)))
				#print("findDest "+str(findDest(board,rowIndex,colIndex,direction,length)))
				capt=findCapture(board,rowIndex,colIndex,length,dirI,dirJ,player)		
				errCode=checkCannotGoJumpOutside(board,destI,destJ,length,rowIndex,colIndex,dirI,dirJ,player)
				if (errCode==NO_ERROR):
					errCode=checkMustCapture(board,rowIndex,colIndex,length,dirI,dirJ,player,capt,hasPlayed,hasCaptured)
					if (errCode==NO_ERROR):
						errCode=checkCannotJumpOutside(board,rowIndex,colIndex,length,dirI,dirJ,player)
						if (errCode==NO_ERROR):
							errCode=checkNoPiece(board,rowIndex,colIndex)
							if(errCode==NO_ERROR):
								errCode=checkOnlyKingGoBack(board,rowIndex,colIndex,direction,dirI,dirJ,length,player,capt)
								if(errCode==NO_ERROR):
									errCode=checkSpaceOccupied(board,destI,destJ,rowIndex,colIndex,length,dirI,dirJ,player,capt)
									if(errCode==NO_ERROR):
										errCode=checkTooLongJump(board,rowIndex,colIndex,length,dirI,dirJ,player,capt)
										if(errCode==NO_ERROR):
											errCode=checkNoFreeWay(board,rowIndex,colIndex,destI,destJ,length,dirI,dirJ,player,capt)
	return(errCode)


def noMorePawn(board,player):
	""" Verifie que le joueur a encore des pions sur le plateau

		Arguments :

			board (list) : plateau du jeu
			player (int) : le joueur

		Valeur de retour :

			res (bool) : False si le joueur a encore des pions, sinon True
	"""
	res=True
	for row in board:
		for col in row:
			if(colorOfPawn(col)==player):
				res=False
				break
	return(res)


def cannotMove(board,player):
	""" Verifie si un joueur peut encore bouger un pion.

		Arguments :

			board (list) : plateau du jeu
			player (int) : le joueur

		Valeur de retour :

			res (bool) : True si le joueur est bloque, sinon False		 

	"""
	res=True
	directions=["L","LB","R","RB"]
	for row in range(DIMENSION):
#		if(res is False):
#			break
		for col in range(DIMENSION):
#			if(res is False):
#				break
			if (board[row][col]!=FREE_SPACE):
					for direction in directions:
#						if(res is False):
#							break
						check=checkMove(board,row,col,direction,\
						player)
						if(check==NO_ERROR):
							#print(row)
							#print(col)
							#print(direction)
							return(False)

	return res


def checkEndOfGame1(board,player):
	printBoard(board,player)
	moves		= {WHITE_PLAYER:False,	BLACK_PLAYER:False}
	pieces	= {WHITE_PLAYER:0,		BLACK_PLAYER:0}
	for row in range(len(board)):
		for col in range(len(board)):
			if(not isFree(board,row,col)):# a piece in x,y
				color = playerColor(board[row][col])
				pieces[color] = pieces[color] + 1
				if(not moves[color]):
					for direction in ('L','R','LB','RB'):
						if(checkMove(board,row,col,direction,color) == NO_ERROR):
							moves[color] = True
	if(pieces[WHITE_PLAYER]+pieces[BLACK_PLAYER] == 0): return 0# never happen
	if(pieces[WHITE_PLAYER] == 0): return BLACK_PLAYER
	if(pieces[BLACK_PLAYER] == 0): return WHITE_PLAYER
	# else they have pieces
	if((not moves[player]) and (not moves[-player])): return 0
	return False if(moves[player])else -player


def isFree(board,row,col):
	return board[row][col] == FREE_SPACE

def playerColor(value):
	return value/abs(value);

def checkEndOfGame(board,player):
	"""Verifie si un pion peut se deplacer vers la gauche ou la droite
		
		Arguments:

			board (list) : plateau du jeu
			player (int) : 1 ou -1 en fonction du joueur

		Valeurs de retour:

			res : 0 si match-nul, 
				  -1 si le joueur noir a gagne, 
				  1 si le joueur blanc a gagne, 
				  False si le jeu n'est pas termine

		"""
	
	#printBoard(board,player)

	if (not(noMorePawn(board,player))):#"""si j'ai des pions"""
		print("j'ai encore des pions")
		if (cannotMove(board,-player)):#""" si l'autre ne peux pas jouer"""
			print("l'autre ne peut plus bouger")
			if (cannotMove(board,player)):# """ si je peux pas jouer non plus"""
				print(" je ne peux plus bouger non plus")
				res=0#""" Match-nul"""
			else:#""" si je peux jouer """
				print("je peux encore bouger et j'ai gagner")
				res=player#""" J'ai gagner"""
		elif(not(cannotMove(board,player))):#""" Si l'autre peux jouer """
			print("je peux encore bouger et l'autre peux jouer")
			res=False#""" Ca continue"""
		else:
			print("l'autre peux jouer et je peux pas jouer")
			res=-player
	elif(noMorePawn(board,-player)):
		print("l'autre n'a plus de pions")
		res=0
	else:
		#""" si j'ai pas de pions"""
		print("je n'ai plus de pions")
		res=-player#""" l'autre a gagner"""
	print("res "+str(res))
	print("player "+str(player))
	return(res)

def changeColToNumbers(letter):
	"""Transforme les lettre de la colonne choisie en chiffre
		
		Arguments:
		letter (str): lettre de la colonne

		Exemples:
		>>>changeColToNumbers("d")
		4
		>>>changeColToNumbers("a")
		1
	"""
	return(ord(letter)-96)

def initIndex(coord):
	"""Retourne les coordonnees entrees par le joueur pour 
		qu'elles coincident avec les index du plateau
		Arguments:

		coord (int): coordonee de la ligne ou de la colonne

		Valeurs de retour:
		int : la coordonnee decrementee de 1

		Exemples:
		>>> print(initIndex(1))
		0
		>>> print(initIndex(5))
		4
	"""
	return(coord-1)

def demandeCoup():
	""" Demande a l'utilisateur son prochain coup.

		Valeur de retour:

			rowIndex (int) : index de la ligne ou se trouve le pion
			colIndex (int) : index de la colonne ou se trouve le pion
			direction (str) : direction du mouvement ("L","R","LB" ou "RB")
			length (int) : taille du deplacement


	"""
	rowIndex=initIndex(int(input("row = ")))
	colIndex=initIndex(changeColToNumbers(input("col = ")))
	direction=input("direction = ")
	length=int(input("length = "))
	return(rowIndex,colIndex,direction,length)


def save(fileName,board,player):
	"""Cette fonction sauvegarde la partie en cours

		Arguments :

			fileName (str) = nom du fichier de sauvegarde
			board (list) : plateau du jeu
			player (int) : 1 ou -1 en fonction du joueur

	"""	
	doc=open(fileName,"w")
	contenu=""
	contenu+=str(player)+"\n"
	contenu+=str(len(board))+"\n"
	for i in board:
		for j in i[:-1]:
			if (j<0):
				contenu+=str(j)+" "
			else:
				contenu+=str(j)+"  "
		contenu+="\n"

	doc.write(contenu)
	doc.close()


def tour(player,board,hasPlayed,hasCaptured):
	""" Cette fonction s'assure du bon deroulement du tour.

		Arguments :

			player (int) : 1 ou -1 en fonction du joueur
			board (list) : plateau du jeu
			hasPlayed (bool) : (default=False) True si le joueur a deja joue
			hasCaptured (bool) : (default=False) True si le joueur a deja capture 

		Valeur de retour : 

			player (int) : 1 ou -1 en fonction du joueur
			hasCaptured (bool) : (default=False) True si le joueur a deja capture 
			hasPlayed (bool) : (default=False) True si le joueur a deja joue

			
	"""
	rowIndex,colIndex,direction,length=demandeCoup()
	while(checkMove(board,rowIndex,colIndex,direction,player,length=length\
	,hasPlayed=hasPlayed,hasCaptured=hasCaptured)!=NO_ERROR):
		rowIndex,colIndex,direction,length=demandeCoup()
	dest,capt=movePiece(board,rowIndex,colIndex,direction)
	hasPlayed=True
	if (capt):
		hasCaptured=True
	end=input("Avez vous fini votre tour ? (Y/N) :")
	if (end=="Y"):
		for i in range(DIMENSION):
			becomeKing(board,0,i)
			becomeKing(board,9,i)
		player=-player
	else:
		player,hasCaptured,hasPlayed=tour(player,board,hasPlayed,hasCaptured)
	return(player,hasCaptured,hasPlayed)
