import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
import datetime as dt

class DoctorPrescriptions(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Doctor Prescriptions"
        
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
            text="Your Prescribed Medications", 
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
        columns = ("ID", "Drug", "Patient", "Diagnosis ID", "Dosage", "Status")
        self.tree = ttk.Treeview(frame, columns=columns, show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)

        # Configure columns width and alignment
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Drug", width=150, anchor="w")
        self.tree.column("Patient", width=150, anchor="w")
        self.tree.column("Diagnosis ID", width=100, anchor="center")
        self.tree.column("Dosage", width=200, anchor="w")
        self.tree.column("Status", width=100, anchor="center")

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
            command=lambda: self.controller.show_frame("DoctorMainScreen"),
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
            width=140,
            height=40,
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        self.view_button.pack(side=tk.LEFT, padx=5)
        
        self.change_status_button = ctk.CTkButton(
            action_buttons, 
            text="Change Status", 
            command=self.change_prescription_status,
            width=140,
            height=40,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        self.change_status_button.pack(side=tk.LEFT, padx=5)

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

    def update_heading_arrow(self, col):
        """Update the heading with an arrow indicating the sort direction"""
        # Remove existing arrows from all columns
        for column in self.tree["columns"]:
            text = self.tree.heading(column)["text"]
            text = text.replace(" ↑", "").replace(" ↓", "")
            self.tree.heading(column, text=text)
        
        # Add arrow to current column
        arrow = " ↑" if not self.sort_order[col] else " ↓"
        current_text = self.tree.heading(col)["text"]
        self.tree.heading(col, text=f"{current_text}{arrow}")

    def on_prescription_select(self, event):
        """Handle prescription selection event"""
        # Check if any item is selected
        selected = self.tree.selection()
        if not selected:
            self.view_button.configure(state="disabled")
            self.change_status_button.configure(state="disabled")
        else:
            self.view_button.configure(state="normal")
            self.change_status_button.configure(state="normal")

    def view_prescription_details(self):
        """Display detailed information about the selected prescription"""
        selected = self.tree.selection()
        if not selected:
            return
            
        # Get prescription ID
        prescription_id = self.tree.item(selected[0], 'values')[0]
        
        try:
            # Get prescription object from hospital data
            prescription = self.controller.hospital.prescriptions.get(int(prescription_id))
            if prescription:
                # Store selected prescription in controller and navigate to details page
                self.controller.selected_prescription = prescription
                self.controller.show_frame("PrescriptionDetails")
            else:
                messagebox.showinfo("Not Found", "Prescription details not found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def change_prescription_status(self):
        """Change the status of the selected prescription (Active/Inactive)"""
        selected = self.tree.selection()
        if not selected:
            return
            
        # Get prescription ID and current status
        values = self.tree.item(selected[0], 'values')
        prescription_id = values[0]
        current_status = values[5]
        
        try:
            # Toggle status
            new_status = "Inactive" if current_status == "Active" else "Active"
            
            # Confirm action
            confirm = messagebox.askyesno(
                "Confirm Status Change", 
                f"Change prescription #{prescription_id} status from {current_status} to {new_status}?"
            )
            
            if confirm:
                # Update prescription status
                prescription = self.controller.hospital.prescriptions.get(int(prescription_id))
                if prescription:
                    # Use autocomplete method to make inactive or set status directly if needed
                    if new_status == "Inactive":
                        prescription.autocomplete()
                    else:
                        # This might need different implementation if reactivation isn't supported
                        pass
                        
                    # Refresh the prescription list
                    self.load_prescriptions()
                    messagebox.showinfo("Success", f"Prescription status changed to {new_status}.")
                else:
                    messagebox.showerror("Error", "Prescription not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to change prescription status: {str(e)}")

    def get_patient_name(self, patient_id):
        """Get patient name from ID"""
        try:
            patient = self.controller.hospital.patients.get(patient_id)
            if patient:
                name = patient.get_protected_attribute("name")
                surname = patient.get_protected_attribute("surname")
                return f"{name} {surname}"
            return "Unknown Patient"
        except Exception:
            return "Unknown Patient"
            
    def get_drug_name(self, drug_id):
        """Get drug name from ID"""
        try:
            drug = self.controller.hospital.drugs.get(drug_id)
            if drug:
                return drug.get("name")
            return f"Drug #{drug_id}"
        except Exception:
            return f"Drug #{drug_id}"

    def load_prescriptions(self):
        """Load prescriptions from the database for the current doctor"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        doctor = self.controller.current_user_data
        
        try:
            prescriptions_ids = doctor.get_protected_attribute("prescriptions", [])
            
            if not prescriptions_ids or len(prescriptions_ids) == 0:
                self.tree.insert("", "end", values=("N/A", "No prescriptions found", "", "", "", ""))
                return
                
            for prescription_id in prescriptions_ids:
                if not isinstance(prescription_id, int):
                    continue
                    
                prescription = self.controller.hospital.prescriptions.get(prescription_id)
                if prescription:
                    drug_name = self.get_drug_name(prescription.get("drug_id"))
                    patient_name = self.get_patient_name(prescription.get("patient_hid"))
                    
                    self.tree.insert("", "end", values=(
                        prescription.get("prescription_id"),
                        drug_name,
                        patient_name,
                        prescription.get("diagnosis_id"),
                        prescription.get("dosage"),
                        prescription.get("status")
                    ))
        except Exception as e:
            print(f"Error loading prescriptions: {e}")
            messagebox.showerror("Error", "An error occurred while loading prescriptions.")

    def tkraise(self, *args, **kwargs):
        """Override tkraise to refresh data when frame is shown"""
        super().tkraise(*args, **kwargs)
        self.load_prescriptions()
        # Reset button states
        self.view_button.configure(state="disabled")
        self.change_status_button.configure(state="disabled")