import customtkinter as ctk
from tkinter import ttk
from datetime import datetime, date

class DiagnosesDetails(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Diagnosis Details"
        
        top_button_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_button_frame.pack(fill="x", padx=30, pady=(15, 0), anchor="nw")
        
        self.top_back_btn = ctk.CTkButton(
            top_button_frame,
            text="Back",
            command=self.go_back,
            width=100,
            height=32,
            font=ctk.CTkFont(size=14)
        )
        self.top_back_btn.pack(side="left")

        # Main container with scrollable frame
        self.container_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.container_frame.pack(expand=True, fill="both", padx=30, pady=30)
        
        # Header with title
        header_frame = ctk.CTkFrame(self.container_frame, fg_color="#f0f5fa", corner_radius=10)
        header_frame.pack(fill="x", padx=10, pady=(0, 30))
        
        self.consultation_title = ctk.CTkLabel(
            header_frame, 
            text="Diagnosis Details", 
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#262850"
        )
        self.consultation_title.pack(pady=20)
        
        ### PATIENT INFO ##########################################
        self.patient_frame = ctk.CTkFrame(
            self.container_frame, 
            fg_color="#ffffff", 
            corner_radius=10, 
            border_width=1, 
            border_color="#e0e0e0"
        )
        self.patient_frame.pack(fill="x", padx=10, pady=(0, 30))
        
        self.patient_info_label = ctk.CTkLabel(
            self.patient_frame, 
            text="Patient Information", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#262850"
        )
        self.patient_info_label.pack(anchor="w", padx=20, pady=(20, 15))
        
        patient_info_grid = ctk.CTkFrame(self.patient_frame, fg_color="transparent")
        patient_info_grid.pack(fill="x", padx=20, pady=(0, 20))
        
        # Define fields and pos
        field_layout = [
            {"field": "Name", "row": 0, "column": 0},
            {"field": "Surname", "row": 0, "column": 2},
            {"field": "Hospital ID", "row": 0, "column": 4},
            {"field": "Gender", "row": 1, "column": 0},
            {"field": "Age", "row": 1, "column": 2},
            {"field": "Weight", "row": 2, "column": 0},
            {"field": "Height", "row": 2, "column": 2},
        ]
        
        self.patient_data = {}
        
        for item in field_layout:
            label = ctk.CTkLabel(
                patient_info_grid, 
                text=f"{item['field']}:", 
                font=ctk.CTkFont(size=16, weight="bold"),
                width=100,
                anchor="e"
            )
            label.grid(row=item['row'], column=item['column'], pady=10, sticky="e")
            
            value_label = ctk.CTkLabel(
                patient_info_grid,
                text="",  # Will be filled when displaying diagnosis
                font=ctk.CTkFont(size=16),
                anchor="w"
            )
            value_label.grid(row=item['row'], column=item['column']+1, padx=15, pady=10, sticky="w")
            self.patient_data[item['field']] = value_label
        
        # Configure grid columns to be more evenly distributed
        for i in range(6):
            patient_info_grid.grid_columnconfigure(i, weight=1)
        
        ### DIAGNOSIS DETAILS ##########################################
        self.diagnosis_frame = ctk.CTkFrame(
            self.container_frame, 
            fg_color="#ffffff", 
            corner_radius=10, 
            border_width=1, 
            border_color="#e0e0e0"
        )
        self.diagnosis_frame.pack(fill="x", padx=10, pady=(0, 30))
        
        ctk.CTkLabel(
            self.diagnosis_frame, 
            text="Diagnosis Details", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#262850"
        ).pack(anchor="w", padx=20, pady=(20, 15))
        
        # Title
        title_frame = ctk.CTkFrame(self.diagnosis_frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=(5, 15))
        
        ctk.CTkLabel(
            title_frame, 
            text="Title:", 
            font=ctk.CTkFont(size=16, weight="bold"),
            width=80,
            anchor="e"
        ).pack(side="left", padx=(0, 15))
        
        self.title_label = ctk.CTkLabel(
            title_frame, 
            text="",
            height=40,
            font=ctk.CTkFont(size=16),
            anchor="w"
        )
        self.title_label.pack(side="left", fill="x", expand=True)
        
        # Description
        desc_label_frame = ctk.CTkFrame(self.diagnosis_frame, fg_color="transparent")
        desc_label_frame.pack(fill="x", padx=20, pady=(5, 10))
        
        ctk.CTkLabel(
            desc_label_frame, 
            text="Description:", 
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        ).pack(anchor="w")
        
        self.description_text = ctk.CTkTextbox(
            self.diagnosis_frame, 
            height=150, 
            width=400, 
            wrap="word",
            font=ctk.CTkFont(size=16),
            border_width=1,
            border_color="#e0e0e0",
            corner_radius=6,
            state="disabled"
        )
        self.description_text.pack(fill="x", padx=20, pady=(0, 20))
        
        # Treatment section
        treatment_label_frame = ctk.CTkFrame(self.diagnosis_frame, fg_color="transparent")
        treatment_label_frame.pack(fill="x", padx=20, pady=(5, 10))
        
        ctk.CTkLabel(
            treatment_label_frame, 
            text="Treatment Plan:", 
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        ).pack(anchor="w")
        
        self.treatment_text = ctk.CTkTextbox(
            self.diagnosis_frame, 
            height=120, 
            width=400, 
            wrap="word",
            font=ctk.CTkFont(size=16),
            border_width=1,
            border_color="#e0e0e0",
            corner_radius=6,
            state="disabled"
        )
        self.treatment_text.pack(fill="x", padx=20, pady=(0, 20))
        
        ### PRESCRIBED MEDICATION ##########################################
        self.medication_frame = ctk.CTkFrame(
            self.container_frame, 
            fg_color="#ffffff", 
            corner_radius=10, 
            border_width=1, 
            border_color="#e0e0e0"
        )
        self.medication_frame.pack(fill="x", padx=10, pady=(0, 30))
        
        ctk.CTkLabel(
            self.medication_frame, 
            text="Prescribed Medication", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#262850"
        ).pack(anchor="w", padx=20, pady=(20, 15))
        
        # Create a frame for the medication treeview
        medication_tree_frame = ctk.CTkFrame(self.medication_frame, fg_color="transparent")
        medication_tree_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(medication_tree_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        
        # Style for treeview
        style = ttk.Style()
        style.configure('Treeview', rowheight=30, font=('Helvetica', 13))
        style.configure('Treeview.Heading', font=('Helvetica', 14, 'bold'))
        
        # Create treeview for medications
        self.medications_tree = ttk.Treeview(
            medication_tree_frame,
            columns=("Name", "Commercial Name", "Dosage"),
            show="headings",
            height=6,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.medications_tree.yview)
        
        # Configure columns
        self.medications_tree.heading("Name", text="Drug Name")
        self.medications_tree.heading("Commercial Name", text="Commercial Name")
        self.medications_tree.heading("Dosage", text="Dosage Instructions")
        
        self.medications_tree.column("Name", width=200)
        self.medications_tree.column("Commercial Name", width=200)
        self.medications_tree.column("Dosage", width=300)
        
        self.medications_tree.pack(fill="x", expand=True)
        
        # # Back button
        # button_frame = ctk.CTkFrame(self.container_frame, fg_color="transparent")
        # button_frame.pack(fill="x", padx=10, pady=(0, 20))
        
        # self.back_btn = ctk.CTkButton(
        #     button_frame,
        #     text="Back",
        #     command=self.go_back,
        #     width=120,
        #     height=40,
        #     font=ctk.CTkFont(size=16)
        # )
        # self.back_btn.pack(side="left")

    def load_diagnosis_data(self):
        """Load the selected diagnosis data into the UI"""
        if not hasattr(self.controller, 'selected_diagnosis') or not self.controller.selected_diagnosis:
            return
        
        diagnosis = self.controller.selected_diagnosis
        
        # Load patient data
        patient_id = diagnosis.get('patient_hid')
        patient = None
        for p in self.controller.hospital.patients.values():
            if p.get_protected_attribute('hospital_id') == patient_id:
                patient = p
                break
        
        if patient:
            # Get patient data and display
            current_date = date.today()
            birthdate = patient.get_protected_attribute('birthday')
            age = current_date.year - birthdate.year - ((current_date.month, current_date.day) < (birthdate.month, birthdate.day))
            
            self.patient_data["Name"].configure(text=patient.get_protected_attribute('name'))
            self.patient_data["Surname"].configure(text=patient.get_protected_attribute('surname'))
            self.patient_data["Hospital ID"].configure(text=patient.get_protected_attribute('hospital_id'))
            self.patient_data["Gender"].configure(text=patient.get_protected_attribute('gender'))
            self.patient_data["Age"].configure(text=f"{age} years")
            self.patient_data["Weight"].configure(text=f"{patient.get('weight')} kg")
            self.patient_data["Height"].configure(text=f"{patient.get('height')} cm")
        
        # Load diagnosis details
        self.title_label.configure(text=diagnosis.get('title'))
        
        # Enable textboxes temporarily to set text
        self.description_text.configure(state="normal")
        self.treatment_text.configure(state="normal")
        
        # Set diagnosis description and treatment
        self.description_text.delete("0.0", "end")
        self.description_text.insert("0.0", diagnosis.get('description') or "No description provided.")
        
        self.treatment_text.delete("0.0", "end")
        self.treatment_text.insert("0.0", diagnosis.get('treatment') or "No treatment plan specified.")
        
        # Disable textboxes again to make them read-only
        self.description_text.configure(state="disabled")
        self.treatment_text.configure(state="disabled")
        
        # Load medications
        self.load_medications(diagnosis.get('diagnosis_id'))

    def load_medications(self, diagnosis_id):
        """Load medications prescribed for this diagnosis"""
        # Clear existing items in the treeview
        for item in self.medications_tree.get_children():
            self.medications_tree.delete(item)
        
        # Get prescriptions for this diagnosis
        if not hasattr(self.controller, 'hospital') or not self.controller.hospital:
            return
            
        for prescription in self.controller.hospital.prescriptions.values():
            if prescription.get('diagnosis_id') == diagnosis_id:
                drug_id = prescription.get('drug_id')
                drug = self.controller.hospital.drugs.get(drug_id)
                
                if drug:
                    self.medications_tree.insert(
                        "", 
                        "end", 
                        values=(
                            drug.get('name'),
                            drug.get('commercial_name'),
                            prescription.get('dosage')
                        )
                    )

    def go_back(self):
        """Return to the previous screen"""
        self.controller.selected_diagnosis = None
        if self.controller.selected_role == "doctor":
            self.controller.show_frame("DoctorConsultation")
        elif self.controller.selected_role == "patient":
            self.controller.show_frame("PatientMedicalRecords")
        else:
            self.controller.show_frame("roleSelectionScreen")

    def tkraise(self, *args, **kwargs):
        """Load data when the frame is raised"""
        super().tkraise(*args, **kwargs)
        self.load_diagnosis_data()