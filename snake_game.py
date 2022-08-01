import pygame
import random # for food
from enum import Enum
from collections import namedtuple # assigns meaning to positions in a tuple = readable + lighter
pygame.init() # init all modules

#MACROS
BLOCK_SIZE = 20 # constant for 1 block on screen
SPEED = 20 # speed of snake

#RGB tuple
WHITE = (255,255,255)
RED = (200,0,0)
BLUE1 = (0,0,255)
BLUE2 = (0,100,255)
BLACK = (0,0,0)

#pygame fonts
font1 = pygame.font.Font('arial.ttf', 25)

Point = namedtuple('Point', 'x,y') # lighter than class,'Point' is name of tuple, Point(x,y) access with Point.x, access the named tuple. 
# takes in a string, but variables seperated 

class Direction(Enum): #class inherit from enum
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class SnakeGame:
    # define init function, needs to be __init__ due to __name_
    def __init__(self, w = 640, h = 480): # display itself, default pixels width , height
        self.w = w
        self.h = h

        #init display, self.any is a new variable
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snakey')
        self.clock = pygame.time.Clock() # speed of game
        
        #init game state
        self.direction = Direction.RIGHT # snake initial direction to right

        #head of snake, starts middle of display
        self.head = Point(self.w / 2, self.h / 2) #stores the cords in a tuple named 'head' which can be accessed in next code
        
        #create snake body of 3 body size, list contains info of 
        self.snake = [  self.head, 
                        Point(self.head.x - BLOCK_SIZE, self.head.y), #head, snake set point abit left of the head of snake (mid), same y
                        Point(self.head.x - (2*BLOCK_SIZE), self.head.y)]  # set 3rd part of body 2 times left of head

        self.score = 0
        self.food = None
        self.place_food() 

    def place_food(self): # gets only self, placed randomly inside our dimensions
        x = random.randint(0, (self.w - BLOCK_SIZE)//BLOCK_SIZE ) * BLOCK_SIZE # x=random int from 0 and [width - blocksize] (so food is in block)
        y = random.randint(0, (self.h - BLOCK_SIZE)//BLOCK_SIZE ) * BLOCK_SIZE
    #in order to get only block size multiples so food inside a block use trick:the width/height divide by blocksize then * by blocksize get 
    #back a random int of a multiple of only block sizes
        self.food =  Point(x,y) #sets food position from this function in a tuple, access by self.food.x or y
        if self.food in self.snake: #dont place food in snake, checks if in self.snake list with 3 cords on the body
            self.place_food() # new random cords

    def play_step(self):
        #1 collect user input
        for event in pygame.event.get(): # gets all user events
            if event.type == pygame.QUIT:
                pygame.quit()
                quit() # python prog

            if event.type == pygame.KEYDOWN: # press a key
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT: #else if
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN      

        #2 move snake 
        self._move(self.direction) # updates new snake head position
        self.snake.insert(0, self.head) #transfer new position into the self.snake list, at index 0 = head
        # this inserts a new block at front of the head, when we use pop below to remove it at the end of snake keeps its size

        #3 check gameover, boundary or into itself
        game_over = False
        if self.Is_collision():
            game_over = True
            return game_over, self.score #immediate return
        
        #4 place new food (when got) or just moving (when move 1 block, we created new one, so just remove last one by pop)
        if self.head == self.food: # if collide
            self.score += 1
            self.place_food()
        else:
            self.snake.pop() # removes last element of snake
        
        #5 update ui (snake + background) + clock
        self.update_ui() 
        self.clock.tick(SPEED) # how fast frame updates

        #6 return gameover + score
        return game_over, self.score  

    def Is_collision(self):
        #hits boundary
        if (self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 # hit left or right width wise
        or self.head.y > self.h - BLOCK_SIZE or self.head.y <0):
            return True # yes collision

        #hits itself (rest of list not head at index 0)
        if self.head in self.snake[1:]: #if head in other body parts so not index 0 
            return True

        return False # no collision    

    def update_ui(self):
        self.display.fill(BLACK) #fill screen with black

        #draw snake
        for pt in self.snake: #iterate over all points of snake body (points of body in its list)
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))#draw on display, blue, rectangle snake
            #set position of rect to self.snake tuple's x + y cords, size of rect (w x h)
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12)) # draw innards of snake at same postion of body

        #draw food
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        #score text
        text_score = font1.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text_score, [0,0]) # upper left
        pygame.display.flip() # updates full display

    def _move(self, direction): # gets self + dir class 
        x = self.head.x #get original x + y position
        y = self.head.y

        if direction == Direction.RIGHT:
            x += BLOCK_SIZE # move right by a block
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE 
        elif direction == Direction.UP:
            y -= BLOCK_SIZE 
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE # pixel 0 at top, increases downwards
        
        self.head = Point(x,y) #head now a new pos

if __name__ == '__main__': # if run as main process
    game = SnakeGame() #create snake game 

    #game loop endless
    while True:
        play_game_over, game_score = game.play_step() # executing func returns gameover + score 

        if play_game_over == True:
            break #exits loop to quit

    print('Final score', game_score)
    pygame.quit()

