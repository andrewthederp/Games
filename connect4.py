
import pygame, sys


def has_won_connect4(board):
	"""Checks if game is over"""
	height = 6
	width = 7
	for x in range(height):
		for y in range(width - 3):
			if (
				board[x][y] == board[x][y + 1]
				and board[x][y] == board[x][y + 2]
				and board[x][y] == board[x][y + 3]
				and board[x][y] != " "
			):
				return True
	for x in range(height - 3):
		for y in range(width):
			if (
				board[x][y] == board[x + 1][y]
				and board[x][y] == board[x + 2][y]
				and board[x][y] == board[x + 3][y]
				and board[x][y] != " "
			):
				return True
	for x in range(height - 3):
		for y in range(width - 3):
			if (
				board[x][y] == board[x + 1][y + 1]
				and board[x][y] == board[x + 2][y + 2]
				and board[x][y] == board[x + 3][y + 3]
				and board[x][y] != " "
			):
				return True
	for x in range(height - 3):
		for y in range(3, width):
			if (
				board[x][y] == board[x + 1][y - 1]
				and board[x][y] == board[x + 2][y - 2]
				and board[x][y] == board[x + 3][y - 3]
				and board[x][y] != " "
			):
				return True
	num = 0
	for row in board:
		for column in row:
			if column != " ":
				num += 1
	if num == (len(board) * len(board[0])):
		return False
	return None

def format_board(board):
    toDisplay = ""
    for y in range(6):
        for x in range(6):
            toDisplay += board[y][x] + '|'
        toDisplay += board[y][6] + "\n"
    toDisplay += "1|2|3|4|5|6|7|"
    return toDisplay

def place_token(board, turn, x, lst):
	y = 0
	while y <= 6:
		if y == 6:
			try:
				lst.pop()
				break
			except ValueError:
				pass
		if board[5 - y][x] == " ":
			board[5 - y][x] = turn
			break
		else:
			y += 1
	return board

pygame.init()
screen = pygame.display.set_mode(size:=(700,600))
pygame.display.set_caption("Connect4")
clock = pygame.time.Clock()

reds = []
blues = []
rects = []

falling = False
turn = 'r'
x = False

for i in range(7):
	rect = pygame.Rect((i*100,0), (i+100,size[1]))
	rects.append(rect)

board = [[" " for _ in range(7)] for i in range(6)]

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN and not falling:
			for rect in rects:
				if rect.collidepoint(event.pos):
					token = pygame.Rect((rect.x, -100), (100, 100))
					if turn == 'r':
						reds.append(token)
					else:
						blues.append(token)
					falling = token
					x = rect.x//100
					turn = 'b' if turn == 'r' else 'r'
					break


	screen.fill((255,255,255))
	for red in reds:
		if red == falling:
			red.y += 10
			if (red.y+red.h) >= size[1]:
				falling = False
				board = place_token(board, 'b' if turn == 'r' else 'r', x, reds)
				x = False
			elif red.collidelist([i for i in reds if i != red]) != -1:
				red.y -= 10
				falling = False
				board = place_token(board, 'b' if turn == 'r' else 'r', x, reds)
				x = False
			elif red.collidelist(blues) != -1:
				red.y -= 10
				falling = False
				board = place_token(board, 'b' if turn == 'r' else 'r', x, reds)
				x = False
		pygame.draw.ellipse(screen, (255,0,0), red)
		pygame.draw.ellipse(screen, (0,0,0), red, 1)
	for blue in blues:
		if blue == falling:
			blue.y += 10
			if (blue.y+blue.h) >= size[1]:
				falling = False
				board = place_token(board, 'b' if turn == 'r' else 'r', x, blues)
				x = False
			elif blue.collidelist([i for i in blues if i != blue]) != -1:
				blue.y -= 10
				falling = False
				board = place_token(board, 'b' if turn == 'r' else 'r', x, blues)
				x = False
			elif blue.collidelist(reds) != -1:
				blue.y -= 10
				falling = False
				board = place_token(board, 'b' if turn == 'r' else 'r', x, blues)
				x = False
		pygame.draw.ellipse(screen, (0,0,255), blue)
		pygame.draw.ellipse(screen, (0,0,0), blue, 1)
	for rect in rects:
		pygame.draw.rect(screen, (0,0,0), rect, 1)
	if has_won_connect4(board):
		print(('blue' if turn == 'r' else 'red') + ' has won connect4')
		pygame.quit()
		sys.exit()
	pygame.display.update()
	clock.tick(60)
