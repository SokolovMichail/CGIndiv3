from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy
shaders = ['lambert', 'blinn', 'minnaert', 'toon', 'gooch', 'rim']
curr_shader_program = None

curr_shader = "lambert"

#Camera
camera_distance = 1
camera_x_rotation = 30
camera_y_rotation = 0
camera_angle_delta = 5
camera_matrix = None

# Objects.
terrain_size = 1
lamp_size = 0.2
lamps_count = 4
tree_size = 0.25
snowman_size = 0.25
car_size = 0.05
snowman_pos_x = snowman_pos_y = 0
light_snowman_matrix = None
#LIGHTS
lights_positions = [
    (-0.5, 0.25, -0.5),
    (-0.2,0.48,0.0)#A light for the tree
]
lights_colors = [
    (0, 0, 0),
    (1, 1, 0)
]
lights_specular_colors = lights_colors
lights_specular_intensities = [1,1]
lights_cool_colors = [(color[0] * 0.1, color[1] * 0.1, color[2] * 0.5) for color in lights_colors]
lights_warm_colors = [(color[0] * 0.5, color[1] * 0.1, color[2] * 0.1) for color in lights_colors]
lights_rim_intensities = [1,1]

# Colors.
white = (1, 1, 1)
light_gray = (0.8, 0.8, 0.8)
gray = (0.5, 0.5, 0.5)
black = (0, 0, 0)
red = (1, 0, 0)
yellow = (1, 1, 0)
orange = (1, 0.5, 0)
green = (0, 1, 0)
brown = (0.9, 0.6, 0.3)

def handle_camera():
    global camera_matrix

    glTranslate(0, 0, -camera_distance)
    glRotate(camera_x_rotation, 1, 0, 0)
    glRotate(camera_y_rotation, 0, 1, 0)
    camera_matrix = numpy.array(glGetFloat(GL_MODELVIEW_MATRIX)).reshape(4, 4)

def load_shader_from_file(filename):
    f = open(filename,"r")
    return f.read()

def create_shader(shader_type, filename):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, load_shader_from_file(filename))
    glCompileShader(shader)
    return shader

def create_shader_programme(vertex_shader_name,fragment_texture_shader_name):
    v_shader = create_shader(GL_VERTEX_SHADER,vertex_shader_name)
    f_shader = create_shader(GL_FRAGMENT_SHADER,fragment_texture_shader_name)
    programme_shader = glCreateProgram()
    glAttachShader(programme_shader,v_shader)
    glAttachShader(programme_shader,f_shader)
    glLinkProgram(programme_shader)
    return programme_shader

def init_shaders():
    global curr_shader_program
    curr_shader_program = create_shader_programme(f'{curr_shader},v',f'{curr_shader}.f')

def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glUseProgram(curr_shader_program)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    handle_camera()
    draw_terrain()
    glTranslate(-0.2, 0, 0)
    glPushMatrix()
    glTranslate(0,0.0,0.48)
    glutWireSphere(0.02,10,10)
    glPopMatrix()
    draw_tree()
    glTranslate(0.4, 0, 0)
    draw_liberty_snowman()
    glTranslate(-0.2, 0, 0)
    glRotate(-120, 0, 1, 0)
    set_uniforms()
    #draw_car()

    glutSwapBuffers()

def set_uniforms():
    for i in range(len(lights_positions)):
        local_light_position = numpy.dot(lights_positions[i] + (1,), camera_matrix)

        light_position_uniform = glGetUniformLocation(curr_shader_program, f'lights[{i}].position')
        light_color_uniform = glGetUniformLocation(curr_shader_program, f'lights[{i}].color')
        light_specular_color_uniform = glGetUniformLocation(curr_shader_program, f'lights[{i}].specularColor')
        light_specular_intensity_uniform = glGetUniformLocation(curr_shader_program,
                                                                f'lights[{i}].specularIntensity')
        light_cool_color_uniform = glGetUniformLocation(curr_shader_program, f'lights[{i}].coolColor')
        light_warm_color_uniform = glGetUniformLocation(curr_shader_program, f'lights[{i}].warmColor')
        light_rim_intensity_uniform = glGetUniformLocation(curr_shader_program, f'lights[{i}].rimIntensity')

        glUniform3f(light_position_uniform, local_light_position[0], local_light_position[1], local_light_position[2])
        glUniform3f(light_color_uniform, lights_colors[i][0], lights_colors[i][1], lights_colors[i][2])
        glUniform3f(light_specular_color_uniform,
                    lights_specular_colors[i][0], lights_specular_colors[i][1], lights_specular_colors[i][2])
        glUniform1f(light_specular_intensity_uniform, lights_specular_intensities[i])
        glUniform3f(light_cool_color_uniform,
                    lights_cool_colors[i][0], lights_cool_colors[i][1], lights_cool_colors[i][2])
        glUniform3f(light_warm_color_uniform,
                    lights_warm_colors[i][0], lights_warm_colors[i][1], lights_warm_colors[i][2])
        glUniform1f(light_rim_intensity_uniform, lights_rim_intensities[i])

def draw_terrain():
    glColor(light_gray)
    glBegin(GL_QUADS)
    glNormal(0, 1, 0)
    glVertex(-terrain_size / 2, 0, -terrain_size / 2)
    glNormal(0, 1, 0)
    glVertex(terrain_size / 2, 0, -terrain_size / 2)
    glNormal(0, 1, 0)
    glVertex(terrain_size / 2, 0, terrain_size / 2)
    glNormal(0, 1, 0)
    glVertex(-terrain_size / 2, 0, terrain_size / 2)
    glEnd()

def draw_tree():
    glPushMatrix()  # Сохраняем текущее положение "камеры"
    glScale(tree_size,tree_size,tree_size)
    glRotate(-90,1,0,0)
    glTranslate(0,0,0.7)
    # Рисуем ствол елки
    # Устанавливаем материал: рисовать с 2 сторон, рассеянное освещение, коричневый цвет
    glColor(brown)
    glTranslatef(0.0, 0.0, -0.7)  # Сдвинемся по оси Z на -0.7
    # Рисуем цилиндр с радиусом 0.1, высотой 0.2
    # Последние два числа определяют количество полигонов
    glutSolidCylinder(0.1, 0.2, 20, 20)
    # Рисуем ветки елки
    # Устанавливаем материал: рисовать с 2 сторон, рассеянное освещение, зеленый цвет
    glColor(green)
    glTranslatef(0.0, 0.0, 0.2)  # Сдвинемся по оси Z на 0.2
    # Рисуем нижние ветки (конус) с радиусом 0.5, высотой 0.5
    # Последние два числа определяют количество полигонов
    glutSolidCone(0.5, 0.5, 20, 20)
    glTranslatef(0.0, 0.0, 0.3)  # Сдвинемся по оси Z на -0.3
    glutSolidCone(0.4, 0.4, 20, 20)  # Конус с радиусом 0.4, высотой 0.4
    glTranslatef(0.0, 0.0, 0.3)  # Сдвинемся по оси Z на -0.3
    glutSolidCone(0.3, 0.3, 20, 20)  # Конус с радиусом 0.3, высотой 0.3

    glPopMatrix()  # Возвращаем сохраненное положение "камеры"

def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, width / height, 0.1, 100)


def special(key, x, y):
    global camera_x_rotation, camera_y_rotation

    if key == GLUT_KEY_UP:
        camera_x_rotation += camera_angle_delta
    if key == GLUT_KEY_DOWN:
        camera_x_rotation -= camera_angle_delta
    if key == GLUT_KEY_LEFT:
        camera_y_rotation += camera_angle_delta
    if key == GLUT_KEY_RIGHT:
        camera_y_rotation -= camera_angle_delta

def draw_liberty_snowman():
    glPushMatrix()
    glTranslate(snowman_pos_x,0,0)
    glTranslate(0,0,snowman_pos_y)
    glScale(snowman_size,snowman_size,snowman_size)
    glRotate(-90,1,0,0)
    glColor3f(1,1,1)
    glTranslate(-1,1,0.4)
    glutSolidSphere(0.25,10,10)
    glTranslate(0, 0, 0.25)
    glutSolidSphere(0.15, 10, 10)
    glTranslate(0, 0, 0.2)
    glutSolidSphere(0.1, 10, 10)
    glTranslate(-0.1,0,-0.2)
    glRotate(45,1,0,0)
    glutSolidCylinder(0.01, 0.5, 20, 20)
    glRotate(-45, 1, 0, 0)
    glTranslate(0,-0.32,0.4)
    glutSolidSphere(0.1,5,5)
    glPopMatrix()

def keyboard(key, x, y):
    global snowman_pos_x,snowman_pos_y
    #print(key)
    if(key == b"w"):
        snowman_pos_x += 0.025
    if (key == b"s"):
        snowman_pos_x -= 0.025
    if (key == b"a"):
        snowman_pos_y -= 0.025
    if (key == b"d"):
        snowman_pos_y += 0.025
    pass

def main():
    glutInit()
    glutInitWindowSize(600, 600)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutCreateWindow(curr_shader_program)
    glutIdleFunc(render)
    glutDisplayFunc(render)
    glutReshapeFunc(reshape)
    glutSpecialFunc(special)
    glutKeyboardFunc(keyboard)
    glClearColor(0, 0.6, 1, 1)
    glEnable(GL_DEPTH_TEST)
    init_shaders()
    glutMainLoop()

main()
