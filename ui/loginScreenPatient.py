from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk

class LoginScreenPatient(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Login Screen"
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=6)
        self.grid_rowconfigure(2, weight=2)
        
        header_label = ctk.CTkLabel(
            self, 
            text="Patient Login", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        header_label.grid(row=0, column=0, sticky="s", pady=(80, 20))
        
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="n")
        
        id_label = ctk.CTkLabel(
            content_frame, 
            text="Personal ID:", 
            anchor="w",
            font=ctk.CTkFont(size=16)
        )
        id_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.user_entry = ctk.CTkEntry(
            content_frame, 
            width=400,
            height=40,
            font=ctk.CTkFont(size=16)
        )
        self.user_entry.grid(row=1, column=0, pady=(0, 25))
        
        pass_label = ctk.CTkLabel(
            content_frame, 
            text="Password:", 
            anchor="w",
            font=ctk.CTkFont(size=16)
        )
        pass_label.grid(row=2, column=0, sticky="w", pady=(0, 5))
        
        self.pass_entry = ctk.CTkEntry(
            content_frame, 
            width=400,
            height=40,
            show="•",
            font=ctk.CTkFont(size=16)
        )
        self.pass_entry.grid(row=3, column=0, pady=(0, 35))
        
        buttons_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        buttons_frame.grid(row=4, column=0)
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
        
        login_btn = ctk.CTkButton(
            buttons_frame, 
            text="Login", 
            command=self.login_action, 
            width=190,
            height=45,
            fg_color="#003366",
            hover_color="#004080",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        login_btn.grid(row=0, column=0, padx=5)
        
        register_btn = ctk.CTkButton(
            buttons_frame, 
            text="Register", 
            command=lambda: self.controller.show_frame("RegisterScreenPatient"), 
            width=190,
            height=45,
            fg_color="#003366",
            hover_color="#004080",
            font=ctk.CTkFont(size=16)
        )
        register_btn.grid(row=0, column=1, padx=5)
        
        content_frame.grid_rowconfigure(5, minsize=40)
        
        back_btn = ctk.CTkButton(
            content_frame, 
            text="← Back to Role Selection", 
            command=lambda: self.controller.show_frame("RoleSelectionScreen"),
            width=400,
            height=40,
            fg_color="transparent", 
            border_width=1,
            border_color="#aaaaaa",
            text_color="#555555",
            hover_color="#eeeeee",
            font=ctk.CTkFont(size=16)
        )
        back_btn.grid(row=6, column=0, pady=(10, 0))

    def clear_entries(self):
        self.user_entry.delete(0, tk.END)
        self.pass_entry.delete(0, tk.END)

    def login_action(self):
        role = getattr(self.controller, "selected_role", None)
        id = self.user_entry.get()
        password = self.pass_entry.get()
        if all([id, password]):
            if role == "patient":
                for patient in self.controller.hospital.patients.values():
                    if int(patient.get_protected_attribute("personal_id")) == int(id):
                        if patient.check_password(str(password)):
                            self.controller.current_user = int(patient.get_protected_attribute("hospital_id"))
                            self.controller.current_user_data = patient
                            self.clear_entries()
                            self.controller.show_frame("PatientMainScreen")
                            return
                messagebox.showerror("Error", "Invalid user or password")
                return
            messagebox.showerror("Error", "Role not supported")
            return
        messagebox.showerror("Error", "Please fill all fields")
