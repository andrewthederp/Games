ort pygame
import sys
import random
import time

pygame.init()
pygame.font.init()

screen_width = 600
screen_height = 600

PAUSE_FONT = pygame.font.SysFont('comicsans', 100)
SMALLER_PAUSE_FONT = pygame.font.SysFont('comicsans', 30)

BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
YELLOW = (255,212,69)
WHITE = (255,255,255)
PINK = (255, 105, 180)

def get_font(path, size):
	return pygame.font.SysFont(path, size)


SCORE_FONT = pygame.font.SysFont('comicsans', 40)

def main():
	clock = pygame.time.Clock()
	pygame.display.set_caption("Platformer")
	screen = pygame.display.set_mode((screen_width,screen_height))
	SPAWNPF = pygame.USEREVENT + 1
	SPAWNCIR = pygame.USEREVENT + 2
	pygame.time.set_timer(SPAWNPF,500)
	pygame.time.set_timer(SPAWNCIR,random.randint(5000,10000))
	in_air = False
	game = False
	PAUSED = False
	location = "mm"
	mm_font = get_font('C:\\Windows\\Fonts\\ARLRDBD.TTF', 100)
	arrow_font = get_font('C:\\Windows\\Fonts\\ARLRDBD.TTF', 50)
	game_font = get_font('C:\\Windows\\Fonts\\vgaf1256.fon', 26)
	player_font = get_font('comicsans', 50)
	player_color = (255,212,69)
	player = pygame.Rect(screen_width//2, screen_height-60, 30, 50)
	player1 = pygame.Rect(100, screen_height-60, 30, 50)
	player2 = pygame.Rect(300, screen_height-60, 30, 51)
	player3 = pygame.Rect(500, screen_height-60, 30, 49)
	platforms = [pygame.Rect(random.randint(0, (screen_width-80)), random.randint(0, (screen_height-10)), 80, 10), pygame.Rect(random.randint(0, (screen_width-80)), random.randint(0, (screen_height-10)), 80, 10), pygame.Rect(random.randint(0, (screen_width-80)), random.randint(0, (screen_height-10)), 80, 10), pygame.Rect(random.randint(0, (screen_width-80)), random.randint(0, (screen_height-10)), 80, 10), pygame.Rect(random.randint(0, (screen_width-80)), random.randint(0, (screen_height-10)), 80, 10), pygame.Rect(random.randint(0, (screen_width-80)), random.randint(0, (screen_height-10)), 80, 10), pygame.Rect(0, screen_height-10, screen_width, 10)]
	game_over = False
	start_time = time.perf_counter()
	pause_time = None
	unpause_time = None
	score = 0
	while True:
		if game_over:
			platforms = [pygame.Rect(random.randint(0, (screen_width-80)), random.randint(0, (screen_height-10)), 80, 10), pygame.Rect(random.randint(0, (screen_width-80)), random.randint(0, (screen_height-10)), 80, 10), pygame.Rect(random.randint(0, (screen_width-80)), random.randint(0, (screen_height-10)), 80, 10), pygame.Rect(random.randint(0, (screen_width-80)), random.randint(0, (screen_height-10)), 80, 10), pygame.Rect(random.randint(0, (screen_width-80)), random.randint(0, (screen_height-10)), 80, 10), pygame.Rect(random.randint(0, (screen_width-80)), random.randint(0, (screen_height-10)), 80, 10), pygame.Rect(0, screen_height-10, screen_width, 10)]
			game_over = False
			player.x = screen_width//2
			player.y = screen_height-60
			location = 'mm'
			game = False
			score = 0
			start_time = time.perf_counter()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if PAUSED and event.key not in [pygame.K_TAB, pygame.K_LALT]:
					PAUSED = False
					unpause_time = time.perf_counter()
					start_time = start_time-(pause_time-unpause_time)
				if event.key == pygame.K_ESCAPE and not location == 'mm' and not PAUSED:
					pause_text = PAUSE_FONT.render("Paused", 1, BLUE)
					screen.blit(pause_text, (screen_width/2 - pause_text.get_width() /2, screen_height/2 - pause_text.get_height()/2))
					pause_text = SMALLER_PAUSE_FONT.render("Press any button to unpause", 1, BLUE)
					screen.blit(pause_text, ((screen_width/2 - pause_text.get_width() /2)+5, (screen_height/2 - pause_text.get_height()/2)+65))
					pygame.display.flip()
					PAUSED = True
					pause_time = time.perf_counter()
				if event.key == pygame.K_SPACE and not in_air:
					if not game and location == 'mm':
						game = True
						location = 'game'
						start_time = time.perf_counter()
					if player.height == 51:
						player.y -= 400
					else:
						player.y -= 300
					in_air = True
			if event.type == SPAWNPF and game and not PAUSED:
				pygame.time.set_timer(SPAWNPF,random.randint(500, 1300))
				i = random.randint(0,10)
				sp_pl = None
				if i == 10:
					sp_pl = pygame.Rect(random.randint(0, screen_width), 0, random.randint(100, 230), 11)
				elif i == 9:
					sp_pl = pygame.Rect(random.randint(0, screen_width), 0, random.randint(100, 230), 9)
				elif i == 8:
					sp_pl = pygame.Rect(random.randint(0, screen_width), 0, random.randint(50, 180), 8)
				elif i == 7:
					sp_pl = pygame.Rect(random.randint(0, screen_width), 0, random.randint(100, 230), 12)
				pl = pygame.Rect(random.randint(0, screen_width), 0, random.randint(100, 230), 10)
				if sp_pl:
					if not sp_pl.colliderect(pl):
						platforms.append(sp_pl)
				platforms.append(pl)
			if event.type == SPAWNCIR and not PAUSED and location == 'game':
				pygame.time.set_timer(SPAWNCIR,random.randint(5000,10000))
				platforms.append(pygame.Rect(random.randint(0, screen_width), 0, 30, 30))
			if event.type == pygame.MOUSEBUTTONUP:
				x, y = event.pos
				if location == 'mm':
					if x in range(screen_width-40, screen_width) and y in range(10, 41):
						location = 'faq'
				elif location == 'faq':
					if x in range(screen_width-40, screen_width) and y in range(10, 41):
						location = 'mm'
					elif x in range(player.x, player.x+player.width) and y in range(player.y,player.y+player.height):
						location = 'p'
				elif location == 'p':
					if x in range(player1.x, player1.x+player1.width) and y in range(player1.y,player1.y+player1.height):
						player_color = YELLOW
						player = player1
						location = 'mm'
					elif x in range(player2.x, player2.x+player2.width) and y in range(player2.y,player2.y+player2.height):
						player_color = RED
						player = player2
						location = 'mm'
					elif x in range(player3.x, player3.x+player3.width) and y in range(player3.y,player3.y+player3.height):
						player_color = PINK
						player = player3
						location = 'mm'

		if PAUSED:
			continue

		keys_pressed = pygame.key.get_pressed()
		if player.height == 51:
			num = 7
		else:
			num = 5
		if keys_pressed[pygame.K_d]:
			if (player.x + num) > screen_width:
				player.x = 0
			else:
				player.x += num
		if keys_pressed[pygame.K_a]:
			if (player.x - num) < 0:
				player.x = screen_width
			else:
				player.x -= num
		if keys_pressed[pygame.K_s] and in_air:
			player.y += 10

		for platform in platforms:
			if platform.colliderect(player):
				if platform.height == 30:
					try:
						platforms.remove(platform)
						score += 5
					except ValueError:
						pass
				if platform.height == 8:
					player.y = 1000
					break
				elif platform.height == 12:
					player.y = -player.height
					in_air = False
				else:
					player.y = ((platform.y-player.height)+1)
					in_air = False
			if game:
				if platform.height == 11:
					platform.y += 8
				else:
					platform.y += 3
				if platform.y >= screen_height:
					try:
						platforms.remove(platform)
					except ValueError:
						pass
		else:
			player.y += 5
			if player.y >= screen_height:
				game_over = True

		screen.fill(BLACK)
		pygame.draw.rect(screen, player_color, player)
		for platform in platforms:
			if platform.height == 30:
				pygame.draw.rect(screen, WHITE, platform)
			elif platform.height == 11:
				pygame.draw.rect(screen, GREEN, platform)
			elif platform.height == 9:
				i = random.randint(1, 60)
				pygame.draw.rect(screen, WHITE if i <= 3 else BLACK, platform)
			elif platform.height == 8:
				pygame.draw.rect(screen, player_color, platform)
			elif platform.height == 12:
				pygame.draw.rect(screen, BLUE, platform)
			else:
				pygame.draw.rect(screen, WHITE, platform)
		if location == 'game':
			score_text = SCORE_FONT.render("Score: " + str(round(time.perf_counter() - start_time)+score), 1, RED)
			screen.blit(score_text, (10, 10))
		if location == 'mm':
			mm_text = mm_font.render("MAIN MENU", 1, player_color)
			screen.blit(mm_text, (screen_width/2 - mm_text.get_width() /2, screen_height/2 - mm_text.get_height()/2))
			h1 = pygame.Rect(screen_width-50, 10, 40, 8)
			h2 = pygame.Rect(screen_width-50, 25, 40, 8)
			h3 = pygame.Rect(screen_width-50, 40, 40, 8)
			pygame.draw.rect(screen, WHITE, h1)
			pygame.draw.rect(screen, WHITE, h2)
			pygame.draw.rect(screen, WHITE, h3)
		elif location == 'faq':
			screen.fill(BLACK)
			mm_text = arrow_font.render('->', 1, WHITE)
			screen.blit(mm_text, (560, 10))
			pygame.draw.rect(screen, player_color, player)
			pl1 = pygame.Rect(20, 100, 140, 10)
			pl2 = pygame.Rect(20, 150, 140, 10)
			pl3 = pygame.Rect(20, 200, 140, 10)
			pl4 = pygame.Rect(20, 250, 140, 10)
			pl5 = pygame.Rect(20, 300, 140, 10)
			pl6 = pygame.Rect(20, 350, 30, 30)
			pygame.draw.rect(screen, WHITE, pl1)
			pygame.draw.rect(screen, GREEN, pl2)
			i = random.randint(1, 60)
			pygame.draw.rect(screen, WHITE if i <= 3 else BLACK, pl3)
			pygame.draw.rect(screen, player_color, pl4)
			pygame.draw.rect(screen, BLUE, pl5)
			pygame.draw.rect(screen, WHITE, pl6)
			screen.blit(game_font.render("Normal platform: Will move down slowly", 1, WHITE), (180, 95))
			screen.blit(game_font.render("Speedy platform: Will move down quickly", 1, GREEN), (180, 147))
			screen.blit(game_font.render("Glitch platform: you can see it, now you can't", 1, WHITE if i <= 3 else BLACK), (180, 197))
			screen.blit(game_font.render("Flesh platform: standing on it kills you", 1, player_color), (180, 247))
			screen.blit(game_font.render("Bouncy platform: makes you jump really high", 1, BLUE), (180, 297))
			screen.blit(game_font.render("Score sqaure: gives you 5 points and allows you to jump again", 1, WHITE), (70, 357))
		elif location == 'p':
			screen.fill(BLACK)
			player_text = player_font.render("Choos your player", 1, player_color)
			screen.blit(player_text, (screen_width/2 - player_text.get_width() /2, screen_height/2 - player_text.get_height()/2))
			pygame.draw.rect(screen, YELLOW, player1)
			pygame.draw.rect(screen, RED, player2)
			pygame.draw.rect(screen, PINK, player3)
		pygame.display.update()
		clock.tick(60)

if __name__ == "__main__":
	main()
