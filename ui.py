import tkinter as tk
from tkinter import ttk

class UserInterface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MediData Hub")
        self.geometry("1000x600")

        ttk.Label(self, text="Select Role", font=("Arial", 14)).pack(pady=20)
        ttk.Button(self, text="Doctor UI", command=self.open_doctor_ui).pack(pady=5)
        ttk.Button(self, text="Patient UI", command=self.open_patient_ui).pack(pady=5)
        ttk.Button(self, text="Admin UI", command=self.open_admin_ui).pack(pady=5)

    def open_doctor_ui(self):
        self.hide()
        DoctorUI(self)

    def open_patient_ui(self):
        self.hide()
        PatientUI(self)

    def open_admin_ui(self):
        self.hide()
        AdminUI(self)

    def hide(self):
        self.withdraw()

    def show(self):
        self.deiconify()

class DoctorUI(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("MediData Hub for Doctors")
        self.geometry("300x200")
        ttk.Label(self, text="Doctor Interface", font=("Arial", 14)).pack(pady=20)
        ttk.Button(self, text="Back to Main", command=self.back_to_main).pack(pady=5)

    def back_to_main(self):
        self.destroy()
        self.master.show()

class PatientUI(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("MediData Hub for Patients")
        self.geometry("300x200")
        ttk.Label(self, text="Patient Interface", font=("Arial", 14)).pack(pady=20)
        ttk.Button(self, text="Back to Main", command=self.back_to_main).pack(pady=5)

    def back_to_main(self):
        self.destroy()
        self.master.show()

class AdminUI(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("MediData Hub for Patients")
        self.geometry("300x200")
        ttk.Label(self, text="Administrator Interface", font=("Arial", 14)).pack(pady=20)
        ttk.Button(self, text="Back to Main", command=self.back_to_main).pack(pady=5)

    def back_to_main(self):
        self.destroy()
        self.master.show()

if __name__ == "__main__":
    app = UserInterface()
    app.mainloop()
