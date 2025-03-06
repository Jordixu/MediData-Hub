import customtkinter as ctk
from tkinter import ttk, messagebox
import datetime as dt
import tkinter as tk

class PatientMedicalRecords(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Patient Medical Records"
        
        # Track active panel
        self.active_panel = "diagnoses"

        # Configure the main layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Header with toggle buttons
        self.grid_rowconfigure(1, weight=1)  # Treeview container
        self.grid_rowconfigure(2, weight=0)  # Buttons
        
        # Header frame with toggle buttons
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(20, 10), padx=20)
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=1)
        header_frame.grid_columnconfigure(2, weight=0)
        
        # Toggle buttons for switching between diagnoses and prescriptions
        self.diagnoses_btn = ctk.CTkButton(
            header_frame,
            text="Your Diagnoses", 
            command=lambda: self.toggle_panel("diagnoses"),
            fg_color="#191c4a" if self.active_panel == "diagnoses" else "#555555",
            hover_color="#393e80",
            height=40,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.diagnoses_btn.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        self.prescriptions_btn = ctk.CTkButton(
            header_frame,
            text="Your Prescriptions", 
            command=lambda: self.toggle_panel("prescriptions"),
            fg_color="#555555" if self.active_panel == "diagnoses" else "#191c4a",
            hover_color="#666666",
            height=40,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.prescriptions_btn.grid(row=0, column=1, padx=(5, 0), sticky="ew")
        
        # View Details button
        self.view_details_button = ctk.CTkButton(
            header_frame,
            text="View Diagnosis Details",  # Default text for diagnoses panel
            command=self.view_details,
            width=150,
            height=40,
            fg_color="#204a1d",
            hover_color="#548251",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.view_details_button.grid(row=0, column=2, padx=(15, 0), sticky="e")

        # Container for panels (both diagnoses and prescriptions)
        self.panel_container = ctk.CTkFrame(self)
        self.panel_container.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        # ------------------- DIAGNOSES PANEL -------------------
        self.diagnoses_frame = ctk.CTkFrame(self.panel_container, fg_color="transparent")
        
        diagnoses_scrollbar = ttk.Scrollbar(self.diagnoses_frame, orient="vertical")
        diagnoses_scrollbar.pack(side="right", fill="y")

        # Treeview Style
        style = ttk.Style()
        style.configure('Treeview', rowheight=30, font=('Helvetica', 12))
        style.configure('Treeview.Heading', font=('Helvetica', 13, 'bold'))
        style.map('Treeview', background=[('selected', '#4a6984')])
        
        # Diagnoses Treeview setup
        self.diagnoses_columns = ("ID", "Date", "Appointment ID", "Doctor", "Title")
        self.diagnoses_tree = ttk.Treeview(
            self.diagnoses_frame, 
            columns=self.diagnoses_columns, 
            show='headings', 
            yscrollcommand=diagnoses_scrollbar.set
        )
        diagnoses_scrollbar.config(command=self.diagnoses_tree.yview)

        # Configure column widths for diagnoses
        self.diagnoses_tree.column("ID", width=60, anchor="center")
        self.diagnoses_tree.column("Date", width=100, anchor="center")
        self.diagnoses_tree.column("Appointment ID", width=120, anchor="center")
        self.diagnoses_tree.column("Doctor", width=180, anchor="w")
        self.diagnoses_tree.column("Title", width=280, anchor="w")
        
        for col in self.diagnoses_columns:
            self.diagnoses_tree.heading(col, text=col, command=lambda c=col: self.sort_diagnoses_treeview(c))
        
        self.diagnoses_tree.pack(expand=True, fill='both')
        self.diagnoses_sort_order = {col: False for col in self.diagnoses_columns}
        self.diagnoses_tree.bind("<<TreeviewSelect>>", self.diagnoses_selected)
        self.diagnoses_tree.bind('<Button-1>', self.block_column_resize)
        
        # ------------------- PRESCRIPTIONS PANEL -------------------
        self.prescriptions_frame = ctk.CTkFrame(self.panel_container, fg_color="transparent")
        
        prescriptions_scrollbar = ttk.Scrollbar(self.prescriptions_frame, orient="vertical")
        prescriptions_scrollbar.pack(side="right", fill="y")
        
        # Prescriptions Treeview setup
        self.prescriptions_columns = ("ID", "Drug", "Doctor", "Diagnosis ID", "Dosage", "Status")
        self.prescriptions_tree = ttk.Treeview(
            self.prescriptions_frame, 
            columns=self.prescriptions_columns, 
            show='headings', 
            yscrollcommand=prescriptions_scrollbar.set
        )
        prescriptions_scrollbar.config(command=self.prescriptions_tree.yview)
        
        # Configure column widths for prescriptions
        self.prescriptions_tree.column("ID", width=60, anchor="center")
        self.prescriptions_tree.column("Drug", width=150, anchor="w")
        self.prescriptions_tree.column("Doctor", width=150, anchor="w")
        self.prescriptions_tree.column("Diagnosis ID", width=100, anchor="center")
        self.prescriptions_tree.column("Dosage", width=220, anchor="w")
        self.prescriptions_tree.column("Status", width=100, anchor="center")
        
        for col in self.prescriptions_columns:
            self.prescriptions_tree.heading(col, text=col, command=lambda c=col: self.sort_prescriptions_treeview(c))
        
        self.prescriptions_tree.pack(expand=True, fill='both')
        self.prescriptions_sort_order = {col: False for col in self.prescriptions_columns}
        self.prescriptions_tree.bind("<<TreeviewSelect>>", self.prescriptions_selected)
        self.prescriptions_tree.bind('<Button-1>', self.block_column_resize)

        # Button frame
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="ew")
        
        # Back button
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
        
        # Initialize the active panel (show diagnoses by default)
        # This is crucial to show content when the frame is first loaded
        self.diagnoses_frame.pack(fill="both", expand=True)

    def toggle_panel(self, panel_name):
        if panel_name == self.active_panel:
            return
            
        # Update active panel
        self.active_panel = panel_name
        
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

    def block_column_resize(self, event):
        if event.widget.identify_region(event.x, event.y) == "separator":
            return "break"

    def diagnoses_selected(self, event=None):
        pass
        
    def prescriptions_selected(self, event=None):
        pass

    def view_details(self):
        if self.active_panel == "diagnoses":
            self.view_diagnosis_details()
        else:
            self.view_prescription_details()

    def view_diagnosis_details(self):
        selected_item = self.diagnoses_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a diagnosis to view details.")
            return
            
        diagnosis_values = self.diagnoses_tree.item(selected_item[0], "values")
        diagnosis_id = int(diagnosis_values[0])
        
        try:
            diagnosis = self.controller.hospital.diagnoses.get(diagnosis_id)
            if not diagnosis:
                messagebox.showerror("Error", f"Diagnosis {diagnosis_id} not found.")
                return
                
            self.controller.selected_diagnosis = diagnosis
            self.controller.show_frame("DiagnosesDetails")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to view diagnosis details: {e}")
            
    def view_prescription_details(self):
        selected = self.prescriptions_tree.selection()
        if not selected:
            messagebox.showinfo("Selection Required", "Please select a prescription to view details.")
            return
            
        prescription_id = int(self.prescriptions_tree.item(selected[0], 'values')[0])
        
        try:
            prescription = self.controller.hospital.prescriptions.get(prescription_id)
            if prescription:
                self.controller.selected_prescription = prescription
                self.controller.show_frame("PrescriptionDetails")
            else:
                messagebox.showinfo("Not Found", "Prescription details not found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def sort_diagnoses_treeview(self, col):
        self.diagnoses_sort_order[col] = not self.diagnoses_sort_order[col]
        
        items = [(self.diagnoses_tree.item(item, "values"), item) for item in self.diagnoses_tree.get_children("")]
        
        col_idx = self.diagnoses_columns.index(col)
        
        # Special handling for different column types
        if col in ("ID", "Appointment ID"):
            def int_sort_key(x):
                if x[0][col_idx] == "N/A":
                    return -999999 if self.diagnoses_sort_order[col] else 999999
                try:
                    return int(x[0][col_idx])
                except ValueError:
                    return 0
            items.sort(key=int_sort_key, reverse=self.diagnoses_sort_order[col])
        elif col == "Date":
            def date_sort_key(x):
                if x[0][col_idx] == "N/A":
                    return dt.datetime.min if self.diagnoses_sort_order[col] else dt.datetime.max
                try:
                    return dt.datetime.strptime(x[0][col_idx], "%Y-%m-%d")
                except ValueError:
                    return dt.datetime.min
            items.sort(key=date_sort_key, reverse=self.diagnoses_sort_order[col])
        else:
            items.sort(key=lambda x: str(x[0][col_idx]).lower(), reverse=self.diagnoses_sort_order[col])
        
        for idx, (_, item) in enumerate(items):
            self.diagnoses_tree.move(item, "", idx)
        
        self.update_diagnoses_heading_arrow(col)
        
    def sort_prescriptions_treeview(self, col):
        self.prescriptions_sort_order[col] = not self.prescriptions_sort_order[col]
        
        items = [(self.prescriptions_tree.item(item, "values"), item) for item in self.prescriptions_tree.get_children("")]
        
        col_idx = self.prescriptions_columns.index(col)
        
        if col in ("ID", "Diagnosis ID"):
            def int_sort_key(x):
                if x[0][col_idx] == "N/A":
                    return -999999 if self.prescriptions_sort_order[col] else 999999
                try:
                    return int(x[0][col_idx])
                except ValueError:
                    return 0
            items.sort(key=int_sort_key, reverse=self.prescriptions_sort_order[col])
        else:
            items.sort(key=lambda x: str(x[0][col_idx]).lower(), reverse=self.prescriptions_sort_order[col])
        
        for idx, (_, item) in enumerate(items):
            self.prescriptions_tree.move(item, "", idx)
        
        self.update_prescriptions_heading_arrow(col)

    def update_diagnoses_heading_arrow(self, sort_col):
        for col in self.diagnoses_columns:
            text = col
            if col == sort_col:
                text = f"{col} {'   ˄' if self.diagnoses_sort_order[col] else '   ˅'}"
            self.diagnoses_tree.heading(col, text=text)
            
    def update_prescriptions_heading_arrow(self, sort_col):
        for col in self.prescriptions_columns:
            text = col
            if col == sort_col:
                text = f"{col} {'   ˄' if self.prescriptions_sort_order[col] else '   ˅'}"
            self.prescriptions_tree.heading(col, text=text)

    def load_diagnoses(self):
        self.diagnoses_tree.delete(*self.diagnoses_tree.get_children())
        patient_data = self.controller.current_user_data
        
        if not patient_data or not hasattr(patient_data, "get_protected_attribute"):
            self.diagnoses_tree.insert("", "end", values=("N/A", "N/A", "N/A", "N/A", "No patient data available"))
            return
            
        diagnoses = patient_data.get_protected_attribute("diagnoses")
        if not diagnoses or diagnoses == [] or diagnoses == "[]":
            self.diagnoses_tree.insert("", "end", values=("N/A", "N/A", "N/A", "N/A", "No diagnoses found"))
            return
            
        for diagnosis_id in diagnoses:
            if not isinstance(diagnosis_id, int):
                continue
                
            try:
                diagnosis = self.controller.hospital.diagnoses.get(diagnosis_id)
                if not diagnosis:
                    continue
                    
                diag_id = diagnosis.get("diagnosis_id")
                
                # Format date
                date_val = diagnosis.get("date")
                if date_val and date_val != "N/A":
                    if isinstance(date_val, dt.date):
                        date = date_val.strftime("%Y-%m-%d")
                    else:
                        date = str(date_val)
                else:
                    date = "N/A"
                
                appointment_id = diagnosis.get("appointment_id", "N/A")
                doctor_id = diagnosis.get("doctor_hid", "N/A")
                
                # Get doctor name
                if doctor_id != "N/A":
                    doctor = self.controller.hospital.doctors.get(doctor_id)
                    doctor_name = doctor.__name__() if doctor else "Unknown"
                else:
                    doctor_name = "N/A"
                    
                title = diagnosis.get("title", "N/A")
                
                # Insert the row
                self.diagnoses_tree.insert(
                    "", "end", 
                    values=(diag_id, date, appointment_id, doctor_name, title)
                )
            except Exception as e:
                print(f"Error loading diagnosis: {e}")

    def load_prescriptions(self):
        self.prescriptions_tree.delete(*self.prescriptions_tree.get_children())
        
        patient_data = self.controller.current_user_data
        
        if not patient_data or not hasattr(patient_data, "get_protected_attribute"):
            self.prescriptions_tree.insert("", "end", values=("N/A", "N/A", "N/A", "N/A", "N/A", "No patient data available"))
            return
            
        prescriptions_ids = patient_data.get_protected_attribute("prescriptions", [])
        if not prescriptions_ids or prescriptions_ids == [] or prescriptions_ids == "[]":
            self.prescriptions_tree.insert("", "end", values=("N/A", "N/A", "N/A", "N/A", "N/A", "No prescriptions found"))
            return
            
        for prescription_id in prescriptions_ids:
            if not isinstance(prescription_id, int):
                continue
                
            try:
                prescription = self.controller.hospital.prescriptions.get(prescription_id)
                if not prescription:
                    continue
                
                doctor_id = prescription.get("doctor_hid", "N/A")
                if doctor_id != "N/A":
                    doctor = self.controller.hospital.doctors.get(doctor_id)
                    doctor_name = doctor.__name__() if doctor else "Unknown"
                else:
                    doctor_name = "N/A"
                    
                drug_id = prescription.get("drug_id", "N/A")
                if drug_id != "N/A":
                    drug = self.controller.hospital.drugs.get(drug_id)
                    drug_name = drug.get("commercial_name", "N/A") if drug else f"Drug #{drug_id}"
                else:
                    drug_name = "N/A"
                    
                self.prescriptions_tree.insert("", "end", values=(
                    prescription.get("prescription_id", "N/A"),
                    drug_name,
                    doctor_name,
                    prescription.get("diagnosis_id", "N/A"),
                    prescription.get("dosage", "N/A"),
                    prescription.get("status", "N/A")
                ))
            except Exception as e:
                print(f"Error loading prescription: {e}")

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.load_diagnoses()
        self.load_prescriptions()
        # Make sure the active panel is correctly displayed
        self.toggle_panel(self.active_panel)