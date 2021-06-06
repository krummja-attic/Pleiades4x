from typing import Optional, Tuple
import os
import pygame as pg

pg.init()

SCREEN_SIZE = (1400, 1000)
COLOR_KEY = (0, 0, 0)
BACKGROUND_COLOR = (21, 21, 21)
SCREEN_RECT = pg.Rect((0, 0), SCREEN_SIZE)
_FONT_PATH = os.path.join("assets", "ShareTechMono-Regular.ttf")
FONT = pg.font.Font(_FONT_PATH, 18)

screen = pg.display.set_mode(SCREEN_SIZE)

screen.fill(BACKGROUND_COLOR)
_render = FONT.render("P L E I A D E S", True, pg.Color("white"))
screen.blit(_render, _render.get_rect(center=SCREEN_RECT.center))
pg.display.update()
