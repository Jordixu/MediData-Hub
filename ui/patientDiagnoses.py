import customtkinter as ctk
from tkinter import ttk, messagebox
import tkinter as tk
import datetime as dt

class PatientDiagnoses(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Patient Diagnoses"

        # Configure the main layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Treeview
        self.grid_rowconfigure(2, weight=0)  # Buttons
        
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(20, 10))
        
        header_label = ctk.CTkLabel(
            header_frame, 
            text="Your Diagnoses", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        header_label.pack(pady=10)

        # Treeview Frame
        frame = ctk.CTkFrame(self)
        frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        # Treeview Style
        style = ttk.Style()
        style.configure('Treeview', rowheight=30, font=('Helvetica', 12))
        style.configure('Treeview.Heading', font=('Helvetica', 13, 'bold'))
        
        # Define tag styles
        style.map('Treeview', background=[('selected', '#4a6984')])
        
        # Treeview setup
        columns = ("ID", "Date", "Doctor", "Condition", "Status")
        self.tree = ttk.Treeview(frame, columns=columns, show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)

        # columns width and alignment
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Date", width=100, anchor="center")
        self.tree.column("Doctor", width=150, anchor="center")
        self.tree.column("Condition", width=200, anchor="center")
        self.tree.column("Status", width=100, anchor="center")

        # Configure headings with sort commands
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c))
        
        self.tree.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Configure status tags
        self.status_colors = {
            'Active': '#ffebeb',    # Light red
            'Resolved': '#ebf7eb',  # Light green
            'Chronic': '#e6f7ff',   # Light blue
            'Monitoring': '#fff9e6' # Light yellow
        }
        
        for status, color in self.status_colors.items():
            self.tree.tag_configure(status.lower(), background=color)
        
        # Disable column resizing
        def block_column_resize(event):
            if self.tree.identify_region(event.x, event.y) == "separator":
                return "break"

        self.tree.bind('<Button-1>', block_column_resize)

        # Initialize sort order tracking
        self.sort_order = {col: False for col in columns}  # False = Ascending, True = Descending

        # Event binding for selection
        self.tree.bind("<<TreeviewSelect>>", self.selected)

        # Action buttons frame
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="ew")
        
        # Back button (left side)
        self.back_button = ctk.CTkButton(
            button_frame, 
            text="Go Back", 
            command=lambda: self.controller.show_frame("PatientMainScreen"),
            width=150,
            height=40,
            fg_color="#555555",
            hover_color="#666666"
        )
        self.back_button.pack(side=tk.LEFT, padx=10)
        
        # Action buttons (right side)
        action_buttons = ctk.CTkFrame(button_frame, fg_color="transparent")
        action_buttons.pack(side=tk.RIGHT)
        
        # View Details button
        self.details_button = ctk.CTkButton(
            action_buttons, 
            text="View Details", 
            command=self.view_diagnosis_details,
            width=150,
            height=40,
            fg_color="#3498db",
            hover_color="#2980b9",
        )
        self.details_button.pack(side=tk.LEFT, padx=10)

    def sort_treeview(self, col):
        # Get all items and their current values in the selected column
        items = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]
        
        # Determine sorting key based on column type
        if col in ("ID", "Doctor"):
            # Integer sorting with N/A handling
            def int_sort_key(x):
                if x[0] == "N/A":
                    return -999999 if self.sort_order[col] else 999999
                try:
                    return int(x[0])
                except ValueError:
                    return 0
            items.sort(key=int_sort_key, reverse=self.sort_order[col])
        elif col == "Date":
            # Date sorting with N/A handling
            def date_sort_key(x):
                if x[0] == "N/A":
                    return dt.datetime.min if self.sort_order[col] else dt.datetime.max
                try:
                    return dt.datetime.strptime(x[0], "%Y-%m-%d")
                except ValueError:
                    return dt.datetime.min
            items.sort(key=date_sort_key, reverse=self.sort_order[col])
        else:
            # Default string sorting for other columns
            items.sort(key=lambda x: str(x[0]).lower(), reverse=self.sort_order[col])
        
        # Rearrange items in Treeview
        for index, (value, item) in enumerate(items):
            self.tree.move(item, '', index)
        
        # Toggle sort order and update heading
        self.sort_order[col] = not self.sort_order[col]
        self.update_heading_arrow(col)

    def update_heading_arrow(self, col):
        # Remove existing arrows from all columns
        for column in self.tree["columns"]:
            text = self.tree.heading(column)["text"]
            text = text.replace("   ˄", "").replace("   ˅", "")
            self.tree.heading(column, text=text)
        
        # Add arrow to current column
        arrow = "   ˅" if self.sort_order[col] else "   ˄"
        current_text = self.tree.heading(col)["text"]
        self.tree.heading(col, text=current_text + arrow)

    def load_diagnoses(self):
        """Load the diagnoses from the controller's patient data."""
        self.tree.delete(*self.tree.get_children())
        patient_data = self.controller.current_user_data
        
        if not patient_data or patient_data.get_protected_attribute("diagnoses") == "[]" or patient_data.get_protected_attribute("diagnoses") == None:
            messagebox.showinfo("No Diagnoses", "You have no diagnoses recorded.")
            return
            
        for diagnosis_id in patient_data.get_protected_attribute("diagnoses"):
            if not isinstance(diagnosis_id, int):
                continue
                
            try:
                diagnosis = self.controller.hospital.diagnoses.get(diagnosis_id)
                if not diagnosis:
                    continue
                    
                diag_id = diagnosis.get("diagnosis_id")
                
                # Format date
                date_val = diagnosis.get("date")
                if date_val and date_val != "N/A":
                    if isinstance(date_val, dt.date):
                        date = date_val.strftime("%Y-%m-%d")
                    else:
                        date = str(date_val)
                else:
                    date = "N/A"
                
                doctor = diagnosis.get("doctor_hid", "N/A")
                condition = diagnosis.get("condition", "N/A")
                status = diagnosis.get("status", "N/A")
                
                # Insert the row and get the item ID
                item_id = self.tree.insert(
                    "", "end", 
                    values=(diag_id, date, doctor, condition, status)
                )
                
                # Apply tag based on status
                if status.lower() in [s.lower() for s in self.status_colors.keys()]:
                    self.tree.item(item_id, tags=(status.lower(),))
                    
            except ValueError as exc:
                messagebox.showerror("Error", str(exc))
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def selected(self, event=None):
        """
        Handle selection events for the treeview.
        """
        _ = event  # To avoid the unused variable warning

    def view_diagnosis_details(self):
        """
        Send the user to the diagnosis details screen.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a diagnosis to view details.")
            return
            
        diagnosis_values = self.tree.item(selected_item[0], "values")
        diagnosis_id = int(diagnosis_values[0])
        
        try:
            diagnosis = self.controller.hospital.diagnoses.get(diagnosis_id)
            if not diagnosis:
                messagebox.showerror("Error", f"Diagnosis {diagnosis_id} not found.")
                return
                
            self.controller.current_diagnosis = diagnosis
            self.controller.show_frame("DiagnosisDetails")
        except ValueError as exc:
            messagebox.showerror("Error", str(exc))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to view diagnosis details: {e}")

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.load_diagnoses()