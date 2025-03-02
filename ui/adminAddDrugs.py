from tkinter import messagebox
import customtkinter as ctk
import tkinter as tk

class AdminAddDrugs(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Add Drug"
        
        # Configure the main layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Title
        self.grid_rowconfigure(1, weight=1)  # Form content
        self.grid_rowconfigure(2, weight=0)  # Buttons
        
        # Title
        title_label = ctk.CTkLabel(
            self, 
            text="Add New Drug", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=(30, 20))
        
        # Main container
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=1, column=0, padx=20, sticky="n")
        
        # Drug information section
        form_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        form_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        ctk.CTkLabel(
            form_frame, 
            text="Drug Information", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", pady=(0, 15))
        
        # Name field
        ctk.CTkLabel(form_frame, text="Drug Name", anchor="w").pack(anchor="w", pady=(5, 2))
        self.name_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Enter drug name", 
            width=300, 
            height=30
        )
        self.name_entry.pack(pady=(0, 10), fill="x")
        
        # Commercial Name field
        ctk.CTkLabel(form_frame, text="Commercial Name", anchor="w").pack(anchor="w", pady=(5, 2))
        self.commercial_name_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Enter commercial name", 
            width=300, 
            height=30
        )
        self.commercial_name_entry.pack(pady=(0, 10), fill="x")
        
        # Price field
        ctk.CTkLabel(form_frame, text="Price (€)", anchor="w").pack(anchor="w", pady=(5, 2))
        self.price_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Enter price", 
            width=300, 
            height=30
        )
        self.price_entry.pack(pady=(0, 10), fill="x")
        
        # Company field
        ctk.CTkLabel(form_frame, text="Company (Optional)", anchor="w").pack(anchor="w", pady=(5, 2))
        self.company_entry = ctk.CTkEntry(
            form_frame, 
            placeholder_text="Enter manufacturer company", 
            width=300, 
            height=30
        )
        self.company_entry.pack(pady=(0, 10), fill="x")
        
        # Prescription checkbox
        self.prescription_var = tk.BooleanVar(value=False)
        self.prescription_checkbox = ctk.CTkCheckBox(
            form_frame,
            text="Requires Prescription",
            variable=self.prescription_var,
            onvalue=True,
            offvalue=False,
        )
        self.prescription_checkbox.pack(anchor="w", pady=(10, 20))
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.grid(row=2, column=0, pady=(20, 30))
        
        # Submit button
        submit_btn = ctk.CTkButton(
            buttons_frame, 
            text="Add Drug", 
            command=self.submit_data,
            width=150,
            height=35,
            fg_color="#003366",
            hover_color="#004080"
        )
        submit_btn.pack(side="left", padx=5)
        
        # Go Back button
        back_btn = ctk.CTkButton(
            buttons_frame, 
            text="Cancel", 
            command=lambda: controller.show_frame("AdminDrugs"),
            width=150,
            height=35,
            fg_color="#555555",
            hover_color="#666666"
        )
        back_btn.pack(side="left", padx=5)
    
    def clear_entries(self):
        """Clear all entry fields"""
        self.name_entry.delete(0, tk.END)
        self.commercial_name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.company_entry.delete(0, tk.END)
        self.prescription_var.set(False)
    
    def validate_price(self, price_str):
        """Validate and convert price to float"""
        try:
            price = float(price_str)
            if price <= 0:
                return False, "Price must be a positive number"
            return True, price
        except ValueError:
            return False, "Price must be a valid number"
    
    def submit_data(self):
        """Submit the drug data to be added to the database"""
        name = self.name_entry.get()
        commercial_name = self.commercial_name_entry.get()
        price_str = self.price_entry.get()
        company = self.company_entry.get()
        prescription = self.prescription_var.get()
        
        # Validate price
        valid_price, price_result = self.validate_price(price_str)
        if not valid_price:
            messagebox.showerror("Error", price_result)
            return
        
        # Validate required fields
        required_fields = [name, commercial_name, price_str]
        if not all(required_fields):
            messagebox.showerror("Error", "Please fill out all required fields")
            return
        
        try:
            self.controller.hospital.add_drug(
                name=name,
                commercial_name=commercial_name,
                price=price_result,
                company=company if company else None,
                prescription=prescription
            )
            messagebox.showinfo("Success", f"Drug '{name}' added successfully!")
            self.clear_entries()
            self.controller.show_frame("AdminDrugs")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
