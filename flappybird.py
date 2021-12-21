# light/dark mode
inp = input("Do you want inverted colors? [y/n]\n\t")

# Imports
import pygame
import sys
import random

# Initialising 
pygame.font.init()
pygame.init()

# Colors
WHITE = (255,255,255)
YELLOW = (255,212,69)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)

# Fonts
SCORE_FONT = pygame.font.SysFont('comicsans', 40)
PAUSE_FONT = pygame.font.SysFont('comicsans', 100)
SMALLER_PAUSE_FONT = pygame.font.SysFont('comicsans', 30)

# Global variables
screen_width = 600
screen_height = 600
player = pygame.Rect(50, 300, 50, 50)

# Obstacle class
class Obstacle:
	def __init__(self):
		# List to append obstacles to
		self.obstacles = []

	# function to spawn obstacles
	def spawn_obstacle(self):
		num = random.randint(200, screen_height)
		num2 = random.randint(200,300)

		boarder1 = pygame.Rect(screen_width, 0, 70, num-num2)
		boarder2 = pygame.Rect(screen_width, num+30, 70, 600)
		self.obstacles.append([boarder1, boarder2])

	# Function to move and delete obstacles
	def move_obstacles(self, score):
		for ob in self.obstacles:
			for obstacle in ob:

				# How fast should the obstacles move
				if score in range(10,30):
					num = 4
				elif score in range(30, 50):
					num = 5
				elif score in range(50,101):
					num = 6
				elif score >= 100:
					num = 9
				else:
					num = 3
				obstacle.x -= num

				#  check if the obstacle is off-screen
				if (obstacle.x+100) < 0:

					# try to remove it, but sometimes it's so quick it will try to remove twice which causes problem
					try:
						self.obstacles.remove(ob)
						score += 1
					except ValueError:
						pass
		return score

# Gravity
def move_player(player):
	player.y += 5
	if player.y >= (screen_height+30):
		pygame.quit()
		sys.exit()
		print('Game over!')
		print(score)

# The actual game
def main():
	# Set the window name as "Flappy bird"
	pygame.display.set_caption("Flappy bird")

	# The actual screen
	screen = pygame.display.set_mode((screen_width,screen_height))

	# Clock to be able to control the framrate
	clock = pygame.time.Clock()

	# User event to summon the obstacles
	SPAWNOB = pygame.USEREVENT + 1
	pygame.time.set_timer(SPAWNOB,1900)
	obstacles = Obstacle()

	score = 0

	# Check if game is paused
	PAUSED = False
	while True:
		# The controls
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if PAUSED and event.key not in [pygame.K_TAB, pygame.K_LALT]: # lalt+tab is how i move between windows ~w~
					# remove the pause
					PAUSED = False
				# make the player jump, but not be able to jump off-screen
				if event.key == pygame.K_SPACE:
					if (player.y - 100) < 0:
						player.y -= player.y
					else:
						player.y -= 100

				# pause the game
				elif event.key == pygame.K_ESCAPE:
					# Draw some text
					pause_text = PAUSE_FONT.render("Paused", 1, BLUE)
					screen.blit(pause_text, (screen_width/2 - pause_text.get_width() /2, screen_height/2 - pause_text.get_height()/2))
					pause_text = SMALLER_PAUSE_FONT.render("Press any button to unpause", 1, BLUE)
					screen.blit(pause_text, ((screen_width/2 - pause_text.get_width() /2)+5, (screen_height/2 - pause_text.get_height()/2)+65))
					pygame.display.flip()
					# set paused to True
					PAUSED = True

			if event.type == SPAWNOB and not PAUSED: # don't spawn obstacles if the game is paused
				# spawn an obstacle every 0.8-4 seconds
				pygame.time.set_timer(SPAWNOB,random.randint((800 if score in range(50, 101) else (600 if score > 100 else 1500)), 4000))
				obstacles.spawn_obstacle()

		if PAUSED:
			# keep looping until unpaused
			continue

		# move
		move_player(player)
		score = obstacles.move_obstacles(score)

		# Draw the background
		screen.fill(WHITE if inp == 'n' else BLACK)
		# Draw the player
		pygame.draw.rect(screen, YELLOW, player)
		for ob in obstacles.obstacles:
			for obstacle in ob:
				# Draw the obstacles 
				pygame.draw.rect(screen, BLACK if inp == 'n' else WHITE, obstacle)
		# Draw the score
		score_text = SCORE_FONT.render("Score: " + str(score), 1, RED)
		screen.blit(score_text, (10, 10))
		pygame.display.flip()
		# 60 fps
		clock.tick(60)

		for ob in obstacles.obstacles:
			for obstacle in ob:
				# check if the player hit any obstacle
				if obstacle.colliderect(player):
					print('Game over!')
					print(score)
					pygame.quit()
					sys.exit()

if __name__ == "__main__":
	# Call the main function to play the game
	main()
