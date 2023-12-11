import pygame

WIDTH = 1280
HEIGHT = 720
FPS = 60
TILEWIDTH = WIDTH/3
TILEHEIGHT = HEIGHT/3

currentTurn = 'X'
gameOver = False
winningLine = -1

## initialize pygame and create window
pygame.init()
pygame.mixer.init()  ## For sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
clock = pygame.time.Clock()     ## For syncing the FPS

font = pygame.font.SysFont("Monocraft", 100)

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.colour = "#000000"
        self.state = 0 # 0 -> Blank, 1 -> X, 2 -> O

    def draw(self):
        pygame.draw.rect(screen, self.colour, pygame.Rect(self.x * TILEWIDTH, self.y * TILEHEIGHT, TILEWIDTH, TILEHEIGHT), 3)

        if(self.state > 0):
            if(self.state == 1):
                text = font.render('X', True, "#000000")
            
            else:
                text = font.render('O', True, "#000000")
            
            screen.blit(text, ((self.x + .45) * TILEWIDTH, (self.y + .3) * TILEHEIGHT))

    def tileClicked(self, x, y):
        if((x > self.x * TILEWIDTH) and (x < (self.x+1) * TILEWIDTH)):
            if(y > self.y * TILEHEIGHT and y < (self.y+1) * TILEHEIGHT):
                return True
            
        # Tile not clicked
        return False
    
    def updateState(self, currentTurn):
        if(currentTurn == 'X'):
            self.state = 1
            return
        
        self.state = 2

    

# Create array which holds all tiles
grid = [[Tile(x,y) for y in range(3)] for x in range(3)]

def checkWin():
    if((grid[0][0].state == grid[0][1].state == grid[0][2].state) and grid[0][0].state != 0):
        return 1
    
    if((grid[1][0].state == grid[1][1].state == grid[1][2].state) and grid[1][0].state != 0):
        return 2
    
    if((grid[2][0].state == grid[2][1].state == grid[2][2].state) and grid[2][0].state != 0):
        return 3
    
    if((grid[0][0].state == grid[1][0].state == grid[2][0].state) and grid[0][0].state != 0):
        return 4

    if((grid[0][1].state == grid[1][1].state == grid[2][1].state) and grid[0][1].state != 0):
        return 5
    
    if((grid[0][2].state == grid[1][2].state == grid[2][2].state) and grid[0][2].state != 0):
        return 6
    
    if((grid[0][0].state == grid[1][1].state == grid[2][2].state) and grid[0][0].state != 0):
        return 7
    
    if((grid[2][0].state == grid[1][1].state == grid[0][2].state) and grid[2][0].state != 0):
        return 8
    
    return -1

## Game loop
running = True
while running:

    #1 Process input/events
    clock.tick(FPS)     ## will make the loop run at the same speed all the time
    for event in pygame.event.get():        # gets all the events which have occured till now and keeps tab of them.
        ## listening for the the X button at the top
        if event.type == pygame.QUIT:
            running = False




    #3 Draw/render
    screen.fill("#6c6565")

    for arr in grid:
        for t in arr:
            t.draw()
        
    if gameOver == False:        
        if(pygame.mouse.get_pressed()[0]): # Left Click
            mouseX, mouseY = pygame.mouse.get_pos()
            for tmp in grid:
                for t in tmp:
                    if(t.tileClicked(mouseX, mouseY)):
                        if(t.state == 0): # Tile is blank
                            t.updateState(currentTurn)
                            winningLine = checkWin()
                            if(winningLine != -1):
                                gameOver = True
                            if(currentTurn == 'X'):
                                currentTurn = 'O'
                            else:
                                currentTurn = 'X'
    else:
        match winningLine:
            case 1:
                pygame.draw.line(screen, "#000000", (.51* TILEWIDTH, .25 * TILEHEIGHT), (.51 * TILEWIDTH, 2.75*TILEHEIGHT), 5)

            case 2:
                pygame.draw.line(screen, "#000000", (1.51* TILEWIDTH, .25 * TILEHEIGHT), (1.51 * TILEWIDTH, 2.75*TILEHEIGHT), 5)

            case 3:
                pygame.draw.line(screen, "#000000", (2.51* TILEWIDTH, .25 * TILEHEIGHT), (2.51 * TILEWIDTH, 2.75*TILEHEIGHT), 5)

            case 4:
                pygame.draw.line(screen, "#000000", (.25 * TILEWIDTH, .5 * TILEHEIGHT), (2.75 * TILEWIDTH, .5*TILEHEIGHT), 5)

            case 5:
                pygame.draw.line(screen, "#000000", (.25 * TILEWIDTH, 1.5 * TILEHEIGHT), (2.75 * TILEWIDTH, 1.5*TILEHEIGHT), 5)

            case 6:
                pygame.draw.line(screen, "#000000", (.25 * TILEWIDTH, 2.5 * TILEHEIGHT), (2.75 * TILEWIDTH, 2.5*TILEHEIGHT), 5)

            case 7:
                pygame.draw.line(screen, "#000000", (.25 * TILEWIDTH, .25 * TILEHEIGHT), (2.75 * TILEWIDTH, 2.75 * TILEHEIGHT), 5)

            case 8:
                pygame.draw.line(screen, "#000000", (.25 * TILEWIDTH, 2.75 * TILEHEIGHT), (2.75 * TILEWIDTH, .25 * TILEHEIGHT), 5)
        


    ## Done after drawing everything to the screen
    pygame.display.flip() 

pygame.quit()