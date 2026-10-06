from pico2d import *

open_canvas()

grass = load_image('grass.png')
character = load_image('animation_sheet.png')

# fill here

action = 0
frame = 0

while True:
    clear_canvas()
    grass.draw(400, 30)
    character.clip_draw(
        frame * 100, action * 100,
        100, 100,
        400, 220,
        500, 500
    )
    update_canvas()

    frame = (frame + 1) % 8
    if (frame == 0):
        action = (action + 1) % 4
    delay(0.05)

close_canvas()

