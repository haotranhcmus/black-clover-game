import pygame
import os
from Player import Player
from HealthBar import HealthBar
from Monster import Monster
from Book import Book
from Decoration import Decoration
from AnimationDecoration import AnimationDecoration
class World():
    def __init__(self):
        self.obstacle_list = []
        self.space_list = []
    def process_data(self, map_data, char_data, map_img_list, char_img_list, TILE_SIZE, monster_group,decoration_group, SCREEN_WIDTH, DISPLAY_SCREEN_HEIGHT, bg_rect, animation_decoration_group, distancex, distancey):
        #iterate through each value in level data file
        player = 0
        for y, row in enumerate(map_data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = map_img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect, tile)
                    if tile >= 0 and tile <= 101:
                        self.obstacle_list.append(tile_data)
                    else:
                        self.space_list.append(tile_data)
        for y, row in enumerate(char_data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = char_img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile == 0:
                        monster = Monster(x * TILE_SIZE+distancex, y * TILE_SIZE - distancey , "black", 1.05)
                        monster_group.add(monster)
                    elif tile == 1:
                        monster = Monster(x * TILE_SIZE+distancex, y * TILE_SIZE - distancey,"green", 1.05)
                        monster_group.add(monster)
                    elif tile == 2:
                        player = Player(x * TILE_SIZE+distancex, y * TILE_SIZE - distancey, DISPLAY_SCREEN_HEIGHT, bg_rect)
                    elif tile == 9:
                        animation_decoration = AnimationDecoration(x * TILE_SIZE+distancex, y * TILE_SIZE - distancey, TILE_SIZE,0.27, "blueRuby")
                        animation_decoration_group.add(animation_decoration)
                    elif tile == 10:
                        animation_decoration = AnimationDecoration(x * TILE_SIZE+distancex, y * TILE_SIZE - distancey, TILE_SIZE,0.27, "redRuby")
                        animation_decoration_group.add(animation_decoration)
                    elif tile == 12:
                        animation_decoration = AnimationDecoration(x * TILE_SIZE+distancex, y * TILE_SIZE - distancey, TILE_SIZE,0.31, "heathItem")
                        animation_decoration_group.add(animation_decoration)
                    elif tile == 11:
                        animation_decoration = AnimationDecoration(x * TILE_SIZE+distancex, y * TILE_SIZE - distancey, TILE_SIZE,0.5, "fire")
                        animation_decoration_group.add(animation_decoration)
                    elif tile == 13:
                        animation_decoration = AnimationDecoration(x * TILE_SIZE+distancex, y * TILE_SIZE - distancey, TILE_SIZE,0.31, "gold")
                        animation_decoration_group.add(animation_decoration)
                    elif tile == 14:
                        monster = Monster(x * TILE_SIZE+distancex, y * TILE_SIZE - distancey,"gray", 0.9)
                        monster_group.add(monster)
                    elif tile == 15:
                        monster = Monster(x * TILE_SIZE+distancex, y * TILE_SIZE - distancey,"yellow", 0.9)
                        monster_group.add(monster)
                    elif tile == 16:
                        monster = Monster(x * TILE_SIZE+distancex, y * TILE_SIZE - distancey,"white", 1)
                        monster_group.add(monster)
                    elif tile == 17:
                        monster = Monster(x * TILE_SIZE+distancex, y * TILE_SIZE - distancey,"red", 1)
                        monster_group.add(monster)
                    elif tile == 19:
                        img = pygame.image.load(f"./image/{tile}.png").convert()
                        decoration = Decoration(img, x * TILE_SIZE+distancex, y * TILE_SIZE - distancey, TILE_SIZE, 0.5)
                        decoration_group.add(decoration)
                    else:
                        img = pygame.image.load(f"./image/{tile}.png").convert_alpha()
                        decoration = Decoration(img, x * TILE_SIZE+distancex, y * TILE_SIZE - distancey, TILE_SIZE, 1.8)
                        decoration_group.add(decoration)

        for tile in self.obstacle_list:
            tile[1].y -= distancey
            tile[1].x += distancex
        for tile in self.space_list:
            tile[1].y -= distancey
            tile[1].x += distancex
        return player
    
    def draw(self, screen, screen_scroll, y_scroll):
        for tile in self.obstacle_list:
            tile[1].x += screen_scroll
            tile[1].y += y_scroll
            screen.blit(tile[0], tile[1])
        for tile in self.space_list:
            tile[1].x += screen_scroll
            tile[1].y += y_scroll
            screen.blit(tile[0], tile[1])

    