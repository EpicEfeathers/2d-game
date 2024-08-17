import noise
import numpy as np
import math
from PIL import Image

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

    return world

dark_blue = [65,90,225]
blue = [65, 105, 225]
light_blue = [65, 130, 225]
beach = [238, 214, 175]
green = [34, 139, 34]
mountain = [139, 137, 137]
snow = [255, 250, 250]

def add_color(world):
    color_world = np.zeros(world.shape + (3,), dtype=np.uint8)
    for i in range(world.shape[0]):
        for j in range(world.shape[1]):
            if world[i][j] < -0.5:
                color_world[i][j] = dark_blue
            elif world[i][j] < -0.27:
                color_world[i][j] = blue
            elif world[i][j] < -0.2:
                color_world[i][j] = light_blue
            elif world[i][j] < -0.1:
                color_world[i][j] = beach
            elif world[i][j] < 0.2:  # Mountain range
                color_world[i][j] = green
            elif world[i][j] < 0.35:  # Mountainous area
                color_world[i][j] = mountain
            else:  # Snowy peaks
                color_world[i][j] = snow

    return color_world


world = generate_world(1, 832, 832)
color_world = add_color(world)

image = Image.fromarray(color_world)

# Optionally, display the image
image.show()