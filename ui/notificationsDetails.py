import customtkinter as ctk
from tkinter import ttk, messagebox
import datetime as dt

class NotificationsDetails(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Notification Details"
        
        # Configure the main layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Content
        self.grid_rowconfigure(2, weight=0)  # Footer/buttons
        
        # Header with title
        header_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(20, 0))
        
        title_label = ctk.CTkLabel(
            header_frame, 
            text="Notification Details", 
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#262850"
        )
        title_label.pack(pady=15)
        
        # Main content area
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=1, column=0, padx=30, pady=20, sticky="nsew")
        
        # Notification title section
        title_section = ctk.CTkFrame(content_frame, fg_color="transparent")
        title_section.pack(fill="x", pady=(0, 20))
        
        title_header = ctk.CTkLabel(
            title_section, 
            text="Title", 
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        title_header.pack(anchor="w", pady=(0, 5))
        
        self.title_entry = ctk.CTkEntry(
            title_section, 
            height=40,
            font=ctk.CTkFont(size=14),
            state='disabled',
            border_width=1,
            corner_radius=6
        )
        self.title_entry.pack(fill="x")
        
        # Notification date/sender info
        info_section = ctk.CTkFrame(content_frame, fg_color="#f0f5fa", corner_radius=6)
        info_section.pack(fill="x", pady=(0, 20))
        
        self.info_label = ctk.CTkLabel(
            info_section,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#555555"
        )
        self.info_label.pack(anchor="w", padx=10, pady=10)
        
        # Notification message section
        message_section = ctk.CTkFrame(content_frame, fg_color="transparent")
        message_section.pack(fill="both", expand=True)
        
        message_header = ctk.CTkLabel(
            message_section, 
            text="Message", 
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        message_header.pack(anchor="w", pady=(0, 5))
        
        self.message_textbox = ctk.CTkTextbox(
            message_section, 
            font=ctk.CTkFont(size=14),
            corner_radius=6,
            border_width=1,
            wrap="word",
            state='disabled'
        )
        self.message_textbox.pack(fill="both", expand=True)
        
        # Button section
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=2, column=0, pady=20)
        
        # Mark as read button - created but not packed yet
        self.mark_read_button = ctk.CTkButton(
            self.button_frame,
            text="Mark as Read",
            command=self.mark_as_read,
            width=150,
            height=40,
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=ctk.CTkFont(size=14)
        )
        
        # Back button - always shown
        self.back_button = ctk.CTkButton(
            self.button_frame,
            text="Go Back",
            command=self.go_back,
            width=150,
            height=40,
            fg_color="#555555",
            hover_color="#666666",
            font=ctk.CTkFont(size=14)
        )
        self.back_button.pack(side="left", padx=10)
        
    def load_data(self):
        if not hasattr(self.controller, "selected_notification") or self.controller.selected_notification is None:
            self.go_back()
            return
            
        notification = self.controller.selected_notification
        
        # Enable widgets for editing
        self.title_entry.configure(state='normal')
        self.message_textbox.configure(state='normal')
        
        # Clear previous content
        self.title_entry.delete(0, "end")
        self.message_textbox.delete("1.0", "end")
        
        # Insert new content
        self.title_entry.insert(0, notification.get("title"))
        
        message = notification.get("message")
        if message:
            self.message_textbox.insert("1.0", message)
        else:
            self.message_textbox.insert("1.0", "No additional message for this notification.")
        
        # Set information label
        date_time = notification.get("datetime")
        if isinstance(date_time, str):
            # If already formatted as string
            formatted_date = date_time
        elif isinstance(date_time, dt.datetime):
            # Format datetime object
            formatted_date = date_time.strftime("%Y-%m-%d %H:%M")
        else:
            formatted_date = "Unknown date"
            
        # Get sender information
        sender_id = notification.get("sender_hid")
        sender_name = self.get_sender_name(sender_id)
        
        self.info_label.configure(text=f"Received: {formatted_date} • From: {sender_name} (ID: {sender_id})")
        
        # Show/hide Mark as Read button based on role
        # First, remove the button if it's already packed
        self.mark_read_button.pack_forget()
        
        # Only show for non-admin users
        if hasattr(self.controller, "selected_role") and self.controller.selected_role != "admin":
            # Update button state based on read status
            if notification.get("read"):
                self.mark_read_button.configure(
                    text="Already Read",
                    state="disabled",
                    fg_color="#cccccc"
                )
            else:
                self.mark_read_button.configure(
                    text="Mark as Read",
                    state="normal",
                    fg_color="#4CAF50"
                )
            # Now pack the button
            self.mark_read_button.pack(side="left", padx=10)
        
        # Disable editing
        self.title_entry.configure(state='disabled')
        self.message_textbox.configure(state='disabled')
    
    def get_sender_name(self, sender_id):
        """Get the name of the sender from their hospital ID"""
        try:
            # Try to find sender in doctors
            if hasattr(self.controller, "hospital") and hasattr(self.controller.hospital, "doctors"):
                for doctor in self.controller.hospital.doctors.values():
                    if doctor.get_protected_attribute("hospital_id") == sender_id:
                        return f"Dr. {doctor.get_protected_attribute('name')} {doctor.get_protected_attribute('surname')}"
            
            # Try to find sender in patients
            if hasattr(self.controller, "hospital") and hasattr(self.controller.hospital, "patients"):
                for patient in self.controller.hospital.patients.values():
                    if patient.get_protected_attribute("hospital_id") == sender_id:
                        return f"Patient {patient.get_protected_attribute('name')} {patient.get_protected_attribute('surname')}"
            
            return "Administration"
        except:
            return "Hospital Staff"
        
    def mark_as_read(self):
        if hasattr(self.controller, "selected_notification") and self.controller.selected_notification:
            # Get notification object
            notification = self.controller.selected_notification
            
            # Update read status
            notification.set("read", True, "bool")
            
            # Update button state
            self.mark_read_button.configure(
                text="Already Read",
                state="disabled",
                fg_color="#cccccc"
            )
        
    def go_back(self):
        self.controller.selected_notification = None
        
        # Determine which screen to return to based on user role
        if self.controller.selected_role == "doctor":
            self.controller.show_frame("DoctorNotifications")
        elif self.controller.selected_role == "patient":
            self.controller.show_frame("PatientNotifications")
        elif self.controller.selected_role == "admin":
            self.controller.show_frame("AdminNotifications")
        else:
            messagebox.showerror("Error", "Unknown user role.")
            self.controller.show_frame("RoleSelectionScreen")
        
    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.load_data()