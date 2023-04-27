
def rgb_to_hex(r: float, g: float, b: float) -> str:
    """
    Convert an RGB color into a Hex color code.

    Args:
        r (float): The red channel component.
        g (float): The green channel component.
        b (float): The blue channel component.

    Returns:
        str: Resulting hex color code.
    """
    return f'#{r:02x}{g:02x}{b:02x}'

def clamp(val: float, minimum: int = 0, maximum: int = 255):
    """
    Clamp a given value within the range [``minimum``, ``maximum``]

    Args:
        val (float): provided value
        minimum (int, optional): The start of the range. Defaults to 0.
        maximum (int, optional): The end of the range. Defaults to 255.

    Returns:
        int: resulting value as an integer.
    """
    if val < minimum:
        return int(minimum)
    if val > maximum:
        return int(maximum)
    return int(val)

def colorscale(hexstr: str, scale_factor: float = None) -> str:
    """
    Scales a hex string by ``scale_factor``. Returns scaled hex string.

    To darken the color, use a float value between 0 and 1.
    To brighten the color, use a float value greater than 1.

    >>> colorscale("#DF3C3C", .5)
    #6F1E1E
    >>> colorscale("#52D24F", 1.6)
    #83FF7E
    >>> colorscale("#4F75D2", 1)
    #4F75D2

    Args:
        hexstr (str): The provided Hex color code.
        scale_factor (float): Value used to scale the color,
        if less than 1.0, darkens the color, if greater, it brightens it.
    Returns:
        str: The new hex color code, after scaling.
    """

    hexstr = hexstr.strip('#')


    r, g, b = int(hexstr[:2], 16), int(hexstr[2:4], 16), int(hexstr[4:], 16)

    if scale_factor < 0 or len(hexstr) != 6:
        return hexstr

    r = clamp(r * scale_factor)
    g = clamp(g * scale_factor)
    b = clamp(b * scale_factor)

    return "#%02x%02x%02x" % (r, g, b)
