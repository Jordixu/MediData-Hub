import customtkinter as ctk
from tkinter import ttk, messagebox

class PatientAppointments(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Patient Appointments"

        self.back_button = ctk.CTkButton(self, text="Go Back", command=lambda: self.controller.show_frame("PatientMainScreen"))
        self.back_button.pack(pady=10)

        frame = ctk.CTkFrame(self)
        frame.pack(pady=20, expand=True, fill='both')

        style = ttk.Style()
        style.configure('Treeview', background='white', foreground='black', rowheight=30, fieldbackground='#e5e5e5', font=('Helvetica', 14))
        style.configure('Treeview.Heading', font=('Helvetica', 16, 'bold'))
        style.map('Treeview', background=[('selected', '#4CAF50')])

        self.tree = ttk.Treeview(frame, columns=("ID", "Date", "Time", "Doctor", "Room", "Status"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Time", text="Time")
        self.tree.heading("Doctor", text="Doctor")
        self.tree.heading("Room", text="Room")
        self.tree.heading("Status", text="Status")
        self.tree.pack(expand=True, fill='both')

        self.tree.bind("<<TreeviewSelect>>", self.selected)

        self.request_button = ctk.CTkButton(self, text="Request New Appointment", command=lambda: self.request_appointment)
        self.request_button.pack(side=ctk.LEFT, padx=20, pady=10)

        self.cancel_button = ctk.CTkButton(self, text="Cancel Appointment", command=lambda: self.cancel_appointment)
        self.cancel_button.pack(side=ctk.RIGHT, padx=20, pady=10)

    def load_appointments(self):
        """Load the appointments from the controller's patient data."""
        self.tree.delete(*self.tree.get_children())
        patient_data = self.controller.current_user_data
        if not patient_data or not patient_data.get_protected_attribute("appointments"):
            print("No appointments found for this patient.") # Debugging purposes
            return
        for appointment_id in patient_data.get_protected_attribute("appointments"):
            print("Appointment ID:", appointment_id) # Debugging purposes
            print("Appointments:", type(patient_data.get_protected_attribute("appointments"))) # Debugging purposes
            for appointment in self.controller.hospital.appointments:
                if appointment.get("appointment_id") == appointment_id:
                    appt_id = appointment.get("appointment_id")
                    date = appointment.get("date")
                    time = appointment.get("timeframe")
                    doc = appointment.get("doctor_hid")
                    room = appointment.get("room_number")
                    status = appointment.get("status")
                    print("Appointment Data:", appt_id, date, time, doc, room, status) # Debugging purposes
                    self.tree.insert("", "end", values=(appt_id, date, time, doc, room, status))

    def selected(self):
        selected_item = self.tree.selection()
        if selected_item:
            items = self.tree.item(selected_item[0], "values")
            print("Selected row:", items) # Debugging purposes

    def request_appointment(self):
        # Implement your logic to add a new appointment to the hospital's data structure
        pass

    def cancel_appointment(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an appointment to cancel.")
            return
        ans = messagebox.askyesno("Confirm Cancelation", "Are you sure you want to cancel the selected appointment?")
        if ans:
            appointment_values = self.tree.item(selected_item[0], "values")
            try:
                self.controller.hospital.cancel_appointment(appointment_values(0))
                messagebox.showinfo("Appointment Canceled", "The appointment has been canceled successfully.")
            except Exception as exc:
                messagebox.showerror("Error", exc)

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.load_appointments()