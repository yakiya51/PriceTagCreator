from tkinter import Label, Entry, Button, LabelFrame, Frame, ttk, messagebox
import tkinter as tk
from config import *
from price_tags_assembler.store_item import StoreItem
from price_tags_assembler.document_assembler import PriceTagDocument


class MainFrame:
    def __init__(self, root):
        self.root = root
        self.frame = Frame(root)
        self.frame.grid(sticky='nesw')
        self.root.title("Price Tag Maker")
        self.set_options()
        self.rows_trashcan = []
        # GUI Components

        # Get Updated and New Items ---------------------------------------------
        get_items_wrapper = LabelFrame(self.frame, text="Get New/Updated Items")
        get_items_wrapper.grid(sticky='nesw', row=0, column=0, padx=5)
        # Start date
        Label(get_items_wrapper, text="Start Date: ", anchor='w', width=13).grid(row=0, column=0)
        self.start_month = Entry(get_items_wrapper, width=4, justify='right')
        self.start_month.grid(row=0, column=1)
        Label(get_items_wrapper, text="/").grid(row=0, column=2)
        self.start_day = Entry(get_items_wrapper, width=4, justify='right')
        self.start_day.grid(row=0, column=3)     
        Label(get_items_wrapper, text="/").grid(row=0, column=4)
        self.start_year = Entry(get_items_wrapper, width=6, justify='right')
        self.start_year.grid(row=0, column=5)     
        # End date
        Label(get_items_wrapper, text="End Date: ", anchor='w', width=13).grid(row=1, column=0)
        self.end_month = Entry(get_items_wrapper, width=4, justify='right')
        self.end_month.grid(row=1, column=1)
        Label(get_items_wrapper, text="/").grid(row=1, column=2)
        self.end_day = Entry(get_items_wrapper, width=4, justify='right')
        self.end_day.grid(row=1, column=3)     
        Label(get_items_wrapper, text="/").grid(row=1, column=4)
        self.end_year = Entry(get_items_wrapper, width=6, justify='right')
        self.end_year.grid(row=1, column=5)     
        # Buttons
        self.get_new_items = Button(get_items_wrapper, text="Get Items")
        self.get_new_items.grid(row=2, column=0, pady=10, columnspan=10)
        # Custom Items ---------------------------------------------
        custom_items_wrapper = LabelFrame(self.frame, text="Custom Item")
        custom_items_wrapper.grid(sticky='nesw',row=1, column=0, padx=5)
        self.custom_inputs = ['Brand Name', 'Item Name', 'Unit Size', 'Packaging Size', 'Price']
        self.custom_entries = {}

        for i, input_name in enumerate(self.custom_inputs):
            Label(custom_items_wrapper, text=input_name + ":", anchor='w', width=13).grid(row=i, column=0)
            self.custom_entries[input_name] = Entry(custom_items_wrapper)
            self.custom_entries[input_name].grid(row=i, column=1)
        
        self.add_custom_item_button = Button(custom_items_wrapper, text="Add Item", command=self.add_custom_item)
        self.add_custom_item_button.grid(sticky='s', row=len(self.custom_inputs)+1, column=1, pady=10)
        # Buttons
        self.clear_custom_item_button = Button(custom_items_wrapper, text="Clear", command=self.clear_custom_item_inputs)
        self.clear_custom_item_button.grid(sticky='s', row=len(self.custom_inputs)+1, column=0, pady=10)

        # Item Viewer ---------------------------------------------
        item_list_wrapper = LabelFrame(self.frame, text="Items")
        item_list_wrapper.grid(sticky='nsew', row=0, column=1, rowspan=100)
        tree_columns = ("#1", "#2", "#3", "#4", "#5")
        tree_column_names = ('Brand Name', 'Item Name', 'Unit Size', 'Packaging Size', 'Price')
        self.tree = ttk.Treeview(item_list_wrapper, columns=tree_columns, show='headings')
        # Tree Columns
        for i in range(len(tree_columns)):
            self.tree.heading(f"#{i+1}", text=tree_column_names[i])
            self.tree.column(f"#{i+1}", minwidth=0, width=100, stretch=False)
        self.tree.grid(sticky='nesw', row=0, column=0, columnspan=3)
        # Buttons
        self.remove_items = Button(item_list_wrapper, text="Remove Items", command=self.remove_rows)
        self.remove_items.grid(row=1, column=0, pady=10)
        self.update_item = Button(item_list_wrapper, text="Update Item")
        self.update_item.grid(row=1, column=1, pady=10)
        self.remove_all_items = Button(item_list_wrapper, text="Remove All", command=self.remove_all_rows)
        self.remove_all_items.grid(row=1, column=2, pady=10)
        self.undo_remove = Button(item_list_wrapper, text="Undo Remove", command=self.restore_rows)
        self.undo_remove.grid(row=2, column=0, pady=10)        
        self.create_price_tags_button = Button(item_list_wrapper, text="Create Price Tags", command=self.create_price_tags)
        self.create_price_tags_button.grid(row=2, column=2, pady=10)       

    def set_options(self):
        """Configuring default options"""
        self.root.option_add("*Font", "Calibri 13")
        #self.root.option_add("*Background", "white")
        self.root.option_add("*Button.Relief", "groove")
        return

    # Custom Items Methods
    def add_custom_item(self):
        """Add a custom item row to the tree based on user inputs."""
        input_values = []
        for entry in self.custom_entries.values():
            input_values.append(entry.get().strip())
        # Makes sure input values aren't all empty
        if any(input_values):
            self.tree.insert(parent="", index=self.get_row_count(), values=input_values)
        self.clear_custom_item_inputs()
        return

    def clear_custom_item_inputs(self):
        """Clear entry fields of the custom item creator."""
        for entry in self.custom_entries.values():
            entry.delete(0, 'end')
        return

    # Tree Methods
    def remove_rows(self):
        """Remove a row from the tree."""
        selected = self.tree.selection()
        if selected:
            self.backup_rows(selected)
            for row in selected:
                self.tree.delete(row)
        else:
            messagebox.showwarning(title="Warning", message="Please select atleast 1 item from the list to remove.")       
        return

    def remove_all_rows(self):
        """Remove all rows from the tree."""
        self.backup_rows(self.tree.get_children())
        self.tree.delete(*self.tree.get_children())
        return        

    def backup_rows(self, rows):
        """Saves removed rows into trashcan."""
        if rows:
            self.rows_trashcan = []
            for row in rows:
                row_details = self.tree.item(row)
                del row_details['text']
                del row_details['image']
                del row_details['open']
                del row_details['tags']
                row_details['index'] = row
                self.rows_trashcan.append(row_details)
        print(self.rows_trashcan)
        return
    
    def restore_rows(self):
        """Restores removed rows from trashcan."""
        if self.rows_trashcan:
            for row in self.rows_trashcan:
                previous_index = int(row['index'].replace('I', ''))-1
                self.tree.insert(parent="", index=previous_index, values=row['values'])
        return    

    def get_row_count(self):
        """Get the row count of the tree."""
        return len(self.tree.get_children())

    def create_price_tags(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    MainFrame(root)
    root.mainloop()

