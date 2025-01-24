# import pygame
# import random
# import os

# # Initialize Pygame
# pygame.init()

# # Constants
# WIDTH, HEIGHT = 800, 600
# TILE_SIZE = 40  # Size of each tile in the maze
# # Color constants
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# GREEN = (0, 255, 0)
# FONT_COLOR = (255, 255, 0)  # Change this to yellow for better visibility
# FPS = 60

# FONT_SIZE = 48  # Increased font size
# FRAME_DELAY = 200  # Delay in milliseconds for frame transitions
# OVERLAY_COLOR = (0, 0, 0, 0)

# # Set up the display
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Maze Game")

# # Load the background image
# background_image = pygame.image.load('background_image.png').convert()

# # Maze generation (Recursive Backtracking)
# def generate_maze(width, height):
#     maze = [[1 for _ in range(width)] for _ in range(height)]
#     stack = []
#     start_x, start_y = random.randint(0, (width // 2) - 1) * 2 + 1, random.randint(0, (height // 2) - 1) * 2 + 1
#     maze[start_y][start_x] = 0
#     stack.append((start_x, start_y))

#     while stack:
#         x, y = stack[-1]
#         neighbors = []

#         for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
#             nx, ny = x + dx, y + dy
#             if 0 < nx < width and 0 < ny < height and maze[ny][nx] == 1:
#                 neighbors.append((nx, ny))

#         if neighbors:
#             nx, ny = random.choice(neighbors)
#             maze[(ny + y) // 2][(nx + x) // 2] = 0
#             maze[ny][nx] = 0
#             stack.append((nx, ny))
#         else:
#             stack.pop()

#     return maze

# # Ensure there's at least one valid path from start to end
# def ensure_path(maze, start, end):
#     x, y = start
#     path = [start]
    
#     while (x, y) != end:
#         if x < end[0]:  # Move right
#             x += 1
#         elif x > end[0]:  # Move left
#             x -= 1
#         elif y < end[1]:  # Move down
#             y += 1
#         elif y > end[1]:  # Move up
#             y -= 1
        
#         if maze[y][x] == 0:  # If the cell is not a wall
#             path.append((x, y))
#         else:
#             break  # If a wall is encountered, stop

#     # Convert the path to maze format
#     for px, py in path:
#         maze[py][px] = 0

# # Define classes for the game
# class Player:
#     def __init__(self):
#         self.rect = pygame.Rect(40, 40, 40, 40)    # Starting position of the player

#     def move(self, dx, dy):
#         if not self.collides(dx, dy):
#             self.rect.x += dx
#             self.rect.y += dy

#     def collides(self, dx, dy):
#         new_rect = self.rect.move(dx, dy)
#         for y in range(len(maze)):
#             for x in range(len(maze[y])):
#                 if maze[y][x] == 1:  # Wall
#                     wall_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
#                     if new_rect.colliderect(wall_rect):
#                         return True
#         return False

# class Game:
#     def __init__(self):
#         self.regenerate_maze()  # Generate initial maze

#     def regenerate_maze(self):
#         global maze, destination
#         maze = generate_maze(21, 21)  # Generate a new maze
#         start = (1, 1)  # Starting point
#         destination = self.set_destination()
#         print("Destination set at:", destination)  # Debug output

#         # Ensure there's a path from start to destination
#         ensure_path(maze, start, destination)

#         self.player = Player()
#         self.clock = pygame.time.Clock()
#         self.running = True
#         self.camera_x = 0
#         self.camera_y = 0
#         self.reached_destination = False  # Flag to check if destination is reached
#         self.message_displayed = False  # Flag to control message display

#     def set_destination(self):
#         while True:
#             x = random.randint(1, len(maze[0]) - 2)  # Ensure within bounds
#             y = random.randint(1, len(maze) - 2)  # Ensure within bounds
#             if maze[y][x] == 0:  # Ensure it's a path
#                 return (x, y)

#     def draw_maze(self):
#         for y in range(len(maze)):
#             for x in range(len(maze[y])):
#                 if maze[y][x] == 1:
#                     pygame.draw.rect(screen, BLACK, ((x * TILE_SIZE) - self.camera_x, (y * TILE_SIZE) - self.camera_y, TILE_SIZE, TILE_SIZE))

#     def draw_destination(self):
#         if destination:
#             dest_x, dest_y = destination
#             pygame.draw.rect(screen, GREEN, ((dest_x * TILE_SIZE) - self.camera_x, (dest_y * TILE_SIZE) - self.camera_y, TILE_SIZE, TILE_SIZE))  # Draw destination

#     def update_camera(self):
#         # Center the camera on the player, but keep it within the bounds of the maze
#         self.camera_x = max(0, min(self.player.rect.x - WIDTH // 2 + TILE_SIZE // 2, (len(maze[0]) - 1) * TILE_SIZE - WIDTH))
#         self.camera_y = max(0, min(self.player.rect.y - HEIGHT // 2 + TILE_SIZE // 2, (len(maze) - 1) * TILE_SIZE - HEIGHT))

#     def run(self):
#         while self.running:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     self.running = False

#             keys = pygame.key.get_pressed()
#             if keys[pygame.K_LEFT]:
#                 self.player.move(-TILE_SIZE, 0)  # Move left
#             if keys[pygame.K_RIGHT]:
#                 self.player.move(TILE_SIZE, 0)  # Move right
#             if keys[pygame.K_UP]:
#                 self.player.move(0, -TILE_SIZE)  # Move up
#             if keys[pygame.K_DOWN]:
#                 self.player.move(0, TILE_SIZE)  # Move down

#             # Check if the player has reached the destination
#             if (self.player.rect.x // TILE_SIZE, self.player.rect.y // TILE_SIZE) == destination:
#                 self.reached_destination = True

#             # Update camera position
#             self.update_camera()

#             # Drawing
#             screen.fill(WHITE)
#             self.draw_maze()  # Draw the maze
#             self.draw_destination()  # Draw the destination
#             pygame.draw.rect(screen, GREEN, (self.player.rect.x - self.camera_x, self.player.rect.y - self.camera_y, self.player.rect.width, self.player.rect.height))  # Draw player

#             # Handle success message and maze regeneration
#             if self.reached_destination:
#                 if not self.message_displayed:
#                     self.display_message("Destination Reached! Generating new maze...", 2000)  # Display message for 2 seconds
#                     self.message_displayed = True  # Set flag to prevent multiple messages
#                     self.regenerate_maze()  # Regenerate maze after displaying message
#                 else:
#                     # Reset flags to allow the message to show again
#                     self.reached_destination = False
#                     self.message_displayed = False

#             pygame.display.flip()
#             self.clock.tick(FPS)

#     def display_message(self, message, duration):
#         font = pygame.font.SysFont('Arial', 36)  # Set the font and size
#         text = font.render(message, True, FONT_COLOR)
#         screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
#         pygame.display.flip()
#         pygame.time.delay(duration)  # Wait for the specified duration


# class Menu:
#     def __init__(self):
#         self.clock = pygame.time.Clock()
#         self.font = pygame.font.SysFont('Arial', FONT_SIZE, bold=True)
#         self.play_music()
#         self.background_image = pygame.image.load('background_image.png').convert()

#     def play_music(self):
#         pygame.mixer.music.load('background_music.mp3')
#         pygame.mixer.music.play(-1)

#     def run(self):
#         while True:
#             screen.blit(self.background_image, (0, 0))

#             title_text = self.font.render("Maze Game", True, FONT_COLOR)
#             start_text = self.font.render("Press ENTER to Start", True, FONT_COLOR)
#             exit_text = self.font.render("Press ESC to Exit", True, FONT_COLOR)

#             screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
#             screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
#             screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 50))

#             overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
#             overlay.fill(OVERLAY_COLOR)
#             screen.blit(overlay, (0, 0))

#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     pygame.mixer.music.stop()
#                     pygame.quit()
#                     return
#                 if event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_RETURN:
#                         game = Game()
#                         pygame.mixer.music.stop()
#                         game.run()
#                     if event.key == pygame.K_ESCAPE:
#                         pygame.mixer.music.stop()
#                         pygame.quit()
#                         return

#             pygame.display.flip()
#             self.clock.tick(FPS)

# if __name__ == "__main__":
#     menu = Menu()
#     menu.run()


import pygame
import random
import os
from queue import PriorityQueue

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 40
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
FONT_COLOR = (255, 255, 0)
FPS = 60
FONT_SIZE = 48

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

# Load resources
background_image = pygame.image.load('background_image.png').convert()
pygame.mixer.music.load('background_music.mp3')

# Maze generation (Recursive Backtracking)
def generate_maze(width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]
    stack = []
    start_x, start_y = random.randint(0, (width // 2) - 1) * 2 + 1, random.randint(0, (height // 2) - 1) * 2 + 1
    maze[start_y][start_x] = 0
    stack.append((start_x, start_y))

    while stack:
        x, y = stack[-1]
        neighbors = []

        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            nx, ny = x + dx, y + dy
            if 0 < nx < width and 0 < ny < height and maze[ny][nx] == 1:
                neighbors.append((nx, ny))

        if neighbors:
            nx, ny = random.choice(neighbors)
            maze[(ny + y) // 2][(nx + x) // 2] = 0
            maze[ny][nx] = 0
            stack.append((nx, ny))
        else:
            stack.pop()

    return maze

def ensure_path(maze, start, end):
    x, y = start
    path = [start]

    while (x, y) != end:
        if x < end[0]:
            x += 1
        elif x > end[0]:
            x -= 1
        elif y < end[1]:
            y += 1
        elif y > end[1]:
            y -= 1

        if maze[y][x] == 0:
            path.append((x, y))
        else:
            break

    for px, py in path:
        maze[py][px] = 0

# A* pathfinding algorithm
def a_star_search(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while not open_set.empty():
        _, current = open_set.get()

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        x, y = current
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for nx, ny in neighbors:
            if 0 <= nx < cols and 0 <= ny < rows and maze[ny][nx] == 0:
                tentative_g_score = g_score[current] + 1
                if (nx, ny) not in g_score or tentative_g_score < g_score[(nx, ny)]:
                    came_from[(nx, ny)] = current
                    g_score[(nx, ny)] = tentative_g_score
                    f_score[(nx, ny)] = tentative_g_score + heuristic((nx, ny), goal)
                    open_set.put((f_score[(nx, ny)], (nx, ny)))

    return None  # No path found

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def display_path(path):
    for (x, y) in path:
        pygame.draw.rect(screen, BLUE, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    pygame.display.flip()
    pygame.time.delay(2000)  # Display for 2 seconds

class Player:
    def __init__(self):
        self.rect = pygame.Rect(40, 40, 40, 40)

    def move(self, dx, dy):
        if not self.collides(dx, dy):
            self.rect.x += dx
            self.rect.y += dy

    def collides(self, dx, dy):
        new_rect = self.rect.move(dx, dy)
        for y in range(len(maze)):
            for x in range(len(maze[y])):
                if maze[y][x] == 1:
                    wall_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if new_rect.colliderect(wall_rect):
                        return True
        return False
    
class Menu:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', FONT_SIZE, bold=True)

    def run(self):
        running = True
        while running:
            screen.blit(background_image, (0, 0))

            title_text = self.font.render("Maze Game", True, FONT_COLOR)
            start_text = self.font.render("Press ENTER to Start", True, FONT_COLOR)
            exit_text = self.font.render("Press ESC to Exit", True, FONT_COLOR)

            # Centering text on the screen
            screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
            screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
            screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 50))

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Start the game
                        running = False
                    elif event.key == pygame.K_ESCAPE:  # Exit
                        pygame.quit()
                        exit()

            pygame.display.flip()
            self.clock.tick(FPS)

class Hunter:
    def __init__(self, maze, player_position, speed=1):
        self.maze = maze
        self.rect = pygame.Rect(player_position[0], player_position[1], TILE_SIZE, TILE_SIZE)
        self.speed = speed

    def update(self, player):
        if self.rect.x < player.rect.x:
            self.rect.x += self.speed
        elif self.rect.x > player.rect.x:
            self.rect.x -= self.speed

        if self.rect.y < player.rect.y:
            self.rect.y += self.speed
        elif self.rect.y > player.rect.y:
            self.rect.y -= self.speed

class Game:
    def __init__(self):
        # Show the menu first
        menu = Menu()
        menu.run()

        self.destination = None
        self.regenerate_maze()

    def regenerate_maze(self):
        global maze
        maze_width, maze_height = 21, 21
        maze = generate_maze(maze_width, maze_height)
        start = (1, 1)
        self.destination = self.set_destination()
        ensure_path(maze, start, self.destination)
        self.player = Player()
        hunter_start_position = self.get_hunter_start_position(maze_width, maze_height)
        self.hunter = Hunter(maze, hunter_start_position, speed=1)
        self.clock = pygame.time.Clock()
        self.running = True
        self.camera_x = 0
        self.camera_y = 0
        self.reached_destination = False
        self.message_displayed = False

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.move(-TILE_SIZE, 0)
            if keys[pygame.K_RIGHT]:
                self.player.move(TILE_SIZE, 0)
            if keys[pygame.K_UP]:
                self.player.move(0, -TILE_SIZE)
            if keys[pygame.K_DOWN]:
                self.player.move(0, TILE_SIZE)

            # Display shortest path with "P" key
            if keys[pygame.K_p]:
                start = (self.player.rect.x // TILE_SIZE, self.player.rect.y // TILE_SIZE)
                path = a_star_search(maze, start, self.destination)
                if path:
                    display_path(path)

            # Regenerate maze with "R" key
            if keys[pygame.K_r] and not self.reached_destination:
                self.regenerate_maze()

            if (self.player.rect.x // TILE_SIZE, self.player.rect.y // TILE_SIZE) == self.destination:
                self.reached_destination = True

            if self.hunter.rect.colliderect(self.player.rect):
                self.handle_player_caught()

            self.hunter.update(self.player)
            self.update_camera()
            screen.fill(WHITE)
            self.draw_maze()
            self.draw_destination()
            pygame.draw.rect(screen, GREEN, (self.player.rect.x - self.camera_x, self.player.rect.y - self.camera_y, self.player.rect.width, self.player.rect.height))
            pygame.draw.rect(screen, (255, 0, 0), (self.hunter.rect.x - self.camera_x, self.hunter.rect.y - self.camera_y, TILE_SIZE, TILE_SIZE))

            if self.reached_destination:
                if not self.message_displayed:
                    self.display_message("Destination Reached! Generating new maze...", 2000)
                    self.message_displayed = True
                    self.regenerate_maze()
                else:
                    self.reached_destination = False
                    self.message_displayed = False

            pygame.display.flip()
            self.clock.tick(FPS)

    def display_message(self, message, duration):
        font = pygame.font.SysFont('Arial', 36)
        text = font.render(message, True, FONT_COLOR)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(duration)

    def update_camera(self):
        self.camera_x = max(0, min(self.player.rect.x - WIDTH // 2, len(maze[0]) * TILE_SIZE - WIDTH))
        self.camera_y = max(0, min(self.player.rect.y - HEIGHT // 2, len(maze) * TILE_SIZE - HEIGHT))

    def draw_maze(self):
        for y in range(len(maze)):
            for x in range(len(maze[y])):
                color = BLACK if maze[y][x] == 1 else WHITE
                pygame.draw.rect(screen, color, (x * TILE_SIZE - self.camera_x, y * TILE_SIZE - self.camera_y, TILE_SIZE, TILE_SIZE))

    def set_destination(self):
        while True:
            x, y = random.randint(1, len(maze[0]) - 2), random.randint(1, len(maze) - 2)
            if maze[y][x] == 0:
                return (x, y)

    def get_hunter_start_position(self, maze_width, maze_height):
        return (random.randint(0, maze_width - 1) * TILE_SIZE, random.randint(0, maze_height - 1) * TILE_SIZE)

    def draw_destination(self):
        pygame.draw.rect(screen, BLUE, (self.destination[0] * TILE_SIZE - self.camera_x, self.destination[1] * TILE_SIZE - self.camera_y, TILE_SIZE, TILE_SIZE))

    def handle_player_caught(self):
        self.display_message("You were caught by the Hunter!", 2000)
        self.regenerate_maze()

# Run the game
game = Game()
game.run()

pygame.quit()
