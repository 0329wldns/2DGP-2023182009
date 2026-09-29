import math

from pico2d import *


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CHARACTER_FILE = 'character.png'
FRAME_DELAY = 0.01


open_canvas(SCREEN_WIDTH, SCREEN_HEIGHT)
character = load_image(CHARACTER_FILE)


def draw_character(x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(FRAME_DELAY)


def move_in_circle():
    center_x = SCREEN_WIDTH / 2
    center_y = SCREEN_HEIGHT / 2
    radius = 200

    for degree in range(360):
        angle = math.radians(degree)
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        draw_character(x, y)


def move_in_rectangle():
    left = 150
    right = 650
    bottom = 100
    top = 500
    step = 5

    for x in range(left, right + 1, step):
        draw_character(x, top)
    for y in range(top, bottom - 1, -step):
        draw_character(right, y)
    for x in range(right, left - 1, -step):
        draw_character(x, bottom)
    for y in range(bottom, top + 1, step):
        draw_character(left, y)


def move_in_triangle():
    left = (150, 100)
    right = (650, 100)
    top = (400, 500)
    step = 5

    move_on_line(left, right, step)
    move_on_line(right, top, step)
    move_on_line(top, left, step)


def move_on_line(start, end, step):
    start_x, start_y = start
    end_x, end_y = end
    distance = math.hypot(end_x - start_x, end_y - start_y)
    frame_count = max(1, int(distance / step))

    for frame in range(frame_count + 1):
        progress = frame / frame_count
        x = start_x + (end_x - start_x) * progress
        y = start_y + (end_y - start_y) * progress
        draw_character(x, y)


while True:
    move_in_circle()
    move_in_rectangle()
    move_in_triangle()