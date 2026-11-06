saveSize = 64
save = "testWorld"
import math, random

SAVEFile={}

def generateOre(type, size, richness, x, y, add=6.6):
    for xreal in range(x-100, x+101):
        for yreal in range(y-100, y+101):
            t = type
            xgenerate = xreal + random.randint(-5, +5)
            ygenerate = yreal + random.randint(-5, +5)
            ore = math.floor(richness*math.log10(add/(size*(xgenerate**2 + ygenerate**2)+1)))
            if ore <0:
                ore = 0
                t= None
            getRegio(xreal//64, yreal//64)[xreal%64][yreal%64] = {"Type":t, "Quantity":ore}

def getRegio(x, y):
    try:
        return SAVEFile[x][y]
    except:
        loadRegio(x, y)
        return SAVEFile[x][y]
def loadRegio(x, y):
    try:
        File = open(f"saves/{save}/ores/{x}_{y}.txt", "r")  
        if not(x in SAVEFile.keys()):
            SAVEFile[x] = {}
        if not(y in SAVEFile[x].keys()):
            SAVEFile[x][y] = {}
        iter = 0
        for Line in File:
            tiles = Line.split(";")
            SAVEFile[x][y][iter]
            for i in range(0, len(tiles)-1):
                data = tiles[i].split(" ")
                SAVEFile[x][y][iter][i] ={"Type":data[0], "Quantity":int(data[1])}
        File.close()


    except:
        if not(x in SAVEFile.keys()):
            SAVEFile[x] = {}
        if not(y in SAVEFile[x].keys()):
            SAVEFile[x][y] = {}
        for i in range(0, 64):
            SAVEFile[x][y][i] ={}
            for h in range(0, 64):
                SAVEFile[x][y][i][h] = {"Type":None, "Quantity":0}
#
def SAVE():
    for x in SAVEFile.keys():
        for y in SAVEFile[x].keys():
            File = open(f"saves\{save}\ores\{x}_{y}.txt", "w")
            for xx in SAVEFile[x][y].keys():
                for yy in SAVEFile[x][y][xx].keys():
                    File.write(str(SAVEFile[x][y][xx][yy]["Type"]) + " "+ str(SAVEFile[x][y][xx][yy]["Quantity"]) + ";")
                File.write("\n")
            File.close()
generateOre("Iron", 0.03, 33.6, 0, 0)
SAVE()