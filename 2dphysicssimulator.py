import pygame, sys
from pygame.locals import *

# Global variables
clock = pygame.time.Clock()
scale = pygame.transform.scale

# Initialization
class App:
    def __init__(self):
        self._running = True
        self.displaySurf = None
        self.imageSurf = None
        self._size = self.width, self.height = 640, 400
        self._display = pygame.display.set_mode(self._size)
        self.fpsLimit = 60
        #self._backdrop = scale(pygame.image.load('2824536.jpg'), self._size)
    
    def exitGame(self):
        pygame.quit()
        sys.exit()

    def onEvent(self, event):
        if event.type == pygame.QUIT:
                self.exitGame()

    def onLoop(self):
        pass

    def render(self):
        self._displaySurf = pygame.display.set_mode((350,350), pygame.HWSURFACE)
        self._imageSurf = pygame.image.load("truck.png").convert()
        self._displaySurf.blit(self._imageSurf, (0,0))
        pygame.display.flip()
    
    def execute(self):
        while (self._running):
            clock.tick(self.fpsLimit)
            pygame.display.update()
            #self._display.blit(self._backdrop, (0,0))
            self._display.fill((255,255,255))

            for event in pygame.event.get():
                self.onEvent(event)
            self.onLoop()
            self.render()

        self.exitGame()

# GUI
"""
class myCircle:
    def __init__(self, (x,y), size, color = (255,255,255), width = 1):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.width = width
"""
game = App()
game.execute()