# may-313
#https://github.com/may-313

# ----------------------------------
import pygame
import random

# Initialize Pygame
pygame.init()

# ------------------- Constants -------------------
WIDTH, HEIGHT = 800, 600
BALL_SPEED = 7
PADDLE_SPEED = 7

# Colors (RGB)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# ------------------- Game Variables -------------------
score1 = 0
score2 = 0
player1_name = "A"
player2_name = "B"

# Ball and Paddles
ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
paddle1 = pygame.Rect(50, HEIGHT // 2 - 60, 10, 120)
paddle2 = pygame.Rect(WIDTH - 60, HEIGHT // 2 - 60, 10, 120)

# Ball movement direction
ball_dx = BALL_SPEED * random.choice((1, -1))
ball_dy = BALL_SPEED * random.choice((1, -1))

# Paddle movement
paddle1_dy = 0
paddle2_dy = 0

# Ball state
ball_in_motion = True

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")

# ------------------- Functions -------------------
def draw_scores():
    """Draw player scores on the screen."""
    font = pygame.font.Font(None, 36)
    score1_text = font.render(f"{player1_name}: {score1}", True, GREEN)
    score2_text = font.render(f"{player2_name}: {score2}", True, GREEN)
    screen.blit(score1_text, (10, 10))
    screen.blit(score2_text, (WIDTH - score2_text.get_width() - 10, 10))

def check_collision(ball, paddle):
    """Check if the ball collides with a paddle."""
    return ball.colliderect(paddle)

def reset_ball_position():
    """Reset ball to the center and set initial direction randomly."""
    global ball
    side = random.choice(('left', 'right'))
    if side == 'left':
        ball.x = paddle1.right + 10
        ball_dx = BALL_SPEED
    else:
        ball.x = paddle2.left - ball.width - 10
        ball_dx = -BALL_SPEED
    ball.y = HEIGHT // 2 - ball.height // 2
    return ball_dx

# ------------------- Main Game Loop -------------------
running = True
while running:
    # ------------------- Event Handling -------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                paddle2_dy = -PADDLE_SPEED
            elif event.key == pygame.K_DOWN:
                paddle2_dy = PADDLE_SPEED
            elif event.key == pygame.K_SPACE:
                ball_in_motion = True
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                paddle2_dy = 0

    # Player 1 controls (W and S)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddle1_dy = -PADDLE_SPEED
    elif keys[pygame.K_s]:
        paddle1_dy = PADDLE_SPEED
    else:
        paddle1_dy = 0

    # ------------------- Ball Movement -------------------
    if ball_in_motion:
        ball.x += ball_dx
        ball.y += ball_dy

    # Ball collision with top/bottom walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_dy *= -1

    # Ball collision with paddles
    if check_collision(ball, paddle1) or check_collision(ball, paddle2):
        ball_dx *= -1

    # Ball out of bounds - scoring
    if ball.left <= 0:
        score2 += 1
        if score2 == 5:
            running = False
        else:
            ball_dx = reset_ball_position()
            ball_in_motion = False
    elif ball.right >= WIDTH:
        score1 += 1
        if score1 == 5:
            running = False
        else:
            ball_dx = reset_ball_position()
            ball_in_motion = False

    # ------------------- Paddle Movement -------------------
    paddle1.y += paddle1_dy
    paddle2.y += paddle2_dy

    # Keep paddles on screen
    if paddle1.top < 0:
        paddle1.top = 0
    if paddle1.bottom > HEIGHT:
        paddle1.bottom = HEIGHT
    if paddle2.top < 0:
        paddle2.top = 0
    if paddle2.bottom > HEIGHT:
        paddle2.bottom = HEIGHT

# ------------------- Drawing -------------------
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, paddle1)
    pygame.draw.rect(screen, WHITE, paddle2)
    pygame.draw.ellipse(screen, RED, ball)
    draw_scores()

    # Update the display
    pygame.display.flip()

    # Control frame rate
    pygame.time.delay(30)

# Quit Pygame
pygame.quit()