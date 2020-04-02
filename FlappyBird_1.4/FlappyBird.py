import pygame
import random 
import time

pygame.init()
pygame.mixer.init()

black = (0,0,0)
white = (225,225,225)
red = (255,0,0)
green = (0,255,0)
light_green = (102,255,102)
light_red = (255,51,51)
blue = (0,0,255)

display_widht = 800
display_height = 600

pipe_widht = 136
pipe_height = 500

gamedisplay = pygame.display.set_mode((display_widht,display_height))
pygame.display.set_caption("FlappyBird")
clock = pygame.time.Clock()

birdimg = pygame.image.load("pictures\Bird.png")
birdUp = pygame.image.load("pictures\BirdUp.png")
birdDown = pygame.image.load("pictures\BirdDown.png")
pipDown = pygame.image.load("pictures\pipeDown.png")
pipeUp = pygame.image.load("pictures\pipeUp.png")
background = pygame.image.load("pictures\Background.png").convert()

flapp = pygame.mixer.Sound("Sounds/flaps.ogg")
pling = pygame.mixer.Sound("Sounds/pling.ogg")
gameover_sound = pygame.mixer.Sound("Sounds/gameover.ogg")

pygame.display.set_icon(pipDown)

highscore_path = "highscore.txt"

f = open(highscore_path, "a")
f.close()

def text_objects(text, font,color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def random_color():
    while True:
        color =(random.randint(0,225),random.randint(0,225),random.randint(0,225))
        if color == black or color == white:
            continue
        else:
            break
    return color

def pipe(x,y):
    global pipeDown_x
    global pipeDown_y
    global pipeUp_x
    global pipeUp_y
    pipeDown_x = x
    pipeDown_y = y
    pipeUp_x = x
    pipeUp_y = y - 150 - pipe_height
    gamedisplay.blit(pipDown, (pipeDown_x,pipeDown_y))
    gamedisplay.blit(pipeUp, (pipeUp_x,pipeUp_y))

def message_display(text,pos,size,color):
    largeText = pygame.font.Font('freesansbold.ttf',size)
    TextSurf, TextRect = text_objects(text, largeText,color)
    TextRect.center = ((display_widht/2),(pos))
    gamedisplay.blit(TextSurf, TextRect)

    #pygame.display.update()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gamedisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(gamedisplay, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText,black)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gamedisplay.blit(textSurf, textRect)

def Quit():
    pygame.QUIT()
    quit()

def bird(x,y,sprite):
    gamedisplay.blit(sprite, (x,y))

def Background(x):
    gamedisplay.blit(background, [x,0])

def start_menu():
    background_x = 0
    f = open(highscore_path, "r")
    highscore = f.read()
    f.close()
    while True:
        if background_x + 2400 < display_widht:
            background_x = -5
        else:
            background_x += -5
        gamedisplay.fill(white)
        Background(background_x)
        bird(200,300,birdimg)
        message_display("Press space to start",420,50,black)
        message_display("Highscore:" + str(highscore), 500, 50,black)
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_SPACE:
                    game_loop()
        pygame.display.update()
        clock.tick(60)
def lost(poeng,x,y,pipe_x,pipe_y,hitpipe,background_x):
    gameover_sound.play()
    counter = 0
    if hitpipe:
        flaks = 1
        while True:
            gamedisplay.fill(white)
            if flaks > 0:
                flaks -= 1
                y_change = -5

            y += y_change
            Background(background_x)
            pipe(pipe_x,pipe_y)
            
            if y_change < 0:
                bird(x,y,birdUp)
            elif y_change > -1 and y_change < 1:
                bird(x,y,birdimg)
            elif y_change > 1:
                bird(x,y,birdDown)

            y_change += 0.2

            if y > display_height - 40:
                break

            pygame.display.update()
            clock.tick(60)

    f = open(highscore_path, "r")
    highscore = f.read()
    f.close()
    if poeng > int(highscore):
        highscore = poeng
        f = open(highscore_path, "w")
        f.write(str(highscore))
        f.close()
        message_display("Game over",display_height/4,100,black)
        message_display("NEW HIGHSCORE!",display_height/2,50,random_color())
        message_display(str(poeng), 400, 50,black)
        pygame.display.update()
        time.sleep(0.5)
        pygame.event.clear()
        while True:
            counter += 1
            message_display("Game over",display_height/4,100,black)
            message_display("NEW HIGHSCORE!",display_height/2,50,random_color())
            message_display(str(poeng), 400, 50,black)
            if counter == 5:
                pygame.display.update()
                counter = 0
            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                    else:
                        game_loop()
    else:
        message_display("Game over",display_height/4,100,black)
        message_display("Score:"+ str(poeng),display_height/2,50,black)
        message_display("Highscore:" + str(highscore), 450, 50,black)
        pygame.display.update()
        time.sleep(0.5)
        pygame.event.clear()
        while True:
            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                    else:
                        game_loop()

def game_loop():
    y = (300)
    x = (200)
    pipe_x = 600
    pipe_y = random.randint(200,display_height - 200)

    bird_height = 40
    bird_width = 48

    hei = 0

    poeng = 0
    level_change = 10
    
    speed = -5

    flaks = 0

    background_x = 0

    y_change = 0
    crashed = False
    hited = False
    pressed = False
    passed = False

    while not crashed:
        if y > display_height - bird_height:
            lost(poeng,x,y,pipe_x,pipe_y,False,background_x)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_SPACE:
                    flapp.play() 
                    if y < 0:
                        y += 10
                    else:
                        flaks += 1
                        pressed = True
        if flaks > 0:
            flaks -= 1
            y_change = -5
        
        if x + bird_width > pipe_x and x < pipe_x + pipe_widht:
            if y + bird_height > pipeDown_y and y < pipeDown_y + pipe_height:
                str(poeng)
                lost(poeng,x,y,pipe_x,pipe_y,True,background_x)
            if y < pipeUp_y + pipe_height:
                str(poeng)
                lost(poeng,x,y,pipe_x,pipe_y,True,background_x)
            elif not passed:
                pling.play()
                poeng += 1
                passed = True

        if poeng >= level_change:
            speed -= 1
            level_change += 10
                



        if pipe_x + pipe_widht < 0:
            pipe_x = 800
            pipe_y = pipe_y = random.randint(200,display_height - 200)
            passed = False
        
        pipe_x += speed
        y += y_change

        gamedisplay.fill(white)
        if background_x + 2400 < display_widht:
            background_x = -5
        else:
            background_x += speed
        Background(background_x)
        pipe(pipe_x,pipe_y)
        if y_change < 0:
            bird(x,y,birdUp)
        elif y_change > -1 and y_change < 1:
            bird(x,y,birdimg)
        elif y_change > 1:
            bird(x,y,birdDown)
        message_display(str(poeng), 30, 50,black)
        y_change += 0.2
        pygame.display.update()
        clock.tick(60)


start_menu()
pygame.quit()
quit()