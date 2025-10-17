import pygame
import os
import random
class AnimationDecoration(pygame.sprite.Sprite):
    def __init__(self, x, y, TILE_SIZE, scale, type):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.img_list = []
        self.length = len(os.listdir(f"./decorate/{type}"))
        for i in range(self.length):
            image = pygame.image.load(f"./decorate/{type}/{i}.png").convert_alpha()
            image = pygame.transform.scale(image, (int(image.get_width()*scale), int(image.get_height()*scale)))
            self.img_list.append(image)
        self.index = int(random.random() * self.length)
        self.count = 0
        self.image = self.img_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        self.x = x
        self.y = y
        self.TILE_SIZE = TILE_SIZE

    def update(self, screen_scroll, y_scroll, player, gold_fx, recharge_fx, fire_fx):
        if self.type == "blueRuby" and self.rect.colliderect(player.body_rect):
            self.kill()
            player.mana += 20
            if player.mana > player.max_mana:
                player.mana = player.max_mana
            recharge_fx.play()
        if self.type == "heathItem" and self.rect.colliderect(player.body_rect):
            self.kill()
            player.health += 30
            if player.health > player.max_health:
                player.health = player.max_health
            recharge_fx.play()
        if self.type == "gold" and self.rect.colliderect(player.body_rect):
            self.kill()
            player.gold += 1
            gold_fx.play()
        if self.type == "redRuby" and self.rect.colliderect(player.body_rect):
            self.kill()
            player.gold += 10
            gold_fx.play()
        self.count += 1
        if self.type == "fire" and self.rect.colliderect(player.body_rect):
            player.quantity_damex2 += 1
            player.damex2 = True
            self.kill()
            fire_fx.play()
        if self.count %10 == 0:
            self.index = self.index + 1
            self.index %= self.length
        self.image = self.img_list[self.index]
        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()
        self.rect.x += screen_scroll
        self.rect.y += y_scroll