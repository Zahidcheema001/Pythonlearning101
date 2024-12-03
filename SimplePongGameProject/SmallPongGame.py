import pygame
import random
import time

# Initialize Pygame and Mixer
pygame.init()
pygame.mixer.init()

# Load Sounds
roar = pygame.mixer.Sound(r'C:\Users\cheem\Downloads\ProgrammingInPython\Pythonlearning101\SimplePongGameProject\GameSounds\roar.mp3')
bellsound = pygame.mixer.Sound(r'C:\Users\cheem\Downloads\ProgrammingInPython\Pythonlearning101\SimplePongGameProject\GameSounds\taco.bellsound.mp3')

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
BALL_SIZE = 21
PADDLE_SPEED = 12
DOUBLE_TAP_SPEED = 18
BALL_SPEED_X = 4
BALL_SPEED_Y = 4
DOUBLE_TAP_THRESHOLD = 0.2

# Create Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Pong Game")

# Game Objects
paddle1 = pygame.Rect(50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle2 = pygame.Rect(SCREEN_WIDTH - 50 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Movement Variables
ball_dx = BALL_SPEED_X * random.choice((1, -1))
ball_dy = BALL_SPEED_Y * random.choice((1, -1))
paddle1_dy = 0
paddle2_dy = 0

# Score and Font
score1, score2 = 0, 0
font = pygame.font.Font(None, 36)

# Ball Colors
ball_colors = [WHITE]
current_color_index = 0

# Double-Tap Detection Timers
last_w_press, last_s_press = 0, 0
last_up_press, last_down_press = 0, 0

# Functions
def random_color():
    """Generate a random color."""
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

def reset_ball():
    """Reset ball position and speed."""
    global ball_dx, ball_dy
    ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    if (score1 + score2) % 12 == 0:
        ball_dx = BALL_SPEED_X * random.choice((1, -1))
        ball_dy = BALL_SPEED_Y * random.choice((1, -1))

# Main Game Loop
running = True
while running:
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            current_time = time.time()
            if event.key == pygame.K_w:
                paddle1_dy = -DOUBLE_TAP_SPEED if current_time - last_w_press < DOUBLE_TAP_THRESHOLD else -PADDLE_SPEED
                last_w_press = current_time
            if event.key == pygame.K_s:
                paddle1_dy = DOUBLE_TAP_SPEED if current_time - last_s_press < DOUBLE_TAP_THRESHOLD else PADDLE_SPEED
                last_s_press = current_time
            if event.key == pygame.K_UP:
                paddle2_dy = -DOUBLE_TAP_SPEED if current_time - last_up_press < DOUBLE_TAP_THRESHOLD else -PADDLE_SPEED
                last_up_press = current_time
            if event.key == pygame.K_DOWN:
                paddle2_dy = DOUBLE_TAP_SPEED if current_time - last_down_press < DOUBLE_TAP_THRESHOLD else PADDLE_SPEED
                last_down_press = current_time
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_s):
                paddle1_dy = 0
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                paddle2_dy = 0

    # Paddle Movement
    paddle1.y += paddle1_dy
    paddle2.y += paddle2_dy

    # Keep Paddles on Screen
    paddle1.y = max(0, min(SCREEN_HEIGHT - PADDLE_HEIGHT, paddle1.y))
    paddle2.y = max(0, min(SCREEN_HEIGHT - PADDLE_HEIGHT, paddle2.y))

    # Ball Movement
    ball.x += ball_dx
    ball.y += ball_dy

    # Ball Collision with Top/Bottom
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_dy = -ball_dy

    # Ball Collision with Paddles
    if ball.colliderect(paddle1) and ball_dx < 0:
        ball.left = paddle1.right
        ball_dx = -ball_dx * 1.05
        ball_dy *= 1.05
        ball_colors.append(random_color())
        current_color_index = (current_color_index + 1) % len(ball_colors)
        pygame.mixer.Sound.play(roar)
    if ball.colliderect(paddle2) and ball_dx > 0:
        ball.right = paddle2.left
        ball_dx = -ball_dx * 1.05
        ball_dy *= 1.05
        ball_colors.append(random_color())
        current_color_index = (current_color_index + 1) % len(ball_colors)
        pygame.mixer.Sound.play(bellsound)

    # Ball Out of Bounds
    if ball.left <= 0:
        score2 += 1
        reset_ball()
        pygame.mixer.Sound.play(roar)
    if ball.right >= SCREEN_WIDTH:
        score1 += 1
        reset_ball()
        pygame.mixer.Sound.play(bellsound)

    # Drawing
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, paddle1)
    pygame.draw.rect(screen, WHITE, paddle2)
    pygame.draw.ellipse(screen, ball_colors[current_color_index], ball)
    pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

    # Display Score
    score_text = font.render(f"{score1} - {score2}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 20))

    # Update Display
    pygame.display.flip()

    # Frame Rate
    pygame.time.Clock().tick(60)

pygame.quit()
