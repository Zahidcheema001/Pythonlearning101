import random
import pygame
import unittest

# Mock constants and initial setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BALL_SPEED_X = 5
BALL_SPEED_Y = 5
score1 = 0
score2 = 0

# Mock ball object
class Ball:
    def __init__(self):
        self.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

ball = Ball()

# Function to be tested
def reset_ball():
    global ball_dx, ball_dy, ball
    ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    if (score1 + score2) % 12 == 0:
        ball_dx = BALL_SPEED_X * random.choice((1, -1))
        ball_dy = BALL_SPEED_Y * random.choice((1, -1))

# Test case for the reset_ball function
class TestResetBall(unittest.TestCase):
    def test_ball_position(self):
        # Before reset
        ball.center = (100, 100)
        reset_ball()
        self.assertEqual(ball.center, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), "Ball position should reset to center.")
    
    def test_ball_speed_reset(self):
        global ball_dx, ball_dy, score1, score2
        score1 = 5
        score2 = 7
        reset_ball()
        # Ball speed should reset when score1 + score2 is a multiple of 12
        if (score1 + score2) % 12 == 0:
            self.assertIn(ball_dx, [BALL_SPEED_X, -BALL_SPEED_X], "Ball speed in X direction should reset with random direction.")
            self.assertIn(ball_dy, [BALL_SPEED_Y, -BALL_SPEED_Y], "Ball speed in Y direction should reset with random direction.")
        else:
            self.assertNotIn(ball_dx, [BALL_SPEED_X, -BALL_SPEED_X], "Ball speed should not change when score is not a multiple of 12.")
            self.assertNotIn(ball_dy, [BALL_SPEED_Y, -BALL_SPEED_Y], "Ball speed should not change when score is not a multiple of 12.")

if __name__ == "__main__":
    unittest.main()
