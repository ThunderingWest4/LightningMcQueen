import neat
import numpy as np
import pygame
from extras import *
import random

pygame.init()
pygame.font.init()
res = (600, 600)
scrn = pygame.display.set_mode(res)
scrn.fill((255, 255, 255))
myfont = pygame.font.SysFont('Comic Sans', 15)
img_scale = (30, 30)
pi = np.pi

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

n_rays = 8 # number of rays that each player uses for getting distances 
START = (70, 90)
FINISH = (520, 430)
MAX_VEL = 2 # max amount it can travel in one frame
walls = getWalls()
mcq = pygame.transform.smoothscale(pygame.image.load('the_mcqueen.png').convert_alpha(), img_scale)
color_options = getColors()

class car(pygame.sprite.Sprite):
    def __init__(self, pos, img, col, rad=7):
        super().__init__()
        global scrn
        # self.img = img
        self.pos = pos
        self.color = col
        self.radius = rad
        # self.angle = 0
        # self.rect = self.img.get_rect(center=pos)

def draw_cross(pos, color):
    pygame.draw.line(scrn, color, (pos[0]+7, pos[1]+7), (pos[0]-7, pos[1]-7))
    pygame.draw.line(scrn, color, (pos[0]-7, pos[1]+7), (pos[0]+7, pos[1]-7))

def eval_genomes(genomes, config):
    # gameloop
    
    nets = []
    cars = []
    gnms = []

    for genome_id, genome in genomes:
        genome.fitness = 0 # base/initial fitness of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        col = random.choice(color_options)
        cars.append(car(START, mcq, col))
        gnms.append(genome)

    run = True
    while run and len(cars)>0: # while still cars

        scrn.fill((255, 255, 255))
        pygame.draw.circle(scrn, (0,0,0), START, 2)
        pygame.draw.circle(scrn, (0,0,0), FINISH, 2)
        for wall in walls:
                pygame.draw.line(scrn, BLACK, wall[0], wall[1], 2)
            
        for idx, c in enumerate(cars):
            
            loc = c.pos
            dist_from_end = np.sqrt((FINISH[0]-loc[0])**2 + (FINISH[1]-loc[1])**2)

            # text_surf = myfont.render(f"Location: {loc} | Distance from Finish: {dist_from_end}", False, (0,0,0))
            # scrn.blit(text_surf, (0, 0))
            # scrn.blit(c.img, (loc[0]-int(img_scale[0]/2), loc[1]-int(img_scale[1]/2)))
            pygame.draw.circle(scrn, c.color, c.pos, c.radius)

            ray_ends = []
            distances = []

            x1, y1 = loc
            valid = True

            for angle in range(0, 360, int(360/n_rays)):
                # x1, y1 = loc # mouse position
                x2, y2 = (pygame.display.get_surface().get_width()*np.cos(np.radians(angle)) + x1, pygame.display.get_surface().get_width()*np.sin(np.radians(angle)) + y1)
                closest = 100000000000000000
                cur_closest = ()
                for wall in walls:
                    
                    # RAYCASTING STUFF
                    x3, y3 = wall[0]
                    x4, y4 = wall[1]

                    # parallel check
                    if ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)) == 0:
                        continue

                    t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)) / ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))

                    u = -((x1-x2)*(y1-y3) - (y1-y2)*(x1-x3)) / ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
                
                    if t>0.0 and 0<u<1:
                        px = x3 + u*(x4-x3)
                        py = y3 + u*(y4-y3)

                        dist = np.sqrt((px-x1)**2 + (py-y1)**2)
                        
                        if dist < closest:
                            closest = dist
                            cur_closest = (px, py)

                    if closest == 100000000000000000:
                        valid = False

                    else:
                        # CIRCLE COLLISION DETECTION

                        q = c.pos # center of circle
                        r = c.radius # radius of circle
                        p1 = (x3, y3) # start of line segment
                        v = (x4-x3, y4-y3) # vector along line seg
                        a = np.dot(v, v)
                        b = 2*np.dot(v, (p1[1]-q[1], p1[0]-q[0]))
                        c2 = np.dot(p1, p1) + np.dot(q, q) - 2*np.dot(q, p1) - r**2
                        valid = ((b**2) - (4*a*c2)) < 0 # if it's less than 0, no intersections

                ray_ends.append(cur_closest if cur_closest!=() else (x2, y2))
                distances.append(closest) # will use to check if the car has collided with a wall

            # for d in distances:
            #     valid = d > 0 # if dist <=0, means it collided (hopefully, assuming my logic is right lol)
            # spoiler alert: it wasn't
            # this, however, is: https://codereview.stackexchange.com/questions/86421/line-segment-to-circle-collision-algorithm
            # moved collision detection code to around line 110

            if valid:
                for end in ray_ends:
                    # pygame.draw.line(scrn, (0, 0, 0), pygame.mouse.get_pos(), end)
                    draw_cross(end, c.color)

                gnms[idx].fitness += 0.1 # more fit because still alive
                gnms[idx].fitness += 10/dist_from_end # smaller the distance, greater the increase

                # now that we've gotten the distances from the walls and determined if the car is (or isn't) valid, we can plug those into its network and adjust path based on outputted velocity and angle
                inps = [x for x in distances]
                inps.append(dist_from_end)
                assert len(inps) == 9 # just a check, if it's not we've got a serious issue
                outs = nets[idx].activate(inps) # get activated outputs
                turn = outs[0]
                vel = outs[1]
                angle = (pi/2) * turn
                new_x = c.pos[0] + int(MAX_VEL*vel*np.cos(angle))
                new_y = c.pos[1] + int(MAX_VEL*vel*np.sin(angle)) + 1
                c.pos = (new_x, new_y)

            else: 
                # means it collided
                cars.pop(idx)
                nets.pop(idx)
                gnms[idx].fitness -= 2
                gnms.pop(idx)
                # continue # cut this loop short

            
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                run = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_q:
                    run = False

        pygame.display.flip()    
    
    # out of loop
