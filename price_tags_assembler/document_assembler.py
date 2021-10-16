# Local Imports
from .store_item import *
from .size_config import *


class PriceTagPage:
    def __init__(self, items: list[StoreItem], offset: int = 0):
        """Document holding up to 36 price tags in each page"""
        self.items = items
        self.items_on_page = 0
        self.offset = offset    # Number of stickers missing from printing paper (count left to right, row by row, top to bottom)

        for i in range(offset):
            self.items.insert(0, '')    

        # Fill in the page with price tags
        self.image = Image.new('RGB', (DOCUMENT_WIDTH, DOCUMENT_HEIGHT), 'white')
        for item in self.items:
            if item:
                self.place_price_tag(self.image, item)
            else:
                self.place_blank_item()

    def place_price_tag(self, document: Image, item: StoreItem):
        """
        Places a price tag image onto the price tag document
        Default None = Blank Item for offset
        """
        price_tag_img = item.create_price_tag()
        cur_row = self.items_on_page // 4
        cur_column = self.items_on_page % 4

        cur_pos_x = SIDE_GAP + (cur_column * TAG_WIDTH) + (cur_column * CROSS_GAP) 
        cur_pos_y = TOP_BOTTOM_GAP + (cur_row * TAG_HEIGHT)

        if cur_row >= 5:
            cur_pos_y += CROSS_GAP 
        
        document.paste(price_tag_img, (cur_pos_x, cur_pos_y))
        
        # Increment item count
        self.items_on_page += 1
        return

    def place_blank_item(self):
        """Place a blank, place-holder item onto the page."""
        self.items_on_page += 1
        return


class PriceTagDocument:
    def __init__(self, all_items: list[StoreItem], offset: int):
        self.all_items = all_items
        # Add blank spaces for offset
        for i in range(offset):
            self.all_items.insert(0, '')
        
        self.pages = []
        if len(self.all_items) > 36:
            # Split items into groups of 36 (for each page)
            for i in range(0, len(self.all_items), 36):
                page = PriceTagPage(self.all_items[i:i+36])
                self.pages.append(page)
        else:
            page = PriceTagPage(self.all_items)
            self.pages.append(page) 
        self.page_count = len(self.pages)

    def preview_document(self):
        """Preview the first page of the document"""
        self.pages[0].image.show()
        
    def save_document(self, path) -> None:
        """
        Save the pdf document containing all pages @ 300 PPI
        """
        if len(self.pages) > 1:
            self.pages[0].image.save(path, save_all=True, append_images=[page.image for page in self.pages[1:]], resolution=300)
        else:
            self.pages[0].image.save(path, resolution=300)
        return
