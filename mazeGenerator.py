import pygame, random
# Started on 3/22/2020 7:54 PM and completed on 3/23/2020 at 6:38 PM. Revisied on 4/26/2020 at 10:00-12:00 AM.

pygame.init()

#Define game variables.
backgroudColour = (0,0,0)

mazeArray = []
wallArray = []

class pathStep():
	def __init__(self, col, row):
		self.col = col
		self.row = row
		self.topWall = True
		self.botWall = True
		self.lefWall = True
		self.rigWall = True


def positionInArray(coordinates): # [c, r]
	colPos = coordinates[0]
	rowPos = coordinates[1]

	if colPos >= 0 and colPos <= COLS-1 and rowPos >= 0 and rowPos <= ROWS-1:
		return True
	else: return False


def testForVal(coordinates): # [c, r]
	global mazeArray, wallArray
	colPos = coordinates[0]
	rowPos = coordinates[1]

	if positionInArray(coordinates):
		if mazeArray[rowPos][colPos] > 0:
			return False
		if mazeArray[rowPos][colPos] == 0:
			# It is okay to place here...
			return True


def getDirList(coordinates, direction):
	possDirList = [[0, -1], [0, 1], [-1, 0], [1, 0]] # U, D, L, R#possDirList = ['UP', 'DOWN', 'LEFT', 'RIGHT'] # U, D, L, R
	
	# Dont use direction (filter it out).
	for elem in possDirList:
		if elem == direction:
			possDirList.remove(elem)



	if wallArray[coordinates[0]][coordinates[1]].topWall == True:
		for elem in possDirList:
			if elem == [0, -1]:
				possDirList.remove(elem)

	if wallArray[coordinates[0]][coordinates[1]].botWall == True:
		for elem in possDirList:
			if elem == [0, 1]:
				possDirList.remove(elem)
		
	if wallArray[coordinates[0]][coordinates[1]].lefWall == True:
		for elem in possDirList:
			if elem == [-1, 0]:
				possDirList.remove(elem)
		
	if wallArray[coordinates[0]][coordinates[1]].rigWall == True: 
		for elem in possDirList:
			if elem == [1, 0]:
				possDirList.remove(elem)
		

	newList = list(filter(lambda x: (x != 0), possDirList))

	return newList


def testForEdge(coordinates): # [c, r]
	global mazeArray, wallArray
	colPos = coordinates[0]
	rowPos = coordinates[1]

	if colPos < 0 or colPos > COLS-1 or rowPos < 0 or rowPos > ROWS-1:
		return False
	else:
		return True


def getNewCoords(coordinates, direction):
	newC = coordinates[0] + direction[0]
	newR = coordinates[1] + direction[1]
	newCoords = [newC, newR]

	return newCoords


def getDirectsList(coordinates, direction): # [c, r], [-1/1/0, -1/1/0]
	global mazeArray
	possDirList = [[0, -1], [0, 1], [-1, 0], [1, 0]] # U, D, L, R

	# Dont use direction (filter it out).
	for elem in possDirList:
		if elem == direction:
			possDirList.remove(elem)

	# Dont use direction (filter it out). You may run into problems of the range not working, but it should always be the four directions minus the one passed through.
	for i in range(4-1):

		if positionInArray(getNewCoords(coordinates, possDirList[i])) and not testForVal(getNewCoords(coordinates, possDirList[i])):
			possDirList[i] = 0
		
		elif not testForEdge(getNewCoords(coordinates, possDirList[i])):
			possDirList[i] = 0

	newList = list(filter(lambda x: (x != 0), possDirList))

	# Should only leave the valid directions.
	return newList


def oppositeDirection(direction):
	for elem in range(2):
		direction[elem] = -1 * int(direction[elem])
	
	return direction

def setWalls(cameFrom, dirGoing, c, r):
	global wallArray
	# The new direction will be: possibleDirections[0], the older direction is oppositeDirection(direction).
	directionGoing = dirGoing
	cameFromDir = cameFrom

	if cameFromDir != None:
		if cameFromDir == [0, -1]: # Up
			wallArray[r][c].botWall = False
		elif cameFromDir == [0, 1]: # Down
			wallArray[r][c].topWall = False
		elif cameFromDir == [-1, 0]: # Left
			wallArray[r][c].rigWall = False
		elif cameFromDir == [1, 0]: # Right
			wallArray[r][c].lefWall = False

	if directionGoing != None:
		if directionGoing == [0, -1]: # Up
			wallArray[r][c].topWall = False
		elif directionGoing == [0, 1]: # Down
			wallArray[r][c].botWall = False
		elif directionGoing == [-1, 0]: # Left
			wallArray[r][c].lefWall = False
		elif directionGoing == [1, 0]: # Right
			wallArray[r][c].rigWall = False
	

def newBranch(coordinates, direction, number, path, resetWalls):
	global mazeArray, wallArray
	
	c, r = coordinates
	if resetWalls:
		wallArray[r][c].topWall = True
		wallArray[r][c].botWall = True
		wallArray[r][c].lefWall = True
		wallArray[r][c].rigWall = True
	
	possibleDirections = getDirectsList(coordinates, oppositeDirection(direction)) # Don't want it to go backwards.
	cameFromDir = oppositeDirection(direction)
	setWalls(cameFromDir, None, c, r)
	
	mazeArray[r][c] = number
	pathList = path
	pathList.append([c,r])

	if len(possibleDirections) > 0:
		random.shuffle(possibleDirections)
		newC = getNewCoords(coordinates, possibleDirections[0])

		if testForVal(newC): # If this spot is blank
			directionGoing = possibleDirections[0]
			
			setWalls(None, directionGoing, c, r)
		
			newBranch(newC, possibleDirections[0], number + 1, pathList, True)

	elif len(possibleDirections) == 0:
		for i in range(len(pathList), -1, -1):
			theseCoordinates = pathList[i-1]
			thisSpotPossibilities = getDirectsList(theseCoordinates, oppositeDirection(direction))
			if len(thisSpotPossibilities) > 0:
				newBranch(theseCoordinates, random.choice(thisSpotPossibilities), number + 1, pathList, False)

		return True # If this is reached, the maze is complete.

#pathList = [[0,0]]
def generateMaze(size):
	global mazeArray, wallArray
	global ROWS
	global COLS
	ROWS = size
	COLS = size

	mazeArray = []
	wallArray = []

	for rows in range(ROWS):
		thisRow = []
		thisRowalso = []
		for cols in range(COLS):
			thisRow.append(0)
			thisRowalso.append(pathStep(cols, rows))

		mazeArray.append(thisRow)
		wallArray.append(thisRowalso)
	
	startX, startY = random.randint(0, size-1), random.randint(0, size-1)
	newBranch([startX,startY], [0,1], 1, [[startX,startY]], True)

	# Make sure the border is outlined
	for s in range(ROWS):
		wallArray[s][0].lefWall = True
		wallArray[s][size-1].rigWall = True 
		wallArray[0][s].topWall = True
		wallArray[size-1][s].botWall = True 

	# f = open('store.pckl', 'wb')
	# pickle.dump(wallArray, f)
	# f.close()
	# f = open('store.pckl', 'rb')
	# mazeArray = pickle.load(f)
	# f.close()

	return mazeArray, wallArray
