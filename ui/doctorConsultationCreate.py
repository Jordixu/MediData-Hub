import tkinter as tk 
import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime, date

class DoctorConsultationCreate(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Doctor Consultation"
        self.selected_drugs = []  # This will now store drug ID, name, commercial name, and dosage

        # Main container with scrollable frame
        self.container_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.container_frame.pack(expand=True, fill="both", padx=30, pady=30)
        
        # Header with title
        header_frame = ctk.CTkFrame(self.container_frame, fg_color="#f0f5fa", corner_radius=10)
        header_frame.pack(fill="x", padx=10, pady=(0, 30))
        
        self.consultation_title = ctk.CTkLabel(
            header_frame, 
            text="New Consultation", 
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#262850"
        )
        self.consultation_title.pack(pady=20)
        
        ### PATIENT INFO ##########################################
        # Here we place the patient information, previous diagnoses, new diagnosis, drugs and buttons, all in a single frame.
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
            # Row 0
            {"field": "Name", "row": 0, "column": 0},
            {"field": "Surname", "row": 0, "column": 2},
            {"field": "Hospital ID", "row": 0, "column": 4},
            # Row 1
            {"field": "Gender", "row": 1, "column": 0},
            {"field": "Age", "row": 1, "column": 2},
            # Row 2
            {"field": "Weight", "row": 2, "column": 0},
            {"field": "Height", "row": 2, "column": 2},
        ]
        
        self.patient_data = {}
        
        for item in field_layout:
            field = item["field"]
            row = item["row"]
            col = item["column"]
            
            # Label
            ctk.CTkLabel(
            patient_info_grid, 
            text=f"{field}:", 
            font=ctk.CTkFont(size=16, weight="bold"),
            width=100,
            anchor="e"
            ).grid(row=row, column=col, sticky="e", padx=(10, 5), pady=12)
            
            # Value (pat data)
            value_label = ctk.CTkLabel(
            patient_info_grid, 
            text="", 
            font=ctk.CTkFont(size=16),
            width=120,
            anchor="w")
            value_label.grid(row=row, column=col+1, sticky="w", padx=(0, 20), pady=12)
            self.patient_data[field] = value_label
        
        # Configure grid columns to be more evenly distributed
        for i in range(6):
            patient_info_grid.grid_columnconfigure(i, weight=1)
        
        
        ### PREVIOUS DIAGNOSES ##########################################
        # Here we place the previous diagnoses treeview and a button to view details. The view details button will open a popup window.
        self.prev_diagnosis_frame = ctk.CTkFrame(
            self.container_frame, 
            fg_color="#ffffff", 
            corner_radius=10, 
            border_width=1, 
            border_color="#e0e0e0"
        )
        self.prev_diagnosis_frame.pack(fill="x", padx=10, pady=(0, 30))
        
        prev_diag_header = ctk.CTkFrame(self.prev_diagnosis_frame, fg_color="transparent")
        prev_diag_header.pack(fill="x", padx=20, pady=(20, 15))
        
        ctk.CTkLabel(
            prev_diag_header, 
            text="Previous Diagnoses", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#262850"
        ).pack(side="left")
        
        self.view_diagnosis_btn = ctk.CTkButton(
            prev_diag_header,
            text="View Details",
            command=self.view_diagnosis_details,
            width=120,
            height=32,
            font=ctk.CTkFont(size=14)
        )
        self.view_diagnosis_btn.pack(side="right")
        
        # Create a treeview for previous diagnoses
        tree_frame = ctk.CTkFrame(self.prev_diagnosis_frame, fg_color="transparent")
        tree_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        
        # Style for treeview
        style = ttk.Style()
        style.configure('Treeview', rowheight=30, font=('Helvetica', 13))
        style.configure('Treeview.Heading', font=('Helvetica', 14, 'bold'))
        
        self.prev_diagnosis_tree = ttk.Treeview(
            tree_frame, 
            columns=("Date", "Title", "Description", "Treatment"),
            show="headings", 
            height=4,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.prev_diagnosis_tree.yview)
        self.prev_diagnosis_tree.pack(fill="x", pady=5)
        
        # Configure columns
        self.prev_diagnosis_tree.heading("Date", text="Date")
        self.prev_diagnosis_tree.heading("Title", text="Title")
        self.prev_diagnosis_tree.heading("Description", text="Description")
        self.prev_diagnosis_tree.heading("Treatment", text="Treatment")
        
        self.prev_diagnosis_tree.column("Date", width=120, anchor="center")
        self.prev_diagnosis_tree.column("Title", width=180)
        self.prev_diagnosis_tree.column("Description", width=300)
        self.prev_diagnosis_tree.column("Treatment", width=180)
        
        
        ### NEW DIAGNOSIS ##########################################
        # Here we place the fields for the new diagnosis: title, description, treatment plan, and drugs.
        self.new_diagnosis_frame = ctk.CTkFrame(
            self.container_frame, 
            fg_color="#ffffff", 
            corner_radius=10, 
            border_width=1, 
            border_color="#e0e0e0"
        )
        self.new_diagnosis_frame.pack(fill="x", padx=10, pady=(0, 30))
        
        ctk.CTkLabel(
            self.new_diagnosis_frame, 
            text="New Diagnosis", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#262850"
        ).pack(anchor="w", padx=20, pady=(20, 15))
        
        # Title for new diagnosis
        title_frame = ctk.CTkFrame(self.new_diagnosis_frame, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=(5, 15))
        
        ctk.CTkLabel(
            title_frame, 
            text="Title:", 
            font=ctk.CTkFont(size=16, weight="bold"),
            width=80,
            anchor="e"
        ).pack(side="left", padx=(0, 15))
        
        self.title_entry = ctk.CTkEntry(
            title_frame, 
            placeholder_text="Enter diagnosis title",
            height=40,
            font=ctk.CTkFont(size=16)
        )
        self.title_entry.pack(side="left", fill="x", expand=True)
        
        # Description for new diagnosis
        desc_label_frame = ctk.CTkFrame(self.new_diagnosis_frame, fg_color="transparent")
        desc_label_frame.pack(fill="x", padx=20, pady=(5, 10))
        
        ctk.CTkLabel(
            desc_label_frame, 
            text="Description:", 
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        ).pack(anchor="w")
        
        self.description_entry = ctk.CTkTextbox(
            self.new_diagnosis_frame, 
            height=150, 
            width=400, 
            wrap="word",
            font=ctk.CTkFont(size=16),
            border_width=1,
            border_color="#e0e0e0",
            corner_radius=6
        )
        self.description_entry.pack(fill="x", padx=20, pady=(0, 20))
        
        # Treatment section
        treatment_label_frame = ctk.CTkFrame(self.new_diagnosis_frame, fg_color="transparent")
        treatment_label_frame.pack(fill="x", padx=20, pady=(5, 10))
        
        ctk.CTkLabel(
            treatment_label_frame, 
            text="Treatment Plan:", 
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        ).pack(anchor="w")
        
        self.treatment_entry = ctk.CTkTextbox(
            self.new_diagnosis_frame, 
            height=120, 
            width=400, 
            wrap="word",
            font=ctk.CTkFont(size=16),
            border_width=1,
            border_color="#e0e0e0",
            corner_radius=6
        )
        self.treatment_entry.pack(fill="x", padx=20, pady=(0, 20))
        
        ### DRUGS SECTION ##########################################
        # Here we place the drug selection area, search results, selected drugs list, and dosage instructions. The hardest part of this file.
        self.drug_frame = ctk.CTkFrame(
            self.container_frame, 
            fg_color="#ffffff", 
            corner_radius=10, 
            border_width=1, 
            border_color="#e0e0e0"
        )
        self.drug_frame.pack(fill="x", padx=10, pady=(0, 30))
        
        ctk.CTkLabel(
            self.drug_frame, 
            text="Medication", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#262850"
        ).pack(anchor="w", padx=20, pady=(20, 15))
        
        # Drug selection area
        self.drug_selection_frame = ctk.CTkFrame(self.drug_frame, fg_color="transparent")
        self.drug_selection_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Search and add drug
        search_frame = ctk.CTkFrame(self.drug_selection_frame, fg_color="transparent")
        search_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            search_frame, 
            text="Search Drug:", 
            font=ctk.CTkFont(size=16, weight="bold"),
            width=120,
            anchor="e"
        ).pack(side="left", padx=(0, 15))
        
        self.drug_search = ctk.CTkEntry(
            search_frame, 
            placeholder_text="Search by name...",
            height=40,
            font=ctk.CTkFont(size=16)
        )
        self.drug_search.pack(side="left", padx=(0, 15), fill="x", expand=True)
        
        self.search_btn = ctk.CTkButton(
            search_frame, 
            text="Search", 
            width=100,
            height=40,
            command=self.search_drugs,
            font=ctk.CTkFont(size=15)
        )
        self.search_btn.pack(side="left", padx=(0, 15))
        
        self.add_drug_btn = ctk.CTkButton(
            search_frame, 
            text="Add Selected", 
            width=140,
            height=40,
            command=self.add_drug,
            font=ctk.CTkFont(size=15)
        )
        self.add_drug_btn.pack(side="left")
        
        # Drug search results
        results_frame = ctk.CTkFrame(self.drug_selection_frame, fg_color="transparent")
        results_frame.pack(fill="x", pady=15)
        
        # Create a frame for the drug results treeview
        drug_tree_frame = ctk.CTkFrame(results_frame, fg_color="#f5f5f5", corner_radius=5)
        drug_tree_frame.pack(fill="x", pady=5)
        
        # Scrollbar for drug results
        drug_scrollbar = ttk.Scrollbar(drug_tree_frame, orient="vertical")
        drug_scrollbar.pack(side="right", fill="y")
        
        # Treeview for drug search results
        self.drug_tree = ttk.Treeview(
            drug_tree_frame, 
            columns=("ID", "Name", "Commercial Name", "Price", "Prescription"),
            show="headings", 
            height=5,
            yscrollcommand=drug_scrollbar.set
        )
        drug_scrollbar.config(command=self.drug_tree.yview)
        self.drug_tree.pack(fill="x", pady=5, padx=5)
        
        # Configure drug results columns
        self.drug_tree.heading("ID", text="ID")
        self.drug_tree.heading("Name", text="Name")
        self.drug_tree.heading("Commercial Name", text="Commercial Name")
        self.drug_tree.heading("Price", text="Price")
        self.drug_tree.heading("Prescription", text="Prescription")
        
        self.drug_tree.column("ID", width=60, anchor="center")
        self.drug_tree.column("Name", width=180)
        self.drug_tree.column("Commercial Name", width=220)
        self.drug_tree.column("Price", width=100, anchor="center")
        self.drug_tree.column("Prescription", width=120, anchor="center")
        
        # Selected drugs list
        selected_drugs_label = ctk.CTkLabel(
            self.drug_selection_frame, 
            text="Prescribed Medications:", 
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        selected_drugs_label.pack(anchor="w", pady=(15, 10))
        
        self.selected_drugs_frame = ctk.CTkScrollableFrame(
            self.drug_selection_frame, 
            fg_color="#f0f0f0",
            height=250,  # Increased height to accommodate dosage instructions
            corner_radius=5
        )
        self.selected_drugs_frame.pack(fill="x", pady=5)
        
        ### BUTTONS SECTION ##########################################
        # There are not much to say about this section, just two buttons.
        self.button_frame = ctk.CTkFrame(self.container_frame, fg_color="transparent")
        self.button_frame.pack(fill="x", padx=10, pady=(0, 20))
        
        self.back_btn = ctk.CTkButton(
            self.button_frame, 
            text="Cancel", 
            fg_color="#6c757d", 
            hover_color="#5a6268", 
            command=self.go_back,
            width=180,
            height=45,
            font=ctk.CTkFont(size=16)
        )
        self.back_btn.pack(side="left", padx=10)
        
        self.end_consultation_btn = ctk.CTkButton(
            self.button_frame, 
            text="Complete Consultation", 
            fg_color="#28a745", 
            hover_color="#218838", 
            command=self.end_consultation,
            width=220,
            height=45,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.end_consultation_btn.pack(side="right", padx=10)
        
    def load_patient_data(self):
        """Load patient data for the current consultation"""
        if not hasattr(self.controller, "selected_patient") or not self.controller.selected_patient:
            messagebox.showerror("Error", "No patient selected for consultation")
            self.go_back()
            return
            
        patient = self.controller.selected_patient
        appointment = self.controller.selected_appointment
        appointment.change_status("In Progress") # Change appointment status to In Progress, sincerely, I don't see the point of this function since we can't see the appointment status.
        
        # Update consultation title with patient name
        name = patient.get_protected_attribute("name")
        surname = patient.get_protected_attribute("surname")
        self.consultation_title.configure(text=f"Consultation with {name} {surname}")
        
        # Update patient information fields
        self.patient_data["Name"].configure(text=name)
        self.patient_data["Surname"].configure(text=surname)
        self.patient_data["Hospital ID"].configure(text=patient.get_protected_attribute("hospital_id"))
        self.patient_data["Gender"].configure(text=patient.get_protected_attribute("gender"))
        
        # Calculate age from birthday
        birthday = patient.get_protected_attribute("birthday")
        if isinstance(birthday, str):
            birthday = datetime.strptime(birthday, "%Y-%m-%d").date()

        today = date.today()
        age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
        self.patient_data["Age"].configure(text=f"{age} years")
        
        # Add weight and height
        self.patient_data["Weight"].configure(text=f"{patient.get('weight')} kg")
        self.patient_data["Height"].configure(text=f"{patient.get('height')} cm")
        
        # Load previous diagnoses
        self.load_previous_diagnoses(patient)
        
        # Load available drugs
        self.load_available_drugs()
        
    def load_previous_diagnoses(self, patient):
        """Load previous diagnoses for the patient"""
        # Clear existing items
        for item in self.prev_diagnosis_tree.get_children():
            self.prev_diagnosis_tree.delete(item)
            
        # Get diagnoses from patient data
        diagnoses = patient.get_protected_attribute("diagnoses")
        if not diagnoses or diagnoses == []:
            # Add a placeholder row if no diagnoses
            self.prev_diagnosis_tree.insert("", "end", values=("No previous diagnoses found", "", "", ""))
            return
            
        # Add diagnoses to treeview
        for diagnosis_id in diagnoses:
            try:
                diagnosis = self.controller.hospital.diagnoses.get(diagnosis_id)
                if diagnosis:
                    date_str = diagnosis.get("date", "N/A")
                    title = diagnosis.get("title", "N/A")
                    description = diagnosis.get("description", "N/A")
                    treatment = diagnosis.get("treatment", "N/A")
                    
                    self.prev_diagnosis_tree.insert("", "end", values=(date_str, title, description, treatment))
            except Exception as e:
                print(f"Error loading diagnosis {diagnosis_id}: {e}")
                
    def view_diagnosis_details(self):
        """View details of the selected diagnosis in a popup window"""
        selected_items = self.prev_diagnosis_tree.selection()
        if not selected_items:
            messagebox.showinfo("No Selection", "Please select a diagnosis to view details")
            return
            
        # Get the selected diagnosis details
        diagnosis_values = self.prev_diagnosis_tree.item(selected_items[0], "values")
        if diagnosis_values[0] == "No previous diagnoses found":
            messagebox.showinfo("No Diagnoses", "There are no previous diagnoses to view")
            return
            
        # Create a popup window to display the diagnosis details
        # Patricia se que dijiste q no hagamos toplevels pero sino tenia que hacer otro frame
        popup = ctk.CTkToplevel(self)
        popup.title("Diagnosis Details")
        popup.geometry("800x600")
        popup.grab_set()
        
        # Set min size
        popup.minsize(700, 500)
        
        # Center the popup to the window
        popup.update_idletasks()
        width = popup.winfo_width()
        height = popup.winfo_height()
        x = (popup.winfo_screenwidth() // 2) - (width // 2)
        y = (popup.winfo_screenheight() // 2) - (height // 2)
        popup.geometry(f"{width}x{height}+{x}+{y}")
        
        # Create a scrollable frame for the content
        content_frame = ctk.CTkScrollableFrame(popup, fg_color="transparent")
        content_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Diagnosis date and title
        header_frame = ctk.CTkFrame(content_frame, fg_color="#f0f5fa", corner_radius=10)
        header_frame.pack(fill="x", pady=(0, 20))
        
        date_label = ctk.CTkLabel(
            header_frame, 
            text=f"Date: {diagnosis_values[0]}", 
            font=ctk.CTkFont(size=14),
            anchor="w"
        )
        date_label.pack(anchor="w", padx=20, pady=(15, 5))
        
        title_label = ctk.CTkLabel(
            header_frame, 
            text=diagnosis_values[1], 
            font=ctk.CTkFont(size=24, weight="bold"),
            anchor="w"
        )
        title_label.pack(anchor="w", padx=20, pady=(0, 15))
        
        # Description section
        desc_frame = ctk.CTkFrame(content_frame, fg_color="#ffffff", corner_radius=10, border_width=1, border_color="#e0e0e0")
        desc_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            desc_frame, 
            text="Description", 
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        ).pack(anchor="w", padx=20, pady=(15, 10))
        
        desc_text = ctk.CTkTextbox(
            desc_frame, 
            height=150, 
            width=400, 
            wrap="word",
            font=ctk.CTkFont(size=16),
            activate_scrollbars=True
        )
        desc_text.pack(fill="x", padx=20, pady=(0, 15))
        desc_text.insert("1.0", diagnosis_values[2])
        desc_text.configure(state="disabled")  # Make it read-only
        
        # Treatment section
        treatment_frame = ctk.CTkFrame(content_frame, fg_color="#ffffff", corner_radius=10, border_width=1, border_color="#e0e0e0")
        treatment_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            treatment_frame, 
            text="Treatment Plan", 
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w"
        ).pack(anchor="w", padx=20, pady=(15, 10))
        
        treatment_text = ctk.CTkTextbox(
            treatment_frame, 
            height=150, 
            width=400, 
            wrap="word",
            font=ctk.CTkFont(size=16),
            activate_scrollbars=True
        )
        treatment_text.pack(fill="x", padx=20, pady=(0, 15))
        treatment_text.insert("1.0", diagnosis_values[3])
        treatment_text.configure(state="disabled")  # Make it read-only
        
        # Close button
        close_btn = ctk.CTkButton(
            popup, 
            text="Close", 
            command=popup.destroy,
            width=150,
            height=40,
            font=ctk.CTkFont(size=16)
        )
        close_btn.pack(pady=20)
        
    def load_available_drugs(self):
        """Load available drugs from the hospital database"""
        # Clear existing items
        for item in self.drug_tree.get_children():
            self.drug_tree.delete(item)
            
        # Get drugs from hospital data
        if hasattr(self.controller.hospital, "drugs"):
            drugs = self.controller.hospital.drugs
            
            # Add first 10 drugs to treeview as initial display
            count = 0
            for drug_id, drug in drugs.items():
                if count >= 10:  # Limit initial display to 10 drugs
                    break
                    
                name = drug.get("name", "N/A")
                commercial_name = drug.get("commercial_name", "N/A")
                price = f"{drug.get('price', 'N/A')} €"
                prescription = "Yes" if drug.get("prescription") else "No"
                
                self.drug_tree.insert("", "end", values=(drug_id, name, commercial_name, price, prescription))
                count += 1
    
    def search_drugs(self):
        """Search for drugs based on the search term"""
        search_term = self.drug_search.get().strip().lower() # Get search term, convert to lowercase, and remove leading/trailing spaces
        if not search_term:
            self.load_available_drugs()  # Reset to show all drugs if search is empty
            return
            
        # Clear existing items
        for item in self.drug_tree.get_children():
            self.drug_tree.delete(item)
            
        # Search drugs from hospital data
        if hasattr(self.controller.hospital, "drugs"):
            drugs = self.controller.hospital.drugs
            
            # Filter drugs based on search term
            matching_drugs = []
            for drug_id, drug in drugs.items():
                name = drug.get("name", "").lower()
                commercial_name = drug.get("commercial_name", "").lower()
                
                if search_term in name or search_term in commercial_name:
                    matching_drugs.append((drug_id, drug))
            
            # Add matching drugs to treeview
            if matching_drugs:
                for drug_id, drug in matching_drugs:
                    name = drug.get("name", "N/A")
                    commercial_name = drug.get("commercial_name", "N/A")
                    price = f"{drug.get('price', 'N/A')} €"
                    prescription = "Yes" if drug.get("prescription") else "No"
                    
                    self.drug_tree.insert("", "end", values=(drug_id, name, commercial_name, price, prescription))
            else:
                # Add a placeholder row if no matching drugs
                self.drug_tree.insert("", "end", values=("No matching drugs found", "", "", "", ""))
    
    def add_drug(self):
        """Add selected drug to the prescription list"""
        selected_items = self.drug_tree.selection()
        if not selected_items:
            messagebox.showinfo("Selection Required", "Please select a drug to add")
            return
            
        # Get selected drug details
        drug_values = self.drug_tree.item(selected_items[0], "values")
        drug_id = drug_values[0]
        
        # Skip if it's the placeholder row
        if drug_id == "No matching drugs found":
            return
            
        # Check if drug is already in the list
        if drug_id in [drug["id"] for drug in self.selected_drugs]:
            messagebox.showinfo("Already Added", "This drug is already in your prescription list")
            return
            
        # Add drug to selected drugs list
        drug_name = drug_values[1]
        commercial_name = drug_values[2]
        
        self.selected_drugs.append({
            "id": drug_id,
            "name": drug_name,
            "commercial_name": commercial_name,
            "dosage": ""  # Initialize with empty dosage
        })
        
        # Update the UI with the selected drugs
        self.update_drug_list()
    
    def update_drug_list(self):
        """Update the UI to show the list of selected drugs"""
        # Clear existing widgets
        for widget in self.selected_drugs_frame.winfo_children():
            widget.destroy()
        
        # Recreate the list of selected drugs
        if not self.selected_drugs:
            ctk.CTkLabel(
                self.selected_drugs_frame, 
                text="No medications selected", 
                fg_color="transparent",
                font=ctk.CTkFont(size=14, slant="italic"),
                text_color="gray50"
            ).pack(pady=15)
        else:
            for i, drug in enumerate(self.selected_drugs):
                # Create a frame for each drug with its details and dosage
                drug_container = ctk.CTkFrame(self.selected_drugs_frame, fg_color="transparent")
                drug_container.pack(fill="x", pady=10, padx=10)
                
                # Drug header with name and remove button
                drug_header = ctk.CTkFrame(drug_container, fg_color="transparent")
                drug_header.pack(fill="x")
                
                drug_text = f"{drug['name']} ({drug['commercial_name']})"
                ctk.CTkLabel(
                    drug_header, 
                    text=drug_text,
                    font=ctk.CTkFont(size=14, weight="bold")
                ).pack(side="left", padx=5)
                
                remove_btn = ctk.CTkButton(
                    drug_header, 
                    text="✕", 
                    width=36, 
                    height=28, 
                    fg_color="#dc3545", 
                    hover_color="#c82333", 
                    command=lambda idx=i: self.remove_drug(idx),
                    font=ctk.CTkFont(size=14)
                )
                remove_btn.pack(side="right", padx=5)
                
                # Dosage instructions for this specific drug
                dosage_label = ctk.CTkLabel(
                    drug_container,
                    text="Dosage Instructions:",
                    font=ctk.CTkFont(size=12),
                    anchor="w"
                )
                dosage_label.pack(anchor="w", padx=5, pady=(5, 2))
                
                # Textbox for dosage instructions
                dosage_entry = ctk.CTkTextbox(
                    drug_container,
                    height=60,
                    width=400,
                    wrap="word",
                    font=ctk.CTkFont(size=12),
                    border_width=1,
                    border_color="#e0e0e0",
                    corner_radius=4
                )
                dosage_entry.pack(fill="x", padx=5, pady=(0, 5))
                
                # Insert current dosage if it exists
                if drug["dosage"]:
                    dosage_entry.insert("1.0", drug["dosage"])
                
                # Store reference to this entry so we can update the drug's dosage when changed
                # Use tag_bind to update the drug's dosage whenever the text changes
                dosage_entry.bind("<KeyRelease>", lambda event, idx=i, entry=dosage_entry: self.update_drug_dosage(idx, entry))
                
                # Add a separator line between drugs
                if i < len(self.selected_drugs) - 1:
                    separator = ctk.CTkFrame(self.selected_drugs_frame, height=1, fg_color="#e0e0e0")
                    separator.pack(fill="x", padx=15, pady=5)
    
    def update_drug_dosage(self, index, entry_widget):
        """Update the dosage for a specific drug in the selected_drugs list"""
        if 0 <= index < len(self.selected_drugs):
            dosage_text = entry_widget.get("1.0", "end-1c").strip()
            self.selected_drugs[index]["dosage"] = dosage_text
    
    def remove_drug(self, index):
        """Remove a drug from the selected drugs list"""
        if 0 <= index < len(self.selected_drugs):
            del self.selected_drugs[index]
            self.update_drug_list()
    
    def go_back(self): # Cancel the consultation means that the appointment is cancelled, not the consultation itself.
        confirm = messagebox.askyesno("Cancel Consultation", "Are you sure you want to cancel this consultation?")
        if confirm:
            self.controller.selected_appointment.change_status("Cancelled")
            self.controller.selected_appointment = None
            self.controller.selected_patient = None
            self.clear_fields()
            self.controller.show_frame("DoctorConsultation")
            return
        return
    
    def end_consultation(self):
        """Save the consultation data and complete the appointment"""
        # Get the diagnosis details
        title = self.title_entry.get().strip()
        description = self.description_entry.get("1.0", "end-1c").strip()
        treatment = self.treatment_entry.get("1.0", "end-1c").strip()
        
        # Validate required fields
        if not title:
            messagebox.showerror("Error", "Please enter a diagnosis title")
            return
        
        if not description:
            messagebox.showerror("Error", "Please enter a diagnosis description")
            return
        
        # Look if all drugs have dosage instructions
        if self.selected_drugs:
            missing_dosage = False
            for drug in self.selected_drugs:
                if not drug["dosage"].strip():
                    missing_dosage = True
                    break
            
            if missing_dosage:
                messagebox.showerror("Error", "Please provide dosage instructions for all medications")
                return
        
        # Confirm completion
        confirm = messagebox.askyesno(
            "Complete Consultation", 
            "Are you sure you want to complete this consultation? This will save the diagnosis and medication information. Once completed you cannot undo this action."
        )
        
        if not confirm:
            return
            
        # Get the relevant IDs
        appointment = self.controller.selected_appointment
        patient = self.controller.selected_patient
        doctor_id = self.controller.current_user
        
        appointment_id = appointment.get("appointment_id")
        patient_id = patient.get_protected_attribute("hospital_id")
        
        # Create a new diagnosis
        diagnosis_id = self.controller.hospital.create_diagnosis(
            title=title,
            description=description,
            treatment=treatment,
            appointment_id=appointment_id,
            doctor_hid=doctor_id,
            patient_hid=patient_id
        )

        # Create individual prescriptions for each medication
        if self.selected_drugs:
            for drug in self.selected_drugs:
                # Create prescription for this specific drug
                self.controller.hospital.prescribe_medication(
                    patient_hid=patient_id,
                    doctor_hid=doctor_id,
                    diagnosis_id=diagnosis_id,
                    drug_id=drug["id"],
                    dosage=drug["dosage"],
                    appointment_id=appointment_id
                )

        # Update appointment status to completed
        appointment.change_status("Completed")

        # Send notification to patient
        self.controller.hospital.send_notification(
            receiver_hid=patient_id,
            sender_hid=doctor_id,
            title="Consultation Completed",
            type="Medical",  # Using notif_type instead of type
            message=f"Your consultation has been completed. Diagnosis: {title}. Please check your prescriptions for any medications. You can see the full report in your «diagnosis» tab."
        )

        messagebox.showinfo("Success", "Consultation completed successfully!")
        self.controller.selected_appointment = None
        self.controller.selected_patient = None
        self.clear_fields()
        self.controller.show_frame("DoctorConsultation")
            
    def clear_fields(self):
        """Clear all fields in the form"""
        self.title_entry.delete(0, "end")
        self.description_entry.delete("1.0", "end")
        self.treatment_entry.delete("1.0", "end")
        self.drug_search.delete(0, "end")
        self.selected_drugs = []
        self.update_drug_list()

    def tkraise(self, *args, **kwargs):
        """Load data when frame is raised"""
        super().tkraise(*args, **kwargs)
        self.load_patient_data()