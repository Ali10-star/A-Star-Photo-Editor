"""
Module responsible for providing image manipulation functionalities.
"""

from settings import *
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

def sepia_palette() -> list[int]:
    """
    Generate a sepia palette to apply to images.

    Returns:
        list[int]: the resulting palette.
    """
    BASE_COLOR = (255, 240, 192)
    palette = []
    r, g, b = BASE_COLOR
    for i in range(255):
        new_red = r * i // 255
        new_green = g * i // 255
        new_blue = b * i // 255
        palette.extend((new_red, new_green, new_blue))

    return palette

def sepia_filter(image: Image) -> Image:
    """
    Converts an image to sepia tone.

    Args:
    image: A PIL.Image object.

    Returns:
    A PIL.Image object in sepia tone.
    """
    sepia = sepia_palette()
    gray = image.convert("L")
    gray.putpalette(sepia)

    return gray.convert("RGB")


class ImageManipulator:
    """
    Class containing all image-manipulation methods used in the app.
    """
    def __init__(self, image_file: Image.Image) -> None:
        self.used_image = image_file
        if self.used_image.mode == 'P':
            self.used_image = self.used_image.convert('RGB')


    def rotate_image(self, rotation_angle: float) -> None:
        """
        Apply a rotation by a given angle to the image.

        Args:
            rotation_angle (float): rotation angle.
        """
        if rotation_angle != ROTATE_DEFAULT:
            self.used_image = self.used_image.rotate(angle=rotation_angle)

    def zoom_image(self, zoom_amount: float) -> None:
        """
        Zoom the image by a given amount.

        Args:
            zoom_amount (float): The given zoom amount.
        """
        if zoom_amount != ZOOM_DEFAULT:
            self.used_image = ImageOps.crop(self.used_image, border=zoom_amount)

    def flip_image(self, flip_option: str) -> None:
        """
        Flip the image horizontally, vertically, or both ways.

        Args:
            flip_option (str): The flip type, can be 'X' for horizontal,
            'Y' for vertical, and 'Both' for both directions.
        """
        if flip_option != 'None':
            mirror = flip_option in ('X', 'Both')
            flip = flip_option in ('Y', 'Both')
            if mirror:
                self.used_image = ImageOps.mirror(self.used_image)
            if flip:
                self.used_image = ImageOps.flip(self.used_image)

    def apply_brightness(self, brightness_value: float) -> None:
        """
        Change the image brightness by a given amount.

        Args:
            brightness_value (float): New brightness value. When set to 0,
            the image becomes completely black.
        """
        if brightness_value != BRIGHTNESS_DEFAULT:
            brightness_enhancer = ImageEnhance.Brightness(self.used_image)
            self.used_image =  brightness_enhancer.enhance(brightness_value)

    def apply_vibrance(self, vibrance_value: float) -> None:
        """
        Change the image vibrance by a given amount.

        Args:
            vibrance_value (float): New vibrance value. When set to 0,
            the image becomes grayscale.
        """
        if vibrance_value != VIBRANCE_DEFAULT:
            brightness_enhancer = ImageEnhance.Color(self.used_image)
            self.used_image =  brightness_enhancer.enhance(vibrance_value)

    def apply_grayscale(self, grayscale_flag: bool) -> None:
        """
        Convert the image to grayscale (Black and White).

        Args:
            grayscale_flag (bool): Set to True, if the filter is chosen.
        """
        if grayscale_flag:
             self.used_image = ImageOps.grayscale(self.used_image)

    def invert_colors(self, invert_flag: bool) -> None:
        """
        Invert the image colors (Negative filter).

        Args:
            invert_flag (bool): Set to True, if the filter is chosen.
        """
        if invert_flag:
            try:
                self.used_image = ImageOps.invert(self.used_image)
            except:
                raise OSError

    def apply_sepia(self, sepia_flag: bool) -> None:
        """
        Apply a sepia filter to the image.

        Args:
            sepia_flag (bool): Set to True, if the filter is chosen.
        """
        if sepia_flag:
            self.used_image = sepia_filter(self.used_image)

    def apply_4color_filter(self, four_col_flag: bool) -> None:
        """
        Apply a 4-color filter to the image i.e. display the image using only 4 colors,
        extracted from the image by an algorithm implemented in Pillow.

        Args:
            four_col_flag (bool): Set to True, if the filter is chosen.
        """
        if four_col_flag:
            self.used_image = self.used_image.convert("P", palette=Image.ADAPTIVE, colors=4)

    def blur_image(self, blur_value: float) -> None:
        """
        Blur the image by a given amount.

        Args:
            blur_value (float): Blur intensity.
        """
        if blur_value != BLUR_DEFAULT:
            blur_filter = ImageFilter.GaussianBlur(blur_value)
            self.used_image = self.used_image.filter(blur_filter)

    def change_contrast(self, contrast_value: float) -> None:
        """
        Change the image contrast by a given amount.

        Args:
            contrast_value (float): Used contrast value.
        """
        if contrast_value != CONTRAST_DEFAULT:
            contrast_filter = ImageFilter.UnsharpMask(contrast_value)
            self.used_image = self.used_image.filter(contrast_filter)

    def change_balance(self, balance_value: float) -> None:
        """
        Change the image balance by a given amount.

        Args:
            balance_value (float): Used balance value.
        """
        if balance_value != BALANCE_DEFAULT:
            balance_enhancer = ImageEnhance.Color(self.used_image)
            self.used_image = balance_enhancer.enhance(balance_value)

    def apply_effect(self, effect_name: str) -> None:
        """
        Applies different types of Pillow built-in filters.

        Args:
            effect_name (str): Selected effect, valid values are
            [Emboss, Find edges, Contour, Edge enhance]
        """
        applied_effect = None
        match effect_name:
            case 'Emboss':
                applied_effect = ImageFilter.EMBOSS
            case 'Find edges':
                applied_effect = ImageFilter.FIND_EDGES
            case 'Contour':
                applied_effect = ImageFilter.CONTOUR
            case 'Edge enhance':
                applied_effect = ImageFilter.EDGE_ENHANCE

        if applied_effect:
            self.used_image = self.used_image.filter(applied_effect)

    @property
    def image_result(self) -> Image.Image:
        """
        Get the resulting image after applying all effects and filters.

        Returns:
            Image.Image: The resulting image.
        """
        return self.used_image