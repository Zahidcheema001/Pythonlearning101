import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
BALL_SIZE = 20
PADDLE_SPEED = 6
BALL_SPEED_X = 4
BALL_SPEED_Y = 4

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Pong Game")

# Game objects
paddle1 = pygame.Rect(50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle2 = pygame.Rect(SCREEN_WIDTH - 50 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Movement variables
ball_dx = BALL_SPEED_X * random.choice((10, -1))
ball_dy = BALL_SPEED_Y * random.choice((1, -1))
paddle1_dy = 0
paddle2_dy = 0

# Score
score1 = 0
score2 = 0
font = pygame.font.Font(None, 36)

# Function to reset the ball position
def reset_ball():
    global ball_dx, ball_dy
    ball.x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
    ball.y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
    ball_dx = BALL_SPEED_X * random.choice((1, -1))
    ball_dy = BALL_SPEED_Y * random.choice((1, -1))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                paddle1_dy = -PADDLE_SPEED
            if event.key == pygame.K_s:
                paddle1_dy = PADDLE_SPEED
            if event.key == pygame.K_UP:
                paddle2_dy = -PADDLE_SPEED
            if event.key == pygame.K_DOWN:
                paddle2_dy = PADDLE_SPEED
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_s):
                paddle1_dy = 0
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                paddle2_dy = 0

    # Move paddles
    paddle1.y += paddle1_dy
    paddle2.y += paddle2_dy

    # Keep paddles on the screen
    if paddle1.top < 0:
        paddle1.top = 0
    if paddle1.bottom > SCREEN_HEIGHT:
        paddle1.bottom = SCREEN_HEIGHT
    if paddle2.top < 0:
        paddle2.top = 0
    if paddle2.bottom > SCREEN_HEIGHT:
        paddle2.bottom = SCREEN_HEIGHT

    # Move the ball
    ball.x += ball_dx
    ball.y += ball_dy

    # Ball collision with top/bottom
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_dy = -ball_dy

    # Ball collision with paddles
    if ball.colliderect(paddle1) or ball.colliderect(paddle2):
        ball_dx = -ball_dx

    # Ball out of bounds
    if ball.left <= 0:
        score2 += 1
        reset_ball()
    if ball.right >= SCREEN_WIDTH:
        score1 += 1
        reset_ball()

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, paddle1)
    pygame.draw.rect(screen, WHITE, paddle2)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

    # Draw the score
    score_text = font.render(f"{score1} - {score2}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 20))

    # Update the display
    pygame.display.flip()

    # Frame rate
    pygame.time.Clock().tick(60)

pygame.quit()