from tkinter import *



class Parent(Tk):
	#def __init__(self):

	#	self.body=Tk()

	def getRoot(self):
		return(self.body)

	def setTitle(self,title):
		self.title(title)
	
	def run(self):
		self.mainloop()

class Drawing:
	def __init__(self,root,width,height):
		self.zone=Canvas(root, width=width, height=height)

	def put(self,root,row,col):
		self.zone.grid(root,row=row,column=col)

	def getDrawing(self):
		return(self.zone)

	def rectangle(self,coordX1,coordY1,coordX2,coordY2,color):
		self.zone.create_rectangle(coordX1,coordY1,coordX2,coordY2,fill=color, outline="black")

	def circle(self,coordX1,coordY1,coordX2,coordY2,color):
		self.zone.create_oval(coordX1,coordY1,coordX2,coordY2,fill=color,outline="black")

if __name__=="__main__":
	root=Parent()
	root.setTitle("Draughts")
	board=Drawing(root,400,400)
	size=40
	logicBoard=[[0, -1, 0, -1, 0, -1, 0, -1, 0, -1], 
				[-1, 0, -1, 0, -1, 0, -1, 0, -1, 0],
				[0, -1, 0, -1, 0, -1, 0, -1, 0, -1], 
				[-1, 0, -1, 0, -1, 0, -1, 0, -1, 0], 
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
				[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
				[0, 1, 0, 1, 0, 1, 0, 1, 0, 1], 
				[1, 0, 1, 0, 1, 0, 1, 0, 1, 0], 
				[0, 1, 0, 1, 0, 1, 0, 1, 0, 1], 
				[1, 0, 1, 0, 1, 0, 1, 0, 1, 0]]
	DIMENSION=10
	for i in range(DIMENSION):
		for j in range(DIMENSION):
			coordX1 = (i * size)
			coordY1 = (j * size)
			coordX2 = coordX1 + size
			coordY2 = coordY1 + size
			if(not(i%2==j%2)):#if the square is black (on the board)
				color="black"
			else:
				color="white"
			case=Drawing(board.getDrawing(),40,40)
			case.rectangle(coordX1,coordY1,coordX2,coordY2,color)
			case.getDrawing().pack()
			if(logicBoard[i][j]>0):
				pawnColor="white"
			elif(logicBoard[i][j]<0):
				pawnColor="black"
			if (not(i%2==j%2)):
				pawn=Drawing(case.getDrawing(),40,40)
				pawn.circle(0,0,30,30,pawnColor)
				pawn.getDrawing().pack()

	board.getDrawing().pack()
	root.run()
