from pathlib import Path

from pico2d import *

screen_width = 800
screen_height = 600

open_canvas(screen_width, screen_height)

sprite_sheet = load_image(str(Path(__file__).with_name('sonic-sprite.png')))

clear_canvas()
sprite_sheet.draw(screen_width // 2, screen_height // 2)
update_canvas()
delay(2.0)

close_canvas()