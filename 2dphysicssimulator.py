import pygame, sys
from pygame.locals import *

# Global variables
clock = pygame.time.Clock()
display = pygame.display

# Initialization
class App:
    def __init__(self):
        self._running = True
        self.size = self.width, self.height = 640, 400
        self._display = display.set_mode(self.size)
        self.fpsLimit = 60

    def exitGame(self):
        pygame.quit()
    
    def execute(self):
        while (self._running):
            clock.tick(self.fpsLimit)
            display.update()

        self.exitGame()

game = App()
game.execute()