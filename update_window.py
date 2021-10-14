from tkinter import Label, Entry, Button, LabelFrame, Toplevel, messagebox


class ItemUpdateWindow(Toplevel):
    def __init__(self, parent_tree, row_selected):
        self.parent_tree = parent_tree
        self.row_selected = row_selected
        self.index_of_row_selected = self.parent_tree.index(self.row_selected)
        self.row_values = self.parent_tree.item(row_selected, 'values')

        self.item_update_window = Toplevel()
        self.item_update_window.title("Update Item")
        self.item_update_window.grab_set()
        self.item_update_attributes = ['Brand Name', 'Item Name', 'Unit Size', 'Packaging Size', 'Price']
        self.item_update_entries = {}
        item_update_wrapper = LabelFrame(self.item_update_window, text="Item Details")
        item_update_wrapper.grid(row=0, column=0, sticky='nesw', padx=5, pady=5)

        for i, input_name in enumerate(self.item_update_attributes):
            Label(item_update_wrapper, text=input_name + ":", anchor='w', width=13).grid(row=i, column=0)
            self.item_update_entries[input_name] = Entry(item_update_wrapper)
            self.item_update_entries[input_name].insert(0, self.row_values[i])
            self.item_update_entries[input_name].grid(row=i, column=1, columnspan=2)

        # Buttons
        self.update_item_button = Button(item_update_wrapper, text="Update Item", command=self.update_item)
        self.update_item_button.grid(sticky='s', row=len(self.item_update_entries)+1, column=2, pady=10)

        self.clear_item_update_button = Button(item_update_wrapper, text="Clear", command=self.clear_item_update_inputs)
        self.clear_item_update_button.grid(sticky='s', row=len(self.item_update_entries)+1, column=0, pady=10)

        self.cancel_update_button = Button(item_update_wrapper, text="Cancel", command=self.close_window)
        self.cancel_update_button.grid(sticky='s', row=len(self.item_update_entries)+1, column=1, pady=10)


    def update_item(self):
        """Update record in the tree view."""
        updated_values = []
        for entry in self.item_update_entries.values():
            updated_values.append(entry.get().strip())
        if any(updated_values):
            self.parent_tree.delete(self.row_selected)
            self.parent_tree.insert(parent="", index=self.index_of_row_selected, values=updated_values)
            self.close_window()
        else:
            messagebox.showwarning("Warning", "Cannot create an empty item.")
        return

    def clear_item_update_inputs(self):
        """Clear all entry fields"""
        for entry in self.item_update_entries.values():
            entry.delete(0, 'end')
        return

    def close_window(self):
        """Exit out of update item window"""
        self.item_update_window.destroy()
        return
