import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

class AdminModifyDrugs(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Modify Drug"
        
        # Configure the main layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Title
        self.grid_rowconfigure(1, weight=1)  # Form content
        self.grid_rowconfigure(2, weight=0)  # Buttons
        
        # Title
        title_label = ctk.CTkLabel(
            self, 
            text="Modify Drug", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=(30, 20))
        
        # Main container
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=1, column=0, padx=20, sticky="n")
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Form fields
        form_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        form_frame.grid(row=0, column=0, padx=20, pady=10, sticky="n")
        
        # Drug ID field (read-only)
        ctk.CTkLabel(form_frame, text="Drug ID", anchor="w").pack(anchor="w", pady=(5, 2))
        self.drug_id_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Drug ID", 
            width=350, 
            height=30,
            state="disabled"  # Make it read-only
        )
        self.drug_id_entry.pack(pady=(0, 10), fill="x")
        
        # Drug Name field (read-only)
        ctk.CTkLabel(form_frame, text="Drug Name", anchor="w").pack(anchor="w", pady=(5, 2))
        self.name_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Drug Name", 
            width=350, 
            height=30,
            state="disabled"  # Make it read-only
        )
        self.name_entry.pack(pady=(0, 10), fill="x")
        
        # Commercial Name field
        ctk.CTkLabel(form_frame, text="Commercial Name", anchor="w").pack(anchor="w", pady=(5, 2))
        self.commercial_name_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Enter commercial name", 
            width=350, 
            height=30
        )
        self.commercial_name_entry.pack(pady=(0, 10), fill="x")
        
        # Price field
        ctk.CTkLabel(form_frame, text="Price (€)", anchor="w").pack(anchor="w", pady=(5, 2))
        self.price_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Enter price", 
            width=350, 
            height=30
        )
        self.price_entry.pack(pady=(0, 10), fill="x")
        
        # Company field
        ctk.CTkLabel(form_frame, text="Company", anchor="w").pack(anchor="w", pady=(5, 2))
        self.company_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Enter manufacturing company", 
            width=350, 
            height=30
        )
        self.company_entry.pack(pady=(0, 10), fill="x")
        
        # Prescription Required checkbox
        self.prescription_var = tk.BooleanVar()
        prescription_checkbox = ctk.CTkCheckBox(
            form_frame,
            text="Requires Prescription",
            variable=self.prescription_var,
            onvalue=True,
            offvalue=False,
            height=30
        )
        prescription_checkbox.pack(anchor="w", pady=(5, 15))
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.grid(row=2, column=0, pady=(20, 30))
        
        # Save Changes button
        save_btn = ctk.CTkButton(
            buttons_frame, 
            text="Save Changes", 
            command=self.save_changes,
            width=150,
            height=35,
            fg_color="#003366",
            hover_color="#004080"
        )
        save_btn.pack(side="left", padx=5)
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            buttons_frame, 
            text="Cancel", 
            command=lambda: self.go_back(),
            width=150,
            height=35,
            fg_color="#555555",
            hover_color="#666666"
        )
        cancel_btn.pack(side="left", padx=5)
        
    def go_back(self):
        """Return to the AdminDrugs screen"""
        self.controller.selected_drug = None
        self.controller.show_frame("AdminDrugs")
    
    def load_drug_data(self):
        """Load the selected drug's data into the form fields"""
        if hasattr(self.controller, 'selected_drug') and self.controller.selected_drug:
            drug = self.controller.selected_drug
            
            # Load drug information
            self.drug_id_entry.configure(state="normal")
            self.drug_id_entry.delete(0, tk.END)
            self.drug_id_entry.insert(0, drug.get("drug_id"))
            self.drug_id_entry.configure(state="disabled")
            
            self.name_entry.configure(state="normal")
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, drug.get("name"))
            self.name_entry.configure(state="disabled")
            
            self.commercial_name_entry.delete(0, tk.END)
            self.commercial_name_entry.insert(0, drug.get("commercial_name", ""))
            
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(0, str(drug.get("price", "")))
            
            self.company_entry.delete(0, tk.END)
            self.company_entry.insert(0, drug.get("company", ""))
            
            # Set prescription checkbox
            self.prescription_var.set(drug.get("prescription", False))
            
    def validate_price(self, price_str):
        """Validate and convert price to float"""
        try:
            price = float(price_str)
            if price <= 0:
                return False, "Price must be a positive number"
            return True, price
        except ValueError:
            return False, "Price must be a valid number"
    
    def save_changes(self):
        """Save the changes to the drug in the database"""
        if not hasattr(self.controller, 'selected_drug') or not self.controller.selected_drug:
            messagebox.showerror("Error", "No drug selected for modification")
            return
        
        drug = self.controller.selected_drug
        
        try:
            # Get form data
            commercial_name = self.commercial_name_entry.get().strip()
            price_str = self.price_entry.get().strip()
            company = self.company_entry.get().strip()
            requires_prescription = self.prescription_var.get()
            
            # Validate commercial name
            if not commercial_name:
                messagebox.showerror("Error", "Commercial name cannot be empty")
                return
            
            # Validate price
            is_valid, price_result = self.validate_price(price_str)
            if not is_valid:
                messagebox.showerror("Error", price_result)
                return
            
            # Update drug data
            drug.set("commercial_name", commercial_name, 'str')
            drug.set("price", price_result, 'float')
            drug.set("company", company, 'str')
            drug.set("prescription", requires_prescription, 'bool')
            
            messagebox.showinfo("Success", "Drug information updated successfully!")
            self.controller.selected_drug = None
            self.controller.show_frame("AdminDrugs")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
    
    def tkraise(self, *args, **kwargs):
        """Load drug data when the frame is raised"""
        super().tkraise(*args, **kwargs)
        self.load_drug_data()