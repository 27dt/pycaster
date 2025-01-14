import pygame
import math

pygame.init()
pygame.display.set_caption('movement testing')
pygame.font.init()
gamefont = pygame.font.SysFont('Arial', 20)

WIDTH, HEIGHT = 200, 200
playerspeed = 5

angle = math.pi/2

playerx, playery = 100, 100

rays = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

while running:
    screen.fill((77, 67, 127))

    pygame.draw.rect(screen, (255, 255, 255), (playerx, playery, 10, 10), 0)
    #pygame.draw.line(screen, (0,0,0), (playerx+5, playery+5), ((playerx+(math.cos(angle)*5)*5)+5, (playery+(math.sin(angle)*5)*5)+5))

    for i in range (0, rays):
        pygame.draw.line(screen, (0,0,0), (playerx+5, playery+5), ((playerx+(math.cos(angle)*5)*5)+5, (playery+(math.sin(angle)*5)*5)+5))

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys=pygame.key.get_pressed()
    if keys[pygame.K_w]:
        playerx += math.cos(angle)*5
        playery += math.sin(angle)*5
    if keys[pygame.K_s]:
        playerx -= math.cos(angle)*5
        playery -= math.sin(angle)*5
    if keys[pygame.K_a]:
        if (angle - math.pi/50 < 0): angle = 2*math.pi
        angle -= math.pi/50
        print(math.degrees(angle))
    if keys[pygame.K_d]:
        if (angle + math.pi/50 > 2*math.pi): angle = 0
        angle += math.pi/50
        print(math.degrees(angle))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()