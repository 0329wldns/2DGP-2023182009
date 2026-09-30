from pathlib import Path

from pico2d import *

screen_width = 800
screen_height = 600

open_canvas(screen_width, screen_height)

sprite_sheet = load_image(str(Path(__file__).with_name('sonic-sprite.png')))

sprite_sheet_width = 399
frame_height = 35
frame_count = 12
walk_row_bottom = 420
frame = 0


def draw_frame(frame_index):
	frame_left = frame_index * sprite_sheet_width // frame_count
	frame_right = (frame_index + 1) * sprite_sheet_width // frame_count
	frame_width = frame_right - frame_left

	clear_canvas()
	sprite_sheet.clip_draw(
		frame_left,
		walk_row_bottom,
		frame_width,
		frame_height,
		screen_width // 2,
		screen_height // 2,
		300,
		315,
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