"""
Module used to extract metadata from an image,
such as EXIF, GPS, and TIFF tags.

"""

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from GPSPhoto import gpsphoto
import os

ONE_MEGABYTE = 1048576

def get_image(image: str | Image.Image) -> Image.Image:
    """
    Returns a given image if it's an instance of ``PIL.Image.Image``,
    otherwise, opens the image using the ``PIL.Image.open`` method.

    Args:
        image (str | Image.Image): Pillow Image instance, or a path to an image.

    Returns:
        Image.Image: The image file.
    """
    return Image.open(image) if isinstance(image, str) else image

def get_bits(image: Image.Image) -> str:
    return str(image.bits) if "bits" in image.__dir__() else None

def format_size(size: int) -> str:
    """
    Return a formatted string of a file size in KB or MB.

    Args:
        size (int): Size in bytes

    Returns:
        str: formatted result string
    """
    result = 0
    if size >= ONE_MEGABYTE:
        result = (size / (1024 * 1024))
        return f"{result:.2f} MB"
    else:
        result = size / 1024
        return f"{result:.2f} KB"

def get_image_info(image: Image.Image) -> str:
    """
    Get multiple attributes of the image file as a string.

    Args:
        image (Image.Image): The provided image file.

    Returns:
        str: image information as a multi-line string
    """
    bit_count = get_bits(image)
    bytes = os.path.getsize(image.filename)
    info_str = f"File: \"{image.filename}\"\n"
    info_str += f"Size: {format_size(bytes)}\n"
    if bit_count: info_str += f"Number of bits: {bit_count}\n"
    info_str += f"Entropy: {image.entropy():.3f}\n"
    if image.format:
        info_str += f"Format: {image.format} ({image.format_description})\n"

    info_str += f"Number of bands: {len(image.getbands())}.\nSize: {image.size[0]}x{image.size[1]}"
    return info_str


def get_metadata(image: str | Image.Image) -> tuple[str, str, str]:
    """
    Extract different metadata types from an image.

    Args:
        image (str | Image.Image): Pillow Image instance, or a path to an image.

    Returns:
        tuple[str, str, str]: EXIF, GPS, and TIFF data as strings.
    """
    exif_table = {}
    image_file = get_image(image)
    info = image_file.getexif()

    # Collect EXIF data from image
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        exif_table[decoded] = value

    # Collect GPS data from image (if any)
    gps_info = {}
    if 'GPSInfo' in exif_table:
        gps_info = gpsphoto.getGPSData(image_file.filename)

    for key, value in gps_info.items():
        exif_table[key] = value

    tiff_metadata = {}
    if image_file.format.lower() == 'tiff':
        for tag in image_file.tag.items():
            tiff_metadata[TAGS.get(tag[0])] = tag[1]

    return stringfy(exif_table, tiff_metadata)


def stringfy(exif_table: dict, tiff_metadata: dict) -> tuple[str, str, str]:
    """
    Parse tags tables and return them as strings.

    Args:
        exif_table (dict): A ``dict`` of EXIF and GPS image data.
        tiff_metadata (dict): A ``dict`` of TIFF image data (for ``.tiff`` images only).

    Returns:
        tuple[str, str, str]: Strings containing all data.
    """
    EXIF_STRING = ""
    for key, val in exif_table.items():
        EXIF_STRING += f'{str(key)}: {str(val)}\n'
        EXIF_STRING += f'---------------------------------------------\n'

    TIFF_STRING = ""
    for key, val in tiff_metadata.items():
        TIFF_STRING += f'{str(key)}: {str(val)}\n'

    return EXIF_STRING, TIFF_STRING