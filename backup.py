# Price tag preview
"""tag_canvas = Canvas(root, width=TAG_WIDTH*2, height=TAG_HEIGHT*2, background='white')

price_bottom_left_x = TAG_WIDTH-PRICE_WIDTH
price_bottom_left_y = ceil((TAG_HEIGHT-PRICE_HEIGHT)/2)

price_top_right_x = TAG_WIDTH+1
price_top_right_y = price_bottom_left_y + PRICE_HEIGHT

tag_canvas.create_rectangle(price_bottom_left_x*2, price_bottom_left_y*2, price_top_right_x*2, price_top_right_y*2, fill=PRICE_COLOR)
tag_canvas.grid(row=1, column=3, rowspan=100, padx=30)"""
