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
        color_world = np.zeros(world.shape, dtype=np.uint8)
        for i in range(world.shape[0]):
            for j in range(world.shape[1]):
                if world[i][j] < -0.5:
                    color_world[i][j] = 0 # Deep water
                elif world[i][j] < -0.27:
                    color_world[i][j] = 1 # Water
                elif world[i][j] < -0.2:
                    color_world[i][j] = 2 # Shallow water
                elif world[i][j] < -0.1:
                    color_world[i][j] = 3 # Sand
                elif world[i][j] < 0.2: 
                    color_world[i][j] = 4 if random.random() < 0.97 else 5 # Grass / Flowers
                elif world[i][j] < 0.35:  
                    color_world[i][j] = 6 # Stone
                else:  # Snowy peaks
                    color_world[i][j] = 7 # Snow

        return color_world
    
    color_world = add_color(world)

    return color_world

def add_edges_sand(world):
    def test_right(w, h):
        if world[w][h+1] <= 2: # backwards bc of how reading array
            world[w][h] = 10

    def test_left(w, h):
        if world[w][h-1] <= 2: # backwards bc of how reading array
            world[w][h] = 10

    def test_up(w, h):
        if world[w+1][h] <= 2: # backwards bc of how reading array
            world[w][h] = 10

    def test_down(w, h):
        if world[w-1][h] <= 2: # backwards bc of how reading array
            world[w][h] = 10

    for w in range(world.shape[0]):
        for h in range(world.shape[1]):
            if world[w][h] == 3:
                test_right(w, h)
                test_left(w, h)
                test_up(w, h)
                test_down(w, h)
    return world

def add_edges_grass(world):
    def test_right(w, h):
        if world[w][h+1] == 3: # backwards bc of how reading array
            world[w][h] = 8

    def test_left(w, h):
        if world[w][h-1] == 3: # backwards bc of how reading array
            world[w][h] = 8

    def test_up(w, h):
        if world[w+1][h] == 3: # backwards bc of how reading array
            world[w][h] = 8

    def test_down(w, h):
        if world[w-1][h] == 3: # backwards bc of how reading array
            world[w][h] = 8

    for w in range(world.shape[0]):
        for h in range(world.shape[1]):
            if world[w][h] == 4 or world[w][h] == 5:
                test_right(w, h)
                test_left(w, h)
                test_up(w, h)
                test_down(w, h)
    return world


def add_edges_stone(world):
    def test_right(w, h):
        if world[w][h+1] == 4 or world[w][h+1] == 5: # backwards bc of how reading array
            world[w][h] = 9

    def test_left(w, h):
        if world[w][h-1] == 4 or world[w][h-1] == 5: # backwards bc of how reading array
            world[w][h] = 9

    def test_up(w, h):
        if world[w+1][h] == 4 or world[w+1][h] == 5: # backwards bc of how reading array
            world[w][h] = 9

    def test_down(w, h):
        if world[w-1][h] == 4 or world[w-1][h] == 5: # backwards bc of how reading array
            world[w][h] = 9

    for w in range(world.shape[0]):
        for h in range(world.shape[1]):
            if world[w][h] == 6:
                test_right(w, h)
                test_left(w, h)
                test_up(w, h)
                test_down(w, h)
    return world

def testing(world):
    start = time.time()
    for w in range(world.shape[0]):
        for h in range(world.shape[1]):
            if world[w][h] == 8:
                world[w][h] == 8
    print(time.time() - start)
    return world

terrain_array = generate_world(1, 832, 832)

terrain_array = add_edges_sand(terrain_array)

terrain_array = add_edges_grass(terrain_array)

terrain_array = add_edges_stone(terrain_array)

terrain_array = testing(terrain_array)

array_2d = terrain_array.reshape(-1, terrain_array.shape[-1])

np.savetxt('map.txt', array_2d, fmt='%d')

print("Successfully generated!")