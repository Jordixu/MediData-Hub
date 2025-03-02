import tkinter as tk 
from tkinter import messagebox
from tkinter import ttk
import customtkinter as ctk

class ChangePassword(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Change Password"
        
        # Configure the main layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Title
        self.grid_rowconfigure(1, weight=1)  # Form content
        self.grid_rowconfigure(2, weight=0)  # Buttons
        
        # Title
        title_label = ctk.CTkLabel(
            self, 
            text="Change Password", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=(30, 20))
        
        # Main content container
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=1, column=0, padx=20, sticky="n")
        
        # Password change form
        form_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        form_frame.pack(padx=20, pady=20)
        
        # Old Password field
        ctk.CTkLabel(form_frame, text="Old Password", anchor="w").pack(anchor="w", pady=(5, 2))
        self.old_password_entry = ctk.CTkEntry(
            form_frame, 
            width=350, 
            height=35,
            show="•",
            font=ctk.CTkFont(size=14)
        )
        self.old_password_entry.pack(pady=(0, 15), fill="x")
        
        # New Password field
        ctk.CTkLabel(form_frame, text="New Password", anchor="w").pack(anchor="w", pady=(5, 2))
        self.new_password_entry = ctk.CTkEntry(
            form_frame, 
            width=350, 
            height=35,
            show="•",
            font=ctk.CTkFont(size=14)
        )
        self.new_password_entry.pack(pady=(0, 15), fill="x")
        
        # Confirm New Password field
        ctk.CTkLabel(form_frame, text="Confirm New Password", anchor="w").pack(anchor="w", pady=(5, 2))
        self.confirm_password_entry = ctk.CTkEntry(
            form_frame, 
            width=350, 
            height=35,
            show="•",
            font=ctk.CTkFont(size=14)
        )
        self.confirm_password_entry.pack(pady=(0, 25), fill="x")
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.grid(row=2, column=0, pady=(20, 30))
        
        # Change Password button
        self.change_btn = ctk.CTkButton(
            buttons_frame, 
            text="Change Password", 
            command=self.change_password,
            width=180,
            height=40,
            fg_color="#003366",
            hover_color="#004080",
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.change_btn.pack(side="left", padx=5)
        
        # Go Back button
        self.back_btn = ctk.CTkButton(
            buttons_frame, 
            text="Cancel", 
            command=self.go_back,
            width=180,
            height=40,
            fg_color="#555555",
            hover_color="#666666",
            font=ctk.CTkFont(size=15)
        )
        self.back_btn.pack(side="left", padx=5)
        
    def change_password(self):
        old_password = self.old_password_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        # Validate inputs
        if not old_password or not new_password or not confirm_password:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        if new_password != confirm_password:
            messagebox.showerror("Error", "New passwords do not match.")
            return
        
        # Check if user data exists
        if not self.controller.current_user_data:
            messagebox.showerror("Error", "No user data found. You are using a test account.")
            return
        
        # Verify old password
        if not self.controller.current_user_data.check_password(old_password):
            messagebox.showerror("Error", "Old password is incorrect.")
            return
        
        # Update password
        try:
            self.controller.current_user_data.set_protected_info("password", new_password, 'str')
            messagebox.showinfo("Success", "Password changed successfully.")
            
            # Clear form fields
            self.old_password_entry.delete(0, "end")
            self.new_password_entry.delete(0, "end")
            self.confirm_password_entry.delete(0, "end")
            
            # Return to appropriate screen
            self.go_back()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to change password: {str(e)}")
    
    def go_back(self):
        """Navigate back to the appropriate screen based on user role"""
        role = self.controller.selected_role
        
        if role == "patient":
            self.controller.show_frame("PatientInformation")
        elif role == "doctor":
            self.controller.show_frame("DoctorInformation")
        elif role == "admin":
            self.controller.show_frame("AdminInformation")
        else:
            # Fallback to role selection if role is unknown
            self.controller.show_frame("RoleSelectionScreen")
    
    def tkraise(self, *args, **kwargs):
        """Clear form fields when the frame is raised"""
        super().tkraise(*args, **kwargs)
        
        self.old_password_entry.delete(0, "end")
        self.new_password_entry.delete(0, "end")
        self.confirm_password_entry.delete(0, "end")