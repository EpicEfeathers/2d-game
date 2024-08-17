import pygame

colors = {
    0: [65, 90, 225],    # dark_blue
    1: [65, 105, 225],   # blue
    2: [65, 130, 225],   # light_blue
    3: [238, 214, 175],    # sand
    4: [34, 139, 34],  # grass
    5: [34, 139, 34],  # flowers (grass)
    6: [139, 137, 137],  # mountain (stone)
    7: [255, 250, 250],  # snow
    8: [34, 139, 34]
}


def generate_map(GAME_SIZE, terrain_map):
    map = pygame.Surface(GAME_SIZE)

    for y in range(GAME_SIZE[1]):
        for x in range(GAME_SIZE[0]):
            value = terrain_map[y, x]
            map.set_at((x, y), colors.get(value, (0, 0, 0)))

    return map


def display_map(screen, map, window_size, game_size, display_x, display_y, player_head):
    # show map
    screen.fill((0,0,0))
    screen.blit(map, ((window_size[0] - game_size[0]) / 2,0))
    # show player head
    screen.blit(player_head, (((window_size[0] / 2 + display_x - player_head.get_width() / 2), (window_size[1] / 2 + display_y - player_head.get_height() / 2))))

    return screen