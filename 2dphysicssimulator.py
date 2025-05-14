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
        self._backdrop = pygame.image.load('2824536.jpg')

    def exitGame(self):
        pygame.quit()
        sys.exit()
    
    def execute(self):
        while (self._running):
            clock.tick(self.fpsLimit)
            display.update()
            self._display.blit(self._backdrop, (0,0))

        self.exitGame()

game = App()
game.execute()