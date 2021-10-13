from PIL import ImageFont


def pt_to_px(pt: int) -> int:
    """Returns the height in pixels of an pt sized font"""
    return round(pt * (72/96))


small_font_size = 13
medium_font_size = 17
large_font_size = 37

small_font = ImageFont.truetype("calibril.ttf", small_font_size)
medium_font = ImageFont.truetype("calibril.ttf", medium_font_size)
large_font = ImageFont.truetype("calibrib.ttf", large_font_size)
