import pygame
import random
from defs import *


class Pipe():

    def __init__(self, gameDisplay, x, y, pipe_type):
        self.gameDisplay = gameDisplay
        #moving when we start
        self.state = PIPE_MOVING
        #is it upper or lower pipe
        self.pipe_type = pipe_type
        #image of pipe
        self.img = pygame.image.load(PIPE_FILENAME)
        #rectangle surrounding pipe
        self.rect = self.img.get_rect()
        if pipe_type == PIPE_UPPER:
            y = y-self.rect.height
        self.set_position(x, y)

    def set_position(self, x, y):
        #set image at certin spot on grid
        self.rect.left = x
        self.rect.top = y

    def move_position(self, dx, dy):
        #change in x and y
        self.rect.centerx += dx
        self.rect.centery += dy

    def draw(self):
        #draw onto game display
        self.gameDisplay.blit(self.img, self.rect)

    #have we move off of screen
    def check_status(self):
        if self.rect.right < 0:
            self.state = PIPE_DONE

    def update(self, dt):
        #if moving 
        if self.state == PIPE_MOVING:
            #negative means move to left
            self.move_position(-(PIPE_SPEED * dt), 0)
            self.draw()
            #have we gone off left hand side of screen?
            self.check_status()

#manage collection of pipes
class PipeCollection():

    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        #contain all current pipes on screen that are active
        self.pipes = []


    def add_new_pipe_pair(self, x):
        #y pos for upper and lower pipes
        #full range is pip max and pipe min 
        top_y = random.randint(PIPE_MIN, PIPE_MAX - PIPE_GAP_SIZE)
        bottom_y = top_y + PIPE_GAP_SIZE
        
        p1 = Pipe(self.gameDisplay, x, top_y, PIPE_UPPER)
        p2 = Pipe(self.gameDisplay, x, bottom_y, PIPE_LOWER)

        #add to our list
        self.pipes.append(p1)
        self.pipes.append(p2)

    #every time we start new game remove all old pipes
    def create_new_set(self):
        self.pipes = [] #reset list
        placed = PIPE_FIRST #now back at pip first

        while placed < DISPLAY_W:
            self.add_new_pipe_pair(placed)
            placed += PIPE_ADD_GAP

    def update(self, dt):
        #rightmost point of newest pair
        rightmost = 0

        for p in self.pipes:
            p.update(dt)
            if p.pipe_type == PIPE_UPPER:
                if p.rect.left > rightmost:
                    rightmost = p.rect.left

        if rightmost < (DISPLAY_W - PIPE_ADD_GAP):
            self.add_new_pipe_pair(DISPLAY_W)

        #focus on only pipes that are moving 
        self.pipes = [p for p in self.pipes if p.state == PIPE_MOVING]