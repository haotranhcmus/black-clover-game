import pygame 

#button class
class ButtonGame():
    def __init__(self,x, y, width, height, list_surface):
        self.list_surface = list_surface
        self.index = 0
        self.surface = self.list_surface[self.index]
        self.rect = pygame.Rect(x, y, width, height)
        self.rect.topleft = (x, y)
        self.clicked = False
        self.start = False
        self.count = 0

    def draw(self, surface):
        action = False

		#get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

		#draw button
        surface.blit(self.surface, (self.rect.x, self.rect.y))
        if action:
            self.start = True
    def update(self):
        if self.start:
            self.count += 1
            if(self.count % 5 == 0):
                self.index += 1
                if(self.index >= len(self.list_surface)):
                    self.start = False
                    self.index = 0
                    return True
        self.surface = self.list_surface[self.index]   
        return False

            