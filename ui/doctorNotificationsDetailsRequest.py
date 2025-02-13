import customtkinter as ctk
from tkinter import ttk, messagebox

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
        
        self.description_entry = ctk.CTkTextbox(self.text_frame, height=250, width=50, wrap="word", border_width=2, state='disabled')
        self.description_entry.pack(pady=20, expand=True, fill="both")
        
        self.time_selection_frame = ctk.CTkFrame(self.container_frame, fg_color="transparent")
        self.time_selection_frame.pack(padx=10, pady=10)
        
        self.date_label = ctk.CTkLabel(self.time_selection_frame, text="Date")
        self.date_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.date_select = ctk.CTkComboBox(self.time_selection_frame, values=["Select Date"], width=200, height=40)
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
                
        self.back_button = ctk.CTkButton(self.buttons_frame, text="Go Back", command=lambda: self.controller.show_frame("DoctorNotifications"), height=40, width=200)
        self.back_button.grid(row=0, column=2, padx=10, pady=10)
        
    def load_data(self, data = None):
        self.title_entry.configure(state='normal')
        self.description_entry.configure(state='normal')
        
        self.title_entry.delete(0, "end")
        self.description_entry.delete(1.0, "end")
        
        self.title_entry.insert(0, "to be mod")
        self.description_entry.insert(1.0, "to be mod")
        self.title_entry.configure(state='disabled')
        
        self.description_entry.configure(state='disabled')
        self.date_select.configure(values="to be mod")
        self.time_select.configure(values="to be mod")
        
    def accept_appointment(self):
        messagebox.showinfo("Info", "Appointment accepted.")
        
    def reject_appointment(self):
        messagebox.showinfo("Info", "Appointment rejected.")
        
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