import os, sys, math, pygame, pygame.mixer
from pygame.locals import *

# Settings

black = 0,0,0
white = 255,255,255
red = 255,0,0
green = 0,255,0
blue = 0,0,255

screenSize = screenWidth, screenHeight = 600, 400
mouseDown = False

planet = "Earth"

screen = pygame.display.set_mode(screenSize)
clock = pygame.time.Clock()
pygame.display.set_caption('2D Physics Simulator')

# Text

global font
pygame.font.init()
font = pygame.font.SysFont('arial',20)

def write(text, location, color=black):
    screen.blit(font.render(text, True, color), location)

# Classes

class Ball:
    def __init__(self, size, color, mass, x = 200, y = 100, width = 2, vx = 0, vy = 0, Fnetx = 0, Fnety = 0):
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
        write(f"Vx: {round(self.vx/10, 2)}m/s", (5,0))
        write(f"Vy: {round(-self.vy/10, 2)}m/s", (5,20))
    
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
            self.vx = 0
            self.vy = 0
            cursor = pygame.mouse.get_pos()
            self.x = cursor[0]
            self.y = cursor[1]

    def addForce(self, Fx, Fy):
        self.Fnetx += Fx
        self.Fnety += Fy
    
    def gravity(self, g):
        self.g = g
        self.addForce(0, self.mass*g)
        write(f"Gravity: {self.g/10}m/s^2", (5,40))
    
    def normalForce(self):
        self.addForce(0, -self.Fnety)
        print(self.Fnety)
        print(self.vy)
    
    def kineticEnergy(self):
        self.Ek = 0.5 * self.mass * (self.vy ** 2)
        write(f"Kinetic energy: {round(self.Ek/10, 2)}N", (5,60))
    
    def potentialEnergy(self, g):
        self.Ep = self.mass * g * (screenHeight - self.y)
        write(f"Potential energy: {round(self.Ep/10, 2)}N", (5,80))
    
    def findMomentum(self):
        self.momentum = self.mass * math.sqrt(self.vx**2 + self.vy**2)
        write(f"Momentum: {round((self.momentum)/10, 2)}kg*m/s", (5,100))
    
    def bounce(self, absorption):
        if self.x <= self.size:
            self.x = 2*self.size - self.x
            self.vx = self.vx/2 * -absorption
        elif self.x >= screenWidth - self.size:
            self.x = 2*(screenWidth - self.size) - self.x
            self.vx = self.vx/2 * -absorption
        if self.y <= self.size:
            self.y = 2*self.size - self.y
            self.vy = self.vy/2 * -absorption
        elif self.y >= screenHeight - self.size:
            self.y = 2*(screenHeight - self.size) - self.y
            self.vy = self.vy * -absorption


# Objects
ball = Ball(20, red, 0.5)

# Buttons

class Button:
    def __init__(self, x, y, l, h, color, text, action):
        self.x = x
        self.y = y
        self.l = l
        self.h = h
        self.rectangle = pygame.Rect(x, y, l, h)
        self.color = color
        self.text = text
        self.action = action
        self.pressed = False

    def display(self):
        pygame.draw.rect(screen, self.color, self.rectangle)
        write(self.text, (self.x+5, self.y+5))
    
    def checkPress(self):
        cursor = pygame.mouse.get_pos()
        if self.x <= cursor[0] <= self.x + self.l and self.y <= cursor[1] <= self.y + self.h:
            if mouseDown:
                if self.action == "RESET":
                    ball.x = 200
                    ball.y = 100
                    ball.vx = 0
                    ball.vy = 0
                    ball.Fnetx = 0
                    ball.Fnety = 0

                if self.action == "CHANGE PLANET" and not self.pressed:
                    ball.x = 200
                    ball.y = 100
                    ball.vx = 0
                    ball.vy = 0
                    ball.Fnetx = 0
                    ball.Fnety = 0
                    self.pressed = True
                    global planet
                    if planet == "Earth":
                        planet = "Mars"
                        self.text = "Mars"
                    elif planet == "Mars":
                        planet = "Moon"
                        self.text = "Moon"
                    elif planet == "Moon":
                        planet = "Jupiter"
                        self.text = "Jupiter"
                    elif planet == "Jupiter":
                        planet = "Sun"
                        self.text = "Sun"
                    elif planet == "Sun":
                        planet = "Earth"
                        self.text = "Earth"
            else:
                self.pressed = False

                

reset = Button(500, 300, 60, 30, red, "Reset", "RESET")
changePlanet = Button(500, 350, 60, 30, green, "Earth", "CHANGE PLANET")

# Game loop

directionTick = 0.0
fpsLimit = 60
running = True

while running:
    clock.tick(fpsLimit)

    if planet == "Earth":
        gravitationalConstant = 9.81 * 10
    elif planet == "Mars":
        gravitationalConstant = 3.73 * 10
    elif planet == "Moon":
        gravitationalConstant = 1.62 * 10
    elif planet == "Jupiter":
        gravitationalConstant = 24.8 * 10
    elif planet == "Sun":
        gravitationalConstant = 274 * 10

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
    
    # Update movement tick
    if moveTicker > 0:
        moveTicker -= 1
    
    ball.display()
    ball.move()
    ball.drag()
    bounceAmount = 0.8 - (ball.mass*0.1 + gravitationalConstant/1000)
    if bounceAmount < 0:
        bounceAmount= 0
    ball.bounce(bounceAmount)
    ball.gravity(gravitationalConstant)
    ball.kineticEnergy()
    ball.potentialEnergy(gravitationalConstant)
    ball.findMomentum()

    # Display buttons

    reset.display()
    reset.checkPress()

    changePlanet.display()
    changePlanet.checkPress()
    
    pygame.display.flip()

pygame.quit()
sys.exit()