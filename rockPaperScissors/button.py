from network import Network
import pygame

class Button:
    def __init__(self, image, position, callback):
        self.image = image
        self.rect = image.get_rect(topleft=position)
        self.callback = callback
 
    def on_click(self, event):
        if event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback(self)
    
def callback_rock(button):
    Network().send("Rock")

def callback_paper(button):
    Network().send("Paper")

def callback_scissors(button):
    Network().send("Scissors")