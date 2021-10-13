from store_item import *
from datetime import date


class PriceTagDocument:
    def __init__(self, items: list[StoreItem]):
        """Document holding up to 36 price tags"""
        self.items = items
        self.items_on_document = 0

    def create_document(self):
        """Create a page in the price tag document"""
        self.image = Image.new('RGBA', (DOCUMENT_WIDTH, DOCUMENT_HEIGHT), 'white')
        for item in self.items:
            self.place_price_tag(self.image, item)
        return

    def place_price_tag(self, document: Image, item: StoreItem):
        """Places a price tag image onto the price tag document"""
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
        self.items_on_document += 1
        return

    def view_document(self):
        """View the document"""
        self.image.show()
        
    def save_document(self) -> None:
        """Print the document"""
        today = str(date.today()).replace('-', '_')
        file_name = f"{today}_Price_Tags.png"
        self.image.save(f'Documents/{file_name}')
        return


milk = StoreItem("abc123", "Horizon", "Milk", 2.99, "1 Gallon")
bread = StoreItem("abc123", "Wonder Bread", "1 Loaf Bread", 1.50, "1 Loaf")
apples = StoreItem("abc123", "apple tree", "1 mf apple", 90.50, "1 apple")
sausage = StoreItem("abc123", "pig farm", "sausage", 3.50, "5 sausages")
cereal = StoreItem("abc123", "corn", "frosted flakes", 3.00, "1 box")
example = StoreItem("abc123", "EXAMPLE BRAND", "EXAMPLE ITEM NAME", 50.00, "1 UNIT")

items = [milk, bread, apples, sausage, cereal]
for i in range(31):
    items.append(example)

test_doc = PriceTagDocument(items)

test_doc.create_document()
test_doc.save_document()

