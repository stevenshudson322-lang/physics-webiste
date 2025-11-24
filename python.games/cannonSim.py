import pygame
import math
import random
from enum import Enum

class GameState(Enum):
    WAITING = 1
    AIMING = 2
    FIRING = 3
    HIT = 4

pygame.init()

WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cannon Projectile Game")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)

CANNON_X, CANNON_Y = 50, HEIGHT - 50
GRAVITY = 9.81
SCALE = 10
TIME_STEP = 0.016  # 60 FPS

cannon_angle = 45
cannon_velocity = 10
target_x, target_y = 0, 0
game_state = GameState.WAITING
trajectory = []
cannonball_pos = None
cannonball_vel = None
input_text = ""
input_mode = None  # None, "angle", or "velocity"

def draw_cannon():
    barrel_length = 25
    end_x = CANNON_X + barrel_length * math.cos(math.radians(cannon_angle))
    end_y = CANNON_Y - barrel_length * math.sin(math.radians(cannon_angle))
    # Draw cannon base (smaller)
    pygame.draw.circle(screen, BLACK, (CANNON_X, CANNON_Y), 10)
    pygame.draw.circle(screen, GRAY, (CANNON_X, CANNON_Y), 10, 2)
    # Draw barrel (thinner)
    pygame.draw.line(screen, BLACK, (CANNON_X, CANNON_Y), (end_x, end_y), 5)

def draw_target():
    pygame.draw.circle(screen, RED, (int(target_x), int(target_y)), 12)
    pygame.draw.circle(screen, WHITE, (int(target_x), int(target_y)), 8)
    pygame.draw.circle(screen, RED, (int(target_x), int(target_y)), 4)

def calculate_trajectory():
    global trajectory
    trajectory = []
    angle_rad = math.radians(cannon_angle)
    vx = cannon_velocity * math.cos(angle_rad)
    vy = cannon_velocity * math.sin(angle_rad)
    
    pos_x = CANNON_X
    pos_y = CANNON_Y
    vel_x = vx
    vel_y = -vy
    
    for _ in range(300):  # Max 5 seconds at 60 FPS
        pos_x += vel_x * TIME_STEP * SCALE
        pos_y += vel_y * TIME_STEP * SCALE
        vel_y += GRAVITY * TIME_STEP
        
        if pos_y > HEIGHT or pos_x > WIDTH:
            break
        trajectory.append((int(pos_x), int(pos_y)))

def draw_trajectory():
    for i, pos in enumerate(trajectory):
        if i % 2 == 0:
            pygame.draw.circle(screen, GREEN, pos, 3)

def update_cannonball():
    global cannonball_pos, cannonball_vel, game_state
    if cannonball_pos is None:
        return
    
    cannonball_pos[0] += cannonball_vel[0] * TIME_STEP * SCALE
    cannonball_pos[1] += cannonball_vel[1] * TIME_STEP * SCALE
    cannonball_vel[1] += GRAVITY * TIME_STEP
    
    if cannonball_pos[1] > HEIGHT or cannonball_pos[0] > WIDTH:
        game_state = GameState.WAITING
        cannonball_pos = None
        return
    
    if math.sqrt((cannonball_pos[0] - target_x)**2 + (cannonball_pos[1] - target_y)**2) < 20:
        pygame.display.set_caption("HIT! Press SPACE for next round")
        game_state = GameState.HIT
        cannonball_pos = None

def draw_cannonball():
    if cannonball_pos:
        pygame.draw.circle(screen, BLACK, (int(cannonball_pos[0]), int(cannonball_pos[1])), 5)
        pygame.draw.circle(screen, GRAY, (int(cannonball_pos[0]), int(cannonball_pos[1])), 5, 1)

def draw_measurement_scales():
    scale_font = pygame.font.Font(None, 28)
    
    # X-axis scale (horizontal distance: 0-100 meters)
    # Map screen width to 100 meters
    meter_per_pixel_x = 100 / (WIDTH - CANNON_X)
    
    # Draw x-axis line (thicker and darker)
    pygame.draw.line(screen, BLACK, (CANNON_X, HEIGHT - 30), (WIDTH, HEIGHT - 30), 3)
    
    # Draw x-axis markers and labels (every 50 pixels)
    for i in range(CANNON_X, WIDTH, 50):
        pygame.draw.line(screen, BLACK, (i, HEIGHT - 30), (i, HEIGHT - 15), 3)
        meters = int((i - CANNON_X) * meter_per_pixel_x)
        label = scale_font.render(f"{meters}m", True, BLACK)
        screen.blit(label, (i - 15, HEIGHT - 28))
    
    # Y-axis scale (height: 0-600 meters from bottom)
    meter_per_pixel_y = 600 / (HEIGHT - 100)
    
    # Draw y-axis line (thicker and darker)
    pygame.draw.line(screen, BLACK, (CANNON_X - 30, 100), (CANNON_X - 30, HEIGHT - 50), 3)
    
    # Draw y-axis markers and labels (every 50 pixels for clearer spacing)
    for i in range(100, HEIGHT - 50, 50):
        pygame.draw.line(screen, BLACK, (CANNON_X - 30, i), (CANNON_X - 10, i), 3)
        meters = int((HEIGHT - 50 - i) * meter_per_pixel_y)
        label = scale_font.render(f"{meters}m", True, BLACK)
        screen.blit(label, (CANNON_X - 75, i - 10))
    
    # Add axis labels (larger and more visible)
    axis_label_x = pygame.font.Font(None, 32).render("Distance (m)", True, BLACK)
    screen.blit(axis_label_x, (WIDTH - 180, HEIGHT - 55))
    
    axis_label_y = pygame.font.Font(None, 32).render("Height (m)", True, BLACK)
    screen.blit(axis_label_y, (CANNON_X - 150, 50))

running = True
while running:
    clock.tick(60)
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if input_mode == "angle":
                if event.key == pygame.K_RETURN and input_text:
                    try:
                        cannon_angle = float(input_text)
                        cannon_angle = max(0, min(90, cannon_angle))
                        input_text = ""
                        input_mode = "velocity"
                    except ValueError:
                        input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.unicode.isdigit() or event.unicode == '.':
                    input_text += event.unicode
            elif input_mode == "velocity":
                if event.key == pygame.K_RETURN and input_text:
                    try:
                        cannon_velocity = float(input_text)
                        cannon_velocity = max(1, min(50, cannon_velocity))
                        input_text = ""
                        input_mode = None
                        
                        # Launch the cannon
                        angle_rad = math.radians(cannon_angle)
                        barrel_length = 25
                        barrel_end_x = CANNON_X + barrel_length * math.cos(angle_rad)
                        barrel_end_y = CANNON_Y - barrel_length * math.sin(angle_rad)
                        cannonball_pos = [barrel_end_x, barrel_end_y]
                        cannonball_vel = [cannon_velocity * math.cos(angle_rad), -cannon_velocity * math.sin(angle_rad)]
                        game_state = GameState.FIRING
                        calculate_trajectory()
                    except ValueError:
                        input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.unicode.isdigit() or event.unicode == '.':
                    input_text += event.unicode
            elif event.key == pygame.K_SPACE and game_state == GameState.WAITING:
                target_x = random.randint(400, WIDTH - 50)
                target_y = random.randint(100, HEIGHT - 100)
                game_state = GameState.AIMING
                input_mode = "angle"
                input_text = ""
            elif event.key == pygame.K_SPACE and game_state == GameState.HIT:
                target_x = random.randint(400, WIDTH - 50)
                target_y = random.randint(100, HEIGHT - 100)
                game_state = GameState.AIMING
                input_mode = "angle"
                input_text = ""
    
    if game_state in [GameState.AIMING, GameState.FIRING]:
        draw_target()
    
    # Only show trajectory during firing
    if game_state == GameState.FIRING:
        draw_trajectory()
    
    draw_cannon()
    update_cannonball()
    draw_cannonball()
    draw_measurement_scales()
    
    ui_text = f"Angle: {cannon_angle:.1f}° | Velocity: {cannon_velocity:.1f} m/s"
    screen.blit(font.render(ui_text, True, BLACK), (10, 10))
    
    if game_state == GameState.WAITING:
        screen.blit(font.render("Press SPACE to START", True, BLUE), (400, 300))
    elif game_state == GameState.AIMING:
        if input_mode == "angle":
            screen.blit(font.render("Enter angle (0-90):", True, BLACK), (100, 100))
            screen.blit(font.render(input_text, True, BLUE), (100, 150))
        elif input_mode == "velocity":
            screen.blit(font.render("Enter velocity (1-50):", True, BLACK), (100, 100))
            screen.blit(font.render(input_text, True, BLUE), (100, 150))
    elif game_state == GameState.FIRING:
        screen.blit(font.render("FIRING!", True, RED), (100, 100))
    elif game_state == GameState.HIT:
        screen.blit(font.render("CONGRATS! You hit the target!", True, GREEN), (300, 300))
        screen.blit(font.render("Press SPACE for next round", True, BLUE), (300, 360))
    
    pygame.display.flip()

pygame.quit()