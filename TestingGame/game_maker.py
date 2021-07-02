import pygame
import os
import button
import csv
import pickle

pygame.init()

clock = pygame.time.Clock()
FPS = 60

# game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Level Editor')

# define game variables
ROWS = 16
MAX_COL = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 2 # number of tile types
current_tile = 0
level = 0

scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1

# load images
rel_path = os.path.dirname(os.path.abspath(__file__))
rel_path = rel_path.replace('\\', '/')
# print(rel_path)

back1_img = pygame.image.load(rel_path + '/img/cyberpunk-street-files/PNG/layers/0.png').convert_alpha()
back1_img = pygame.transform.scale(back1_img, (SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT))
back2_img = pygame.image.load(rel_path + '/img/cyberpunk-street-files/PNG/layers/1.png').convert_alpha()
back2_img = pygame.transform.scale(back2_img, (SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT))
back3_img = pygame.image.load(rel_path + '/img/cyberpunk-street-files/PNG/layers/2.png').convert_alpha()
back3_img = pygame.transform.scale(back3_img, (SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT))
# store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(rel_path + f'/img/tiles/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

save_img = pygame.image.load(rel_path + '/img/buttons/save.png').convert_alpha()
save_img = pygame.transform.scale(save_img, (75, 75))
load_img = pygame.image.load(rel_path + '/img/buttons/load.png').convert_alpha()
load_img = pygame.transform.scale(load_img, (75, 75))
quit_img = pygame.image.load(rel_path + '/img/buttons/quit.png').convert_alpha()
quit_img = pygame.transform.scale(quit_img, (75, 75))

# define colors
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

# define font
font = pygame.font.SysFont('Futura', 30)

# create empty tile list
world_data = []

def empty_world():
    for r in range(ROWS):
        r = [-1] * MAX_COL
        world_data.append(r)

# create ground
def draw_ground():
    for tile in range(0, MAX_COL):
        world_data[ROWS - 1][tile] = 0

empty_world()
draw_ground()

# function for outputting text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# function for drawing background
def draw_bg():
    screen.fill(GREEN)
    width = back1_img.get_width()
    for x in range(6):
        screen.blit(back1_img, ((x * width) - scroll * 0.7, 0))
        screen.blit(back2_img, ((x * width) - scroll * 0.8, 0))
        screen.blit(back3_img, ((x * width) - scroll, 0))

def draw_grid():
    # vertical lines
    for c in range(MAX_COL + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))
    # horizontal lines
    for r in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, r * TILE_SIZE), (SCREEN_WIDTH, r * TILE_SIZE))

# function for drawing world tiles
def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))

# create buttons
save_button = button.Button(SCREEN_WIDTH // 3 + 50, SCREEN_HEIGHT + LOWER_MARGIN - 85, save_img, 1)
load_button = button.Button(SCREEN_WIDTH // 3 + 250, SCREEN_HEIGHT + LOWER_MARGIN - 85, load_img, 1)
quit_button = button.Button(SCREEN_WIDTH // 3 + 450, SCREEN_HEIGHT + LOWER_MARGIN - 85, quit_img, 1)
# make a button list
button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    tile_button = button.Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0


run = True
while run:

    clock.tick(FPS)

    draw_bg()
    draw_grid()
    draw_world()

    draw_text(f'Level: {level}', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
    draw_text('Press UP or DOWN to', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)
    draw_text('change level', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 40)

    # save and load data
    if save_button.draw(screen):
        # save level data
        # 'pickle' save method
        # pickle_out = open(f'level{level}_data' 'wb')
        # pickle.dump(world_data, pickle_out)
        # pickle_out.closer()

        os.chdir(rel_path + '/level_data')

        with open(f'level{level}_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            for row in world_data:
                writer.writerow(row)
        
        os.chdir(rel_path)

    if load_button.draw(screen):
        # load level data
        # reset scroll
        scroll = 0
        # 'pickle' load method
        # world_data = []
        # pickle_in = open(f'level{level}_data', 'rb')
        # world_data = pickle.load(pickle_in)

        os.chdir(rel_path + '/level_data')

        try:
            with open(f'level{level}_data.csv', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter = ',')
                for row in world_data:
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
        except FileNotFoundError:
            pass

        os.chdir(rel_path)

    if quit_button.draw(screen):
        world_data = []
        empty_world()
        draw_ground()
        

    # draw tile panel and tiles
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

    # choose tile
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count

    # highlight selected rectangle
    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

    # scroll map
    if scroll_left == True and scroll > 0:
        scroll -= 5 * scroll_speed
    if scroll_right == True and scroll < (MAX_COL * TILE_SIZE) - SCREEN_WIDTH:
        scroll += 5 * scroll_speed

    # add new tiles to screen
    # get mouse pos
    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll) // TILE_SIZE
    y = pos[1] // TILE_SIZE
    # print(f'({x}, {y})')

    # check if within tile area
    if pos [0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        # update tile value
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = -1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                scroll_left = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                scroll_right = True
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                level += 1
            if event.key == pygame.K_DOWN or event.key == pygame.K_s and level > 0:
                level -= 1
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                scroll_speed = 5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                scroll_left = False
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                scroll_right = False
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                scroll_speed = 1

    pygame.display.update()

pygame.quit()