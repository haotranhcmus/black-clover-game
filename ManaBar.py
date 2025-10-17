import pygame
class ManaBar():
    def __init__(self, x, y, mana):
        self.x = x
        self.y = y
        self.mana = mana
        self.max_mana = mana

    def draw(self, screen, mana):
        BLUE = (52, 155, 235)
        GRAY = (185, 191, 199)
        BLACK = (0, 0, 0)
        #update with new mana
        self.mana = mana
        #calculate mana ratio
        ratio = (self.mana) / (self.max_mana)
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 139, 24), 20)
        pygame.draw.rect(screen, GRAY, (self.x, self.y, 135, 20))
        pygame.draw.rect(screen, BLUE, (self.x, self.y, 135 * ratio, 20))