# Импортируем все необходимые библиотеки:
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
from PIL import Image
from math import sin,cos
global globvars

class Global_Variables:
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

globvars = Global_Variables()

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


def loadTexture(fileName,globvars):

    image = Image.open(fileName)
    width = image.size[0]
    height = image.size[1]
    image = image.tostring("raw", "RGBX", 0, -1)
    texture = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texture)  # 2d texture (x and y size)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    gluBuild2DMipmaps(GL_TEXTURE_2D, 3, width, height, GL_RGBA, GL_UNSIGNED_BYTE, image)
    globvars.floor_texture_id = texture
    return texture

def drawFloor(globvars) :
    glEnable(GL_TEXTURE_2D)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, globvars.amb)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, globvars.dif)
    glBindTexture(GL_TEXTURE_2D, globvars.floor_texture_id)

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glNormal3f(0, 0, 1); glVertex3f(-10, -10, 0)
    glTexCoord2f(0, 1); glNormal3f(0, 0, 1); glVertex3f(-10, 10, 0)
    glTexCoord2f(1, 1); glNormal3f(0, 0, 1); glVertex3f(10, 10, 0)
    glTexCoord2f(1, 0); glNormal3f(0, 0, 1); glVertex3f(10, -10, 0)
    glEnd()

    glDisable(GL_TEXTURE_2D)

def update(globvars):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    ang_vert_r = globvars.ang_vert / 180 * 3.1416
    ang_hor_r = globvars.ang_hor / 180 * 3.1416
    cam_x = globvars.cam_dist * sin(ang_vert_r) * cos(ang_hor_r)
    cam_y = globvars.cam_dist * sin(ang_vert_r) * sin(ang_hor_r)
    cam_z = globvars.cam_dist * cos(ang_vert_r)

    gluLookAt(cam_x, cam_y, cam_z, 0., 0., 0., 0., 0., 1.)
    drawLamps()
    drawFloor(globvars)
	drawCar()
    glFlush()
    glutSwapBuffers()


def updateCamera(globvars):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60., globvars.w / globvars.h, 1.0, 1000.)
    glMatrixMode(GL_MODELVIEW)


