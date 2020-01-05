"""Snake Arcade application window & game board constants."""

VERSION = 'v.0.9.0'

# Application window. Size in pixels.
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 640
WINDOW_TITLE = 'Snake Arcade'

# Game grid system. Cell (one grid square) size in pixels.
CELL = 16
COLUMNS = int(WINDOW_WIDTH / CELL)
ROWS = int(WINDOW_HEIGHT / CELL)

# Padding between the game board & window borders. Units in "cells".
PADDING = {'left': 1, 'right': 1, 'top': 6, 'bottom': 1}

# Game board edges.
BOARD_LEFT = PADDING['left'] + 1
BOARD_RIGHT = COLUMNS - (PADDING['right'])
BOARD_TOP = ROWS - (PADDING['top'])
BOARD_BOTTOM = PADDING['bottom'] + 1

# Frames per second.
FPS = 60
