import tkinter as tk 
import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk

class DoctorConsultation(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Doctor Consultation"

        # Main frame layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Title row
        self.grid_rowconfigure(1, weight=1)  # Treeview row
        self.grid_rowconfigure(2, weight=0)  # Buttons row

        # Title label
        self.title_label = ctk.CTkLabel(self, text="Upcoming Appointments", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="ew")

        # Frame for treeview with scrollbar
        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        # Create scrollbar
        scrollbar = ttk.Scrollbar(self.tree_frame)
        scrollbar.pack(side="right", fill="y")

        # Configure style for treeview
        style = ttk.Style()
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b")
        style.map('Treeview', background=[('selected', 'grey30')])

        # Create treeview
        columns = ("ID", "Date", "Time", "Patient", "Room", "Status")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)

        # Configure column headings
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c))
            self.tree.column(col, width=100, anchor="center")

        self.tree.pack(expand=True, fill='both')

        # Initialize sort order tracking
        self.sort_order = {col: False for col in columns}  # False = Ascending, True = Descending

        # Event binding
        self.tree.bind("<<TreeviewSelect>>", self.selected)

        # Buttons frame
        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="ew")

        # Back button
        self.back_button = ctk.CTkButton(self.buttons_frame, text="Back", command=lambda: self.controller.show_frame("DoctorDashboard"))
        self.back_button.pack(side="left", padx=20, pady=10)

        # Start consultation button
        self.consult_button = ctk.CTkButton(self.buttons_frame, text="Start Consultation", command=self.start_consultation)
        self.consult_button.pack(side="right", padx=20, pady=10)

    def selected(self, event=None):
        """Handle selection event"""
        selected_items = self.tree.selection()
        if not selected_items:
            return
        
        # Enable/disable start consultation button based on selection
        self.consult_button.configure(state="normal" if selected_items else "disabled")

    def start_consultation(self):
        """Start a consultation with the selected patient"""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("Selection Required", "Please select an appointment to start consultation.")
            return
            
        # Get the appointment ID from the selected item
        appointment_id = self.tree.item(selected_items[0], "values")[0]
        
        # Store the selected appointment ID for use in the consultation frame
        self.controller.selected_appointment_id = appointment_id
        
        # Navigate to the consultation create frame
        self.controller.show_frame("DoctorConsultationCreate")

    def sort_treeview(self, col):
        """Sort treeview by the selected column"""
        # Toggle sort order for clicked column
        self.sort_order[col] = not self.sort_order[col]
        
        # Get all items with their values
        items = [(self.tree.item(item, "values"), item) for item in self.tree.get_children("")]
        
        # Determine column index
        columns = ("ID", "Date", "Time", "Patient", "Room", "Status")
        col_idx = columns.index(col)
        
        # Sort items based on column and order
        items.sort(key=lambda x: x[0][col_idx], reverse=self.sort_order[col])
        
        # Rearrange items in the sorted order
        for idx, (_, item) in enumerate(items):
            self.tree.move(item, "", idx)
        
        # Update heading to show sort direction
        self.update_heading_arrow(col)

    def update_heading_arrow(self, sort_col):
        """Update column headings to show sort direction"""
        columns = ("ID", "Date", "Time", "Patient", "Room", "Status")
        for col in columns:
            text = col
            if col == sort_col:
                text = f"{col} {'   ˄' if self.sort_order[col] else '  ˅'}"
            self.tree.heading(col, text=text)

    def process_time_tuples(self, time):
        """Convert a tuple of time strings to a single string."""
        if isinstance(time, str) and time.startswith("(") and time.endswith(")"):
            try:
                # Extract times from the tuple string format
                time_str = time.strip("()").replace("'", "")
                start_time, end_time = time_str.split(", ")
                return f"{start_time} - {end_time}"
            except:
                return time
        return time

    def load_appointments(self):
        """Load the appointments from the controller's doctor data."""
        self.tree.delete(*self.tree.get_children(''))
        doctor_data = self.controller.current_user_data
        
        if not doctor_data:
            messagebox.showinfo("No Data", "Doctor data not found.")
            return
            
        appointments = doctor_data.get_protected_attribute("appointments")
        
        if not appointments or appointments == "[]" or appointments is None:
            messagebox.showinfo("No Appointments", "You have no appointments scheduled.")
            return
            
        for appointment_id in appointments:
            if not isinstance(appointment_id, int):
                if isinstance(appointment_id, list) and len(appointment_id) == 1:
                    appointment_id = appointment_id[0]
                else:
                    continue
                    
            try:
                appointment = self.controller.hospital.appointments.get(appointment_id)
                
                # Skip appointments that aren't scheduled
                if appointment.get("status") != "Scheduled":
                    continue
                    
                appt_id = appointment.get("appointment_id")
                date = appointment.get("date") if appointment.get("date") else "N/A"
                time = self.process_time_tuples(appointment.get("timeframe"))
                patient_id = appointment.get("patient_hid")
                room = appointment.get("room_number")
                status = appointment.get("status")
                
                self.tree.insert("", "end", values=(appt_id, date, time, patient_id, room, status))
            except Exception as exc:
                messagebox.showerror("Error", str(exc))

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.load_appointments()
        self.consult_button.configure(state="disabled")