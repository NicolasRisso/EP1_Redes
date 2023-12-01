import pygame as pg

pg.font.init() 

FONT_SIZE = 32

class Text:
    def __init__(self, x, y, text='', color=(0, 0, 0), font_size=None):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font_size = font_size or FONT_SIZE

    def draw(self, screen):
        font = pg.font.SysFont("roboto", self.font_size)
        text_surface = font.render(self.text, True, self.color)
        screen.blit(text_surface, (self.x, self.y))
    
    def setText(self, text=''):
        self.text = text