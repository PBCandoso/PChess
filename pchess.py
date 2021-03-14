import pygame
import os

RESOLUTION = (500,500)
BOARD_SIZE = 8
X_PADDING = 10
BOARD_LENGTH = RESOLUTION[1]-X_PADDING*2
SQUARE_SIZE = BOARD_LENGTH/BOARD_SIZE
BOARD_COLOR1 = (215,205,165)
BOARD_COLOR2 = (120,80,30)
BLACK = (0,0,0)
board_coords = {}

bK = pygame.image.load(os.path.join("static","bK.png"))
bQ = pygame.image.load(os.path.join("static","bQ.png"))
bR = pygame.image.load(os.path.join("static","bR.png"))
bB = pygame.image.load(os.path.join("static","bB.png"))
bN = pygame.image.load(os.path.join("static","bN.png"))
bP = pygame.image.load(os.path.join("static","bP.png"))

wK = pygame.image.load(os.path.join("static","wK.png"))
wQ = pygame.image.load(os.path.join("static","wQ.png"))
wR = pygame.image.load(os.path.join("static","wR.png"))
wB = pygame.image.load(os.path.join("static","wB.png"))
wN = pygame.image.load(os.path.join("static","wN.png"))
wP = pygame.image.load(os.path.join("static","wP.png"))

fenToImage = {"r": bR, "n": bN, "b": bB, "q": bQ, "k": bK, "p": bP, "R": wR, "N": wN, "B": wB, "Q": wQ, "K": wK, "P": wP, "-": None}

def decode_fen(fen):
    board = []
    fields = fen.split(" ")
    positions = fields[0]
    for i,v in enumerate(positions.split("/")):
        board.append([])
        for ch in v:
            if ch.isdigit():
                for spaces in range(int(ch)):
                    board[i].append("-")
            else:
                board[i].append(ch)
    return board


def draw_board(fen):
    # Draw board
    cnt = 0
    xcoords = "abcdefgh"
    ycoords = "87654321"
    for i in range(BOARD_SIZE):
        for z in range(BOARD_SIZE):
            x = X_PADDING + SQUARE_SIZE*z
            y = X_PADDING  + SQUARE_SIZE*i 
            board_coords[xcoords[i]+ycoords[z]] = (x,y)
            if cnt % 2 == 0:
                pygame.draw.rect(screen, BOARD_COLOR1,[x,y,SQUARE_SIZE,SQUARE_SIZE])
            else:
                pygame.draw.rect(screen, BOARD_COLOR2, [x,y,SQUARE_SIZE,SQUARE_SIZE])
            cnt +=1
        cnt-=1
    pygame.draw.rect(screen,BLACK,[X_PADDING,X_PADDING,BOARD_SIZE*SQUARE_SIZE,BOARD_SIZE*SQUARE_SIZE],1)
    # Draw pieces based on fen string
    bstate = decode_fen(fen)
    for indx,row in enumerate(bstate):
        for indy,c in enumerate(row):
            image = fenToImage.get(c)
            if image:
                coords = board_coords.get(xcoords[indx] + ycoords[indy])
                screen.blit(image,coords)
    pygame.display.update()

# Initializations

pygame.init()
screen = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("Pchess")
screen.fill(BLACK)
draw_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
FPS = 30
clock = pygame.time.Clock()

running = True

while running:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        print("fuck")
        pygame.display.flip()
        clock.tick(FPS)