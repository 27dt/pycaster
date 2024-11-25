import pygame
import math

pygame.init()
pygame.display.set_caption('movement testing')
pygame.font.init()
gamefont = pygame.font.SysFont('Arial', 20)

WIDTH, HEIGHT = 200, 200
playerspeed = 10

playerx, playery = 100, 100
angle = math.pi/2

ismoving = False

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

while running:
    screen.fill((77, 67, 127))

    pygame.draw.rect(screen, (255, 255, 255), (playerx, playery, 10, 10), 0)
    pygame.draw.line(screen, (0, 0, 0), (playerx+5, playery+5), (playerx+5, playery-20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                playery -= math.sin(angle)*playerspeed
                playerx -= math.cos(angle)*playerspeed
            if event.key == pygame.K_s:
                playery += math.sin(angle)*playerspeed
                playerx += math.cos(angle)*playerspeed
            if event.key == pygame.K_a:
                angle -= 0.3
            if event.key == pygame.K_d:
                angle += 0.3


    
    #playery-=playerspeed
               
    pygame.display.flip()
    clock.tick(60)

pygame.quit()