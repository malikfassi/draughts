# -*- coding: utf8 -*-

from math import *
from os.path import exists
from config import *

def checkEndOfGame(board,player):
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

def directionToCoordinates(board,player,row,col,direction,moves):
	if(isFree(board,row,col)): return errorCode(NO_PIECE)
	if(playerColor(board[row][col]) != player): return errorCode(OPPONENT_PIECE)
	if(moves>1 and (not isKing(board,row,col))): return errorCode(PAWN_ONLY_ONE_MOVE)
	#
	direction	= direction.strip().lower();
	goBack		= badFormat = False
	color			= playerColor(board[row][col])
	#
	if(len(direction)>1):# go back
		goBack = direction[1] == 'b'
		# if direction start with L/R but not followed by B, bad format
		badFormat = not(goBack)
	#
	#compute position
	new = computeDirection(row,col,direction,color,moves);
	if(isinstance(new,bool)):
		badFormat = True
	#
	if(badFormat): return errorCode(BAD_DIRECTION_FORMAT)
	#
	newY,newX = new
	if(not outside(board,newY,newX)):
		# case is free, No opponent
		if(isFree(board,newY,newX)):
			if(goBack and not(isKing(board,row,col))): return errorCode(ONLY_KING_GO_BACK);
			elif(countFree(board,row,col,direction)>=moves): return (NO_ERROR,newY,newX)
			else: return errorCode(NO_FREE_WAY);
		else:
		# case busy
			if(not isFree(board,newY,newX)):
				if(not isOpponent(board[row][col],board[newY][newX])): return errorCode(SPACE_OCCUPIED);
				else: # jump over the opponent
					newY,newX = computeDirection(newY,newX,direction,color);
					if(outside(board,newY,newX)): return errorCode(CANNOT_JUMP_OUTSIDE);
					elif(not isFree(board,newY,newX)): return errorCode(TOO_LONG_JUMP);
					elif(countFree(board,row,col,direction)>=moves-1):return (NO_ERROR,newY,newX)
					else: return errorCode(NO_FREE_WAY);
	# else new position is outside
	return errorCode(CANNOT_GO_OUTSIDE)

def countCapture(board,row,col,direction):
	moves = countFree(board,row,col,direction)
	color = playerColor(board[row][col])
	# move to the end of free cases and try one move again
	moves = moves + 1
	row,col = computeDirection(row,col,direction,color,moves);
	#
	if((not outside(board,row,col)) and isOpponent(color,board[row][col])):
		row,col = computeDirection(row,col,direction,color);
		if((not outside(board,row,col)) and isFree(board,row,col)):
			return moves
	# else not an opponent, or outside or too many opponents
	return -1

def countFree(board,row,col,direction,color=None,moves=0):
	if(color == None):
		color = playerColor(board[row][col])
	y,x = computeDirection(row,col,direction,color);
	# if it is inside and free space, continue
	if((not outside(board,y,x)) and isFree(board,y,x)):
		return countFree(board,y,x,direction,color,moves+1)
	# else return value of the counter
	return moves

def errorCode(code):
	return code,None,None

def checkMove(board,fromY,fromX,direction,player,moves=1,hasPlayed=False,hasCaptured=False):
	errCode,toY,toX = directionToCoordinates(board,player,fromY,fromX,direction,moves)
	if(errCode == NO_ERROR):
		if(hasPlayed):# if the player has started a rafle
			if(not hasCaptured): return MUST_CAPTURE# he never can continue his rafle
			# else check if the current move is a capture move
			row,col = computeDirection(toY,toX,reverseDirection(direction),player)
			if((not jump(fromX,toX)) or isFree(board,row,col)): return MUST_CAPTURE
	return errCode

def movePiece(board,fromY,fromX,direction,moves=1):
	player		= playerColor(board[fromY][fromX])
	_,toY,toX	= directionToCoordinates(board,player,fromY,fromX,direction,moves);
	# move
	board[toY][toX]		= board[fromY][fromX];
	board[fromY][fromX]	= FREE_SPACE
	capture					= None
	if(jump(fromX,toX)):
		direction = reverseDirection(direction)
		row,col = computeDirection(toY,toX,direction,player)
		if(not isFree(board,row,col)):# if free, just a jump on a free way
			capture = (row,col)
	return ((toY,toX),capture)

def becomeKing(board,row,col):
	if(isFree(board,row,col)): return
	player = playerColor(board[row][col])
	if(row != (0 if(player == WHITE_PLAYER) else len(board)-1)): return
	if(playerColor(board[row][col])!=player): return
	board[row][col] = player*(abs(board[row][col])+1)

def computeDirection(row,col,direction,player,moves=1):
	direction = direction.lower()
	row = row + player*(moves if(len(direction)>1) else -moves);
	if(direction[0] == 'l'): col = col+(-moves*player)
	elif(direction[0] == 'r'): col = col+(moves*player)
	else: return False
	return int(row),int(col)

def reverseDirection(direction):
	direction = direction.upper()
	if(len(direction)>1): return 'L' if(direction == 'RB')else 'R'
	return 'RB' if(direction == 'L')else 'LB'

def jump(index1,index2):
	if(index1<index2):
		return jump(index2,index1)
	return abs(index1-index2)>1

def capture(board,row,col):
	board[row][col] = FREE_SPACE

def isFree(board,row,col):
	return board[row][col] == FREE_SPACE
	
def initBoard(dimension):
	nPlayableRows = int((dimension-1)/2)
	board = [ dimension*[0] for array in range(dimension) ]
	for odd in range(2):
		for row in range(odd,nPlayableRows,2):
			for col in range(odd,dimension,2):
				board[row][col-1]					= BLACK_PLAYER
				board[dimension-1-row][col]	= WHITE_PLAYER
	return board

def printBoard(myboard,toplay):
	dimension = len(myboard)
	order = range(dimension) if(toplay==WHITE_PLAYER) else range(dimension-1,-1,-1)
	for row in order:
		#line = ''
		for col in order:
			char = WHITE_SQUARE
			if(myboard[row][col]):# filled case
				# define the color of player
				char = ''
				if(playerColor(myboard[row][col]) == WHITE_PLAYER): char = char + 'WHITE_'
				else: char = char + 'BLACK_'
				# define char for simple piece or king
				if(isKing(myboard,row,col)): char = char + 'KING'
				else: char = char + 'PAWN'
				# evaluate the name of variable contained in config 
				char = eval(char)
			elif((row+col)%2): char = BLACK_SQUARE# update if black case and no piece
			print(char,sep='',end=' ')
		print('| ',row+1,sep='')
	for i in order: print('-',sep='',end=' ')
	print()
	for pos in order : print(chr(pos+ord('a')),sep='',end=' ')
	print()

def strerr(errCode):
	return ({
		PAWN_ONLY_ONE_MOVE	: 'only king can play more than 1 move',
		BAD_DIRECTION_FORMAT	: 'error only L,R,LB and RB',
		ONLY_KING_GO_BACK		: 'only king can go back',
		SPACE_OCCUPIED			: 'one of your pieces is in this direction',
		CANNOT_JUMP_OUTSIDE	: 'you cannot jump outside',
		TOO_LONG_JUMP			: 'you cannot jump here, too long jump',
		CANNOT_GO_OUTSIDE		: 'you cannot go outside',
		NO_FREE_WAY				: 'the path is not free',
		NO_PIECE					: 'invalid position',
		OPPONENT_PIECE			: 'this is not your piece',
		MUST_CAPTURE			: 'you must capture a piece if you want to continue your rafle'
	}[errCode])

def outside(board,row,col):
	return row<0 or col<0 or row>= len(board) or col>= len(board)

def isKing(board,row,col):
	return abs(board[row][col])>1

def playerColor(value):
	return value/abs(value);

def isOpponent(myValue,value):
	return (playerColor(myValue) * playerColor(value)) < 0

def save(filename,myboard,player):
	dimension = len(myboard)
	f = None
	try:
		f = open(filename, "w")
		f.write(str(player)+"\n")
		f.write(str(dimension)+"\n")
		list(map(lambda sub:f.write(' '.join(map(lambda x:str(x),sub))+"\n"),myboard))
		return True
	except:
		raise
	finally:
		if(f != None):
			f.close();

def load(filename):
	f = None
	board = []
	try:
		f = open(filename, "r")
		player		= int(f.readline())
		dimension	= int(f.readline())
		#
		board = list(map(lambda i:
						list(map(lambda x:int(x),f.readline().split())),
						range(dimension)))
		return player,board
	except:
		raise
	finally:
		if(f != None):
			f.close();
