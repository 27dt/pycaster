import math
import pygame

pygame.init()
pygame.display.set_caption("pycaster")

# Initial Variables: Map
TILE = 42                                       # Size of each "grid tile"
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

    # Rayangle is normalized player angle - half FOV, used to find ray coordinates/distances
    # (i.e. for 60 degrees, a middle ray splits fov between two 30 degree angles)
    rayAngle = normalize(pa) - FOV/2 
    
    # Drawing rays
    for i in range(TOTALRAYS):
        wall_x = 0              # Final x and y coordinates
        wall_y = 0
        
        found_hor_wall = False  # Booleans for checking if walls have been found on hor/ver intersections
        found_ver_wall = False
        hor_hit_x = 0           # Horizontal/vertical coordinates for where a wall is hit (if it is)
        hor_hit_y = 0
        ver_hit_x = 0
        ver_hit_y = 0

        first_x = None          # Initial distance from px to first horizontal intersection
        first_y = None          # Initial distance from py to first vertical intersection

        # HORIZONTAL INTERSECTIONS
        # If player angle is facing down (ray angle between 0 and pi, as we move down in a flipped unit circle)
        if rayAngle > 0 and rayAngle < math.pi:
            # Location of first vertical intersection is tile next to the current tile the player is in
            first_y = (py // TILE) * TILE + TILE
        else:
            # If player is facing up, first vertical intersection is the top of the tile the player is in
            first_y = (py // TILE) * TILE - 1

        # In this case, first horizontal intersection is solved using py, px, rayAngle, and first_y
        first_x = ((first_y - py) / math.tan(rayAngle)) + px

        # Increment hor_step_x and y with the initial distances of the first intersections
        hor_step_x = first_x
        hor_step_y = first_y

        # Step amount: increases by +tilesize if looking down, or -tilesize if looking up
        ya = TILE if (rayAngle > 0 and rayAngle < math.pi) else -TILE
        xa = ya / math.tan(rayAngle)

        # As long as the distance calculations are in bounds of the 3D screen
        while(hor_step_x <= WIDTH and hor_step_x >= 0 and hor_step_y <= HEIGHT and hor_step_y >= 0):
            # Call helper function to check if wall exists at coordinate
            if wall_check(hor_step_x, hor_step_y):
                # Set found_wall trigger, with hit coordinates equal to current step
                found_hor_wall = True
                hor_hit_x = hor_step_x
                hor_hit_y = hor_step_y
                break
            else:
                # Else, increment by step amount until a wall is eventually found
                hor_step_x += xa
                hor_step_y += ya
        
        # VERTICAL INTERSECTIONS:
        if rayAngle < 0.5 * math.pi or rayAngle > 1.5 * math.pi: #right
             first_x = ((px // TILE) * TILE) + TILE
        else: #facing left
             first_x = ((px // TILE) * TILE) - 1

        first_y = ((first_x-px) * math.tan(rayAngle)) + py

        ver_step_x = first_x
        ver_step_y = first_y

        xa = TILE if (rayAngle < 0.5 * math.pi or rayAngle > 1.5 * math.pi) else -TILE
        ya = xa * math.tan(rayAngle)

        while(ver_step_x <= WIDTH and ver_step_x >= 0 and ver_step_y <= HEIGHT and ver_step_y >= 0):
            if wall_check(ver_step_x, ver_step_y):
                found_ver_wall = True
                ver_hit_x = ver_step_x
                ver_hit_y = ver_step_y
                break
            else:
                ver_step_x += xa
                ver_step_y += ya
        
        # Ray Distance Calculations
        # Because each ray is casted to determine the horizontal and vertical intersections of a wall, 
        # The ray with the shorter distance must be determined, as this is the one to draw
        hor_dist = 0
        ver_dist = 0

        # If a horizontal/vertical wall was found, find distance. Else, set distance to arbitrary large number 
        if found_hor_wall:
            hordist = math.sqrt(math.pow((hor_hit_x - px), 2) + math.pow((hor_hit_y-py), 2))
        else:
            hordist = 99999

        if found_ver_wall:
            verdist = math.sqrt(math.pow((ver_hit_x - px), 2) + math.pow((ver_hit_y-py), 2))
        else:
            verdist = 99999
        
        # Compare horizontal and vertical distance calculations to the wall, and set wall coordinates to shortest
        if hordist < verdist:
            wall_x = hor_hit_x
            wall_y = hor_hit_y
            hordist *= math.cos(pa - rayAngle)
        else:
            wall_x = ver_hit_x
            wall_y = ver_hit_y
            verdist *= math.cos(pa - rayAngle)

        # Append "winning" distance to ray_dist array (will be used for rendering walls)
        if hordist < verdist:
            ray_dist.append(hordist)
        else:
            # Quick and dirty way shade vertical walls a different colour
            # (append the distance value with a negative offset, and check if the  
            # current ray being drawn is negative. If so, change colour and remove offset)
            ray_dist.append(verdist - 1000)
        
        # Draw ray (for 2D side) and increment rayAngle to draw next
        pygame.draw.line(screen, (255, 0, 0), (px, py), (wall_x, wall_y))
        rayAngle += FOV / TOTALRAYS

    # Counter to draw all casted rays (3D view)
    counter = 0
    for i in range(TOTALRAYS):
        # Recall: workaround to make vertical rays appear darker with -1000 offset
        if ray_dist[counter] < 0:
            line_height = (32 / (ray_dist[counter] + 1000)) * 315
            drawbegin = (HEIGHT / 2) - (line_height / 2)
            draw_end = line_height
            pygame.draw.rect(screen, (130, 0, 0), (counter*BARWIDTH + WIDTH, drawbegin, BARWIDTH, draw_end))
        else:
            # Height: dividing 32 by the distance of the ray from the player (times 415, offset of player to screen)
            line_height = (32 / (ray_dist[counter])) * 315
            # Beginning of casted ray located at window height / 2 minus line height
            drawbegin = (HEIGHT / 2) - (line_height / 2)
            draw_end = line_height
            pygame.draw.rect(screen, (255, 0, 0), (counter*BARWIDTH + WIDTH, drawbegin, BARWIDTH, draw_end))
        counter += 1

    # 60 FPS cap
    clock.tick(60)
    pygame.display.update()