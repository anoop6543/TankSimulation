import pygame
from OpenGL.GL import *

pygame.init()
pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)
print(glGetString(GL_VERSION))