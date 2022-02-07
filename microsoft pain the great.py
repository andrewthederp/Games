
import pygame, sys

screen = pygame.display.set_mode(screen_size:=(700,700))
pygame.display.set_caption('microsoft paint the great')
clock = pygame.time.Clock()
surface = pygame.Surface((600,600))
RED = ((255,0,0),(200,0,0))
GREEN = ((0,255,0),(0,200,0))
BLUE = ((0,0,255),(0,0,200))
BLACK = ((0,0,0),(50,50,50))
GREY = ((105,105,105),(128,128,128))
PINK = ((255,105,180),(255,182,193))
BROWN = ((139,69,19),(205,133,63))
PURPLE = ((75,0,130),(148,0,211))
RED2 = (0xC42847,0xDE3C4B)
GREEN2 = (0x172815,(0x3E5622))
YELLOW = (0xEC9F05, 0xF5BB00)
BLUE2 = (0x264653, 0x2A9D8F)
SOMECOL = (0xF4A261, 0xE9C46A)


cols = [RED,GREEN,BLUE,BLACK,GREY,PINK,BROWN,PURPLE,RED2,GREEN2,YELLOW,BLUE2,SOMECOL]
distance = screen_size[0]//len(cols)
pixels = []
lines = []
colors = []
mode = 0
pixel_size = 7
original_press_pos = None
class Button:
	def __init__(self, colors, width, height, pos, elevation):
		self.pressed = False
		self.elevation = elevation
		self.dynamic_elevation = elevation
		self.original_y_position = pos[1]

		self.top_rect = pygame.Rect((pos), (width, height))
		self.top_color = colors[0]
		self.bottom_rect = pygame.Rect(pos, (width, elevation))
		self.bottom_color = colors[0]

		self.bottom_rect = pygame.Rect(pos, (width, elevation))
		self.colors = colors


	def draw(self):
		self.top_rect.y = self.original_y_position-self.dynamic_elevation

		self.bottom_rect.midtop = self.top_rect.midtop
		self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

		pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=11)
		pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=11)


	def check_click(self):
		mouse_pos = pygame.mouse.get_pos()
		if self.top_rect.collidepoint(mouse_pos):
			self.top_color = self.colors[1]
			if pygame.mouse.get_pressed()[0]:
				self.dynamic_elevation = 0
				self.pressed = True
			else:
				if self.pressed:
					self.dynamic_elevation = self.elevation
					self.pressed = False
					return self.colors[0]
		else:
			self.dynamic_elevation = self.elevation
			self.top_color = self.colors[0]

for num, tup in enumerate(cols):
	colors.append(Button(tup, 20, 20, (distance*num,10), 1))
current_color = (0,0,0)
while True:
	pos = list(pygame.mouse.get_pos())
	pos[0] -= 50
	pos[1] -= 50
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_TAB:
				mode += 1
				if mode > 3:
					mode = 0
	if pygame.mouse.get_pressed()[0]:
		if mode == 0:
			rect = pygame.Rect((pos[0]-pixel_size//2,pos[1]-pixel_size//2), (pixel_size,pixel_size))
			if not rect in pixels:
				pixels.append({'rect':rect, 'col':current_color})
		elif mode == 1:
			rect = pygame.Rect((pos[0]-14, pos[1]-14), (30,30))
			for pixel in pixels:
				if rect.colliderect(pixel['rect']):
					try:
						pixels.remove(pixel)
					except ValueError:
						pass
		elif mode == 2 or mode == 3:
			if not original_press_pos:
				original_press_pos = list(pygame.mouse.get_pos())
				original_press_pos[0] -= 50
				original_press_pos[1] -= 50
	else:
		if mode == 2 and original_press_pos:
			line = [(original_press_pos[0], original_press_pos[1]), (pos[0], pos[1])]
			if not line in lines:
				lines.append({'line':line, 'col':current_color})
				original_press_pos = None
		elif mode == 3 and original_press_pos:

			if pos[0] > original_press_pos[0] and pos[1] > original_press_pos[1]:
				for column in range(original_press_pos[1], original_press_pos[1]+(pos[1]-original_press_pos[1]), 7):
					for row in range(original_press_pos[0], original_press_pos[0]+(pos[0]-original_press_pos[0]), 7):
						rect = pygame.Rect((row, column), (7,7))
						if not rect in pixels:
							pixels.append({'rect':rect, 'col':current_color})

			elif pos[0] < original_press_pos[0] and pos[1] < original_press_pos[1]:
				for column in range(pos[1], pos[1]+(original_press_pos[1]-pos[1]), 7):
					for row in range(pos[0], pos[0]+(original_press_pos[0]-pos[0]), 7):
						rect = pygame.Rect((row, column), (7,7))
						if not rect in pixels:
							pixels.append({'rect':rect, 'col':current_color})

			elif pos[0] > original_press_pos[0] and pos[1] < original_press_pos[1]:
				for column in range(pos[1], pos[1]+(original_press_pos[1]-pos[1]), 7):
					for row in range(original_press_pos[0], original_press_pos[0]+(pos[0]-original_press_pos[0]), 7):
						rect = pygame.Rect((row, column), (7,7))
						if not rect in pixels:
							pixels.append({'rect':rect, 'col':current_color})

			elif pos[0] < original_press_pos[0] and pos[1] > original_press_pos[1]:
				for column in range(original_press_pos[1], original_press_pos[1]+(pos[1]-original_press_pos[1]), 7):
					for row in range(pos[0], pos[0]+(original_press_pos[0]-pos[0]), 7):
						rect = pygame.Rect((row, column), (7,7))
						if not rect in pixels:
							pixels.append({'rect':rect, 'col':current_color})

			original_press_pos = None

	screen.fill((77, 74, 66))
	screen.blit(surface, (50, 50))
	surface.fill((255, 255, 255))
	for pixel in pixels:
		pygame.draw.rect(surface, pixel['col'], pixel['rect'])
	for line in lines:
		pygame.draw.line(surface, line['col'], line['line'][0], line['line'][1], 4)
	if mode == 0:
		rect = pygame.Rect((pos[0]-pixel_size//2,pos[1]-pixel_size//2), (pixel_size,pixel_size))
		pygame.draw.rect(surface, current_color, rect)
	elif mode == 1:
		rect = pygame.Rect((pos[0]-14, pos[1]-14), (30,30))
		pygame.draw.rect(surface, (0,0,0), rect, 1)
	elif mode == 2 and pygame.mouse.get_pressed()[0]:
		pygame.draw.aaline(surface, current_color, (original_press_pos[0], original_press_pos[1]), (pos[0], pos[1]))
	elif mode == 3 and pygame.mouse.get_pressed()[0]:
		pygame.draw.rect(surface, current_color, pygame.Rect((original_press_pos[0], original_press_pos[1]), (pos[0]-original_press_pos[0], pos[1]-original_press_pos[1])), 4)
	for button in colors:
		button.draw()
		col = button.check_click()
		current_color = col or current_color
	pygame.display.update()
	clock.tick(60)
