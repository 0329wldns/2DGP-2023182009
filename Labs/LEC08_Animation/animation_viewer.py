from pathlib import Path

from pico2d import *

screen_width = 800
screen_height = 600

open_canvas(screen_width, screen_height)

sprite_sheet = load_image(str(Path(__file__).with_name('sonic-sprite.png')))

frame_width = 133
frame_height = 105
frame_count = 3
second_row_bottom = frame_height * 3
frame = 0


def draw_frame(frame_index):
	clear_canvas()
	sprite_sheet.clip_draw(
		frame_index * frame_width,
		second_row_bottom,
		frame_width,
		frame_height,
		screen_width // 2,
		screen_height // 2,
		380,
		300,
	)
	update_canvas()
	delay(0.12)


running = True
while running:
	for event in get_events():
		if event.type == SDL_QUIT:
			running = False
		elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
			running = False

	draw_frame(frame)
	frame = (frame + 1) % frame_count

close_canvas()