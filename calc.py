import pygame, sys
from math import sin, cos, tan, pi

pygame.init()
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption('Calc')
gui_font = pygame.font.Font(None, 30)
bigger_gui_font = pygame.font.Font(None, 70)
clock = pygame.time.Clock()
calc_surf = pygame.Surface((400,200))

class Button:
	def __init__(self, text, width, height, pos, elevation):
		self.pressed = False
		self.elevation = elevation
		self.dynamic_elevation = elevation
		self.original_y_position = pos[1]

		self.top_rect = pygame.Rect((pos), (width, height))
		self.top_color = '#475F77'

		self.bottom_rect = pygame.Rect(pos, (width, elevation))
		self.bottom_color = '#354B5E'

		self.text = text
		self.text_surf = gui_font.render(text, True, "#FFFFFF")
		self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

	def draw(self):
		self.top_rect.y = self.original_y_position-self.dynamic_elevation
		self.text_rect.center = self.top_rect.center

		self.bottom_rect.midtop = self.top_rect.midtop
		self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

		pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=11)
		pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=11)
		screen.blit(self.text_surf, self.text_rect)
		return self.check_click()

	def check_click(self):
		mouse_pos = pygame.mouse.get_pos()
		if self.top_rect.collidepoint(mouse_pos):
			self.top_color = '#D74B4B'
			if pygame.mouse.get_pressed()[0]:
				self.dynamic_elevation = 0
				self.pressed = True
			else:
				if self.pressed:
					self.dynamic_elevation = self.elevation
					self.pressed = False
					return self.text
		else:
			self.dynamic_elevation = self.elevation
			self.top_color = '#475F77'

lst = []
i = 200
ANS = '0'
for num, title in enumerate(['AC','ANS','sin(','tan(','cos(','pi','1','2','3','+','-','4','5','6','*','/','7','8','9','**','//','0','(',')','=']):
	i += 50 if not num%5 else 0
	lst.append(Button(title, 50, 40, ((100+(50*(num%5))+(10*(num%5))), i), 6))

eq = ''
eqd = False
veq = ''

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	screen.fill((77, 74, 66))
	for button in lst:
		h = button.draw()
		if h:
			if eqd:
				eqd = False
				veq = ''
			if h == 'AC':
				eq = ''
				veq = ''
			elif h == '=':
				try:
					veq = str(eval(eq))
					ANS = veq
				except Exception as e:
					veq = 'Error'
				eq = ''
				eqd = True
			elif h == 'ANS':
				veq += ANS
				eq += ANS
			else:
				eq += h
				veq += h
				if len(veq) > 12:
					veq = veq[1:]
	screen.blit(calc_surf, (50, 30))
	calc_surf.fill('white')
	text_surf = bigger_gui_font.render(veq, True, (0,0,0))
	text_rect = text_surf.get_rect(topleft = ((135, 70) if veq == 'Error' else (25,75)))
	calc_surf.blit(text_surf, text_rect)
	pygame.display.update()
	clock.tick(60)
