import os
import sys
from pathlib import Path

from pico2d import (
	SDL_KEYDOWN,
	SDL_QUIT,
	SDLK_ESCAPE,
	Image,
	clear_canvas,
	close_canvas,
	delay,
	get_events,
	get_time,
	load_font,
	load_image,
	open_canvas,
	update_canvas,
)

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
SPRITE_SHEET_PATH = str(Path(__file__).with_name('sonic-sprite.png'))

# 캔버스 높이의 절반 높이로 확대해 그린다 (원본 비율 유지)
TARGET_SPRITE_HEIGHT = CANVAS_HEIGHT // 2

sprite_sheet: Image | None = None

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

FRAME_TIME = 0.1  # 프레임 간격(초)
REPEAT_COUNT = 5  # 동작당 반복 횟수
PAUSE_TIME = 1.0  # 동작 간 정지 시간(초)

PHASE_PLAY = 'play'
PHASE_PAUSE = 'pause'

PHASE_LABELS = {PHASE_PLAY: 'PLAY', PHASE_PAUSE: 'PAUSE'}

# 화면에 상태를 찍을 폰트 후보 (운영체제별 폰트 경로)
FONT_CANDIDATES = [
	r'C:\Windows\Fonts\malgun.ttf',
	r'C:\Windows\Fonts\arial.ttf',
	'/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
]


def draw_frame(frames, frame_index):
	assert sprite_sheet is not None
	left, bottom, width, height = frames[frame_index]
	draw_height = max(1, round(height * SCALE))
	draw_width = max(1, round(width * SCALE))
	sprite_sheet.clip_draw(
		left, bottom, width, height,
		CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2,
		draw_width, draw_height,
	)


def load_hud_font(size=22):
	for path in FONT_CANDIDATES:
		if os.path.exists(path):
			try:
				return load_font(path, size)
			except OSError:
				continue
	return None


def validate_frames(sheet_width, sheet_height):
	for action_name, frames in ACTIONS:
		if not frames:
			raise ValueError(f'{action_name} 동작에 프레임이 없습니다.')
		for frame_index, (left, bottom, width, height) in enumerate(frames):
			if (
				left < 0
				or bottom < 0
				or width <= 0
				or height <= 0
				or left + width > sheet_width
				or bottom + height > sheet_height
			):
				raise ValueError(
					f'{action_name} 프레임 {frame_index}가 스프라이트 시트 범위를 벗어났습니다.'
				)


def draw_hud(font, action_name, frame_index, frame_total, repeat, phase):
	if font is None:
		return
	# 정지 상태에서는 5회 반복이 끝난 직후이므로 5회로 표시한다
	shown_repeat = REPEAT_COUNT if phase == PHASE_PAUSE else repeat + 1
	text = f'{action_name}  frame {frame_index + 1}/{frame_total}  repeat {shown_repeat}/{REPEAT_COUNT}  [{PHASE_LABELS[phase]}]'
	font.draw(20, CANVAS_HEIGHT - 30, text, (20, 20, 20))


def update_state(state, now):
	"""상태 기계를 한 번 갱신한다. state는 main()의 재생 상태 딕셔너리."""
	if state['phase'] == PHASE_PAUSE:
		# 정지 상태: 마지막 프레임을 유지하고 1초 뒤 다음 동작으로 넘어간다
		if now - state['pause_timer'] >= PAUSE_TIME:
			state['repeat'] = 0
			state['frame_index'] = 0
			state['frame_timer'] = now
			state['action_index'] = (state['action_index'] + 1) % len(ACTIONS)
			state['action_name'], state['action_frames'] = ACTIONS[state['action_index']]
			state['phase'] = PHASE_PLAY
		return

	while now - state['frame_timer'] >= FRAME_TIME:
		state['frame_timer'] += FRAME_TIME
		state['frame_index'] = (state['frame_index'] + 1) % len(state['action_frames'])
		if state['frame_index'] == 0:
			state['repeat'] += 1
			if state['repeat'] == REPEAT_COUNT:
				state['repeat'] = 0
				state['phase'] = PHASE_PAUSE
				state['pause_timer'] = now
				return


def render(state, hud_font):
	clear_canvas()
	draw_frame(state['action_frames'], state['frame_index'])
	draw_hud(
		hud_font,
		state['action_name'],
		state['frame_index'],
		len(state['action_frames']),
		state['repeat'],
		state['phase'],
	)
	update_canvas()


def main():
	global sprite_sheet

	open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
	try:
		try:
			sprite_sheet = load_image(SPRITE_SHEET_PATH)
		except OSError as error:
			print(f'스프라이트를 불러올 수 없습니다: {SPRITE_SHEET_PATH}', file=sys.stderr)
			print(error, file=sys.stderr)
			return

		try:
			validate_frames(sprite_sheet.w, sprite_sheet.h)
		except ValueError as error:
			print(f'프레임 정의 오류: {error}', file=sys.stderr)
			return

		hud_font = load_hud_font()
		action_name, action_frames = ACTIONS[0]
		state = {
			'action_index': 0,
			'action_name': action_name,
			'action_frames': action_frames,
			'frame_index': 0,
			'frame_timer': get_time(),
			'repeat': 0,
			'phase': PHASE_PLAY,
			'pause_timer': 0.0,
		}

		running = True
		while running:
			for event in get_events():
				if event.type == SDL_QUIT:
					running = False
				elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
					running = False

			update_state(state, get_time())
			render(state, hud_font)
			delay(1.0 / 60.0)
	finally:
		close_canvas()


if __name__ == '__main__':
	main()
