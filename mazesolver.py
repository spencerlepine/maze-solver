import pygame, sys, random
from mazeGenerator import generateMaze

# Started on July 4th, 2020, at 3:45 PM, finished on 7/11/2020 at 12:05 PM. 

pygame.init()

# Define variables.
backgroundColour = (0, 0, 0)

runLoop = True
mazeSIZE = 10
tileSize = 30
ROWS, COLS = mazeSIZE, mazeSIZE
w_width = tileSize + (tileSize * mazeSIZE)
w_height = tileSize + (tileSize * mazeSIZE) + tileSize

mazeArray, wallArray = generateMaze(mazeSIZE)
pathArray = []
pathArrayTemp = []
testedArray = []

for rows in range(ROWS):
	thisRow = []
	for cols in range(COLS):
		thisRow.append(0)

	testedArray.append(thisRow)

screen = pygame.display.set_mode((w_width, w_height))
pygame.display.set_caption("Maze Solver")
# logo = pygame.image.load("images/icon.jpg")
# pygame.display.set_icon(logo)

# Define mouse event variable.
cursorEvent = pygame.event.poll()

# Set up the game clock.
clock = pygame.time.Clock()

# Reusable function to return desired text object, which can be displayed.
def drawText(labelText, xPos, yPos, labelType, size):
	color = (120, 111, 102)
	if labelType == "gray":
		color = (255, 255, 255)
	font = pygame.font.Font('freesansbold.ttf', size)
	text = font.render(labelText, True, color)
	textRect = text.get_rect()
	#textRect.center = (xPos // 2, yPos // 2)
	textRect.center = (xPos, yPos)
	return screen.blit(text, textRect)


def positionInArray(coordinates): # [c, r]
	colPos = coordinates[0]
	rowPos = coordinates[1]

	if colPos >= 0 and colPos <= COLS-1 and rowPos >= 0 and rowPos <= ROWS-1:
		return True
	else: return False


def getNewCoords(coordinates, direction):
	newC = coordinates[0] + direction[0]
	newR = coordinates[1] + direction[1]
	newCoords = [newC, newR]

	return newCoords


def testForVal(coordinates): # [c, r]
	global testedArray

	colPos = coordinates[0]
	rowPos = coordinates[1]

	if positionInArray(coordinates):
		if testedArray[rowPos][colPos] == 0:
			return False
		if testedArray[rowPos][colPos] > 0:
			# It is okay to place here...
			return True


def getDirList(coordinates):#, direction
	possDirList = []#[[0, -1], [0, 1], [-1, 0], [1, 0]] # U, D, L, R

	if positionInArray(coordinates):

		if wallArray[coordinates[1]][coordinates[0]].topWall != True and not testForVal(getNewCoords(coordinates, [0, -1])):
			possDirList.append([0,-1])
			if coordinates[1] > 0 and wallArray[coordinates[1]-1][coordinates[0]].botWall == True:
				possDirList.pop()
					
		if wallArray[coordinates[1]][coordinates[0]].botWall != True and not testForVal(getNewCoords(coordinates, [0, 1])):
			possDirList.append([0,1])
			if coordinates[1] < ROWS-1 and wallArray[coordinates[1]+1][coordinates[0]].topWall == True:
				possDirList.pop()
			
		if wallArray[coordinates[1]][coordinates[0]].lefWall != True and not testForVal(getNewCoords(coordinates, [-1, 0])):
			possDirList.append([-1,0])
			if coordinates[0] > 0 and wallArray[coordinates[1]][coordinates[0]-1].rigWall == True:
				possDirList.pop()
			
		if wallArray[coordinates[1]][coordinates[0]].rigWall != True and not testForVal(getNewCoords(coordinates, [1, 0])): 
			possDirList.append([1, 0])
			if coordinates[0] < COLS-1 and wallArray[coordinates[1]][coordinates[0]+1].lefWall == True:
				possDirList.pop()

	else:
		possDirList = [0,0,0,0]

	newList = list(filter(lambda x: (x != 0), possDirList))

	return newList


targetCoords = [random.randint(0, COLS), random.randint(0, ROWS)]
while targetCoords == [0,0]:
	targetCoords = [random.randint(0, COLS), random.randint(0, ROWS)]

def getPreffered(coordinates):
	global targetCoords

	possibleDirections = [[0, -1], [0, 1], [-1, 0], [1, 0]] # U, D, L, R

	thisX = coordinates[0]
	thisY = coordinates[1]
	targX = targetCoords[0]
	targY = targetCoords[1]

	getXDifference = -1 * (thisX - targX)
	getYDifference = -1 * (thisY - targY)

	if getXDifference > 0:
		XDif = 1
	elif getXDifference < 0:
		XDif = -1

	if getYDifference > 0:
		YDif = 1
	elif getYDifference < 0:
		YDif = -1

	# [getXDifference, getYDifference]

	if abs(getXDifference) > abs(getYDifference):
		return [XDif, 0]
	elif abs(getYDifference) > abs(getXDifference):
		return [0, YDif]
	elif abs(getYDifference) == abs(getXDifference):
		return [0, YDif]

attempts = 0
def solveMaze(coordinates, pathList): #[0, 0], [[0, 0]], [[0, 0]], [0, 0], Bool
	global mazeArray, targetCoords, pathArray, attempts, limit, pathArrayTemp, testedArray

	pathArrayTemp = pathList
	attempts += 1

	# Add this spot to tested.
	testedArray[coordinates[1]][coordinates[0]] = 1

	# Test if we have found are target, if not, just keep trying.
	if coordinates == targetCoords:#9
		print('SOLVED in: ' + str(attempts) + ' steps.')
		pathList.append(coordinates)
		pathArrayTemp = pathList
		return True


	possibleDirections = getDirList(coordinates)

	if len(possibleDirections) > 0:
		# Use a function to aim towards the target, reducing the steps since it is less random.
		prefDir = getPreffered(coordinates)
		if prefDir in possibleDirections:
			directionChosen = prefDir
		else:
			directionChosen = random.choice(possibleDirections)

		# (Add these coordinates to patharray)
		pathList.append(coordinates)
		
		#Recurse and try to expand at the next spot - newCoords(directionChosen)
		nextPosition = getNewCoords(coordinates, directionChosen)
		solveMaze(nextPosition, pathList)

	if len(possibleDirections) == 0:
		if coordinates != targetCoords:
			# Loop backwards through the path array:
			for a in range(len(pathList)-1, -1, -1):
				theseCoords = [pathList[a][0], pathList[a][1]]
				possibleHere = getDirList(theseCoords)

				# Test if this spot has multiple directions:
				if len(possibleHere):
					# Recurse at this spot and continue to solve
					newPathList = list(filter(lambda x: (x != 0), pathList))
					# print('NEW LIST: ' + str(newPathList))
					solveMaze(theseCoords, newPathList)
					break # Without this break line here, it would continue the loop AFTER the maze was already solved.
				else:
					pathList[a] = 0


def draw():
	global tileSize, pathArray, pathArrayTemp

	lineSize = 3
	lineMarg = tileSize/2
	for row in range(ROWS):
		for col in range(COLS):
			x = col*tileSize+tileSize
			y = row*tileSize+tileSize
			if wallArray[row][col].topWall == True:
				pygame.draw.line(screen, (255,255,255), (int(x-lineMarg), int(y-lineMarg)), (int(x+lineMarg), int(y-lineMarg)), lineSize)
			if wallArray[row][col].botWall == True:
				pygame.draw.line(screen, (255,255,255), (int(x-lineMarg), int(y+lineMarg)), (int(x+lineMarg), int(y+lineMarg)), lineSize)
			if wallArray[row][col].rigWall == True:
				pygame.draw.line(screen, (255,255,255), (int(x+lineMarg), int(y-lineMarg)), (int(x+lineMarg), int(y+lineMarg)), lineSize)
			if wallArray[row][col].lefWall == True:
				pygame.draw.line(screen, (255,255,255), (int(x-lineMarg), int(y-lineMarg)), (int(x-lineMarg), int(y+lineMarg)), lineSize)

	for coordinate in range(len(pathArrayTemp)):
		x = pathArrayTemp[coordinate][0] * tileSize + tileSize/2
		y = pathArrayTemp[coordinate][1] * tileSize + tileSize/2

		pygame.draw.rect(screen, (250, 250, 250), (int(x+ tileSize/4), int((y+ tileSize/4)), int(tileSize/2), int(tileSize/2)))

		if coordinate == 0:
			pygame.draw.rect(screen, (250, 0, 0), (int(x+ tileSize/4), int((y+ tileSize/4)), int(tileSize/2), int(tileSize/2)))			
		if coordinate == len(pathArrayTemp)-1:
			pygame.draw.rect(screen, (0, 250, 0), (int(x+ tileSize/4), int((y+ tileSize/4)), int(tileSize/2), int(tileSize/2)))

	drawText(str("Press: (G) to generate new maze - (SPACE) to solve maze."), w_width/2, w_height-tileSize+10, "gray", 10)


def reset():
	global pathArrayTemp, testedArray, mazeArray, wallArray, attempts
	attempts = 0

	for r in range(ROWS):
		for c in range(COLS):
			wallArray[r][c].topWall = False
			wallArray[r][c].botWall = False
			wallArray[r][c].lefWall = False
			wallArray[r][c].rigWall = False

	pathArrayTemp, testedArray, mazeArray, wallArray = [], [], [], []

	for rows in range(ROWS):
		thisRow = []
		for cols in range(COLS):
			thisRow.append(0)

		testedArray.append(thisRow)

	mazeArray, wallArray = generateMaze(mazeSIZE)

	# solveMaze([0, 0], [])


def updateDisplay():
	global runLoop

	while runLoop:
		mouseX, mouseY = pygame.mouse.get_pos()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					pygame.quit()
					sys.exit()
				if event.key == pygame.K_g:	
					reset()
				if event.key == pygame.K_SPACE:
					if not any(1 in sublist for sublist in testedArray):
						solveMaze([0, 0], [])

		screen.fill(backgroundColour)
		draw()
		pygame.display.update()

		clock.tick(60)

updateDisplay()