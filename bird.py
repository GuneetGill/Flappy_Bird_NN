import pygame
import random
from defs import *
from nnet import Nnet
import numpy as np

class Bird():

    def __init__(self, gameDisplay):
        #start off with bird
        self.gameDisplay = gameDisplay
        self.state = BIRD_ALIVE
        self.img = pygame.image.load(BIRD_FILENAME)
        self.rect = self.img.get_rect()
        self.speed = 0
        self.fitness = 0
        #how long bird has survived
        self.time_lived = 0
        #give neural net work 
        self.nnet = Nnet(NNET_INPUTS, NNET_HIDDEN, NNET_OUTPUTS)
        self.set_position(BIRD_START_X, BIRD_START_Y)
    
    #reset elements in the birds to starting state
    def reset(self):
        self.state = BIRD_ALIVE
        self.speed = 0
        self.fitness = 0
        self.time_lived = 0
        self.set_position(BIRD_START_X, BIRD_START_Y)

    #set position using rectangle
    def set_position(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y

    def move(self, dt):
        '''
        distance travelled is each time we move our bird how far has it travelled
        s = ut+1/2at^2
        
        new speed so constant acceleration, inital speed + accerlation times time
        v = u+at
        '''
        distance = 0
        new_speed = 0

        distance = (self.speed * dt) + (0.5 * GRAVITY * dt * dt)
        new_speed = self.speed + (GRAVITY * dt)

        #move it based on distance we calc and distance
        self.rect.centery += distance
        self.speed = new_speed

        #do not go top of screen
        if self.rect.top < 0:   
            self.rect.top = 0
            self.speed = 0

    def jump(self, pipes):
        inputs = self.get_inputs(pipes)
        val = self.nnet.get_max_value(inputs)
        if val > JUMP_CHANCE:
            self.speed = BIRD_START_SPEED

    def draw(self):
        self.gameDisplay.blit(self.img, self.rect)

    #if it goes off bottom of screen it has died 
    #if we have not hit bottom check if we hit any pipes
    def check_status(self, pipes):
        if self.rect.bottom > DISPLAY_H:
            self.state = BIRD_DEAD
        else:
            self.check_hits(pipes)
    
    #take in p the pipe we collided into
    def assign_collision_fitness(self, p):
        gap_y = 0
        #if pipe is upper use bottom of pipe to find where gap is 
        if p.pipe_type == PIPE_UPPER:
            gap_y = p.rect.bottom + PIPE_GAP_SIZE / 2
        else:
            gap_y = p.rect.top - PIPE_GAP_SIZE / 2

        self.fitness = -(abs(self.rect.centery - gap_y))

    #check if pipes rectangle overlaps our rectangle if it does bird has hit pipe
    def check_hits(self, pipes):
        for p in pipes:
            if p.rect.colliderect(self.rect):
                self.state = BIRD_DEAD
                self.assign_collision_fitness(p)
                break

    def update(self, dt, pipes):
        if self.state == BIRD_ALIVE:
            self.time_lived += dt
            self.move(dt)
            self.jump(pipes)
            self.draw()
            self.check_status(pipes)

    def get_inputs(self, pipes):

        #closest x position of nearest pipe
        closest = DISPLAY_W * 2 
        #y pos of pip
        bottom_y = 0  
        #loop thorugh all pipes and check for cloest pipes
        for p in pipes:
            #if the pipe is upper and its closer than cloest and it has not gone past us 
            if p.pipe_type == PIPE_UPPER and p.rect.right < closest and p.rect.right > self.rect.left:
                closest = p.rect.right
                bottom_y = p.rect.bottom

        #hoirztanl disnace to nearest pipe
        horizontal_distance = closest - self.rect.centerx
        #veritcal distance from our center to center of pipe gap
        vertical_distance = (self.rect.centery) - (bottom_y + PIPE_GAP_SIZE / 2)

        #normilze distances and make inputs array 
        inputs = [
            ((horizontal_distance / DISPLAY_W) * 0.99) + 0.01,
            ((( vertical_distance + Y_SHIFT) / NORMALIZER ) * 0.99 ) + 0.01
        ]

        return inputs
    
    def create_offspring(p1, p2, gameDisplay):
        #create new bird
        new_bird = Bird(gameDisplay)
        #create mixed weights from both parents 
        new_bird.nnet.create_mixed_weights(p1.nnet, p2.nnet)
        return new_bird


class BirdCollection():

    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.birds = [] #list of birds
        self.create_new_generation()

    #make new list of birds
    def create_new_generation(self):
        self.birds = []
        for i in range(0, GENERATION_SIZE):
            self.birds.append(Bird(self.gameDisplay))

    def update(self, dt, pipes):
        num_alive = 0
        #loop thorugh all birds
        for b in self.birds:
            b.update(dt, pipes)
            #check if its alive
            if b.state == BIRD_ALIVE:
                num_alive += 1

        return num_alive
    
    def evolve_population(self):
        #calculate fitness of bird
        #loop thorugh all birds
        for b in self.birds:
            #calc the fitness
            b.fitness += b.time_lived * PIPE_SPEED

        #sort in order of fitness 
        self.birds.sort(key=lambda x: x.fitness, reverse=True)

        #how many good birds we want to keep
        cut_off = int(len(self.birds) * MUTATION_CUT_OFF)
        #store good birds list 
        good_birds = self.birds[0:cut_off]
        #store other birds aka bad birds
        bad_birds = self.birds[cut_off:]
        #how many of bad birds we want to use in final bird list
        num_bad_to_take = int(len(self.birds) * MUTATION_BAD_TO_KEEP)

        #modify wieghts in our bad birds in all of them 
        for b in bad_birds:
            b.nnet.modify_weights()

        #final list of birds of new pop
        new_birds = []

        #index of bad birds to take get random indexs
        idx_bad_to_take = np.random.choice(np.arange(len(bad_birds)), num_bad_to_take, replace=False)

        for index in idx_bad_to_take:
            new_birds.append(bad_birds[index])

        #add good birds we want to keep in final list
        new_birds.extend(good_birds)

        #children we need
        children_needed = len(self.birds) - len(new_birds)

        #keep looping while length of new birds is less than self birds
        while len(new_birds) < len(self.birds):
            #randonmly select index from out list of two good birds for our parents
            idx_to_breed = np.random.choice(np.arange(len(good_birds)), 2, replace=False)
            #if indexs are not unique we do not want to breed bird with same bird
            #we manually create new bird
            if idx_to_breed[0] != idx_to_breed[1]:
                new_bird = Bird.create_offspring(good_birds[idx_to_breed[0]], good_birds[idx_to_breed[1]], self.gameDisplay)
                #add randomness to child and moidfy weights of this bird
                if random.random() < MUTATION_MODIFY_CHANCE_LIMIT:
                    new_bird.nnet.modify_weights()
                #add bird to new generaion of birds
                new_birds.append(new_bird)

        #reset all of old birds 
        for b in new_birds:
            b.reset()

        #keep new birds list
        self.birds = new_birds























