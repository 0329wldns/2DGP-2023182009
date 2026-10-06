from pathlib import Path

from pico2d import *

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
SPRITE_SHEET_PATH = str(Path(__file__).with_name('sonic-sprite.png'))

sprite_sheet = None

# 동작별 프레임 정의: (left, bottom, width, height)
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


def draw_frame(frames, frame_index):
	left, bottom, width, height = frames[frame_index]
	sprite_sheet.clip_draw(
		left, bottom, width, height,
		CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2,
		width * 4, height * 4,
	)


def main():
	global sprite_sheet

	open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
	sprite_sheet = load_image(SPRITE_SHEET_PATH)

	running = True
	while running:
		for event in get_events():
			if event.type == SDL_QUIT:
				running = False
			elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
				running = False

		clear_canvas()
		draw_frame(jump_frames, 0)
		update_canvas()
		delay(0.1)

	close_canvas()


if __name__ == '__main__':
	main()
