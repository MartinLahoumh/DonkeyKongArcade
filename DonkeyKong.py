import pygame
import random 
import os
from settings import * #Import everything from settings.py

pygame.init() #Initialize all modules 

#OBJECTS

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, imgWidth, imgHeight, image):
        pygame.sprite.Sprite.__init__(self)
        self.width = imgWidth
        self.height = imgHeight
        self.image = pygame.image.load(os.path.join('images', image)).convert_alpha() #Sprite Image
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft = pos) #Get a rectangle the same size as the image with its pos starting at topleft
       
class Barell(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.xCord = 210
        self.yCord = tileList[len(tileList)-5].y - 35
        self.width = width
        self.height = height
        self.velocity = 5 #How fast the barell will move
        self.barellSprites = [] #Will store all barell sprites
        self.movingRight = True #Default movement
        self.movingLeft = False
        self.nextLedge = False
        self.canMove = False
        self.frame = 0 #For animation purposes
        for i in range(1,5):
            #This will load an image from the 'image' file source
            #note: convert() is used to optimize image formate and to make the drawing faster
            img = pygame.image.load(os.path.join('Images', 'Barell' + str(i) + '.png')).convert_alpha()
            #Scale the image down 
            img = pygame.transform.scale(img, (35,35))
            self.barellSprites.append(img)
            #Since images do not have a position, we have to store in a rect. With get_rect(), we get a new rect
            #that is the same size of the image and is placed w/ the cords (0,0)
            self.image = self.barellSprites[i-1]
            self.image = pygame.transform.scale(self.image, (width, 10))
        self.image = self.barellSprites[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.xCord
        self.rect.y = self.yCord

    def barellMovement(self):
        if self.canMove: 
            #Move in a straight line (NO ANIMATION)
            self.hitbox = self.hitbox = pygame.Rect(self.rect.x, self.rect.y, 40, 45)
            #pygame.draw.rect(display, (255,0,0), self.hitbox, 2)
            #Check if hit boundaries
            if self.xCord <= 11:
                self.movingRight = True
                self.movingLeft = False
                self.yCord += 5 #Make barell fall
                self.rect.y = self.yCord
            elif self.xCord >= width - 40:
                self.movingRight = False
                self.movingLeft = True
                self.yCord += 5 #Make barell fall
                self.rect.y = self.yCord

            for tile in tileList:
                if pygame.Rect.colliderect(self.hitbox, tile):
                    if self.movingRight:
                        self.xCord += self.velocity
                        self.rect.x = self.xCord
                        self.yCord = tile.y - 35
                        self.rect.y = self.yCord
                        #ANIMATION
                        if self.frame > 3:
                            self.frame = 0
                        else:
                            self.frame += 1
                        self.image = self.barellSprites[self.frame-1]

                        
                    elif self.movingLeft:
                        self.xCord -= self.velocity
                        self.rect.x = self.xCord
                        self.yCord = tile.y - 35
                        self.rect.y = self.yCord
                        #ANIMATION
                        if self.frame > 3:
                            self.frame = 0
                        else:
                            self.frame += 1
                        self.image = self.barellSprites[self.frame-1]

class Player(pygame.sprite.Sprite):
    def __init__(self, xCord, yCord, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        self.velocity = 10 #how fast the character moves
        self.xCord = xCord
        self.yCord = yCord
        self.moveLeft = True #Determines if the player is able to walk left
        self.moveRight = True #Determines if the player is able to walk right
        self.lookingLeft = False #Determines which idle sprite to go back to after a jump
        self.lookingRight = False
        self.movingLeft = False #This keeps track if player is currently walking in a cerrtain direction
        self.movingRight = False
        self.walkSprites = [] #Will store all walking sprites
        self.climbSprites = [] #Will store all climb sprites
        self.frame = 0 #For animation purposes
        self.climb = False
        self.jump = False
        self.descend = False
        self.gravity = 1
        self.jumpVelocity = 10
        self.jumpHeight = 20
        self.currentTileHeight = 0
        self.playerToGround = 0

        for i in range(1,4):
            #This will load an image from the 'image' file source
            #note: convert() is used to optimize image formate and to make the drawing faster
            img = pygame.image.load(os.path.join('Images', 'PlayerWalk' + str(i) + '.png')).convert_alpha()
            #Scale the image down 
            img = pygame.transform.scale(img, (100,100))
            self.walkSprites.append(img)
            img2 = pygame.image.load(os.path.join('Images', 'PlayerClimb' + str(i) + '.png')).convert_alpha()
            img2 = pygame.transform.scale(img2, (100,100))
            self.climbSprites.append(img2)
            #Since images do not have a position, we have to store in a rect. With get_rect(), we get a new rect
            #that is the same size of the image and is placed w/ the cords (0,0)
            self.image = self.walkSprites[i-1]
            self.image = pygame.transform.scale(self.image, (width, 30))
        #Jumping image (seperate since it is only 1)
        self.jumpImg = pygame.image.load(os.path.join('Images', 'PlayerJump.png')).convert_alpha()
        self.jumpImg = pygame.transform.scale(self.jumpImg, (100, 100))
        #set image to idle position 
        self.image = self.walkSprites[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.xCord
        self.rect.y = self.yCord
    
    def playerCollision(self):
        #Create the players hitbox
        self.hitbox = pygame.Rect(self.rect.x + 30, self.rect.y + 30, 40, 45)
        #pygame.draw.rect(display, (255,0,0), self.hitbox, 2)
        #For walking on platforms (red tiles)
        #We will need player to not be jumping, sicne when they jump, the head will collide with the top platforms
        if self.jump == False:
            for tile in tileList:
                if pygame.Rect.colliderect(self.hitbox, tile): #If player collides with a tile
                    #Move player up to that tile
                    self.rect.y = tile.y - 70
                    self.currentTileHeight = tile.y
                    self.playerToGround = self.currentTileHeight

        #For climbing ladders
        if pygame.Rect.colliderect(self.hitbox, ladderList[0]) or pygame.Rect.colliderect(self.hitbox, ladderList[1]) or pygame.Rect.colliderect(self.hitbox, ladderList[2]) or pygame.Rect.colliderect(self.hitbox, ladderList[3]) or pygame.Rect.colliderect(self.hitbox, ladderList[4]) or pygame.Rect.colliderect(self.hitbox, ladderList[5]) or pygame.Rect.colliderect(self.hitbox, ladderList[6]) or pygame.Rect.colliderect(self.hitbox, ladderList[7]) or pygame.Rect.colliderect(self.hitbox, ladderList[8]) or pygame.Rect.colliderect(self.hitbox, ladderList[9]) or pygame.Rect.colliderect(self.hitbox, ladderList[10]) or pygame.Rect.colliderect(self.hitbox, ladderList[11]):
            #Check if it is a complete ladder
            self.climb = True
        else: 
            self.climb = False


    def movement(self):
        keys = pygame.key.get_pressed() #List of keys that we can press
        #This is the boundary of our screen, this will make sure that the player will not be able to go out of bounds
        if self.jump == False:
            if self.xCord <= 0:
                self.moveLeft = False
                self.moveRight = True
            elif self.xCord >= width - self.width:
                self.moveLeft = True
                self.moveRight = False
            else:
                self.moveLeft = True
                self.moveRight = True

        #Player Movement & Walk Animation
        if keys[pygame.K_a]:
            self.lookingLeft = True
            self.lookingRight = False
            if self.moveLeft == True:
                self.movingLeft = True
                self.moveRight = False
                if self.jump == False:
                    if self.frame > 2:
                        self.frame = 0
                    else:
                        self.frame += 1
                    self.image = self.walkSprites[self.frame-1]
            elif self.moveLeft == False and self.jump == False:
                self.xCord -= 0
                if self.frame > 2:
                    self.frame = 0
                else:
                    self.frame += 1
                self.image = self.walkSprites[self.frame-1]
            if self.movingLeft == True: 
                self.xCord -= self.velocity
                self.rect.x = self.xCord
        elif keys[pygame.K_d]:
            self.lookingLeft = False
            self.lookingRight = True
            if self.moveRight == True:
                self.movingLeft = False
                self.movingRight = True
                if self.jump == False:
                    if self.frame > 2:
                        self.frame = 0
                    else:
                        self.frame += 1
                    self.image = pygame.transform.flip(self.walkSprites[self.frame-1], True, False)
            elif self.moveRight == False and self.jump == False:
                self.xCord += 0
                if self.frame > 2:
                    self.frame = 0 
                else:
                    self.frame += 1
                self.image = pygame.transform.flip(self.walkSprites[self.frame-1], True, False)
            if self.movingRight == True:
                self.xCord += self.velocity
                self.rect.x = self.xCord
        elif keys[pygame.K_w]: #Player climb movement & climb animation
            if self.climb == True:
                self.yCord -= (self.velocity-5)
                if self.frame > 2:
                    self.frame = 0
                else:
                    self.frame += 1
                self.image = self.climbSprites[self.frame-1]
                self.rect.y = self.yCord
        if keys[pygame.K_j]:
            #Lock left and right movement
            self.velocity = 4
            if self.movingRight == True:
                self.moveLeft = False
                self.moveRight = True
                self.movingLeft = False
                self.movingRight = True
            elif self.movingLeft == True:
                self.moveLeft = True
                self.moveRight = False
                self.movingLeft = True
                self.movingRight = False
            else:
                self.moveLeft = False
                self.moveRight = False
                self.movingLeft = False
                self.movingRight = False

            if self.lookingRight == True:
                self.image = pygame.transform.flip(self.jumpImg, True, False)
            elif self.lookingLeft == True:
                    self.image = self.jumpImg
            if self.jump == False:
                self.jump = True
            #note: Player jumps a great distance x-cord wise when walkign and then jumping, 
            #so shorten x-velocity

    def playerJump(self, maxVelocity):
        if self.jumpVelocity == 10:
            self.yCord = self.currentTileHeight - 70
            print("DONE")
        self.jumpVelocity -= 1
        self.yCord -= self.jumpVelocity
        self.rect.y = self.yCord
        if self.jumpVelocity <= -9:
            self.jumpVelocity = 10 #reset
            self.velocity = 10
            self.yCord = self.currentTileHeight - 70
            self.rect.y = self.yCord
            if self.lookingRight == True:
                self.image = pygame.transform.flip(self.walkSprites[0], True, False)
            elif self.lookingLeft == True:
                self.image = self.walkSprites[0]
            self.jump = False

class DK(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.xCord = 84
        self.yCord = 53
        self.width = 200
        self.height = 200
        self.donkeyKongSprites = []
        self.image = 0
        self.frame = 0
        self.timer = 0
        for i in range(1, 3):
            self.image = pygame.image.load(os.path.join('Images', 'DonkeyKong' + str(i) + '.png')).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width,self.height)) 
            self.image = pygame.transform.flip(self.image, True, False)
            for i in range(0,5):
                self.donkeyKongSprites.append(self.image)
            self.image = self.donkeyKongSprites[i-1]  
        self.image = pygame.transform.flip(self.donkeyKongSprites[0], True, False)
        self.donkeyKongSprites.append(self.image)
        for i in range(0,5):
            self.donkeyKongSprites.append(self.image)
        self.image = self.donkeyKongSprites[7]
        self.rect = self.image.get_rect()
        self.rect.x = self.xCord
        self.rect.y = self.yCord
    
    def spawnDKBarell(self, barellGroup):
        if self.timer >= 30:
            if self.frame < len(self.donkeyKongSprites):
                self.image = self.donkeyKongSprites[self.frame]
                self.frame += 1
            else:
                spawnBarell()
                self.frame = 0
                self.image = self.donkeyKongSprites[7]
                self.timer = 0
        self.timer += 1
        

    

#SETUP (INITAL SETTINGS)
 
 #Inital settings of game
#General
width = 700 #640 wuz old one 700
height = 920
score = 0
velocity = 10
clock = pygame.time.Clock() #Controlls speed of the game
#Set the size of the screen window
display = pygame.display.set_mode((width,height))
pygame.display.set_caption('Donkey Kong') #Title for window 

#Player
player = Player(50,height - 60,40,60)
playerGroup = pygame.sprite.Group()
playerGroup.add(player)

#Create the level layout
tileGroup = pygame.sprite.Group() #Stores all the tiles
xCordList = [] #This will hold all tile xCords (Used for collision)
yCordList = []
tileList = []#This is so we can access each tile
for ledge in range(1,7): #Since there are 6 ledges in total, we wi.ll cycle 6 times, 1 for each ledge
    for tileNum in range (1,15):
        xCord = 0 + (60*(tileNum-1)) #player.xCord + (60*(tileNum-1)) #60 Is the width of each tile
        #Ledge 1 is a special case since at the start, each tile is connected regularly with no 
        #"stair case" effect being done to it
        if ledge == 1:
            if tileNum >= 1 and tileNum <= 6:
                yCord = height - 28
                tileObject = Tile((xCord, yCord), 60, 25, 'platform.png') #create the tile
                tileGroup.add(tileObject) #Add the tile to the sprite group
                tileList.append(tileObject.rect)
                xCordList.append(xCord)
                yCordList.append(yCord) 
            else:
                yCord = (height-28) - ((tileNum-6)*3) #Increase a tile ycord by 5 units
                tileObject = Tile((xCord, yCord), 60, 25, 'platform.png')
                tileGroup.add(tileObject)
                tileList.append(tileObject.rect)
                xCordList.append(xCord)
                yCordList.append(yCord)  
        elif ledge == 6:
                xCord = width - 100
                xCord = xCord - (60 *(tileNum-1))
                if tileNum >= 1 and tileNum <= 6:
                    yCord = (height - (140* (ledge-1))) #Increase a tile ycord by 5 units
                    yCord = yCord - ((tileNum-1)*3)
                    tileObject = Tile((xCord, yCord), 60, 25, 'platform.png')
                    tileGroup.add(tileObject)
                    tileList.append(tileObject.rect)
                else:
                    yCord = yCord
                    tileObject = Tile((xCord, yCord), 60, 25, 'platform.png')
                    tileGroup.add(tileObject)
                    tileList.append(tileObject.rect)
                    
        else:
            #All other ledges have a stair case effect where the y cord of the tile is slightly higher than the previous
            if ledge%2 == 0: #An even ledge expands to the left
                xCord = width - (100)
                yCord = (height - (140* (ledge-1))) #Increase a tile ycord by 5 units
                xCord = xCord - (60 *(tileNum-1))
                yCord = yCord - ((tileNum-1)*3)
                tileObject = Tile((xCord, yCord), 60, 25, 'platform.png')
                tileGroup.add(tileObject)
                tileList.append(tileObject.rect)
                xCordList.append(xCord) 
                yCordList.append(yCord)
            else: #An odd ledge expands to the right
                xCord = 50
                yCord = (height - (140* (ledge-1))) #Increase a tile ycord by 5 units
                xCord = xCord + (60 *(tileNum-1))
                yCord = yCord - ((tileNum-1)*3)
                tileObject = Tile((xCord, yCord), 60, 25, 'platform.png')
                tileGroup.add(tileObject)
                tileList.append(tileObject.rect)
                xCordList.append(xCord) 
                yCordList.append(yCord)  
barellStack = Tile((-20, 53), 200,200, 'StackBarell.png')
tileGroup.add(barellStack)
#Test Barell
#test = Barell(0,165,5,5)
testGroup = pygame.sprite.Group()
#testGroup.add(test)
#Background Elements (Ladders, hammer, DonkeyKong, Pauline)
#LADDERS
#Since ladder placement is not random, we got to place them individually at each respected tile

#THis will indicate if it is a broken ladder or a fixed. This is important since player can not go to next
#ledge with a broken ladder, but they are able to climb the broken ladder for protection
ladderType = [] #0 is a broken ladder, 1 is a fixed ladder
ladderList = []
for i in range(0,len(tileList)):
    if i == 4:
        ladder = Tile((tileList[i].x,tileList[i].y - 28), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladder =  Tile((tileList[i].x,tileList[i].y - 103), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladderType.append(0) 
    elif i == 10: 
        ladder = Tile((tileList[i].x,tileList[i].y - 28), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladder =  Tile((tileList[i].x,tileList[i].y - 56), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladder =  Tile((tileList[i].x,tileList[i].y - 84), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladderType.append(1) 
    elif i == 19: 
        ladder = Tile((tileList[i].x,tileList[i].y - 28), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladder =  Tile((tileList[i].x,tileList[i].y - 56), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladder =  Tile((tileList[i].x,tileList[i].y - 84), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladder =  Tile((tileList[i].x,tileList[i].y - 112), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladderType.append(1) 
    elif i == 23:
        ladder = Tile((tileList[i].x,tileList[i].y - 28), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladder =  Tile((tileList[i].x,tileList[i].y - 56), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladder =  Tile((tileList[i].x,tileList[i].y - 84), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladderType.append(1) 
    elif i == 30: 
        ladder = Tile((tileList[i].x,tileList[i].y - 28), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladder =  Tile((tileList[i].x,tileList[i].y - 56), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladder =  Tile((tileList[i].x,tileList[i].y - 112), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladder =  Tile((tileList[i].x,tileList[i].y - 134), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladderType.append(0) 
    elif i == 33:
        ladder = Tile((tileList[i].x,tileList[i].y - 28), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladder =  Tile((tileList[i].x,tileList[i].y - 56), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladder =  Tile((tileList[i].x,tileList[i].y - 84), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladder =  Tile((tileList[i].x,tileList[i].y - 112), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladderType.append(1) 
    elif i == 37:
        ladder = Tile((tileList[i].x,tileList[i].y - 28), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladder =  Tile((tileList[i].x,tileList[i].y - 56), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladder =  Tile((tileList[i].x,tileList[i].y - 84), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladderType.append(1) 
    elif i == 43:
        ladder = Tile((tileList[i].x,tileList[i].y - 28), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladder =  Tile((tileList[i].x,tileList[i].y - 56), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladder =  Tile((tileList[i].x,tileList[i].y - 112), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladder =  Tile((tileList[i].x,tileList[i].y - 134), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladderType.append(0)
    elif i == 48: 
        ladder = Tile((tileList[i].x,tileList[i].y - 28), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladder =  Tile((tileList[i].x,tileList[i].y - 56), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladder =  Tile((tileList[i].x,tileList[i].y - 84), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladder =  Tile((tileList[i].x,tileList[i].y - 112), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladderType.append(1) 
    elif i == 51: 
        ladder = Tile((tileList[i].x,tileList[i].y - 28), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladder =  Tile((tileList[i].x,tileList[i].y - 56), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladder =  Tile((tileList[i].x,tileList[i].y - 84), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladderType.append(1) 
    elif i == 60:
        ladder = Tile((tileList[i].x,tileList[i].y - 28), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladder =  Tile((tileList[i].x,tileList[i].y - 56), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladder =  Tile((tileList[i].x,tileList[i].y - 115), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladderType.append(0) 
    elif i == 65:
        ladder = Tile((tileList[i].x,tileList[i].y - 28), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladder =  Tile((tileList[i].x,tileList[i].y - 56), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladder =  Tile((tileList[i].x,tileList[i].y - 84), 28,28,'ladder.png')
        tileGroup.add(ladder)
        ladderList.append(ladder.rect)
        ladderType.append(1) 

#Spawn Barell Function
donkeykong = DK()
dkGroup = pygame.sprite.Group()
dkGroup.add(donkeykong)

barellSpawnedList = []
def spawnBarell():
    barellSpawned = Barell(5,5)
    barellSpawned.canMove = True
    testGroup.add(barellSpawned)
    barellSpawnedList.append(barellSpawned)
    
#MAIN_LOOP
if __name__ == '__main__':
    runGame = True
    while runGame:
        display.fill((0,0,0)) #Draw the background
        player.movement()
        for i in range(0, len(barellSpawnedList)):
            barellSpawnedList[i].barellMovement()
        player.playerCollision()
        donkeykong.spawnDKBarell(testGroup)
        if player.jump == True:
            player.playerJump(18)
        #Collect User Input (What key they pressed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP: #If player releases key, set back to idle position
                if event.key == pygame.K_d:
                    player.image = pygame.transform.flip(player.walkSprites[0], True, False)  #set to idle
                    player.movingLeft = False
                    player.movingRight = False
                elif event.key == pygame.K_a:
                    player.image = player.walkSprites[0]
                    player.movingLeft = False
                    player.movingRight = False
        tileGroup.draw(display)
        playerGroup.draw(display)
        testGroup.draw(display)
        dkGroup.draw(display)
        pygame.display.update() #Continuosuly draw on display (basically update frames)
        clock.tick(20)
    pygame.quit()
