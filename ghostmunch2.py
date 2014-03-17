#ghostcount is a program consisting of the minigame "Ghost Count" in Pie Parlor

#----------------INITIALIZATION
import pygame, sys
import pygame.font
from pygame.locals import *
import math, random

pygame.init()

W = 640
H = 480
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((W,H))
pygame.display.set_caption('Ghost Munch 2')

#Colors
red = (255,0,0)
lime = (152,251,120)
blue = (0,0,255)
sky = (0,191,255)
darkBlue = (0,0,128)
white = (255,255,255)
offWhite = (240,240,240)
black = (0,0,0)
softBlack = (30,30,30)
pink = (240,4,127)
brown = (205,133,63)
lightBrown = (222, 200, 120)
ivory = (255,240,220)

#---------------------------TEXT
pygame.font.init()
#makeText is a function that returns a tuple (textSurface, textRect)
#Note that fontName is a string in quotes which must be in the same file
def makeText(text, fontName, fontSize, color, center):
    font = pygame.font.Font(fontName, fontSize)
    textSurf = font.render(text, False, color)
    textRect = textSurf.get_rect()
    textRect.center = center
    return (textSurf, textRect)

#Title
titleSurf, titleRect = makeText('GHOST MUNCH 2', 'Minecraftia.ttf', 48, darkBlue, (320,150))
subtitleSurf, subtitleRect = makeText('Press enter to start', 'Minecraftia.ttf', 24, pink, (320,300))
#End game
continueSurf, continueRect = makeText('Play Again?', 'Minecraftia.ttf', 24, darkBlue, (328,260))


#-------------------------FUNCTIONS
#checker is a function that draws a checkerboard pattern
#rect = (x, y, width, heigth)
def checker(rect, squareSize, color):
    i = rect[0]     #Steps through x-coordinate of square
    j = rect[1]     #Steps through y-coordinate of square
    b1 = 0          #Switches colors moving horizontally
    b2 = 0          #Switches colors moving vertically

    for j in range(rect[1], rect[1]+rect[3], squareSize):
        b1 = b2
        for i in range(rect[0], rect[0]+rect[2], squareSize):
            pygame.draw.rect(screen, color[b1], (i, j, squareSize, squareSize), 0)
            b1 = (b1 + 1)%2
        b2 = (b2+1)%2
        i = rect[0]


##-------------------------CLASSES
class Pie(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        #Set the background color and Surface object
        self.image = pygame.Surface([42,42])
        self.image.fill(white)
        self.image.set_colorkey(white)

        x = 21
        y = 21

        #Draw the pie
        pygame.draw.circle(self.image, lightBrown, (x,y), 20, 0)
        pygame.draw.circle(self.image, brown, (x,y), 20, 2)
        pygame.draw.circle(self.image, brown, (x,y), 2, 0)
        pygame.draw.line(self.image, brown, (x+5,y), (x+12,y), 2)
        pygame.draw.line(self.image, brown, (x,y-5), (x,y-12), 2)
        pygame.draw.line(self.image, brown, (x-5,y), (x-12,y), 2)
        pygame.draw.line(self.image, brown, (x,y+5), (x,y+12), 2)

        #Rectangle
        self.rect = self.image.get_rect()

class Ghost(pygame.sprite.Sprite):
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)

        #Set the background color and Surface object
        self.image = pygame.Surface([50,70])
        self.image.fill(white)
        self.image.set_colorkey(white)

        x = 25
        y = 25

        #Draw the Ghost
        #draw the body
        pygame.draw.circle(self.image, color, (x,y), 25, 0)
        pygame.draw.rect(self.image, color, (x-25,y,50,35), 0)
        #draw the feet
        pygame.draw.circle(self.image, color, (x-19,y+35), 6, 0)
        pygame.draw.circle(self.image, color, (x-7,y+35), 6, 0)
        pygame.draw.circle(self.image, color, (x+7,y+35), 6, 0)
        pygame.draw.circle(self.image, color, (x+19,y+35), 6, 0)
        #draw the eyes
        pygame.draw.circle(self.image, black, (x-10,y), 4, 0)
        pygame.draw.circle(self.image, black, (x+10,y), 4, 0)

        #Rectangle
        self.rect = self.image.get_rect()


#-------------OTHER STUFF
#Booleans for menu, gameplay and endgame
inMenu = True
inGame = False
endGame = False

#MENU OBJECTS
menu_sprite_list = pygame.sprite.Group()

#Create pies and ghosts
pie_xcoord = [0, 150, 300, 450, 600]
ghost_xcoord = [70, 220, 370, 520, 670]

for x in pie_xcoord:
    pie = Pie()
    pie.rect.x = x
    pie.rect.y = 210
    menu_sprite_list.add(pie)

for x in ghost_xcoord:
    ghost = Ghost(ivory)
    ghost.rect.x = x
    ghost.rect.y = 200
    menu_sprite_list.add(ghost)

#GAME OBJECTS
moveSpeed = 8   #player movement speed
pie_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

#Create Pies
pieNum = 50
for i in range(pieNum):
    #create Pie object
    pie = Pie()
    #Set random location for ghost
    pie.rect.x = random.randrange(W-50)
    pie.rect.y = random.randrange(H-50)
    #Add the pie to the lists
    pie_list.add(pie)
    all_sprites_list.add(pie)

#Create Ghost player 1 and 2
player1 = Ghost(ivory)
player1.rect.x = random.randrange(W/2)
player1.rect.y = random.randrange(H-50)
all_sprites_list.add(player1)

player2 = Ghost(sky)
player2.rect.x = random.randrange(W/2, W-50)
player2.rect.y = random.randrange(H-50)
all_sprites_list.add(player2)

#Score
score1 = 0
score2 = 0

#Winner strings and pointer
winner = ['DRAW', 'PLAYER 1 WINS', 'PLAYER 2 WINS']
winboo = 0

#-------------------MAIN GAME LOOP--------------------#
while True:

    screen.fill(white)

    #Event handling loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        #determine whether enter has been pressed
        if event.type == KEYDOWN:
            if inMenu == True:
                if event.key == K_RETURN:
                    inMenu = False
                    inGame = True
            if endGame == True:
                if event.key == K_RETURN:
                    endGame = False
                    inGame = True
                    score1 = 0
                    score2 = 0
                    winboo = 0
                    #new pies
                    for i in range(pieNum):
                        #create Pie object
                        pie = Pie()
                        #Set random location for ghost
                        pie.rect.x = random.randrange(W-50)
                        pie.rect.y = random.randrange(H-50)
                        #Add the pie to the lists
                        pie_list.add(pie)
                        all_sprites_list.add(pie)
                    #new player location
                    player1.rect.x = random.randrange(W/2)
                    player1.rect.y = random.randrange(H-50)
                    player2.rect.x = random.randrange(W/2, W-50)
                    player2.rect.y = random.randrange(H-50)

    if inMenu == True:
        #Draw Background
        pygame.draw.rect(screen, lime, (0,0,640,400), 0)
        checker((0,400,640,80), 20, (softBlack, offWhite))
        pygame.draw.rect(screen, black, (0,400,640,80), 2)

        #Blit text to screen
        screen.blit(titleSurf, titleRect)
        screen.blit(subtitleSurf, subtitleRect)

        #Move pies and ghosts
        menu_sprite_list.draw(screen)
        for thing in menu_sprite_list:
            thing.rect.x += 5
            if thing.rect.x == 700:
                thing.rect.x = -50

    #If there are no more pies left to eat, the game is over
    if not pie_list:
        inGame = False
        endGame = True
        

    if inGame == True:
        #Draw Background
        pygame.draw.rect(screen, lime, (0,0,640,400), 0)
        checker((0,400,640,80), 20, (softBlack, offWhite))
        pygame.draw.rect(screen, black, (0,400,640,80), 2)

        #Check for keyboard input to control player
        keys = pygame.key.get_pressed()
        #Arrow keys move player
        #can't move beyond the screen frame
        if keys[K_d]:
            if player1.rect.x > (W-moveSpeed):
                player1.rect.x = -50
            player1.rect.x += moveSpeed
        if keys[K_a]:
            if player1.rect.x < (-50+moveSpeed):
                player1.rect.x = W
            player1.rect.x -= moveSpeed
        if keys[K_s]:
            if player1.rect.y > (H-moveSpeed):
                player1.rect.y = -50
            player1.rect.y += moveSpeed
        if keys[K_w]:
            if player1.rect.y < (-50+moveSpeed):
                player1.rect.y = H
            player1.rect.y -= moveSpeed
        if keys[K_RIGHT]:
            if player2.rect.x > (W-moveSpeed):
                player2.rect.x = -50
            player2.rect.x += moveSpeed
        if keys[K_LEFT]:
            if player2.rect.x < (-50+moveSpeed):
                player2.rect.x = W
            player2.rect.x -= moveSpeed
        if keys[K_DOWN]:
            if player2.rect.y > (H-moveSpeed):
                player2.rect.y = -50
            player2.rect.y += moveSpeed
        if keys[K_UP]:
            if player2.rect.y < (-50+moveSpeed):
                player2.rect.y = H
            player2.rect.y -= moveSpeed

        #Check for collisions
        pie_hit_list1 = pygame.sprite.spritecollide(player1, pie_list, True)
        for pie in pie_hit_list1:
            score1 += 1
        pie_hit_list2 = pygame.sprite.spritecollide(player2, pie_list, True)
        for pie in pie_hit_list2:
            score2 += 1

        #Draw all of the sprites
        all_sprites_list.draw(screen)

        #Draw scores
        score1Surf, score1Rect = makeText(str(score1), 'Minecraftia.ttf', 24, red, (24,20))
        screen.blit(score1Surf, score1Rect)
        score2Surf, score2Rect = makeText(str(score2), 'Minecraftia.ttf', 24, red, (W-24,20))
        screen.blit(score2Surf, score2Rect)

    if endGame == True:
        #Draw Background
        pygame.draw.rect(screen, lime, (0,0,640,400), 0)
        checker((0,400,640,80), 20, (softBlack, offWhite))
        pygame.draw.rect(screen, black, (0,400,640,80), 2)

        #Draw scores
        score1Surf, score1Rect = makeText(str(score1), 'Minecraftia.ttf', 24, red, (24,20))
        screen.blit(score1Surf, score1Rect)
        score2Surf, score2Rect = makeText(str(score2), 'Minecraftia.ttf', 24, red, (W-24,20))
        screen.blit(score2Surf, score2Rect)

        #Endgame Text
        if score1 > score2:
            winboo = 1
        elif score2 > score1:
            winboo = 2
        endSurf, endRect = makeText(winner[winboo], 'Minecraftia.ttf', 48, pink, (320,180))
        screen.blit(endSurf, endRect)
        screen.blit(continueSurf, continueRect)

    pygame.display.update()
    fpsClock.tick(20)
