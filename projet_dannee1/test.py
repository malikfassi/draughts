
from draughtsFunctions import * 
from config import *

def initBoard():
	myboard=[]
	rangeDimension=range(10)
	for i in rangeDimension:
		myboard.append([])
		for j in rangeDimension:
			myboard[i].append(0)
	myboard[5][2]=1
	myboard[4][3]=-1
	return(myboard)


def main():
	"""Fonction qui lance le jeu"""
	player=WHITE_PLAYER
	board=initBoard()

	while(checkEndOfGame(board,player) is not 0):
		
		print(board)
		printBoard(board,player)
		rowIndex=initIndex(int(input("row = ")))
		colIndex=initIndex(changeColToNumbers(input("col = ")))
		direction=input("direction = ")
		movePiece(board,rowIndex,colIndex,direction)
		player=-player
main()