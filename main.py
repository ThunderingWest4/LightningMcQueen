import neat
import numpy as np
import pygame
from helper import *

compl_gens = 0 # generations completed
n_agents = 20 # number of agents per generation
n_rays = 10 # number of rays that each player uses for getting distances
#genome = 

pygame.init()
pygame.font.init()
res = (600, 600)
scrn = pygame.display.set_mode(res)
scrn.fill((255, 255, 255))
myfont = pygame.font.SysFont('Comic Sans', 15)

walls = [((590, 590), (590, 10)), ((10, 590), (590, 590)), ((10, 10), (10, 590)), ((10, 10), (590, 10)), ((69, 18), (151, 73)), ((151, 73), (325, 80)), ((327, 82), (404, 153)), ((316, 82), (333, 88)), ((310, 80), (332, 87)), ((26, 69), (99, 134)), ((99, 134), (285, 178)), ((285, 178), (377, 217)), ((405, 153), (452, 214)), ((377, 220), (380, 291)), ((373, 217), (377, 225)), ((453, 215), (438, 284)), ((437, 282), (426, 399)), ((380, 291), (380, 384)), ((426, 402), (375, 476)), ((426, 393), (419, 416)), ((380, 383), (350, 439)), ((350, 439), (295, 400)), ((373, 479), (341, 497)), ((338, 493), (261, 445)), ((378, 472), (365, 482)), ((335, 492), (345, 495)), ((296, 403), (297, 351)), ((261, 446), (250, 367)), ((251, 368), (182, 372)), ((294, 352), (255, 314)), ((298, 356), (289, 349)), ((255, 315), (191, 317)), ((191, 317), (98, 361)), ((184, 371), (126, 411)), ((99, 364), (66, 418)), ((67, 422), (102, 481)), ((124, 411), (155, 456)), ((109, 359), (94, 375)), ((94, 372), (116, 353)), ((68, 415), (69, 427)), ((154, 455), (229, 491)), ((104, 484), (213, 543)), ((102, 480), (116, 490)), ((228, 492), (389, 528)), ((212, 544), (373, 573)), ((388, 530), (444, 450)), ((372, 576), (443, 562)), ((443, 560), (487, 468)), ((373, 574), (383, 574)), ((487, 466), (570, 425)), ((445, 449), (521, 396)), ((568, 425), (574, 326)), ((518, 397), (520, 330))]

# got walls after drawing using ray-tracing code from github, going to be set map for genetic

# gameloop

START = (53, 41)
FINISH = (547, 330)
pygame.mouse.set_pos(START)

while True:
    scrn.fill((255, 255, 255))
    loc = pygame.mouse.get_pos()
    
    text_surf = myfont.render(f"Location: {loc}", False, (0,0,0))
    scrn.blit(text_surf, (0, 0))

    for wall in walls:
        pygame.draw.line(scrn, (0, 0, 0), wall[0], wall[1], 2)
    
    ray_ends = []
    for angle in range(0, 360, int(360/n_rays)):
        x1, y1 = pygame.mouse.get_pos() # mouse position
        x2, y2 = (pygame.display.get_surface().get_width()*np.cos(np.radians(angle)) + x1, pygame.display.get_surface().get_width()*np.sin(np.radians(angle)) + y1)
        closest = 100000000000000000
        cur_closest = ()
        for wall in walls:
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

        ray_ends.append(cur_closest if cur_closest!=() else (x2, y2))
        
    for end in ray_ends:
        pygame.draw.line(scrn, (0, 0, 0), pygame.mouse.get_pos(), end)



    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()

    pygame.display.flip()    
