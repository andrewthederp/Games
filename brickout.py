import pygame, sys, random, time

screen_width, screen_height = (600, 700)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Brick Out")

player = pygame.Rect(((screen_width//2)-50, screen_height-30),(100, 10))
ball = pygame.Rect(((screen_width/2)-(20/2),(screen_height-60)),(20,20))

clock = pygame.time.Clock()

BLACK = (0,0,0)
YELLOW = (255,212,69)
WHITE = (255,255,255)
colors = [(38, 32, 115),(40, 24, 174),(21, 151, 190),(250, 185, 59),(162, 14, 29),(233, 120, 22)]
num = random.randint(0,1)
speed = random.randint(3,4)
ball_speed_y = speed
ball_speed_x = speed if num else -speed

class Bricks:
	def __init__(self, xy):
		self.brick = pygame.Rect(xy, (60, 25))
		self.color = random.choice(colors)

class Ball:
	def __init__(self, player):
		self.ball = pygame.Rect((player.center[0]-(20/2),(screen_height-60)),(20,20))
		num = random.randint(0,1)
		speed_y = random.randint(3,5)
		speed_x = random.randint(3,5)
		self.ball_speed_y = speed_y
		self.ball_speed_x = speed_x if num else -speed_x
		self.orignal_speed = speed_x

bricks = []
for x in range(9):
	for y in range(10):
		bricks.append(Bricks((x+(60*x)+25,y+(25*y)+30)))

power_up = None
power = 0
player_speed = 5
powerup_time = None
game = False
balls = [Ball(player)]
while True:
	if not len(balls):
		pygame.quit()
		sys.exit()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and not game:
				game = True

	if not bricks:
		print("You won!")
		pygame.quit()
		sys.exit()
	if powerup_time:
		if (time.perf_counter()-powerup_time) > 5 and power < 3:
			powerup_time = None
			if power == 1:
				player.x += 20
				player.width -= 40
			elif power == 2:
				player_speed -= 3
			power = None
			power_up = None
		elif (time.perf_counter()-powerup_time) > 1 and power == 3:
			powerup_time = None
			power = None
			for ball in balls:
				ball.ball_speed_y -= 5 if ball.ball_speed_y > 0 else -5
				ball.ball_speed_x -= 5 if ball.ball_speed_x > 0 else -5

	for ball in balls:
		if game:
			ball.ball.x += ball.ball_speed_x
			ball.ball.y += ball.ball_speed_y
		else:
			ball.ball.center = (player.x+player.width//2, player.y-30)

		if ball.ball.y >= screen_height:
			try:
				balls.remove(ball)
			except ValueError:
				pass

		elif ball.ball.y <= 0:
			ball.ball_speed_y *= -1
		elif ball.ball.x <= 0 or ball.ball.x >= (screen_width-ball.ball.width):
			ball.ball_speed_x *= -1

		if ball.ball.colliderect(player):
			if abs(player.left - ball.ball.right) < 10:
				ball.ball_speed_x *= -1
				ball.ball_speed_y *= -1
			elif abs(player.right - ball.ball.left) < 10:
				ball.ball_speed_x *= -1
				ball.ball_speed_y *= -1
			elif abs(player.top - ball.ball.bottom) < 10 and ball.ball_speed_y > 0:
				speed = -1*(player.center[0]-ball.ball.center[0])
				ball.ball_speed_x = (ball.orignal_speed + speed//10) if speed > 0 else (-ball.orignal_speed + speed//10)
				ball.ball_speed_y *= -1

	if power_up:
		if player.colliderect(power_up):
			power_up = None
			power = random.randint(1,4)
			powerup_time = time.perf_counter()
			if power == 1:
				player.x -= 20
				player.width += 40
			elif power == 2:
				player_speed += 3
			elif power == 3:
				for ball in balls:
					ball.ball_speed_y += 5 if ball.ball_speed_y > 0 else -5
					ball.ball_speed_x += 5 if ball.ball_speed_x > 0 else -5
			elif power == 4:
				for _ in range(2):
					balls.append(Ball(player))
				power = None
				powerup_time = None

	keys_pressed = pygame.key.get_pressed()
	if keys_pressed[pygame.K_LEFT]:
		if not (player.x - player_speed) < 0:
			player.x -= player_speed
		else:
			player.x = 0

	elif keys_pressed[pygame.K_RIGHT]:
		if not (player.x + player.width) >= screen_width:
			player.x += player_speed
		else:
			player.x = (screen_width-player.width)

	screen.fill(BLACK)
	for brick in bricks:
		for ball in balls:
			if ball.ball.colliderect(brick.brick):
				if power != 3:
					if abs(brick.brick.left - ball.ball.right) < 10:
						ball.ball_speed_x *= -1
					elif abs(brick.brick.right - ball.ball.left) < 10:
						ball.ball_speed_x *= -1
					elif abs(brick.brick.top - ball.ball.bottom) < 10 and ball.ball_speed_y > 0:
						ball.ball_speed_y *= -1
					elif abs(brick.brick.bottom - ball.ball.top) < 10 and ball.ball_speed_y < 0:
						ball.ball_speed_y *= -1
				else:
					pass
				try:
					num = random.randint(1, 10)
					bricks.remove(brick)
					if num == 1 and not power_up and not powerup_time:
						power_up = pygame.Rect(brick.brick.center,(25,25))
				except ValueError:
					pass
			pygame.draw.ellipse(screen, (255,0,0) if power == 3 else WHITE, ball.ball)

		pygame.draw.rect(screen, brick.color, brick.brick)

	if power_up:
		power_up.y += 3
		pygame.draw.rect(screen, WHITE, power_up)
		if power_up.y >= screen_height:
			power_up = None
	pygame.draw.rect(screen, YELLOW, player)
	pygame.display.update()
	clock.tick(60)
