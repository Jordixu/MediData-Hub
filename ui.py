import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

class RoleSelectionScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Role Selection"

        # Configure the grid
        for i in range(5):
            self.grid_rowconfigure(i, weight=1)
        for j in range(5):
            self.grid_columnconfigure(j, weight=1)

        # Title
        label = ctk.CTkLabel(self, text="Select Role", font=("Helvetica", 24, "bold"))
        label.grid(row=1, column=2, pady=10)

        # Buttons
        ctk.CTkButton(
            self, text="Patient",
            command=lambda: self.select_role("patient"),
            width=200
        ).grid(row=2, column=1, pady=20, padx=20)

        ctk.CTkButton(
            self, text="Doctor",
            command=lambda: self.select_role("doctor"),
            width=200
        ).grid(row=2, column=2, pady=20, padx=20)

        ctk.CTkButton(
            self, text="Administrator",
            command=self.not_implemented,
            width=200
        ).grid(row=2, column=3, pady=20, padx=20)

    def select_role(self, role):
        self.controller.selected_role = role
        if role == "patient":
            self.controller.show_frame("LoginScreenPatient")
        elif role == "doctor":
            self.controller.show_frame("LoginScreenDoctor")

    def not_implemented(self):
        messagebox.showinfo("Info", "Not implemented yet.")

# Repeat for each widget using .pack(...) in other classes:
#   1) Call self.grid_rowconfigure(...) and self.grid_columnconfigure(...)
#   2) Replace pack(...) with grid(row=?, column=?, padx=?, pady=?)

class LoginScreenPatient(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Login Screen"

        # Test Frame (DELETE)
        title_frame = ctk.CTkFrame(self, height=20, fg_color="transparent")
        title_frame.pack(pady=10)
        bypass_label = ctk.CTkLabel(title_frame, text="Direct Navigation (Test Only)", font=("Helvetica", 16, "bold"))
        bypass_label.pack()
        ctk.CTkButton(
            title_frame, text="Go to Patient Main Screen",
            command=lambda: self.controller.show_frame("PatientMainScreen"), width=180, height=35
        ).pack(pady=5)

        # Divider
        line_frame = ctk.CTkFrame(self, height=2, fg_color="grey")
        line_frame.pack(fill="x", pady=20)

        # Credentials frame
        credentials_frame = ctk.CTkFrame(self, height=50, fg_color="transparent")
        credentials_frame.pack(pady=5)
        self.user_entry = ctk.CTkEntry(credentials_frame, width=240, height=35, placeholder_text="User (Personal or Hospital ID)")
        self.user_entry.grid(row=0, column=0, padx=10, pady=10)

        self.pass_entry = ctk.CTkEntry(credentials_frame, show="*", width=240, height=35,  placeholder_text="Password")
        self.pass_entry.grid(row=1, column=0, padx=10, pady=10)

        # Action frame
        action_frame = ctk.CTkFrame(self, fg_color="transparent", height=50)
        action_frame.pack(pady=5)
        ctk.CTkButton(
            action_frame, text="Login", command=self.login_action, width=160, height=35
        ).grid(row=0, column=0, padx=5, pady=5)
        ctk.CTkButton(
            action_frame, text="Register", command=lambda: self.controller.show_frame("RegisterScreenPatient"), 
            width=160, height=35
        ).grid(row=0, column=1, padx=5, pady=5)

        # Go Back frame
        back_frame = ctk.CTkFrame(self, fg_color="transparent")
        back_frame.pack(pady=20, fill="x")
        ctk.CTkButton(
            back_frame, text="Go Back", command=lambda: self.controller.show_frame("RoleSelectionScreen"),
            width=320, height=35
        ).pack()

    def clear_entries(self):
        self.user_entry.delete(0, tk.END)
        self.pass_entry.delete(0, tk.END)

    def login_action(self):
        role = getattr(self.controller, "selected_role", None)
        personal_id = self.user_entry.get()
        password = self.pass_entry.get()
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
        messagebox.showerror("Error", "Role not supported")

class LoginScreenDoctor(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Login Screen"

        # Test Frame (DELETE)
        title_frame = ctk.CTkFrame(self, height=20, fg_color="transparent")
        title_frame.pack(pady=10)
        bypass_label = ctk.CTkLabel(title_frame, text="Direct Navigation (Test Only)", font=("Helvetica", 16, "bold"))
        bypass_label.pack()
        ctk.CTkButton(
            title_frame, text="Go to Doctor Main Screen",
            command=lambda: self.controller.show_frame("DoctorMainScreen"), width=180, height=35
        ).pack(pady=5)

        # Divider
        line_frame = ctk.CTkFrame(self, height=2, fg_color="grey")
        line_frame.pack(fill="x", pady=20)

        # Credentials frame
        credentials_frame = ctk.CTkFrame(self, height=50, fg_color="transparent")
        credentials_frame.pack(pady=5)
        self.user_entry = ctk.CTkEntry(credentials_frame, width=240, height=35, placeholder_text="User (Personal or Hospital ID)")
        self.user_entry.grid(row=0, column=0, padx=10, pady=10)

        self.pass_entry = ctk.CTkEntry(credentials_frame, show="*", width=240, height=35,  placeholder_text="Password")
        self.pass_entry.grid(row=1, column=0, padx=10, pady=10)

        # Action frame
        action_frame = ctk.CTkFrame(self, fg_color="transparent", height=50)
        action_frame.pack(pady=5, fill="x")
        ctk.CTkButton(
            action_frame, text="Login", command=self.login_action, width=160, height=35
        ).pack()

        # Go Back frame
        back_frame = ctk.CTkFrame(self, fg_color="transparent")
        back_frame.pack(pady=20, fill="x")
        ctk.CTkButton(
            back_frame, text="Go Back", command=lambda: self.controller.show_frame("RoleSelectionScreen"),
            width=250, height=35
        ).pack()

    def clear_entries(self):
        self.user_entry.delete(0, tk.END)
        self.pass_entry.delete(0, tk.END)

    def login_action(self):
        role = getattr(self.controller, "selected_role", None)
        personal_id = self.user_entry.get()
        password = self.pass_entry.get()
        if role == "doctor":
            for doctor in self.controller.hospital.doctors:
                if int(doctor.personal_id) == int(personal_id):
                    if doctor.password == password:
                        self.controller.current_user = int(personal_id)
                        self.controller.current_user_data = doctor
                        self.controller.show_frame("DoctorMainScreen")
                        self.clear_entries()
                    return
            messagebox.showerror("Error", "Invalid user or password")
        messagebox.showerror("Error", "Role not supported")

class RegisterScreenPatient(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Register"
        
        ctk.CTkLabel(self, text="Register", font=("Helvetica", 24, "bold")).pack(pady=10)
        
        two_frames_container = ctk.CTkFrame(self, fg_color="transparent")
        two_frames_container.pack(pady=20)

        # Login Information Frame
        login_information_frame = ctk.CTkFrame(two_frames_container, fg_color="transparent")
        login_information_frame.pack(side="left", padx=50)

        ctk.CTkLabel(login_information_frame, text="Login Information", font=("Helvetica", 16)).pack(pady=5)
        ctk.CTkLabel(login_information_frame, text="User (ID)").pack(padx=5, pady=2)
        self.user_entry = ctk.CTkEntry(login_information_frame)
        self.user_entry.pack(padx=5, pady=2)

        ctk.CTkLabel(login_information_frame, text="Password").pack(padx=5, pady=2)
        self.pass_entry = ctk.CTkEntry(login_information_frame, show='*')
        self.pass_entry.pack(padx=5, pady=2)

        # Vertical Line
        line_frame = ctk.CTkFrame(two_frames_container, width=2, fg_color="grey")
        line_frame.pack(side="left", fill="y", padx=20)

        # Personal Information Frame
        personal_information_frame = ctk.CTkFrame(two_frames_container, fg_color="transparent")
        personal_information_frame.pack(side="left", padx=50)

        ctk.CTkLabel(personal_information_frame, text="Personal Information", font=("Helvetica", 16)).pack(pady=5)
        ctk.CTkLabel(personal_information_frame, text="Name").pack(padx=5, pady=2)
        self.name_entry = ctk.CTkEntry(personal_information_frame)
        self.name_entry.pack(padx=5, pady=2)

        ctk.CTkLabel(personal_information_frame, text="Surname").pack(padx=5, pady=2)
        self.surname_entry = ctk.CTkEntry(personal_information_frame)
        self.surname_entry.pack(padx=5, pady=2)

        ctk.CTkLabel(personal_information_frame, text="Gender").pack(pady=2)
        gender_frame = ctk.CTkFrame(personal_information_frame, fg_color="transparent")
        gender_frame.pack(pady=2)
        self.gender_var = tk.StringVar()
        ctk.CTkRadioButton(gender_frame, text="Male", variable=self.gender_var, value="Male").grid(row=0, column=0)
        ctk.CTkRadioButton(gender_frame, text="Female", variable=self.gender_var, value="Female").grid(row=0, column=1)

        ctk.CTkLabel(personal_information_frame, text="Age").pack(padx=5, pady=2)
        self.age_entry = ctk.CTkEntry(personal_information_frame)
        self.age_entry.pack(padx=5, pady=2)

        ctk.CTkLabel(personal_information_frame, text="Weight (in kg)").pack(padx=5, pady=2)
        self.weight_entry = ctk.CTkEntry(personal_information_frame)
        self.weight_entry.pack(padx=5, pady=2)

        ctk.CTkLabel(personal_information_frame, text="Height (in cm)").pack(padx=5, pady=2)
        self.height_entry = ctk.CTkEntry(personal_information_frame)
        self.height_entry.pack(padx=5, pady=2)

        # Buttons below both frames
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(pady=20)
        ctk.CTkButton(buttons_frame, text="Submit", command=self.submit_data).pack(side="left", padx=5)
        ctk.CTkButton(buttons_frame, text="Go Back", command=lambda: controller.show_frame("LoginScreenPatient")).pack(side="left", padx=5)
        
    def clear_entries(self):
        self.user_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.surname_entry.delete(0, tk.END)
        self.gender_var.set("")
        self.age_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.height_entry.delete(0, tk.END)
        self.pass_entry.delete(0, tk.END)

    def submit_data(self):
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

class PatientMainScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Patient Main Screen"

        ctk.CTkLabel(self, text="Patient Main Screen", font=("Helvetica", 24)).pack(pady=20)

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=10)
        ctk.CTkButton(button_frame, text="Personal Data", width=200,
            command=lambda: controller.show_frame("PatientInformation")).grid(row=0, column=0, padx=10, pady=10)
        ctk.CTkButton(button_frame, text="Prescriptions", width=200,
            command=lambda: controller.show_frame("Prescriptions")).grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkButton(button_frame, text="Appointments", width=200,
            command=self.not_implemented).grid(row=1, column=0, padx=10, pady=10)
        ctk.CTkButton(button_frame, text="Notifications", width=200,
            command=self.not_implemented).grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkButton(self, text="Go Back", command=lambda: controller.show_frame("RoleSelectionScreen")).pack(pady=20)

    def not_implemented(self):
        messagebox.showinfo("Info", "Not implemented yet.")
        


class DoctorMainScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Doctor Main Screen"

        ctk.CTkLabel(self, text="Doctor Main Screen", font=("Helvetica", 16)).pack(pady=10)

        ctk.CTkButton(self, text="Prescriptions", command=self.not_implemented).pack(pady=5)
        ctk.CTkButton(self, text="Appointments", command=self.not_implemented).pack(pady=5)
        ctk.CTkButton(self, text="Notifications", command=self.not_implemented).pack(pady=5)
        ctk.CTkButton(self, text="Go Back", command=lambda: controller.show_frame("RoleSelectionScreen")).pack(pady=10)

    def not_implemented(self):
        messagebox.showinfo("Info", "Not implemented yet.")

class Prescriptions(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Prescriptions"

        ctk.CTkLabel(self, text="Patient: Prescriptions", font=("Helvetica", 16)).pack(pady=10)

        table_frame = ctk.CTkFrame(self)
        table_frame.pack(pady=10)

        headers = ["Name", "Dosage", "Duration", "By Doctor (name)"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(table_frame, text=header, font=("Helvetica", 10, "bold"), width=100).grid(row=0, column=i, padx=1, pady=1)

        for row in range(1, 6):
            for col in range(len(headers)):
                ctk.CTkLabel(table_frame, text="", width=100).grid(row=row, column=col, padx=1, pady=1)

        ctk.CTkButton(self, text="Go Back", command=lambda: controller.show_frame("PatientMainScreen")).pack(side="left", pady=20, padx=20)
        ctk.CTkButton(self, text="More", command=self.not_implemented).pack(side="right", pady=20, padx=20)

    def not_implemented(self):
        messagebox.showinfo("Info", "Not implemented yet.")

class PatientInformation(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Personal Data"

        ctk.CTkLabel(self, text="Name").pack(pady=2)
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.pack(pady=2)

        ctk.CTkLabel(self, text="Surname").pack(pady=2)
        self.surname_entry = ctk.CTkEntry(self)
        self.surname_entry.pack(pady=2)
        
        ctk.CTkLabel(self, text="Gender").pack(pady=2)
        gender_frame = ctk.CTkFrame(self, fg_color="transparent")
        gender_frame.pack(pady=2)
        self.gender_var = tk.StringVar()
        self.male_check = ctk.CTkRadioButton(gender_frame, text="Male", variable=self.gender_var, value="Male").grid(row=0, column=0)
        self.female_check = ctk.CTkRadioButton(gender_frame, text="Female", variable=self.gender_var, value="Female").grid(row=0, column=1)

        ctk.CTkLabel(self, text="Age").pack(pady=2)
        self.age_entry = ctk.CTkEntry(self)
        self.age_entry.pack(pady=2)

        ctk.CTkLabel(self, text="Weight in kg").pack(pady=2)
        self.weight_entry = ctk.CTkEntry(self)
        self.weight_entry.pack(pady=2)

        ctk.CTkLabel(self, text="Height (in cm)").pack(pady=2)
        self.height_entry = ctk.CTkEntry(self)
        self.height_entry.pack(pady=2)
        
        spacer_frame = ctk.CTkFrame(self, fg_color="transparent", height=10)
        spacer_frame.pack()

        ctk.CTkButton(self, text="Modify", command=self.modify_data).pack(pady=5)
        ctk.CTkButton(self, text="Go Back", command=lambda: controller.show_frame("PatientMainScreen")).pack(pady=10)
        
        delete_button = ctk.CTkButton(self, text="Delete User", fg_color=("gray75", "red"), command=self.delete_patient)
        delete_button.pack(pady=5)

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
            messagebox.showerror("Error", "Data not found. You are using a test account.")
            return
        try:
            for patient in self.controller.hospital.patients:
                if patient.personal_id == self.controller.current_user:
                    patient.set_info("name", self.name_entry.get(), 'str')
                    patient.set_info("surname", self.surname_entry.get(), 'str')
                    patient.set_info("gender", self.gender_var.get(), 'str')
                    patient.set_info("age", self.controller.hospital.validate_value(
                        self.age_entry.get(), int, 0, 150,
                        custom_message_incorrect_type="The age is a number...",
                        custom_message_lower="The age must be a positive number.",
                        custom_message_upper="I don't think you are that old."),'int')
                    patient.set_info("weight", self.controller.hospital.validate_value(
                        self.weight_entry.get(), float, 0, 1000,
                        custom_message_incorrect_type="The weight must be a number...",
                        custom_message_lower="The weight must be a positive number.",
                        custom_message_upper="Did you know that the heaviest person ever recorded was 635 kg?"), 'float')
                    patient.set_info("height", self.controller.hospital.validate_value(
                        self.height_entry.get(), float, 0, 300,
                        custom_message_incorrect_type="The height must be a number...",
                        custom_message_lower="The height must be a positive number.",
                        custom_message_upper="Are you human or giraffe?"), 'float')
                
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

class MedidataHubUI(ctk.CTk):
    def __init__(self, hospital=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Hospital Management System")
        self.selected_role = None
        self.current_user = None
        self.current_user_data = None
        self.hospital = hospital
        self.geometry("800x600")

        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("theme.json")
        
        self.frames = {}
        for F in (
            RoleSelectionScreen, LoginScreenPatient, RegisterScreenPatient, LoginScreenDoctor, PatientMainScreen,DoctorMainScreen, Prescriptions, PatientInformation
        ):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("RoleSelectionScreen")

    def show_frame(self, name):
        frame = self.frames[name]
        self.title(frame.title)
        frame.tkraise()
