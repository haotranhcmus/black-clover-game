import pygame
class HealthBar():
    def __init__(self, x, y, health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = health

    def draw(self, screen, health):
        RED = (255, 0, 0)
        GRAY = (185, 191, 199)
        BLACK = (0, 0, 0)
        #update with new health
        self.health = health
        #calculate health ratio
        ratio = (self.health) / (self.max_health)
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24), 20)
        pygame.draw.rect(screen, GRAY, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150 * ratio, 20))
        