import tkinter as tk 
import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk

class DoctorConsultationCreate(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Doctor Consultation"

        self.container_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.container_frame.pack(expand=True, fill="both")
        
        self.text_frame = ctk.CTkFrame(self.container_frame, fg_color="transparent")
        self.text_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.patient_frame = ctk.CTkFrame(self.text_frame, fg_color="transparent")
        self.patient_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.patient_info = ctk.CTkLabel(self.patient_frame, text="Patient Information", font=("Helvetica", 24))
        self.patient_info.pack(pady=20)
        
        self.patient_name_label = ctk.CTkLabel(self.patient_frame, text="Patient Name", font=("Helvetica", 14, "bold"))
        self.patient_name_label.pack(pady=10)
        
        self.patient_age_label = ctk.CTkLabel(self.patient_frame, text="Patient Age", font=("Helvetica", 14, "bold"))
        self.patient_age_label.pack(pady=10)
        
        self.patient_name_entry = ctk.CTkEntry(self.text_frame, width=50, state='disabled')
        self.patient_name_entry.pack(pady=10, expand=True, fill="both")
        
        
        self.title_label = ctk.CTkLabel(self.text_frame, text="Title", font=("Helvetica", 24))
        self.title_label.pack(pady=20)
        
        self.title_entry = ctk.CTkEntry(self.text_frame, width=50)
        self.title_entry.pack(pady=10, expand=True, fill="both")
        
        self.description_label = ctk.CTkLabel(self.text_frame, text="Description", font=("Helvetica", 24))
        self.description_label.pack(pady=20)
        
        self.description_entry = ctk.CTkTextbox(self.text_frame, height=180, width=50, wrap="word", border_width=2)
        self.description_entry.pack(pady=20, expand=True, fill="both")