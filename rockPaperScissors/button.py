from network import Network
import pygame

class Button:
    def __init__(self, image, position, callback, background_image):
        self.image = image
        self.rect = image.get_rect(topleft=position)
        self.callback = callback
        self.background_image = background_image
 
    def on_click(self, event):
        if event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback(self)

    def get_width(self):
        return self.image.get_width()

    def draw(self, win):
        if self.background_image:
            win.blit(self.background_image, self.rect)

        win.blit(self.image, self.rect)
    
    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.rect.x <= x1 <= self.rect.x + self.image.get_width() and self.rect.y <= y1 <= self.rect.y + self.image.get_height():
            return True
        else:
            return False
        