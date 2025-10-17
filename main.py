import pygame
import csv
import os
from Player import Player
from Rock import Rock
from Book import Book
from Monster import Monster
from HealthBar import HealthBar
from Decoration import Decoration
from World import World
from ButtonGame import ButtonGame
from ManaBar import ManaBar
from pygame import mixer
import random
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
mixer.init()
pygame.init()
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.7)
DISPLAY_SCREEN_HEIGHT = SCREEN_HEIGHT*0.6
DISPLAY_SCREEN_WIDTH =  SCREEN_WIDTH*0.8
distance = SCREEN_HEIGHT - DISPLAY_SCREEN_HEIGHT
screen = pygame.display.set_mode((DISPLAY_SCREEN_WIDTH, DISPLAY_SCREEN_HEIGHT))
pygame.display.set_caption("ULTIMATE SURVIVORS")

#set framerate------------------------------------------------------------
clock = pygame.time.Clock()
FPS = 60
#define player action variables------------------------------------------------
moving_left = False
moving_right = False
skill = False
#define color--------------------------------------------------------------------
GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
RED = (255, 0, 0)
GREEN = (144, 201, 120)
#load music and sounds
pygame.mixer.music.load("./sounds/sound2.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1, 0.0, 5000)

attack_fx = pygame.mixer.Sound("./sounds/attack.wav")
jump_fx = pygame.mixer.Sound("./sounds/jump.wav")
dead_fx = pygame.mixer.Sound("./sounds/dead.wav")
gold_fx = pygame.mixer.Sound("./sounds/gold.ogg")
drop_fx = pygame.mixer.Sound("./sounds/move.wav")
rock_fx = pygame.mixer.Sound("./sounds/rock.wav")
fire_fx = pygame.mixer.Sound("./sounds/damex2.wav")
recharge_fx = pygame.mixer.Sound("./sounds/recharge.wav")
explosion_fx = pygame.mixer.Sound("./sounds/explosion.wav")

attack_fx.set_volume(0.2)
jump_fx.set_volume(0.06)
dead_fx.set_volume(0.2)
gold_fx.set_volume(0.2)
drop_fx.set_volume(0.8)
rock_fx.set_volume(0.1)
fire_fx.set_volume(0.2)
recharge_fx.set_volume(0.2)
explosion_fx.set_volume(0.27)

play_dead_sound = True
#define font
game_font = pygame.font.Font("04B_19.TTF", 60)
explain_font = pygame.font.Font("04B_19.TTF", 50)
gold_font = pygame.font.Font("04B_19.TTF", 30)
pixel_font = pygame.font.Font("pixel.ttf", 40)
time_font = pygame.font.Font("pixel.ttf", 50)
def score_display(x, y, color, font, content):
    score_surface = font.render(content, True, color)
    score_rect = score_surface.get_rect(center = (x, y))
    screen.blit(score_surface, score_rect)
#define game variables--------------------------------------------------------------------
ROWS = 16
COLS = 21
rand_level = 0
GRAVITY = 0.6
TILE_SIZE = (SCREEN_HEIGHT // (2*ROWS))*2 
screen_scroll = 0
y_sroll = 0
bg_scroll = 0
km = 0
score = 0
high_score = 0
with open("./data/score.csv") as file:
    line = file.readlines()
    for score in line:
        high_score = max(high_score, int(score))
        
#load data of map--------------------------------------------------------------------
list_mapdata = []
for level in range(14):
    map_data = []
    for row in range(ROWS):
        r = [-1] * COLS
        map_data.append(r)
    with open(f"./map/level{level}_data.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                map_data[x][y] = int(tile) 
    list_mapdata.append(map_data)
#load image of map--------------------------------------------------------------------
all_tile_image = pygame.image.load("img/tile.png").convert_alpha()
tile = all_tile_image.get_width() // 17
map_img_list = []
for y in range(11):
    for x in range(17):
        img = all_tile_image.subsurface((x*tile, y*tile, tile, tile))
        img = pygame.transform.scale(img, (TILE_SIZE,TILE_SIZE))
        map_img_list.append(img)
#load image of character--------------------------------------------------------------------
char_img_list = []
addition = len(os.listdir(f'./image'))
for i in range(addition):
    if i <=2:
        img = pygame.image.load(f"./image/{i}.png").convert()
        img.set_colorkey((255,255,255))
    img = pygame.transform.scale(img, (TILE_SIZE,TILE_SIZE))
    char_img_list.append(img)   
#load data of char--------------------------------------------------------------------       
list_chardata = []
for level in range(14):
    char_data = []
    for row in range(ROWS):
        r = [-1] * COLS
        char_data.append(r)
    with open(f"./char/char{level}_data.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                char_data[x][y] = int(tile)
    list_chardata.append(char_data)
#draw_bg
bg = pygame.image.load("img/background/mountain.png").convert_alpha()
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
bg_rect = bg.get_rect()
bg_rect.centery -= distance
bg_rect.centerx = 0
def draw_bg():
    bg_rect.centery += y_sroll

#create sprite groups--------------------------------------------------------------------
rock_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
monster_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
animation_decoration_group = pygame.sprite.Group()

world0 = World()
world1 = World()
world2 = World()
rand_level = int(random.random()*14)
player = world0.process_data(list_mapdata[0], list_chardata[0], map_img_list, char_img_list, TILE_SIZE, monster_group,decoration_group, SCREEN_WIDTH, DISPLAY_SCREEN_HEIGHT, bg_rect, animation_decoration_group, 0, distance)
world1.process_data(list_mapdata[rand_level], list_chardata[rand_level], map_img_list, char_img_list, TILE_SIZE, monster_group,decoration_group, SCREEN_WIDTH, DISPLAY_SCREEN_HEIGHT, bg_rect, animation_decoration_group, TILE_SIZE*COLS, distance)
rand_level = int(random.random()*14)
world2.process_data(list_mapdata[rand_level], list_chardata[rand_level], map_img_list, char_img_list, TILE_SIZE, monster_group,decoration_group, SCREEN_WIDTH, DISPLAY_SCREEN_HEIGHT, bg_rect, animation_decoration_group, 2*TILE_SIZE*COLS, distance)
world_list = [world0, world1, world2]
book = Book(player)
health_bar = HealthBar(110, 30, player.health)
mana_bar = ManaBar(125, 60, player.mana)
run = True
game_start = False
#load menu png
menu_bg = pygame.image.load("./menu/menu_bg.jpg")
magician_img = pygame.image.load("./menu/magician.png")
all_button_img = pygame.image.load("./menu/button.png")
adventure_text = pygame.image.load("./menu/adventure.png")
status_bar = pygame.image.load("./img/statusbar.png")
status_bar = pygame.transform.scale(status_bar, (status_bar.get_width()*0.6, status_bar.get_height()*0.6))
#scale img
menu_bg = pygame.transform.scale(menu_bg, (DISPLAY_SCREEN_WIDTH, DISPLAY_SCREEN_HEIGHT))
magician_img = pygame.transform.scale(magician_img, (magician_img.get_width()*0.5, magician_img.get_height()*0.5))
adventure_text = pygame.transform.scale(adventure_text, (adventure_text.get_width()*0.7, adventure_text.get_height()*0.5))

button_width = all_button_img.get_width()//3
button_height = all_button_img.get_height()//3
frames_button = []
for row in range(3):
    for col in range(3):
        frame_rect = pygame.Rect(col * button_width, row * button_height, button_width, button_height)
        frame = all_button_img.subsurface(frame_rect)
        frames_button.append(frame)
restart_btn = ButtonGame((DISPLAY_SCREEN_WIDTH - button_width)/2, (DISPLAY_SCREEN_HEIGHT - button_height)/2, button_width, button_height, frames_button[6:9])
start_btn = ButtonGame((DISPLAY_SCREEN_WIDTH - button_width)/2, 270, button_width, button_height, frames_button[0:3])
exit_btn = ButtonGame((DISPLAY_SCREEN_WIDTH - button_width)/2, 400, button_width, button_height, frames_button[3:6])

explosion_img = pygame.image.load("./img/Explosion.png")
explosion_img = pygame.transform.flip(explosion_img, True, False)
explosion_img = pygame.transform.scale(explosion_img, (int(explosion_img.get_width()*0.6), int(explosion_img.get_height()*0.6)))

frames_exp = []
exp_width = explosion_img.get_width()//15
for col in range(15):
    frame_rect = pygame.Rect(col * exp_width, 0, exp_width, explosion_img.get_height())
    frame = explosion_img.subsurface(frame_rect)
    frames_exp.append(frame)
exp_index = 0
exp_count = 0

damex2_bg = pygame.image.load("./assest/damex2.png").convert_alpha()
damex2_bg = pygame.transform.scale(damex2_bg, (damex2_bg.get_width()//2, damex2_bg.get_height()//2))
dame_rect = damex2_bg.get_rect()
dame_rect.center = (60, 120)
start_timex2 = pygame.time.get_ticks()

update_time = pygame.time.get_ticks()
wait_for_start = True
def play_explosion_sound(update_time):
    if pygame.time.get_ticks() - update_time > 1500:
        explosion_fx.play()
        return pygame.time.get_ticks()
    return update_time
def draw_damex2(x):
    time_item = 25
    period = (pygame.time.get_ticks() - start_timex2)//1000
    player.damage = 20
    if time_item - period + (x - 1)*10 >= 10:
        score_display(140, 120, (227, 118, 9), time_font, f"00:{time_item - period + (x - 1)*10}")
    elif time_item - period + (x - 1)*10 < 10 and time_item - period + (x - 1)*10 >=0:
        score_display(140, 120, (227, 118, 9), time_font, f"00:0{time_item - period + (x - 1)*10}")
    else:
        player.damex2 = False
        player.quantity_damex2 = 0
        player.damage = 10
    screen.blit(damex2_bg, dame_rect)

recharge_health = False
recharge_mana = False
price_item = 20
while run:
    
    if game_start == False:
        screen.blit(menu_bg, (0, 0))
        screen.blit(adventure_text, ((DISPLAY_SCREEN_WIDTH - adventure_text.get_width())/2, 70))
        screen.blit(magician_img, (200, 300))
        start_btn.draw(screen)
        exit_btn.draw(screen)

        if start_btn.update():
            game_start = True
        if exit_btn.update():
            run = False
    else:
        if player.injured:
            attack_fx.play()
            player.injured = False
        update_time = play_explosion_sound(update_time)
        if player.damex2 == False:
            start_timex2 = pygame.time.get_ticks()
        if player.health <= 0 and player.playsound:
            player.playsound = False
        draw_bg()
        for world in world_list:
            world.draw(screen, screen_scroll, y_sroll)
        km -= screen_scroll
        score_display(1160, 100, (255,216,52), pixel_font, f"Score: {int(km/20)}m")
        score_display(1160, 67, (255,255,255), pixel_font, f"Kill: x{int(player.score/2)}")
        score_display(1160, 35, (255,255, 255), pixel_font, f"High score: {high_score}m")
        score_display(347, 75, (255,216,52), gold_font, f"Gold: {player.gold}")
        score_display(340, 35, (255, 255, 255), pixel_font, f"FPS: {FPS}")

        # pygame.draw.line(screen, RED, (0, 560), (SCREEN_WIDTH, 560), 3)
        #update and draw decoration
        decoration_group.update(screen_scroll, y_sroll)
        decoration_group.draw(screen)
        #update and draw decoration
        animation_decoration_group.update(screen_scroll, y_sroll, player, gold_fx, recharge_fx, fire_fx)
        animation_decoration_group.draw(screen)
        #draw player
        player.update(player, rock_group, explosion_group)
        player.draw(screen)
        #update and draw groups
        rock_group.update(SCREEN_WIDTH, explosion_group, monster_group, screen_scroll, player, rock_fx, y_sroll, world_list)
        rock_group.draw(screen)
        #update and draw book
        book.update(player)
        book.draw(screen)
        #update and draw explosion
        explosion_group.update(screen_scroll)
        explosion_group.draw(screen)
        #update and draw monster
        for monster in monster_group:
            if(monster.rect.left < 160):
                monster.health = 0
            monster.update(monster, rock_group, player, world_list, GRAVITY, screen_scroll, y_sroll, animation_decoration_group, TILE_SIZE)
            monster.draw(screen)
        exp_count += 1
        if(exp_count % 5 == 0):
            exp_index = (exp_index + 1)%15
        screen.blit(frames_exp[exp_index], (-20, 0))
        #draw health bar and mana ba
        pygame.draw.rect(screen, (113, 118, 124), (20, 20, 250, 70))
        pygame.draw.rect(screen, (0,0,0), (20, 20, 250, 70), 3)
        health_bar.draw(screen, player.health)
        mana_bar.draw(screen, player.mana)
        screen.blit(status_bar, (20, 20))
        first_tile_rect = world_list[0].obstacle_list[0]
        last_tile_rect = world_list[0].obstacle_list[20]
        if screen_scroll == 0 and km == 0:
            score_display(600, 210, (255, 255, 255), explain_font, "PRESS > : RIGHT")
            score_display(600, 290, (255, 255, 255), explain_font, "PRESS < : LEFT")
            score_display(600, 370, (255, 255, 255), explain_font, "PRESS ^ : JUMP")
            score_display(600, 450, (255, 255, 255), explain_font, "PRESS SPACE : ATTACK")
        if player.damex2:
            draw_damex2(player.quantity_damex2)
            
        if first_tile_rect[1].x <= -TILE_SIZE*COLS:
            world_list.pop(0)
            rand_level = int(random.random()*14)
            new_world = World()
            new_world.process_data(list_mapdata[rand_level], list_chardata[rand_level], map_img_list, char_img_list, TILE_SIZE, monster_group,decoration_group, SCREEN_WIDTH, DISPLAY_SCREEN_HEIGHT, bg_rect, animation_decoration_group, 2*TILE_SIZE*COLS, -first_tile_rect[1].y)
            world_list.append(new_world)

        if player.start:
            pygame.draw.rect(screen, (255, 0 , 0), (0,0,DISPLAY_SCREEN_WIDTH, DISPLAY_SCREEN_HEIGHT), 6)
            player.start = False
        #update player actions
        if player.alive:
            if player.in_air and skill:
                player.skill(rock_group)
                player.update_action(4)
            elif player.in_air:
                player.update_action(2)
            elif moving_left or moving_right:
                player.update_action(1) #1: run
            elif book.update_animation:
                player.update_action(4)
            elif skill:
                player.skill(rock_group)
                player.update_action(4)
            else:
                player.update_action(0) #0: stand or idle
        else:
            high_score = max(high_score, int(km/20))
            with open("./data/score.csv", "a") as file:
                file.write(str(high_score) + "\n")
            screen_scroll = 0
            restart_btn.draw(screen)
            score_display(650, 240, (255, 255, 255), game_font,"PLAY AGAIN?")
            pygame.mixer.music.set_volume(0)
            explosion_fx.set_volume(0)
            if play_dead_sound:
                dead_fx.play()
                play_dead_sound = False
            if restart_btn.update():
                y_sroll = 0
                rock_group.empty()
                explosion_group.empty()
                monster_group.empty()
                decoration_group.empty()
                animation_decoration_group.empty()
                bg_rect.top = -distance
                bg_rect.centerx = 0
                world0 = World()
                world1 = World()
                world2 = World()
                rand_level = int(random.random()*14)
                player = world0.process_data(list_mapdata[0], list_chardata[0], map_img_list, char_img_list, TILE_SIZE, monster_group,decoration_group, SCREEN_WIDTH, DISPLAY_SCREEN_HEIGHT, bg_rect, animation_decoration_group, 0, distance)
                world1.process_data(list_mapdata[rand_level], list_chardata[rand_level], map_img_list, char_img_list, TILE_SIZE, monster_group,decoration_group, SCREEN_WIDTH, DISPLAY_SCREEN_HEIGHT, bg_rect, animation_decoration_group, TILE_SIZE*COLS, distance)
                rand_level = int(random.random()*14)
                world2.process_data(list_mapdata[rand_level], list_chardata[rand_level], map_img_list, char_img_list, TILE_SIZE, monster_group,decoration_group, SCREEN_WIDTH, DISPLAY_SCREEN_HEIGHT, bg_rect, animation_decoration_group, 2*TILE_SIZE*COLS, distance)
                world_list = [world0, world1, world2]
                book = Book(player)
                km = 0
                pygame.mixer.music.set_volume(0.2)
                explosion_fx.set_volume(0.27)
                play_dead_sound = True
                wait_for_start = True
        y_sroll, dx = player.move(moving_left, moving_right, GRAVITY, world_list, screen_scroll, drop_fx)
        if wait_for_start == False and player.health > 0:
            screen_scroll = dx
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False
        #keyboard presses
        if event.type == pygame.KEYDOWN:
            screen_scroll = -2
            wait_for_start = False
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_RIGHT :
                moving_right = True
            if event.key == pygame.K_SPACE or event.key == pygame.K_z:
                book.frame_index = 1
                book.update_animation = False
                skill = True
            if event.key == pygame.K_UP and player.alive and player.mana > 0: 
                player.jump = True
                jump_fx.play()
                player.mana -= 3
            if event.key == pygame.K_q and player.alive and player.gold >= price_item:
                player.gold -= price_item
                recharge_health = True
            if event.key == pygame.K_w and player.alive and player.gold >= price_item:
                player.gold -= price_item
                recharge_mana = True
        #keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_SPACE or event.key == pygame.K_z:
                book.update_animation = True
                skill = False
            if event.key == pygame.K_q and player.alive and recharge_health:
                player.health += 30
                if player.health > player.max_health:
                    player.health = player.max_health
                recharge_fx.play()
                recharge_health = False
            if event.key == pygame.K_w and player.alive and recharge_mana:
                player.mana += 30
                if player.mana > player.max_mana:
                    player.mana = player.max_mana
                recharge_fx.play()
                recharge_mana = False

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()