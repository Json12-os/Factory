import shape_generator
import json
import math
import random
from string import ascii_letters
LETTERS = ascii_letters + "0123456789"

WORLD_NAME = "testWorld"
biome_data = None
with open(f"biome_settings/plains.json", "r") as file:
    biome_data = json.load(file)

with open(f"saves/{WORLD_NAME}/world/0_0.txt", "w") as file:
    chances = []
    if biome_data["chances_type"] == "arctan":
        for x in range(biome_data["max_radius"] - biome_data["min_radius"]):
            chances.append(math.atan(x ** 2 / 100) * 2 / math.pi)
    elif biome_data["chances_type"] == "linear":
        for x in range(biome_data["max_radius"] - biome_data["min_radius"]):
            chances.append(x / 100)
    chances = chances[::-1]
    seed = "".join([random.choice(LETTERS) for _ in range(10)])
    print(seed)
    spawn_point = (31, 31)
    tiles = shape_generator.fix_shape(shape_generator.generate_shape(spawn_point, seed+str(spawn_point[0])+str(spawn_point[1]), (biome_data["min_radius"], biome_data["max_radius"], chances)))
    for x in range(64):
        for y in range(64):
            if (x, y) in tiles:
                #file.write(biome_data["map_id"])
                file.write("150")
            file.write(";")
        if x != 511:
            file.write("\n")