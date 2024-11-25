import pygame

pygame.init()
pygame.display.set_caption('pycaster v1.5')
pygame.font.init()
gamefont = pygame.font.SysFont('Arial', 20)

WIDTH, HEIGHT = 200, 200
cubeside = 20       
gameMap = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
           [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
           [1, 0, 1, 1, 0, 0, 0, 0, 0, 1],
           [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
           [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
           [1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
           [1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
           [1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
           [1, 0, 0, 0, 0, 0, 0, 1, 1, 1],
           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

while running:
    screen.fill((77, 67, 127))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    for i in range (len(gameMap)):
        for j in range (len(gameMap[i])):         
            
            if gameMap[i][j] == 1:
                pygame.draw.rect(screen, (255, 255, 255), ((i*cubeside), (j*cubeside), cubeside, cubeside), 1)
            else:
                pygame.draw.rect(screen, (0, 0, 0), ((i*cubeside), (j*cubeside), cubeside, cubeside), 1)
               
    pygame.display.flip()
    clock.tick(60)

pygame.quit()