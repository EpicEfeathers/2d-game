import pygame
import time

screen = pygame.Surface((16, 16), pygame.SRCALPHA)
grass = pygame.image.load("textures/tiles/grass_corners.png")
grass_img = pygame.image.load("textures/tiles/grass.png")
sand = pygame.image.load("textures/tiles/sand_corners.png")
sand_img = pygame.image.load("textures/tiles/sand.png")
water = pygame.image.load("textures/tiles/water.png")
stone = pygame.image.load("textures/tiles/stone_corners.png")

def check_sand_tile(tile_map, x, y):
    screen = pygame.Surface((16, 16), pygame.SRCALPHA)
    screen.blit(water, (0,0))
    #check top left
    if tile_map[x-1][y][0] == "w": # above is sand?
        if tile_map[x][y-1][0] == "w": # left is sand?
            screen.blit(sand, (0, 0), (0, 0, 10, 10)) # top left corner
        else:
            screen.blit(sand, (0, 0), (8, 0, 8, 8)) # straight edge top

        if tile_map[x][y+1][0] == "w": # right is sand?
            screen.blit(sand, (6,0), (14, 0, 10, 10))
        else:
            screen.blit(sand, (8,0), (8, 0, 8, 8))

    else: # above not sand
        if tile_map[x][y-1][0] == "w": # left is sand
            screen.blit(sand, (0,0), (0, 8, 8, 8))
        else:
            screen.blit(sand, (0,0), (7, 7, 10, 10))

        if tile_map[x][y+1][0] == "w": # right is sand
            screen.blit(sand, (8,0), (16, 8, 8, 8))
        else:
            screen.blit(sand, (6,0), (7, 7, 10, 10))

        
    #check bottom right
    if tile_map[x+1][y][0] == "w": # below is sand?
        if tile_map[x][y+1][0] == "w": # right is sand?
            screen.blit(sand, (6, 6), (14, 14, 10, 10)) # bottom right corner
        else:
            screen.blit(sand, (6, 6), (7, 14, 10, 10)) # straight edge bottom
        if tile_map[x][y-1][0] == "w": # left is sand?
            screen.blit(sand, (0,6), (0, 14, 10, 10)) # bottom right corner
        else:
            screen.blit(sand, (0,8), (8, 16, 8, 8)) # straight edge bottom

    else: # below is stone
        if tile_map[x][y-1][0] == "w": # left is sand
            screen.blit(sand, (0,8), (0, 8, 8, 8)) #
        else:
            screen.blit(sand, (0,8), (7, 7, 10, 10)) 

        if tile_map[x][y+1][0] == "w": # right is sand
            screen.blit(sand, (8,8), (16, 8, 8, 8))
        else:
            screen.blit(sand, (6,6), (7, 7, 10, 10))


    return pygame.transform.scale(screen, (64, 64))

def check_grass_tile(tile_map, x, y):
    screen = pygame.Surface((16, 16), pygame.SRCALPHA)
    screen.blit(sand_img, (0,0))
    #check top left
    if tile_map[x-1][y] == "sa": # above is sand?
        if tile_map[x][y-1] == "sa": # left is sand?
            screen.blit(grass, (0, 0), (0, 0, 10, 10)) # top left corner
        else:
            screen.blit(grass, (0, 0), (8, 0, 8, 8)) # straight edge top

        if tile_map[x][y+1] == "sa": # right is sand?
            screen.blit(grass, (6,0), (14, 0, 10, 10))
        else:
            screen.blit(grass, (8,0), (8, 0, 8, 8))

    else: # above not sand
        if tile_map[x][y-1] == "sa": # left is sand
            screen.blit(grass, (0,0), (0, 8, 8, 8))
        else:
            screen.blit(grass, (0,0), (7, 7, 10, 10))

        if tile_map[x][y+1] == "sa": # right is sand
            screen.blit(grass, (8,0), (16, 8, 8, 8))
        else:
            screen.blit(grass, (6,0), (7, 7, 10, 10))

    
    #check bottom right
    if tile_map[x+1][y] == "sa": # below is sand?
        if tile_map[x][y+1] == "sa": # right is sand?
            screen.blit(grass, (6, 6), (14, 14, 10, 10)) # bottom right corner
        else:
            screen.blit(grass, (6, 6), (7, 14, 10, 10)) # straight edge bottom
        if tile_map[x][y-1] == "sa": # left is sand?
            screen.blit(grass, (0,6), (0, 14, 10, 10)) # bottom right corner
        else:
            screen.blit(grass, (0,8), (8, 16, 8, 8)) # straight edge bottom

    else: # below is grass
        if tile_map[x][y-1] == "sa": # left is sand
            screen.blit(grass, (0,8), (0, 8, 8, 8)) #
        else:
            screen.blit(grass, (0,8), (7, 7, 10, 10)) 

        if tile_map[x][y+1] == "sa": # right is sand
            screen.blit(grass, (8,8), (16, 8, 8, 8))
        else:
            screen.blit(grass, (6,6), (7, 7, 10, 10))


    return pygame.transform.scale(screen, (64, 64))


def check_stone_tile(tile_map, x, y):
    screen = pygame.Surface((16, 16), pygame.SRCALPHA)
    screen.blit(grass_img, (0,0))
    #check top left
    if tile_map[x-1][y][0] == "g": # above is sand?
        if tile_map[x][y-1][0] == "g": # left is sand?
            screen.blit(stone, (0, 0), (0, 0, 10, 10)) # top left corner
        else:
            screen.blit(stone, (0, 0), (8, 0, 8, 8)) # straight edge top

        if tile_map[x][y+1][0] == "g": # right is sand?
            screen.blit(stone, (6,0), (14, 0, 10, 10))
        else:
            screen.blit(stone, (8,0), (8, 0, 8, 8))

    else: # above not sand
        if tile_map[x][y-1][0] == "g": # left is sand
            screen.blit(stone, (0,0), (0, 8, 8, 8))
        else:
            screen.blit(stone, (0,0), (7, 7, 10, 10))

        if tile_map[x][y+1][0] == "g": # right is sand
            screen.blit(stone, (8,0), (16, 8, 8, 8))
        else:
            screen.blit(stone, (6,0), (7, 7, 10, 10))

    
    #check bottom right
    if tile_map[x+1][y][0] == "g": # below is sand?
        if tile_map[x][y+1][0] == "g": # right is sand?
            screen.blit(stone, (6, 6), (14, 14, 10, 10)) # bottom right corner
        else:
            screen.blit(stone, (6, 6), (7, 14, 10, 10)) # straight edge bottom
        if tile_map[x][y-1][0] == "g": # left is sand?
            screen.blit(stone, (0,6), (0, 14, 10, 10)) # bottom right corner
        else:
            screen.blit(stone, (0,8), (8, 16, 8, 8)) # straight edge bottom

    else: # below is stone
        if tile_map[x][y-1][0] == "g": # left is sand
            screen.blit(stone, (0,8), (0, 8, 8, 8)) #
        else:
            screen.blit(stone, (0,8), (7, 7, 10, 10)) 

        if tile_map[x][y+1][0] == "g": # right is sand
            screen.blit(stone, (8,8), (16, 8, 8, 8))
        else:
            screen.blit(stone, (6,6), (7, 7, 10, 10))


    return pygame.transform.scale(screen, (64, 64))
