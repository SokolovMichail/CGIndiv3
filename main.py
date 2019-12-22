# Импортируем все необходимые библиотеки:
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

class  Global_Variables:
    def __init__(self):
        self.w = 0
        self.h = 0
        self.floor_texture_id = None
        self.car_texture_id = None
        self.dist_x = 0
        self.dist_y = 0
        self.angle = 0
        self.machine_coord_x = 0
        self.machine_coord_y = 0
        self.machine_angle = 0
        self.cam_dist = 20
        self.ang_hor = 0
        self.ang_vert = -60
        self.no_light = [0, 0, 0, 1]
        self.light=[1, 1, 1, 0]
        self.cam_x = 0
        self.cam_y = 0
        self.cam_z = 0
        self.amb = [0.8, 0.8, 0.8]
        self.dif=[0.2, 0.2, 0.2]
        self.step = 1

def init():
    glClearColor(0, 0, 0, 1)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    light_diffuse = [ 1.0, 1.0, 1.0, 1.0 ]
    light_specular = [ 1.0, 1.0, 1.0, 1.0 ]

    #loadTextures();

    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT2, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT2, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT3, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT3, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT4, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT5, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT5, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT6, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT6, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT7, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT7, GL_DIFFUSE, light_diffuse)



    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
}