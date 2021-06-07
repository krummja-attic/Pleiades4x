from typing import Optional, Tuple
import os
import pygame as pg

pg.init()

CLOCK = pg.time.Clock()

COLOR_KEY = (255, 0, 255)
BACKGROUND_COLOR = (21, 21, 21)
_FONT_PATH = os.path.join("assets", "ShareTechMono-Regular.ttf")
FONT = pg.font.Font(_FONT_PATH, 18)

pg.mouse.set_visible(False)
pg.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))

FULLSCREEN = False
SCREEN_MODE = (0, pg.FULLSCREEN)[FULLSCREEN]

if FULLSCREEN:
    info = pg.display.Info()
    SCREEN_SIZE = (info.current_w, info.current_h)
else:
    SCREEN_SIZE = (1400, 1000)

SCREEN_RECT = pg.Rect((0, 0), SCREEN_SIZE)

BACKGROUND = pg.Surface(SCREEN_SIZE)
BACKGROUND.fill(BACKGROUND_COLOR)

SCREEN = pg.display.set_mode(SCREEN_SIZE, SCREEN_MODE)
SCREEN.set_colorkey(COLOR_KEY)

DEBUG = {
    "mouse": False,
    "fps": True,
    "gui": False,
}
