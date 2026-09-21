import random

SEED = "a5dD5e156AS"

MIN_RADIUS = 5
MAX_RADIUS = 20
CHANCES = [0.99 - 0.01 * i for i in range(MAX_RADIUS)]

def generate_biome(biome: str, spawn: list[int]) -> dict[int, list[int]]:
    tiles = {0: spawn}
    tiles_to_iterate = {0: True}
    while True in set(tiles_to_iterate.values()):
        for index in range(len(tiles)):
            tile = tiles[index]
            if tiles_to_iterate[index]:
                distance = (abs(tile[0] - tiles[0][0]) ** 2 + abs(tile[1] - tiles[0][1]) ** 2) ** 1/2
                if MAX_RADIUS < distance:
                    tiles_to_iterate[index] = False
                    continue
                if distance > MIN_RADIUS:
                    if random.random() > CHANCES[int(distance) - 6]:
                        tiles_to_iterate[index] = False
                        continue
                
                if [tile[0] + 1, tile[1]] not in tiles.values():
                    tiles[len(tiles)] = [tile[0] + 1, tile[1]]
                    tiles_to_iterate[len(tiles_to_iterate)] = True
                if [tile[0] - 1, tile[1]] not in tiles.values():
                    tiles[len(tiles)] = [tile[0] - 1, tile[1]]
                    tiles_to_iterate[len(tiles_to_iterate)] = True
                if [tile[0], tile[1] + 1] not in tiles.values():
                    tiles[len(tiles)] = [tile[0], tile[1] + 1]
                    tiles_to_iterate[len(tiles_to_iterate)] = True
                if [tile[0], tile[1] - 1] not in tiles.values():
                    tiles[len(tiles)] = [tile[0], tile[1] - 1]
                    tiles_to_iterate[len(tiles_to_iterate)] = True
                tiles_to_iterate[index] = False
    return tiles

with open("saves/testWorld/humidity/0_0.txt", "w") as file:
    tiles = generate_biome("null", [31, 31])
    for x in range(64):
        for y in range(64):
            if [x, y] in tiles.values():
                file.write("0")
            file.write(";")
        if x != 63:
            file.write("\n")
