from tkinter import messagebox
import tkinter as tk
import datetime as dt
import customtkinter as ctk
from tkcalendar import DateEntry
from tkinter import ttk  # Importing ttk

class PatientInformation(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Personal Data"

        # Main container
        container_frame = ctk.CTkFrame(self, fg_color="transparent")
        container_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Center Frame to hold info and modify frames
        center_frame = ctk.CTkFrame(container_frame, fg_color="transparent")
        center_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        # Info Frame
        info_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        info_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        top_spacer = ctk.CTkFrame(info_frame, height=140, fg_color="transparent")
        top_spacer.pack()

        ctk.CTkLabel(info_frame, text="User Personal ID").pack(pady=2)
        self.personal_id_entry = ctk.CTkEntry(info_frame, state="readonly")
        self.personal_id_entry.pack(pady=2)
        ctk.CTkLabel(info_frame, text="User Hospital ID").pack(pady=2)
        self.hospital_id_entry = ctk.CTkEntry(info_frame, state="readonly")
        self.hospital_id_entry.pack(pady=2)

        # Password Frame
        password_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        password_frame.pack(pady=10)
        ctk.CTkButton(password_frame, text="Change Password", command=lambda: controller.show_frame("PatientChangePassword")).pack(pady=5)

        # Vertical Separator
        separator = ttk.Separator(center_frame, orient='vertical')
        separator.grid(row=0, column=1, rowspan=2, sticky="ns", padx=10)

        # Modify Frame
        modify_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        modify_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(modify_frame, text="Name").pack(pady=2)
        self.name_entry = ctk.CTkEntry(modify_frame)
        self.name_entry.pack(pady=2)

        ctk.CTkLabel(modify_frame, text="Surname").pack(pady=2)
        self.surname_entry = ctk.CTkEntry(modify_frame)
        self.surname_entry.pack(pady=2)

        ctk.CTkLabel(modify_frame, text="Gender").pack(pady=2)
        gender_frame = ctk.CTkFrame(modify_frame)
        gender_frame.pack(pady=2)
        self.gender_var = tk.StringVar()
        self.male_check = ctk.CTkRadioButton(gender_frame, text="Male", variable=self.gender_var, value="Male").grid(row=0, column=0)
        self.female_check = ctk.CTkRadioButton(gender_frame, text="Female", variable=self.gender_var, value="Female").grid(row=0, column=1)

        ctk.CTkLabel(modify_frame, text="Birthday").pack(pady=2)
        self.birthday_entry = DateEntry(modify_frame, width=20, borderwidth=2, font=('Helvetica', 12), date_pattern='dd/MM/yyyy')
        self.birthday_entry.pack(pady=2)

        ctk.CTkLabel(modify_frame, text="Weight (in kg)").pack(pady=2)
        self.weight_entry = ctk.CTkEntry(modify_frame)
        self.weight_entry.pack(pady=2)

        ctk.CTkLabel(modify_frame, text="Height (in cm)").pack(pady=2)
        self.height_entry = ctk.CTkEntry(modify_frame)
        self.height_entry.pack(pady=2)

        spacer_frame = ctk.CTkFrame(modify_frame, height=10, fg_color="transparent")
        spacer_frame.pack()

        ctk.CTkButton(modify_frame, text="Modify", command=self.modify_data).pack(pady=5)
        ctk.CTkButton(modify_frame, text="Go Back", command=lambda: controller.show_frame("PatientMainScreen")).pack(pady=10)
        delete_button = ctk.CTkButton(modify_frame, text="Delete User", fg_color="#8B0000", command=self.delete_patient)
        delete_button.pack(pady=5)

        # Configure grid weights for centering
        container_frame.grid_columnconfigure(0, weight=1)
        container_frame.grid_columnconfigure(1, weight=1)
        container_frame.grid_columnconfigure(2, weight=1)
        container_frame.grid_rowconfigure(0, weight=1)
        container_frame.grid_rowconfigure(1, weight=1)
        container_frame.grid_rowconfigure(2, weight=1)

        center_frame.grid_rowconfigure(0, weight=1)
        center_frame.grid_rowconfigure(1, weight=1)
        center_frame.grid_columnconfigure(0, weight=1)
        center_frame.grid_columnconfigure(1, weight=1)
        center_frame.grid_columnconfigure(2, weight=1)

    def load_data(self):
        self.name_entry.delete(0, tk.END)
        self.surname_entry.delete(0, tk.END)
        self.gender_var.set("")
        self.weight_entry.delete(0, tk.END)
        self.height_entry.delete(0, tk.END)
        
        try:
            self.personal_id_entry.configure(state="normal")
            self.personal_id_entry.delete(0, tk.END)
            self.personal_id_entry.insert(0, self.controller.current_user_data.get_protected_attribute("personal_id"))
            self.personal_id_entry.configure(state="readonly")
            
            self.hospital_id_entry.configure(state="normal")
            self.hospital_id_entry.delete(0, tk.END)
            self.hospital_id_entry.insert(0, self.controller.current_user_data.get_protected_attribute("hospital_id"))
            self.hospital_id_entry.configure(state="readonly")
            
            self.name_entry.insert(0, self.controller.current_user_data.get_protected_attribute("name"))
            self.surname_entry.insert(0, self.controller.current_user_data.get_protected_attribute("surname"))
            self.gender_var.set(self.controller.current_user_data.get_protected_attribute("gender"))
            birthday_str = self.controller.current_user_data.get_protected_attribute("birthday")
            birthday_date = dt.datetime.strptime(birthday_str, "%Y-%m-%d").date() if isinstance(birthday_str, str) else birthday_str
            self.birthday_entry.set_date(birthday_date)
            self.weight_entry.insert(0, self.controller.current_user_data.get("weight"))
            self.height_entry.insert(0, self.controller.current_user_data.get("height"))

        except AttributeError as exc:
            messagebox.showerror("Error", exc)

    def modify_data(self):
        if self.controller.current_user_data is None:
            messagebox.showerror("Error", "Data not found. You are using a test account.")
            return
        try:
            patient = self.controller.current_user_data
            patient.set_protected_info("name", self.name_entry.get(), 'str')
            patient.set_protected_info("surname", self.surname_entry.get(), 'str')
            patient.set_protected_info("gender", self.gender_var.get(), 'str')
            if not (dt.date(1900, 1, 1) <= self.birthday_entry.get_date() <= dt.date.today()):
                raise ValueError("I don't think you were born in the future or in the 19th century...")
            patient.set_protected_info("birthday", self.birthday_entry.get_date(), 'date')
            patient.set_private_info("weight", self.controller.hospital.validate_value(
                self.weight_entry.get(), float, 0, 1000,
                custom_message_incorrect_type="The weight must be a number...",
                custom_message_lower="The weight must be a positive number.",
                custom_message_upper="Did you know that the heaviest person ever recorded was 635 kg?"), 'float')
            patient.set_private_info("height", self.controller.hospital.validate_value(
                self.height_entry.get(), float, 0, 300,
                custom_message_incorrect_type="The height must be a number...",
                custom_message_lower="The height must be a positive number.",
                custom_message_upper="Are you human or giraffe?"), 'float')

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
                self.controller.show_frame("RoleSelectionScreen")
            except TypeError:
                messagebox.showerror("Error", "There is no data to delete since you are using a test account.")
            except ValueError as e:
                messagebox.showerror("Error", e)
            
    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.load_data()
        
    def not_implemented(self):
        messagebox.showinfo("Info", "Not implemented yet.")


# if __name__ == "__main__":
#     root = ctk.CTk()
#     ctk.set_appearance_mode("light")
#     container = PatientInformation(root, None)
#     container.pack(expand=True, fill="both")
#     root.mainloop()