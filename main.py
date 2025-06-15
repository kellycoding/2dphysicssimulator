import os, sys, math, pygame, pygame.mixer
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
pygame.display.set_caption('2D Physics Simulator')

# Classes

class Ball:
    def __init__(self, x, y, size, color, width = 1, vx = 0, vy = 0, mass=0.1, Fnetx = 0, Fnety = 0):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.width = width
        self.vx = vx
        self.vy = vy
        self.mass = mass
        self.Fnetx = Fnetx
        self.Fnety = Fnety
        
    def display(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size, self.width)
    
    def move(self):
        self.x += (self.vx/fpsLimit)
        self.y += (self.vy/fpsLimit)

        if not self.checkIfDragging():
            self.changeVelocity((self.Fnetx*self.mass)/fpsLimit, (self.Fnety*self.mass)/fpsLimit)


    def changeVelocity(self, vx, vy):
        self.vx = self.vx + vx
        self.vy = self.vy + vy
    
    def checkIfDragging(self):
        cursor = pygame.mouse.get_pos()
        leeway = self.size*5
        if mouseDown and self.x - leeway <= cursor[0] <= self.x + leeway and self.y - leeway <= cursor[1] <= self.y + leeway:
            return True

    def drag(self):
        if self.checkIfDragging():
            cursor = pygame.mouse.get_pos()
            self.x = cursor[0]
            self.y = cursor[1]

    def addForce(self, Fx, Fy):
        self.Fnetx += Fx
        self.Fnety += Fy
    
    def gravity(self, g):
        self.g = g
        self.addForce(0, self.mass*g)
    
    def normalForce(self):
        self.addForce(0, -self.Fnety)
        print(self.Fnety)
        print(self.vy)
    
    def kineticEnergy(self):
        self.Ek = 0.5 * self.mass * (self.vy ** 2)

class Obstacle:
    def __init__(self, x1, y1, x2, y2, color):
        self.rectangle = pygame.Rect(x1,y1,x2-x1,y2-y1)
        self.color = color

    def display(self):
        pygame.draw.rect(screen, self.color, self.rectangle)

# Objects
ball = Ball(100, 10, 10, red)

obstacles = []
obstacles.append(Obstacle(0, 300, 600, 400, black))

# Game loop

directionTick = 0.0
fpsLimit = 60
running = True
mouseDown = False
planet = "Earth"
normal = False

while running:
    clock.tick(fpsLimit)

    if planet == "Earth":
        gravitationalConstant = 9.81 * 10

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseDown = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouseDown = False

    screen.fill(white)

    # Ball

    moveTicker = 0

    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        if moveTicker == 0:
            moveTicker = 10
            ball.changeVelocity(-10, 0)
    if keys[K_RIGHT]:
        if moveTicker == 0:
            moveTicker = 10
            ball.changeVelocity(10, 0)
    if keys[K_UP]:
        if moveTicker == 0:
            moveTicker = 10
            ball.changeVelocity(0, -10)
    if keys[K_DOWN]:
        if moveTicker == 0:
            moveTicker = 10
            ball.changeVelocity(0, 10)
    
    # Update movement tick
    if moveTicker > 0:
        moveTicker -= 1
    
    ball.display()
    ball.move()
    ball.drag()
    if not normal:
        ball.gravity(gravitationalConstant)

    # Obstacles
    
    for obstacle in obstacles:
        r = pygame.Rect(*screen.get_rect().center, 0, 0).inflate(75, 75)
        collide = obstacle.rectangle.colliderect(r)
        
        if collide:
            ball.normalForce()
            ball.vy = 0
            normal = True

        obstacle.display()
    
    pygame.display.flip()

pygame.quit()
sys.exit()