#!/usr/bin/python3
# -*- coding: utf8 -*-
from draughtsFunctions import *
import sys
from os.path import *

def stdread(lower=False):
	print("=>",sep="",end="")
	return input().lower()

def nameOf(player):
	return "WHITE" if(player == WHITE_PLAYER)else "BLACK"

def promptDirection(askNumberOfMoves=False):
	print("Select a direction, please.");
	print("\tL, R, LB, RB or S ((L)eft, (R)ight, (B)ack, (S)top).")
	direction = stdread(True)
	if(askNumberOfMoves and direction != 's'):
		try:
			print("Give the number of successive moves")
			moves = int(stdread())
			if(moves<1): raise ValueError("invalid number of moves, must be > 1 : '",moves,"'")
			return direction,moves
		except ValueError:
			print("Not a correct number of moves.")
			return promptDirection(askNumberOfMoves)
	return direction,1

def isDAT(filename):
	try:
		return filename.lower().index('.dat')>0
	except ValueError:
		return False

def prompt(board,player):
	print(nameOf(player),"player, type one of:")
	print("\t- 'r' to send an interrupt request (ask to the other player)")
	print("\t- 's' to save the game")
	print("\t- 'l' to load a game")
	print("\t- 'p' to print board")
	print("\t- a character from 'a' to 'j' to select a piece (x-coordinate)")
	choice = stdread(True)
	if(len(choice)==1 and ((choice>='a' and choice<='j') or (choice in ('r','s','l')))):
		if(choice == 'r'):
			print(nameOf(player)," send an interrupt request.")
			print(nameOf(nextPlayer(player))," player, do you accept? ([y]es/[n]o)")
			if(stdread(True) in ('y','yes')):
				print("Accepted. Interrupt.")
				return False,0,-1
			else: print("Refused. Continue")
		elif(choice in ('l','s')):
			print("Give a path to the file ending by '.dat', please.")
			fileName = stdread()
			if(isDAT(fileName)):
				saveAction = choice == 's'
				loadAction = not saveAction
				if(isfile(fileName)):
					if(saveAction):
						print("Are you sure to overwrite? ([y]es/[n]o)")
						saveAction = stdread(True) in ('y','yes')
				elif(loadAction): print("Cannot load, file not found.")
				if(saveAction):
					try:
							save(fileName,board,player)
							print("file saved.")
					except IOError:	print("I/O Error")
				elif(loadAction):
					try:
						player,board = load(fileName)
						print("file loaded.")
						return False,player,board
					except TypeError:	print("Bad format")
					except IOError:	print("I/O Error")
				else: print("Abording")
			else:
				print("Not a *.dat file")
		else:
			print("Enter the y-coordinate to select the piece.")
			try:
				y = int(stdread());
				if(y<1 or y>10): raise ValueError("invalid number to select a row : '",y,"'")
				return True,y-1,ord(choice)-ord('a')
			except ValueError:	print("Not a correct row number.");
	elif(choice == 'p'): printBoard(board,player)
	else: print("Wrong input, please try again")
	return prompt(board,player)

def nextPlayer(player):
	return (-1)*player

def main():
	board		= initBoard(DIMENSION)
	player	= WHITE_PLAYER
	finished	= False
	#
	while(isinstance(finished,bool) and (not finished)):#not finished is not useful
		printBoard(board,player)
		normalInput,row,col = prompt(board,player)
		if(normalInput):
			playAgain = True
			captured = False
			played = False
			while(playAgain):
				direction,moves = promptDirection(isKing(board,row,col))
				if(direction == 's'):
					playAgain = False
					if(not played):
						print('Player want to select another piece.')
						player = nextPlayer(player)
				else:
					error = checkMove(board,row,col,direction,player,moves,played,captured)
					if(error == NO_ERROR):
						dst,captured = movePiece(board,row,col,direction,moves)
						played = True
						if(captured != None):
							y,x = captured
							capture(board,y,x)
							captured = True
						row,col = dst
						if(not captured): playAgain = False
						printBoard(board,player)
					else:
						print('Error: '+strerr(error)+'.')
						if(error in (NO_PIECE,OPPONENT_PIECE)):
							playAgain = False
							player = nextPlayer(player)
				finished = checkEndOfGame(board,player)
				if(isinstance(finished,int) and finished!=0): playAgain = False
			becomeKing(board,row,col)
			player = nextPlayer(player)
			finished = checkEndOfGame(board,player)
		elif(row != 0): player,board = row,col# game loaded
		else: finished = 0 # Abording (interrupt request)
	player = nextPlayer(player)
	print('Draw game, both players are blocked' if(finished == 0) else (nameOf(player)+" wins"))

if __name__ == '__main__':
	main()
