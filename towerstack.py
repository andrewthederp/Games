pygame, random, sys

pygame.init()


screen_width, screen_height = 400, 600


SCORE_FONT = pygame.font.SysFont('comicsans', 40)
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Stack towers")

BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
YELLOW = (255,212,69)
WHITE = (255,255,255)
PINK = (255, 105, 180)

colors = [RED, BLUE, GREEN, YELLOW, WHITE, PINK]

cur_rec = None
move_left = True
clock = pygame.time.Clock()
length = 200
score = 0
class Block:
	def __init__(self, length, y=screen_height-50):
		self.color = random.choice(colors)
		self.shape = pygame.Rect((screen_width//4, y),(length,50))

rectangles=[Block(200),Block(200,screen_height-100)]
going_down = False
went_down = 0
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
			pygame.quit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and cur_rec:
				h = rectangles[-2]
				h = h.shape.x+h.shape.width
				cover = cur_rec.shape.x+cur_rec.shape.width
				if cover != h:
					if cover < h:
						length -= h-cover
						cur_rec.shape.x = rectangles[-2].shape.x
					elif cover > h:
						length -= cover-h
						cur_rec.shape.x = h-length
					if length <= 0:
						print('You lost, score: ' + str(score))
						pygame.quit()
						sys.exit()
					score += 1
				while not cur_rec.shape.colliderect(rectangles[-2].shape):
					cur_rec.shape.y += 1
				cur_rec.shape.y-=1
				cur_rec.shape.width = length
				going_down = True
				while going_down:
					went_down += 3
					for rectangle in rectangles:
						rectangle.shape.y += 3
					screen.fill(BLACK)
					for num, rectangle in enumerate(rectangles):
						if not rectangle.shape.y > screen_width+200:
							pygame.draw.rect(screen, rectangle.color, rectangle.shape)

					score_text = SCORE_FONT.render("Score: " + str(score), 1, RED)
					screen.blit(score_text, (10, 10))
					pygame.display.update()
					if went_down >= 48:
						going_down = False
						went_down = 0
				cur_rec = None

	if not cur_rec:
		cur_rec = Block(length, screen_height-350)
		rectangles.append(cur_rec)
	if cur_rec:
		if move_left:
			cur_rec.shape.x -= 3
			if cur_rec.shape.x <= 0:
				move_left = False
		else:
			cur_rec.shape.x += 3
			if (cur_rec.shape.x+cur_rec.shape.width) >= screen_width:
				move_left = True


	screen.fill(BLACK)
	for num, rectangle in enumerate(rectangles):
		if not rectangle.shape.y > screen_width+200:
			pygame.draw.rect(screen, rectangle.color, rectangle.shape)

	score_text = SCORE_FONT.render("Score: " + str(score), 1, RED)
	screen.blit(score_text, (10, 10))
	pygame.display.update()
	clock.tick(60)
