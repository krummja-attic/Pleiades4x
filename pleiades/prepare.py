from typing import Optional, Tuple
import os
import pygame as pg

pg.init()

CLOCK = pg.time.Clock()

COLOR_KEY = (255, 0, 255)
BACKGROUND_COLOR = (21, 21, 21)

pg.mouse.set_visible(False)
pg.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))

FULLSCREEN = True
SCREEN_MODE = (0, pg.FULLSCREEN)[FULLSCREEN]

if FULLSCREEN:
    info = pg.display.Info()
    SCREEN_SIZE = (info.current_w, info.current_h)
else:
    SCREEN_SIZE = (1400, 1000)

SCREEN_RECT = pg.Rect((0, 0), SCREEN_SIZE)

background = pg.Surface(SCREEN_SIZE)
background.fill(BACKGROUND_COLOR)

pg.display.set_mode(SCREEN_SIZE, SCREEN_MODE)
pg.display.get_surface().set_colorkey(COLOR_KEY)

DEBUG = {
    "mouse": False,
    "fps": True,
    "gui": False,
}
