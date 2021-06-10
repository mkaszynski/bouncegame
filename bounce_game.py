import pygame
import pygame.locals as pg_locals
import random
import time as t

WELCOME_TXT = 'Hello! Welcome to bounce game! Press a to go left, press d to go right, press w to jump, press e to make the floor bouncier, press r to make it less bouncier, press z and x to control gravity, press f and f to control frition, press c and v to control the size of the person, and press q to quit.  Press enter to start.'

def wrap_text(text, font, colour, x, y, screen, allowed_width):
    # first, split the text into words
    words = text.split()

    # now, construct lines out of these words
    lines = []
    while len(words) > 0:
        # get as many words as will fit within allowed_width
        line_words = []
        while len(words) > 0:
            line_words.append(words.pop(0))
            fw, fh = font.size(' '.join(line_words + words[:1]))
            if fw > allowed_width:
                break

        # add a line consisting of those words
        line = ' '.join(line_words)
        lines.append(line)

    # now we've split our text into lines that fit into the width, actually
    # render them

    # we'll render each line below the last, so we need to keep track of
    # the culmative height of the lines we've rendered so far
    y_offset = 0
    for line in lines:
        fw, fh = font.size(line)

        # (tx, ty) is the top-left of the font surface
        tx = x
        ty = y + y_offset
        y_offset += fh

        font_surface = font.render(line, True, colour)
        screen.blit(font_surface, (tx, ty))


def rand_color():
    return (random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255))


def add_line(screen, text, x, y):
    # used to print the status of the variables
    text = font.render(text, True, white) 
    text_rect = text.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text, text_rect)


# these are used when inputting colors into pygame
black = (0, 0, 0)
white = (255, 255, 255)

TICKS = 60
vel_y = 0

GRAVITY = -3
ANTIGRAVITY = 3
red = 0
green = 0
blue = 0

pygame.init()
font = pygame.font.Font('freesansbold.ttf', 32)


# set the screen size
full_screen = True
if full_screen:
    info = pygame.display.Info()
    SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h - 65
else:
    SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600

screen = pygame.display.set_mode((0, 0))


HEIGHT = 40
GROUND_Y = SCREEN_HEIGHT - HEIGHT

pos_x = 0.5 * SCREEN_WIDTH
pos_y = GROUND_Y

my_color = (255, 0, 0)
bounce = 0.1
gravity = 1
friction = 0.1
jump = 20

vel_x = 0
vel_y = 0
# use this clock to limit the update of the game
clock = pygame.time.Clock()

unn = True
while unn:
    screen.fill((120, 0, 170))# make entire screen black
    add_line(screen, 'Kaszynski studios',
                     550, 250)
    pygame.event.poll()
    pygame.display.update()
    t.sleep(2)
    clock.tick(TICKS)
    unn = False

first_time = True
running = True
while running:
    screen.fill((red, green, blue))  # make entire screen black
    
    # display welcome text
    if first_time:
        
        wrap_text(WELCOME_TXT, font, 'white', 400, 200, screen,
                  SCREEN_WIDTH // 2)

        pygame.event.poll()
        keys = pygame.key.get_pressed()
        pygame.display.update()

        if keys[pg_locals.K_RETURN]:
            first_time = False
        
        continue        

    pygame.display.set_caption('bounce game')

    GROUND_Y = SCREEN_HEIGHT - HEIGHT
    on_ground = pos_y == GROUND_Y

    # update events
    pygame.event.poll()

    keys = pygame.key.get_pressed()
    
    if True:
        if keys[pg_locals.K_d]:
            vel_x = 10
        if keys[pg_locals.K_a]:
            vel_x = -10
    
        # simulate drag
        vel_x -= friction *vel_x
        if abs(vel_x) < 0.5:
            vel_x = 0
        
    # controls size of person
    if keys[pg_locals.K_c]:
        HEIGHT = HEIGHT + 1
    if keys[pg_locals.K_v]:
        HEIGHT = HEIGHT - 1
    if HEIGHT < 1:
        HEIGHT = 1
    if HEIGHT > 400:
        HEIGHT = 400
    
    # control bouncing
    if keys[pg_locals.K_e]:
        bounce = bounce + 0.01
    if keys[pg_locals.K_r]:
        bounce = bounce - 0.01
    if bounce < 0.1:
        bounce = 0.1
    if bounce > 0.9:
        bounce = 0.9
        
    # controls screen color
    if keys[pg_locals.K_u]:
        red = red + 1
    if keys[pg_locals.K_j]:
        red = red - 1
    if keys[pg_locals.K_i]:
        green = green + 1
    if keys[pg_locals.K_k]:
        green = green - 1
    if keys[pg_locals.K_o]:
        blue = blue + 1
    if keys[pg_locals.K_l]:
        blue = blue - 1
    if blue < 0:
        blue = 0
    if red < 0:
        red = 0
    if green < 0:
        green = 0
    if blue > 255:
        blue = 255
    if green > 255:
        green = 255
    if red > 255:
        red = 255
        
    # control gravity
    if keys[pg_locals.K_z]:
        gravity = gravity + 0.1
    if keys[pg_locals.K_x]:
        gravity = gravity - 0.1
    if gravity < -20:
        gravity = -20
    if gravity > 20:
        gravity = 20
    
    # controls jump height
    if keys[pg_locals.K_t]:
        jump = jump + 0.1
    if keys[pg_locals.K_y]:
        jump = jump - 0.1
    if jump < 1:
        jump = 1
    if jump > 100:
        jump = 100
    
    # control fricton
    if keys[pg_locals.K_f]:
        friction = friction + 0.01
    if keys[pg_locals.K_g]:
        friction = friction - 0.01
    if friction > 0.5:
        friction = 0.5
    if friction < 0:
        friction = 0

    pos_x += vel_x

    # bounds checking
    if pos_x < 0:
        pos_x = 0
        vel_x = vel_x * -1
        my_color = rand_color()
    if pos_x > SCREEN_WIDTH - HEIGHT:
        pos_x = SCREEN_WIDTH - HEIGHT
        vel_x = vel_x * -1
        my_color = rand_color()
    
    if keys[pg_locals.K_q]:
        running = False
    if keys[pg_locals.K_w]:
        if pos_y == GROUND_Y:
            vel_y -= jump
    
    # jumps of roof
    if keys[pg_locals.K_s]:
        if pos_y == 0:
            vel_y += jump
    
    # falls to the roof
    if gravity < 0:
        vel_y -= 1
        
    
    # update position using velocity
    pos_y += vel_y
    
    # slowly return to 0
    vel_y += gravity
    
    if pos_y < 0:
        pos_y = 0
        vel_y *= bounce * -1  # make bounce
        my_color = rand_color()
    if pos_y > GROUND_Y:
        pos_y = GROUND_Y
        # must reset velocity as well
        vel_y *= bounce * -1  # make bounce
        my_color = rand_color()
    
    # simulate drag
    if abs(vel_y) < 3.0:
        vel_y = 3.0

    # print out the current variables
    add_line(screen, f'Friction (g or f): {friction * 10:.2f}',
             0, 0)    
    add_line(screen, f'Gravity (z or x): {gravity:.2f}',
             0, 45)
    add_line(screen, f'Bounce (e or r): {bounce * 10:.2f}',
             0, 90)
    add_line(screen, f'Person Size (c or v): {HEIGHT * 0.1:.2f}',
             0, 135)
    add_line(screen, f'jump height (t or y): {jump * 0.1:.2f}',
             0, 180)
    add_line(screen, f'red (u or j): {red :.0f}',
             0, 225)
    add_line(screen, f'green (i or k): {green :.0f}',
             0, 270)
    add_line(screen, f'blue (o or l): {blue :.0f}',
             0, 315)
    
    rect = pygame.Rect(pos_x, pos_y, HEIGHT, HEIGHT)
    pygame.draw.rect(screen, my_color, rect)

    pygame.display.update()

    # wait until next tick
    clock.tick(TICKS)

pygame.quit()
