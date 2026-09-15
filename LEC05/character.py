from pico2d import *

screen_width = 800
screen_height = 600

open_canvas(screen_width, screen_height)

class Object:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.facing = [1, 0]
        self.image = image

    def draw(self):
        self.image.draw(self.x, self.y)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def turnLeft(self):
        if self.facing[0] == 1 and self.facing[1] == 0:
            self.facing[0] = 0
            self.facing[1] = 1
        elif self.facing[0] == 0 and self.facing[1] == 1:
            self.facing[0] = -1
            self.facing[1] = 0
        elif self.facing[0] == -1 and self.facing[1] == 0:
            self.facing[0] = 0
            self.facing[1] = -1
        elif self.facing[0] == 0 and self.facing[1] == -1:
            self.facing[0] = 1
            self.facing[1] = 0

grass = Object(400, 30, load_image('grass.png'))
character = Object(100, 90, load_image('character.png'))

objects = (grass, character)

dis = 0
speed = 2

while True:

    character.move(character.facing[0] * speed, character.facing[1] * speed)
    dis += speed

    clear_canvas()

    for obj in objects:
        obj.draw()

    update_canvas()
    delay(0.01)

    if dis >= 400:
        character.turnLeft()
        dis = 0

close_canvas()

