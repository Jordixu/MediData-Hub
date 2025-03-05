import tkinter as tk 
import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk

class DoctorConsultation(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Doctor Consultation"

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        # Left side: Upcoming Appointments
        self.title_label = ctk.CTkLabel(self, text="Upcoming Appointments", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="ew")

        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.tree_frame)
        scrollbar.pack(side="right", fill="y")

        style = ttk.Style()
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b")
        style.map('Treeview', background=[('selected', 'grey30')])

        columns = ("ID", "Date", "Time", "Patient", "Room", "Status")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)

        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c))
            self.tree.column(col, width=100, anchor="center")

        self.tree.pack(expand=True, fill='both')

        self.sort_order = {col: False for col in columns}

        self.tree.bind("<<TreeviewSelect>>", self.selected)

        # Right side: Previous Diagnoses
        self.history_label = ctk.CTkLabel(self, text="Previous Diagnoses", font=ctk.CTkFont(size=20, weight="bold"))
        self.history_label.grid(row=0, column=1, pady=(20, 10), padx=20, sticky="ew")

        self.history_frame = ctk.CTkFrame(self)
        self.history_frame.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")

        history_scrollbar = ttk.Scrollbar(self.history_frame)
        history_scrollbar.pack(side="right", fill="y")

        self.history_columns = ("ID", "Date", "Patient", "Title", "Appointment ID")
        self.history_tree = ttk.Treeview(self.history_frame, columns=self.history_columns, show='headings', yscrollcommand=history_scrollbar.set)
        history_scrollbar.config(command=self.history_tree.yview)

        for col in self.history_columns:
            self.history_tree.heading(col, text=col, command=lambda c=col: self.sort_history_treeview(c))
            self.history_tree.column(col, width=100, anchor="center")
        
        # Make the title column wider
        self.history_tree.column("Title", width=200)

        self.history_tree.pack(expand=True, fill='both')

        self.history_sort_order = {col: False for col in self.history_columns}

        self.history_tree.bind("<<TreeviewSelect>>", self.history_selected)

        # Bottom buttons frame
        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.grid(row=2, column=0, columnspan=2, padx=20, pady=(10, 20), sticky="ew")

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
        self.back_button.pack(side="left", padx=20, pady=10)

        # Action buttons (right side)
        self.consult_button = ctk.CTkButton(
            self.buttons_frame,
            text="Start Consultation",
            command=self.start_consultation,
            width=180,
            height=40,
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        self.consult_button.pack(side="right", padx=20, pady=10)

        self.view_details_button = ctk.CTkButton(
            self.buttons_frame,
            text="View Diagnosis Details",
            command=self.view_diagnosis_details,
            width=180,
            height=40,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        self.view_details_button.pack(side="right", padx=20, pady=10)

    def selected(self, event=None):
        selected_items = self.tree.selection()
        if not selected_items:
            return
        
    def history_selected(self, event=None):
        selected_items = self.history_tree.selection()
        if not selected_items:
            return

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

    def process_time_tuples(self, time):
        if isinstance(time, str) and time.startswith("(") and time.endswith(")"):
            try:
                time_str = time.strip("()").replace("'", "")
                start_time, end_time = time_str.split(", ")
                return f"{start_time} - {end_time}"
            except:
                return time
        return time

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
                room = appointment.get("room_number")
                status = appointment.get("status")
                
                appointment_data.append((appt_id, date, time, patient_id, room, status))
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
                title = diagnosis.get("title", "N/A")
                appointment_id = diagnosis.get("appointment_id", "Completed")
                    
                diagnosis_data.append((diag_id, date, patient_id, title, appointment_id))
            except Exception as exc:
                print(f"Error processing diagnosis: {exc}")
        
        # Sort diagnoses by date (newest first)
        diagnosis_data.sort(key=lambda x: x[1], reverse=True)
        
        for data in diagnosis_data:
            self.history_tree.insert("", "end", values=data)

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.load_appointments()
        self.load_diagnoses()