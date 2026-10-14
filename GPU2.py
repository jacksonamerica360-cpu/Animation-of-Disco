import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
"""Want to Generrate a Disco Light Using Python and Mathematics Logic @2seniors and @JACKSON"""


INITIAL_PARTICLE_COUNT = 80000
WINDOW_SIZE = (1280, 720)

def generate_particle_cloud(count):
    """Tumhara hi wala formula - bas ek baar banega"""
    indices = np.arange(count)
    phi = np.arccos(1 - 2 * (indices / count))
    theta = np.pi * (1 + 5**0.5) * indices

    radius = 5.0 + 2.0 * np.sin(theta * 5)#"""Use Of Mathematical Concepts Like Trigonometry and 3D Geometry
   # People who says what is use of sin cos and 3D Geometry"""
    x = radius * np.sin(phi) * np.cos(theta)
    y = radius * np.sin(phi) * np.sin(theta)
    z = radius * np.cos(phi)

    r = 0.5 + 0.5 * np.sin(theta)
    g = 0.5 + 0.5 * np.cos(phi)
    b = 0.8 + 0.2 * np.sin(phi * theta)

    positions = np.stack((x, y, z), axis=-1).astype(np.float32)#Vector Algbra
    colors = np.stack((r, g, b), axis=-1).astype(np.float32)
    return positions, colors

def main():
    pygame.init()
    pygame.display.set_mode(WINDOW_SIZE, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Fixed Loop - Jackson's Visualization")

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_POINT_SMOOTH)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glPointSize(2.5)
    glClearColor(0.02, 0.02, 0.05, 1.0) 

    gluPerspective(45, (WINDOW_SIZE[0] / WINDOW_SIZE[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -18.0)


    print("[SYSTEM] Generating beautiful structure... Locked!")
    positions, colors = generate_particle_cloud(INITIAL_PARTICLE_COUNT)

    clock = pygame.time.Clock()
    t = 0.0

    print("[SYSTEM] Starting infinite loop - ab kabhi kharab nahi hoga. ESC se band karo")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()

        glRotatef(t * 20, 0, 1, 0)#3D Geometry""""
        glRotatef(t * 15, 1, 0, 0)
        glRotatef(math.sin(t*0.01)*10, 0, 0, 1) 

        
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, positions)
        glColorPointer(3, GL_FLOAT, 0, colors)
        glDrawArrays(GL_POINTS, 0, INITIAL_PARTICLE_COUNT)
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)

        glPopMatrix()
        pygame.display.flip()

        t += 0.5 # speed
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    import math
    main()
    """Let see How This Will Look Like @JACKSON and 2 Others Sunday Project I Hope You Will Like This Visual
    Visualization lets Run The Code"""
    

