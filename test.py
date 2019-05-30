import pygame, sys
from pygame.locals import *
wsize=(720, 480)
BACKGROUNDCOLOUR = (0, 0, 0)
Images=[]
LoadLevel=jump=y3=x3=0
playerPosX=-4
playerPosY=64
moveLeft=moveRight=moveJump=False
FPS = 60
levelx=levely=0
playerMoveX=playerMoveY=0
ImagesNum=4
levelBlock=0

player_list=pygame.sprite.Group()
ground_list=pygame.sprite.Group()
for i in range(ImagesNum + 1):
    Images.append(pygame.transform.scale(pygame.image.load('block_' + str(LoadLevel) + '.png'), (32, 32)))
    LoadLevel += 1

def drawBlock(group, block, size, x, y, x2, y2):
    global x3, y3
    x0 = x
    y0 = y
    if x > x2:
        x3 = x - x2
    elif x < x2:
       x3 = x2 - x
    if y > y2:
        y3 = y - y2
    elif y < y2:
        y3 = y2 - y
    x3 = int(x3 / size)
    y3 = int(y3 / size)
    while True:
        for i in range(x3):
            group.add(block(x, y))
            x += size
        x = x0
        y += size
        if y >= y2:
            break

def loadLevel(fileName):
    global levelBlock
    level = open(fileName,"r+")
    level.read(0)
    for line in level:
        if line.startswith("1"):
            numbers = [word.split(' ') for word in line.splitlines()]
            levelx = numbers[0][2]
            levely = numbers[0][1]
            levelBlock = numbers[0][3]
            ground_list.add(ground(int(levelx), int(levely), int(levelBlock)))
    level.close()

class player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Images[1]
        self.rect = self.image.get_rect()
        self.rect.x = 340
        self.rect.y = 280

class collideleft(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Images[2], (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = 332
        self.rect.y = 280

class collideright(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Images[2], (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = 347
        self.rect.y = 280

class collidetop(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Images[2], (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = 340
        self.rect.y = 273

class collidebottom(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Images[2], (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = 340
        self.rect.y = 287

class ground(pygame.sprite.Sprite):
    def __init__(self, x, y, levelBlock):
        pygame.sprite.Sprite.__init__(self)
        self.image = Images[levelBlock]
        self.rect = self.image.get_rect()
        self.rect.x = x * 32 - playerPosX
        self.rect.y = y * 32 - playerPosY
        self.groundPosX = x * 32
        self.groundPosY = y * 32
    def update(self):
        global playerPosX, playerPosY
        self.rect.x = self.groundPosX - playerPosX
        self.rect.y = self.groundPosY - playerPosY

pygame.init()
windowSurface = pygame.display.set_mode(wsize)
pygame.mouse.set_visible(False)
mainClock = pygame.time.Clock()
player_list.add(collideleft())
player_list.add(collideright())
player_list.add(collidetop())
player_list.add(collidebottom())
player_list.add(player())
def mainLoop():
    global playerPosX, playerPosY, jump, moveLeft, moveRight, moveJump
    windowSurface.fill(BACKGROUNDCOLOUR)
    ground_list.update()
    ground_list.draw(windowSurface)
    player_list.draw(windowSurface)
    pygame.display.update()
    if moveLeft == True and moveRight == False and not pygame.sprite.spritecollideany(collideleft(), ground_list):
        playerPosX -= 8
    if moveRight == True and moveLeft == False and not pygame.sprite.spritecollideany(collideright(), ground_list):
        playerPosX += 8
    if moveJump == True:
        playerPosY -= 8
        jump += 1
    if jump >= 40 or moveJump == False or pygame.sprite.spritecollideany(collidetop(), ground_list):
        jump = 0
        moveJump = False
    if not pygame.sprite.spritecollideany(collidebottom(), ground_list) and moveJump == False:
        playerPosY += 8
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT and not pygame.sprite.spritecollideany(collideleft(), ground_list):
                moveLeft = True
            if event.key == K_RIGHT and not pygame.sprite.spritecollideany(collideright(), ground_list):
                moveRight = True
            if event.key == ord('x') and pygame.sprite.spritecollideany(collidebottom(), ground_list):
                moveJump = True
        if event.type == KEYUP:
            if event.key == K_LEFT:
                moveLeft = False
            if event.key == K_RIGHT:
                moveRight = False
            if event.key == ord('x'):
                moveJump = False
    mainClock.tick(FPS)
   # if pygame.sprite.spritecollideany(collideleft(), ground_list) and pygame.sprite.spritecollideany(collidetop(), ground_list):
      #  playerPosX += 8
       # playerPosY += 8
  #  elif pygame.sprite.spritecollideany(collideright(), ground_list) and pygame.sprite.spritecollideany(collidetop(), ground_list):
     #   playerPosX -= 8
     #   playerPosY += 8
     
loadLevel("level1.lvl")
while True:
    mainLoop()
