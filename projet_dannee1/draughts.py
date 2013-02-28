"""
INFO-F106 : Projets d’Informatique 1
fichier : draughts.py

Malik Fassi Fihri 
Matricule : 000364845

"""
from draughtsFunctions import *
from config import *


def main():
	"""Fonction qui lance le jeu"""
	player=WHITE_PLAYER
	board=initBoard(DIMENSION)

	while(checkEndOfGame(board,player) is not 0 or checkEndOfGame(board,player)\
	 is not abs(player)):
		hasPlayed=False
		hasCaptured=False
		printBoard(board,player)
		
		save=input("Voulez vous charger une partie ou sauvegarder une partie\
		 ou proposer une partie nulle a l'adversaire ? (C = charger, S = sauv\
		 egarder, P = partie nulle, N = non) : ")
		if (save=="N"):
			player,hasCaptured,hasPlayed=tour(player,boars,hasPlayed,hasCaptured)
		elif (save=="Y"):
			save('sauvegarde.dat',board,player)
		elif (save=="P")
			P1=input("Partie nulle ? (Y/N) ")
			if (P1==Y):
				P2=input("Partie nulle ? (Y/N) ")
				if(P2==P1):
					break
	print("FIN DE PARTIE")
main()