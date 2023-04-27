"""
Module to create and manage editor menus.
"""
import customtkinter as ctk
import image_tools.metadata as Metadata
from panel import *
from settings import *
from typing import Any, Callable
from PIL.Image import Image

class Menu(ctk.CTkTabview):
    """
    Main tabbed menu for the editor. Subtype of customtkinter.CTkTabView
    """
    def __init__(
        self, parent: ctk.CTk, pos_vars: dict[Any], color_vars: dict[Any],
        effect_vars: dict[Any], image: Image, export_func: Callable[[str, str, str],None]
    ):
        super().__init__(master=parent)
        self.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        # Tabs
        self.add('Position')
        self.add('Color')
        self.add('Effect')
        self.add('Export')
        self.add('Info')

        # Widgets
        PositionFrame(self.tab('Position'), pos_vars)
        ColorFrame(self.tab('Color'), image, color_vars)
        EffectFrame(self.tab('Effect'), effect_vars)
        ExportFrame(self.tab('Export'), export_func)
        InfoFrame(self.tab('Info'), image)


class InfoFrame(ctk.CTkFrame):
    """
    CTkFrame to display image EXIF, GPS, and TIFF tags (if found).
    """
    def __init__(self, parent: ctk.CTkFrame, image: Image) -> None:
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')
        EXIF_STRING, GPS_STRING, TIFF_STRING = Metadata.get_metadata(image)

        if EXIF_STRING:
            InfoPanel(self, panel_name='EXIF Data', info_str=EXIF_STRING)
        if GPS_STRING:
            InfoPanel(self, panel_name='GPS Data', info_str=GPS_STRING)
        if TIFF_STRING:
            InfoPanel(self, panel_name='TIFF Data', info_str=TIFF_STRING)


class PositionFrame(ctk.CTkFrame):
    """
    CTkFrame to control image positioning, such as rotation, zoom and flipping.
    """
    def __init__(self, parent: ctk.CTkFrame, pos_vars: dict[Any]) -> None:
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')

        SliderPanel(
            self,
            panel_name='Rotation',
            data_var=pos_vars['rotate'],
            min_value=0,
            max_value=360,
        )
        SliderPanel(
            self,
            panel_name='Zoom',
            data_var=pos_vars['zoom'],
            min_value=0,
            max_value=400,
        )
        SegmentedPanel(
            self,
            panel_name='Invert',
            data_var=pos_vars['flip'],
            options=FLIP_OPTIONS,
        )
        RevertButton(
            self,
            (pos_vars['rotate'], ROTATE_DEFAULT),
            (pos_vars['zoom'], ZOOM_DEFAULT),
            (pos_vars['flip'], FLIP_OPTIONS[0]),
        )


class ColorFrame(ctk.CTkFrame):
    """
    CTkFrame to apply image color filters and effects (grayscale, sepia, ...),
    with functionality to extract colors from the open image.
    """
    def __init__(self, parent: ctk.CTkFrame, image: Image, color_vars: dict[Any]) -> None:
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')
        self.image_file = Metadata.get_image(image)

        SwitchPanel(
            self,
            (color_vars['grayscale'], 'B/W'),
            (color_vars['sepia'], 'Sepia'),
            (color_vars['invert'], 'Negative'),
            (color_vars['4-color'], '4-Color'),
        )
        SliderPanel(
            self,
            panel_name='Brightness',
            data_var=color_vars['brightness'],
            min_value=0,
            max_value=5,
        )
        SliderPanel(
            self,
            panel_name='Vibrance',
            data_var=color_vars['vibrance'],
            min_value=0,
            max_value=5,
        )

        ColorsPanel(self, self.image_file)

        RevertButton(
            self,
            (color_vars['grayscale'], GRAYSCALE_DEFAULT),
            (color_vars['sepia'], SEPIA_DEFAULT),
            (color_vars['invert'], INVERT_DEFAULT),
            (color_vars['4-color'], FOUR_COLOR_DEFAULT),
            (color_vars['brightness'], BRIGHTNESS_DEFAULT),
            (color_vars['vibrance'], VIBRANCE_DEFAULT),
        )


class EffectFrame(ctk.CTkFrame):
    """
    CTkFrame to apply different effects to the open image,
    such as blurring, changing contrast, balance.
    """
    def __init__(self, parent: ctk.CTkFrame, effect_vars: dict[Any]) -> None:
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')

        DropDownPanel(
            self, data_var=effect_vars['effect'], options=EFFECT_OPTIONS
        )
        SliderPanel(
            self,
            panel_name='Blur',
            data_var=effect_vars['blur'],
            min_value=0,
            max_value=30,
        )
        SliderPanel(
            self,
            panel_name='Contrast',
            data_var=effect_vars['contrast'],
            min_value=0,
            max_value=10,
        )
        SliderPanel(
            self,
            panel_name='Balance',
            data_var=effect_vars['balance'],
            min_value=0,
            max_value=10,
        )

        RevertButton(
            self,
            (effect_vars['effect'], EFFECT_OPTIONS[0]),
            (effect_vars['blur'], BLUR_DEFAULT),
            (effect_vars['contrast'], CONTRAST_DEFAULT),
            (effect_vars['balance'], BALANCE_DEFAULT),
        )


class ExportFrame(ctk.CTkFrame):
    """
    CTkFrame to export the open image in different output formats.
    """
    def __init__(self, parent: ctk.CTkFrame, export_func: Callable):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')

        self.file_name = ctk.StringVar()
        self.file_extension = ctk.StringVar(value='jpg')
        self.path = ctk.StringVar()

        FileNamePanel(self, self.file_name, self.file_extension)
        FilePathPanel(self, self.path)
        ExportButton(
            self, export_func, self.file_name, self.file_extension, self.path
        )
