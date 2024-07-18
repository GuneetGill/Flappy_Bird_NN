import pygame
from defs import *
from pipe import PipeCollection
from bird import BirdCollection

#draws font on screen to display game time and time elasped
def update_label(data, title, font, x, y, gameDisplay):
    #render font with title and date with specfic color
    label = font.render('{} {}'.format(title, data), 1, DATA_FONT_COLOR)
    #draw at x and y position 
    gameDisplay.blit(label, (x, y))
    return y


def update_data_labels(gameDisplay, dt, game_time, num_itterations, num_alive ,font):
    y_pos = 10
    gap = 20
    x_pos = 10
    #update y pos
    y_pos = update_label(round(1000/dt,2), 'FPS', font, x_pos, y_pos + gap, gameDisplay)
    y_pos = update_label(round(game_time/1000,2),'Game time', font, x_pos, y_pos + gap, gameDisplay)
    y_pos = update_label(num_itterations, 'Iteration', font, x_pos, y_pos + gap, gameDisplay)
    y_pos = update_label(num_alive, 'Alive', font, x_pos, y_pos + gap, gameDisplay)


def run_game():

    #intilize pygame 
    pygame.init()
    #display pygame 
    gameDisplay = pygame.display.set_mode((DISPLAY_W,DISPLAY_H))
    #title of our window
    pygame.display.set_caption('Learn to fly')

    running = True
    #store our background image and store in varible 
    bgImg = pygame.image.load(BG_FILENAME)
    pipes = PipeCollection(gameDisplay)
    pipes.create_new_set()
    birds = BirdCollection(gameDisplay)
    
    #font that we can use 
    label_font = pygame.font.SysFont("monospace", DATA_FONT_SIZE)

    clock = pygame.time.Clock()
    dt = 0
    game_time = 0
    num_itterations = 1
    
    while running:

        #tick 30 times a second 
        dt = clock.tick(FPS)
        #keep track of game time 
        game_time += dt

        #draw our image where in x and y 
        gameDisplay.blit(bgImg, (0, 0))

        #if we want to quit exit while loop so user does keyboard shortcut to quit or keydown                    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                running = False

        
        pipes.update(dt)
        num_alive = birds.update(dt, pipes.pipes)

        if num_alive == 0:
            pipes.create_new_set()
            game_time = 0
            birds.evolve_population()
            num_itterations += 1

        update_data_labels(gameDisplay, dt, game_time, num_itterations,num_alive, label_font)
        #show us the screen 
        pygame.display.update()



if __name__== "__main__":
    run_game()
































