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

gridsize=256
LoadLevel=playerPosY=playerPosX=x3=y3=x0=y0=0
LoadFrame=1
ImagesNum=4
left=1
objectType=0
playerPosX=0
mouseposx=mouseposy=100
moveLeft=moveRight=moveUp=moveDown=clicked=resized=False
blockType=3
levelBlock = 0

L2 = Label(buttonwin, text="Level Size:TopSize")
L2.pack( side = TOP)
E2 = Entry(buttonwin, bd =5)
E2.pack(side = TOP)
L3 = Label(buttonwin, text="BottomSize")
L3.pack( side = TOP)
E3 = Entry(buttonwin, bd =5)
E3.pack(side = TOP)
L4 = Label(buttonwin, text="LeftSize")
L4.pack( side = TOP)
E4 = Entry(buttonwin, bd =5)
E4.pack(side = TOP)
L5 = Label(buttonwin, text="RightSize")
L5.pack( side = TOP)
E5 = Entry(buttonwin, bd =5)
E5.pack(side = TOP)

def resize():
    global resized
    resized=True
    ground_list.update()
    resized=False
    drawBlockWorld(ground_list, ground, 0, 1, int(E4.get()), int(E2.get()), int(E5.get()), int(E3.get()))

button5 = Button(buttonwin,text = 'Resize',  command=resize)
button5.pack(side=TOP)

L1 = Label(buttonwin, text="FileName")
L1.pack( side = TOP)
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

def loadBox():
    global clicked, blockType, levelblock
    level = open(str(E1.get()),"r+")
    level.read(0)
    clicked = True
    for line in level:
        if line.startswith("1"):
            numbers = [word.split(' ') for word in line.splitlines()]
            levelx = numbers[0][2]
            levely = numbers[0][1]
            levelblock = numbers[0][3]
            blockType = int(levelblock)
            mouse_list.add(loadBlocks(int(levelx), int(levely)))
            ground_list.update()
            mouse_list.update()
    clicked = False
    level.close()

saveButton = Button(buttonwin,text = 'save',  command=saveBox)
saveButton.pack(side=LEFT)
loadButton = Button(buttonwin,text = 'load',  command=loadBox)
loadButton.pack(side=LEFT)

print("Loading Images")

gridImage = pygame.transform.scale(pygame.image.load('grid.png'), (gridsize, gridsize))

for i in range(ImagesNum + 1):
    Images.append(pygame.transform.scale(pygame.image.load('block_' + str(LoadLevel) + '.png'), (32, 32)))
    LoadLevel += 1
ground_list = pygame.sprite.Group()
mouse_list = pygame.sprite.Group()
grid_list = pygame.sprite.Group()

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
        self.rect.x = mouseposx - 4
        self.rect.y = mouseposy - 4
        if pygame.sprite.spritecollideany(self, mouse_list):
            self.image = pygame.transform.scale(Images[int(blockType)], (8, 8))

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

class loadBlocks(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Images[2]
        self.rect = self.image.get_rect()
        self.rect.x = x * 32 - playerPosX
        self.rect.y = y * 32 - playerPosY
    def update(self):
        self.remove(mouse_list)

class grid(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = gridImage
        self.rect = self.image.get_rect()
        self.rect.x = x * gridsize - playerPosX
        self.rect.y = y * gridsize - playerPosY
        self.groundPosX = x * gridsize
        self.groundPosY = y * gridsize
    def update(self):
        global playerPosX, playerPosY
        self.rect.x = self.groundPosX - playerPosX
        self.rect.y = self.groundPosY - playerPosY
        if self.rect.x > self.groundPosX + gridsize:
            self.rect.x -= gridsize
        if self.rect.x < self.groundPosX - gridsize:
            self.rect.x += gridsize
        if self.rect.y > self.groundPosY + gridsize:
            self.rect.y -= gridsize
        if self.rect.y < self.groundPosY - gridsize:
            self.rect.y += gridsize        

class ground(pygame.sprite.Sprite):
    def __init__(self, x, y, blockImage):
        pygame.sprite.Sprite.__init__(self)
        self.image = Images[blockImage]
        self.rect = self.image.get_rect()
        self.rect.x = x * 32 - playerPosX
        self.rect.y = y * 32 - playerPosY
        self.groundPosX = x * 32
        self.groundPosY = y * 32
        self.type = 0
    def update(self):
        global playerPosX, playerPosY, blockType, clicked
        if pygame.sprite.spritecollideany(self, mouse_list) and clicked == True:
            self.image = Images[blockType]
            self.type = blockType
        self.rect.x = self.groundPosX - playerPosX
        self.rect.y = self.groundPosY - playerPosY
        if resized == True:
            self.remove(ground_list)
    def save(self):
        global file1, resized, blockType, objectType
        if self.groundPosX > 0:
            self.xloc = int(self.groundPosX / 32)
        else:
            self.xloc = self.groundPosX
        if self.groundPosY > 0:
            self.yloc = int(self.groundPosY / 32)
        else:
            self.yloc = self.groundPosY
        if int(self.type) > 0:
            objectType = 1
            file1.write(str(objectType) + " " + str(self.yloc) +" " + str(self.xloc) + " " + str(self.type) + "\n")        

pygame.display.set_caption('Super Mario 8-Bit Odyssey Editor')
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode(WINDOWSIZE)
windowSurface.fill(BACKGROUNDCOLOUR)
mouse_list.add(mouse())

def mainLoop():
    global moveLeft, moveRight, moveDown, moveUp, playerPosY, playerPosX, mouseposx, mouseposy, blockType, clicked
    ground_list.update()
    grid_list.update()
    windowSurface.fill(BACKGROUNDCOLOUR)
    ground_list.draw(windowSurface)
    grid_list.draw(windowSurface)
    mouse_list.draw(windowSurface)
    pygame.display.update()
    root.update()
    clicked = False
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
            mouseposx = event.pos[0]
            mouseposy = event.pos[1]
            mouse_list.update()
                
    if pygame.mouse.get_pressed()[0]:
        ground_list.update()
        clicked = True
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
    global blockType, objectType
    blockType = int(E6.get())
    if blockType < 1:
        blockType = 1
    if blockType > ImagesNum + 1:
        blockType = ImagesNum + 1
    objectType=1
    print(objectType)

def erase():
    global blockType
    blockType = 0
    objectType=0

drawBlockWorld(ground_list, ground, 0, 1, 0, 0, 15, 15)
drawBlock(grid_list, grid, 1, -32, -32, 32, 32)

button2 = Button(buttonwin,text = 'Erase',  command=erase)
button2.pack(side=LEFT)
button1 = Button(buttonwin,text = 'Block',  command=draw)
button1.pack(side=LEFT)
button5 = Button(buttonwin,text = 'Background',  command=draw)
button5.pack(side=LEFT)
button6 = Button(buttonwin,text = 'Enemy',  command=draw)
button6.pack(side=LEFT)
button7 = Button(buttonwin,text = 'Item',  command=draw)
button7.pack(side=LEFT)

L6 = Label(buttonwin, text="BlockImage")
L6.pack( side = BOTTOM)
E6 = Entry(buttonwin, bd =5)
E6.pack(side = BOTTOM)
    
while True:
    mainLoop()
