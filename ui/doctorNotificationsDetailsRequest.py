import customtkinter as ctk
from tkinter import ttk, messagebox
import datetime as dt

class DoctorNotificationsDetailsRequest(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Appointment Request Details"
        
        # Configure the main layout with better spacing
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Content
        self.grid_rowconfigure(2, weight=0)  # Footer/buttons
        
        # Enhanced header with subtle gradient effect
        header_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=("#e6eef5", "#2d3035"))
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 0))
        
        title_label = ctk.CTkLabel(
            header_frame, 
            text="Appointment Request", 
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color=("#262850", "#e0e0e0")
        )
        title_label.pack(pady=20)
        
        # Main content area with improved padding and organization
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=1, column=0, padx=40, pady=25, sticky="nsew")
        
        # Notification title section with improved styling
        title_section = ctk.CTkFrame(content_frame, fg_color="transparent")
        title_section.pack(fill="x", pady=(0, 25))
        
        title_header = ctk.CTkLabel(
            title_section, 
            text="Title", 
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        )
        title_header.pack(anchor="w", pady=(0, 8))
        
        self.title_entry = ctk.CTkEntry(
            title_section, 
            height=45,
            font=ctk.CTkFont(size=16),
            state='disabled',
            border_width=1,
            corner_radius=8
        )
        self.title_entry.pack(fill="x")
        
        # Message section with improved styling
        message_section = ctk.CTkFrame(content_frame, fg_color="transparent")
        message_section.pack(fill="x", expand=False, pady=(0, 25))
        
        message_header = ctk.CTkLabel(
            message_section, 
            text="Message", 
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        )
        message_header.pack(anchor="w", pady=(0, 8))
        
        self.description_entry = ctk.CTkTextbox(
            message_section, 
            font=ctk.CTkFont(size=16),
            corner_radius=8,
            border_width=1,
            wrap="word",
            height=160,
            state='disabled'
        )
        self.description_entry.pack(fill="x")
        
        # Time selection section with enhanced visual appeal
        time_selection_section = ctk.CTkFrame(
            content_frame, 
            fg_color=("#f0f5fa", "#32363a"), 
            corner_radius=10,
            border_width=1,
            border_color=("#d0d7de", "#40454a")
        )
        time_selection_section.pack(fill="x", pady=(0, 25), padx=0)
        
        time_selection_header = ctk.CTkLabel(
            time_selection_section, 
            text="Select Appointment Time", 
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#262850", "#e0e0e0")
        )
        time_selection_header.pack(anchor="w", padx=20, pady=(20, 15))
        
        selection_container = ctk.CTkFrame(time_selection_section, fg_color="transparent")
        selection_container.pack(fill="x", padx=20, pady=(0, 20))
        selection_container.columnconfigure(0, weight=1)  # Left margin
        selection_container.columnconfigure(1, weight=0)  # Date column
        selection_container.columnconfigure(2, weight=0)  # Time column
        selection_container.columnconfigure(3, weight=1)  # Right margin

        date_frame = ctk.CTkFrame(selection_container, fg_color="transparent")
        date_frame.grid(row=0, column=1, padx=10)

        date_label = ctk.CTkLabel(
            date_frame, 
            text="Available Date",
            font=ctk.CTkFont(size=16),
            anchor="center"
        )
        date_label.pack(anchor="center", pady=(0, 8))

        self.date_select = ctk.CTkComboBox(
            date_frame, 
            values=["Select Date"], 
            width=220, 
            height=45,
            font=ctk.CTkFont(size=15),
            command=self.update_times,
            dropdown_font=ctk.CTkFont(size=15),
            border_width=1,
            button_color=("#4a6fdc", "#3a5bbc"),
            button_hover_color=("#3a5bbc", "#2a4bac")
        )
        self.date_select.pack()

        time_frame = ctk.CTkFrame(selection_container, fg_color="transparent")
        time_frame.grid(row=0, column=2, padx=10)

        time_label = ctk.CTkLabel(
            time_frame, 
            text="Available Time",
            font=ctk.CTkFont(size=16),
            anchor="center"
        )
        time_label.pack(anchor="center", pady=(0, 8))

        self.time_select = ctk.CTkComboBox(
            time_frame, 
            values=["Select Time"], 
            width=220, 
            height=45,
            font=ctk.CTkFont(size=15),
            dropdown_font=ctk.CTkFont(size=15),
            border_width=1,
            button_color=("#4a6fdc", "#3a5bbc"),
            button_hover_color=("#3a5bbc", "#2a4bac")
        )
        self.time_select.pack()
        
        # Button section with enhanced styling
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=2, column=0, pady=25)
        
        # Accept button with improved appearance
        self.accept_button = ctk.CTkButton(
            button_frame,
            text="Accept Request",
            command=self.accept_appointment,
            width=200,
            height=48,
            fg_color=("#4CAF50", "#3d9140"),
            hover_color=("#45a049", "#358035"),
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=8,
            border_width=1,
            border_color=("#40a044", "#307030")
        )
        self.accept_button.pack(side="left", padx=12)
        
        # Reject button with improved appearance
        self.reject_button = ctk.CTkButton(
            button_frame,
            text="Reject Request",
            command=self.reject_appointment,
            width=200,
            height=48,
            fg_color=("#e74c3c", "#d32f2f"),
            hover_color=("#c0392b", "#b71c1c"),
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=8,
            border_width=1,
            border_color=("#c0392b", "#9e1c1c")
        )
        self.reject_button.pack(side="left", padx=12)
        
        # Back button with improved appearance
        back_button = ctk.CTkButton(
            button_frame,
            text="Go Back",
            command=self.go_back,
            width=160,
            height=48,
            fg_color=("#555555", "#444444"),
            hover_color=("#666666", "#333333"),
            font=ctk.CTkFont(size=16),
            corner_radius=8,
            border_width=1,
            border_color=("#444444", "#333333")
        )
        back_button.pack(side="left", padx=12)
        
    def load_data(self):
        # (Functionality unchanged)
        if not hasattr(self.controller, "selected_notification") or self.controller.selected_notification is None:
            self.go_back()
            return
            
        # Enable widgets for editing
        self.title_entry.configure(state='normal')
        self.description_entry.configure(state='normal')
        
        # Clear previous content
        self.title_entry.delete(0, "end")
        self.description_entry.delete("1.0", "end")
        
        # Insert new content
        self.title_entry.insert(0, self.controller.selected_notification.get("title", "Appointment Request"))
        self.description_entry.insert("1.0", self.controller.selected_notification.get("message", "No additional details provided."))
        
        # Disable editing
        self.title_entry.configure(state='disabled')
        self.description_entry.configure(state='disabled')
        
        # Load available slots
        if hasattr(self.controller, 'current_user_data') and self.controller.current_user_data:
            available_slots = self.controller.current_user_data.get("availability")
            if available_slots:
                dates_proc = [date.strftime("%Y-%m-%d") for date in available_slots.keys()]
                dates = sorted(dates_proc)
                self.date_select.configure(values=dates)
                if dates:
                    selected_date = dates[0]
                    self.date_select.set(selected_date)
                    self.update_times(selected_date)
                else:
                    self.date_select.set("No available dates")
                    self.time_select.set("No available times")
            else:
                self.date_select.set("No available dates")
                self.time_select.set("No available times")
        else:
            self.date_select.set("No availability data")
            self.time_select.set("No availability data")

    def update_times(self, selected_date):
        # (Functionality unchanged)
        available_slots = self.controller.current_user_data.get("availability")
        times_dict = available_slots[dt.datetime.strptime(selected_date, "%Y-%m-%d").date()]

        available_times = [time_range for time_range, available in times_dict.items() if available]

        sorted_ranges = sorted(available_times, key=lambda x: x[0])

        formatted_times = []
        for time_range in sorted_ranges:
            if isinstance(time_range, tuple) and len(time_range) >= 1:
                start_time = time_range[0]
                try:
                    if isinstance(start_time, str):
                        h, m, _ = start_time.split(':')
                    elif hasattr(start_time, 'hour') and hasattr(start_time, 'minute'):
                        h, m = start_time.hour, start_time.minute
                    else:
                        continue

                    formatted_time = f"{int(h):02d}:{int(m):02d}"
                    formatted_times.append(formatted_time)
                except (ValueError, AttributeError):
                    continue

        self.time_select.configure(values=formatted_times)
        if formatted_times:
            self.time_select.set(formatted_times[0])
        else:
            self.time_select.set("No available times")
            
    def accept_appointment(self):
        # (Functionality unchanged)
        selected_time_str = self.time_select.get()
        
        if selected_time_str == "No available times" or selected_time_str == "Select Time":
            messagebox.showwarning("Warning", "Please select a valid time slot.")
            return
            
        try:
            start_hour, start_minute = map(int, selected_time_str.split(':'))
            
            start_time = dt.time(start_hour, start_minute)
            end_time = dt.time(start_hour + 1, start_minute)
            appt = self.controller.selected_notification.get("appointment_id")
            
            self.controller.hospital.schedule_appointment(
                appointment_id=appt,
                date=dt.datetime.strptime(self.date_select.get(), "%Y-%m-%d").date(),
                timeframe=(start_time, end_time)
            )
            
            self.controller.selected_notification.set("read", True, "bool")
            self.controller.selected_notification = None
            
            messagebox.showinfo("Success", "Appointment has been accepted and scheduled successfully.")
            self.controller.show_frame("DoctorNotifications")
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid time format: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to schedule appointment: {e}")
        
    def reject_appointment(self):
        # (Functionality unchanged)
        self.controller.hospital.send_notification(
            sender_hid=self.controller.current_user_data.get("hospital_id"),
            receiver_hid=self.controller.selected_notification.get("sender_hid"),
            title="Appointment Request Rejected",
            message="Your appointment request has been rejected by the doctor.",
            notif_type="Appointment Rejected"
        )
        
        appt = self.controller.selected_notification.get("appointment_id")
        self.controller.hospital.appointments[appt].change_status("Rejected")
        
        self.controller.selected_notification.set("read", True, "bool")
        self.controller.selected_notification = None
        
        messagebox.showinfo("Success", "Appointment request has been rejected and the patient has been notified.")
        self.controller.show_frame("DoctorNotifications")
        
    def go_back(self):
        # (Functionality unchanged)
        self.controller.selected_notification = None
        self.controller.show_frame("DoctorNotifications")
        
    def tkraise(self, *args, **kwargs):
        # (Functionality unchanged)
        super().tkraise(*args, **kwargs)
        self.load_data()