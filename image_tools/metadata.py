"""
Module used to extract metadata from an image,
such as EXIF, GPS, and TIFF tags.

"""

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from GPSPhoto import gpsphoto

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

    tiff_metadata = {}
    if image_file.format.lower() == 'tiff':
        for tag in image_file.tag.items():
            tiff_metadata[TAGS.get(tag[0])] = tag[1]

    return stringfy(exif_table, gps_info, tiff_metadata)


def stringfy(exif_table: dict, gps_info: dict, tiff_metadata: dict) -> tuple[str, str, str]:
    """
    Parse tags tables and return them as strings.

    Args:
        exif_table (dict): A ``dict`` of EXIF image data.
        gps_info (dict): A ``dict`` of GPS image data.
        tiff_metadata (dict): A ``dict`` of TIFF image data (for ``.tiff`` images only).

    Returns:
        tuple[str, str, str]: Strings containing all data.
    """
    EXIF_STRING = ""
    for key, val in exif_table.items():
        EXIF_STRING += f'{str(key)}: {str(val)}\n'
        EXIF_STRING += f'---------------------------------------------\n'

    GPS_STRING = ""
    for key, val in gps_info.items():
        GPS_STRING += f'{str(key)}: {str(val)}\n'

    TIFF_STRING = ""
    for key, val in tiff_metadata.items():
        TIFF_STRING += f'{str(key)}: {str(val)}\n'

    return EXIF_STRING, GPS_STRING, TIFF_STRING