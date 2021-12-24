import pygame, random, sys
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((100,100))
pygame.display.set_caption('Color test')
color = (255,255,255)
screen.fill(color)
clock = pygame.time.Clock()
colors = [color]

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			f.close()
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				color = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
				colors.append(color)
			if event.key == pygame.K_RETURN:
				print(color)
			if event.key == pygame.K_RIGHT:
				try:
					colors.pop()
					color =  colors[-1]
				except IndexError:
					pass
	screen.fill(color)
	clock.tick(10)
	pygame.display.update()
