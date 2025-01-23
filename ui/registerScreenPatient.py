from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk

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