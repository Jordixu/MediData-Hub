import tkinter as tk 
from tkinter import messagebox
from tkinter import ttk
import customtkinter as ctk

class PatientChangePassword(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Change Password"

        # Main container
        container_frame = ctk.CTkFrame(self, fg_color="transparent")
        container_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Center Frame to hold modify frames
        center_frame = ctk.CTkFrame(container_frame, fg_color="transparent")
        center_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        top_spacer = ctk.CTkFrame(center_frame, height=140, fg_color="transparent")
        top_spacer.pack()
        
        # Modify Frame
        modify_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        modify_frame.pack(expand=True, fill="both", padx=10, pady=10)

        ctk.CTkLabel(modify_frame, text="Old Password").pack(pady=2)
        self.old_password_entry = ctk.CTkEntry(modify_frame, show="*")
        self.old_password_entry.pack(pady=2)
        
        ctk.CTkLabel(modify_frame, text="New Password").pack(pady=2)
        self.new_password_entry = ctk.CTkEntry(modify_frame, show="*")
        self.new_password_entry.pack(pady=2)
        
        ctk.CTkLabel(modify_frame, text="Confirm New Password").pack(pady=2)
        self.confirm_password_entry = ctk.CTkEntry(modify_frame, show="*")
        self.confirm_password_entry.pack(pady=2)
        
        ctk.CTkButton(modify_frame, text="Change Password", command=self.change_password).pack(pady=10)
        
        ctk.CTkButton(self, text="Go Back", width=220, height=40, command=lambda: controller.show_frame("PatientInformation")).pack(pady=20)
        
    def change_password(self):
        old_password = self.old_password_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        if not old_password or not new_password or not confirm_password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        if new_password != confirm_password:
            messagebox.showerror("Error", "New passwords do not match.")
            return
        
        if not self.controller.current_user_data:
            messagebox.showerror("Error", "No user data found. Your are using a test account.")
            return
        
        if not self.controller.current_user_data.check_password(old_password):
            messagebox.showerror("Error", "Old password is incorrect.")
            return
        
        self.controller.current_user_data.set_protected_info("password", new_password, 'str')

        print(self.controller.current_user_data.get_protected_attribute("password"))
        messagebox.showinfo("Success", "Password changed successfully.")
        
        self.old_password_entry.delete(0, "end")
        self.new_password_entry.delete(0, "end")
        self.confirm_password_entry.delete(0, "end")

        self.controller.show_frame("PatientInformation")
        
# if __name__ == "__main__":
#     root = ctk.CTk()
#     ctk.set_appearance_mode("light")
#     container = PatientChangePassword(root, None)
#     container.pack(expand=True, fill="both")
#     root.mainloop()