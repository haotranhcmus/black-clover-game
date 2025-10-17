import pygame
import button
import csv
import pickle
import os

pygame.init()

clock = pygame.time.Clock()
FPS = 60

#game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(800*0.8)
LOWER_MARGIN = 100
SIDE_MARGIN = 1100

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption("Level Editor")

#define game variables
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1
ROWS = 16
MAX_COLS = 21
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21
current_tile = 0
level = 0

#load images
pine1_img = pygame.image.load("img/background/pine1.png").convert_alpha()
pine2_img = pygame.image.load("img/background/pine2.png").convert_alpha()
mountain_img = pygame.image.load("img/background/mountain.png").convert_alpha()
sky_img = pygame.image.load("img/background/sky_cloud.png").convert_alpha()
#store tiles in a list
all_tile_image = pygame.image.load("img/tile.png").convert_alpha()
rows = 11
cols = 17
tile = all_tile_image.get_width() // 17
img_list = []
char_img_list = []
length = len(os.listdir("image"))
for i in range(length):
    img = pygame.image.load(f"image/{i}.png")
    img = pygame.transform.scale(img, (TILE_SIZE,TILE_SIZE))
    char_img_list.append(img)
for y in range(11):
    for x in range(17):
        img = all_tile_image.subsurface((x*tile, y*tile, tile, tile))
        img = pygame.transform.scale(img, (TILE_SIZE,TILE_SIZE))
        img_list.append(img)
        

save_img = pygame.image.load("img/save_btn.png").convert_alpha()
load_img = pygame.image.load("img/load_btn.png").convert_alpha()

#define colours
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

#define font
font = pygame.font.SysFont("Futura", 30)

#create empty tile list
world_data = []
char_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLS
    world_data.append(r)
for row in range(ROWS):
    r = [-1] * MAX_COLS
    char_data.append(r)

#function outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#create function for drawing background
def draw_bg():
    screen.fill(GREEN)
    width = sky_img.get_width()
    for x in range(4):
        screen.blit(sky_img, (x*width-scroll*0.5,0))
        screen.blit(mountain_img, (x*width-scroll*0.6,SCREEN_HEIGHT - mountain_img.get_height() - 300))
        screen.blit(pine1_img, (x*width-scroll*0.7,SCREEN_HEIGHT - pine1_img.get_height() - 150))
        screen.blit(pine2_img, (x*width-scroll*0.8,SCREEN_HEIGHT - pine2_img.get_height()))
#draw grid
def draw_grid():
    #vertical lines
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))
    #horizontal lines
    for c in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))
#function for drawing the world tiles
def draw_world():
    for y, row in enumerate(char_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(char_img_list[tile], (x * TILE_SIZE - scroll, y*TILE_SIZE))
#create buttons
save_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = button.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)
#make a button list
button_list = []
button_col = 0
button_row = 0
for i in range(len(char_img_list)):
    tile_button = button.Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, char_img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 14:
        button_row += 1
        button_col = 0
with open(f"./map/level{level}_data.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter = ",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

run = True
while run:
    draw_bg()
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y*TILE_SIZE))
    draw_grid()
    draw_world()
    
    draw_text(f"Level: {level}", font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
    draw_text("Press UP or DOWN to change level", font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN -50)
    #save and load data
    if save_button.draw(screen):
        #save level data
        with open(f"./char/char{level}_data.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter = ",")
            for row in char_data:
                writer.writerow(row)

    if load_button.draw(screen):
        #load in level data
        #reset scroll back to the start of the level
        scroll = 0
        with open(f"./char/char{level}_data.csv", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter = ",")
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    char_data[x][y] = int(tile)
        with open(f"./map/level{level}_data.csv", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter = ",")
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)



    #draw tile panel and tiles
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count
    pygame.draw.rect(screen, RED, button_list[current_tile], 3)
    #scroll the map
    if scroll_left == True and scroll > 0:
        scroll -= 5*scroll_speed
    if scroll_right == True and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
        scroll += 5*scroll_speed
    #add new tiles to the screen
    #get mouse position
    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll) // TILE_SIZE
    y = pos[1] // TILE_SIZE

    #check that the coordinates are within the tile area
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        #update tile value
        if pygame.mouse.get_pressed()[0] == 1:
            if char_data[y][x] != current_tile:
                char_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2] == 1:
            char_data[y][x] = -1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
            if event.key == pygame.K_DOWN and level > 1:
                level -= 1
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_LSHIFT:
                scroll_speed = 5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_LSHIFT:
                scroll_speed = 1
    clock.tick(FPS)
    pygame.display.update()
pygame.quit()