from typing import Optional, Tuple
import os
import pygame as pg

pg.init()

CLOCK = pg.time.Clock()

SCREEN_SIZE = (1400, 1000)
COLOR_KEY = (0, 0, 0)
BACKGROUND_COLOR = (21, 21, 21)
SCREEN_RECT = pg.Rect((0, 0), SCREEN_SIZE)
_FONT_PATH = os.path.join("assets", "ShareTechMono-Regular.ttf")
FONT = pg.font.Font(_FONT_PATH, 18)

pg.mouse.set_visible(False)
pg.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))

screen = pg.display.set_mode(SCREEN_SIZE)
screen.fill(BACKGROUND_COLOR)
pg.display.update()
