from pathlib import Path

from pico2d import *

screen_width = 800
screen_height = 600

open_canvas(screen_width, screen_height)

sprite_sheet = load_image(str(Path(__file__).with_name('sonic-sprite.png')))

walk_frames = [
	(8, 408, 26, 37),
	(36, 408, 28, 37),
	(65, 407, 31, 38),
	(97, 409, 37, 37),
	(135, 411, 32, 35),
	(170, 409, 32, 38),
	(206, 409, 26, 38),
	(238, 409, 24, 37),
	(263, 409, 30, 37),
	(295, 409, 36, 37),
	(334, 410, 32, 36),
	(370, 409, 29, 38),
]

kick_frames = [
	(1, 361, 33, 40),
	(39, 363, 35, 39),
	(89, 363, 35, 38),
	(129, 362, 35, 42),
	(181, 363, 34, 41),
	(225, 363, 36, 40),
]

jump_frames = [
	(1, 326, 29, 30),
	(35, 327, 29, 31),
	(67, 327, 30, 29),
	(98, 327, 31, 29),
	(131, 327, 29, 30),
	(162, 326, 29, 31),
	(193, 326, 30, 29),
	(229, 326, 32, 29),
	(267, 325, 31, 30),
]

run_frames = [
	(1, 207, 29, 33),
	(36, 207, 30, 33),
	(74, 208, 37, 31),
	(123, 208, 39, 32),
	(172, 208, 39, 31),
	(218, 208, 38, 32),
]

spring_frames = [
	(1, 154, 24, 41),
	(31, 154, 29, 41),
	(65, 154, 20, 41),
	(90, 155, 25, 40),
	(119, 155, 25, 40),
	(149, 154, 20, 41),
]

back_turn_frames = [
	(1, 108, 27, 37),
	(31, 110, 31, 35),
	(64, 110, 31, 35),
	(99, 110, 33, 35),
	(136, 110, 32, 35),
	(174, 110, 35, 35),
	(217, 110, 33, 35),
	(254, 111, 33, 34),
]

animations = [
	walk_frames,
	kick_frames,
	jump_frames,
	run_frames,
	spring_frames,
	back_turn_frames,
]
animation_index = 0
frame_count = len(animations[animation_index])
animation_repeat = 0
target_sprite_height = screen_height // 2
frame = 0


def draw_frame(frames, frame_index):
	frame_left, frame_bottom, frame_width, frame_height = frames[frame_index]
	draw_height = target_sprite_height
	draw_width = frame_width * draw_height // frame_height

	clear_canvas()
	sprite_sheet.clip_draw(
		frame_left,
		frame_bottom,
		frame_width,
		frame_height,
		screen_width // 2,
		screen_height // 2,
		draw_width,
		draw_height,
	)
	update_canvas()
	delay(1 / 30 if frames is jump_frames else 1 / 24)


running = True
while running:
	for event in get_events():
		if event.type == SDL_QUIT:
			running = False
		elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
			running = False

	draw_frame(animations[animation_index], frame)
	if animations[animation_index] is jump_frames and frame == frame_count - 1:
		delay(2 / 30)
	frame += 1
	if frame == frame_count:
		frame = 0
		animation_repeat += 1
		if animation_repeat == 5:
			animation_repeat = 0
			animation_index = (animation_index + 1) % len(animations)
			frame_count = len(animations[animation_index])
			delay(1.0)

close_canvas()