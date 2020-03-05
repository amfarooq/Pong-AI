# Ali Farooqui
# Single Player Pong AI

import pygame
import numpy
import random
import time

#colors
BLACK = (0,0,0)
GREEN = (0,255,0)
WHITE = (255,255,255)
RED = (255,0,0)

buttonMessage1 = 'Click here to speed up'
buttonMessage2 = 'Click here to show game'

#initialize pygame
pygame.init()

#Initialize the game screen
size = (800,600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong AI")

# bool used to decide whether the screen should be displaying the game
printgame = True

#Starting coordinates of the paddle
rect_x = 400 #left side starts at 400 on X axis
rect_y = 580 #top side starts at 580 on Y axis
width = 100 #paddle width
height = 20 #paddle height

#Declare the paddle variable
paddle = pygame.Rect(rect_x, rect_y, width, height)

#initial position of the ball
ball_x = 50
ball_y = 50

#The change in X and Y axis whenever the ball moves
ball_change_x = 5
ball_change_y = 5

# Creats a Q-table to store an arbitrary number of states in the columns, each corresponding to its
# three actions(stay = 0, left = 1, right = 0) in the rows
QStates = numpy.zeros([25000, 3]) #Initialize our Q table

score = 0 #keeps track of current score
total = 0 #keeps track of total score
highscore = 0 #keeps track of highest score reached
average = 0 #keeps track of average score of all games played
averageTwenty = 0 #keeps track of average score of the last twenty games
scoreList = [] #list that holds scores of the last 20 games, most recent score at the beginning
numberofgame = 0 #count for number of games played
index = {} #index that represents states as integer values so they can be easily referred to

#alpha is learning rate. y is gamma, or the discount rate
alpha = 0.9
y = 0.5

i = 0

# calculates the reward value for a state (a state includes position of the paddle, and position of the ball)
def evaluateReward(paddle, ball):
    
    # if the ball is at the bottom of the screen
    if ball.y == 565:
        if paddle.left <= ball.x <= paddle.right: # if the ball makes contact with the paddle
            return 1 # reward 1 point
        else: # if it doesn't
            return -1 # the paddle has missed the ball, game is over. Negative reward of -1

    else : # ball is anywhere else on the screen, no reward earned. return 0 points
        return 0

# This class represents a state. A state includes position of the paddle and the position of the ball
class State:
    def __init__(self, paddle, ball):
        self.paddle = paddle
        self.ball = ball

# This class represents the position of the ball, with x being the x coordinate and y being the y coordinate
class Ball:
    def __init__(self, ball_x, ball_y):
        self.x = ball_x
        self.y = ball_y

# gives a state an integer value, so it can be stored in and/or accessed from our index
def convert(s):
    y = int(s.ball.y)
    x = int(s.ball.x)
    z = int(s.paddle.left)
    n = float(str(x) + str(z))

    if n in index:
        return index[n]
    else:
        if len(index):
            maximum = max(index, key=index.get) #value the location of max value in index
            index[n] = index[maximum] + 1
        else:
            index[n] = 1
    return index[n]

# returns the best action
def bestAction(s): 
    return numpy.argmax(QStates[convert(s), :])

def newStartForBall():
    x = 100 - 15
    change = random.randint(1,8)
    x = x * change
    return x

# update position of the paddle based on what action we took
def updatePaddle(paddle, act):
    if act == 2:
        if paddle.right + 50 > 800:
            return paddle
        else:
            return pygame.Rect(paddle.left + 50, paddle.top, paddle.width, paddle.height)
    elif act == 1:
        if paddle.left - 50 < 0:
            return paddle
        else:
            return pygame.Rect(paddle.left - 50, paddle.top, paddle.width, paddle.height)
    else:
        return paddle

# Get the new state after we have made an action
def postActionState(s, act):
    newPaddle = updatePaddle(s.paddle, act)
    X = s.ball.x + ball_change_x
    Y = s.ball.y + ball_change_y
    newBall = Ball(X,Y)

    return State(newPaddle, newBall)

#Button class for creating button with all its properties
class button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
    
    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
        
        pygame.draw.rect(screen, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('Times New Roman', 20)
            text = font.render(self.text, 1, (0,0,0))
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
    #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

def PrintScreen(screen, score, highscore, count, printgame, DisplayButton, paddle, ball):
    DisplayButton.draw(screen, (0,0,0))
    roundoff = round(average,2)
    roundoff2 = round(averageTwenty,2)
    #score board
    font= pygame.font.SysFont('Times New Roman', 20, False, False)
    font2 = pygame.font.SysFont('Times New Roman', 40, False, False)
    text = font.render("High Score = " + str(highscore), True, WHITE)
    text_rect = text.get_rect(center=(size[0]/2, 40))
    text2 = font.render("Average Score = " + str(roundoff), True, WHITE)
    text3 = font.render("20 Game Average = " + str(roundoff2), True, WHITE)
    text4 = font.render("Current game # " + str(count), True, WHITE)
    screen.blit(text,text_rect)
    screen.blit(text2,[600,30])
    screen.blit(text3, [600,50])
    screen.blit(text4, [50,30])

    if printgame == False:
        text5 = font2.render("Games are being played. AI is learning", True, WHITE)
        text_rect2 = text5.get_rect(center=(size[0]/2, size[1]/2))
        screen.blit(text5, text_rect2)
    else:
        pygame.draw.rect(screen,WHITE,ball)
        pygame.draw.rect(screen, RED, paddle)
        text1 = font.render("Current Score = " + str(score), True, WHITE)
        screen.blit(text1,[50,50])

    pygame.display.update()
    
    return


#####
#####
#####
## main function begins here
clock=pygame.time.Clock()
count = 1
DisplayButton = button(GREEN, 590, 70, 200, 25, buttonMessage1)

while True:
    # getting position of the mouse
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            numpy.savetxt('QTable.txt', QStates)
            pygame.quit()
            sys.exit()
        
        # what to do if button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN and DisplayButton.isOver(mouse):
            if printgame == True:
                printgame = False
                DisplayButton.text = buttonMessage2
                
            else:
                printgame = True
                DisplayButton.text = buttonMessage1

    screen.fill(BLACK)


    ####
    ####
    ## This is how we update the position of the ball
    if ball_x>785:
        ball_change_x = ball_change_x * -1 
        ball_x=785

    elif ball_x < 15:
        ball_x += ball_change_x
        ball_change_x = abs(ball_change_x)

    else:
        ball_x += ball_change_x

    #high score
    if score > highscore:
        highscore = score
        if printgame == False:
            PrintScreen(screen, score, highscore, count, printgame, DisplayButton, paddle, [ball_x,ball_y,15,15])


    # if ball is at the bottom of the screen
    if ball_y>=565:

        # if ball has made contact with the paddle
        if ball_x>=paddle.left and ball_x<=paddle.right:
            ball_change_y = ball_change_y * -1
            ball_y += ball_change_y
            score = score + 1 #update score
            
        else: # ball hit the ground, and game restarts
            ball_x = newStartForBall()
            ball_y = 50
            
            # calculate average score for the last 20 games
            scoreList.insert(0,score)
            if len(scoreList) > 20:
                scoreList.pop()
            averageTwenty = float(sum(scoreList) / len(scoreList))

            #calculate average score for the whole game 
            total = total + score
            numberofgame = numberofgame + 1
            average = float(total / numberofgame)
            

            #reset score to zero after game restarts
            count = count + 1
            score = 0
            
            if printgame == False:
                PrintScreen(screen, score, highscore, count, printgame, DisplayButton, paddle, [ball_x,ball_y,15,15])

            
    elif ball_y < 15:
        ball_y += ball_change_y
        ball_change_y = abs(ball_change_y)

    else:
        ball_y += ball_change_y
    ####
    ####


    s = State(paddle, Ball(ball_x, ball_y))
    a = bestAction(s)
    r = evaluateReward(s.paddle, s.ball)
    s1 = postActionState(s,a)
    a1 = bestAction(s1)

    #Applying Bellman's equation for Q learning to update an existing state-action pair
    QStates[convert(s), a] += alpha*(r + y * numpy.max(QStates[convert(s1), :]) - QStates[convert(s), a])


    paddle = updatePaddle(s.paddle, a)

    if printgame == True:
        PrintScreen(screen, score, highscore, count, printgame, DisplayButton, paddle, [ball_x,ball_y,15,15])



pygame.quit()
