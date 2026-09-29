# 실습 과제 진행
from pico2d import *

open_canvas(800, 600)

boy = load_image('character.png')

speed = 3

def move_top():
    print('TOP')
    pass

def move_right():
    print('RIGHT')
    pass

def move_bottom():
    print('BOTTOM')
    pass

def move_left():
    print('LEFT')
    pass

def move_circle():
    for degree in range(0, 360, speed):
        theta = math.radians(degree)
        x = 400 + 200 * math.cos(theta)
        y = 300 + 200 * math.sin(theta)

        clear_canvas()
        boy.draw(x, y)
        update_canvas()
        delay(0.01)

def move_rectangle():
    print('rectangle')
    move_top()
    move_right()
    move_bottom()
    move_left()
    pass

def move_triangle():
    print('triangle')
    pass

while True:
    move_circle()
    move_rectangle()
    move_triangle()
    pass