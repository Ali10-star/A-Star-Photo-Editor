"""
Global values and flags used across the application.
"""

import darkdetect

ROTATE_DEFAULT = 0
ZOOM_DEFAULT = 0
FLIP_OPTIONS = ['None', 'X', 'Y', 'Both']
BLUR_DEFAULT = 0
CONTRAST_DEFAULT = 0
BALANCE_DEFAULT = 0
EFFECT_OPTIONS = ['None', 'Emboss', 'Find edges', 'Contour', 'Edge enhance']
THEME_OPTIONS = ['Light', 'Dark', 'System']
BRIGHTNESS_DEFAULT = 1
VIBRANCE_DEFAULT = 1
HUE_DEFAULT = 0
GRAYSCALE_DEFAULT = False
SEPIA_DEFAULT = False
FOUR_COLOR_DEFAULT = False
INVERT_DEFAULT = False
# ----------------------------- COLORS --------------------------
WHITE = '#FFF'
GREY = 'grey'
DARK_GREY = '#212121' if darkdetect.isDark() else "gray70"
CANVAS_BACKGROUND = '#242424' if darkdetect.isDark() else "gray95"
CLOSE_BUTTON_COLOR = '#242424' if darkdetect.isLight() else "gray95"
BLUE = '#1F6AA5'
CLOSE_RED = '#8a0606'
SLIDER_BG = '#64686b'
PANEL_BG = '#181818' if darkdetect.isDark() else "gray75"
DROPDOWN_MAIN_COLOR = '#444'
DROPDOWN_HOVER_COLOR = '#333'
DROPDOWN_MENU_COLOR = '#666'
# ---------------------- APP PALETTE ----------------------------
BACKGROUND_PRIMARY = "#131c22"
BACKGROUND_SECONDARY = "#2C394B"
BACKGROUND_TERNARY = "#334756"
THEME_COLOR = "#FF4C29" if darkdetect.isDark() else "#2F58CD"
THEME_GRADIENT = "#ff401a" if darkdetect.isDark() else "#172c66"
THEME_HOVER = "#ff2b00" if darkdetect.isDark() else "#1c347b"
THEME_HOVER_GRADIENT = "#e62600" if darkdetect.isDark() else "#162962"