import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

earth_radius = 1.0
latitude_lines = 20
longitude_lines = 40


def draw_earth():
    glColor3f(0.0, 0.0, 1.0)  # Blue color for the Earth
    glPushMatrix()
    gluSphere(gluNewQuadric(), earth_radius, latitude_lines, longitude_lines)
    glPopMatrix()


def draw_dots():
    glColor3f(1.0, 1.0, 1.0)  # White color for the dots
    for lat in range(-90, 91, 15):
        for lon in range(0, 360, 30):
            lat_rad = math.radians(lat)
            lon_rad = math.radians(lon)
            x = earth_radius * math.cos(lat_rad) * math.cos(lon_rad)
            y = earth_radius * math.cos(lat_rad) * math.sin(lon_rad)
            z = earth_radius * math.sin(lat_rad)

            glPushMatrix()
            glTranslatef(x, y, z)
            gluSphere(gluNewQuadric(), 0.02, 10, 10)  # Adjust the size of the dots as needed
            glPopMatrix()


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    rotation_angle = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(1, 0, 1, 0)  # Rotate the Earth around the Y-axis
        rotation_angle += 1

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_earth()
        draw_dots()
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
