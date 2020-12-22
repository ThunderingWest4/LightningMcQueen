import pygame
import numpy as np

pygame.init()
pygame.font.init()
res = (600, 600)
scrn = pygame.display.set_mode(res)

img_scale = (30, 30)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

scrn.fill(WHITE)
myfont = pygame.font.SysFont('Comic Sans', 15)
n_rays = 8

mcq = pygame.transform.smoothscale(pygame.image.load('the_mcqueen.png').convert_alpha(), img_scale)

START = (70, 90)
FINISH = (520, 430)
walls = [((27, 53), (113, 64)), ((560, 401), (549, 472)), ((590, 590), (590, 10)), ((10, 590), (590, 590)), ((10, 10), (10, 590)), ((10, 10), (590, 10)), ((27, 53), (35, 457)), ((35, 457), (92, 558)), ((92, 558), (128, 559)), ((130, 559), (173, 488)), ((179, 464), (167, 498)), ((114, 62), (95, 131)), ((94, 131), (85, 285)), ((85, 285), (96, 393)), ((96, 393), (105, 482)), ((105, 482), (131, 442)), ((131, 442), (113, 314)), ((113, 314), (131, 224)), ((131, 224), (203, 72)), ((178, 469), (212, 317)), ((212, 316), (212, 243)), ((212, 243), (261, 117)), ((261, 117), (284, 207)), ((204, 73), (293, 49)), ((293, 49), (366, 145)), ((366, 145), (401, 275)), ((401, 275), (483, 393)), ((483, 393), (562, 400)), ((284, 207), (310, 315)), ((310, 315), (384, 425)), ((384, 425), (554, 473))]

class car(pygame.sprite.Sprite):
    def __init__(self, pos, img):
        super().__init__()
        global scrn
        self.img = img
        self.pos = pos
        self.rect = self.img.get_rect(center=pos)

def draw_cross(pos):
    pygame.draw.line(scrn, BLACK, (pos[0]+7, pos[1]+7), (pos[0]-7, pos[1]-7))
    pygame.draw.line(scrn, BLACK, (pos[0]-7, pos[1]+7), (pos[0]+7, pos[1]-7))

mouse = car(pygame.mouse.get_pos(), mcq)

while True:
    scrn.fill((255, 255, 255))
    loc = pygame.mouse.get_pos()
    dist_from_end = np.sqrt((FINISH[0]-loc[0])**2 + (FINISH[1]-loc[1])**2)

    text_surf = myfont.render(f"Location: {loc} | Distance from Finish: {dist_from_end}", False, (0,0,0))
    scrn.blit(text_surf, (0, 0))
    scrn.blit(mouse.img, (loc[0]-int(img_scale[0]/2), loc[1]-int(img_scale[1]/2)))

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
        # pygame.draw.line(scrn, (0, 0, 0), pygame.mouse.get_pos(), end)
        draw_cross(end)

    pygame.draw.circle(scrn, (0,0,0), START, 2)
    pygame.draw.circle(scrn, (0,0,0), FINISH, 2)


    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()

    pygame.display.flip()    
