from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk

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
            except ValueError as e:
                messagebox.showerror("Error", e)
            
    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.load_data()