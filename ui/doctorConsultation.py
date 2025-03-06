import tkinter as tk 
import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk

class DoctorConsultation(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Doctor Consultation"
        
        # Track active right panel
        self.active_right_panel = "diagnoses"  # or "prescriptions"

        # Configure grid layout with consistent weights
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Headers
        self.grid_rowconfigure(1, weight=1)  # Content
        self.grid_rowconfigure(2, weight=0)  # Bottom buttons

        # Left side header: Upcoming Appointments w/ action button
        left_header_frame = ctk.CTkFrame(self, fg_color="transparent")
        left_header_frame.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="ew")
        
        left_header_frame.columnconfigure(0, weight=1)
        left_header_frame.columnconfigure(1, weight=0)
        
        self.title_label = ctk.CTkLabel(
            left_header_frame, 
            text="Upcoming Appointments", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.grid(row=0, column=0, sticky="w")
        
        # Start Consultation btn
        self.consult_button = ctk.CTkButton(
            left_header_frame,
            text="Start Consultation",
            command=self.start_consultation,
            width=160,
            height=35,
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        self.consult_button.grid(row=0, column=1, padx=(10, 0), sticky="e")

        # Left side content: Appointments table
        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.tree_frame)
        scrollbar.pack(side="right", fill="y")

        style = ttk.Style()
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b")
        style.map('Treeview', background=[('selected', 'grey30')])

        # Adjusted column widths for appointments table
        columns = ("ID", "Date", "Time", "Patient", "Room", "Status")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)

        # Configure column widths based on content importance
        self.tree.column("ID", width=60, anchor="center")
        self.tree.column("Date", width=100, anchor="center")
        self.tree.column("Time", width=120, anchor="center")
        self.tree.column("Patient", width=180, anchor="w")
        self.tree.column("Room", width=80, anchor="center")
        self.tree.column("Status", width=100, anchor="center")
        
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c))

        self.tree.pack(expand=True, fill='both')

        self.sort_order = {col: False for col in columns}
        self.tree.bind("<<TreeviewSelect>>", self.selected)

        # Right side: Header with toggle buttons
        right_header_frame = ctk.CTkFrame(self, fg_color="transparent")
        right_header_frame.grid(row=0, column=1, pady=(20, 10), padx=20, sticky="ew")
        
        right_header_frame.columnconfigure(0, weight=1)
        right_header_frame.columnconfigure(1, weight=1)
        right_header_frame.columnconfigure(2, weight=0)
        
        # Toggle buttons for switching between diagnoses and prescriptions
        self.diagnoses_btn = ctk.CTkButton(
            right_header_frame,
            text="Previous Diagnoses", 
            command=lambda: self.toggle_right_panel("diagnoses"),
            fg_color="#191c4a" if self.active_right_panel == "diagnoses" else "#555555",
            hover_color="#393e80",
            height=35
        )
        self.diagnoses_btn.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        self.prescriptions_btn = ctk.CTkButton(
            right_header_frame,
            text="Your Prescriptions", 
            command=lambda: self.toggle_right_panel("prescriptions"),
            fg_color="#555555" if self.active_right_panel == "diagnoses" else "#191c4a",
            hover_color="#666666",
            height=35
        )
        self.prescriptions_btn.grid(row=0, column=1, padx=(5, 0), sticky="ew")
        
        # View Details button
        self.view_details_button = ctk.CTkButton(
            right_header_frame,
            text="View Details",
            command=self.view_details,
            width=120,
            height=35,
            fg_color="#204a1d",
            hover_color="#548251"
        )
        self.view_details_button.grid(row=0, column=2, padx=(15, 0), sticky="e")

        # Container for right side panels (both diagnoses and prescriptions)
        self.right_panel_container = ctk.CTkFrame(self)
        self.right_panel_container.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")
        
        # Diagnoses panel
        self.diagnoses_frame = ctk.CTkFrame(self.right_panel_container)
        self.diagnoses_frame.pack(fill="both", expand=True)
        
        history_scrollbar = ttk.Scrollbar(self.diagnoses_frame)
        history_scrollbar.pack(side="right", fill="y")

        # Adjusted columns for diagnoses table
        self.history_columns = ("ID", "Date", "Patient", "Title", "Appointment ID")
        self.history_tree = ttk.Treeview(self.diagnoses_frame, columns=self.history_columns, show='headings', yscrollcommand=history_scrollbar.set)
        history_scrollbar.config(command=self.history_tree.yview)

        # Configure column widths for diagnoses
        self.history_tree.column("ID", width=60, anchor="center")
        self.history_tree.column("Date", width=100, anchor="center")
        self.history_tree.column("Patient", width=150, anchor="w")
        self.history_tree.column("Title", width=220, anchor="w")
        self.history_tree.column("Appointment ID", width=110, anchor="center")
        
        for col in self.history_columns:
            self.history_tree.heading(col, text=col, command=lambda c=col: self.sort_history_treeview(c))

        self.history_tree.pack(expand=True, fill='both')
        self.history_sort_order = {col: False for col in self.history_columns}
        self.history_tree.bind("<<TreeviewSelect>>", self.history_selected)
        
        # Prescriptions panel
        self.prescriptions_frame = ctk.CTkFrame(self.right_panel_container)
        # Not packed yet, will be toggled on demandd
        
        prescriptions_scrollbar = ttk.Scrollbar(self.prescriptions_frame)
        prescriptions_scrollbar.pack(side="right", fill="y")
        
        # Adjusted columns for prescriptions table
        self.prescriptions_columns = ("ID", "Drug", "Patient", "Diagnosis ID", "Dosage", "Status")
        self.prescriptions_tree = ttk.Treeview(self.prescriptions_frame, columns=self.prescriptions_columns, 
                                               show='headings', yscrollcommand=prescriptions_scrollbar.set)
        prescriptions_scrollbar.config(command=self.prescriptions_tree.yview)
        
        # Configure column widths for prescriptions
        self.prescriptions_tree.column("ID", width=60, anchor="center")
        self.prescriptions_tree.column("Drug", width=150, anchor="w")
        self.prescriptions_tree.column("Patient", width=150, anchor="w")
        self.prescriptions_tree.column("Diagnosis ID", width=90, anchor="center")
        self.prescriptions_tree.column("Dosage", width=180, anchor="w")
        self.prescriptions_tree.column("Status", width=90, anchor="center")
        
        for col in self.prescriptions_columns:
            self.prescriptions_tree.heading(col, text=col, command=lambda c=col: self.sort_prescriptions_treeview(c))
        
        self.prescriptions_tree.pack(expand=True, fill='both')
        self.prescriptions_sort_order = {col: False for col in self.prescriptions_columns}
        self.prescriptions_tree.bind("<<TreeviewSelect>>", self.prescription_selected)

        # Bottom buttons frame (Back button)
        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=(10, 20), sticky="w")

        # Back button (left side)
        self.back_button = ctk.CTkButton(
            self.buttons_frame, 
            text="Go Back", 
            command=lambda: self.controller.show_frame("DoctorMainScreen"),
            width=150,
            height=40,
            fg_color="#555555",
            hover_color="#666666"
        )
        self.back_button.pack(side="left", pady=10)

    def toggle_right_panel(self, panel_name):
        """Switch between diagnoses and prescriptions panels"""
        if panel_name == self.active_right_panel:
            return
            
        # Update active panel
        self.active_right_panel = panel_name
        
        # Update button colors
        self.diagnoses_btn.configure(fg_color="#191c4a" if panel_name == "diagnoses" else "#555555")
        self.prescriptions_btn.configure(fg_color="#191c4a" if panel_name == "prescriptions" else "#555555")
        
        # Hide all panels
        self.diagnoses_frame.pack_forget()
        self.prescriptions_frame.pack_forget()
        
        # Show active panel
        if panel_name == "diagnoses":
            self.diagnoses_frame.pack(fill="both", expand=True)
            self.view_details_button.configure(text="View Diagnosis Details", command=self.view_diagnosis_details)
        else:
            self.prescriptions_frame.pack(fill="both", expand=True)
            self.view_details_button.configure(text="View Prescription Details", command=self.view_prescription_details)
    
    def selected(self, event=None):
        selected_items = self.tree.selection()
        if not selected_items:
            return
        
    def history_selected(self, event=None):
        selected_items = self.history_tree.selection()
        if not selected_items:
            return
            
    def prescription_selected(self, event=None):
        selected_items = self.prescriptions_tree.selection()
        if not selected_items:
            return

    def view_details(self):
        """Generic view details function that routes to the appropriate view function"""
        if self.active_right_panel == "diagnoses":
            self.view_diagnosis_details()
        else:
            self.view_prescription_details()

    def start_consultation(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("Selection Required", "Please select an appointment to start consultation.")
            return
        
        ans = messagebox.askyesno("Start Consultation", "Are you sure you want to start the consultation? Once started, the appointment either needs to be completed or cancelled.")
        
        if ans:
            appointment_id = int(self.tree.item(selected_items[0], "values")[0])
            
            # print(appointment_id)
            
            self.controller.selected_appointment = self.controller.hospital.appointments.get(appointment_id)
            self.controller.selected_patient = self.controller.hospital.patients.get(self.controller.selected_appointment.get("patient_hid"))
            
            self.controller.show_frame("DoctorConsultationCreate")
    
    def view_diagnosis_details(self):
        selected_items = self.history_tree.selection()
        if not selected_items:
            messagebox.showinfo("Selection Required", "Please select a diagnosis to view details.")
            return
        
        diagnosis_id = int(self.history_tree.item(selected_items[0], "values")[0])
        self.controller.selected_diagnosis = self.controller.hospital.diagnoses.get(diagnosis_id)
        self.controller.show_frame("DiagnosesDetails")
        
    def view_prescription_details(self):
        """Display detailed information about the selected prescription"""
        selected = self.prescriptions_tree.selection()
        if not selected:
            messagebox.showinfo("Selection Required", "Please select a prescription to view details.")
            return
            
        # Get prescription ID
        prescription_id = self.prescriptions_tree.item(selected[0], 'values')[0]
        
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

    def sort_treeview(self, col):
        self.sort_order[col] = not self.sort_order[col]
        
        items = [(self.tree.item(item, "values"), item) for item in self.tree.get_children("")]
        
        columns = ("ID", "Date", "Time", "Patient", "Room", "Status")
        col_idx = columns.index(col)
        
        items.sort(key=lambda x: x[0][col_idx], reverse=self.sort_order[col])
        
        for idx, (_, item) in enumerate(items):
            self.tree.move(item, "", idx)
        
        self.update_heading_arrow(col)

    def sort_history_treeview(self, col):
        self.history_sort_order[col] = not self.history_sort_order[col]
        
        items = [(self.history_tree.item(item, "values"), item) for item in self.history_tree.get_children("")]
        
        col_idx = self.history_columns.index(col)
        
        items.sort(key=lambda x: x[0][col_idx], reverse=self.history_sort_order[col])
        
        for idx, (_, item) in enumerate(items):
            self.history_tree.move(item, "", idx)
        
        self.update_history_heading_arrow(col)
        
    def sort_prescriptions_treeview(self, col):
        """Sort prescriptions treeview by column"""
        self.prescriptions_sort_order[col] = not self.prescriptions_sort_order[col]
        
        items = [(self.prescriptions_tree.item(item, "values"), item) for item in self.prescriptions_tree.get_children("")]
        
        col_idx = self.prescriptions_columns.index(col)
        
        items.sort(key=lambda x: x[0][col_idx], reverse=self.prescriptions_sort_order[col])
        
        for idx, (_, item) in enumerate(items):
            self.prescriptions_tree.move(item, "", idx)
        
        self.update_prescriptions_heading_arrow(col)

    def update_heading_arrow(self, sort_col):
        columns = ("ID", "Date", "Time", "Patient", "Room", "Status")
        for col in columns:
            text = col
            if col == sort_col:
                text = f"{col} {'   ˄' if self.sort_order[col] else '  ˅'}"
            self.tree.heading(col, text=text)
    
    def update_history_heading_arrow(self, sort_col):
        for col in self.history_columns:
            text = col
            if col == sort_col:
                text = f"{col} {'   ˄' if self.history_sort_order[col] else '  ˅'}"
            self.history_tree.heading(col, text=text)
            
    def update_prescriptions_heading_arrow(self, sort_col):
        """Update the heading with an arrow indicating the sort direction"""
        for col in self.prescriptions_columns:
            text = col
            if col == sort_col:
                text = f"{col} {'   ˄' if self.prescriptions_sort_order[col] else '  ˅'}"
            self.prescriptions_tree.heading(col, text=text)

    def process_time_tuples(self, time):
        if isinstance(time, str) and time.startswith("(") and time.endswith(")"):
            try:
                time_str = time.strip("()").replace("'", "")
                start_time, end_time = time_str.split(", ")
                return f"{start_time} - {end_time}"
            except:
                return time
        return time
        
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

    def load_appointments(self):
        self.tree.delete(*self.tree.get_children(''))
        doctor_data = self.controller.current_user_data
        
        if not doctor_data:
            messagebox.showinfo("No Data", "Doctor data not found.")
            return
            
        appointments = doctor_data.get_protected_attribute("appointments")
        
        if not appointments or appointments == "[]" or appointments is None:
            messagebox.showinfo("No Appointments", "You have no appointments scheduled.")
            return
            
        appointment_data = []
        for appointment_id in appointments:
            if not isinstance(appointment_id, int):
                if isinstance(appointment_id, list) and len(appointment_id) == 1:
                    appointment_id = appointment_id[0]
                else:
                    continue
                    
            try:
                appointment = self.controller.hospital.appointments.get(appointment_id)
                
                if appointment.get("status") != "Scheduled":
                    continue
                    
                appt_id = appointment.get("appointment_id")
                date = appointment.get("date") if appointment.get("date") else "N/A"
                time = self.process_time_tuples(appointment.get("timeframe"))
                
                patient_id = appointment.get("patient_hid")
                patient_name = self.get_patient_name(patient_id)
                
                room = appointment.get("room_number")
                status = appointment.get("status")
                
                appointment_data.append((appt_id, date, time, patient_name, room, status))
            except Exception as exc:
                messagebox.showerror("Error", str(exc))
        
        # Sort appointments by date and time
        appointment_data.sort(key=lambda x: (x[1], x[2]))
        
        for data in appointment_data:
            self.tree.insert("", "end", values=data)

    def load_diagnoses(self):
        self.history_tree.delete(*self.history_tree.get_children(''))
        doctor_data = self.controller.current_user_data
        
        if not doctor_data:
            return
            
        doctor_id = doctor_data.get_protected_attribute("hospital_id")
        
        diagnoses = []
        for diag_id, diag in self.controller.hospital.diagnoses.items():
            if diag.get("doctor_hid") == doctor_id:
                diagnoses.append(diag)
        
        if not diagnoses:
            return
            
        diagnosis_data = []
        for diagnosis in diagnoses:
            try:
                diag_id = diagnosis.get("diagnosis_id")
                date = diagnosis.get("date", "N/A")
                
                patient_id = diagnosis.get("patient_hid", "N/A")
                patient_name = self.get_patient_name(patient_id)
                
                title = diagnosis.get("title", "N/A")
                appointment_id = diagnosis.get("appointment_id", "Completed")
                    
                diagnosis_data.append((diag_id, date, patient_name, title, appointment_id))
            except Exception as exc:
                print(f"Error processing diagnosis: {exc}")
        
        diagnosis_data.sort(key=lambda x: (x[1] is None, x[1]), reverse=True)
        
        for data in diagnosis_data:
            self.history_tree.insert("", "end", values=data)
            
    def load_prescriptions(self):
        """Load prescriptions from the database for the current doctor"""
        # Clear existing items
        for item in self.prescriptions_tree.get_children():
            self.prescriptions_tree.delete(item)
            
        doctor = self.controller.current_user_data
        
        try:
            prescriptions_ids = doctor.get_protected_attribute("prescriptions", [])
            
            if not prescriptions_ids or len(prescriptions_ids) == 0:
                self.prescriptions_tree.insert("", "end", values=("N/A", "No prescriptions found", "", "", "", ""))
                return
                
            for prescription_id in prescriptions_ids:
                if not isinstance(prescription_id, int):
                    continue
                    
                prescription = self.controller.hospital.prescriptions.get(prescription_id)
                if prescription:
                    drug_name = self.get_drug_name(prescription.get("drug_id"))
                    patient_name = self.get_patient_name(prescription.get("patient_hid"))
                    
                    self.prescriptions_tree.insert("", "end", values=(
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
        super().tkraise(*args, **kwargs)
        self.load_appointments()
        self.load_diagnoses()
        self.load_prescriptions()
        # Show default right panel
        self.toggle_right_panel(self.active_right_panel)
        
