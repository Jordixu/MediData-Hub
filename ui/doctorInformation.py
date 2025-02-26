from tkinter import messagebox
import tkinter as tk
import datetime as dt
import customtkinter as ctk
from tkcalendar import DateEntry
from tkinter import ttk  # Importing ttk

class DoctorInformation(ctk.CTkFrame):
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
        ctk.CTkLabel(info_frame, text="Social Security Number").pack(pady=2)
        self.ssn_entry = ctk.CTkEntry(info_frame, state="readonly")
        self.ssn_entry.pack(pady=2)

        # Vertical Separator
        separator = ttk.Separator(center_frame, orient='vertical')
        separator.grid(row=0, column=1, rowspan=2, sticky="ns", padx=10)

        # Modify Frame
        modify_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        modify_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        
        top_spacer = ctk.CTkFrame(modify_frame, height=140, fg_color="transparent")
        top_spacer.pack()

        ctk.CTkLabel(modify_frame, text="Name").pack(pady=2)
        self.name_entry = ctk.CTkEntry(modify_frame, state="readonly")
        self.name_entry.pack(pady=2)

        ctk.CTkLabel(modify_frame, text="Surname").pack(pady=2)
        self.surname_entry = ctk.CTkEntry(modify_frame, state="readonly")
        self.surname_entry.pack(pady=2)

        ctk.CTkLabel(modify_frame, text="Gender").pack(pady=2)
        gender_frame = ctk.CTkFrame(modify_frame)
        gender_frame.pack(pady=2)
        self.gender_var = tk.StringVar()
        self.male_check = ctk.CTkRadioButton(gender_frame, text="Male", variable=self.gender_var, value="Male", state="readonly").grid(row=0, column=0)
        self.female_check = ctk.CTkRadioButton(gender_frame, text="Female", variable=self.gender_var, value="Female", state="readonly").grid(row=0, column=1)

        ctk.CTkLabel(modify_frame, text="Birthday").pack(pady=2)
        self.birthday_entry = DateEntry(modify_frame, width=20, borderwidth=2, font=('Helvetica', 12), date_pattern='dd/MM/yyyy', state="readonly")
        self.birthday_entry.pack(pady=2)


        spacer_frame = ctk.CTkFrame(modify_frame, height=10, fg_color="transparent")
        spacer_frame.pack()

        ctk.CTkButton(modify_frame, text="Go Back", command=lambda: controller.show_frame("DoctorMainScreen")).pack(pady=10)

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
        self.gender_var.set("")
        self.birthday_entry.set_date(dt.datetime.now())

        
        try:
            self.personal_id_entry.configure(state="normal")
            self.personal_id_entry.delete(0, tk.END)
            self.personal_id_entry.insert(0, self.controller.current_user_data.get_protected_attribute("personal_id"))
            self.personal_id_entry.configure(state="readonly")
            
            self.hospital_id_entry.configure(state="normal")
            self.hospital_id_entry.delete(0, tk.END)
            self.hospital_id_entry.insert(0, self.controller.current_user_data.get_protected_attribute("hospital_id"))
            self.hospital_id_entry.configure(state="readonly")
            
            self.name_entry.configure(state="normal")
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, self.controller.current_user_data.get_protected_attribute("name"))
            self.name_entry.configure(state="readonly")
            
            self.surname_entry.configure(state="normal")
            self.surname_entry.delete(0, tk.END)
            self.surname_entry.insert(0, self.controller.current_user_data.get_protected_attribute("surname"))
            self.surname_entry.configure(state="readonly")
            
            self.gender_var.set(self.controller.current_user_data.get_protected_attribute("gender"))
            birthday_str = self.controller.current_user_data.get_protected_attribute("birthday")
            birthday_date = dt.datetime.strptime(birthday_str, "%Y-%m-%d").date() if isinstance(birthday_str, str) else birthday_str
            self.birthday_entry.set_date(birthday_date)
            
            self.ssn_entry.configure(state="normal")
            self.ssn_entry.delete(0, tk.END)
            self.ssn_entry.insert(0, self.controller.current_user_data.get("socialsecurity"))
            self.ssn_entry.configure(state="readonly")

        except AttributeError as exc:
            messagebox.showerror("Error", exc)
            
    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.load_data()
        
    def not_implemented(self):
        messagebox.showinfo("Info", "Not implemented yet.")

if __name__ == "__main__":
    root = ctk.CTk()
    ctk.set_appearance_mode("light")
    container = DoctorInformation(root, None)
    container.pack(expand=True, fill="both")
    root.mainloop()