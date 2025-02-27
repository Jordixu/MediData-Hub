import customtkinter as ctk
from tkinter import ttk, messagebox
import datetime as dt

class DoctorNotificationsDetailsRequest(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Doctor Notifications Details"
        
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=4)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)
        self.columnconfigure(2, weight=1)

        self.top_frame = ctk.CTkFrame(self, fg_color="transparent", height=10)
        self.top_frame.grid(row=0, column=0, columnspan=3, sticky="n")

        self.left_frame = ctk.CTkFrame(self, fg_color="transparent", width=10)
        self.left_frame.grid(row=1, column=0, sticky="w")

        self.container_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.container_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.right_frame = ctk.CTkFrame(self, fg_color="transparent", width=10)
        self.right_frame.grid(row=1, column=2, sticky="e")

        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent", height=10)
        self.bottom_frame.grid(row=2, column=0, columnspan=3, sticky="s")
        
        self.text_frame = ctk.CTkFrame(self.container_frame, fg_color="transparent")
        self.text_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.title_label = ctk.CTkLabel(self.text_frame, text="Title", font=("Helvetica", 24))
        self.title_label.pack(pady=20)
        
        self.title_entry = ctk.CTkEntry(self.text_frame, width=50, state='disabled')
        self.title_entry.pack(pady=10, expand=True, fill="both")
        
        self.description_label = ctk.CTkLabel(self.text_frame, text="Description", font=("Helvetica", 24))
        self.description_label.pack(pady=20)
        
        self.description_entry = ctk.CTkTextbox(self.text_frame, height=180, width=50, wrap="word", border_width=2, state='disabled')
        self.description_entry.pack(pady=20, expand=True, fill="both")
        
        self.time_selection_frame = ctk.CTkFrame(self.container_frame, fg_color="transparent")
        self.time_selection_frame.pack(padx=10, pady=10)
        
        self.date_label = ctk.CTkLabel(self.time_selection_frame, text="Date")
        self.date_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.date_select = ctk.CTkComboBox(
            self.time_selection_frame, 
            values=["Select Date"], 
            width=200, 
            height=40,
            command=self.update_times
        )
        self.date_select.grid(row=1, column=0, padx=10, pady=10)
        
        self.time_label = ctk.CTkLabel(self.time_selection_frame, text="Time")
        self.time_label.grid(row=0, column=1, padx=10, pady=10)
        
        self.time_select = ctk.CTkComboBox(self.time_selection_frame, values=["Select Time"], width=200, height=40)
        self.time_select.grid(row=1, column=1, padx=10, pady=10)       
        
        self.buttons_frame = ctk.CTkFrame(self.container_frame, fg_color="transparent")
        self.buttons_frame.pack(padx=10, pady=10)
        
        self.accept_button = ctk.CTkButton(self.buttons_frame, text="Accept", command=lambda: self.accept_appointment(), height=40, width=200)
        self.accept_button.grid(row=0, column=0, padx=10, pady=10)
        
        self.reject_button = ctk.CTkButton(self.buttons_frame, text="Reject", command=lambda: self.reject_appointment(), height=40, width=200)
        self.reject_button.grid(row=0, column=1, padx=10, pady=10)
                
        self.back_button = ctk.CTkButton(self.buttons_frame, text="Go Back", command=lambda: self.go_back(), height=40, width=200)
        self.back_button.grid(row=0, column=2, padx=10, pady=10)
        
    def load_data(self):
        self.title_entry.configure(state='normal')
        self.description_entry.configure(state='normal')
        
        self.title_entry.delete(0, "end")
        self.description_entry.delete(1.0, "end")
        
        self.title_entry.insert(0, self.controller.selected_notification.get("title"))
        self.description_entry.insert(1.0, self.controller.selected_notification.get("message"))
        self.title_entry.configure(state='disabled')
        self.description_entry.configure(state='disabled')
        
        if hasattr(self.controller, 'current_user_data') and self.controller.current_user_data:
            available_slots = self.controller.current_user_data.get("availability")
            if available_slots:
                dates_proc = [date.strftime("%Y-%m-%d") for date in available_slots.keys()]
                print(dates_proc)
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
        # Get selected time string from ComboBox
        selected_time_str = self.time_select.get()  # e.g., "09:00"
        
        try:
            # Parse hours and minutes from the string
            start_hour, start_minute = map(int, selected_time_str.split(':'))
            
            # Create start and end times (assume 1-hour slots)
            start_time = dt.time(start_hour, start_minute)
            end_time = dt.time(start_hour + 1, start_minute)
            appt = self.controller.selected_notification.get("appointment_id")
            print(appt)
            # Schedule the appointment
            self.controller.hospital.schedule_appointment(
                appointment_id = appt,
                date=dt.datetime.strptime(self.date_select.get(), "%Y-%m-%d").date(),
                timeframe=(start_time, end_time)
            )
            
            messagebox.showinfo("Success", "Appointment accepted.")
            
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid time format: {e}")
        # except Exception as e:
        #     messagebox.showerror("Error", f"Failed to schedule: {e}")
        
    def reject_appointment(self):
        self.controller.hospital.send_notification(
            sender_hid=self.controller.current_user_data.get("hospital_id"),
            receiver_hid=self.controller.selected_notification.get("sender_hid"),
            title="Appointment Rejected",
            message="Your appointment request has been rejected.",
            notif_type="Appointment Rejected"
        )
        appt = self.controller.selected_notification.get("appointment_id")
        self.controller.hospital.appointments[appt].change_status("Rejected")
        messagebox.showinfo("Info", "Appointment rejected.")
        
    def go_back(self):
        self.controller.selected_notification = None
        self.controller.show_frame("DoctorNotifications")
        
    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.load_data()

if __name__ == "__main__":
    root = ctk.CTk()
    ctk.set_appearance_mode("light")
    container = DoctorNotificationsDetailsRequest(root, None)
    container.pack(expand=True, fill="both")
    container.load_data()
    root.mainloop()