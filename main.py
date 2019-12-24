# Импортируем все необходимые библиотеки:
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
from PIL import Image
import numpy

# Объявляем все глобальные переменные
global programme_shader
global floor_texture_id
global xrot         # Величина вращения по оси x
global yrot         # Величина вращения по оси y
global ambient      # рассеянное освещение
global greencolor   # Цвет елочных иголок
global treecolor    # Цвет елочного стебля
global lightpos     # Положение источника освещения
global width,height
global shader_text_loc
global floor_vertices
global floor_textures
#############Shader_Block
def load_shader_from_file(filename):
    f = open(filename,"r")
    return f.read()

def set_floor_vertices_n_textures():
    global floor_vertices,floor_textures
    floor_vertices = [[-10,-10,-0.7],
                      [-10,10,-0.7],
                      [10,10,-0.7],
                      [10,-10,-0.7]]
    floor_textures = [[0,0],[0,1],[1,1],[1,0]]

def set_texture_params():
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)

def create_shader(shader_type, filename):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, load_shader_from_file(filename))
    glCompileShader(shader)
    return shader

def create_shader_programme(vertex_shader_name,fragment_texture_shader_name):
    global programme_shader
    v_shader = create_shader(GL_VERTEX_SHADER,vertex_shader_name)
    f_shader = create_shader(GL_FRAGMENT_SHADER,fragment_texture_shader_name)
    programme_shader = glCreateProgram()
    glAttachShader(programme_shader,v_shader)
    glAttachShader(programme_shader,f_shader)
    glLinkProgram(programme_shader)
    return programme_shader

def initialise_shader_programme():
    global shader_text_loc,programme_shader
    programme_shader = create_shader_programme("vertex_shader","fragment_texture_shader")
    shader_text_loc = glGetUniformLocation(programme_shader ,'texture1')
    return programme_shader

def free_shaders(program):
    glUseProgram(0)
    glDeleteProgram(program)

###########################
def ReadTexture(filename):
    # PIL can open BMP, EPS, FIG, IM, JPEG, MSP, PCX, PNG, PPM
    # and other file types.  We convert into a texture using GL.
    print('trying to open', filename)
    try:
        image = Image.open(filename)
    except IOError as ex:
        print('IOError: failed to open texture file')
        message = "ERR"#template.format(type(ex).__name__, ex.args)
        print(message)
        return -1
    print('opened file: size=', image.size, 'format=', image.format)
    imageData = numpy.array(list(image.getdata()), numpy.uint8)

    textureID = glGenTextures(1)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 4)
    glBindTexture(GL_TEXTURE_2D, textureID)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_BASE_LEVEL, 0)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 0)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.size[0], image.size[1],
                 0, GL_RGB, GL_UNSIGNED_BYTE, imageData)
    image.close()
    return textureID

# Процедура инициализации
def init():
    global xrot         # Величина вращения по оси x
    global yrot         # Величина вращения по оси y
    global ambient      # Рассеянное освещение
    global greencolor   # Цвет елочных иголок
    global treecolor    # Цвет елочного ствола
    global lightpos     # Положение источника освещения
    xrot = 0.0                          # Величина вращения по оси x = 0
    yrot = 0.0                          # Величина вращения по оси y = 0
    ambient = (1.0, 1.0, 1.0, 1)        # Первые три числа цвет в формате RGB, а последнее - яркость
    greencolor = (0.2, 0.8, 0.0, 0.8)   # Зеленый цвет для иголок
    treecolor = (0.9, 0.6, 0.3, 0.8)    # Коричневый цвет для ствола
    lightpos = (1.0, 1.0, 1.0)          # Положение источника освещения по осям xyz

    glClearColor(0.5, 0.5, 0.5, 1.0)                # Серый цвет для первоначальной закраски
    #glRotatef(-90, 1.0, 0.0, 0.0)                   # Сместимся по оси Х на 90 градусов
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambient) # Определяем текущую модель освещения
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)                           # Включаем освещение
    glEnable(GL_LIGHT0)                             # Включаем один источник света
    glLightfv(GL_LIGHT0, GL_POSITION, lightpos)     # Определяем положение источника света


# Процедура обработки специальных клавиш
def specialkeys(key, x, y):
    global xrot
    global yrot
    # Обработчики для клавиш со стрелками
    if key == GLUT_KEY_UP:      # Клавиша вверх
        xrot -= 2.0             # Уменьшаем угол вращения по оси Х
    if key == GLUT_KEY_DOWN:    # Клавиша вниз
        xrot += 2.0             # Увеличиваем угол вращения по оси Х
    if key == GLUT_KEY_LEFT:    # Клавиша влево
        yrot -= 2.0             # Уменьшаем угол вращения по оси Y
    if key == GLUT_KEY_RIGHT:   # Клавиша вправо
        yrot += 2.0             # Увеличиваем угол вращения по оси Y

    glutPostRedisplay()         # Вызываем процедуру перерисовки

def draw_polygon():
    global shader_text_loc,floor_texture_id,programme_shader
    glPushMatrix()
    glUseProgram(programme_shader)
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, floor_texture_id)
    set_texture_params()
    glProgramUniform1i(programme_shader,shader_text_loc,0)
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_TEXTURE_COORD_ARRAY)
    glVertexPointer(4,GL_FLOAT,0,floor_vertices)
    glTexCoordPointer(4,GL_FLOAT,0,floor_textures)
    glDrawArrays(GL_QUADS,0,4)
    glDisableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_TEXTURE_COORD_ARRAY)
    glPopMatrix()
    glGetError()
    glUseProgram(0)

def draw_tree():
    glPushMatrix()  # Сохраняем текущее положение "камеры"
    glLightfv(GL_LIGHT0, GL_POSITION, lightpos)  # Источник света вращаем вместе с елкой

    # Рисуем ствол елки
    # Устанавливаем материал: рисовать с 2 сторон, рассеянное освещение, коричневый цвет
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, treecolor)
    glTranslatef(0.0, 0.0, -0.7)  # Сдвинемся по оси Z на -0.7
    # Рисуем цилиндр с радиусом 0.1, высотой 0.2
    # Последние два числа определяют количество полигонов
    glutSolidCylinder(0.1, 0.2, 20, 20)
    # Рисуем ветки елки
    # Устанавливаем материал: рисовать с 2 сторон, рассеянное освещение, зеленый цвет
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, greencolor)
    glTranslatef(0.0, 0.0, 0.2)  # Сдвинемся по оси Z на 0.2
    # Рисуем нижние ветки (конус) с радиусом 0.5, высотой 0.5
    # Последние два числа определяют количество полигонов
    glutSolidCone(0.5, 0.5, 20, 20)
    glTranslatef(0.0, 0.0, 0.3)  # Сдвинемся по оси Z на -0.3
    glutSolidCone(0.4, 0.4, 20, 20)  # Конус с радиусом 0.4, высотой 0.4
    glTranslatef(0.0, 0.0, 0.3)  # Сдвинемся по оси Z на -0.3
    glutSolidCone(0.3, 0.3, 20, 20)  # Конус с радиусом 0.3, высотой 0.3

    glPopMatrix()  # Возвращаем сохраненное положение "камеры"

def draw_liberty_snowman():
    glPushMatrix()
    glTranslate(-1,1,-0.5)
    glutSolidSphere(0.25,10,10)
    glTranslate(0, 0, 0.25)
    glutSolidSphere(0.15, 10, 10)
    glTranslate(0, 0, 0.2)
    glutSolidSphere(0.1, 10, 10)
    glPopMatrix()
# Процедура перерисовки

def draw():
    global xrot
    global yrot
    global lightpos
    global greencolor
    global treecolor
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Очищаем экран и заливаем серым цветом
    glTranslate(0, 0, -10)
    glRotate(-60,1,0,0)
    glRotatef(xrot, 1.0, 0.0, 0.0)  # Вращаем по оси X на величину xrot
    glRotatef(yrot, 0.0, 1.0, 0.0)  # Вращаем по оси Y на величину yrot

    draw_polygon()
    draw_tree()
    draw_liberty_snowman()
    glFlush()
    glutSwapBuffers()                                           # Выводим все нарисованное в памяти на экран

def reshape(w,h):
    global width,height
    width = w
    height = h

    glViewport(0, 0, w, h)
    update_camera()

def update_camera():
    global width,height
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60,width/height,1,1000)
    glMatrixMode(GL_MODELVIEW)

def main():
    global floor_texture_id,programme_shader
    set_floor_vertices_n_textures()
    # Здесь начинается выполнение программы
    # Использовать двойную буферизацию и цвета в формате RGB (Красный, Зеленый, Синий)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    # Указываем начальный размер окна (ширина, высота)
    glutInitWindowSize(800, 1000)
    # Указываем начальное положение окна относительно левого верхнего угла экрана
    glutInitWindowPosition(50, 50)
    # Инициализация OpenGl
    glutInit(sys.argv)
    # Создаем окно с заголовком "Happy New Year!"
    glutCreateWindow(b"Happy New Year!")
    # Определяем процедуру, отвечающую за перерисовку
    glutDisplayFunc(draw)
    # Определяем процедуру, отвечающую за обработку клавиш
    glutSpecialFunc(specialkeys)
    glutReshapeFunc(reshape)
    # Вызываем нашу функцию инициализации
    init()

    #Загрузка текстуры
    floor_texture_id = ReadTexture("snowy04.bmp")
    programme_shader = initialise_shader_programme()
    # Запускаем основной цикл
    glutMainLoop()

main()
