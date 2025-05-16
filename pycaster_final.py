import math
import pygame

pygame.init()
pygame.display.set_caption("pycaster")

# Initial Variables: Map
TILE = 32                                       # Size of each "grid tile"
ROWS = 10                                       # Rows and columns in map
COLS = 10                                       
WIDTH = COLS*TILE                               # Grid display width and height
HEIGHT = ROWS*TILE                              
FOV = 60 * (math.pi/180)                        # Player field of view in radians (python math in rads)
BARWIDTH = 4                                    # Width of each "bar" making up walls 
TOTALRAYS = WIDTH // BARWIDTH                   # Total amount of rays to cast to make screen
ray_dist = []                                   # To save distances of each ray (for drawing on screen)
game_map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],     # 2D Map for player: 0 = empty, 1 = wall
           [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
           [1, 0, 1, 1, 0, 0, 0, 1, 0, 1],
           [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
           [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
           [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
           [1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
           [1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
           [1, 0, 0, 0, 0, 0, 0, 1, 1, 1],
           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


# Initial Variables: Player
px = WIDTH / 2                                  # Player x and y coordinates
py = HEIGHT / 2
pa = 45 * (math.pi/180)                         # Player angle (initial value)
mov_speed = 1                                   # Player step increment (when moving)
rot_speed = 2 * (math.pi / 180)                 # Player rotation increment (when turning)

# Helper functions
def wall_check(x, y):
    # Given pixel coordinates, find corresponding grid block and verify it is 1 (wall)
    return game_map[int(y // TILE)][int(x // TILE)] == 1

def normalize(angle):
    # Normalizes a given angle to be between 0 and 2pi if it is < 0 or > 2pi
    angle = angle % (2*math.pi)
    if angle <= 0:
        angle = (2*math.pi) + angle
    return angle

# Pygame Variables
screen = pygame.display.set_mode((WIDTH*2, HEIGHT))
clock = pygame.time.Clock()

# Main Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill((0, 0, 0))
    # At start of each "refresh", empty ray_dist array for new set of rays to draw
    ray_dist = []

    keys=pygame.key.get_pressed()
    turn_dir = 0

    # To move forward/back, multiply position coordinates by x,y vector components (to account for angle)
    if keys[pygame.K_w]:
        px += math.cos(pa) * mov_speed
        py += math.sin(pa) * mov_speed
    if keys[pygame.K_s]:
        px -= math.cos(pa) * mov_speed
        py -= math.sin(pa) * mov_speed
    # To turn left/right, add/subtract angle increment from player angle
    if keys[pygame.K_a]:
        pa -= rot_speed
    if keys[pygame.K_d]:
        pa += rot_speed

    # Grid drawing algorithm
    for row in range(len(game_map)):
        for col in range(len(game_map[row])):
            if game_map[row][col] == 0:
                # Draws grid squares by looping through, and multiplying by TILE size offset
                pygame.draw.rect(screen, (255, 255, 255), (col * TILE, row * TILE, TILE - 1, TILE - 1))
            if game_map[row][col] == 1:
                pygame.draw.rect(screen, (10, 10, 10), (col * TILE, row * TILE, TILE - 1, TILE - 1))

    # Draw small circle for player (2D View)
    pygame.draw.circle(screen, (0, 0, 255), (px, py), 4)

    #RAYS
    rayAngle = normalize(pa) - FOV/2 
    
    for i in range(TOTALRAYS):
        wall_x = 0
        wall_y = 0
        found_horizontal_wall = False
        horizontal_hitx = 0
        horizontal_hity = 0

        firstintx = None
        firstinty = None

        if rayAngle > 0 and rayAngle < math.pi: #facing down
            firstinty = (py // TILE) * TILE + TILE
        else: #facing up
            firstinty = (py // TILE) * TILE - 1

        firstintx = ((firstinty - py) / math.tan(rayAngle)) + px

        hor_step_x = firstintx
        hor_step_y = firstinty

        ya = TILE if (rayAngle > 0 and rayAngle < math.pi) else -TILE
        xa = ya / math.tan(rayAngle)

        while(hor_step_x <= WIDTH and hor_step_x >= 0 and hor_step_y <= HEIGHT and hor_step_y >= 0):
            if wall_check(hor_step_x, hor_step_y):
                found_horizontal_wall = True
                horizontal_hitx = hor_step_x
                horizontal_hity = hor_step_y
                break
            else:
                hor_step_x += xa
                hor_step_y += ya
        
        
        found_vertical_wall = False
        vertical_hitx = 0
        vertical_hity = 0

        if rayAngle < 0.5 * math.pi or rayAngle > 1.5 * math.pi: #right
             firstintx = ((px // TILE) * TILE) + TILE
        else: #facing left
             firstintx = ((px // TILE) * TILE) - 1

        firstinty = ((firstintx-px) * math.tan(rayAngle)) + py

        ver_step_x = firstintx
        ver_step_y = firstinty

        xa = TILE if (rayAngle < 0.5 * math.pi or rayAngle > 1.5 * math.pi) else -TILE
        ya = xa * math.tan(rayAngle)

        while(ver_step_x <= WIDTH and ver_step_x >= 0 and ver_step_y <= HEIGHT and ver_step_y >= 0):
            if wall_check(ver_step_x, ver_step_y):
                found_vertical_wall = True
                vertical_hitx = ver_step_x
                vertical_hity = ver_step_y
                break
            else:
                ver_step_x += xa
                ver_step_y += ya
        
        # distance
        hordist = 0
        verdist = 0

        if found_horizontal_wall:
            hordist = math.sqrt(math.pow((horizontal_hitx - px), 2) + math.pow((horizontal_hity-py), 2))
        else:
            hordist = 99999

        if found_vertical_wall:
            verdist = math.sqrt(math.pow((vertical_hitx - px), 2) + math.pow((vertical_hity-py), 2))
        else:
            verdist = 99999
        
        if hordist < verdist:
            wall_x = horizontal_hitx
            wall_y = horizontal_hity
            hordist *= math.cos(pa - rayAngle)
        else:
            wall_x = vertical_hitx
            wall_y = vertical_hity
            verdist *= math.cos(pa - rayAngle)

        if hordist < verdist:
            ray_dist.append(hordist)
        else:
            ray_dist.append(verdist - 1000)
        
        pygame.draw.line(screen, (255, 0, 0), (px, py), (wall_x, wall_y))
        rayAngle += FOV / TOTALRAYS

    counter = 0
    for i in range(TOTALRAYS):
        if ray_dist[counter] < 0:
            line_height = (32 / (ray_dist[counter] + 1000)) * 415
            drawbegin = (HEIGHT / 2) - (line_height / 2)
            draw_end = line_height
            pygame.draw.rect(screen, (130, 0, 0), (counter*BARWIDTH + WIDTH, drawbegin, BARWIDTH, draw_end))
        else:
            line_height = (32 / (ray_dist[counter])) * 415
            drawbegin = (HEIGHT / 2) - (line_height / 2)
            draw_end = line_height
            pygame.draw.rect(screen, (255, 0, 0), (counter*BARWIDTH + WIDTH, drawbegin, BARWIDTH, draw_end))
        counter += 1

    # 60 FPS cap
    clock.tick(60)
    pygame.display.update()