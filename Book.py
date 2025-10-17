import pygame
class Book():
    def __init__(self, player):
        self.direction = player.direction
        self.dy = -5
        self.orientation = True
        self.scale = player.scale
#_----------------------------Extract frames---------------------------------------------------
        self.frame_index = 0
        imgBook = pygame.image.load("./assest/book/0.png").convert_alpha()
        imgBook = pygame.transform.scale(imgBook, (imgBook.get_width()*self.scale, imgBook.get_height()*self.scale))
        
        imgBookBlink = pygame.image.load("./assest/book/5.png").convert_alpha()
        imgBookBlink = pygame.transform.scale(imgBookBlink, (imgBookBlink.get_width()*self.scale, imgBookBlink.get_height()*self.scale))
        self.animation_list = [imgBook, imgBookBlink]
#--------------------------------------------------------------------------------
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.flip = True
        self.update_time = pygame.time.get_ticks()
        self.update_animation = False

    def update(self, player):
        #self.update_animation()
        if self.update_animation:
            ANIMATION_COOLDOWN = 1100
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
                self.update_time = pygame.time.get_ticks()
                self.frame_index = 0
                self.update_animation = False 
        self.image = self.animation_list[self.frame_index]
        if self.orientation:
            self.dy += 0.5
        else:
            self.dy -= 0.5
        if self.dy == 7:
            self.orientation = False
        if self.dy == -7:
            self.orientation = True
        
        x = player.rect.centerx
        y = player.rect.centery + self.dy
        self.direction = player.direction
        self.rect.center = (int(x - player.rect.width*self.direction/2.2), y)
        if self.direction == 1:
            self.flip = True
        else:
            self.flip = False

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)