import tkinter, math
root = tkinter.Tk()
Cwidth = 1024
Cheight = 800
regioSize = 64
tileSize = 40
from spolocneVariables import playerX, playerY, saveName
root.geometry(f"{Cwidth}x{Cheight}")
canvas = tkinter.Canvas(root, width=Cwidth, height=Cheight)
canvas.pack()

pointers = {}
def getTileDataHumidity(Yirl, Xirl):
    file = open(f"saves/{saveName}/humidity/{math.floor(Xirl/regioSize)}_{math.floor(Yirl/regioSize)}.txt", "r")
    lines = file.readlines()
    line = lines[Yirl%regioSize].strip("\n")
    lineL = line.split(";")
    val = lineL[Xirl%regioSize]
    return int(val)
    ...
tiles = []
pointers = {}
def chngeTileSize():
    global tiles, pointers
    index = 0
    for j in range(0, math.floor(Cheight/tileSize)+2):
        tiles.append([])
        for i in range(0, math.floor(Cwidth/tileSize)+2):
            tiles[j].append([])
            pointers[index] = (i, j)
            tiles[j][i] = [
            canvas.create_rectangle((0 + (i)*tileSize - playerY%tileSize,0 + j*tileSize- playerX%tileSize), (tileSize+i*tileSize- playerY%tileSize, tileSize+j*tileSize- playerX%tileSize), tags=["index", "del"])          
            ,canvas.create_text((0 + (i)*tileSize + tileSize//2- playerY%tileSize,0 + j*tileSize+tileSize//2- playerX%tileSize),  tags=["index", "del"], text=f"{index}")
            ,index]
            index += 1
    pass

def render():
    for j in range(0, math.floor(Cheight/tileSize)+2):
        for i in range(0, math.floor(Cwidth/tileSize)+2):
            canvas.coords(tiles[j][i][0], 0 + (i)*tileSize - playerY%tileSize,0 + j*tileSize- playerX%tileSize, tileSize+i*tileSize- playerY%tileSize, tileSize+j*tileSize- playerX%tileSize)
            #canvas.coords(tiles[j][i][1], (0 + (i)*tileSize + tileSize//2- playerY%tileSize,0 + j*tileSize+tileSize//2- playerX%tileSize))
            try:
                humidity = getTileDataHumidity(j+math.floor(playerX/tileSize)
                                               ,
                                                i+math.floor(playerY/tileSize)
                                                )
            except:
                humidity = 17

            c = "#"+ str(hex(255-humidity).replace("0x", "")) + str(hex(255-humidity).replace("0x", "")) + str(hex(humidity).replace("0x", ""))
            canvas.itemconfig(tiles[j][i][0], fill=c)
            

def forv():
    global playerX
    playerX -=1
def back():
    global playerX
    playerX +=1
def rig():
    global playerY
    playerY -=1
def lef():
    global playerY
    playerY +=1

import keyboard
keyboard.add_hotkey("a", rig)
keyboard.add_hotkey("d", lef)
keyboard.add_hotkey("w", forv)
keyboard.add_hotkey("s", back)



chngeTileSize()
import time
def rendering():
    render()
    root.update()