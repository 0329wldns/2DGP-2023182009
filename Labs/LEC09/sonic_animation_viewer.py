from pathlib import Path

from pico2d import *

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
SPRITE_SHEET_PATH = str(Path(__file__).with_name('sonic-sprite.png'))

# 캔버스 높이의 절반 높이로 확대해 그린다 (원본 비율 유지)
TARGET_SPRITE_HEIGHT = CANVAS_HEIGHT // 2

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

# 재생 순서대로 나열한 동작 목록
ACTIONS = [
	('walk', walk_frames),
	('kick', kick_frames),
	('jump', jump_frames),
	('run', run_frames),
	('spring', spring_frames),
	('back_turn', back_turn_frames),
]

# 가장 큰 프레임 높이가 타깃 높이가 되도록 하는 확대 비율 (비율 유지)
MAX_FRAME_HEIGHT = max(max(height for _, _, _, height in frames) for _, frames in ACTIONS)
SCALE = TARGET_SPRITE_HEIGHT / MAX_FRAME_HEIGHT

FRAME_RATE = 10  # 프레임 전환 속도(초당 프레임 수)
REPEAT_COUNT = 5  # 동작당 반복 횟수


def draw_frame(frames, frame_index):
	left, bottom, width, height = frames[frame_index]
	draw_height = max(1, round(height * SCALE))
	draw_width = max(1, round(width * SCALE))
	sprite_sheet.clip_draw(
		left, bottom, width, height,
		CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2,
		draw_width, draw_height,
	)


def main():
	global sprite_sheet

	open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
	sprite_sheet = load_image(SPRITE_SHEET_PATH)

	action_name, action_frames = ACTIONS[0]
	frame_index = 0
	frame_timer = get_time()
	repeat = 0

	running = True
	while running:
		for event in get_events():
			if event.type == SDL_QUIT:
				running = False
			elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
				running = False

		now = get_time()
		if now - frame_timer >= 1.0 / FRAME_RATE:
			frame_timer = now
			frame_index = (frame_index + 1) % len(action_frames)
			if frame_index == 0:
				repeat += 1
				if repeat == REPEAT_COUNT:
					repeat = 0

		clear_canvas()
		draw_frame(action_frames, frame_index)
		update_canvas()
		delay(0.05)

	close_canvas()


if __name__ == '__main__':
	main()
