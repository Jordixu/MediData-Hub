import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk

class AdminDrugs(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Admin Drugs"

        # Configure the main layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Treeview
        self.grid_rowconfigure(2, weight=0)  # Buttons
        
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(20, 10))
        
        header_label = ctk.CTkLabel(
            header_frame, 
            text="Drugs Management", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        header_label.pack(pady=10)

        # Treeview Frame
        frame = ctk.CTkFrame(self)
        frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        # Treeview Style
        style = ttk.Style()
        style.configure('Treeview', rowheight=30, font=('Helvetica', 12))
        style.configure('Treeview.Heading', font=('Helvetica', 13, 'bold'))
        style.map('Treeview', background=[('selected', '#4a6984')])

        # Treeview setup
        columns = ("Drug ID", "Name", "Commercial Name", "Price", "Company", "Requires Prescription")
        self.tree = ttk.Treeview(frame, columns=columns, show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)

        # Columns width and alignment
        self.tree.column("Drug ID", width=70, anchor="center")
        self.tree.column("Name", width=150, anchor="w")
        self.tree.column("Commercial Name", width=180, anchor="w")
        self.tree.column("Price", width=80, anchor="center")
        self.tree.column("Company", width=150, anchor="center")
        self.tree.column("Requires Prescription", width=150, anchor="center")

        # Configure headings with sort commands
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c))
        
        self.tree.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Disable column resizing
        def block_column_resize(event):
            if self.tree.identify_region(event.x, event.y) == "separator":
                return "break"

        self.tree.bind('<Button-1>', block_column_resize)

        # Initialize sort order tracking
        self.sort_order = {col: False for col in columns}  # False = Ascending, True = Descending

        # Event binding for selection
        self.tree.bind("<<TreeviewSelect>>", self.selected)

        # Action buttons frame
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="ew")
        
        # Back button (left side)
        self.back_button = ctk.CTkButton(
            button_frame, 
            text="Go Back", 
            command=lambda: self.controller.show_frame("AdminMainScreen"),
            width=150,
            height=40,
            fg_color="#555555",
            hover_color="#666666"
        )
        self.back_button.pack(side=tk.LEFT, padx=10)
        
        # Action buttons (right side)
        action_buttons = ctk.CTkFrame(button_frame, fg_color="transparent")
        action_buttons.pack(side=tk.RIGHT)
        
        self.add_button = ctk.CTkButton(
            action_buttons, 
            text="Add Drug", 
            command=self.add_drug,
            width=150,
            height=40,
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        self.add_button.pack(side=tk.LEFT, padx=10)
        
        self.modify_button = ctk.CTkButton(
            action_buttons, 
            text="Modify Drug", 
            command=self.modify_drug,
            width=150,
            height=40,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        self.modify_button.pack(side=tk.LEFT, padx=10)

        self.delete_button = ctk.CTkButton(
            action_buttons, 
            text="Delete Drug", 
            command=self.delete_drug,
            width=150,
            height=40,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        self.delete_button.pack(side=tk.LEFT, padx=10)

    def sort_treeview(self, col): 
        # Get all items and their current values in the selected column
        items = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]
        
        # Determine sorting key based on column type
        if col in ["Drug ID", "Price"]:
            # Numeric sorting with N/A handling
            def num_sort_key(x):
                if x[0] == "N/A":
                    return -999999 if self.sort_order[col] else 999999
                try:
                    return float(x[0])
                except ValueError:
                    return 0
            items.sort(key=num_sort_key, reverse=self.sort_order[col])
        elif col == "Requires Prescription":
            # Boolean sorting
            items.sort(key=lambda x: x[0] == "Yes", reverse=self.sort_order[col])
        else:
            # Default string sorting for other columns
            items.sort(key=lambda x: str(x[0]).lower(), reverse=self.sort_order[col])
        
        # Rearrange items in Treeview
        for index, (value, item) in enumerate(items):
            self.tree.move(item, '', index)
        
        # Toggle sort order and update heading
        self.sort_order[col] = not self.sort_order[col]
        self.update_heading_arrow(col)

    def update_heading_arrow(self, col):
        # Remove existing arrows from all columns
        for column in self.tree["columns"]:
            text = self.tree.heading(column)["text"]
            text = text.replace("   ˄", "").replace("   ˅", "")
            self.tree.heading(column, text=text)
        
        # Add arrow to current column
        arrow = "   ˅" if self.sort_order[col] else "   ˄"
        current_text = self.tree.heading(col)["text"]
        self.tree.heading(col, text=current_text + arrow)

    def load_drugs(self):
        """Load all drugs in the system."""
        self.tree.delete(*self.tree.get_children(''))
        
        # Get all drugs from the hospital
        drugs = self.controller.hospital.drugs if hasattr(self.controller.hospital, "drugs") else {}
        
        if not drugs:
            messagebox.showinfo("No Drugs", "There are no drugs in the system.")
            return
            
        for drug in drugs.values():
            try:
                drug_id = drug.get("drug_id")
                name = drug.get("name")
                commercial_name = drug.get("commercial_name")
                price = drug.get("price")
                company = drug.get("company") if drug.get("company") else "N/A"
                prescription = "Yes" if drug.get("prescription") else "No"
                
                self.tree.insert("", "end", values=(drug_id, name, commercial_name, price, company, prescription))
            except Exception as e:
                # Skip drugs that cause errors
                print(f"Exception loading drug {drug_id}: {e}")
                continue

    def selected(self, event=None):
        """
        Handle selection events for the treeview.
        """
        _ = event  # To avoid the unused variable warning

    def add_drug(self):
        """
        Navigate to the drug addition screen.
        """
        self.controller.selected_drug = None  # Clear any selected drug
        self.controller.show_frame("AdminAddDrugs")

    def modify_drug(self):
        """
        Navigate to the drug modification screen.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a drug to modify.")
            return
            
        drug_values = self.tree.item(selected_item[0], "values")
        try:
            drug_id = int(drug_values[0])
            drug = self.controller.hospital.drugs.get(drug_id)
            if drug:
                self.controller.selected_drug = drug
                self.controller.show_frame("AdminModifyDrugs")
            else:
                messagebox.showerror("Error", "Failed to load drug data for modification")
        except ValueError as e:
            messagebox.showerror("Error", f"Failed to load drug data for modification: {e}")

    def delete_drug(self):
        """
        Delete the selected drug.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a drug to delete.")
            return
            
        drug_values = self.tree.item(selected_item[0], "values")
        try:
            drug_id = drug_values[0]
            
            # Confirm deletion
            confirm = messagebox.askyesno(
                "Confirm Deletion", 
                f"Are you sure you want to delete drug {drug_values[1]} ({drug_values[2]})?"
            )
            
            if confirm:
                try:
                    self.controller.hospital.remove_drug(drug_id)
                    messagebox.showinfo("Success", f"Drug '{drug_values[1]}' deleted successfully!")
                    self.load_drugs()
                except ValueError as e:
                    messagebox.showerror("Error", f"Failed to delete drug: {e}")
        except ValueError as e:
            messagebox.showerror("Error", f"Failed to delete drug: {e}")

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.load_drugs()  # Refresh the list whenever the frame is shown