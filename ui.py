import tkinter as tk
from tkinter import ttk, messagebox

class RoleSelectionScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.title("Role Selection")

        label = ttk.Label(self, text="Select Role", font=("Helvetica", 16))
        label.pack(pady=20)

        ttk.Button(self, text="Patient", command=lambda: self.select_role("patient"), width=20).pack(pady=5)
        ttk.Button(self, text="Doctor", command=lambda: self.select_role("doctor"), width=20).pack(pady=5)
        ttk.Button(self, text="Administrator", command=self.not_implemented, width=20).pack(pady=5)

    def select_role(self, role):
        self.controller.selected_role = role
        if role == "patient":
            self.controller.show_frame("LoginScreenPatient")
        elif role == "doctor":
            self.controller.show_frame("LoginScreenDoctor")

    def not_implemented(self):
        messagebox.showinfo("Info", "Not implemented yet.")

class LoginScreenPatient(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.title("Login Screen")
        
        ## TEST ONLY
        
        bypass_label = ttk.Label(self, text="Direct Navigation (Test Only)", font=("Helvetica", 14, "bold"))
        bypass_label.pack(pady=10)
        
        ttk.Button(
            self,
            text="Go to Patient Main Screen",
            command=lambda: self.controller.show_frame("PatientMainScreen")
        ).pack(pady=5)
        
        ## END TEST ONLY

        ttk.Label(self, text="User (ID):", font=("Helvetica", 12)).pack(pady=5)
        self.user_entry = ttk.Entry(self)
        self.user_entry.pack(pady=5)

        ttk.Label(self, text="Password:", font=("Helvetica", 12)).pack(pady=5)
        self.pass_entry = ttk.Entry(self, show="*")
        self.pass_entry.pack(pady=5)

        ttk.Button(self, text="Login", command=self.login_action).pack(pady=5)
        ttk.Button(self, text="Register", command=lambda: self.controller.show_frame("RegisterScreenPatient")).pack(pady=5)
        ttk.Button(self, text="Go Back", command=lambda: self.controller.show_frame("RoleSelectionScreen")).pack(pady=5)
        
    def clear_entries(self):
        """Clear all input fields."""
        self.user_entry.delete(0, tk.END)
        self.pass_entry.delete(0, tk.END)

    def login_action(self):
        role = getattr(self.controller, "selected_role", None)
        personal_id = self.user_entry.get()
        password = self.pass_entry.get()
        roles = role + 's' 
        if role == "patient":
            for patient in self.controller.hospital.patients:
                if int(patient.personal_id) == int(personal_id):
                    if patient.check_password(password):
                        self.controller.current_user = int(personal_id)
                        self.controller.current_user_data = patient
                        self.controller.show_frame("PatientMainScreen")
                        self.clear_entries()
                    return
            messagebox.showerror("Error", "Invalid user or password")
        elif role == "doctor":
            for doctor in self.controller.hospital.doctors:
                if int(doctor.personal_id) == int(personal_id):
                    if doctor.password == password:
                        self.controller.current_user = int(personal_id)
                        self.controller.current_user_data = doctor
                        self.controller.show_frame("DoctorMainScreen")
                        self.clear_entries()
                    return
            messagebox.showerror("Error", "Invalid user or password")
        else:
            messagebox.showerror("Error", "Role not supported")

class LoginScreenDoctor(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.title("Login Screen")
        
        ## TEST ONLY
        
        bypass_label = ttk.Label(self, text="Direct Navigation (Test Only)", font=("Helvetica", 14, "bold"))
        bypass_label.pack(pady=10)
        
        ttk.Button(
            self,
            text="Go to Doctor Main Screen",
            command=lambda: self.controller.show_frame("DoctorMainScreen")
        ).pack(pady=5)
        
        ## END TEST ONLY

        ttk.Label(self, text="User (ID):", font=("Helvetica", 12)).pack(pady=5)
        self.user_entry = ttk.Entry(self)
        self.user_entry.pack(pady=5)

        ttk.Label(self, text="Password:", font=("Helvetica", 12)).pack(pady=5)
        self.pass_entry = ttk.Entry(self, show="*")
        self.pass_entry.pack(pady=5)

        ttk.Button(self, text="Login", command=self.login_action).pack(pady=5)
        ttk.Button(self, text="Go Back", command=lambda: self.controller.show_frame("RoleSelectionScreen")).pack(pady=5)
        
    def clear_entries(self):
        """Clear all input fields."""
        self.user_entry.delete(0, tk.END)
        self.pass_entry.delete(0, tk.END)

    def login_action(self):
        role = getattr(self.controller, "selected_role", None)
        personal_id = self.user_entry.get()
        password = self.pass_entry.get()
        roles = role + 's' 
        if role == "patient":
            for patient in self.controller.hospital.patients:
                if int(patient.personal_id) == int(personal_id):
                    if patient.password == password:
                        self.controller.current_user = personal_id
                        self.controller.current_user_data = patient
                        self.controller.show_frame("PatientMainScreen")
                        self.clear_entries()
                    return
            messagebox.showerror("Error", "Invalid user or password")
        elif role == "doctor":
            for doctor in self.controller.hospital.doctors:
                if doctor.personal_id == personal_id:
                    if doctor.password == password:
                        self.controller.current_user = personal_id
                        self.controller.current_user_data = doctor
                        self.controller.show_frame("DoctorMainScreen")
                        self.clear_entries()
                    return
            messagebox.showerror("Error", "Invalid user or password")
        else:
            messagebox.showerror("Error", "Role not supported")

class RegisterScreenPatient(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.title("Register")
        
        ttk.Label(self, text="Register", font=("Helvetica", 16)).pack(pady=10)
        
        ttk.Label(self, text="User (ID)").pack(padx=5, pady=2)
        self.user_entry = ttk.Entry(self)
        self.user_entry.pack(padx=5, pady=2)

        ttk.Label(self, text="Password").pack(padx=5, pady=2)
        self.pass_entry = ttk.Entry(self, show='*')
        self.pass_entry.pack(padx=5, pady=2)
        
        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=5, pady=5)
        
        ttk.Label(self, text="Personal Information", font=("Helvetica", 12)).pack(pady=5)

        ttk.Label(self, text="Name").pack(padx=5, pady=2)
        self.name_entry = ttk.Entry(self)
        self.name_entry.pack(padx=5, pady=2)

        ttk.Label(self, text="Surname").pack(padx=5, pady=2)
        self.surname_entry = ttk.Entry(self)
        self.surname_entry.pack(padx=5, pady=2)

        ttk.Label(self, text="Gender").pack(padx=5, pady=2)
        self.gender_var = tk.StringVar()
        self.male_check = ttk.Checkbutton(self, text="Male", variable=self.gender_var, onvalue="Male", offvalue="")
        self.female_check = ttk.Checkbutton(self, text="Female", variable=self.gender_var, onvalue="Female", offvalue="")
        self.male_check.pack(padx=5, pady=2)
        self.female_check.pack(padx=5, pady=2)

        ttk.Label(self, text="Age").pack(padx=5, pady=2)
        self.age_entry = ttk.Entry(self)
        self.age_entry.pack(padx=5, pady=2)

        ttk.Label(self, text="Weight (in kg)").pack(padx=5, pady=2)
        self.weight_entry = ttk.Entry(self)
        self.weight_entry.pack(padx=5, pady=2)

        ttk.Label(self, text="Height (in cm)").pack(padx=5, pady=2)
        self.height_entry = ttk.Entry(self)
        self.height_entry.pack(padx=5, pady=2)

        ttk.Button(self, text="Submit", command=self.submit_data).pack(pady=5)
        ttk.Button(self, text="Go Back", command=lambda: controller.show_frame("LoginScreenPatient")).pack(pady=5)
        
    def clear_entries(self):
        """Clear all input fields."""
        self.user_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.surname_entry.delete(0, tk.END)
        self.gender_var.set("")
        self.age_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.height_entry.delete(0, tk.END)
        self.pass_entry.delete(0, tk.END)

    def submit_data(self):
        role = getattr(self.controller, "selected_role", "patient")
        personal_id = self.user_entry.get()
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        gender = self.gender_var.get()
        age = self.age_entry.get()
        weight = self.weight_entry.get()
        height = self.height_entry.get()
        password = self.pass_entry.get()

        fields = [name, surname, gender, age, weight, height, personal_id, password]
        if all(fields):
            try:
                self.controller.hospital.add_patient(
                    personal_id=personal_id,
                    password=password,
                    name=name,
                    surname=surname,
                    age=age,
                    gender=gender,
                    weight=weight,
                    height=height
                )
                messagebox.showinfo("Info", "Registration completed!")
                self.clear_entries()
                self.controller.show_frame("LoginScreenPatient")
            except ValueError as e:
                messagebox.showerror("Error", e)
            except Exception as e:
                messagebox.showerror("Error", e)
        else:
            messagebox.showerror("Error", "Please fill out all fields")

class RegisterScreenDoctor(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.title("Register")
        
        ttk.Label(self, text="Register", font=("Helvetica", 16)).pack(pady=10)
        
        ttk.Label(self, text="User (ID)").pack(padx=5, pady=2)
        self.user_entry = ttk.Entry(self)
        self.user_entry.pack(padx=5, pady=2)

        ttk.Label(self, text="Password").pack(padx=5, pady=2)
        self.pass_entry = ttk.Entry(self, show='*')
        self.pass_entry.pack(padx=5, pady=2)
        
        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=5, pady=5)
        
        ttk.Label(self, text="Personal Information", font=("Helvetica", 12)).pack(pady=5)

        ttk.Label(self, text="Name").pack(padx=5, pady=2)
        self.name_entry = ttk.Entry(self)
        self.name_entry.pack(padx=5, pady=2)

        ttk.Label(self, text="Surname").pack(padx=5, pady=2)
        self.surname_entry = ttk.Entry(self)
        self.surname_entry.pack(padx=5, pady=2)

        ttk.Label(self, text="Gender").pack(padx=5, pady=2)
        self.gender_var = tk.StringVar()
        self.male_check = ttk.Checkbutton(self, text="Male", variable=self.gender_var, onvalue="Male", offvalue="")
        self.female_check = ttk.Checkbutton(self, text="Female", variable=self.gender_var, onvalue="Female", offvalue="")
        self.male_check.pack(padx=5, pady=2)
        self.female_check.pack(padx=5, pady=2)

        ttk.Label(self, text="Age").pack(padx=5, pady=2)
        self.age_entry = ttk.Entry(self)
        self.age_entry.pack(padx=5, pady=2)

        ttk.Label(self, text="Speciality").pack(padx=5, pady=2)
        self.speciality_entry = ttk.Entry(self)
        self.speciality_entry.pack(padx=5, pady=2)

        ttk.Label(self, text="Department").pack(padx=5, pady=2)
        self.department_entry = ttk.Entry(self)
        self.department_entry.pack(padx=5, pady=2)
        
        ttk.Label(self, text="Social Security Number").pack(padx=5, pady=2)
        self.social_security_entry = ttk.Entry(self)
        self.social_security_entry.pack(padx=5, pady=2)
        
        ttk.Label(self, text="Salary").pack(padx=5, pady=2)
        self.salary_entry = ttk.Entry(self)
        self.salary_entry.pack(padx=5, pady=2)

        ttk.Button(self, text="Submit", command=self.submit_data).pack(pady=5)
        ttk.Button(self, text="Go Back", command=lambda: controller.show_frame("LoginScreen")).pack(pady=5)
        
    def clear_entries(self):
        """Clear all input fields."""
        self.user_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.surname_entry.delete(0, tk.END)
        self.gender_var.set("")
        self.age_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.height_entry.delete(0, tk.END)
        self.pass_entry.delete(0, tk.END)

    def submit_data(self):
        role = getattr(self.controller, "selected_role", "patient")
        personal_id = self.user_entry.get()
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        gender = self.gender_var.get()
        age = self.age_entry.get()
        weight = self.weight_entry.get()
        height = self.height_entry.get()
        password = self.pass_entry.get()

        fields = [name, surname, gender, age, weight, height, personal_id, password]
        if all(fields):
            try:
                self.controller.hospital.add_patient(
                    personal_id=personal_id,
                    password=password,
                    name=name,
                    surname=surname,
                    age=age,
                    gender=gender,
                    weight=weight,
                    height=height
                )
                messagebox.showinfo("Info", "Registration completed!")
                self.clear_entries()
                self.controller.show_frame("LoginScreen")
            except ValueError as e:
                messagebox.showerror("Error", e)
            except Exception as e:
                messagebox.showerror("Error", e)
        else:
            messagebox.showerror("Error", "Please fill out all fields")

class PatientMainScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.title("Patient Main Screen")

        ttk.Label(self, text="Patient Main Screen", font=("Helvetica", 16)).pack(pady=10)

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Personal Data", width=15,
                   command=lambda: controller.show_frame("PatientInformation")).grid(row=0, column=0, padx=10, pady=10)
        ttk.Button(button_frame, text="Prescriptions", width=15,
                   command=lambda: controller.show_frame("Prescriptions")).grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(button_frame, text="Appointments", width=15,
                   command=self.not_implemented).grid(row=1, column=0, padx=10, pady=10)
        ttk.Button(button_frame, text="Notifications", width=15,
                   command=self.not_implemented).grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(self, text="Go Back", command=lambda: controller.show_frame("RoleSelectionScreen")).pack(pady=20)

    def not_implemented(self):
        messagebox.showinfo("Info", "Not implemented yet.")

class DoctorMainScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.title("Doctor Main Screen")

        ttk.Label(self, text="Doctor Main Screen", font=("Helvetica", 16)).pack(pady=10)

        ttk.Button(self, text="Prescriptions", command=self.not_implemented).pack(pady=5)
        ttk.Button(self, text="Appointments", command=self.not_implemented).pack(pady=5)
        ttk.Button(self, text="Notifications", command=self.not_implemented).pack(pady=5)
        ttk.Button(self, text="Go Back", command=lambda: controller.show_frame("RoleSelectionScreen")).pack(pady=10)

    def not_implemented(self):
        messagebox.showinfo("Info", "Not implemented yet.")

class Prescriptions(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.title("Prescriptions")

        ttk.Label(self, text="Patient: Prescriptions", font=("Helvetica", 16)).pack(pady=10)

        table_frame = ttk.Frame(self)
        table_frame.pack(pady=10)

        headers = ["Name", "Dosage", "Duration", "By Doctor (name)"]
        for i, header in enumerate(headers):
            ttk.Label(table_frame, text=header, font=("Helvetica", 10, "bold"), width=15).grid(row=0, column=i, padx=1, pady=1)

        for row in range(1, 6):
            for col in range(len(headers)):
                ttk.Label(table_frame, text="", width=15).grid(row=row, column=col, padx=1, pady=1)

        ttk.Button(self, text="Go Back", command=lambda: controller.show_frame("PatientMainScreen")).pack(side="left", pady=20, padx=20)
        ttk.Button(self, text="More", command=self.not_implemented).pack(side="right", pady=20, padx=20)

    def not_implemented(self):
        messagebox.showinfo("Info", "Not implemented yet.")

class PatientInformation(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.controller.title("Personal Data")

        ttk.Label(self, text="Name").pack(pady=2)
        self.name_entry = ttk.Entry(self)
        self.name_entry.pack(pady=2)

        ttk.Label(self, text="Surname").pack(pady=2)
        self.surname_entry = ttk.Entry(self)
        self.surname_entry.pack(pady=2)

        ttk.Label(self, text="Gender").pack(pady=2)
        self.gender_var = tk.StringVar()
        self.male_check = ttk.Radiobutton(self, text="Male", variable=self.gender_var, value="Male")
        self.female_check = ttk.Radiobutton(self, text="Female", variable=self.gender_var, value="Female")
        self.male_check.pack(pady=2)
        self.female_check.pack(pady=2)

        ttk.Label(self, text="Age").pack(pady=2)
        self.age_entry = ttk.Entry(self)
        self.age_entry.pack(pady=2)

        ttk.Label(self, text="Weight").pack(pady=2)
        self.weight_entry = ttk.Entry(self)
        self.weight_entry.pack(pady=2)

        ttk.Label(self, text="Height").pack(pady=2)
        self.height_entry = ttk.Entry(self)
        self.height_entry.pack(pady=2)

        ttk.Button(self, text="Modify", command=self.modify_data).pack(pady=5)
        ttk.Button(self, text="Go Back", command=lambda: controller.show_frame("PatientMainScreen")).pack(pady=10)
        
        # Delete button
        delete_button = ttk.Button(self, text="Delete User", command=self.delete_patient)
        delete_button.pack(pady=5)
        delete_button.config(style="Red.TButton")

        style = ttk.Style()
        style.configure("Red.TButton", foreground="#8B0000", font=("Helvetica", 10, "bold"))

    def load_data(self):
        data = getattr(self.controller, "current_user_data", {})
        self.name_entry.delete(0, tk.END)
        self.surname_entry.delete(0, tk.END)
        self.gender_var.set("")
        self.age_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.height_entry.delete(0, tk.END)
        
        try:
            self.name_entry.insert(0, self.controller.current_user_data.get("name"))
            self.surname_entry.insert(0, self.controller.current_user_data.get("surname"))
            self.gender_var.set(self.controller.current_user_data.get("gender"))
            self.age_entry.insert(0, self.controller.current_user_data.get("age"))
            self.weight_entry.insert(0, self.controller.current_user_data.get("weight"))
            self.height_entry.insert(0, self.controller.current_user_data.get("height"))
        except AttributeError:
            messagebox.showerror("Error", "Data not found. You are using a test account. Please login with a valid account.")

    def modify_data(self):
        if self.controller.current_user_data is None:
            messagebox.showerror("Error", "Data not found. You are using a test account. Please login with a valid account.")
            return
        try:
            for patient in self.controller.hospital.patients:
                if patient.personal_id == self.controller.current_user:
                    
                    patient.set_info("name", self.name_entry.get(), 'str')
                    patient.set_info("surname", self.surname_entry.get(), 'str')
                    patient.set_info("gender", self.gender_var.get(), 'str')
                    patient.set_info("age", self.controller.hospital.validate_value(self.age_entry.get(), int, 0, 150, custom_message_incorrect_type="The age is a number...", custom_message_lower="The age must be a positive number.", custom_message_upper="I don't think you are that old."),'int')
                    patient.set_info("weight", self.controller.hospital.validate_value(self.weight_entry.get(), float, 0, 1000, custom_message_incorrect_type="The weight must be a number...", custom_message_lower="The weight must be a positive number.", custom_message_upper="Did you know that the heaviest person ever recorded was 635 kg?, either you are lying or you are a record breaker."), 'float')
                    patient.set_info("height", self.controller.hospital.validate_value(self.height_entry.get(), float, 0, 300, custom_message_incorrect_type="The height must be a number...", custom_message_lower="The height must be a positive number.", custom_message_upper="Are you human or giraffe?"), 'float')
                
                    self.controller.current_user_data = patient
                
                    messagebox.showinfo("Info", "Data updated successfully")
            self.controller.show_frame("PatientMainScreen")
        except ValueError as e:
            messagebox.showerror("Error", e)
        
    def delete_patient(self):
        message = "Are you sure you want to delete your account?"
        if messagebox.askyesno("Warning", message):
            try:
                self.controller.hospital.remove_patient(self.controller.current_user)
                messagebox.showinfo("Info", "Account deleted successfully")
            except TypeError:
                messagebox.showerror("Error", "There is no data to delete since you are using a test account.")
            
    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.load_data()

class MedidataHubUI(tk.Tk):
    def __init__(self, hospital = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Hospital Management System")
        self.resizable(True, True)
        self.selected_role = None
        self.current_user = None
        self.current_user_data = None
        self.hospital = hospital

        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in (
            RoleSelectionScreen, LoginScreenPatient, LoginScreenDoctor, RegisterScreenPatient, RegisterScreenDoctor, PatientMainScreen, DoctorMainScreen, Prescriptions, PatientInformation
        ):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("RoleSelectionScreen")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
