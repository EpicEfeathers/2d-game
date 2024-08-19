import pygame
import numpy as np
import sys
import math
import time
import random

from generate_corners import check_grass_tile, check_stone_tile, check_sand_tile
from map import generate_map, display_map
from terrain import generate_terrain, blit_terrain

from pygame.locals import *

pygame.init()

WINDOW_SIZE = 1280, 832
GAME_SIZE = 832, 832

game_font = pygame.font.SysFont('arial', 22)

scale = 4
terrain_images_size = 16
new_size = (terrain_images_size * scale, terrain_images_size * scale)
tile_size = terrain_images_size * scale


sand_img = pygame.transform.scale(pygame.image.load('textures/tiles/sand.png'), new_size)
stone_img = pygame.transform.scale(pygame.image.load('textures/tiles/stone.png'), new_size)
grass_img = pygame.transform.scale(pygame.image.load('textures/tiles/grass.png'), (new_size[0]*4, new_size[1]*4))
grass_img2 = pygame.transform.scale(pygame.image.load('textures/tiles/grass2.png'), (new_size[0]*2, new_size[1]*2))

flowers1_img = pygame.transform.scale(pygame.image.load('textures/tiles/flowers1.png'), new_size)
water_img = pygame.transform.scale(pygame.image.load('textures/tiles/water.png'), new_size)
#deep_water_img = pygame.transform.scale(pygame.image.load('textures/blocks/deep_water.png'), new_size)
#shore_water_img = pygame.transform.scale(pygame.image.load('textures/blocks/shore_water.png'), new_size)
snow_img = pygame.transform.scale(pygame.image.load('textures/tiles/snow.png'), new_size)
grass_corners_img = (pygame.image.load('textures/tiles/grass_corners.png'))

tile_surfaces = {
    "st": pygame.transform.scale(pygame.image.load("textures/tiles/stone.png"), new_size),  # Load image and optimize it
    "sa": pygame.transform.scale(pygame.image.load("textures/tiles/sand.png"), new_size),
    "w": pygame.transform.scale(pygame.image.load("textures/tiles/water.png"), new_size),
    "g": pygame.transform.scale(pygame.image.load("textures/tiles/dirt.png"), new_size),
    "sn": pygame.transform.scale(pygame.image.load("textures/tiles/snow.png"), new_size)
}


#terrain_images = [deep_water_img, water_img, shore_water_img, sand_img, grass_img, stone_img, snow_img]
terrain_images = [water_img, sand_img, grass_img, flowers1_img, stone_img, snow_img, grass_corners_img]

player_skin = pygame.image.load('textures/skins.png')
wave = pygame.image.load('textures/wave.png')
player_head = pygame.transform.scale(pygame.image.load('textures/player_head.png'), (8 * scale / 2, 7 * scale / 2))


class Player:
    def __init__(self):
        self.base_speed = 16
        self.speed = self.base_speed
        self.animations = self.Animations()

    class Animations:
        def __init__(self):
            self.last_tick = pygame.time.get_ticks()
            self.frame = 0
        def get_image(self, x, y, width, height):
            self.image = pygame.Surface((width, height), pygame.SRCALPHA)
            self.image.blit(player_skin, (0,0), ((x * width), (y*height), width, height))

            return self.image
        
        def get_frame(self):
            keys = pygame.key.get_pressed()
            if keys:
                now = pygame.time.get_ticks()
                if now - self.last_tick > 200:
                    self.frame += 1
                    self.last_tick = pygame.time.get_ticks()


        def walk_left(self):
            self.get_frame()
            return pygame.transform.flip(self.get_image(self.frame%2,1,16,16), True, False)
        def walk_right(self):
            self.get_frame()
            return self.get_image(self.frame%2,1,16,16)
        def walk_up(self):
            self.get_frame()
            return pygame.transform.flip(self.get_image(1,0,16,16), bool(self.frame%2), False)
        def walk_down(self):
            self.get_frame()
            return pygame.transform.flip(self.get_image(0,0,16,16), bool(self.frame%2), False)
        def swim(self):
            self.get_frame()
            return self.get_image(2 + self.frame%2,0,16,16)
        

class Game:
    def __init__(self, window_size, game_size):
        self.player = Player()
        self.window_size = window_size
        self.game_size = game_size
        self.edges = (game_size[0] - window_size[0]/tile_size)*tile_size, (game_size[1] - window_size[1]/tile_size)*tile_size
        self.screen = pygame.display.set_mode(window_size, pygame.HWSURFACE | pygame.DOUBLEBUF, vsync=1)
        pygame.display.set_caption('Game')
        self.clock = pygame.time.Clock()
        self.debug_value = True
        self.fps = 0
        self.clock = pygame.time.Clock()
        self.terrain_map = generate_terrain()
        self.x = game_size[0]/2 * tile_size - (self.window_size[0] / 2)
        self.y = game_size[1]/2 * tile_size - (self.window_size[1] / 2)
        self.frame = self.player.animations.get_image(0,1,16,16)
        self.player_tile = 4
        self.speed = self.player.speed

        self.game_state = "overworld"
        self.map = generate_map(self.game_size, self.terrain_map)

    def run(self):
        while True:
            self.check_main_input()
            self.check_game_state()
            self.debug_screen()

            self.fps = self.clock.get_fps()
            pygame.display.update()
            self.clock.tick()



    def check_game_state(self):
        if self.game_state == "overworld":
            self.overworld()
        elif self.game_state == "map":
            #self.display_map()
            self.screen = display_map(self.screen, self.map, self.window_size, self.game_size, self.display_x, self.display_y, player_head)



    def overworld(self):
        self.check_player_input()
        self.player_tile = self.get_tile()
        blit_terrain(self.screen, self.window_size, tile_size, self.x, self.y, self.terrain_map, grass_img, terrain_images_size, terrain_images, tile_surfaces)
        self.blit_player()



    def check_main_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.exit()
                if event.key == K_F3:
                    self.debug_value = not self.debug_value
                if event.key == K_m:
                    if self.game_state == "overworld":
                        self.game_state = "map"
                    elif self.game_state == "map":
                        self.game_state = "overworld"
    


    def exit(self):
        pygame.quit()
        sys.exit()



    def check_player_input(self):
        keys = pygame.key.get_pressed()
        direction = [0,0]

        if keys[K_d]:
            direction[0] += 1
            self.frame = self.player.animations.walk_right()

        elif keys[K_a]:
            direction[0] -= 1
            self.frame = self.player.animations.walk_left()
        if keys[K_w]:
            direction[1] -= 1
            self.frame = self.player.animations.walk_up()
        elif keys[K_s]:
            direction[1] += 1
            self.frame = self.player.animations.walk_down()
           

        if direction[0] != 0 and direction[1] != 0:
            diagonal_speed = self.speed/math.sqrt(2)  # Adjust speed for diagonal movement
        else:
            diagonal_speed = self.speed

        self.x += direction[0] * diagonal_speed
        self.y += direction[1] * diagonal_speed

        # check boundaries
        if self.x < 0:
            self.x = 0
        elif self.x > self.edges[0] - tile_size:
            self.x = self.edges[0] - tile_size
        if self.y < 0:
            self.y = 0
        elif self.y > self.edges[1] - tile_size:
            self.y = self.edges[1] - tile_size
        self.display_x = round(self.x/tile_size - self.game_size[0]/2 + (self.window_size[0] / tile_size / 2), 2)
        self.display_y = round(self.y/tile_size - self.game_size[1] / 2 + (self.window_size[1] / tile_size / 2), 2)
            


    def draw_text(self, text, antialias: bool, color: tuple[int, int, int], position: tuple[int, int]):
        text_surf = game_font.render(text, antialias, color)
        self.screen.blit(text_surf, position)



    def debug_screen(self):
        if self.debug_value:
            self.draw_text(f"FPS: {round(self.fps)}\nX: {self.display_x}\nY: {self.display_y}\nX act: {self.x}\nY act: {self.y}\nGame state: {self.game_state}\nTile: {self.player_tile}", False, (255, 255, 255), (3,0))



    def get_tile(self):
        return self.terrain_map[int(self.display_y + GAME_SIZE[1]/2)][int(self.display_x + GAME_SIZE[0]/2)]

 

    def blit_player(self):
        if self.player_tile[0] != "w":
            self.speed = self.player.base_speed
            self.screen.blit(pygame.transform.scale(self.frame, new_size), (self.window_size[0]/2-tile_size/2,self.window_size[1]/2-tile_size/2))
        else:
            # player (just head)
            self.speed = self.player.base_speed/2
            self.screen.blit(pygame.transform.scale(self.frame, new_size), (self.window_size[0]/2-tile_size/2,self.window_size[1]/2-tile_size/2), (0, 0, 64, 32))
            # wave
            self.screen.blit(pygame.transform.scale(self.player.animations.swim(), new_size), (self.window_size[0]/2-tile_size/2,self.window_size[1]/2-tile_size/2))



def main():
    game = Game(WINDOW_SIZE, GAME_SIZE)
    game.run()

if __name__ == "__main__":
    main()