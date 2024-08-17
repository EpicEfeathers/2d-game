import pygame
import numpy as np
import random

from generate_corners import check_grass_tile, check_sand_tile, check_stone_tile

def generate_terrain():
    arr = np.loadtxt('map.txt', dtype=int)  
    return arr

def blit_terrain(screen, window_size, tile_size, x, y, terrain_map, grass_img, terrain_images_size, terrain_images):
    screen.fill((0,0,0))
    blit_list = []
    for height in range(int(window_size[1]/tile_size) + 1):
        for width in range(int(window_size[0]/tile_size) + 1):
            tile_type = terrain_map[int(height + y/tile_size), int(width + x/tile_size)]
            if tile_type == 4:
                tile = grass_img.subsurface((random.randint(0,3)*terrain_images_size, random.randint(0,3) * terrain_images_size, 64, 64))
                #tile = grass_img.subsurface(0*terrain_images_size, 0 * terrain_images_size, 64, 64)
                blit_list.append((tile, (width*tile_size - x%tile_size, height*tile_size - y%tile_size)))
            elif tile_type == 8:
                tile = check_grass_tile(terrain_map, int(height + y/tile_size), int(width + x/tile_size))
                blit_list.append((tile, (width*tile_size - x%tile_size, height*tile_size - y%tile_size)))
            elif tile_type == 9:
                tile = check_stone_tile(terrain_map, int(height + y/tile_size), int(width + x/tile_size))
                blit_list.append((tile, (width*tile_size - x%tile_size, height*tile_size - y%tile_size)))
            elif tile_type == 10:
                tile = check_sand_tile(terrain_map, int(height + y/tile_size), int(width + x/tile_size))
                blit_list.append((tile, (width*tile_size - x%tile_size, height*tile_size - y%tile_size)))
            else:
                blit_list.append((terrain_images[max(tile_type - 2, 0)], (width*tile_size - x%tile_size, height*tile_size - y%tile_size))) # - 2 for proper item from list, max to account for different blues in tile map
    
    screen.blits(blit_list)

    return screen