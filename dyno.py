pygame, random, sys

pygame.init()


screen_width, screen_height = 700, 350
SCORE_FONT = pygame.font.SysFont('comicsans', 40)
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Dino")
clock = pygame.time.Clock()

BLACK = (0,0,0)
YELLOW = (255,212,69)
WHITE = (255,255,255)

SPAWNOB = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWNOB,100)
player = pygame.Rect((50, screen_height-50),(30, 50))
obstacles = []
in_air = False
score = 0
jumping = False
jumping_speed = 10
game = False
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
			pygame.quit()
		if event.type == SPAWNOB and game:
			pygame.time.set_timer(SPAWNOB,random.randint(500, 2000) if score//10 < 500 else random.randint(300,1500))
			num = random.choice([30, 50])
			obstacles.append(pygame.Rect((screen_width, screen_height-num),(50 if num == 30 else 30, num)))
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and not in_air:
				jumping = True
				game = True
	if game:
		if jumping:
			player.y -= jumping_speed
			jumping_speed -= .5
			if jumping_speed <= 0:
				jumping = False
			in_air = True
		keys_pressed = pygame.key.get_pressed()
		if keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]:
			jumping = False
			if player.y < (screen_height-player.height):
				player.y += 8
			else:
				player.height = 30
				player.width = 50
				player.y = screen_height-player.height
			in_air = True
		elif not keys_pressed[pygame.K_s]:
			player.height = 50
			player.width = 30
			in_air = False

		if not jumping:
			if player.y < (screen_height-player.height):
				player.y -= jumping_speed
				jumping_speed -= .5
			else:
				jumping_speed = 10
				player.y = (screen_height-player.height)
				if not player.height == 30:
					in_air = False
		score += 1

	screen.fill(WHITE)
	pygame.draw.rect(screen, YELLOW, player)
	for obstacle in obstacles:
		obstacle.x -= 6 if score//10 < 200 else (7 if score//10 < 500 else (8 if score//10 in range(1000, 1501) else 10))
		if player.colliderect(obstacle):
			print("You lost, your score:", score//10)
			pygame.quit()
			sys.exit()
		if (obstacle.x+obstacle.width) > 0:
			pygame.draw.rect(screen, BLACK, obstacle)
	score_text = SCORE_FONT.render("Score: " + str(score//10), 1, BLACK)
	screen.blit(score_text, (10, 10))
	pygame.display.update()
	clock.tick(60)
