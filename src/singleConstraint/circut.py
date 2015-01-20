import pygame
import time
import numpy
import math

red = (255,0,0)
blue = (0,0,255)
black = (0,0,0)

'''
These are the queues for the processes
-1: no responce from associated process
INF: process is not competing for CS
t: timestamp of competing process
Q := Q1, Q2, Q3, Q4
'''
Q = numpy.zeros((4,4))

class Car(pygame.sprite.Sprite):
    width = 10       # my car width in px
    height = 10      # my car height in px
    state = -1      # the state of the car, helps in determining direction    
    Xadj = 16       # adjustment for viewing correctly
    Yadj = 44

    velocity = 1    # this demo is designed with this value being a factor of 2
    pos_x = Xadj + 0.0
    pos_y = Yadj + 0.0
   
    in_cs = False       # we assume we are not starting in the CS
    move = True         # if we are allowed to progress/keep driving
    req = False         # if we are requesting access to CS
    at_entrance = False # at entrance to CS
    at_exit = False     # at exit of CS


    def __init__(self, car_color, car_id):
        pygame.sprite.Sprite.__init__(self)
        
        self.car_id = car_id 
        self.image = pygame.Surface([self.width, self.height])  # init img of car
        self.image.fill(car_color)
        
        self.rect = self.image.get_rect()   # rect(where img is)
        
        # Get attributes for the height/width of the screen
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
        
    
    def update(self, v):
        global Q

        ''' coordinates of transitions '''
        x1 = 0
        x2 = 256
        x3 = 512
        x4 = 768
    
        y1 = 0
        y2 = 256
        y3 = 512
    
        A = self.Xadj    # pos adjustment : done so the code below is more concise
        B = self.Yadj

        self.velocity = v
        
        if self.move:
            ''' determine if we have a state update '''
            if self.pos_y == B+y1:
                if self.pos_x == A+x1 or self.pos_x == A+x2 or self.pos_x == A+x3 or self.pos_x == A+x4:
                    self.state += 1
            if self.pos_y == B+y2:
                if self.pos_x == A+x2 or self.pos_x == A+x3:
                    self.state += 1
            if self.pos_y == B+y3:
                if self.pos_x == A+x1 or self.pos_x == A+x2 or self.pos_x == A+x3 or self.pos_x == A+x4:
                    self.state += 1

        if self.state == 12:
            self.state = 0 

        ''' update pos by state and velocity '''
        if self.state == 0 or self.state == 2 or self.state == 4:
            x = 1
            y = 0
        if self.state == 1 or self.state == 5 or self.state == 9:
            x = 0
            y = 1
        if self.state == 3 or self.state == 7 or self.state == 11:
            x = 0
            y = -1
        if self.state == 6 or self.state == 8 or self.state == 10:
            x = -1
            y = 0
        

        ''' Evaluate where we are rel to CS '''
        if self.move and self.in_cs:
            if self.pos_y == B+y2:
                if self.pos_x == A+x2 or self.pos_x == A+x3:
                    self.at_exit = True
        if self.move and (not self.in_cs):
            if self.pos_y == B+y2:  
                if self.pos_x == A+x2 or self.pos_x == A+x3:
                    self.at_entrance = True
        
        ''' Message passing part '''
        if self.in_cs:
            self.move = True
            if self.at_exit:
                self.in_cs = False
                ''' signify we are out of the CS, no other ack at this time '''
                Q[0,self.car_id] = Q[1,self.car_id] = Q[2,self.car_id] = Q[3,self.car_id] = float(-1)
                self.at_exit = False
            
        if (not self.req) and (not self.in_cs) and (self.at_entrance):
            ''' We send out TS as a request to all other process' queues '''
            Q[0,self.car_id] = Q[1,self.car_id] = Q[2,self.car_id] = Q[3,self.car_id] = time.time()
            self.req = True
            self.move = False
            
        if self.req and (not self.in_cs):
            ''' do nothing until all other processes have responded to request '''
            if (Q[self.car_id, 0] > float(-1)) and (Q[self.car_id, 1] > float(-1)) and (Q[self.car_id, 2] > float(-1)) and (Q[self.car_id, 3] > float(-1)):
                if numpy.amin(Q[self.car_id]) == Q[self.car_id, self.car_id]:
                    self.in_cs = True
                    self.at_entrance = False
                    self.req = False

        if (not self.in_cs) and (not self.at_entrance) and (not self.at_exit):
            ''' respond to requests from other processes '''
            if Q[self.car_id, 0] > -1:            
                Q[0, self.car_id] = float('inf')
            
            if Q[self.car_id, 1] > -1:            
                Q[1, self.car_id] = float('inf')
            
            if Q[self.car_id, 2] > -1:            
                Q[2, self.car_id] = float('inf')
            
            if Q[self.car_id, 3] > -1:            
                Q[3, self.car_id] = float('inf')
        
    
        oldx = self.pos_x
        oldy = self.pos_y
        
        ''' This is where our movement happens '''
        if self.move:
            self.pos_x += self.velocity * x 
            self.pos_y += self.velocity * y
        
            ''' off road corrections '''
            if (oldx < A+x2) and (self.pos_x > A+x2):
                self.pos_x = A+x2
            if (oldx < A+x3) and (self.pos_x > A+x3):
                self.pos_x = A+x3
            if (self.pos_x > A+x4):
                self.pos_x = A+x4

            if (self.pos_x < A+x1):
                self.pos_x = A+x1
            if (oldx > A+x2) and (self.pos_x < A+x2):
                self.pos_x = A+x2
            if (oldx > A+x3) and (self.pos_x < A+x3):
                self.pos_x = A+x3

            if (self.pos_y < B+y1):
                self.pos_y = B+y1
            if (self.pos_y > B+y3):
                self.pos_y = B+y3
            if (oldy > B+y2) and (self.pos_y < B+y2):
                self.pos_y = B+y2
            if (oldy < B+y2) and (self.pos_y > B+y2):
                self.pos_y = B+y2

            self.rect.x = self.pos_x
            self.rect.y = self.pos_y 


''' Our display environment '''    
pygame.init()
screen = pygame.display.set_mode([800,600])
pygame.display.set_caption('critical bridge')
#background = pygame.Surface(screen.get_size())
background = pygame.image.load("bridge1.png").convert()   # load our background image

''' weird stuff stop '''


''' Init and organize our objects '''
cars = pygame.sprite.Group()    # create cars group
car1 = Car(red, 0)                    # create a car object
car2 = Car(red, 1)                    # create ... another car!
car3 = Car(blue, 2)
car4 = Car(blue, 3)
cars.add(car1)                   # add car to car group
cars.add(car2)
cars.add(car3)
cars.add(car4)
allsprites = pygame.sprite.Group()  # create an all sprites group
allsprites.add(car1)             # add car to all sprites group
allsprites.add(car2)
allsprites.add(car3)
allsprites.add(car4)


''' This is the heartbeat of the game '''
clock = pygame.time.Clock()
i = 0
maxItterations = 10000

a_velocity = 1
b_velocity = 2
c_velocity = 4
d_velocity = 8

while i < maxItterations:
    clock.tick(20)  #limit fps
    screen.fill(black)
    key = pygame.key.get_pressed()
    pygame.event.get()
    if key[pygame.K_ESCAPE]:
        i = maxItterations
    if key[pygame.K_q]:
        a_velocity *= 2
    if key[pygame.K_w]:
        b_velocity *= 2
    if key[pygame.K_e]:
        c_velocity *= 2
    if key[pygame.K_r]:
        d_velocity *= 2
    if key[pygame.K_a]:
        a_velocity = math.ceil(a_velocity / 2)
    if key[pygame.K_s]:
        b_velocity = math.ceil(b_velocity / 2)
    if key[pygame.K_d]:
        c_velocity = math.ceil(c_velocity / 2)
    if key[pygame.K_f]:
        d_velocity = math.ceil(d_velocity / 2)
        
    

    car1.update(a_velocity)      # update with a new velocity - must be a factor of 2
    car2.update(b_velocity)
    car3.update(c_velocity)
    car4.update(d_velocity)
    i += 1
    
    screen.blit(background, [0,0])  # known 'screen' variable.  blist 'draws' our background image each frame
    
    allsprites.draw(screen)
    pygame.display.flip()
     
pygame.quit()
