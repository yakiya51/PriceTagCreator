from tkinter import Frame, ttk, Scrollbar, filedialog
from tkinter.messagebox import askyesno
import tkinter as tk
# Local Imports
from update_window import *
from price_tags_assembler.document_assembler import PriceTagDocument
from price_tags_assembler.store_item import StoreItem
from gui_config import *

"""
todo
  - Get new/updated items
  - Validate date inputs
"""

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
        self.get_new_items = Button(get_items_wrapper, text="Get Items", command=self.get_new_updated_rows)
        self.get_new_items.grid(row=2, column=1, pady=10, columnspan=10)

        self.clear_dates = Button(get_items_wrapper, text="Clear", command=self.clear_search_dates)
        self.clear_dates.grid(row=2, column=0, pady=10)

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

        # Tree View ---------------------------------------------
        item_list_wrapper = LabelFrame(self.frame, text="Items")
        item_list_wrapper.grid(sticky='nsew', row=0, column=1, rowspan=100)
        # Scroll bar
        self.tree_scroll = Scrollbar(item_list_wrapper)
        self.tree_scroll.grid(row=0, column=4, sticky='ns')
        tree_columns = ("#1", "#2", "#3", "#4", "#5")
        self.tree_column_names = ('Brand Name', 'Item Name', 'Unit Size', 'Packaging Size', 'Price')
        self.tree = ttk.Treeview(item_list_wrapper, columns=tree_columns, show='headings', yscrollcommand=self.tree_scroll.set)
        self.tree_scroll.config(command=self.tree.yview)

        # Tree Columns
        for i in range(len(tree_columns)):
            self.tree.heading(f"#{i+1}", text=self.tree_column_names[i])
            self.tree.column(f"#{i+1}", minwidth=0, width=120, stretch=True)
        self.tree.grid(sticky='nesw', row=0, column=0, columnspan=3)
        # Buttons
        self.remove_items = Button(item_list_wrapper, text="Remove Selected", command=self.remove_rows, background=RED)
        self.remove_items.grid(row=1, column=0, pady=10)
        self.update_item = Button(item_list_wrapper, text="Update Selected", command=self.update_row)
        self.update_item.grid(row=1, column=1, pady=10)
        self.remove_all_items = Button(item_list_wrapper, text="Remove All", command=self.remove_all_rows, background=RED)
        self.remove_all_items.grid(row=2, column=0, pady=10)
        self.undo_remove = Button(item_list_wrapper, text="Undo Remove", command=self.restore_rows)
        self.undo_remove.grid(row=2, column=1, pady=10)        
        self.preview_price_tags_button = Button(item_list_wrapper, text="Preview Price Tags", command=lambda: self.create_price_tags(preview=True), background=BLUE)
        self.preview_price_tags_button.grid(row=1, column=2, pady=10)      
        self.create_price_tags_button = Button(item_list_wrapper, text="Save Price Tags", command=self.create_price_tags, background=GREEN)
        self.create_price_tags_button.grid(row=2, column=2, pady=10)       


    def set_options(self):
        """Configuring default options"""
        self.root.option_add("*Font", "Calibri 13")
        #self.root.option_add("*Background", "white")
        self.root.option_add("*Button.Relief", "groove")
        return

    # Get Items methods
    def clear_search_dates(self):
        """Clear user date inputs."""
        self.start_day.delete(0, 'end')
        self.start_month.delete(0, 'end')
        self.start_year.delete(0, 'end')
        self.end_day.delete(0, 'end')
        self.end_month.delete(0, 'end')
        self.end_year.delete(0, 'end')
        return

    def get_new_updated_rows(self):
        """
        Query new/updated records within the user-specified 
        date range and display the queried rows onto the tree view.
        """
        start_date = f"{self.start_day.get()} / {self.start_month.get()} / {self.start_year.get()}"
        end_date = f"{self.end_day.get()} / {self.end_month.get()} / {self.end_year.get()}"
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
    def update_row(self):
        selected = self.tree.selection()
        if selected:
            if len(selected) > 1:
                messagebox.showwarning("You can only update one row at a time.")
            else:
                self.item_update_window = ItemUpdateWindow(self.tree, selected[0])
        else:
            messagebox.showwarning("Warning", "Please select atleast 1 item from the list to update.")
        return

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
        if self.tree.get_children():
            confirmation = askyesno(title='Confirmation', message='Are you sure you want to remove all items?')
            if confirmation:
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
        return
    
    def restore_rows(self):
        """Restores removed rows from trashcan."""
        if self.rows_trashcan:
            for row in self.rows_trashcan:
                previous_index = int(row['index'].replace('I', ''))-1
                self.tree.insert(parent="", index=previous_index, values=row['values'])
        self.rows_trashcan = []
        return    

    def get_row_count(self):
        """Get the row count of the tree."""
        return len(self.tree.get_children())
    
    # Price Tag Making Methods
    def create_price_tags(self, preview=False):
        """Generate price tags for the items in the tree."""
        if self.tree.get_children():
            item_list = []
            for row in self.tree.get_children():
                row_values = self.tree.item(row)['values']
                print(row_values)
                # Price is stored in index 4
                item_list.append(StoreItem(row_values[0], row_values[1], str(row_values[4]), row_values[2], row_values[3]))
            price_tag_doc = PriceTagDocument(item_list)
            price_tag_doc.assemble_document()
            if preview:
                price_tag_doc.view_document()
            else:
                file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=(("PNG File", "*.png"),("All Files", "*.*") ))
                price_tag_doc.save_document(file_path)
        else:
            messagebox.showwarning("Warning", "There are no items in the list.")
        return


if __name__ == "__main__":
    root = tk.Tk()
    MainFrame(root)
    root.mainloop()
