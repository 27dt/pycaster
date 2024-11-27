import pygame
import math

pygame.init()
pygame.display.set_caption('movement testing')
pygame.font.init()
gamefont = pygame.font.SysFont('Arial', 20)

WIDTH, HEIGHT = 200, 200
playerspeed = 10

angle = math.pi/2

playerdeltax = 0
playerdeltay = 0

playerx, playery = 100+playerdeltax*10, 100+playerdeltay*10

ismoving = False

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

while running:
    screen.fill((77, 67, 127))

    pygame.draw.rect(screen, (255, 255, 255), (playerx, playery, 10, 10), 0)
    #pygame.draw.line(screen, (0, 0, 0), (playerx+5, playery+5), ((playerx+5)-math.cos(angle)*playerspeed, playery-math.sin(angle)*playerspeed))
    pygame.draw.line(screen, (0, 0, 0), (playerx+5, playery+5), (playerx+playerdeltax*10, playery+playerdeltay*10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                #playery -= math.sin(angle)*playerspeed
                #playerx -= math.cos(angle)*playerspeed
                playerx += playerdeltax
                playery += playerdeltay
            if event.key == pygame.K_s:
                #playery += math.sin(angle)*playerspeed
                #playerx += math.cos(angle)*playerspeed
                playerx -= playerdeltax
                playery -= playerdeltay
            if event.key == pygame.K_a:
                if (angle - math.pi/50 < 0): angle = 2*math.pi
                #angle += math.pi/10 #changes to +
                angle -= math.pi/50
                if angle < 0: angle += 2*math.pi
                playerdeltax = math.cos(angle)*10 #new
                playerdeltay = math.sin(angle)*10 #new
                print(math.degrees(angle))
            if event.key == pygame.K_d:
                if (angle + math.pi/50 > 2*math.pi): angle = 0
                #angle -= math.pi/10 #changes to -
                angle += math.pi/50
                if angle > (math.pi*2): angle -= 2*math.pi
                playerdeltax = math.cos(angle)*10 #new
                playerdeltay = math.sin(angle)*10 #new
                print(math.degrees(angle))


    
    #playery-=playerspeed
               
    pygame.display.flip()
    clock.tick(60)

pygame.quit()