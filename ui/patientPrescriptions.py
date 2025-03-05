import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
import datetime as dt

class PatientPrescriptions(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Patient Prescriptions"
        
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
            text="Your Prescriptions", 
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
        
        # Define tag styles
        style.map('Treeview', background=[('selected', '#4a6984')])
        
        # Treeview setup
        columns = ("ID", "Drug ID", "Doctor", "Diagnosis ID", "Dosage Instructions", "Status")
        self.tree = ttk.Treeview(frame, columns=columns, show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)

        # Configure columns width and alignment
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Drug ID", width=100, anchor="center")
        self.tree.column("Doctor", width=150, anchor="center")
        self.tree.column("Diagnosis ID", width=180, anchor="w")
        self.tree.column("Dosage Instructions", width=250, anchor="w")
        self.tree.column("Status", width=120, anchor="center")

        # Configure headings with sort commands
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c))
            
        self.tree.pack(expand=True, fill="both")
        
        # Store sort order state
        self.sort_order = {col: False for col in columns}
        
        # Event bindings
        self.tree.bind("<<TreeviewSelect>>", self.on_prescription_select)
        self.tree.bind('<Button-1>', self.block_column_resize)

        # Button frame
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="ew")
        
        # Back button (left side)
        self.back_button = ctk.CTkButton(
            button_frame, 
            text="Go Back", 
            command=lambda: self.controller.show_frame("PatientMainScreen"),
            width=150,
            height=40,
            fg_color="#555555",
            hover_color="#666666"
        )
        self.back_button.pack(side=tk.LEFT, padx=10)
        
        # Action buttons (right side)
        action_buttons = ctk.CTkFrame(button_frame, fg_color="transparent")
        action_buttons.pack(side=tk.RIGHT)
        
        self.view_button = ctk.CTkButton(
            action_buttons, 
            text="View Details", 
            command=self.view_prescription_details,
            width=180,
            height=40,
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        self.view_button.pack(side=tk.LEFT, padx=10)

    def block_column_resize(self, event):
        if self.tree.identify_region(event.x, event.y) == "separator":
            return "break"

    def sort_treeview(self, col):
        """Sort treeview by column"""
        # Toggle sort order
        self.sort_order[col] = not self.sort_order[col]
        
        # Get all items with their values
        items = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]
        
        # Sort items
        items.sort(reverse=self.sort_order[col])
        
        # Rearrange items in the tree
        for index, (_, item) in enumerate(items):
            self.tree.move(item, '', index)
            
        # Update arrow indicators
        self.update_heading_arrow(col)

    def update_heading_arrow(self, sort_col):
        for col in self.tree["columns"]:
            arrow = " ↑" if col == sort_col and not self.sort_order[col] else " ↓" if col == sort_col else ""
            self.tree.heading(col, text=f"{col}{arrow}")

    def on_prescription_select(self, event):
        """Handle prescription selection event"""
        # Check if any item is selected
        selected = self.tree.selection()
        if not selected:
            self.view_button.configure(state="disabled")
        else:
            self.view_button.configure(state="normal")

    def view_prescription_details(self):
        """Display detailed information about the selected prescription"""
        selected = self.tree.selection()
        if not selected:
            return
            
        # Get prescription ID
        prescription_id = self.tree.item(selected[0], 'values')[0]
        
        # In a real implementation, you would fetch the prescription details from your data model
        # For now, we'll just show a message box with the ID
        messagebox.showinfo(
            "Prescription Details", 
            f"Viewing detailed information for prescription #{prescription_id}\n\nThis feature will be implemented soon."
        )

    def load_prescriptions(self):
        """Load prescriptions from the database for the current patient"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        patient = self.controller.current_user_data
        
        try:
            prescriptions_ids = patient.get("prescriptions", [])
            for prescription_id in prescriptions_ids:
                prescription = self.controller.hospital.prescriptions.get(prescription_id)
                if prescription:
                    print(prescription)
                    self.tree.insert("", "end", values=(
                        prescription.get("prescription_id"),
                        prescription.get("drug_id"),
                        prescription.get("doctor_hid"),
                        prescription.get("diagnosis_id"),
                        prescription.get("dosage_instructions"),
                        prescription.get("status")
                    ))
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "An error occurred while loading prescriptions.")
        

    def tkraise(self, *args, **kwargs):
        """Override tkraise to refresh data when frame is shown"""
        super().tkraise(*args, **kwargs)
        self.load_prescriptions()