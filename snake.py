
import sys, pygame, random

screen = pygame.display.set_mode(size:=(500,500))
pygame.display.set_caption("Snake!")

clock = pygame.time.Clock()

snakes = [pygame.Rect((size[0]//2-10, size[1]//2-10),(20,20))]
apple = pygame.Rect((random.randint(0, size[0]-20), random.randint(0, size[1]-20)),(20,20))
length = 1
UP = (0, -5)
LEFT = (-5, 0)
RIGHT = (5, 0)
DOWN = (0, 5)
directions = [UP,LEFT,RIGHT,DOWN]
direction = random.choice(directions)

def change_dir(snakes, current_dir, direction):
	if len(snakes) == 1:
		return direction
	conversion = {UP:DOWN, RIGHT:LEFT, DOWN:UP, LEFT:RIGHT}
	if not conversion[current_dir] == direction:
		return direction
	return current_dir

def move_snake(snakes, length, direction, apple):
	snek = snakes[-1]
	if len(snakes) == length:
		snakes.pop(0)
	pos = [snek.x+(-snek.w if direction == LEFT else (snek.w if direction == RIGHT else 0)), snek.y+(-snek.h if direction == UP else (snek.h if direction == DOWN else 0))]
	if pos[0] < 0:
		pos[0] = size[0]+direction[0]
	elif pos[0] > size[0]:
		pos[0] = 0

	elif pos[1] < 0:
		pos[1] = size[1]+direction[1]
	elif pos[1] > size[1]:
		pos[1] = 0

	rect = pygame.Rect(tuple(pos),(20,20))
	if rect.collidelist(snakes) != -1:
		return False, False, False
	if rect.colliderect(apple):
		apple = pygame.Rect((random.randint(0, size[0]-20), random.randint(0, size[1]-20)),(20,20))
		while apple.collidelist(snakes) != -1:
			apple = pygame.Rect((random.randint(0, size[0]-20), random.randint(0, size[1]-20)),(20,20))
		length += 1
	else:
		apple = None
	snakes.append(rect)
	return snakes, apple, length

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				direction = change_dir(snakes, direction, UP)
			if event.key == pygame.K_LEFT:
				direction = change_dir(snakes, direction, LEFT)
			if event.key == pygame.K_RIGHT:
				direction = change_dir(snakes, direction, RIGHT)
			if event.key == pygame.K_DOWN:
				direction = change_dir(snakes, direction, DOWN)

	snakes, aple, length = move_snake(snakes, length, direction, apple)
	if not snakes:
		pygame.quit()
		sys.exit()
	if aple:
		apple = aple

	screen.fill((255,255,255))
	for snake in snakes:
		pygame.draw.rect(screen, (255,212,69), snake)
		pygame.draw.rect(screen, (0,0,0), snake, 1)
	pygame.draw.rect(screen, (255,0,0), apple)
	pygame.draw.rect(screen, (0,0,0), apple,1)
	pygame.display.update()
	clock.tick(5+len(snakes)//2 if 5+len(snakes)//2 <= 15 else 15)
