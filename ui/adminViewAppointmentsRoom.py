from tkinter import ttk, messagebox
import datetime as dt
import customtkinter as ctk
import tkinter as tk

class AdminViewAppointmentsRoom(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Room Appointments"
        
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
            text="Room Appointments", 
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
        
        # Create status tags
        self.status_colors = {
            'Scheduled': '#e6f7ff',  # Light blue
            'Completed': '#ebf7eb',  # Light green
            'Canceled': '#ffebeb',   # Light red
            'Pending': '#fff9e6',    # Light yellow
            'Rejected': '#f7e6f7'    # Light purple
        }
        
        # Treeview setup
        columns = ("ID", "Date", "Time", "Doctor", "Patient", "Status")
        self.tree = ttk.Treeview(frame, columns=columns, show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)

        # columns width and alignment
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Date", width=100, anchor="center")
        self.tree.column("Time", width=150, anchor="center")
        self.tree.column("Doctor", width=100, anchor="center")
        self.tree.column("Patient", width=100, anchor="center")
        self.tree.column("Status", width=100, anchor="center")

        # Configure headings with sort commands
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c))
        
        self.tree.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Configure status tags
        for status, color in self.status_colors.items():
            self.tree.tag_configure(status.lower(), background=color)
        
        # Disable column resizing
        self.tree.bind('<Button-1>', self.block_column_resize)

        # Initialize sort order tracking
        self.sort_order = {col: False for col in columns}  # False = Ascending, True = Descending

        # Action buttons frame
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="ew")
        
        # Back button (left side)
        self.back_button = ctk.CTkButton(
            button_frame, 
            text="Go Back", 
            command=self.go_back,
            width=150,
            height=40,
            fg_color="#555555",
            hover_color="#666666"
        )
        self.back_button.pack(side=tk.LEFT, padx=10)

    def block_column_resize(self, event):
        if self.tree.identify_region(event.x, event.y) == "separator":
            return "break"

    def sort_treeview(self, col):
        # Get all items and their current values in the selected column
        items = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]
        
        # Determine sorting key based on column type
        if col == "ID":
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
        elif col == "Time":
            # Time sorting with N/A handling
            def time_sort_key(x):
                if x[0] == "N/A":
                    return dt.time.min if self.sort_order[col] else dt.time.max
                try:
                    # Extract start time from range (e.g., "09:00 - 10:00")
                    start_time = x[0].split(" - ")[0]
                    return dt.datetime.strptime(start_time, "%H:%M:%S").time()
                except (ValueError, IndexError):
                    try:
                        # Try without seconds
                        start_time = x[0].split(" - ")[0]
                        return dt.datetime.strptime(start_time, "%H:%M").time()
                    except (ValueError, IndexError):
                        return dt.time.min
            items.sort(key=time_sort_key, reverse=self.sort_order[col])
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

    def load_appointments(self):
        self.tree.delete(*self.tree.get_children())

        appointments = self.controller.hospital.appointments
        
        if not appointments:
            messagebox.showinfo("No Appointments", "There are no appointments in the system.")
            return
            
        for appt_id, appointment in appointments.items():
            try:
                if appointment.get("room_number") == self.controller.selected_room.get("number"):
                    # Format date
                    date_val = appointment.get("date")
                    if date_val and date_val != "N/A":
                        if isinstance(date_val, dt.date):
                            date = date_val.strftime("%Y-%m-%d")
                        else:
                            date = str(date_val)
                    else:
                        date = "N/A"
                    
                    # Format time
                    timeframe = appointment.get("timeframe")
                    time = self.process_time_tuples(timeframe) if timeframe and timeframe != 'N/A' else "N/A"
                    
                    doctor_id = appointment.get("doctor_hid", "N/A")
                    patient_id = appointment.get("patient_hid", "N/A")
                    status = appointment.get("status", "N/A")
                    
                    # Insert the row and get the item ID
                    item_id = self.tree.insert(
                        "", "end", 
                        values=(appt_id, date, time, doctor_id, patient_id, status)
                    )
                    
                    # Apply tag based on status
                    if status.lower() in [s.lower() for s in self.status_colors.keys()]:
                        self.tree.item(item_id, tags=(status.lower(),))
            except Exception as e:
                print(f"Exception loading appointment: {e}")
                continue

    def process_time_tuples(self, time):
        """Convert a tuple of time strings or time objects to a single string."""
        if isinstance(time, tuple) and len(time) >= 2:
            start_time = time[0]
            end_time = time[1]
            
            # Handle different types of time representations
            if isinstance(start_time, dt.time) and isinstance(end_time, dt.time):
                return f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}"
            elif isinstance(start_time, str) and isinstance(end_time, str):
                return f"{start_time} - {end_time}"
            else:
                return f"{start_time} - {end_time}"
        elif isinstance(time, str) and time.startswith("(") and time.endswith(")"):
            try:
                time_parts = time.strip("()").replace("'", "").split(", ")
                return f"{time_parts[0]} - {time_parts[1]}"
            except (IndexError, AttributeError):
                return time
        return "N/A"
    
    def go_back(self):
        self.controller.selected_room = None
        self.controller.show_frame("AdminRooms")

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.load_appointments()
