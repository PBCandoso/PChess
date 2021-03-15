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
boardState = []

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

def update_fen(bState):
    # Update fen through scanning the whole board
    # TODO: Do the whole fen string rather than positions alone
    fen = ""
    for row in bState:
        spaces = 0
        for col in row:
            if col != "-":
                if spaces != 0:
                    fen+=str(spaces)
                    spaces = 0
                fen+=col
            else:
                spaces+=1
        if spaces != 0:
            fen+=str(spaces)
        fen+="/"
    
    fen = fen[:-1]
    print(fen)
    return fen

def draw_board(screen):
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
    pygame.draw.rect(screen,BLACK,[X_PADDING,X_PADDING,BOARD_SIZE*SQUARE_SIZE,BOARD_SIZE*SQUARE_SIZE],2)

def draw_pieces(screen,fen):
    # Draw pieces based on fen string
    xcoords = "abcdefgh"
    ycoords = "87654321"
    bstate = decode_fen(fen)
    global boardState
    boardState = bstate
    for indx,row in enumerate(bstate):
        for indy,c in enumerate(row):
            image = fenToImage.get(c)
            if image:
                coords = board_coords.get(xcoords[indx] + ycoords[indy])
                screen.blit(image,coords)

def get_square_under_mouse(board):
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - (X_PADDING,X_PADDING)
    x,y = [int(v // SQUARE_SIZE) for v in mouse_pos]
    try:
        if x >= 0 and y >= 0: 
            return (board[y][x],x,y)
    except: 
        pass
    return None,None,None

def draw_selector(screen, piece, x, y):
    if piece != None:
        rect = (X_PADDING + x * SQUARE_SIZE, X_PADDING + y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)

def draw_drag(screen,board,selected_piece):
    if selected_piece and selected_piece[0] != "-":
        piece, x ,y = get_square_under_mouse(board)
        if x != None:
            rect = (X_PADDING + x * SQUARE_SIZE, X_PADDING + y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, (0, 255, 0, 50), rect, 2)
        p1 = fenToImage.get(selected_piece[0])
        pos = pygame.Vector2(pygame.mouse.get_pos())
        screen.blit(p1,p1.get_rect(center=pos + (1,1)))
        return (x,y)


# Initializations

def main():

    pygame.init()
    screen = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption("Pchess")
    # Draw initial board
    draw_board(screen)
    current_fen ="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" 
    draw_pieces(screen,current_fen)
    selected_piece = None
    drop_pos = None
    FPS = 60
    clock = pygame.time.Clock()

    # Game Loop

    running = True

    while running:
        piece, x, y = get_square_under_mouse(boardState)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if piece != None:
                        selected_piece = piece,x,y
                elif event.type == pygame.MOUSEBUTTONUP:
                    if drop_pos and drop_pos != (None, None):
                        piece,old_x,old_y = selected_piece
                        boardState[old_y][old_x] = "-"
                        new_x, new_y = drop_pos
                        boardState[new_y][new_x] = piece
                        current_fen = update_fen(boardState)
                    selected_piece = None
                    drop_pos = None
        screen.fill(BLACK)
        draw_board(screen)
        draw_pieces(screen,current_fen)
        # Draw selected square
        draw_selector(screen,piece,x,y)
        # Draw piece being dragged
        drop_pos = draw_drag(screen,boardState,selected_piece)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()