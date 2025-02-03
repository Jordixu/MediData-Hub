import customtkinter as ctk
from tkinter import ttk

class PatientListOfDoctors(ctk.CTkToplevel):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "List of Doctors"

        self.doctor_list_frame = ctk.CTkFrame(self)
        self.doctor_list_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.tree = ttk.Treeview(self.doctor_list_frame, columns=("ID", "Name", "Specialty"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Specialty", text="Specialty")
        self.tree.pack(expand=True, fill="both")

        # self.load_doctors()

    # def load_doctors(self):
    #     self.tree.delete(*self.tree.get_children())
    #     doctors = self.controller.hospital.get_doctors()
    #     for doctor in doctors:
    #         self.tree.insert("", "end", values=(doctor.id, doctor.name, doctor.specialty))
            
    # def selected(self, event):
    #     selected_item = self.tree.selection()[0]
    #     values = self.tree.item(selected_item, "values")
    #     doctor_id = values[0]
    #     self.controller.selected_doctor_id = doctor_id
    #     self.controller.show_frame("DoctorInformation")
    
    # def request_appointment(self):
    #     if not getattr(self.controller, "selected_doctor_id", None):
    #         messagebox.showerror("Error", "Please select a doctor.")
    #         return
    
    #     self.controller.show_frame("RequestAppointment")
    
    # def go_back(self):
    #     self.controller.show_frame("PatientMainScreen")   
    
