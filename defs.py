#width and height of screen along with frames per second 
DISPLAY_W = 960
DISPLAY_H = 540
FPS = 30

#font size and color
DATA_FONT_SIZE = 18 
DATA_FONT_COLOR =  (40,40,40)
#background image
BG_FILENAME = './BG.png'

#acutal pip image
PIPE_FILENAME = './Pipe.png'
#speed pipe moves across screen
PIPE_SPEED = 70/1000
PIPE_DONE = 1
PIPE_MOVING = 0
PIPE_UPPER = 1
PIPE_LOWER = 0

PIPE_ADD_GAP = 160 #gap between pairs of pipes
#min and max for pipe 
PIPE_MIN = 80 
PIPE_MAX = 500
#start pos of new pipe 
PIPE_START_X = DISPLAY_W
#gap between upper and lower pipe
PIPE_GAP_SIZE = 160
#fist pair of pipes should be
PIPE_FIRST = 400

BIRD_FILENAME = './Robin.png'
#when we first jump 
BIRD_START_SPEED = -0.32
#start pos of bird
BIRD_START_X = 200
BIRD_START_Y = 200 
BIRD_ALIVE = 1
BIRD_DEAD = 0
#this pushes bird down if we do not flap
GRAVITY = 0.001

GENERATION_SIZE = 60 #each itteration has 60 new birds

'''
our neural net will be simple with 2 input nodes 5 nodes in the hidden layer and 1 output node
'''
NNET_INPUTS = 2
NNET_HIDDEN = 5
NNET_OUTPUTS = 1

#greater than 0.5 we flap
JUMP_CHANCE = 0.5

'''
what is the max range of y for the robin 
few cases we need to consider what if robin is at bottom of screen then the max y 
would be the display height of our page minus pipe min so top of the pip but also minus middle
of pipe gap divided by two so the bird can fit through
another case is the case where robin is at top of screen then pipe max so bottom pipe minus
middle of pipe gap
same for horizonital distance aka max is width of entire display
but we need to normalize these values as well after to get all postive values 
'''

MAX_Y_DIFF = DISPLAY_H - PIPE_MIN - PIPE_GAP_SIZE/2
MIN_Y_DIFF = PIPE_GAP_SIZE/2 - PIPE_MAX
Y_SHIFT = abs(MIN_Y_DIFF)
NORMALIZER = abs(MIN_Y_DIFF) + MAX_Y_DIFF

#probability we will modify a weight
MUTATION_WEIGHT_MODIFY_CHANCE = 0.2
#when we create offspring mix we make is 50%
MUTATION_ARRAY_MIX_PERC = 0.5


MUTATION_CUT_OFF = 0.4
#percentage of bad we keep
MUTATION_BAD_TO_KEEP = 0.2
MUTATION_MODIFY_CHANCE_LIMIT = 0.4