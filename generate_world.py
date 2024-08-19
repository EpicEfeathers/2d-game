import noise
import numpy as np
import math
import random

import time

def generate_world(seed: int, width: int, height: int):
    shape = (width, height)
    middle = (shape[0] / 2, shape[1] / 2)
    scale = 100.0
    octaves = 6
    persistence = 0.5
    lacunarity = 2.0
    print(f"Seed: {seed}")

    world = np.zeros(shape)
    for h in range(shape[0]):
        for w in range(shape[1]):
            world[h][w] = noise.pnoise2(h / scale,
                                        w / scale,
                                        octaves=octaves,
                                        persistence=persistence,
                                        lacunarity=lacunarity,
                                        repeatx=shape[0],
                                        repeaty=shape[1],
                                        base=seed)
            
            # Distance formula from center
            distance = math.sqrt((w - middle[0])**2 + (h - middle[1])**2)

            # Normalize distance
            distance = distance / middle[0]

            # Exponential distance
            distance = distance ** 3

            world[h][w] = world[h][w] - min(distance, 1)

    dark_blue = [65, 90, 225]
    blue = [65, 105, 225]
    light_blue = [65, 130, 225]
    green = [34, 139, 34]
    beach = [238, 214, 175]
    snow = [255, 250, 250]
    mountain = [139, 137, 137]

    def add_color(world):
        color_world = np.zeros(world.shape, dtype = object)
        for i in range(world.shape[0]):
            for j in range(world.shape[1]):
                if world[i][j] < -0.5:
                    color_world[i][j] = "w0" # Deep water
                elif world[i][j] < -0.27:
                    color_world[i][j] = "w1" # Water
                elif world[i][j] < -0.2:
                    color_world[i][j] = "w2" # Shallow water
                elif world[i][j] < -0.1:
                    color_world[i][j] = "sa" # Sand
                elif world[i][j] < 0.2: 
                    color_world[i][j] = "g" + str(random.randint(0, 15))
                elif world[i][j] < 0.35:  
                    color_world[i][j] = "st" # Stone
                else:  # Snowy peaks
                    color_world[i][j] = "sn" # Snow

        return color_world
    
    color_world = add_color(world)

    return color_world

def add_edges_sand(world):
    def test(w, h):
        neighbors = [world[w][h+1], world[w][h-1], world[w+1][h], world[w-1][h]]
        if "w2" in neighbors:
            world[w][h] = "saE"


    for w in range(world.shape[0]):
        for h in range(world.shape[1]):
            if world[w][h] == "sa":
                test(w, h)
    return world

def add_edges_grass(world):
    def test(w, h):
        neighbors = [world[w][h+1], world[w][h-1], world[w+1][h], world[w-1][h]]
        if "sa" in neighbors:
            world[w][h] = "gE"

    for w in range(world.shape[0]):
        for h in range(world.shape[1]):
            try:
                if int(world[w][h][1:]) >= 0 and int(world[w][h][1:]) <= 15:
                    test(w, h)
            except:
                pass
    return world


def add_edges_stone(world):
    def test(w, h):
        neighbors = [world[w][h+1], world[w][h-1], world[w+1][h], world[w-1][h]]
        for n in neighbors:
            try:
                if 0 <= int(n[1:]) <= 15:
                    world[w][h] = "stE"
            except:
                pass


    for w in range(world.shape[0]):
        for h in range(world.shape[1]):
            if world[w][h] == "st":
                test(w, h)
    return world


terrain_array = generate_world(1, 832, 832)

terrain_array = add_edges_sand(terrain_array)

terrain_array = add_edges_grass(terrain_array)

terrain_array = add_edges_stone(terrain_array)

array_2d = terrain_array.reshape(-1, terrain_array.shape[-1])

np.savetxt('map.txt', array_2d, fmt="%s")

print("Successfully generated!")