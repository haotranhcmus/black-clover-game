import pygame
from AnimationDecoration import AnimationDecoration
import os
import random
class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, color, scale):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = 1
        self.health = 25
        if color == "red":
            self.health = 40
        self.max_health = self.health
        self.direction = 1
        self.flip = False
        self.animation_list = []
        self.action = 1
        self.frame_index = 0
        self.color = color
        self.scale = scale
        
        self.injured = False
        self.quantity_injured_countdown = 5

        self.kill_countdown = 30
        self.update_time = pygame.time.get_ticks()
        self.count = 0
        #load all images for the players
        animation_type = ["run", "attack", "dead"]
        for animation in animation_type:
            #reset temporary list of images
            temp_list = []
            #count number of files in the folder
            number_of_frames = len(os.listdir(f'./assest/{self.color}_monster/{animation}'))
            for i in range(number_of_frames):
                if animation == "dead" and i == 1:
                    img = pygame.image.load(f"./assest/{self.color}_monster/{animation}/{i}.png").convert()
                    img.set_colorkey((255,255,255))
                else:
                    img = pygame.image.load(f"./assest/{self.color}_monster/{animation}/{i}.png").convert_alpha()
                    
                img = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.vel_y = 0
        self.vision = pygame.Rect(0, 0, self.rect.width + 20, self.rect.height)
        self.area = pygame.Rect(0, 0, 500, 80)
        if self.color == "white":
            self.vision.width = self.rect.width + 150
        self.body_rect = pygame.Rect(self.rect.x, self.rect.y + 10, self.rect.width, self.rect.height - 10)

    def update(self, monster, rock_group, player, world_list, GRAVITY, screen_scroll, y_scroll, animation_decoration_group, TILE_SIZE):
        self.rect.x += screen_scroll
        self.rect.y += y_scroll
        self.area.centery = self.rect.centery
        self.update_animation()
        self.check_alive()
        moving_right = False
        if self.alive:
            #check if the monster in near player
            if self.area.colliderect(player.body_rect) and player.alive:
                #check if the player is to the left or right of the monster.
                if player.body_rect.centerx - self.rect.centerx > 0:
                    self.direction = 1
                    moving_right = True
                else: 
                    self.direction = -1
                    moving_right = False
                moving_left = not moving_right
                #check if the player is within the monster's line of sight.
                if self.vision.colliderect(player.body_rect):
                    self.speed = 0
                    self.update_action(1)
                    if self.frame_index == 1 and self.color == "white":
                        player.health -= 1
                        player.start = True
                        player.update_action(5)
                        player.injured = True
                        if player.vel_y == 0:
                            player.tele(self.direction*4, world_list)
                    elif (self.frame_index == 2 or self.frame_index == 7) and self.color != "white":
                        player.injured = True
                        player.health -= 1
                        player.update_action(5)
                        player.start = True
                        if player.vel_y == 0:
                            player.tele(self.direction*4, world_list)
                else:
                    self.speed = 2
                    self.update_action(0)
                #update moving
                self.move(moving_left, moving_right, world_list, GRAVITY)
            else:
                if self.injured:
                    self.speed = 0
                    self.update_action(2)
                    self.quantity_injured_countdown -= 1
                    if self.quantity_injured_countdown < 0:
                        self.quantity_injured_countdown = 5
                        self.injured = False
                else:
                    self.speed = 2
                    self.update_action(0)
                if self.direction == 1:
                    moving_right = True
                moving_left = not moving_right
                self.move(moving_left, moving_right, world_list, GRAVITY)
            self.vision.center = (self.rect.centerx, self.rect.centery)
            self.area.center = (self.rect.centerx, self.rect.centery)
        else:
            self.kill_countdown -= 1
            if self.kill_countdown <= 0:
                rand_number = int(random.random() * 10)
                if rand_number == 1:
                    animation_decoration = AnimationDecoration(self.rect.centerx, self.rect.centery, TILE_SIZE,0.31, "heathItem")
                elif rand_number == 2:
                    animation_decoration = AnimationDecoration(self.rect.centerx, self.rect.centery, TILE_SIZE,0.31, "fire")
                elif rand_number == 3:
                    animation_decoration = AnimationDecoration(self.rect.centerx, self.rect.centery, TILE_SIZE,0.31, "blueRuby")
                else:
                    animation_decoration = AnimationDecoration(self.rect.centerx, self.rect.centery, TILE_SIZE,0.31, "gold")
                animation_decoration_group.add(animation_decoration)
                animation_decoration = AnimationDecoration(self.rect.centerx + 20, self.rect.centery + 20, TILE_SIZE,0.31, "gold")
                animation_decoration_group.add(animation_decoration)
                animation_decoration = AnimationDecoration(self.rect.centerx - 20,  self.rect.centery +20, TILE_SIZE,0.31, "gold")
                animation_decoration_group.add(animation_decoration)
                if self.color == "red":
                    animation_decoration = AnimationDecoration(self.rect.centerx + 20, self.rect.centery - 20, TILE_SIZE,0.31, "gold")
                    animation_decoration_group.add(animation_decoration)
                    animation_decoration = AnimationDecoration(self.rect.centerx - 20,  self.rect.centery - 20, TILE_SIZE,0.31, "gold")
                    animation_decoration_group.add(animation_decoration)
                self.kill()

    def move(self, moving_left, moving_right, world_list, GRAVITY):
        #reset movement variables
        dx = 0
        dy = 0
        self.vel_y += GRAVITY
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y
        #assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
        if moving_right:
            dx = self.speed
            self.flip = False
        for world in world_list:
            for tile in world.obstacle_list:
                #check collision in the x direction
                if tile[1].colliderect((self.body_rect.x + dx, self.body_rect.y - 10, self.body_rect.width, self.body_rect.height)):
                    dx = 0
                    self.direction *= (-1)
                if tile[1].colliderect(self.body_rect.x , self.body_rect.y + dy - 1, self.body_rect.width, self.body_rect.height):
                    dy = 0
                    #check if above the ground, i.e. falling
                    if self.vel_y >= 0:
                        self.vel_y = 0
                        self.in_air = False
                        dy = tile[1].top - self.rect.bottom
            for tile in world.space_list:
                if tile[1].colliderect(self.rect.centerx + (self.width/2)*self.direction, self.rect.bottom + 10, 1, 1):
                    dx = 0
                    self.direction *= (-1)

        
        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def update_action(self, new_action):
        #check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
        #update the animation ssettings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(2)

    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 100
        if self.action == 0:
            ANIMATION_COOLDOWN = 150
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index = (self.frame_index + 1) % len(self.animation_list[self.action])
        #update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
    
    def draw(self, screen):
        if self.flip and self.action == 1:
            rect = self.image.get_rect()
            rect.right = self.rect.right
            rect.centery = self.rect.centery
            screen.blit(pygame.transform.flip(self.image, self.flip, False), rect)

        else:
            screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x, self.rect.y + 10, self.rect.width, self.rect.height))
            RED = (255, 0, 0)
            GRAY = (133, 130, 125)
            BLACK = (0, 0, 0)
            #calculate health ratio
            ratio = (self.health) / (self.max_health)
            boder_length = 1
            length = 40
            height = 5
            if self.color == "red":
                length = 70
                height = 10
            pygame.draw.rect(screen, BLACK, (self.rect.centerx - (length//2 + boder_length), self.rect.y + 20 - 1, length + 2*boder_length, height + 2*boder_length), boder_length)
            pygame.draw.rect(screen, GRAY, (self.rect.centerx - length//2, self.rect.y + 20, length, height))
            pygame.draw.rect(screen, RED, (self.rect.centerx - length//2, self.rect.y + 20, length * ratio, height))
        # pygame.draw.rect(screen, (0,0,0) , self.area, 4)
        dy = 40
        if self.color == "red":
            dy = 55
        dx = 10
        self.body_rect = pygame.Rect(self.rect.x + dx, self.rect.y + dy, self.rect.width - 2*dx, self.rect.height - dy)
        # pygame.draw.rect(screen, (0,0,0) , self.body_rect, 4)
        # if self.color == "white":
        #     screen.fill((255,0,0), self.vision, 4)



            
