#Imports essentials and initiates pygame
import pygame
import time
from pygame.locals import *
from random import randint
pygame.init()

#Sets initial variable values
playing = False
Width = 30
Height = 20

#Loads images
arrow = pygame.image.load("PyGameArrow.png")
character = pygame.image.load("character.png")

#Creates screen
screen = pygame.display.set_mode(((Width+2)*32,(Height+2)*32))
pygame.display.set_caption("Arrows")

#Fills background
back = pygame.Surface(((Width+2)*32,(Height+2)*32))
background = back.convert()
background.fill((255,255,255))
screen.blit(background,(0,0))

#Creates array for directions
grid = [["0000" for x in range(Width)] for x in range(Height)]

#Creates list locations, class mover, and completes background
locations = list()

for x in range(Width):
		for y in range(Height):
			pygame.draw.rect(screen, (0, 0, 0), Rect(32+x*32,32+y*32,32,32), 3)

class mover(object):
	def __init__(self, x, y):
		super(mover, self).__init__()
		self.x = x
		self.y = y

#Defines generator "person" and player "player"
person = mover(0, Height-1)
player = mover(0, Height-1)

#Defines start and end position by coloring green and red
pygame.draw.rect(screen, (0, 255, 0), Rect(34,34+(Height-1)*32,28,28))
pygame.draw.rect(screen, (255, 0, 0), Rect(34+(Width-1)*32,34,28,28))

#Sets rotation variables for later use in generation
rotation = 0
oldrotation = 0

def stamp():
	global arrow
	if(player.x == 0 and player.y == Height-1):
		pygame.draw.rect(screen, (0, 255, 0), Rect(34+(player.x)*32,34+(player.y)*32,28,28))
	else:
		pygame.draw.rect(screen, (255, 255, 255), Rect(34+(player.x)*32,34+(player.y)*32,28,28))
	for direction in grid[player.y][player.x]:
		if direction == "1":
			screen.blit(arrow,(35+player.x*32, 35+player.y*32))
		arrow = pygame.transform.rotate(arrow, 90)

def stamp2():
	global arrow
	arrow = pygame.transform.rotate(arrow, rotation - oldrotation)
	screen.blit(arrow,(35+person.x*32, 35+person.y*32))

#Main code, responsible for generation of map and gameplay
while True:
	if(playing == True and grid[player.y][player.x].count('1') == 0):
		pygame.draw.rect(screen, (0, 0, 255), Rect(34+(player.x)*32,34+(player.y)*32,28,28))
		player = mover(0, Height-1)
		time.sleep(0.5)
	elif(playing == True and grid[player.y][player.x].count('1') == 1):
		stamp()
		if(grid[player.y][player.x] == "1000"):
			player.x = player.x + 1
		elif(grid[player.y][player.x] == "0100"):
			player.y = player.y - 1
		elif(grid[player.y][player.x] == "0010"):
			player.x = player.x - 1
		elif(grid[player.y][player.x] == "0001"):
			player.y = player.y + 1
		time.sleep(0.2)
	for event in pygame.event.get():
		#Checks for key inputs W, A, S or D
		if event.type == KEYDOWN: 
			if event.key == K_q:
				exit()
			if playing == True:
				if event.key == K_w:
					if grid[player.y][player.x][1] == "1":
						stamp()
						player.y = player.y - 1
				if event.key == K_a:
					if grid[player.y][player.x][2] == "1":
						stamp()
						player.x = player.x - 1
				if event.key == K_s:
					if grid[player.y][player.x][3] == "1":
						stamp()
						player.y = player.y + 1
				if event.key == K_d:
					if grid[player.y][player.x][0] == "1":
						stamp()
						player.x = player.x + 1

	#Defines which directions the generator can move
	directions = list()
	if not person.y == 0 and grid[person.y-1][person.x] == "0000":
		directions.append("w")
	if not person.y == Height-1 and grid[person.y+1][person.x] == "0000":
		directions.append("s")
	if not person.x == Width-1 and grid[person.y][person.x+1] == "0000":
		directions.append("d")
	if not person.x == 0 and grid[person.y][person.x-1] == "0000":
		directions.append("a")
	
	#Changes array text according to direction information
	if not len(directions) == 0 and not (person.x == Width - 1 and person.y == 0):
		if len(directions) > 1:
			locations.append([person.x,person.y])
		text = grid[person.y][person.x]
		random = randint(0, len(directions) - 1)
		canmove = True
		if directions[random] == "w":
			rotation = 90
			stamp2()
			grid[person.y][person.x] = text[:1] + '1' + text[2:]
			person.y = person.y - 1					
		elif directions[random] == "d":
			rotation = 0
			stamp2()
			grid[person.y][person.x] = '1' + text[1:]
			person.x = person.x + 1
		elif directions[random] == "a":
			rotation = 180
			stamp2()
			grid[person.y][person.x] = text[:2] + '1' + text[3:]
			person.x = person.x - 1
		elif directions[random] == "s":
			rotation = 270
			stamp2()
			grid[person.y][person.x] = text[:3] + '1'
			person.y = person.y + 1
		oldrotation = rotation
	elif(len(locations) > 0):
		#No location to move to, has to create a new branch
		if(canmove == True):
			if not (person.x == Width - 1 and person.y == 0):
				pygame.draw.rect(screen, (0, 0, 255), Rect(34+(person.x)*32,34+(person.y)*32,28,28))
			grid[person.y][person.x] = "xxxx"
			canmove = False
		else:
			person.x = locations[0][0]
			person.y = locations[0][1]
			del locations[0]
	else:
		#Generation over, starts game here
		screen.blit(character,(40+player.x*32, 40+player.y*32))
		if playing == False:
			arrow = pygame.image.load("PyGameArrow.png")
		playing = True

	#Updates display
	if(playing == True):
		pygame.display.update()