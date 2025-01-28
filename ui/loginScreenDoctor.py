from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk

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
        id = self.user_entry.get()
        password = self.pass_entry.get()
        if role == "doctor":
            for doctor in self.controller.hospital.doctors:
                if int(doctor.get_protected_info("personal_id")) == int(id) or int(doctor.get_protected_info("hospital_id")) == int(id):
                    if doctor.check_password(password):
                        self.controller.current_user = int(doctor.hospital_id)
                        self.controller.current_user_data = doctor
                        self.clear_entries()
                        self.controller.show_frame("DoctorMainScreen")
                    return
            messagebox.showerror("Error", "Invalid user or password")
        messagebox.showerror("Error", "Role not supported")