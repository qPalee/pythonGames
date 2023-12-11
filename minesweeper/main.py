import pygame
import random
import os

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
global isGameOver
isGameOver = False
dt = 0
screenWidth = screen.get_width()
screenHeight = screen.get_height()
cols = 13
rows = 18
tileWidth = screenWidth / cols
tileHeight = screenHeight / rows

FILE_PATH = os.path.dirname(os.path.abspath(__file__))

bombImg = pygame.image.load(os.path.join(FILE_PATH, "sprites/bomb.png"))
bombImg = pygame.transform.scale(bombImg, (tileWidth, tileHeight))
flagImg = pygame.image.load(os.path.join(FILE_PATH, "sprites/flag.png"))
flagImg = pygame.transform.scale(flagImg, (tileWidth, tileHeight))

bombsGenerated = False
noBombs = 0

buttonHeld = False

tilesChecked = []

font = pygame.font.SysFont("Monocraft", 16)

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.colour = "#000000"
        self.clicked = False
        self.hasBomb = False
        self.hasFlag = False
        self.noBombsSurrounding = 0
        self.neighbours = []
        self.isClicked = False

    def draw(self):
        if isGameOver:
            pygame.draw.rect(screen, self.colour, pygame.Rect(self.x * tileWidth, self.y * tileHeight, tileWidth + 1, tileHeight + 1), 2)
            if(self.isClicked == True):
                if not self.hasBomb:
                    if(self.noBombsSurrounding > 0):
                        text = font.render(str(self.noBombsSurrounding), True, "#000000")
                        screen.blit(text, ((self.x+.5)*tileWidth, (self.y+.25)*tileHeight))
                else: # Tile has bomb
                    screen.blit(bombImg, (self.x*tileWidth, self.y*tileHeight))
            else: # Tile not been clicked
                if self.hasBomb:
                    screen.blit(bombImg, (self.x*tileWidth, self.y*tileHeight))
        else: # Game not over
            pygame.draw.rect(screen, self.colour, pygame.Rect(self.x * tileWidth, self.y * tileHeight, tileWidth + 1, tileHeight + 1), 2)
            if(self.isClicked == True):
                if(self.noBombsSurrounding > 0):
                    text = font.render(str(self.noBombsSurrounding), True, "#000000")
                    screen.blit(text, ((self.x+.5)*tileWidth, (self.y+.25)*tileHeight))
            
            else:
                if self.hasFlag:
                    screen.blit(flagImg, (self.x*tileWidth, self.y*tileHeight))

    def tileClicked(self, x, y):
        if((x > self.x*tileWidth) and (x < (self.x+1)*tileWidth)):
            if(y > self.y*tileHeight and y < (self.y+1)*tileHeight):
                return True
            
        # Tile not clicked
        return False
    
# Add tiles to list
grid = [[Tile(x,y) for y in range(rows)] for x in range(cols)]
    
def generateBombs(x,y):
    area = cols * rows
    noBombs = round(area/60) * 10
    noBombsGenerated = 0
    while(noBombsGenerated < noBombs):
        xPos = random.randint(0,cols-1)
        yPos = random.randint(0,rows-1)
        if(grid[xPos][yPos].hasBomb == False):
            if((xPos < x-1 or xPos > x+1) and (yPos < y-1 or yPos > y+1)):
                grid[xPos][yPos].hasBomb = True
                noBombsGenerated += 1
    
    for i in range(cols):
        for j in range(rows):
            if i < cols - 1:
                grid[i][j].neighbours.append(grid[i+1][j])

            if (i > 0):
                grid[i][j].neighbours.append(grid[i - 1][j])
    
            if (j < rows - 1):
                grid[i][j].neighbours.append(grid[i][j + 1])
            
            if (j > 0):
                grid[i][j].neighbours.append(grid[i][j - 1])
            
            if (i > 0 and j > 0):
                grid[i][j].neighbours.append(grid[i - 1][j - 1])
            
            if (i < cols - 1 and j > 0):
                grid[i][j].neighbours.append(grid[i + 1][j - 1])
            
            if (i > 0 and j < rows - 1):
                grid[i][j].neighbours.append(grid[i - 1][j + 1])
            
            if (i < cols - 1 and j < rows - 1):
                grid[i][j].neighbours.append(grid[i + 1][j + 1])

            for k in grid[i][j].neighbours:
                if k.hasBomb:
                    grid[i][j].noBombsSurrounding += 1
    
    grid[x][y].isClicked = True
    grid[x][y].colour = "#646464"

    checkSurroundingBombs(grid[x][y])


def checkSurroundingBombs(tile):
    if(tile.noBombsSurrounding == 0):
        if tile not in tilesChecked:
            tilesChecked.append(tile)
            for newTile in tile.neighbours:
                grid[newTile.x][newTile.y].isClicked = True
                newTile.colour = "#646464"
                checkSurroundingBombs(newTile)

    
while running:

    if isGameOver:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("#C8C8C8")

        for tiles in grid:
            for tile in tiles:
                tile.draw()

        pygame.display.flip()
   
    else:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screenWidth = screen.get_width()
        screenHeight = screen.get_height()

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("#C8C8C8")

        for tiles in grid:
            for tile in tiles:
                tile.draw()

        # Click event
        if(pygame.mouse.get_pressed()[0]): # Left Click
            mouseX, mouseY = pygame.mouse.get_pos()
            for tmp in grid:
                for t in tmp:
                    if(t.tileClicked(mouseX, mouseY)):
                        if(t.isClicked == False):
                            if(bombsGenerated == False):
                                bombsGenerated = True
                                generateBombs(t.x,t.y)
                            else:
                                if(t.hasBomb):
                                    isGameOver = True

                                t.isClicked = True
                                t.hasFlag = False
                                t.colour = "#646464"
                                checkSurroundingBombs(t)


        if(pygame.mouse.get_pressed()[2]): # Right Click
            if not buttonHeld:
                buttonHeld = True
                mouseX, mouseY = pygame.mouse.get_pos()
                for tmp in grid:
                    for t in tmp:
                        if(t.tileClicked(mouseX, mouseY)):
                            if(t.isClicked == False):
                                t.hasFlag = not t.hasFlag
        else:
            buttonHeld = False
        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate
        # independent physics.
        dt = clock.tick(60) / 1000

pygame.quit()