import pygame
from Explosion import Explosion
import random
class Rock(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, scale):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 20
        self.frame_index = 0
        self.timer = 55
        self.scale = scale
#--------------------sprites---------------
        self.animation_list = []
        for i in range(4):
            image = pygame.image.load(f'./assest/skill_far/{3 - i}.png').convert_alpha()
            image = pygame.transform.scale(image, (image.get_width()*self.scale, image.get_height()*self.scale))
            image.set_colorkey((255,255,255))
            self.animation_list.append(image)
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
#---------------------end----------------------
        self.direction = direction
        self.update_time = pygame.time.get_ticks()

    def update(self, SCREEN_WIDTH, explosion_group, monster_group, screen_scroll, player, rock_fx, y_scroll, world_list):
        #move rock
        self.rect.x += screen_scroll
        self.rect.y += y_scroll
        ANIMATION_COOLDOWN = 150
        start = False
        self.image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index = self.frame_index + 1
        if self.frame_index >= len(self.animation_list) - 1:
            self.frame_index = len(self.animation_list) - 1
            self.rect.x += (self.direction * self.speed)
            #check if rock has gone off screen
            if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
                self.kill()
        self.timer -= 1
        for monster in monster_group:
            if monster.body_rect.colliderect(self.rect):
                damage = 5 + int((player.damage + 5) * random.random())
                if player.damage == 20:
                    damage = player.damage
                if monster.health <= damage:
                    player.score += 1
                monster.health -= damage
                monster.rect.x += player.direction*10
                monster.injured = True
                self.kill()
                rock_fx.play()
                explosion = Explosion(self.rect.centerx, self.rect.centery - 15, self.scale)
                explosion_group.add(explosion)
        for world in world_list:
            for tile in world.obstacle_list:
                #check collision in the x direction
                if tile[1].colliderect(self.rect.x, self.rect.y - 20, self.rect.width, self.rect.height - 20):
                    self.kill()
                    rock_fx.play()
                    explosion = Explosion(self.rect.centerx, self.rect.centery - 15, self.scale)
                    explosion_group.add(explosion)
                    
        if self.timer <= 0:
            self.kill()
            explosion = Explosion(self.rect.centerx, self.rect.centery - 15, self.scale)
            explosion_group.add(explosion)
            rock_fx.play()
