import tkinter, math
root = tkinter.Tk()
Cwidth = 1024
Cheight = 800
regioSize = 64
saveName = "testWorld"
tileSize = 40
playerX = 25
playerY = 0
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



def render():
    canvas.delete("del")
    index = 0
    pointers = {}
    for j in range(-1, math.floor(Cheight/tileSize)+1):
        for i in range(-1, math.floor(Cwidth/tileSize)+1):
            pointers[index] = (i, j)
            try:
                humidity = getTileDataHumidity(j+math.floor(playerX/tileSize)
                                               ,
                                                i+math.floor(playerY/tileSize)
                                                )
            except:
                humidity = 17
            c = "#"+ str(hex(255-humidity).replace("0x", "")) + str(hex(255-humidity).replace("0x", "")) + str(hex(humidity).replace("0x", ""))
            canvas.create_rectangle((0 + (i)*tileSize + playerX%tileSize,0 + j*tileSize+ playerY%tileSize), (tileSize+i*tileSize+ playerX%tileSize, tileSize+j*tileSize+ playerY%tileSize), tags=["index", "del"], 
                                    fill= c,
                                    outline=c
                                    )
            
            #canvas.create_text((0 + (i)*tileSize + tileSize//2+ playerX%tileSize,0 + j*tileSize+tileSize//2+ playerY%tileSize),  tags=["index", "del"], text=f"{index}")
            index += 1
    
    ...
    
import keyboard
def forv():
    global playerX
    playerX +=1
def back():
    global playerX
    playerX -=1
keyboard.add_hotkey("w", forv)
keyboard.add_hotkey("s", back)
def rig():
    global playerY
    playerY +=1
def lef():
    global playerY
    playerY -=1
keyboard.add_hotkey("a", rig)
keyboard.add_hotkey("d", lef)


while True:
    render()
    
    root.update()