import random
from hashlib import sha256
from typing import TypedDict, cast

class shapeData(TypedDict):
    min_radius: int
    max_radius: int
    chances: list[float]

def sha256_seed(seed: str) -> int:
    return int.from_bytes(sha256(seed.encode("utf-8")).digest(), "big")
def get_randomness(seed:str) -> random.Random:
    return random.Random(sha256_seed(seed))

SEED = "a5dD5e156AS"
MIN_RADIUS = 10
MAX_RADIUS = 100
CHANCES = [0.99 - 0.0099 * i for i in range(MAX_RADIUS - MIN_RADIUS)]

def shape_data_to_list(data: dict[str, int | list[float]]) -> shapeData:
    return {
        "min_radius": int(cast(int, data["min_radius"])),
        "max_radius": int(cast(int, data["max_radius"])),
        "chances": [float(chance) for chance in cast(list[float], data["chances"])],
    }


def tiles_to_map(tiles: list[tuple[int, int]], start_pos: tuple[int, int] = (0, 0), end_pos: tuple[int, int] = (63, 63)) -> dict[int, dict[int, bool]]:
    if end_pos[0] < start_pos[0]:
        temp = end_pos[0]
        end_pos = (start_pos[0], end_pos[1])
        start_pos = (temp, start_pos[1])
    if end_pos[1] < start_pos[1]:
        temp = end_pos[1]
        end_pos = (end_pos[0], start_pos[1])
        start_pos = (start_pos[0], temp)

    map = {x: {y: False for y in range(start_pos[0], end_pos[0] + 1)} for x in range(start_pos[1], end_pos[1] + 1)}

    for item in range(len(tiles)):
        tile = tiles[item]
        map[tile[0]][tile[1]] = True
    return map

def legacy_generate_shape(spawn: tuple[int, int], seed: str, shape_data: tuple[int, int, list[float]]) -> list[tuple[int, int]]:
    randomness = get_randomness(seed)
    tiles = [spawn]
    tiles_to_iterate = {0: True}
    INSERT_OFFSET = ((1, 0), (-1, 0), (0, 1), (0, -1))
    while True in set(tiles_to_iterate.values()):
        for index in range(len(tiles)):
            tile = tiles[index]
            if tiles_to_iterate[index]:
                distance = (abs(tile[0] - tiles[0][0]) ** 2 + abs(tile[1] - tiles[0][1]) ** 2) ** 1/2
                if shape_data[1] < distance:
                    tiles_to_iterate[index] = False
                    continue
                if distance > shape_data[0]:
                    if randomness.random() > shape_data[2][int(distance) - (shape_data[0] + 1)]:
                        tiles_to_iterate[index] = False
                        continue
                for x, y in INSERT_OFFSET:
                    new_tile = (tile[0] + x, tile[1] + y)
                    if new_tile not in set(tiles):
                        tiles.append(new_tile)
                        tiles_to_iterate[len(tiles_to_iterate)] = True
                tiles_to_iterate[index] = False
    return tiles

def generate_shape(spawn: tuple[int, int], seed: str, shape_data: tuple[int, int, list[float]]) -> list[tuple[int, int]]:
    randomness = get_randomness(seed)
    tiles = [spawn]
    iterate_map = tiles_to_map(tiles)
    tiles_to_iterate = {0: True}
    INSERT_OFFSET = ((1, 0), (-1, 0), (0, 1), (0, -1))
    while True in set(tiles_to_iterate.values()):
        for index in range(len(tiles)):
            tile = tiles[index]
            if tiles_to_iterate[index]:
                distance = (abs(tile[0] - tiles[0][0]) ** 2 + abs(tile[1] - tiles[0][1]) ** 2) ** 1/2
                if shape_data[1] < distance:
                    tiles_to_iterate[index] = False
                    iterate_map[tile[0]][tile[1]] = False
                    continue
                if distance > shape_data[0]:
                    if randomness.random() > shape_data[2][int(distance) - (shape_data[0] + 1)]:
                        tiles_to_iterate[index] = False
                        iterate_map[tile[0]][tile[1]] = False
                        for x in range(tile[0] - 1, tile[0] + 2):
                            for y in range(tile[1] - 1, tile[1] + 2):
                                if 0 <= tile[0] + x < 64 and 0 <= tile[1] + y < 64:
                                    iterate_map[tile[0] + x][tile[1] + y] = False
                                    if (tile[0] + x, tile[1] + y) in tiles_to_iterate.values():
                                        tiles_to_iterate[tuple(tiles_to_iterate.values()).index((tile[0] + x, tile[1] + y))] = False
                        continue
                for x, y in INSERT_OFFSET:
                    new_tile = (tile[0] + x, tile[1] + y)
                    if new_tile not in tiles:
                        tiles.append(new_tile)
                        iterate_map[new_tile[0]][new_tile[1]] = True
                        tiles_to_iterate[len(tiles_to_iterate)] = True
                tiles_to_iterate[index] = False
    return tiles

def fix_shape(tiles: list[tuple[int, int]], iteration_count: int = 1) -> list[tuple[int, int]]:
    new_tiles = tiles.copy()
    vals = set(new_tiles)

    CHECKS_OFFSET = ((-1, 1), (1, 1), (1, -1), (-1, -1))
    INSERT_OFFSET = ((1, 0), (-1, 0), (0, 1), (0, -1), (0, 0))
    for _ in range(iteration_count):
        new_vals = set(new_tiles)
        added = False
        for tile in new_vals:
            if all((tile[0] + x, tile[1] + y) in new_vals for x, y in CHECKS_OFFSET):
                for x, y in INSERT_OFFSET:
                    if (tile[0] + x, tile[1] + y) not in vals:
                        new_tiles.append((tile[0] + x, tile[1] + y))
                        vals.add((tile[0] + x, tile[1] + y))
                        added = True
        if not added:
            break
    return new_tiles