import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Game objects
BALL_RADIUS = 10
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_vel = [random.choice([-5, 5]), random.choice([-5, 5])]

PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
left_paddle_pos = [50, HEIGHT // 2 - PADDLE_HEIGHT // 2]
right_paddle_pos = [WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2]
PADDLE_SPEED = 7

# Scores
left_score = 0
right_score = 0
FONT = pygame.font.Font(None, 50)
WINNING_SCORE = 5

def draw_objects():
    SCREEN.fill(BLACK)

    # Draw center line
    pygame.draw.line(SCREEN, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)

    # Draw ball
    pygame.draw.circle(SCREEN, WHITE, (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)

    # Draw paddles
    pygame.draw.rect(SCREEN, BLUE, (left_paddle_pos[0], left_paddle_pos[1], PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(SCREEN, RED, (right_paddle_pos[0], right_paddle_pos[1], PADDLE_WIDTH, PADDLE_HEIGHT))

    # Draw scores
    left_score_text = FONT.render(str(left_score), True, WHITE)
    right_score_text = FONT.render(str(right_score), True, WHITE)
    SCREEN.blit(left_score_text, (WIDTH // 4, 50))
    SCREEN.blit(right_score_text, (WIDTH * 3 // 4, 50))

    # Draw instructions
    font_small = pygame.font.Font(None, 24)
    instructions = [
        "Left Player: W/S keys",
        "Right Player: Up/Down arrows",
        "First to 5 points wins!",
        "Press R to restart"
    ]
    for i, text in enumerate(instructions):
        instr_text = font_small.render(text, True, WHITE)
        SCREEN.blit(instr_text, (20, HEIGHT - 100 + i * 25))

def update():
    global left_score, right_score

    # Ball movement
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Ball collision with top and bottom walls
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]

    # Ball collision with paddles
    # Left paddle
    if (ball_pos[0] - BALL_RADIUS <= left_paddle_pos[0] + PADDLE_WIDTH and
        ball_pos[0] - BALL_RADIUS >= left_paddle_pos[0] and
        left_paddle_pos[1] <= ball_pos[1] <= left_paddle_pos[1] + PADDLE_HEIGHT):
        ball_vel[0] = -ball_vel[0]
        # Add some randomness to make it more interesting
        ball_vel[1] += random.uniform(-2, 2)

    # Right paddle
    if (ball_pos[0] + BALL_RADIUS >= right_paddle_pos[0] and
        ball_pos[0] + BALL_RADIUS <= right_paddle_pos[0] + PADDLE_WIDTH and
        right_paddle_pos[1] <= ball_pos[1] <= right_paddle_pos[1] + PADDLE_HEIGHT):
        ball_vel[0] = -ball_vel[0]
        # Add some randomness
        ball_vel[1] += random.uniform(-2, 2)

    # Limit ball speed
    if abs(ball_vel[0]) > 8:
        ball_vel[0] = 8 if ball_vel[0] > 0 else -8
    if abs(ball_vel[1]) > 8:
        ball_vel[1] = 8 if ball_vel[1] > 0 else -8

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
    ball_vel[0] = random.choice([-5, 5])
    ball_vel[1] = random.choice([-5, 5])

def check_winner():
    if left_score >= WINNING_SCORE:
        return "Left Player Wins!"
    elif right_score >= WINNING_SCORE:
        return "Right Player Wins!"
    return None

def draw_winner(winner_text):
    SCREEN.fill(BLACK)
    winner_font = pygame.font.Font(None, 70)
    winner_surface = winner_font.render(winner_text, True, WHITE)
    SCREEN.blit(winner_surface, (WIDTH // 2 - winner_surface.get_width() // 2, HEIGHT // 2 - 50))

    restart_font = pygame.font.Font(None, 30)
    restart_surface = restart_font.render("Press R to restart or Q to quit", True, WHITE)
    SCREEN.blit(restart_surface, (WIDTH // 2 - restart_surface.get_width() // 2, HEIGHT // 2 + 20))

    pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Reset game
                    global left_score, right_score
                    left_score = 0
                    right_score = 0
                    reset_ball()
                    game_over = False
                elif event.key == pygame.K_q and game_over:
                    pygame.quit()
                    sys.exit()

        if not game_over:
            # Handle paddle movement
            keys = pygame.key.get_pressed()

            # Left paddle (W/S)
            if keys[pygame.K_w] and left_paddle_pos[1] > 0:
                left_paddle_pos[1] -= PADDLE_SPEED
            if keys[pygame.K_s] and left_paddle_pos[1] < HEIGHT - PADDLE_HEIGHT:
                left_paddle_pos[1] += PADDLE_SPEED

            # Right paddle (Up/Down arrows)
            if keys[pygame.K_UP] and right_paddle_pos[1] > 0:
                right_paddle_pos[1] -= PADDLE_SPEED
            if keys[pygame.K_DOWN] and right_paddle_pos[1] < HEIGHT - PADDLE_HEIGHT:
                right_paddle_pos[1] += PADDLE_SPEED

            update()
            draw_objects()

            winner = check_winner()
            if winner:
                game_over = True
                draw_winner(winner)
            else:
                pygame.display.flip()
        else:
            # Game over screen - just wait for input
            pass

        clock.tick(60)

if __name__ == "__main__":
    main()