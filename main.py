import pygame
import random
import sys
import math

# --- Configuration Constants ---
WIDTH = 800
HEIGHT = 600
FPS = 60
GROUND_HEIGHT = HEIGHT - 100

# Colors (Sunset/Evening Theme)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_TOP = (40, 20, 60)
SKY_BOTTOM = (200, 100, 50)
ROOFTOP_COLOR = (40, 40, 45)

SPIDER_RED = (210, 30, 30)
SPIDER_BLUE = (30, 50, 150)
SPIDER_EYE = (240, 240, 240)

# Physics
GRAVITY = 0.6
JUMP_STRENGTH = -12

# Game Speeds
INITIAL_SPEED = 5
MAX_SPEED = 18
SPEED_INCREMENT = 0.15

class Player:
    """Represents Spider-Man."""
    def __init__(self):
        self.width = 40
        self.height = 60
        self.x = 100
        self.y = GROUND_HEIGHT - self.height
        self.vel_y = 0
        self.is_jumping = False
        self.animation_timer = 0
        self.state = "RUN" # RUN, JUMP, FALL, LAND

    def jump(self):
        if not self.is_jumping:
            self.vel_y = JUMP_STRENGTH
            self.is_jumping = True
            self.state = "JUMP"

    def update(self):
        self.vel_y += GRAVITY
        self.y += self.vel_y

        if self.vel_y > 0 and self.is_jumping:
            self.state = "FALL"

        if self.y >= GROUND_HEIGHT - self.height:
            self.y = GROUND_HEIGHT - self.height
            self.vel_y = 0
            self.is_jumping = False
            self.state = "RUN"
            
        self.animation_timer += 1

    def draw(self, surface):
        # Spider-man proportions
        head_radius = 12
        head_x = self.x + self.width // 2
        head_y = self.y + 12
        
        body_rect = (self.x + 10, self.y + 20, 20, 25)
        
        if self.state == "RUN":
            # Running pose
            offset = math.sin(self.animation_timer * 0.4) * 12
            # Back leg (Blue)
            pygame.draw.line(surface, SPIDER_BLUE, (self.x + 20, self.y + 40), (self.x + 20 - offset, self.y + 60), 6)
            # Back arm (Red)
            pygame.draw.line(surface, SPIDER_RED, (self.x + 20, self.y + 25), (self.x + 20 + offset, self.y + 45), 5)
            
            # Body (Blue sides, Red middle)
            pygame.draw.rect(surface, SPIDER_BLUE, body_rect)
            pygame.draw.rect(surface, SPIDER_RED, (self.x + 15, self.y + 20, 10, 25))
            
            # Front leg (Blue/Red boot)
            pygame.draw.line(surface, SPIDER_BLUE, (self.x + 20, self.y + 40), (self.x + 20 + offset, self.y + 55), 6)
            pygame.draw.circle(surface, SPIDER_RED, (int(self.x + 20 + offset), self.y + 58), 4) # boot
            
            # Front arm (Red)
            pygame.draw.line(surface, SPIDER_RED, (self.x + 20, self.y + 25), (self.x + 20 - offset, self.y + 40), 5)
            
            # Head (Red) leaning forward slightly
            pygame.draw.circle(surface, SPIDER_RED, (head_x + 5, head_y), head_radius)
            # Eyes (White polygon)
            pygame.draw.polygon(surface, SPIDER_EYE, [(head_x+5, head_y-4), (head_x+12, head_y-6), (head_x+10, head_y), (head_x+3, head_y)])
            
        elif self.state == "JUMP" or self.state == "FALL":
            # Dynamic superhero jumping pose
            # Body angled up
            pygame.draw.rect(surface, SPIDER_BLUE, body_rect)
            pygame.draw.rect(surface, SPIDER_RED, (self.x + 15, self.y + 20, 10, 25))
            
            # Knees bent
            # Back leg tucked
            pygame.draw.line(surface, SPIDER_BLUE, (self.x + 20, self.y + 40), (self.x + 5, self.y + 45), 6)
            pygame.draw.line(surface, SPIDER_RED, (self.x + 5, self.y + 45), (self.x + 10, self.y + 55), 5)
            # Front leg extended slightly
            pygame.draw.line(surface, SPIDER_BLUE, (self.x + 20, self.y + 40), (self.x + 30, self.y + 50), 6)
            pygame.draw.line(surface, SPIDER_RED, (self.x + 30, self.y + 50), (self.x + 35, self.y + 45), 5)
            
            # Arms swinging up/out
            if self.state == "JUMP":
                # Arm up
                pygame.draw.line(surface, SPIDER_RED, (self.x + 20, self.y + 25), (self.x + 35, self.y + 10), 5)
                pygame.draw.line(surface, SPIDER_RED, (self.x + 20, self.y + 25), (self.x + 5, self.y + 10), 5)
            else: # FALL
                # Arm out/down
                pygame.draw.line(surface, SPIDER_RED, (self.x + 20, self.y + 25), (self.x + 35, self.y + 35), 5)
                pygame.draw.line(surface, SPIDER_RED, (self.x + 20, self.y + 25), (self.x + 5, self.y + 35), 5)
            
            # Head looking forward/up
            pygame.draw.circle(surface, SPIDER_RED, (head_x, head_y), head_radius)
            pygame.draw.polygon(surface, SPIDER_EYE, [(head_x+2, head_y-4), (head_x+10, head_y-6), (head_x+8, head_y), (head_x, head_y)])
            
        # Draw some black web lines on the body/head (subtle)
        pygame.draw.line(surface, BLACK, (head_x, head_y-10), (head_x, head_y+10), 1)
        pygame.draw.line(surface, BLACK, (head_x-10, head_y), (head_x+10, head_y), 1)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Obstacle:
    """Represents a rooftop obstacle."""
    def __init__(self, game_speed, obs_type):
        self.obs_type = obs_type
        self.passed = False
        self.x = WIDTH + 50
        
        if obs_type == 'ac_unit':
            self.width = 40
            self.height = 35
            self.y = GROUND_HEIGHT - self.height
            self.color = (180, 180, 185)
            self.speed = game_speed
        elif obs_type == 'fireball': # We'll retheme this to a thrown goblin bomb or flying drone
            self.width = 25
            self.height = 25
            self.y = GROUND_HEIGHT - 50 - random.randint(0, 30)
            self.color = (255, 140, 0) # Pumpkin bomb color
            self.speed = game_speed * 1.3
        elif obs_type == 'barrier':
            self.width = 30
            self.height = 45
            self.y = GROUND_HEIGHT - self.height
            self.color = (255, 100, 0)
            self.speed = game_speed
        elif obs_type == 'water_tank':
            self.width = 45
            self.height = 90
            self.y = GROUND_HEIGHT - self.height
            self.color = (139, 100, 50)
            self.speed = game_speed
            
    def update(self, current_game_speed):
        if self.obs_type == 'fireball':
            self.x -= current_game_speed * 1.3
        else:
            self.x -= current_game_speed

    def draw(self, surface):
        if self.obs_type == 'fireball':
            # Goblin bomb
            center = (int(self.x + self.width/2), int(self.y + self.height/2))
            pygame.draw.circle(surface, self.color, center, int(self.width/2))
            pygame.draw.circle(surface, (0, 255, 0), center, int(self.width/4)) # Green center
        elif self.obs_type == 'ac_unit':
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
            pygame.draw.line(surface, BLACK, (self.x+10, self.y+5), (self.x+30, self.y+5), 2)
            pygame.draw.line(surface, BLACK, (self.x+10, self.y+15), (self.x+30, self.y+15), 2)
            pygame.draw.circle(surface, BLACK, (int(self.x+20), int(self.y+25)), 8, 1) # fan
        elif self.obs_type == 'barrier':
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
            # stripes
            pygame.draw.line(surface, WHITE, (self.x, self.y+10), (self.x+self.width, self.y+20), 4)
            pygame.draw.line(surface, WHITE, (self.x, self.y+30), (self.x+self.width, self.y+40), 4)
        elif self.obs_type == 'water_tank':
            # Wooden tank
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height-20))
            # Legs
            pygame.draw.rect(surface, (80, 80, 80), (self.x+5, self.y+self.height-20, 5, 20))
            pygame.draw.rect(surface, (80, 80, 80), (self.x+self.width-10, self.y+self.height-20, 5, 20))
            # Bands
            pygame.draw.line(surface, BLACK, (self.x, self.y+10), (self.x+self.width, self.y+10), 2)
            pygame.draw.line(surface, BLACK, (self.x, self.y+40), (self.x+self.width, self.y+40), 2)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class BuildingLayer:
    """Manages a scrolling layer of buildings for parallax effect."""
    def __init__(self, color_range, speed_factor, min_height, max_height, y_offset, width_range):
        self.buildings = []
        self.color_range = color_range
        self.speed_factor = speed_factor
        self.min_h = min_height
        self.max_h = max_height
        self.y_offset = y_offset
        self.w_range = width_range
        
        # Initial fill
        x = 0
        while x < WIDTH + 200:
            w = random.randint(*self.w_range)
            h = random.randint(self.min_h, self.max_h)
            c = self.get_color()
            self.buildings.append([x, w, h, c])
            x += w

    def get_color(self):
        c1, c2 = self.color_range
        r = random.randint(min(c1[0], c2[0]), max(c1[0], c2[0]))
        g = random.randint(min(c1[1], c2[1]), max(c1[1], c2[1]))
        b = random.randint(min(c1[2], c2[2]), max(c1[2], c2[2]))
        return (r, g, b)

    def update(self, game_speed):
        speed = game_speed * self.speed_factor
        for b in self.buildings:
            b[0] -= speed
            
        # Remove offscreen and add new
        if self.buildings[0][0] + self.buildings[0][1] < 0:
            self.buildings.pop(0)
            
        last_x = self.buildings[-1][0] + self.buildings[-1][1]
        if last_x < WIDTH + 200:
            w = random.randint(*self.w_range)
            h = random.randint(self.min_h, self.max_h)
            c = self.get_color()
            self.buildings.append([last_x, w, h, c])

    def draw(self, surface):
        for b in self.buildings:
            x, w, h, c = b
            y = self.y_offset - h
            pygame.draw.rect(surface, c, (x, y, w, h))
            
            # If foreground or midground, maybe draw windows
            if self.speed_factor > 0.2:
                # simple windows
                if w > 30 and h > 50:
                    for wx in range(int(x) + 5, int(x + w) - 10, 15):
                        for wy in range(int(y) + 10, int(y + h) - 10, 20):
                            if random.random() > 0.3: # 70% chance window is on
                                pygame.draw.rect(surface, (255, 255, 150), (wx, wy, 8, 12))


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Spider-Man Rooftop Runner")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.font = pygame.font.SysFont("Arial", 36, bold=True)
        self.large_font = pygame.font.SysFont("Arial", 64, bold=True)
        
        self.high_score = 0
        self.state = "START"
        self.reset_game()
        
    def reset_game(self):
        self.player = Player()
        self.obstacles = []
        
        # Parallax Layers
        # Distant Skyline
        self.layer_far = BuildingLayer(((20, 15, 30), (30, 20, 40)), 0.1, 100, 300, GROUND_HEIGHT, (50, 100))
        # Midground Skyscrapers
        self.layer_mid = BuildingLayer(((40, 30, 50), (60, 40, 70)), 0.4, 200, 450, GROUND_HEIGHT, (80, 150))
        
        self.score = 0
        self.game_speed = INITIAL_SPEED
        self.spawn_timer = 0
        self.spawn_interval = 90
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.state == "START":
                        self.state = "PLAYING"
                    elif self.state == "PLAYING":
                        self.player.jump()
                    elif self.state == "GAME_OVER":
                        self.reset_game()
                        self.state = "PLAYING"
                        
    def spawn_obstacle(self):
        obs_types = ['ac_unit', 'ac_unit', 'barrier', 'barrier', 'water_tank', 'fireball']
        
        if self.score > 15:
            obs_type = random.choice(obs_types)
        elif self.score > 5:
            obs_type = random.choice(obs_types[:5])
        else:
            obs_type = random.choice(obs_types[:4])
            
        self.obstacles.append(Obstacle(self.game_speed, obs_type))
        
        min_interval = max(40, int(90 - self.game_speed * 3))
        max_interval = max(70, int(150 - self.game_speed * 3))
        self.spawn_interval = random.randint(min_interval, max_interval)

    def update(self):
        if self.state != "PLAYING":
            return
            
        self.player.update()
        
        self.layer_far.update(self.game_speed)
        self.layer_mid.update(self.game_speed)
        
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_obstacle()
            self.spawn_timer = 0
            
        for obs in self.obstacles[:]:
            obs.update(self.game_speed)
            
            if self.player.get_rect().colliderect(obs.get_rect()):
                self.state = "GAME_OVER"
                if self.score > self.high_score:
                    self.high_score = self.score
                    
            if not obs.passed and obs.x + obs.width < self.player.x:
                obs.passed = True
                self.score += 1
                self.game_speed = min(MAX_SPEED, self.game_speed + SPEED_INCREMENT)
                
            if obs.x + obs.width < 0:
                self.obstacles.remove(obs)
                
    def draw_text(self, text, font, color, x, y, center=False):
        surface = font.render(text, True, color)
        rect = surface.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        self.screen.blit(surface, rect)
        
    def draw_sky(self):
        for y in range(HEIGHT):
            r = int(SKY_TOP[0] + (SKY_BOTTOM[0] - SKY_TOP[0]) * (y / HEIGHT))
            g = int(SKY_TOP[1] + (SKY_BOTTOM[1] - SKY_TOP[1]) * (y / HEIGHT))
            b = int(SKY_TOP[2] + (SKY_BOTTOM[2] - SKY_TOP[2]) * (y / HEIGHT))
            pygame.draw.line(self.screen, (r, g, b), (0, y), (WIDTH, y))

    def draw(self):
        self.draw_sky()
        
        self.layer_far.draw(self.screen)
        self.layer_mid.draw(self.screen)
        
        # Draw foreground rooftop
        pygame.draw.rect(self.screen, ROOFTOP_COLOR, (0, GROUND_HEIGHT, WIDTH, HEIGHT - GROUND_HEIGHT))
        pygame.draw.line(self.screen, (80, 80, 90), (0, GROUND_HEIGHT), (WIDTH, GROUND_HEIGHT), 6)
        
        if self.state == "START":
            self.draw_text("SPIDER-MAN ROOFTOP RUNNER", self.large_font, WHITE, WIDTH//2, HEIGHT//3, center=True)
            self.draw_text("Press SPACE to Start", self.font, WHITE, WIDTH//2, HEIGHT//2, center=True)
            self.draw_text("Use SPACE to Jump", self.font, (200, 200, 200), WIDTH//2, HEIGHT//2 + 50, center=True)
            
        elif self.state == "PLAYING":
            self.player.draw(self.screen)
            for obs in self.obstacles:
                obs.draw(self.screen)
                
            self.draw_text(f"Score: {self.score}", self.font, WHITE, WIDTH - 160, 20)
            self.draw_text(f"HI: {self.high_score}", self.font, WHITE, WIDTH - 160, 60)
            
        elif self.state == "GAME_OVER":
            self.player.draw(self.screen)
            for obs in self.obstacles:
                obs.draw(self.screen)
                
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(150)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            self.draw_text("GAME OVER", self.large_font, WHITE, WIDTH//2, HEIGHT//3, center=True)
            self.draw_text(f"Final Score: {self.score}", self.font, WHITE, WIDTH//2, HEIGHT//2, center=True)
            if self.score == self.high_score and self.score > 0:
                self.draw_text("NEW HIGH SCORE!", self.font, (255, 215, 0), WIDTH//2, HEIGHT//2 + 50, center=True)
            self.draw_text("Press SPACE to Restart", self.font, WHITE, WIDTH//2, HEIGHT//2 + 100, center=True)
            
        pygame.display.flip()
        
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
