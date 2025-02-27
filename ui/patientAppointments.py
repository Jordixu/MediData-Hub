import customtkinter as ctk
from tkinter import ttk, messagebox
import datetime as dt

class PatientAppointments(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Patient Appointments"

        # Back button
        self.back_button = ctk.CTkButton(self, text="Go Back", command=lambda: self.controller.show_frame("PatientMainScreen"))
        self.back_button.pack(pady=10)

        # Treeview Frame
        frame = ctk.CTkFrame(self)
        frame.pack(pady=20, expand=True, fill='both')

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        # Treeview Style
        style = ttk.Style()
        style.configure('Treeview', background='white', foreground='black', rowheight=30, fieldbackground='#e5e5e5', font=('Helvetica', 14))
        style.configure('Treeview.Heading', font=('Helvetica', 16, 'bold'))
        style.map('Treeview', background=[('selected', 'grey30')])

        # Treeview setup
        columns = ("ID", "Date", "Time", "Doctor", "Room", "Status")
        self.tree = ttk.Treeview(frame, columns=columns, show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)

        # Configure headings with sort commands
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c))
        self.tree.pack(expand=True, fill='both')

        # Initialize sort order tracking
        self.sort_order = {col: False for col in columns}  # False = Ascending, True = Descending

        # Event binding
        self.tree.bind("<<TreeviewSelect>>", self.selected)

        # Buttons
        self.request_button = ctk.CTkButton(self, text="Request New Appointment", command=lambda: self.controller.show_frame("PatientRequestAppointment"))
        self.request_button.pack(side=ctk.LEFT, padx=20, pady=10)

        self.cancel_button = ctk.CTkButton(self, text="Cancel Appointment", command=self.cancel_appointment)
        self.cancel_button.pack(side=ctk.RIGHT, padx=20, pady=10)

    def sort_treeview(self, col): 
        # Get all items and their current values in the selected column
        items = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]
        
        # Determine sorting key based on column type
        if col == "ID" or col == "Room" or col == "Doctor":
            items.sort(key=lambda x: int(x[0]), reverse=self.sort_order[col])
        elif col == "Date":
            items.sort(key=lambda x: dt.datetime.strptime(x[0], "%Y-%m-%d"), reverse=self.sort_order[col])
        elif col == "Time":
            items.sort(key=lambda x: x[0].split(" - ")[0], reverse=self.sort_order[col])
        else: # Default to string sorting (Status)
            items.sort(key=lambda x: x[0].lower(), reverse=self.sort_order[col])
        
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

    def load_appointments(self):
        """Load the appointments from the controller's patient data."""
        self.tree.delete(*self.tree.get_children())
        patient_data = self.controller.current_user_data
        # print("Patient Data:", patient_data)
        # print("Appointments:", patient_data.get_protected_attribute("appointments"))
        if not patient_data or patient_data.get_protected_attribute("appointments") == "[]" or patient_data.get_protected_attribute("appointments") == None:
            messagebox.showinfo("No Appointments", "You have no appointments scheduled.")
            # print("No appointments found.")
            return
        for appointment_id in patient_data.get_protected_attribute("appointments"):
            if not isinstance(appointment_id, int):
                # print("app type", type(appointment_id)) # Debugging purposes
                continue
            if isinstance(appointment_id, list) and len(appointment_id) == 1:
                appointment_id = appointment_id[0]
            # print("Appointment ID:", appointment_id) # Debugging purposes
            # print("Appointments:", type(patient_data.get_protected_attribute("appointments"))) # Debugging purposes
            try:
                appointment = self.controller.hospital.appointments.get(appointment_id)
                appt_id = appointment.get("appointment_id")
                date = appointment.get("date") if appointment.get("date") else "N/A"
                time = self.process_time_tuples(appointment.get("timeframe")) if appointment.get("timeframe") else "N/A"
                doc = appointment.get("doctor_hid")
                room = appointment.get("room_number") if appointment.get("room_number") else "N/A"
                status = appointment.get("status")
                # print("Appointment Data:", appt_id, date, time, doc, room, status)
                self.tree.insert("", "end", values=(appt_id, date, time, doc, room, status))
            except ValueError as exc:
                messagebox.showerror("Error", exc)
            except KeyError:
                messagebox.showerror("Error", "Appointment data not found.")

    def process_time_tuples(self, time):
        """Convert a tuple of time strings to a single string."""
        return f"{time[0]} - {time[1]}"

    def selected(self, event=None):
        """
        Handle selection events for the treeview.
        """
        _ = event # To avoid the unused variable warning
        selected_item = self.tree.selection()
        if selected_item:
            items = self.tree.item(selected_item[0], "values")
            # print("Selected row:", items)

    def cancel_appointment(self):
        """
        Cancel the currently selected appointment.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection","Please select an appointment to cancel.")
            return
        ans = messagebox.askyesno("Confirm Cancelation","Are you sure you want to cancel this appointment?")
        if ans:
            appointment_values = self.tree.item(selected_item[0], "values")
            try:
                # print("appointment_values[0]:", appointment_values[0])
                # print("appointment_values_type:", type(appointment_values[0]))
                self.controller.hospital.cancel_appointment(int(appointment_values[0]), "patient")
                messagebox.showinfo("Appointment Canceled", "The appointment has been canceled.")
                self.load_appointments()
            except ValueError as exc:
                messagebox.showerror("Error", exc)

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.load_appointments()
        # print("Appointments loaded.")
        