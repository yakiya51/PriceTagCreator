def cm_to_px(cm, ppi=300):
    px_cm = ppi/2.54
    return round(px_cm * cm)

# Template Size (8.5 x 11 inches) in pixels @ 300 PPI
DOCUMENT_WIDTH = 2550
DOCUMENT_HEIGHT = 3300

TOP_BOTTOM_GAP = cm_to_px(1.35) # 1.35 cm
SIDE_GAP = cm_to_px(0.9) # 0.9 cm

CROSS_GAP = cm_to_px(0.24) # 0.22 cm

# Price Tag Size in pixels
TAG_WIDTH = cm_to_px(4.75) # 4.75 cm
TAG_HEIGHT = cm_to_px(2.75) # 2.75 cm

# Price Part of the Price Tag in pixels
PRICE_WIDTH = cm_to_px(2.61) # 2.61 cm
PRICE_HEIGHT = cm_to_px(1.26) # 1.26 cm


