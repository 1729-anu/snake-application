import pygame
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 480
CELL_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Snake class
class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (0, -1)

    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        tail = self.body[-1]
        new_tail = (tail[0] - self.direction[0], tail[1] - self.direction[1])
        self.body.append(new_tail)

    def change_direction(self, direction):
        if (direction[0] != -self.direction[0]) or (direction[1] != -self.direction[1]):
            self.direction = direction

    def check_collision(self):
        head = self.body[0]
        if head[0] < 0 or head[0] >= GRID_WIDTH or head[1] < 0 or head[1] >= GRID_HEIGHT:
            return True
        if head in self.body[1:]:
            return True
        return False

# Food class
class Food:
    def __init__(self):
        self.position = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))

    def respawn(self):
        self.position = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))

# Initialize game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()
snake = Snake()
food = Food()
score = 0

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction((0, -1))
            elif event.key == pygame.K_DOWN:
                snake.change_direction((0, 1))
            elif event.key == pygame.K_LEFT:
                snake.change_direction((-1, 0))
            elif event.key == pygame.K_RIGHT:
                snake.change_direction((1, 0))

    screen.fill(BLACK)

    # Move snake
    snake.move()

    # Check collision with food
    if snake.body[0] == food.position:
        snake.grow()
        food.respawn()
        score += 1

    # Check collision with walls or itself
    if snake.check_collision():
        running = False

    # Draw snake
    for segment in snake.body:
        pygame.draw.circle(screen, GREEN, (int(segment[0] * CELL_SIZE + CELL_SIZE / 2), int(segment[1] * CELL_SIZE + CELL_SIZE / 2)), CELL_SIZE // 2)

    # Draw food
    pygame.draw.rect(screen, RED, (food.position[0] * CELL_SIZE, food.position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Display score
    font = pygame.font.Font(None, 36)
    text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(7)

pygame.quit()
