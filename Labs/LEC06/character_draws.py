# 실습 과제 진행
from pico2d import *

open_canvas(800, 600)

boy = load_image('character.png')

speed = 2

# 0.01초의 딜레이를 두고 넘겨준 좌표에 캐릭터를 그림
def draw_boy(x, y):
    clear_canvas()
    boy.draw(x, y)
    update_canvas()
    delay(0.01)

def move_top():
    for x in range(50, 551, speed * 10):
        draw_boy(x, 550)

def move_right():
    for y in range(550, 49, -speed * 10):
        draw_boy(550, y)
    pass

def move_bottom():
    for x in range(550, 49, -speed * 10):
        draw_boy(x, 50)
    pass

def move_left():
    for y in range(50, 551, speed * 10):
        draw_boy(50, y)
    pass

def move_left_side():
    x = 50
    y = 50
    while x < 300:
        x += speed * 6.25
        y += speed * 6.25
        draw_boy(x, y)
        print(x, y)
    pass

def move_right_side():
    x = 300
    y = 300
    while x < 550:
        x += speed * 6.25
        y -= speed * 6.25
        draw_boy(x, y)
    pass

def move_circle():
    for degree in range(0, 360, speed):
        theta = math.radians(degree)
        x = 400 + 200 * math.sin(theta)
        y = 300 + 200 * math.cos(theta)

        draw_boy(x, y)

def move_rectangle():
    move_top()
    move_right()
    move_bottom()
    move_left()
    pass

def move_triangle():
    move_bottom()
    move_left_side()
    move_right_side()
    pass

while True:
    move_circle()
    move_rectangle()
    move_triangle()