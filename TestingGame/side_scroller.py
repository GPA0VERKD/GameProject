import pygame
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Ducky')

# set framerate
clock = pygame.time.Clock()
FPS = 60

# define game variables
GRAVITY = 0.75

# player action variables
moving_left = False
moving_right = False

# define colors
BG = (144, 201, 120)
RED = (255, 0, 0)

def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 600), (SCREEN_WIDTH, 600))

class Mob(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, speed, scale=1):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.char_type = char_type
        self.animation_list = []
        self.index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # load all images for the players
        animation_types = ['idle', 'run', 'jump', 'in_air_rise', 'in_air_fall']
        for animation in animation_types:
            # reset temp list of images
            temp_list = []
            # count nuumber of files in folder
            num_frames = len(os.listdir(f'/Users/hungt/Desktop/GameProject/TestingGame/img/{animation}/{self.char_type}'))
            for i in range(num_frames):
                img = pygame.image.load(f'/Users/hungt/Desktop/GameProject/TestingGame/img/{animation}/{self.char_type}/{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.index]
        self.rect = img.get_rect()
        self.rect.center = (x,y)

    def move(self, moving_left, moving_right):
        # reset movement variables
        dx = 0
        dy = 0
        
        # move left and right
        if moving_left:
            dx = -self.speed
            self.flip = False
            self.direction = 1
        if moving_right:
            dx = self.speed
            self.flip = True
            self.direction = -1

        # jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -11 # jump height
            self.jump = False
            self.in_air = True

        # apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # check collision with floor
        if self.rect.bottom + dy > 600:
            dy = 600 - self.rect.bottom
            self.in_air = False

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 60
        # update image depending on current frame
        self.image = self.animation_list[self.action][self.index]
        # check if enough time passed since last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.index += 1
        # reset animation list loop
        if self.index >= len(self.animation_list[self.action]):
            self.index = 0

    def update_action(self, new_action):
        # check if new action is different from previous one
        if new_action != self.action:
            self.action = new_action
            # update animations settings
            self.index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        
        

player = Mob('duck', 200, 200, 5, 2)



# main game loop
run = True
while run:
    
    clock.tick(FPS)
    draw_bg()
    player.update_animation()
    player.draw()
    
    # update player actions
    if player.alive:
        if moving_left or moving_right:
            player.update_action(1)
        else:
            player.update_action(0)
        
        if player.in_air:
            if player.vel_y > 0: # falling
                player.update_action(4)
            else: # rising
                player.update_action(3)

    player.move(moving_left, moving_right)

    for event in pygame.event.get():
        # quit game with 'X' button
        if event.type == pygame.QUIT:
            run = False
        # keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False
        # keyboard button release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
        
    
    pygame.display.update()

pygame.quit()