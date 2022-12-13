
import pygame, sys, random
pygame.init()

screen = pygame.display.set_mode(size:=(400, 400))
pygame.display.set_caption("Bouncy balls")


class FlyingCircle:
	def __init__(self):
		self.color = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
		self.rect = pygame.Rect((random.randint(0, size[0]),random.randint(0, size[1])),(20,20))
		self.speed_x = random.choice([random.randint(5, 7), random.randint(-7, -5)])
		self.speed_y = random.choice([random.randint(5, 7), random.randint(-7, -5)])

	def move(self):
		self.rect.x += self.speed_x
		self.rect.y += self.speed_y
		if self.rect.x < 0 or (self.rect.x+self.rect.w) > size[0]:
			self.speed_x *= -1
		if self.rect.y < 0 or (self.rect.y+self.rect.h) > size[1]:
			self.speed_y *= -1
		self.draw()

	def draw(self):
		pygame.draw.ellipse(screen, self.color, self.rect)
		pygame.draw.ellipse(screen, (0,0,0), self.rect, 1)

clock = pygame.time.Clock()
font = pygame.font.Font(None, 80)

mouse_rect = pygame.Rect((0,0),(20,20))
bigger_mouse_rect = pygame.Rect((0,0),(100,100))
flying_circles = []
score_rect = False
score = 0

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	if not score_rect:
		score_rect = pygame.Rect((random.randint(0,(size[0]-25)), random.randint(0, (size[1])-25)), (25,25))

	mouse_rect.center = pygame.mouse.get_pos()
	bigger_mouse_rect.center = pygame.mouse.get_pos()

	screen.fill((100,100,100))
	pygame.draw.ellipse(screen, (255,0,0), mouse_rect)
	if score_rect:
		pygame.draw.rect(screen, (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)), score_rect)

	for flyingcircle in flying_circles:
		flyingcircle.move()
		if flyingcircle.rect.colliderect(mouse_rect):
			print(score)
			pygame.quit()
			sys.exit()
		# flyingcircle.draw()

	if mouse_rect.colliderect(score_rect):
		score += 1
		if score == 1 or not score%5:
			circle = FlyingCircle()
			while circle.rect.colliderect(bigger_mouse_rect):
				circle = FlyingCircle()
			flying_circles.append(circle)
		score_rect = None

	score_surf = font.render(str(score), False, 'black')
	score_r = score_surf.get_rect(topleft=(10,10))
	screen.blit(score_surf, score_r)
	pygame.display.update()
	clock.tick(60)
