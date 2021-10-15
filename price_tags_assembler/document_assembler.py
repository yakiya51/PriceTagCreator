from datetime import date
# Local Imports
from .store_item import *
from .size_config import *


class PriceTagPage:
    def __init__(self, items: list[StoreItem], offset: int = 0):
        """Document holding up to 36 price tags in each page"""
        self.items = items
        self.items_on_document = 0
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
        cur_row = self.items_on_document // 4
        cur_column = self.items_on_document % 4

        cur_pos_x = 34 + (cur_column * TAG_WIDTH)
        cur_pos_y = 54 + (cur_row * TAG_HEIGHT)

        if cur_column != 0:
            cur_pos_x += (cur_column * CROSS_GAP) 
        if cur_row >= 5:
            cur_pos_y += (CROSS_GAP) 
        
        document.paste(price_tag_img, (cur_pos_x, cur_pos_y))
        
        # Increment item count
        self.items_on_document += 1
        return

    def place_blank_item(self):
        self.items_on_document += 1
        return

    def view_document(self):
        """View the document"""
        self.image.show()

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
        self.pages[0].view_document()
        
    def save_document(self, path) -> None:
        """Print the pdf document containing all pages"""
        if len(self.pages) > 1:
            self.pages[0].image.save(path, save_all=True, append_images=[page.image for page in self.pages[1:]])
        else:
            self.pages[0].image.save(path)
        return

if __name__ == "__main__":
    pass
    """milk = StoreItem("abc123", "Horizon", "Milk", 2.99, "1 Gallon")
    bread = StoreItem("abc123", "Wonder Bread", "1 Loaf Bread", 1.50, "1 Loaf")
    apples = StoreItem("abc123", "apple tree", "1 mf apple", 90.50, "1 apple")
    sausage = StoreItem("abc123", "pig farm", "sausage", 3.50, "5 sausages")
    cereal = StoreItem("abc123", "corn", "frosted flakes", 3.00, "1 box")
    example = StoreItem("abc123", "EXAMPLE BRAND", "EXAMPLE ITEM NAME", 50.00, "1 UNIT")

    items = [milk, bread, apples, sausage, cereal]
    for i in range(31):
        items.append(example)

    test_doc = PriceTagDocument(items)

    test_doc.assemble_page()
    test_doc.view_document()"""

