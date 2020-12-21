# import pygame 
# import sys

# pygame.init()
# pygame.font.init()

# scrn = pygame.display.set_mode((500, 500))
# scrn.fill((255, 255, 255))
# myfont = pygame.font.SysFont('Comic Sans', 15)

# walls = []

# while True:
#     scrn.fill((255, 255, 255))
#     loc = pygame.mouse.get_pos()
    
#     text_surf = myfont.render(f"Location: {loc}", False, (0,0,0))
#     scrn.blit(text_surf, (0, 0))

#     for ev in pygame.event.get():
#         if ev.type == pygame.QUIT:
            
#             with open("maps.txt", "w+") as f:
#                 f.write(walls)

#             pygame.quit()
#             sys.exit()

                    

#     pygame.display.flip()

# yeeted from https://github.com/kubapilch/Ray-Tracing/blob/master/ for ez setup lol

import pygame
import math
import time

class Wall():
    def __init__(self, A, B):
        self.A = A
        self.B = B

class Ray():
    def __init__(self, start_pos, angle):
        self.start_pos = start_pos
        self.angle = angle
        self.helper_pos = self.getHelperPoint(pygame.display.get_surface().get_width())
        # Set same as helper if there is no walls and ray has to go out of the screen
        self.end_point = self.getHelperPoint(pygame.display.get_surface().get_width())
    
    def getHelperPoint(self, lenght):
        # Is needed for calculating intersections
        # Get a point from starting pos, angle and lenght of vector
        return (lenght * math.cos(math.radians(self.angle)) + self.start_pos[0], lenght * math.sin(math.radians(self.angle)) + self.start_pos[1])


class Button():
    def __init__(self, x, y, width, height, text, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
    
    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, t):
        # Render new label
        self._text = t
        self.label = pygame.font.SysFont("monospace", 10).render(t, 1, (0, 0, 0))

    def values(self):
        return (self.x, self.y, self.width, self.height)

    def draw(self, surface):
        # Draw button
        pygame.draw.rect(surface, self.color, self.values())
        # Draw label
        surface.blit(self.label, (self.x + (self.width/2 - self.label.get_width()/2), self.y+(self.height/2 - self.label.get_height()/2)))
    
    def clicked(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


# --- CUSTOMIZABLE VARIABLES ---
number_of_rays = 120 # Max 360
wall_thicknes = 2
boundarySpacing = 10
# ------------------------------


# Setup
pygame.init()
size = (600, 600)
menuSize = (90, 80)
surface = pygame.display.set_mode(size, pygame.RESIZABLE)
menuSurface = pygame.Surface(menuSize)
pygame.display.set_caption("Rays")
font = pygame.font.SysFont("monospace", 15)


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 50)


# Game variables
walls = []
rays = []
drawing = False
wall_starting_pos = (0, 0)
play = False
carryOn = True
clock = pygame.time.Clock()


# --- INITIAL SETUP ---

# Buttons
resetButton = Button(10, size[1]-menuSize[1]+10, 70, 25, 'Reset', RED)
playButton = Button(10, resetButton.y + 10 + resetButton.height, 70, 25, 'Play', GREEN)

# Boundaries
def addBoundaries():
    walls.insert(0, Wall((boundarySpacing, boundarySpacing), (size[0] - boundarySpacing, boundarySpacing)))
    walls.insert(0, Wall((boundarySpacing, boundarySpacing), (boundarySpacing, size[1] - boundarySpacing)))
    walls.insert(0, Wall((boundarySpacing, size[1] - boundarySpacing), (size[0] - boundarySpacing, size[1] - boundarySpacing)))
    walls.insert(0, Wall((size[0] - boundarySpacing, size[1] - boundarySpacing), (size[0] - boundarySpacing, boundarySpacing)))

addBoundaries()

# Draw Menu
def drawMenu():
    # Set colot and transparency of the menu box
    menuSurface.fill(WHITE)
    menuSurface.set_alpha(126)

    # Draw menu box
    surface.blit(menuSurface, (0, size[1]-menuSize[1]))

    # Draw buttons
    resetButton.draw(surface)
    playButton.draw(surface)


# -------- Main Program Loop -----------
while carryOn:
    
    # --- MAIN EVENT LOOP ---
    for event in pygame.event.get(): 
        # If user wants to leave
        if event.type == pygame.QUIT: 
              carryOn = False 
        
        # User has changed the size of a window
        if event.type == pygame.VIDEORESIZE:
            size = (event.w, event.h)
            surface = pygame.display.set_mode(size, pygame.RESIZABLE)
            
            # Change boundaries
            walls = walls[4:]
            addBoundaries()

            # Change buttons
            resetButton.y = size[1]-menuSize[1]+10
            playButton.y = resetButton.y + 10 + resetButton.height

        # User has clicked mouse button
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            
            if event.button == 1: #Left click
                # Check if user clicked on one of the buttons
                if resetButton.clicked(pos):
                    walls = []
                    addBoundaries()

                elif playButton.clicked(pos):
                    # Change status of play button
                    if play:
                        playButton.color = GREEN
                        playButton.text = 'Play'
                    else:
                        playButton.color = YELLOW
                        playButton.text = 'Stop'
                    
                    drawing = False
                    play = not play
                    
                elif not play: # Drawing a wall
                    
                    # Check if user is already drawing a wall
                    if drawing:
                        # Finish drawing and add a new wall
                        drawing = False
                        walls.append(Wall(wall_starting_pos, pos))
                    else:
                        # Start drawing
                        drawing = True
                        wall_starting_pos = pos
            
            elif event.button == 3: # Right Click
                drawing = False
 
    # --- GAME LOGIC ---
    
    # Calculate new rays
    if play:
        rays = []
        with open("set_1.txt", "w+") as f:
            f.write(str([(x.A, x.B) for x in walls]))

        for angle in range(0, 360, int(360/number_of_rays)):
            # Create a new ray
            ray = Ray(pygame.mouse.get_pos(), angle)

            closest = 100000000000000000000000000 # Very big number
            # Check every wall
            for wall in walls:
                x1, y1 = ray.start_pos
                x2, y2 = ray.end_point

                x3, y3 = wall.A
                x4, y4 = wall.B

                # Magical formula from wikipedia https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
                div = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)
                if div == 0:
                    # Parallel
                    continue
                
                t = ((x1 - x3)*(y3 - y4) - (y1 - y3)*(x3 - x4))/div
                u = -((x1 - x2)*(y1 - y3) - (y1 - y2)*(x1 - x3))/div

                # Check if there is an intersection point
                if 0.0 < t and u > 0.0 and u < 1:
                    point = (int(x1 + t*(x2 - x1)), int(y1 + t*(y2 - y1)))
                    distance = ((point[0] - ray.start_pos[0])**2 + (point[1] - ray.start_pos[1])**2)**(1/2)

                    # Check if this is the colosest wall
                    if closest > distance:
                        ray.end_point = point
                        closest = distance

            rays.append(ray)


    # --- DRAWING ---
    surface.fill(BLACK)

    # Draw currently constructing wall
    if drawing:
        pygame.draw.line(surface, WHITE, wall_starting_pos, pygame.mouse.get_pos(), wall_thicknes)
    
    # Draw existing walls
    for wall in walls:
        pygame.draw.line(surface, WHITE, wall.A, wall.B, wall_thicknes)

    # Draw player and rays
    if play:
        pygame.draw.circle(surface, WHITE, pygame.mouse.get_pos(), 10)

        for ray in rays:
            pygame.draw.line(surface, WHITE, ray.start_pos, ray.end_point, 1)

    # Draw menu and all buttons
    drawMenu()

    # --- UPDATE THE SCREEN ---
    pygame.display.flip()

    clock.tick(60)
 
pygame.quit()