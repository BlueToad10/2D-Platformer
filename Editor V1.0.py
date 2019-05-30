import pygame, sys, time
import tkinter as tk
from tkinter import *
from pygame.locals import *
import os

WINDOWSIZE = (720, 520)
BACKGROUNDCOLOUR = (0, 0, 0)
TEXTCOLOUR = (255, 255, 255)
FPS=60
Images=[]

root = tk.Tk()
embed = tk.Frame(root, width = 500, height = 500) #creates embed frame for pygame window
embed.grid(columnspan = (600), rowspan = 500) # Adds grid
embed.pack(side = LEFT) #packs window to the left
buttonwin = tk.Frame(root, width = 75, height = 500)
buttonwin.pack(side = LEFT)
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'

LoadLevel=playerPosY=playerPosX=x3=y3=x0=y0=0
LoadFrame=1
ImagesNum=3
left=1
playerPosX=-4
mouseposx=mouseposy=100
moveLeft=moveRight=moveUp=moveDown=clicked=False

blockType=3


L1 = Label(buttonwin, text="FileName")
L1.pack( side = LEFT)
E1 = Entry(buttonwin, bd =5)
E1.pack(side = TOP)

def saveBox():
    global file1
    if E1.get().endswith(".lvl"):
        if os.path.exists(str(E1.get())):
            os.remove(str(E1.get()))
        file1 = open(str(E1.get()),"a")
        file1 = open(str(E1.get()),"r+")
        for object in ground_list:
            object.save()
        file1.read(0)
        for line in file1:
            print(line, end='')
        file1.close()

saveButton = Button(buttonwin,text = 'save',  command=saveBox)
saveButton.pack(side=LEFT)

#loadButton = Button(buttonwin,text = 'save',  command=loadBox)
#loadButton.pack(side=LEFT)






print("Loading Images")

for i in range(ImagesNum + 1):
    Images.append(pygame.transform.scale(pygame.image.load('block_' + str(LoadLevel) + '.png'), (32, 32)))
    LoadLevel += 1
ground_list = pygame.sprite.Group()
mouse_list = pygame.sprite.Group()

def drawBlockWorld(group, block, world, size, x, y, x2, y2):
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
            group.add(block(x, y, world))
            x += size
        x = x0
        y += size
        if y >= y2:
            break

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

class mouse(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Images[1], (16, 16))
        self.rect = self.image.get_rect()
        self.rect.x = 340
        self.rect.y = 280
    def update(self):
        global mouseposx, mouseposy, blockType
        self.rect.x = mouseposx
        self.rect.y = mouseposy
        
        if pygame.sprite.spritecollideany(self, mouse_list):
            self.image = pygame.transform.scale(Images[blockType], (16, 16))

class player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Images[0]
        self.rect = self.image.get_rect()
        self.rect.x = 340
        self.rect.y = 280
        self.groundPosX = x
        self.groundPosY = y
    def update(self):
        global playerPosX, playerPosY
        self.rect.x = self.groundPosX - playerPosX
        self.rect.y = self.groundPosY - playerPosY

class ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x - playerPosX
        self.rect.y = y - playerPosY
        self.groundPosX = x
        self.groundPosY = y
        self.type = 0
    def update(self):
        global playerPosX, playerPosY, blockType
        if pygame.sprite.spritecollideany(self, mouse_list):
            self.image = Images[blockType]
            self.type = blockType
        self.rect.x = self.groundPosX - playerPosX
        self.rect.y = self.groundPosY - playerPosY
    def save(self):
        global file1
        if self.groundPosX > 0:
            self.xloc = int(self.groundPosX / 32)
        else:
            self.xloc = self.groundPosX
        if self.groundPosY > 0:
            self.yloc = int(self.groundPosY / 32)
        else:
            self.yloc = self.groundPosY
        if self.type > 0:
            self.type = 1
            file1.write(str(self.type) + " " + str(self.xloc) +" " + str(self.yloc) + "\n")
        
      #  if self.groundPosX > levelSizeRight or self.groundPosX < levelSizeLeft or self.groundPosY > levelSizeBottom or self.groundPosY < levelSizeTop:
          # self.remove(ground_list)
        

pygame.display.set_caption('Super Mario 8-Bit Odyssey Editor')
mainClock = pygame.time.Clock()
#windowSurface = pygame.display.set_mode(WINDOWSIZE, pygame.FULLSCREEN)
windowSurface = pygame.display.set_mode(WINDOWSIZE)
pygame.mouse.set_visible(False)
windowSurface.fill(BACKGROUNDCOLOUR)
mouse_list.add(mouse())

def mainLoop():
    global moveLeft, moveRight, moveDown, moveUp, playerPosY, playerPosX, mouseposx, mouseposy, blockType
    
    windowSurface.fill(BACKGROUNDCOLOUR)
    ground_list.draw(windowSurface)
    mouse_list.draw(windowSurface)
    pygame.mouse.set_visible(False)
    pygame.display.update()
    root.update()
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_LEFT:
                moveLeft = True
            if event.key == K_RIGHT:
                moveRight = True
            if event.key == K_DOWN:
                moveDown=True
            if event.key == K_UP:
                moveUp=True
        if event.type == KEYUP:
            if event.key == K_LEFT:
                moveLeft = False
            if event.key == K_RIGHT:
                moveRight = False
            if event.key == K_DOWN:
                moveDown=False
            if event.key == K_UP:
                moveUp=False
        if event.type == MOUSEMOTION:
            pygame.mouse.set_visible(False)
            mouseposx = event.pos[0]
            mouseposy = event.pos[1]
            mouse_list.update()
                
    if pygame.mouse.get_pressed()[0]:
        pygame.mouse.set_visible(False)
        ground_list.update()
    if moveLeft == True:
        playerPosX -= 8
    if moveUp == True:
        playerPosY -= 8
    if moveRight == True:
        playerPosX += 8
    if moveDown == True:
        playerPosY += 8
    mainClock.tick(FPS)

def draw():
    global blockType
    blockType = 3

def erase():
    global blockType
    blockType = 0

drawBlock(ground_list, ground, 32, 0, 0, 500, 470)

button2 = Button(buttonwin,text = 'Erase',  command=erase)
button2.pack(side=LEFT)
root.update()

button1 = Button(buttonwin,text = 'Draw',  command=draw)
button1.pack(side=LEFT)
root.update()
    
while True:
    mainLoop()
