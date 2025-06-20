import os, sys, math, pygame, pygame.mixer, numpy
from pygame.locals import *

# Settings

black = 0,0,0
white = 255,255,255
red = 255,0,0
green = 0,255,0
blue = 0,0,255

screenSize = screenWidth, screenHeight = 600, 400

screen = pygame.display.set_mode(screenSize)
clock = pygame.time.Clock()
pygame.display.set_caption('Mass Spectrometer')

# Text

global font
pygame.font.init()
font = pygame.font.SysFont('arial',20)

def write(text, location, color=black):
    screen.blit(font.render(text, True, color), location)

# Classes

class Particle:
    def __init__(self, x, y, size, color, charge, velocity = 0, direction = 0):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.width = 1
        self.velocity = velocity
        self.direction = direction
        self.vx = velocity * numpy.cos(self.direction)
        self.vy = velocity * numpy.sin(self.direction)
        self.mass = 0.911
        self.Fnetx = 0
        self.Fnety = 0
        self.charge = charge
    
    def display(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size, self.width)
        write(f"Velocity: {int(self.velocity)}", (5,0))
        write(f"Direction: {self.direction}", (5,20))
        write(f"Charge: {self.charge*10}C", (5,40))
    
    def move(self):
        self.x += self.vx/fpsLimit
        self.y += self.vy/fpsLimit
        self.direction = numpy.arctan(self.vy/self.vx)
    
    def changeVelocity(self, magnitude, direction):
        self.vx += magnitude * numpy.cos(direction)
        self.vy += magnitude * numpy.sin(direction)
        self.velocity = math.sqrt(self.vx**2 + self.vy**2)

    def updateVelocity(self, direction):
        self.vx += self.Fnetx * self.mass * numpy.cos(direction)
        self.vy += self.Fnety * self.mass * numpy.cos(direction)
        self.velocity = math.sqrt(self.vx**2 + self.vy**2)

    def magneticForce(self, direction, field):
        self.Fnety = self.charge * self.velocity * field
        self.updateVelocity(direction)
        write(f"Magnetic force: {int(self.charge * self.velocity * field)}N", (5,80))
    
    def centripetalForce(self, clockwise=True):
        if clockwise:
            self.updateVelocity(self.direction + 20)
    
    def collide(self, color):
        try:
            if screen.get_at((int(self.x - self.size), int(self.y - self.size))) == color or screen.get_at((int(self.x + self.size), int(self.y + self.size))) == color:
                self.vy = self.vy * -1
        except:
            pass
    
    def bounce(self):
        if self.x <= self.size:
            self.x = 2*self.size - self.x
            self.vx = self.vx * -1
        elif self.x >= screenWidth - self.size:
            self.x = 2*(screenWidth - self.size) - self.x
            self.vx = self.vx * -1
        if self.y <= self.size:
            self.y = 2*self.size - self.y
            self.vy = self.vy * -1
        elif self.y >= screenHeight - self.size:
            self.y = 2*(screenHeight - self.size) - self.y
            self.vy = self.vy * -1

class Plate:
    def __init__(self, x, y, l, color, field):
        self.x = x
        self.y = y
        self.l = l
        self.color = color
        self.field = field
    
    def display(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.x+self.l, self.y+10))
        pygame.draw.rect(screen, self.color, (self.x, self.y+100, self.x+self.l, self.y+10))
        write(f"Magnetic field: {self.field}T", (5,60))

e = 1.602 * (10 ** -2)
particle = Particle(100, 90, 10, red, e)
plates = Plate(150, 20, 60, black, 5)

# Game loop

fpsLimit = 60
running = True

while running:
    clock.tick(fpsLimit)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(white)

    # Particle

    moveTicker = 0

    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        if moveTicker == 0:
            moveTicker = 10
            particle.changeVelocity(10, 180)
    if keys[K_RIGHT]:
        if moveTicker == 0:
            moveTicker = 10
            particle.changeVelocity(10, 0)
    if keys[K_UP]:
        if moveTicker == 0:
            moveTicker = 10
            particle.changeVelocity(10, 270)
    if keys[K_DOWN]:
        if moveTicker == 0:
            moveTicker = 10
            particle.changeVelocity(10, 90)
    
    # Update movement tick
    if moveTicker > 0:
        moveTicker -= 1
    
    particle.display()
    particle.move()

    plates.display()

    particle.collide(black)
    particle.bounce()

    # Check if between plates
    if plates.x <= particle.x <= plates.x + plates.l and plates.y <= particle.y <= plates.y + 100:
        particle.magneticForce(3.14, plates.field)
    elif particle.x > plates.x:
        particle.centripetalForce()
    
    pygame.display.flip()

pygame.quit()
sys.exit()