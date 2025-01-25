import tkinter as tk
import customtkinter as ctk

class AdminAppointments(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Admin Appointments"
        
        title_frame = ctk.CTkFrame(self)
        title_frame.pack()
        
        label = ctk.CTkLabel(title_frame, text="Appointments", font=("Helvetica", 24, "bold"))
        label.pack()
        
        # Divider
        line_frame = ctk.CTkFrame(self, height=2, fg_color="grey")
        line_frame.pack(fill="x", pady=20)
        
        # Search frame
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(pady=10)
        self.search_entry = ctk.CTkEntry(search_frame, width=240, height=35, placeholder_text="Search Appointments")
        
        self.search_entry.grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkButton(
            search_frame, text="Search", command=self.search_action, width=160, height=35
        ).grid(row=0, column=1, padx=10, pady=10)
        
        # Appointments frame
        appointments_frame = ctk.CTkFrame(self, fg_color="transparent")
        appointments_frame.pack(pady=10)
        self.appointments_list = tk.Listbox(appointments_frame, width=80, height=10)
        self.appointments_list.pack()
        
        # Action frame
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.pack(pady=10)
        ctk.CTkButton(
            action_frame, text="View Appointment", command=self.view_appointment, width=160, height=35
        ).pack(side="left", padx=10)
        ctk.CTkButton(
            action_frame, text="Delete Appointment", command=self.delete_appointment, width=160, height=35
        ).pack(side="left", padx=10)
        
        # Go Back frame
        back_frame = ctk.CTkFrame(self, fg_color="transparent")
        back_frame.pack(pady=20, fill="x")
        ctk.CTkButton(
            back_frame, text="Go Back", command=lambda: self.controller.show_frame("AdminMainScreen"),
            width=320, height=35
        ).pack()
        
    def search_action(self):
        search_term = self.search_entry.get()
        if search_term:
            appointments = self.controller.hospital.search_appointments(search_term)
            self.appointments_list.delete(0, tk.END)
            for appointment in appointments:
                self.appointments_list.insert(tk.END, f"{appointment.appointment_id} - {appointment.get_date()} - {appointment.get_time()}")
                print(self.appointments_list.get(0))
                
    def view_appointment(self):
        selected = self.appointments_list.curselection()
        if selected:
            appointment = self.appointments_list.get(selected[0])
            appointment_id = appointment.split(" - ")[0]
            self.controller.current_appointment = self.controller.hospital.get_appointment(appointment_id)
            self.controller.show_frame("AdminViewAppointment")
            
    def delete_appointment(self):
        selected = self.appointments_list.curselection()
        if selected:
            appointment = self.appointments_list.get(selected[0])
            appointment_id = appointment.split(" - ")[0]
            self.controller.hospital.delete_appointment(appointment_id)
            self.search_action()
            self.controller.show_frame("AdminAppointments")
            
    def clear_entries(self):
        self.search_entry.delete(0, tk.END)
        self.appointments_list.delete(0, tk.END)
        
    def load_appointments(self):
        appointments = self.controller.hospital.get_appointments()
        self.appointments_list.delete(0, tk.END)
        for appointment in appointments:
            self.appointments_list.insert(tk.END, f"{appointment[0]} - {appointment[1]} - {appointment[2]}")
            
    def on_show_frame(self):
        self.clear_entries()
        self.load_appointments()
        
    def on_hide_frame(self):
        self.clear_entries()
        self.controller.current_appointment = None