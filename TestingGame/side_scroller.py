import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')

# set framerate
clock = pygame.time.Clock()
FPS = 60

# player action variables
moving_left = False
moving_right = False

# define colors
BG = (144, 201, 120)

def draw_bg():
    screen.fill(BG)

class Mob(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, speed, scale=1):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.char_type = char_type
        self.animation_list = []
        self.index = 0
        self.update_time = pygame.time.get_ticks()
        for i in range(9):
            img = pygame.image.load(f'/Users/hungt/Desktop/GameProject/TestingGame/img/idle/{self.char_type}/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.animation_list.append(img)
        self.image = self.animation_list[self.index]
        self.rect = img.get_rect()
        self.rect.center = (x,y)

    def move(self, moving_left, moving_right):
        # reset movement variables
        dx = 0
        dy = 0
        
        if moving_left:
            dx = -self.speed
            self.flip = False
            self.direction = 1
        if moving_right:
            dx = self.speed
            self.flip = True
            self.direction = -1

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 60
        # update image depending on current frame
        self.image = self.animation_list[self.index]
        # check if enough time passed since last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.index += 1
            if self.index > 8:
                self.index = 0

    def draw(self):
        self.update_animation()
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

player = Mob('duck', 200, 200, 5)



# main game loop
run = True
while run:
    
    clock.tick(FPS)

    draw_bg()

    player.draw()
    
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