#change sql password
#fix sql database creation
import pygame
import random

#from sqlmodule import *
'''
tablecreate()

gamestartinstructions()
suggestions()
'''
pygame.init() #initializing pygame window
pygame.mixer.init() #intializing pygame audio 

#windowsize
winwidth=640 #The width of the window
winheight=360 #The height of the windo
win = pygame.display.set_mode((winwidth, winheight)) #creating the window.
win2=pygame.display.set_mode((winwidth, winheight)) 
pygame.display.set_caption('Game')

#sprites
walkLeft=[pygame.image.load('L1.png'),pygame.image.load('L2.png'),pygame.image.load('L3.png'),pygame.image.load('L4.png'),pygame.image.load('L5.png'),pygame.image.load('L6.png'),pygame.image.load('L7.png'),pygame.image.load('L8.png'),pygame.image.load('L9.png'),pygame.image.load('L1.png')]
walkRight=[pygame.image.load('R1.png'),pygame.image.load('R2.png'),pygame.image.load('R3.png'),pygame.image.load('R4.png'),pygame.image.load('R5.png'),pygame.image.load('R6.png'),pygame.image.load('R7.png'),pygame.image.load('R8.png'),pygame.image.load('R9.png'),pygame.image.load('R1.png')]
char=pygame.image.load('standing.png')
bg=pygame.image.load('background.png')
clock=pygame.time.Clock()

#Sounds
pygame.mixer.music.load('Bg_music.mp3')
pygame.mixer.music.set_volume(0.4)
shootSound = pygame.mixer.Sound('shoot_sound.mp3')
enemyDyingSound = pygame.mixer.Sound('enemy_dying.mp3')



class player():
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.vel=5
        self.isJump=False
        self.jumpCount=10
        self.left= False
        self.right= False
        self.standing= True
        self.walkCount=0
        self.hitbox=(self.x+20,self.y,28,60)
        self.health=100
        self.score=0
        
    def draw(self,win):
        if self.walkCount+1>=27:
           self.walkCount=0
        if not(self.standing):
            if self.left:
                    win.blit(walkLeft[self.walkCount//3],(self.x,self.y))
                    self.walkCount+=1
            elif self.right:
                win.blit(walkRight[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1
        else:
            #to keep character faced left or right
            if self.right:
                win.blit(walkRight[0],(self.x,self.y))
            elif self.left:
                win.blit(walkLeft[0],(self.x,self.y))
                
            else:
                #change this
                win.blit(char,(self.x,self.y))
                #win.blit(walkLeft[0],(self.x,self.y))
        self.hitbox=(self.x+20,self.y,28,60)
        pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] -20,50,10))
        #to decrease the health bar
        pygame.draw.rect(win, (0,255,0), (self.hitbox[0], self.hitbox[1] -20,(50-0.5*(100-self.health)),10))
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
            
    def hit(self):
        if self.health>0:
            self.health-=1

    def healthfunc(self):
        if self.health>0 and self.health+20<=100:
            self.health+=20
        elif self.health+20>=100:
            self.health=105

class healthpack():
    def __init__(self,x,y,radius,color):
        self.x=x
        self.y=y
        self.radius=radius
        self.color=color
    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)
        
class projectile():
    def __init__(self,x,y,radius,color,facing):
        self.x=x
        self.y=y
        self.radius=radius
        self.color=color
        self.facing=facing
        self.vel=8*facing
    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)

class enemy():
    walkLeft=[pygame.image.load('L1E.png'),pygame.image.load('L2E.png'),pygame.image.load('L3E.png'),pygame.image.load('L4E.png'),pygame.image.load('L5E.png'),pygame.image.load('L6E.png'),pygame.image.load('L7E.png'),pygame.image.load('L8E.png'),pygame.image.load('L9E.png'),pygame.image.load('L1E.png')]
    walkRight=[pygame.image.load('R1E.png'),pygame.image.load('R2E.png'),pygame.image.load('R3E.png'),pygame.image.load('R4E.png'),pygame.image.load('R5E.png'),pygame.image.load('R6E.png'),pygame.image.load('R7E.png'),pygame.image.load('R8E.png'),pygame.image.load('R9E.png'),pygame.image.load('R1E.png')]
    def __init__(self,x,y,width,height,end):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.end=end
        self.path=[self.x,self.end]
        self.walkCount=0
        self.vel=random.randint(1,3)
        self.hitbox=(self.x+20,self.y,28,60)

    def draw(self,win):
        #self.move()
        self.move1()
        if self.walkCount+1>=27:
            self.walkCount=0
       #if enemy is left of player it will face right (towards the player) 
        if self.x<man.x:
            win.blit(self.walkRight[self.walkCount//3],(self.x,self.y))
            self.walkCount+=1
        else:
            win.blit(self.walkLeft[self.walkCount//3],(self.x,self.y))
            self.walkCount+=1
        self.hitbox=(self.x+20,self.y,28,60)

        
        #pygame.draw.rect(win,(255,0,0),(self.x,self.y,self.width,self.height),2)
    #used for movement of enemy(makes enemy follow player   
    def move(self):
        if self.vel>0:
            if self.x+self.vel<self.path[1]:
                self.x+=self.vel
            else:
                self.vel=self.vel*-1
                self.walkCount=0
        else:
            if self.x-self.vel>self.path[0]:
                self.x+=self.vel
            else:
                self.vel=self.vel*-1
                self.walkCount=0
    def move1(self):
        if man.x>self.x:
            self.x+=self.vel*.925
        elif man.x<self.x:
            self.x-=self.vel*.925
        if man.y<self.y:
            self.y-=self.vel*.925
        elif man.y>self.y:
            self.y+=self.vel*.925

    def hit(self):
        enemyDyingSound.play()
        #print('hit')
        man.score+=1
        #print(man.score)
                     
    
def redrawGameWindow():
    if man.health>0:
        win.blit(bg,(0,0)) 
        #pygame.draw.rect(win, (200,0,0),(x,y,width,height))
        man.draw(win)
        #enemy1.draw(win)
        
        for i in enemies:
            i.draw(win)
        for i in bullets:
            i.draw(win)
        for i in healthpacks:
            i.draw(win)
        pygame.display.update()
    else:
        win2.blit(bg,(0,0))
        # pygame.quit()

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def show_go_screen():
    draw_text(win, 'GAME', 60, winwidth/2, winheight/4 )
    draw_text(win, 'Use Arrow keys to move and space bar to shoot', 34, winwidth/2, winheight/2)
    draw_text(win, f'Press any key to continue', 15, winwidth/2, winheight * 3/4)
    waiting = True
    while waiting:
        clock.tick(27)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
        pygame.display.flip() 
run=True
game_over = True
#enemies=[enemy(random.randint(30,60),200,64,64,200),enemy(random.randint(30,60),100,64,64,200)]
#enemy1=enemy(60,110,64,64,200)

#delay before the game starts
pygame.time.delay(1000)

pygame.mixer.music.play(loops=-1)
while run:
    if game_over==True:
        show_go_screen()
        game_over = False
        enemies=[]
        bullets=[]
        healthpacks=[]
        man=player(70,100,64,64)
        man.score = 0


    # print(run)
    #controls frame rate (how fast the loop runs)
    clock.tick(27)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    if man.score<3:
        countofenemies=2
    elif man.score<7:
        countofenemies=3
    elif man.score<15:
        countofenemies=4
    else:
        countofenemies=5
    #colourrand=random.choice([(0,0,100),(100,0,0),(0,100,0),(50,50,0),(0,50,50),(50,0,50)])
    while len(healthpacks)<1:
        healthpacks.append(healthpack(random.randint(30,winwidth-50),random.randint(120,winheight-50),8,(0,0,100)))
    while len(enemies)<countofenemies:
        enemies.append(enemy(random.randint(30,winwidth),random.randint(120,winheight),64,64,200))
    for x in enemies:
        if man.hitbox[1]<x.hitbox[1]+x.hitbox[3] and man.hitbox[1]+man.hitbox[3]>x.hitbox[1]:
                if man.hitbox[0] +man.hitbox[2]>x.hitbox[0] and man.hitbox[0]<x.hitbox[0]+x.hitbox[2]:
                    man.hit()
    for i in healthpacks:
        if i.y+i.radius<man.hitbox[1]+man.hitbox[3] and i.y+i.radius>man.hitbox[1]:
            if i.x +i.radius>man.hitbox[0] and i.x-i.radius<man.hitbox[0]+man.hitbox[2]:
                man.healthfunc()
                #print("health")
                healthpacks.pop(healthpacks.index(i))
    for i in bullets:
        for x in enemies:
            #checks for collision within hitbox
            if i.y-i.radius<x.hitbox[1]+x.hitbox[3] and i.y+i.radius>x.hitbox[1]:
                if i.x +i.radius>x.hitbox[0] and i.x-i.radius<x.hitbox[0]+x.hitbox[2]:
                     x.hit()
                     enemies.pop(enemies.index(x))
                     if i in bullets:
                        bullets.pop(bullets.index(i))
        if i.x<winwidth and i.x>0:
            i.x+=i.vel
        else:
            bullets.pop(bullets.index(i))
    keys=pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        shootSound.play()
        if man.left:
            facing=-1
            #tomoveleft
        else:
            facing=1
            #shootright
        #restricts n.o of bullets
        if len(bullets)<1: 
            bullets.append(projectile(round(man.x+man.width//2),round(man.y+man.height//2),6,(100,0,0),facing))
              #we use x+y/2 to project bullet from center of man  
    if keys[pygame.K_LEFT] and man.x >man.vel:
        man.x-=man.vel
        man.left=True
        man.right=False
        man.standing=False
    elif keys[pygame.K_RIGHT] and man.x<winwidth-man.width-man.vel:
        man.x+=man.vel
        man.right=True
        man.left=False
        man.standing=False
    else:
        man.standing=True
        man.walkCount=0
    
    if not(man.isJump):
        if keys[pygame.K_UP] and man.y>man.vel:
            man.y-=man.vel
            man.right=False
            man.left=False
            man.standing=True
        if keys[pygame.K_DOWN] and man.y<winheight-man.height-man.vel:
            man.y+=man.vel
            man.standing=True
            man.right=False
            man.left=False
    if man.health<=0:
        game_over=True

    redrawGameWindow()


pygame.quit()

print('\n'*3)
print("Your score is ",man.score,"!!!")

'''
recordinsert(man.score)
mediadriven()
'''
