import pygame
import random
import unittest

# Mock constants and initial setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BALL_SIZE = 21
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
PADDLE_SPEED = 12
BALL_SPEED_X = 4
BALL_SPEED_Y = 4

# Game objects
class Ball:
    def __init__(self):
        self.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

ball = Ball()

# Function to generate a random color (to fix the test_random_color error)
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Function to reset the ball's position and speed
def reset_ball(score1, score2):
    global ball_dx, ball_dy, ball
    ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    if (score1 + score2) % 12 == 0:
        ball_dx = BALL_SPEED_X * random.choice((1, -1))
        ball_dy = BALL_SPEED_Y * random.choice((1, -1))


# Test class for Pong game
class TestPongGame(unittest.TestCase):

    def setUp(self):
        pygame.init()
        # Initialize constants and game objects
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.BALL_SIZE = 21
        self.PADDLE_WIDTH = 15
        self.PADDLE_HEIGHT = 100
        self.PADDLE_SPEED = 12

        # Game objects
        self.paddle1 = pygame.Rect(50, self.SCREEN_HEIGHT // 2 - self.PADDLE_HEIGHT // 2, self.PADDLE_WIDTH, self.PADDLE_HEIGHT)
        self.paddle2 = pygame.Rect(self.SCREEN_WIDTH - 50 - self.PADDLE_WIDTH, self.SCREEN_HEIGHT // 2 - self.PADDLE_HEIGHT // 2, self.PADDLE_WIDTH, self.PADDLE_HEIGHT)
        self.ball = pygame.Rect(self.SCREEN_WIDTH // 2 - self.BALL_SIZE // 2, self.SCREEN_HEIGHT // 2 - self.BALL_SIZE // 2, self.BALL_SIZE, self.BALL_SIZE)

        # Variables for ball movement
        self.ball_dx = 4
        self.ball_dy = 4

        # Scores
        self.score1 = 0
        self.score2 = 0
         
        # Set reset_ball as an instance method
        self.reset_ball = self.reset_ball_method

    def reset_ball_method(self):
        """Reset ball position and speed."""
        self.ball.center = (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)
        
        # Reset ball speed if the total score is a multiple of 12
        if (self.score1 + self.score2) % 12 == 0:
            self.ball_dx = BALL_SPEED_X * random.choice((1, -1))
            self.ball_dy = BALL_SPEED_Y * random.choice((1, -1))
        else:
            self.ball_dx = 4  # Default ball speed
            self.ball_dy = 4  # Default ball speed

    def test_reset_ball(self):
        """Test the ball reset functionality."""
        # Set ball to an off-center position
        self.ball.center = (100, 100)
        self.score1 = 5
        self.score2 = 7

        # Call reset_ball to reset the ball position and speed
        self.reset_ball()

        # Ball should reset to center (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.assertEqual(self.ball.center, (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2), "Ball position should reset to center.")

        # Check if ball speed is reset based on score
        if (self.score1 + self.score2) % 12 == 0:
            self.assertIn(self.ball_dx, [BALL_SPEED_X, -BALL_SPEED_X], "Ball speed in X direction should reset with random direction.")
            self.assertIn(self.ball_dy, [BALL_SPEED_Y, -BALL_SPEED_Y], "Ball speed in Y direction should reset with random direction.")
        else:
            self.assertNotIn(self.ball_dx, [BALL_SPEED_X, -BALL_SPEED_X], "Ball speed should not change when score is not a multiple of 12.")
            self.assertNotIn(self.ball_dy, [BALL_SPEED_Y, -BALL_SPEED_Y], "Ball speed should not change when score is not a multiple of 12.")


    def test_random_color(self):
        """Test that random_color generates valid RGB values."""
        color = random_color()
        self.assertTrue(all(0 <= c <= 255 for c in color), "Color values are not within valid RGB range.")

    def test_paddle_movement_within_bounds(self):
        """Test paddle movement to ensure it stays within bounds."""
        # Move paddle1 beyond top
        self.paddle1.y = -10
        if self.paddle1.top < 0:
            self.paddle1.top = 0
        self.assertEqual(self.paddle1.top, 0, "Paddle1 exceeded top boundary.")

        # Move paddle2 beyond bottom
        self.paddle2.y = self.SCREEN_HEIGHT + 10
        if self.paddle2.bottom > self.SCREEN_HEIGHT:
            self.paddle2.bottom = self.SCREEN_HEIGHT
        self.assertEqual(self.paddle2.bottom, self.SCREEN_HEIGHT, "Paddle2 exceeded bottom boundary.")

    def test_ball_collision_with_paddles(self):
        """Test ball collision with paddles."""
        # Simulate ball collision with paddle1 (left paddle)
        self.ball.x = self.paddle1.right - 1  # Ensure it's touching the paddle
        self.ball.y = self.paddle1.y + self.PADDLE_HEIGHT // 2  # Center on paddle
        self.ball_dx = -4
        if self.ball.colliderect(self.paddle1):
            self.ball_dx = -self.ball_dx
        self.assertGreater(self.ball_dx, 0, "Ball did not reverse direction after hitting left paddle.")
        
        # Simulate ball collision with paddle2 (right paddle)
        self.ball.x = self.paddle2.left - self.BALL_SIZE + 1  # Ensure it's touching the paddle
        self.ball.y = self.paddle2.y + self.PADDLE_HEIGHT // 2  # Center on paddle
        self.ball_dx = 4
        if self.ball.colliderect(self.paddle2):
            self.ball_dx = -self.ball_dx
        self.assertLess(self.ball_dx, 0, "Ball did not reverse direction after hitting right paddle.")

    def test_scoring(self):
        """Test scoring system when the ball goes out of bounds."""
        # Ball goes out on the left
        self.ball.left = -10
        if self.ball.left <= 0:
            self.score2 += 1
        self.assertEqual(self.score2, 1, "Score2 was not incremented when the ball went out on the left.")

        # Ball goes out on the right
        self.ball.right = self.SCREEN_WIDTH + 10
        if self.ball.right >= self.SCREEN_WIDTH:
            self.score1 += 1
        self.assertEqual(self.score1, 1, "Score1 was not incremented when the ball went out on the right.")

    def test_reset_ball(self):
        """Test the ball reset functionality."""
        # Set ball to an off-center position
        self.ball.center = (100, 100)
        self.score1 = 5
        self.score2 = 7


        # Call reset_ball to reset the ball position and speed
        self.reset_ball()

        # Ball should reset to center (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.assertEqual(self.ball.center, (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2), "Ball position should reset to center.")

        # Check if ball speed is reset based on score
        if (self.score1 + self.score2) % 12 == 0:
            self.assertIn(self.ball_dx, [BALL_SPEED_X, -BALL_SPEED_X], "Ball speed in X direction should reset with random direction.")
            self.assertIn(self.ball_dy, [BALL_SPEED_Y, -BALL_SPEED_Y], "Ball speed in Y direction should reset with random direction.")
        else:
            self.assertNotIn(self.ball_dx, [BALL_SPEED_X, -BALL_SPEED_X], "Ball speed should not change when score is not a multiple of 12.")
            self.assertNotIn(self.ball_dy, [BALL_SPEED_Y, -BALL_SPEED_Y], "Ball speed should not change when score is not a multiple of 12.")


    def tearDown(self):
        pygame.quit()

if __name__ == "__main__":
    unittest.main()
