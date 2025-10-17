import pygame
from Rock import Rock
from Explosion import Explosion
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, DISPLAY_SCREEN_HEIGHT, bg_rect):
        pygame.sprite.Sprite.__init__(self)
        self.bg_rect = bg_rect
        self.DISPLAY_SCREEN_HEIGHT = DISPLAY_SCREEN_HEIGHT
        self.THREADS = 500
        self.scale = 1
        self.alive = True
        self.speed = 6
        self.skill_cooldown = 0
        self.health = 100
        self.max_health = self.health
        self.mana = 100
        self.max_mana = self.mana
        self.direction = 1 #Identify direction
        self.flip = False
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.in_air = False
        self.jump = False
        self.vel_y = 10
        self.high_jump = -15
        self.score = 0
        self.gold = 0
        self.playsound = True
        self.start = False
        self.damage = 10
        self.damex2 = False
        self.quantity_damex2 = 0
        self.speed_skill = 42
        self.injured = False
#-----------------create sprites------------------------------------------------------
        sprite_sheet = pygame.image.load("./assest/eight.png").convert_alpha()
        sprite_sheet = pygame.transform.scale(sprite_sheet, (sprite_sheet.get_width()*self.scale, sprite_sheet.get_height()*self.scale))
        blink_sheet = pygame.image.load("./assest/blink.png").convert()
        blink_sheet.set_colorkey((255,255,255))
        blink_sheet = pygame.transform.scale(blink_sheet, (sprite_sheet.get_width()*self.scale, sprite_sheet.get_height()*self.scale))
        ROWS = 9
        COLS = 8
        FRAME_WIDTH = sprite_sheet.get_width() // COLS
        FRAME_HEIGHT = sprite_sheet.get_height() // ROWS
        frames = []
        for row in range(ROWS):
            for col in range(COLS):
                frame_rect = pygame.Rect(col * FRAME_WIDTH, row * FRAME_HEIGHT, FRAME_WIDTH, FRAME_HEIGHT)
                frame = sprite_sheet.subsurface(frame_rect)
                frames.append(frame)
        blink = [blink_sheet.subsurface(pygame.Rect( 0, 0, FRAME_WIDTH, FRAME_HEIGHT)), blink_sheet.subsurface(pygame.Rect( FRAME_WIDTH, 0, FRAME_WIDTH, FRAME_HEIGHT))]
        stand = frames[0: 2]
        stand.extend(frames[8: 10])
        skill = frames[64:66]
        self.animation_list = [stand, frames[24:29], frames[40:48], frames[48:51], skill, blink]

        # 0: stand, 1: run, 2: jump, 3: skill
#-----------------create sprites------------------------------------------------------

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect(center = (x,y))
        self.body_rect = pygame.Rect(self.rect.left, self.rect.top, self.rect.width - 40, self.rect.height)
        self.width = self.body_rect.width
        self.height = self.body_rect.height

    def update(self, player, rock_group, explosion_group):
        self.check_alive()
        self.body_rect.center = self.rect.center
        if self.rect.x <= 140 or self.rect.y >= self.DISPLAY_SCREEN_HEIGHT:
            self.health = 0
        self.update_animation()
        #update cooldown
        if self.skill_cooldown > 0:
            self.skill_cooldown -= 1


    def move(self, moving_left, moving_right, GRAVITY, world_list, screen_scroll, drop_fx):
        #reset movement variables
        dx = 0
        dy = 0
        #assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        #jump
        if self.jump and self.in_air == False:
            self.vel_y = self.high_jump
            self.jump = False
            self.in_air = True
        #apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y
        #check for collision-------------------------------------------
        for world in world_list:
            for tile in world.obstacle_list:
                #check collision in the x direction
                if tile[1].colliderect(self.body_rect.x + dx, self.body_rect.y - 10, self.width, self.height):
                    dx = 0
                #check for collision in the y direction
                if tile[1].colliderect(self.body_rect.x, self.body_rect.y + dy, self.width, self.height):
                    dy = 0
                    #check if below the ground, i.e. jumping
                    if self.vel_y < 0:
                        self.vel_y = 0
                        dy = tile[1].bottom - self.rect.top
                    #check if above the ground, i.e. falling
                    elif self.vel_y >= 0:
                        if self.vel_y > 5 and self.jump == False:
                            drop_fx.play()
                        self.vel_y = 0
                        self.in_air = False
                        dy = tile[1].top - self.rect.bottom
        
        #update rectangele position
        self.rect.x += dx + screen_scroll
        self.rect.y += dy
        y_scroll = 0
        x_scroll = 0
        if (self.bg_rect.bottom - dy > self.DISPLAY_SCREEN_HEIGHT) and (self.bg_rect.top -dy < -1) and ((self.bg_rect.bottom - self.rect.bottom > 700) or (self.rect.top -self.bg_rect.top >800)):
            self.rect.y -= dy
            y_scroll = -int(dy)
        if self.rect.right > 950:
            self.rect.x -= 3
            x_scroll -= 3
        return y_scroll, int(x_scroll - 2)

    def skill(self, rock_group):
        if self.skill_cooldown == 0 and self.mana >0:
            self.mana -= 4
            self.skill_cooldown = self.speed_skill
            rock = Rock(self.rect.centerx + int((self.rect.size[0]/1.3 - 20)) * self.direction, self.rect.centery * 1.06, self.direction, self.scale)
            if(self.direction == -1):
                rock = Rock(self.rect.centerx + int((self.rect.size[0]) - 50) * self.direction, self.rect.centery * 1.06, self.direction, self.scale)
            rock_group.add(rock)
            
    def tele(self, dx, world_list):
        for world in world_list:
            for tile in world.obstacle_list:
                #check collision in the x direction
                if tile[1].colliderect(self.body_rect.x + dx, self.body_rect.y - 10, self.width, self.height):
                    dx = 0
        self.rect.x += dx

    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 120
        if self.action == 4:
            ANIMATION_COOLDOWN = 200
        if self.action == 5:
            ANIMATION_COOLDOWN = 80
        #update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index = (self.frame_index + 1) 
        
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action != 3:
                self.frame_index = 0
            else:
                self.frame_index = len(self.animation_list[self.action]) - 1

    def update_action(self, new_action):
        #check if the new actions is different to the previous one
        if self.action == 5 and self.frame_index == 0:
            pass
        else:
            if new_action != self.action:
                self.action = new_action
            #update the animation settings
                self.frame_index = 0
                self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        # pygame.draw.rect(screen, (0,0,0) , self.body_rect, 4)

