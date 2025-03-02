import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk

class AdminDoctors(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Admin Doctors"

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
            text="Doctors Management", 
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
        columns = ("Personal ID", "Hospital ID", "Name", "Surname", "Specialty", "Department", "Social Security")
        self.tree = ttk.Treeview(frame, columns=columns, show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)

        # Columns width and alignment
        self.tree.column("Personal ID", width=100, anchor="center")
        self.tree.column("Hospital ID", width=100, anchor="center")
        self.tree.column("Name", width=150, anchor="w")
        self.tree.column("Surname", width=150, anchor="w")
        self.tree.column("Specialty", width=150, anchor="center")
        self.tree.column("Department", width=150, anchor="center")
        self.tree.column("Social Security", width=150, anchor="center")

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
            text="Add Doctor", 
            command=self.add_doctor,
            width=150,
            height=40,
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        self.add_button.pack(side=tk.LEFT, padx=10)
        
        self.modify_button = ctk.CTkButton(
            action_buttons, 
            text="Modify Doctor", 
            command=self.modify_doctor,
            width=150,
            height=40,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        self.modify_button.pack(side=tk.LEFT, padx=10)

        self.delete_button = ctk.CTkButton(
            action_buttons, 
            text="Delete Doctor", 
            command=self.delete_doctor,
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
        if col in ["Personal ID", "Hospital ID"]:
            # Integer sorting with N/A handling
            def int_sort_key(x):
                if x[0] == "N/A":
                    return -999999 if self.sort_order[col] else 999999
                try:
                    return int(x[0])
                except ValueError:
                    return 0
            items.sort(key=int_sort_key, reverse=self.sort_order[col])
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

    def load_doctors(self):
        """Load all doctors in the system."""
        self.tree.delete(*self.tree.get_children(''))
        
        # Get all doctors from the hospital
        doctors = self.controller.hospital.doctors if hasattr(self.controller.hospital, "doctors") else {}
        
        if not doctors:
            messagebox.showinfo("No Doctors", "There are no doctors in the system.")
            return
            
        for doctor in doctors.values():
            try:
                personal_id = doctor.get_protected_attribute("personal_id")
                hospital_id = doctor.get_protected_attribute("hospital_id")
                name = doctor.get_protected_attribute("name")
                surname = doctor.get_protected_attribute("surname")
                specialty = doctor.get("speciality") 
                department = doctor.get("department")
                security = doctor.get("socialsecurity")
                
                self.tree.insert("", "end", values=(personal_id, hospital_id, name, surname, specialty, department, security))
            except Exception as e:
                # Skip doctors that cause errors
                print(f"Exception loading doctor {hospital_id}: {e}")
                continue

    def selected(self, event=None):
        """
        Handle selection events for the treeview.
        """
        _ = event  # To avoid the unused variable warning

    def add_doctor(self):
        """
        Navigate to the doctor addition screen.
        """
        self.controller.selected_doctor = None  # Clear any selected doctor
        self.controller.show_frame("AdminAddDoctor")

    def modify_doctor(self):
        """
        Navigate to the doctor modification screen with the selected doctor.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a doctor to modify.")
            return
            
        doctor_values = self.tree.item(selected_item[0], "values")
        try:
            hospital_id = int(doctor_values[1])
            doctor = None
            
            if hasattr(self.controller.hospital, "doctors"):
                doctor = self.controller.hospital.doctors.get(hospital_id)
            
            if doctor:
                self.controller.selected_doctor = doctor
                self.controller.show_frame("AdminModifyDoctor")
            else:
                messagebox.showerror("Error", f"Doctor with Hospital ID {hospital_id} not found.")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid hospital ID: {e}")

    def delete_doctor(self):
        """
        Delete the selected doctor.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a doctor to delete.")
            return
            
        doctor_values = self.tree.item(selected_item[0], "values")
        try:
            hospital_id = int(doctor_values[1])
            
            # Confirm deletion
            confirm = messagebox.askyesno(
                "Confirm Deletion", 
                f"Are you sure you want to delete doctor {doctor_values[2]} {doctor_values[3]} (Hospital ID: {hospital_id})?"
            )
            
            if confirm:
                try:
                    self.controller.hospital.remove_doctor(hospital_id)
                    messagebox.showinfo("Success", f"Doctor {doctor_values[2]} {doctor_values[3]} has been deleted.")
                    self.load_doctors()
                except ValueError as e:
                    messagebox.showerror("Error", f"Failed to delete doctor: {e}")
        except ValueError as e:
            messagebox.showerror("Error", f"Failed to delete doctor: {e}")

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.load_doctors()