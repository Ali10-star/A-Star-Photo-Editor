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
        effect_vars: dict[Any], image: Image, export_func: Callable[[str, str, str],None],
        save_thumb_func: Callable[[str, str, str],None]
    ):
        super().__init__(master=parent)
        self.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        # Tabs
        self.add('Position')
        self.add('Color')
        self.add('Effect')
        self.add('Export')
        self.add('File')

        # Widgets
        PositionFrame(self.tab('Position'), pos_vars)
        ColorFrame(self.tab('Color'), image, color_vars)
        EffectFrame(self.tab('Effect'), effect_vars)
        ExportFrame(self.tab('Export'), export_func, save_thumb_func)
        InfoFrame(self.tab('File'), image)


class InfoFrame(ctk.CTkFrame):
    """
    CTkFrame to display image EXIF, GPS, and TIFF tags (if found).
    """
    def __init__(self, parent: ctk.CTkFrame, image: Image) -> None:
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')
        EXIF_STRING, TIFF_STRING = Metadata.get_metadata(image)
        IMAGE_INFO = Metadata.get_image_info(image)

        InfoPanel(self, panel_name='Image Data', info_str=IMAGE_INFO, custom_box_height=130)
        if EXIF_STRING:
            InfoPanel(self, panel_name='EXIF & GPS Data', info_str=EXIF_STRING)
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
        SliderPanel(
            self,
            panel_name='Hue',
            data_var=effect_vars['hue'],
            min_value=-100,
            max_value=100,
        )

        RevertButton(
            self,
            (effect_vars['effect'], EFFECT_OPTIONS[0]),
            (effect_vars['blur'], BLUR_DEFAULT),
            (effect_vars['contrast'], CONTRAST_DEFAULT),
            (effect_vars['balance'], BALANCE_DEFAULT),
            (effect_vars['hue'], HUE_DEFAULT),
        )


class ExportFrame(ctk.CTkFrame):
    """
    CTkFrame to export the open image in different output formats.
    """
    def __init__(self, parent: ctk.CTkFrame, export_func: Callable, thumbnail_save_func: Callable):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')

        self.file_name = ctk.StringVar()
        self.file_extension = ctk.StringVar(value='jpg')
        self.path = ctk.StringVar()
        self.quality = ctk.DoubleVar(value=100)

        self.thumbnail_name = ctk.StringVar()
        self.thumbnail_path = ctk.StringVar()
        self.thumbnail_width = ctk.IntVar(value=200)
        self.thumbnail_height = ctk.IntVar(value=200)

        FileNamePanel(self, self.file_name, self.file_extension, self.quality)
        FilePathPanel(self, self.path)
        ThumbnailPanel(
            self,
            self.thumbnail_name,
            self.thumbnail_path,
            (self.thumbnail_width, self.thumbnail_height),
            thumbnail_save_func
        )

        ExportButton(
            self, export_func, self.file_name, self.file_extension, self.path,
            self.quality
        )