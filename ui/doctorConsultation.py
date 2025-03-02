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
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

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

        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="ew")

        self.back_button = ctk.CTkButton(self.buttons_frame, text="Back", command=lambda: self.controller.show_frame("DoctorMainScreen"))
        self.back_button.pack(side="left", padx=20, pady=10)

        self.consult_button = ctk.CTkButton(self.buttons_frame, text="Start Consultation", command=self.start_consultation)
        self.consult_button.pack(side="right", padx=20, pady=10)

    def selected(self, event=None):
        selected_items = self.tree.selection()
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

    def sort_treeview(self, col):
        self.sort_order[col] = not self.sort_order[col]
        
        items = [(self.tree.item(item, "values"), item) for item in self.tree.get_children("")]
        
        columns = ("ID", "Date", "Time", "Patient", "Room", "Status")
        col_idx = columns.index(col)
        
        items.sort(key=lambda x: x[0][col_idx], reverse=self.sort_order[col])
        
        for idx, (_, item) in enumerate(items):
            self.tree.move(item, "", idx)
        
        self.update_heading_arrow(col)

    def update_heading_arrow(self, sort_col):
        columns = ("ID", "Date", "Time", "Patient", "Room", "Status")
        for col in columns:
            text = col
            if col == sort_col:
                text = f"{col} {'   ˄' if self.sort_order[col] else '  ˅'}"
            self.tree.heading(col, text=text)

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

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.load_appointments()
