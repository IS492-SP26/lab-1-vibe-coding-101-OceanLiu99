import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game objects
BALL_RADIUS = 10
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_vel = [5, 5]

PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
left_paddle_pos = [50, HEIGHT // 2 - PADDLE_HEIGHT // 2]
right_paddle_pos = [WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2]
PADDLE_SPEED = 10

# Scores
left_score = 0
right_score = 0
FONT = pygame.font.Font(None, 50)

def draw_objects():
    SCREEN.fill(BLACK)
    pygame.draw.circle(SCREEN, WHITE, (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)
    pygame.draw.rect(SCREEN, WHITE, (left_paddle_pos[0], left_paddle_pos[1], PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(SCREEN, WHITE, (right_paddle_pos[0], right_paddle_pos[1], PADDLE_WIDTH, PADDLE_HEIGHT))

    left_score_text = FONT.render(str(left_score), True, WHITE)
    right_score_text = FONT.render(str(right_score), True, WHITE)
    SCREEN.blit(left_score_text, (WIDTH // 4, 50))
    SCREEN.blit(right_score_text, (WIDTH * 3 // 4, 50))

def update():
    global left_score, right_score

    # Ball movement
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Ball collision with walls
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]

    # Ball collision with paddles
    if (left_paddle_pos[0] < ball_pos[0] - BALL_RADIUS < left_paddle_pos[0] + PADDLE_WIDTH and
            left_paddle_pos[1] < ball_pos[1] < left_paddle_pos[1] + PADDLE_HEIGHT):
        ball_vel[0] = -ball_vel[0]

    if (right_paddle_pos[0] < ball_pos[0] + BALL_RADIUS < right_paddle_pos[0] + PADDLE_WIDTH and
            right_paddle_pos[1] < ball_pos[1] < right_paddle_pos[1] + PADDLE_HEIGHT):
        ball_vel[0] = -ball_vel[0]

    # Scoring
    if ball_pos[0] <= BALL_RADIUS:
        right_score += 1
        reset_ball()
    elif ball_pos[0] >= WIDTH - BALL_RADIUS:
        left_score += 1
        reset_ball()

def reset_ball():
    ball_pos[0] = WIDTH // 2
    ball_pos[1] = HEIGHT // 2
    ball_vel[0] = -ball_vel[0]
    ball_vel[1] = 5

def main():
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and left_paddle_pos[1] > 0:
            left_paddle_pos[1] -= PADDLE_SPEED
        if keys[pygame.K_s] and left_paddle_pos[1] < HEIGHT - PADDLE_HEIGHT:
            left_paddle_pos[1] += PADDLE_SPEED
        if keys[pygame.K_UP] and right_paddle_pos[1] > 0:
            right_paddle_pos[1] -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and right_paddle_pos[1] < HEIGHT - PADDLE_HEIGHT:
            right_paddle_pos[1] += PADDLE_SPEED

        update()
        draw_objects()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
