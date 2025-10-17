import pygame
class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y, TILE_SIZE, scale):
        pygame.sprite.Sprite.__init__(self)
        self.scale = scale
        self.image = pygame.transform.scale(img, (img.get_width()*scale, img.get_height()*scale))
        # self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
    def update(self, screen_scroll, y_scroll):
        self.rect.x += screen_scroll
        self.rect.y += y_scroll