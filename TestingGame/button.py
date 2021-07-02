import pygame

class Button():
    def __init__(self, x, y, image, scale):
        self.width = image.get_width()
        self.height = image.get_height()
        self.image = pygame.transform.scale(image, (int(self.width * scale), int(self.height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.click = False

    def draw(self, surface):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()
        #draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            pygame.draw.rect(surface, (255, 255, 255), self.rect, 1)
            if pygame.mouse.get_pressed()[0] == 1 and self.click == False:
                self.click = True
                action = True
                # print('Clicked')
        if pygame.mouse.get_pressed()[0] == 0:
            self.click = False


        return action