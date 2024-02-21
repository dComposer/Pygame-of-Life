# Example file showing a basic pygame "game loop"
import pygame
import numpy as np

# pygame setup
pygame.init()
pygame.display.set_caption("PyGame of Life")
pixels = 800
screen = pygame.display.set_mode((pixels, pixels))
clock = pygame.time.Clock()
running = True

size = 80
prob = 35

# Colors
colors = np.random.randint(256, size=3)
R = colors[0]
G = colors[1]
B = colors[2]
background = (255 - R, 255 - G, 255 - B)

# Initialize game board
gol = np.random.randint(100, size=(size, size))
gol = (gol > prob) * 1

# print(gol)

while running:
    # poll for events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                gol = np.random.randint(100, size=(size, size))
                gol = (gol > prob) * 1

                colors = np.random.randint(256, size=3)
                R = colors[0]
                G = colors[1]
                B = colors[2]
                background = (255 - R, 255 - G, 255 - B)
                print("Game of Life: Reset")
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(background)

    # GoL
    # Calculate how many neighbors exist around each cell
    neighbors = []
    for row in range(size):
        for col in range(size):
            total_cells = 0
            # test for up
            if gol[row - 1][col] == 1:
                total_cells += 1
            # test for up-right
            if col == size - 1:
                if gol[row - 1][0] == 1:
                    total_cells += 1
            else:
                if gol[row - 1][col + 1] == 1:
                    total_cells += 1
            # test for right
            if col == size - 1:
                if gol[row][0] == 1:
                    total_cells += 1
            else:
                if gol[row][col + 1] == 1:
                    total_cells += 1
            # test for down-right
            if col == size - 1 & row == size - 1:
                if gol[0][0] == 1:
                    total_cells += 1
            elif col == size - 1:
                if gol[row + 1][0] == 1:
                    total_cells += 1
            elif row == size - 1:
                if gol[0][col + 1] == 1:
                    total_cells += 1
            else:
                if gol[row + 1][col + 1] == 1:
                    total_cells += 1
            # test for down
            if row == size - 1:
                if gol[0][col] == 1:
                    total_cells += 1
            else:
                if gol[row + 1][col] == 1:
                    total_cells += 1
            # test for down-left
            if row == size - 1:
                if gol[0][col - 1] == 1:
                    total_cells += 1
            else:
                if gol[row + 1][col - 1] == 1:
                    total_cells += 1
            # test for left
            if gol[row][col - 1] == 1:
                total_cells += 1
            # test for up-left
            if gol[row - 1][col - 1] == 1:
                total_cells += 1
            neighbors.append(total_cells)

    total_neighbors = np.array(neighbors).reshape((size, size))

    # print(total_neighbors)

    # Rules:
    # 1) Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
    # 2) Any live cell with two or three live neighbours lives on to the next generation.
    # 3) Any live cell with more than three live neighbours dies, as if by overpopulation.
    # 4) Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

    alive = []
    for row in range(size):
        for col in range(size):
            if gol[row][col] == 1:
                if total_neighbors[row][col] < 2:
                    alive.append(0)  # death by underpopulation
                elif total_neighbors[row][col] < 4:
                    alive.append(1)  # survives
                else:
                    alive.append(0)  # death by overpopulation
            else:
                if total_neighbors[row][col] == 3:
                    alive.append(1)  # reproduction
                else:
                    alive.append(0)  # still dead

    next_gen = np.array(alive).reshape((size, size))
    # print(next_gen)

    # RENDER YOUR GAME HERE
    length = pixels // size
    for row in range(size):
        for col in range(size):
            if gol[row][col] == 1:
                color = (R, G, B)
            else:
                color = background
            pygame.draw.rect(
                screen, color, pygame.Rect(length * row, length * col, length, length)
            )

    gol = next_gen

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(10)  # limits FPS to 60

pygame.quit()
