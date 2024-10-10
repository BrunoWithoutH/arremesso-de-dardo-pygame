import pygame
import math
import random

pygame.init()

WIDTH, HEIGHT = 1300, 500
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (135, 206, 235)  # Cor do céu
BLACK = (0, 0, 0)
DARK_GREEN = (34, 139, 34)  # Cor de grama
PURPLE = (128, 0, 128)

dart_pos = [100, HEIGHT - 44]
dart_vel = [0, 0]
launched = False
charging = False
charge_start_time = 0
force = 0
crashed_angle = 0
angulo_arremesso = None

character_pos = [100, HEIGHT - 44]

def update_dart(dt):
    global dart_pos, dart_vel
    gravity = 9.81 * 20
    dart_vel[1] += gravity * dt
    dart_pos[0] += dart_vel[0] * dt
    dart_pos[1] += dart_vel[1] * dt

def main():
    global dart_pos, dart_vel, launched, charging, charge_start_time, force, crashed_angle

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Arremesso de Dardo")

    clock = pygame.time.Clock()
    running = True
    font = pygame.font.SysFont(None, 36)
    distance = 0

    while running:
        dt = clock.tick(60) / 1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not launched:
                    charging = True
                    dart_pos = [100, HEIGHT - 44]
                    dart_vel = [0, 0]
                    distance = 0
                    charge_start_time = pygame.time.get_ticks()
                if event.key == pygame.K_r:
                    dart_pos = [100, HEIGHT - 44]
                    dart_vel = [0, 0]
                    distance = 0
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    charging = False
                    angulo_arremesso = random.uniform(32, 47)
                    angle = math.radians(angulo_arremesso)
                    dart_vel[0] = force * math.cos(angle)
                    dart_vel[1] = -force * math.sin(angle)
                    launched = True
                    force = 0
        
        if charging:
            elapsed_time = (pygame.time.get_ticks() - charge_start_time) / 1000
            force = min(1000, int(elapsed_time * 200))
        
        if launched:
            update_dart(dt)
            if dart_pos[1] > HEIGHT - 10:
                dart_pos[1] = HEIGHT - 10
                dart_vel = [0, 0]
                launched = False
                crashed_angle = 45
                distance = (dart_pos[0] - 100 + 15) / 10  # Ajuste para contar a partir da ponta do dardo

        screen.fill(BLUE)
        pygame.draw.rect(screen, DARK_GREEN, (0, HEIGHT - 10, WIDTH, 10))
        
        for i in range(10, 110, 10):
            x = 100 + i * 10
            pygame.draw.line(screen, BLACK, (x, HEIGHT - 10), (x, HEIGHT - 20), 2)
            label = font.render(f"{i}m", True, BLACK)
            screen.blit(label, (x - 10, HEIGHT - 40))
        
        if launched or not launched:
            angle = math.degrees(math.atan2(dart_vel[1], dart_vel[0])) if launched else crashed_angle
        
        dart_image = pygame.Surface((41, 5), pygame.SRCALPHA)
        pygame.draw.line(dart_image, PURPLE, (0, 2), (41, 2), 3)
        rotated_dart = pygame.transform.rotate(dart_image, -angle)
        dart_rect = rotated_dart.get_rect(center=(int(dart_pos[0]), int(dart_pos[1]) - 13))  # Ajuste para cravar no chão
        screen.blit(rotated_dart, dart_rect.topleft)
        
        pygame.draw.rect(screen, (220, 220, 240), (*character_pos, 10, 24))  # Corpo do personagem
        pygame.draw.rect(screen, BLACK, (character_pos[0], character_pos[1] + 24, 10, 10))  # Calção do personagem
        distance_text = font.render(f"Distância: {distance:.2f} metros", True, BLACK)
        if launched:
            angle_text = font.render(f"Ângulo: {angulo_arremesso:.1f}°", True, BLACK)
            screen.blit(angle_text, (10, 50))
        screen.blit(distance_text, (10, 10))
        
        
        if charging:
            pygame.draw.rect(screen, GREEN, (10, 50, force, 20))
            pygame.draw.rect(screen, BLACK, (10, 50, 500, 20), 2)
        
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()