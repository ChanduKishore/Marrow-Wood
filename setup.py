import pygame

class Dimensions():
    def __init__(self):
        self.width = 720
        self.height = 480
        self.half_screen_width = self.width / 2
        self.one_tenth_screen_height = self.height / 10
        self.screen = pygame.display.set_mode((self.width, self.height))

