import pygame, random, sys
pygame.init()

screen = pygame.display.set_mode(screen_size:=(500,500))
pygame.display.set_caption('test')
color = (255,255,255)
screen.fill(color)
clock = pygame.time.Clock()

direction = None

maze = "wpw wwwwwwwwwww\nw u       ww   \nw www  ww ww  w\nw      ww ww  w\nwwwwwwwww ww  w\nww      w ww  w\nw  lw          \n    www wwwwwww\nw   wwx       w\nwwwwwww       w\n              w\n        wwwww w\nw              \nww     wwwwwwrw"
class Wall:
	def __init__(self, size, location):
		self.color = (0,0,0)
		self.rect = pygame.Rect(size,location)

class Player:
	def __init__(self, size, location):
		self.color = (255,212,69)
		self.rect = pygame.Rect(size,location)

class Exit:
	def __init__(self, size, location):
		self.color = (255,0,0)
		self.rect = pygame.Rect(size,location)

class Direction:
	def __init__(self, size, location, direction):
		self.color = (0,0,255)
		self.rect = pygame.Rect(size,location)
		self.direction = direction

class Ghost:
	def __init__(self, size, location):
		self.color = (25,25,25)
		self.rect = pygame.Rect(size,location)

walls = []
block_width = screen_size[0]//len(maze.split('\n')[0])
block_hieght = screen_size[1]//len(maze.split('\n'))
p = None

LEFT = (-block_width, 0)
RIGHT = (block_width, 0)
UP = (0, -block_hieght)
DOWN = (0, block_hieght)
for row, line in enumerate(maze.split('\n')):
	for column, char in enumerate(line):
		if char == 'w':
			walls.append(Wall((block_width*column, block_hieght*row), (block_width,block_hieght)))
		elif char == 'p':
			p = Player((block_width*column, block_hieght*row), (block_width,block_hieght))
		elif char == 'x':
			walls.append(Exit((block_width*column, block_hieght*row), (block_width,block_hieght)))
		elif char == 'u':
			walls.append(Direction((block_width*column, block_hieght*row), (block_width,block_hieght), UP))
		elif char == 'd':
			walls.append(Direction((block_width*column, block_hieght*row), (block_width,block_hieght), DOWN))
		elif char == 'r':
			walls.append(Direction((block_width*column, block_hieght*row), (block_width,block_hieght), RIGHT))
		elif char == 'l':
			walls.append(Direction((block_width*column, block_hieght*row), (block_width,block_hieght), LEFT))
		elif char == 'g':
			walls.append(Ghost((block_width*column, block_hieght*row), (block_width,block_hieght)))
i = 0
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN and not direction:
			if event.key == pygame.K_LEFT:
				direction = LEFT
			if event.key == pygame.K_RIGHT:
				direction = RIGHT
			if event.key == pygame.K_UP:
				direction = UP
			if event.key == pygame.K_DOWN:
				direction = DOWN
	if direction:
		p.rect.x += direction[0]
		p.rect.y += direction[1]
		for block in walls:
			if p.rect.colliderect(block.rect):
				if block.color == (0,0,0):
					p.rect.x -= direction[0]
					p.rect.y -= direction[1]
					direction = None
				elif block.color == (255,0,0):
					print("You won!!!")
					pygame.quit()
					sys.exit()
				elif block.color == (0,0,255):
					p.rect.x -= direction[0]
					p.rect.y -= direction[1]
					direction = block.direction
				elif block.color == (25,25,25):
					p.rect.x -= direction[0]
					p.rect.y -= direction[1]
					direction = None
					try:
						walls.remove(block)
					except ValueError:
						pass
		if p.rect.x < 0 or p.rect.y < 0 or (p.rect.x+p.rect.width) > screen_size[0] or (p.rect.y+p.rect.height) > screen_size[1]:
			print("You lost!!!")
			pygame.quit()
			sys.exit()
	screen.fill(color)
	pygame.draw.rect(screen, (255,212,69), p.rect)
	for block in walls:
		pygame.draw.rect(screen, block.color, block.rect)
	clock.tick(45)
	pygame.display.update()
