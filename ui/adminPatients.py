import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk

class AdminPatients(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Admin Patients"

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
            text="Patients Management", 
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
        columns = ("Personal ID", "Hospital ID", "Name", "Surname", "Status", "Weight", "Height")
        self.tree = ttk.Treeview(frame, columns=columns, show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)

        # Columns width and alignment
        self.tree.column("Personal ID", width=100, anchor="center")
        self.tree.column("Hospital ID", width=100, anchor="center")
        self.tree.column("Name", width=150, anchor="w")
        self.tree.column("Surname", width=150, anchor="w")
        self.tree.column("Status", width=120, anchor="center")
        self.tree.column("Weight", width=80, anchor="center")
        self.tree.column("Height", width=80, anchor="center")

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
        
        # Delete button (right side)
        self.delete_button = ctk.CTkButton(
            button_frame, 
            text="Delete Patient", 
            command=self.delete_patient,
            width=150,
            height=40,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        self.delete_button.pack(side=tk.RIGHT, padx=10)

    def sort_treeview(self, col): 
        # Get all items and their current values in the selected column
        items = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]
        
        # Determine sorting key based on column type
        if col in ["Personal ID", "Hospital ID", "Weight", "Height"]:
            # Numeric sorting with N/A handling
            def numeric_sort_key(x):
                if x[0] == "N/A":
                    return -999999 if self.sort_order[col] else 999999
                try:
                    return float(x[0])
                except ValueError:
                    return 0
            items.sort(key=numeric_sort_key, reverse=self.sort_order[col])
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

    def load_patients(self):
        """Load all patients in the system."""
        self.tree.delete(*self.tree.get_children(''))
        
        # Get all patients from the hospital
        patients = self.controller.hospital.patients if hasattr(self.controller.hospital, "patients") else {}
        
        if not patients:
            messagebox.showinfo("No Patients", "There are no patients in the system.")
            return
            
        for patient in patients.values():
            try:
                personal_id = patient.get_protected_attribute("personal_id")
                hospital_id = patient.get_protected_attribute("hospital_id")
                name = patient.get_protected_attribute("name")
                surname = patient.get_protected_attribute("surname")
                status = patient.get("status")
                weight = patient.get("weight")
                height = patient.get("height")
                
                self.tree.insert("", "end", values=(
                    personal_id, 
                    hospital_id, 
                    name, 
                    surname, 
                    status, 
                    weight, 
                    height, 
                ))
            except Exception as e:
                # Skip patients that cause errors
                print(f"Exception loading patient: {e}")
                continue

    def selected(self, event=None):
        """
        Handle selection events for the treeview.
        """
        _ = event  # To avoid the unused variable warning

    def delete_patient(self):
        """
        Delete the selected patient.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a patient to delete.")
            return
            
        patient_values = self.tree.item(selected_item[0], "values")
        try:
            hospital_id = int(patient_values[1])
            
            # Confirm deletion
            confirm = messagebox.askyesno(
                "Confirm Deletion", 
                f"Are you sure you want to delete patient {patient_values[2]} {patient_values[3]} (Hospital ID: {hospital_id})?"
            )
            
            if confirm:
                # Delete the patient
                try:
                    self.controller.hospital.remove_patient(hospital_id)
                    messagebox.showinfo("Success", f"Patient {patient_values[2]} {patient_values[3]} has been deleted.")
                    self.load_patients()  # Refresh the list
                except ValueError as e:
                    messagebox.showerror("Error", f"Failed to delete patient: {e}")
        except ValueError as e:
            messagebox.showerror("Error", f"Failed to delete patient: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.load_patients()