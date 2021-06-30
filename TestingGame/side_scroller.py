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
TILE_SIZE = 40

# player action variables
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False

# load images
# bullets
bullet_img = pygame.image.load('/Users/hungt/Desktop/GameProject/TestingGame/img/bullet.png').convert_alpha()
# grenade
grenade_img = pygame.image.load('/Users/hungt/Desktop/GameProject/TestingGame/img/egg.png').convert_alpha()
grenade_img = pygame.transform.scale(grenade_img, (25, 25))
# pick up boxes
health_img = pygame.image.load('/Users/hungt/Desktop/GameProject/TestingGame/img/items/corn.png').convert_alpha()
health_img = pygame.transform.scale(health_img, (20, 20))
grenade_item_img = pygame.transform.scale(grenade_img, (20, 20))
bullet_item_img = pygame.transform.scale(bullet_img, (20, 20))
item_boxes = {
    'Health'    : health_img,
    'Ammo'      : bullet_item_img,
    'Grenade'  : grenade_item_img
}

# define colors
BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# define font
font = pygame.font.SysFont('Futura', 30)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 600), (SCREEN_WIDTH, 600))

class Mob(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, speed, ammo, grenades, scale=1):
        pygame.sprite.Sprite.__init__(self)
        # mob stat fields
        self.alive = True
        self.speed = speed
        self.health = 100
        self.max_health = self.health
        # action fields
        self.ammo = ammo
        self.start_ammo = ammo
        self.shoot_cooldown = 0
        self.grenades = grenades
        # movement fields
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.pound_cd = False
        # animation fields
        self.char_type = char_type
        self.animation_list = []
        self.index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # load all images for the players
        animation_types = ['idle', 'run', 'jump', 'in_air_rise', 'in_air_fall', 'hit']
        for animation in animation_types:
            # reset temp list of images
            temp_list = []
            # count nuumber of files in folder
            try:
                num_frames = len(os.listdir(f'/Users/hungt/Desktop/GameProject/TestingGame/img/{animation}/{self.char_type}'))
                for i in range(num_frames):
                    img = pygame.image.load(f'/Users/hungt/Desktop/GameProject/TestingGame/img/{animation}/{self.char_type}/{i}.png').convert_alpha()
                    img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                    temp_list.append(img)
            except FileNotFoundError:
                print(f'no sprite animations for {self.char_type}: {animation}')
            finally:
                self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.index]
        self.rect = img.get_rect()
        self.rect.center = (x,y)

    def update(self):
        self.update_animation()
        self.check_alive()
        # update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left=0, moving_right=0):
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
            self.vel_y = -13 # jump height
            self.jump = False
            self.in_air = True

        # apply gravity + pound
        self.vel_y += GRAVITY
        if self.pound_cd:
            self.vel_y = 20
            if not self.in_air:
                self.pound_cd = False
        elif self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # check collision with floor
        if self.rect.bottom + dy > 600:
            dy = 600 - self.rect.bottom
            self.in_air = False

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (-0.8 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)

            self.ammo -= 1

    def pound(self):
        if self.in_air and not self.pound_cd:
            self.pound_cd = True

    def update_animation(self):
        # update animation
        ANIMATION_COOLDOWN = 60
        # update image depending on current framea
        try:
            self.image = self.animation_list[self.action][self.index]
        except IndexError:
            self.image = self.animation_list[self.action][0]

        # check if enough time passed since last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.index += 1
        # reset animation list loop
        if self.index >= len(self.animation_list[self.action]):
            if self.action == 5:
                if self.alive:
                    self.action = 0
                else:
                    self.index = len(self.animation_list[self.action]) - 1
            else:
                self.index = 0

    def update_action(self, new_action):
        # check if new action is different from previous one
        if new_action != self.action:
            self.action = new_action
            # update animations settings
            self.index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(5)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        # pygame.draw.rect(screen, RED, self.rect, 1)
        
class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        # check collision with player
        if pygame.sprite.collide_rect(self, player):
            # check which box
            if self.item_type == 'Health':
                player.health += 50
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'Ammo':
                player.ammo += 10
            elif self.item_type == 'Grenade':
                player.grenades += 5
            # delete item
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        # move bullet
        self.rect.x += (self.direction * self.speed * -1)
        # check if bullet went off screen
        if self.rect.right < -100 or self.rect.left > SCREEN_WIDTH + 100:
            self.kill()
        # check collision with characters
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                player.update_action(5)
                self.kill()
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    enemy.health -= 25
                    enemy.update_action(5)
                    self.kill()

class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -11
        self.speed = 7
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
    
    def update(self):
        self.vel_y += GRAVITY
        dx = self.direction * self.speed
        dy = self.vel_y

        # check collision with floor
        if self.rect.bottom + dy > 600:
            dy = 600 - self.rect.bottom
            self.speed = 0

        # check collision with walls
        if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
            self.direction *= -1
            dx = self.direction * self.speed
        # update grenade position
        self.rect.x += dx
        self.rect.y += dy

        # countdown timer
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            explosion = Explosion(self.rect.x, self.rect.y, 0.3)
            explosion_group.add(explosion)
            # do damage in radius
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
                abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2:
                player.health -= 50
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2:
                    enemy.health -= 50
            
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 13):
            img = pygame.image.load(f'/Users/hungt/Desktop/GameProject/TestingGame/img/Explosion/{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        EXPLOSION_SPEED = 4
        # update explosion animation
        self.counter += 1

        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.index += 1
            # delete explosion after animation
            if self.index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.index]


# create sprite groups 
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()

# temp - create item boxes
item_box = ItemBox('Health', 400, 550)
item_box_group.add(item_box)
item_box = ItemBox('Ammo', 300, 550)
item_box_group.add(item_box)
item_box = ItemBox('Grenade', 500, 550)
item_box_group.add(item_box)

# generate mobs
player = Mob('duck', 200, 400, 7, 20, 5, 2)
enemy = Mob('plant', 400, 400, 5, 100, 0, 2)
enemy2 = Mob('jere', 600, 400, 5, 100, 0, 2)
enemy_group.add(enemy)
enemy_group.add(enemy2)


# main game loop
run = True
while run:
    
    clock.tick(FPS)
    draw_bg()
    # show ammo
    draw_text('PEAS: ', font, WHITE, 15, 620)
    for x in range(player.ammo):
        screen.blit (bullet_img, (95 + (x * 10), 620))
    # show grenades
    draw_text('EGGS: ', font, WHITE, 15, 600)
    # show health
    draw_text('HEALTH: ', font, WHITE, 700, 620)

    for enemy in enemy_group:
        enemy.update()
        enemy.draw()

    player.update()
    player.draw()
    

    # update and draw groups
    bullet_group.update()
    grenade_group.update()
    explosion_group.update()
    item_box_group.update()
    bullet_group.draw(screen)
    grenade_group.draw(screen)
    explosion_group.draw(screen)
    item_box_group.draw(screen)

    
    # update player actions
    if player.alive:
        # shoot bullets
        if shoot:
            player.shoot()
            # throw grenades
        elif grenade and grenade_thrown == False and player.grenades > 0:
            grenade = Grenade(player.rect.centerx + (-0.5 * player.rect.size[0] * player.direction),\
                              player.rect.top, player.direction * -1)
            grenade_group.add(grenade)
            # reduce grenades
            player.grenades -= 1
            grenade_thrown = True
        if player.in_air:
            if player.vel_y > 0: # falling
                player.update_action(4)
            else: # rising
                player.update_action(3)
        elif moving_left or moving_right:
            player.update_action(1)
        else:
            player.update_action(0)        

    player.move(moving_left, moving_right)
    
    for enemy in enemy_group:
        enemy.move()

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
            if event.key == pygame.K_s:
                player.pound()
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_q:
                grenade = True
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
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_q:
                grenade = False
                grenade_thrown = False
        
    
    pygame.display.update()

pygame.quit()