import csv


"""
Cleaning Steps:
 - Import CSV
 - Delete contents in column D through G
 - Remove blank rows
 - Remove irrelevat rows
    - Title
    - Column names
    - Category names
    - If row doesn't have price it is irrelevant
 - Strip/Upper each item name & size
 - Try and extract the unit/packaging size
 - Save as csv
"""

def get_unit_or_packaging_size(item_name):
    pass



def remove_blank_rows(file):
    pass


if __name__ == "__main__":
    with open('price_list.csv', 'r') as csv_file:
        price_list = csv.reader(csv_file)
        for row in price_list:
            print(row)
    

