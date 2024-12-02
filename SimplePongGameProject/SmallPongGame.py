import pygame
import random
import time

# Function to generate a random color
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Function to reset the ball position
def reset_ball():
    global ball_dx, ball_dy
    ball.x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
    ball.y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
    if (score1 + score2) % 12 == 0:  # Reset speed only after 12 points
        ball_dx = BALL_SPEED_X * random.choice((1, -1))
        ball_dy = BALL_SPEED_Y * random.choice((1, -1))

if __name__ == "__main__":
# Initialize Pygame
    pygame.init()
# Initialize Pygame mixer for sound
    pygame.mixer.init()
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
    DOUBLE_TAP_SPEED = 18  # Speed when double-tap is detected
    BALL_SPEED_X = 4
    BALL_SPEED_Y = 4
    DOUBLE_TAP_THRESHOLD = 0.2  # Maximum time (seconds) for detecting a double-tap

    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Simple Pong Game")

    # Game objects
    paddle1 = pygame.Rect(50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    paddle2 = pygame.Rect(SCREEN_WIDTH - 50 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

    # Movement variables
    ball_dx = BALL_SPEED_X * random.choice((1, -1))
    ball_dy = BALL_SPEED_Y * random.choice((1, -1))
    paddle1_dy = 0
    paddle2_dy = 0

    # Score
    score1 = 0
    score2 = 0
    font = pygame.font.Font(None, 36)

    # Colors for the ball
    ball_colors = [WHITE]  # Start with one color (white)
    current_color_index = 0  # Index to track the current color of the ball

    # Timers for double-tap detection
    last_w_press = 0
    last_s_press = 0
    last_up_press = 0
    last_down_press = 0

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # Paddle 1 (W/S keys)
                if event.key == pygame.K_w:
                    current_time = time.time()
                    if current_time - last_w_press < DOUBLE_TAP_THRESHOLD:
                        paddle1_dy = -DOUBLE_TAP_SPEED
                    else:
                        paddle1_dy = -PADDLE_SPEED
                    last_w_press = current_time
                if event.key == pygame.K_s:
                    current_time = time.time()
                    if current_time - last_s_press < DOUBLE_TAP_THRESHOLD:
                        paddle1_dy = DOUBLE_TAP_SPEED
                    else:
                        paddle1_dy = PADDLE_SPEED
                    last_s_press = current_time

                # Paddle 2 (Arrow keys)
                if event.key == pygame.K_UP:
                    current_time = time.time()
                    if current_time - last_up_press < DOUBLE_TAP_THRESHOLD:
                        paddle2_dy = -DOUBLE_TAP_SPEED
                    else:
                        paddle2_dy = -PADDLE_SPEED
                    last_up_press = current_time
                if event.key == pygame.K_DOWN:
                    current_time = time.time()
                    if current_time - last_down_press < DOUBLE_TAP_THRESHOLD:
                        paddle2_dy = DOUBLE_TAP_SPEED
                    else:
                        paddle2_dy = PADDLE_SPEED
                    last_down_press = current_time

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
        if ball.colliderect(paddle1) and ball_dx < 0:  # Ball moving towards paddle1
            ball.left = paddle1.right  # Adjust ball position to the right of paddle1
            ball_dx = -ball_dx * 1.05  # Increase speed by 5%
            ball_dy *= 1.05  # Increase vertical speed by 5%
            new_color = random_color()
            ball_colors.append(new_color)  # Add a new random color to the list
            current_color_index = (current_color_index + 1) % len(ball_colors)  # Cycle through colors
            pygame.mixer.Sound.play(roar)
        if ball.colliderect(paddle2) and ball_dx > 0:  # Ball moving towards paddle2
            ball.right = paddle2.left  # Adjust ball position to the left of paddle2
            ball_dx = -ball_dx * 1.05  # Increase speed by 5%
            ball_dy *= 1.05  # Increase vertical speed by 5%
            new_color = random_color()
            ball_colors.append(new_color)  # Add a new random color to the list
            current_color_index = (current_color_index + 1) % len(ball_colors)  # Cycle through colors
            pygame.mixer.Sound.play(bellsound)
        # Ball out of bounds
        if ball.left <= 0:
            score2 += 1
            reset_ball()
            pygame.mixer.Sound.play(roar)
        if ball.right >= SCREEN_WIDTH:
            score1 += 1
            reset_ball()
            pygame.mixer.Sound.play(bellsound)

        if ball.colliderect(paddle1) and ball_dx < 0:  # Ball hits left paddle
            ball.left = paddle1.left
            ball_dx = -ball_dx * 1.05
            ball_dy *= 1.05
            pygame.mixer.Sound.play(roar)
        if ball.colliderect(paddle2) and ball_dx > 0:  # Ball hits right paddle
            ball.right = paddle2.left
            ball_dx = -ball_dx * 1.05
            ball_dy *= 1.05
            pygame.mixer.music.load(r'C:\Users\cheem\Downloads\ProgrammingInPython\Pythonlearning101\SimplePongGameProject\GameSounds\roar.mp3')
            pygame.mixer.music.play()


        # Draw game elements
        screen.fill(BLACK)  # Fill the screen with a black color before drawing
        pygame.draw.rect(screen, WHITE, paddle1)
        pygame.draw.rect(screen, WHITE, paddle2)
        pygame.draw.ellipse(screen, ball_colors[current_color_index], ball)  # Draw the ball with the current color
        pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

        # Draw the score
        score_text = font.render(f"{score1} - {score2}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 20))

        # Update the display
        pygame.display.flip()

        # Frame rate
        pygame.time.Clock().tick(60)

    pygame.quit()

    #NOTE- Try to orgranize the code better.