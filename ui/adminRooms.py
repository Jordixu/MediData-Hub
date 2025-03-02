import datetime as dt
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry 
import customtkinter as ctk

class AdminRooms(ctk.CTkFrame):    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Admin Rooms"
        self.selected_date = dt.date.today()
        
        # Header section
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame, 
            text="Room Management", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(side="left")
        
        # Date selection frame
        date_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        date_frame.pack(side="right")
        
        date_label = ctk.CTkLabel(
            date_frame, 
            text="Select Date:", 
            font=ctk.CTkFont(size=14)
        )
        date_label.pack(side=tk.LEFT, padx=10)

        # Date picker
        self.date_picker = DateEntry(
            date_frame, 
            width=15, 
            background='white',
            foreground='black', 
            borderwidth=2,
            font=('Helvetica', 12),
            date_pattern='yyyy-mm-dd',
            year=self.selected_date.year,
            month=self.selected_date.month,
            day=self.selected_date.day
        )
        self.date_picker.pack(side=tk.LEFT, padx=10, pady=5, ipady=2)
        self.date_picker.bind("<<DateEntrySelected>>", self.on_date_change)

        # Main frame for treeview
        frame = ctk.CTkFrame(self)
        frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        # Treeview Style
        style = ttk.Style()
        style.configure(
            'Treeview', 
            background='white', 
            foreground='black', 
            rowheight=30, 
            fieldbackground='#e5e5e5', 
            font=('Helvetica', 14)
        )
        style.configure('Treeview.Heading', font=('Helvetica', 16, 'bold'))
        style.map('Treeview', background=[('selected', '#2D5A88')]) 
        

        base_columns = ("Number", "Floor")
        hours = [f"{h:02d}:00" for h in range(9, 21)]
        columns = base_columns + tuple(hours)
        
        # Create Treeview
        self.tree = ttk.Treeview(
            frame, 
            columns=columns, 
            show='headings', 
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)

        self.sort_order = {col: False for col in base_columns}
        
        # Configure headings with sort commands
        for col in base_columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c))
            self.tree.column(col, width=100, anchor='center')
            
        # Configure hour columns
        for hour in hours:
            self.tree.heading(hour, text=hour)
            self.tree.column(hour, width=60, anchor='center')
            
        self.tree.pack(expand=True, fill='both')
        
        # Event binding for selection
        self.tree.bind("<<TreeviewSelect>>", self.selected)

        # Legend frame
        legend_frame = ctk.CTkFrame(self)
        legend_frame.pack(fill='x', padx=20, pady=5)

        ctk.CTkLabel(
            legend_frame, 
            text="Legend:", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side=tk.LEFT, padx=10)

        available_label = ctk.CTkLabel(
            legend_frame, 
            text="O - Available", 
            fg_color="green", 
            text_color="white", 
            corner_radius=5,
            font=ctk.CTkFont(size=12)
        )
        available_label.pack(side=tk.LEFT, padx=10, pady=5)

        booked_label = ctk.CTkLabel(
            legend_frame, 
            text="X - Booked", 
            fg_color="red", 
            text_color="white", 
            corner_radius=5,
            font=ctk.CTkFont(size=12)
        )
        booked_label.pack(side=tk.LEFT, padx=10, pady=5)

        # Action buttons
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill='x', padx=20, pady=(10, 20))
        
        # Left side buttons
        left_buttons = ctk.CTkFrame(button_frame, fg_color="transparent")
        left_buttons.pack(side="left")
        
        self.back_button = ctk.CTkButton(
            left_buttons, 
            text="Go Back", 
            command=lambda: self.controller.show_frame("AdminMainScreen"),
            width=120,
            height=35,
            fg_color="#555555",
            hover_color="#666666",
            font=ctk.CTkFont(size=14)
        )
        self.back_button.pack(side="left", padx=(0, 10))
        
        self.view_appointments_button = ctk.CTkButton(
            left_buttons, 
            text="View Room Appointments", 
            command=self.view_room_appointments,
            width=200,
            height=35,
            fg_color="#003366",
            hover_color="#004080",
            font=ctk.CTkFont(size=14)
        )
        self.view_appointments_button.pack(side="left", padx=10)
        
        # Right side buttons
        right_buttons = ctk.CTkFrame(button_frame, fg_color="transparent")
        right_buttons.pack(side="right")
        
        self.delete_button = ctk.CTkButton(
            right_buttons, 
            text="Close Room", 
            command=self.close_room,
            width=150,
            height=35,
            fg_color="#E53E3E",
            hover_color="#C53030",
            font=ctk.CTkFont(size=14)
        )
        self.delete_button.pack(side="right", padx=(10, 0))
        
        self.add_button = ctk.CTkButton(
            right_buttons, 
            text="Open Room", 
            command=self.open_room,
            width=150,
            height=35,
            fg_color="#38A169",
            hover_color="#2F855A",
            font=ctk.CTkFont(size=14)
        )
        self.add_button.pack(side="right", padx=10)
        
    def on_date_change(self, _):
        self.selected_date = self.date_picker.get_date()
        self.load_rooms()
        
    def sort_treeview(self, col):
        items = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]
        
        if col == "Number" or col == "Floor":
            def int_sort_key(x):
                if x[0] == "N/A":
                    return -999999 if self.sort_order[col] else 999999
                try:
                    return int(x[0])
                except ValueError:
                    return 0
            items.sort(key=int_sort_key, reverse=self.sort_order[col])
        else:
            # Default string sorting for other columns
            items.sort(key=lambda x: str(x[0]).lower(), reverse=self.sort_order[col])
        
        # Rearrange items in Treeview
        for index, (_, item) in enumerate(items):
            self.tree.move(item, '', index)
        
        self.sort_order[col] = not self.sort_order[col]
        self.update_heading_arrow(col)

    def update_heading_arrow(self, col):
        # Remove existing arrows from all columns
        for column in ["Number", "Floor"]:
            text = self.tree.heading(column)["text"]
            text = text.replace("   ˄", "").replace("   ˅", "")
            self.tree.heading(column, text=text)
        
        # Add arrow to current column
        arrow = "   ˅" if self.sort_order[col] else "   ˄"
        current_text = self.tree.heading(col)["text"]
        self.tree.heading(col, text=current_text + arrow)
    
    def get_appointments_for_date_room(self, room_number, date):
        appointments = []
        
        try:
            all_appointments = self.controller.hospital.appointments
            
            # Filter appointments for this room and date
            for appt_id, appointment in all_appointments.items():
                if (appointment.get('room_number') == room_number and 
                    appointment.get('date') == date.strftime('%Y-%m-%d')):
                    appointments.append(appointment)
        except Exception as e:
            print(f"Error getting appointments: {e}")
            
        return appointments

    def load_rooms(self):
        self.tree.delete(*self.tree.get_children(''))
        
        # Get all rooms from the hospital
        try:
            rooms = self.controller.hospital.rooms
            
            if not rooms:
                return
                    
            hours = [f"{h:02d}:00" for h in range(9, 21)]
            
            # Get selected date as a date object for comparison
            selected_date = self.selected_date
                
            for room_id, room_obj in rooms.items():
                try:
                    # Get room attributes
                    number = room_obj.get("number")
                    floor = room_obj.get("floor")
                    availability = room_obj.display_schedule()
                    
                    # Create a row with base data
                    row_values = [number, floor]
                    
                    # Check availability for each hour slot
                    for hour_str in hours:
                        # Parse the hour and create time objects
                        hour_time = dt.datetime.strptime(hour_str, "%H:%M").time()
                        
                        # Default to available
                        is_available = False
                        
                        # Check availability for this date and time
                        for avail_date, timeframes in availability.items():
                            if avail_date == selected_date:
                                # Found our date, now check timeframes
                                for time_tuple, avail_status in timeframes.items():
                                    start_time, end_time = time_tuple
                                    
                                    # Check if our hour falls within this timeframe
                                    if (start_time.hour == hour_time.hour and 
                                        start_time.minute == hour_time.minute):
                                        is_available = avail_status
                                        break
                                break
                        
                        # The og idea was to place color codes here, but treeview doesn't support it (modifying each cell)
                        if is_available:
                            status = "O"  # Available
                        else:
                            status = "X"  # Booked
                        
                        row_values.append(status)
                    
                    # Insert row with all values
                    self.tree.insert("", "end", values=tuple(row_values))
                    
                except (AttributeError, KeyError, ValueError) as e:
                    # Skip rooms that cause errors
                    print(f"Exception loading room {room_id}:", e)
                    continue
                    
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def selected(self, event=None):
        """
        Handle selection events for the treeview.
        """
        _ = event # To avoid the unused variable warning
        selected_item = self.tree.selection()
        if selected_item:
            items = self.tree.item(selected_item[0], "values")
            # print("Selected row:", items)

    def modify_room(self):
        """Navigate to the room modification screen with the selected room."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a room to modify.")
            return
            
        room_values = self.tree.item(selected_item[0], "values")
        try:
            room_number = int(room_values[0])
            room = self.controller.hospital.rooms.get(room_number)
            
            if room:
                self.controller.selected_room = room
                self.controller.show_frame("AdminModifyRoom")
            else:
                messagebox.showerror("Error", f"Room with number {room_number} not found.")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid room number: {e}")

    def close_room(self):
        """Delete the selected room."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a room to close.")
            return
            
        ans = messagebox.askyesno("Confirm Close", "Are you sure you want to close this room?")
        try:
            if ans:
                self.controller.hospital.close_room(int(self.tree.item(selected_item[0], "values")[0]))
                self.load_rooms()
                messagebox.showinfo("Room Closed", "The room has been closed.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while closing the room: {e}")
            
    def open_room(self):
        """Open the selected room."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a room to open.")
            return
            
        ans = messagebox.askyesno("Confirm Open", "Are you sure you want to open this room?")
        try:
            if ans:
                self.controller.hospital.open_room(int(self.tree.item(selected_item[0], "values")[0]))
                self.load_rooms()
                messagebox.showinfo("Room Opened", "The room has been opened.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while opening the room: {e}")
            
    def view_room_appointments(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a room to view appointments.")
            return
            
        room_values = self.tree.item(selected_item[0], "values")
        try:
            room_number = int(room_values[0])
            room = self.controller.hospital.rooms.get(room_number)
            
            if room:
                self.controller.selected_room = room
                self.controller.show_frame("AdminViewAppointmentsRoom")
            else:
                messagebox.showerror("Error", f"Room with number {room_number} not found.")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid room number: {e}")

    def tkraise(self, *args, **kwargs):
        """Override tkraise to refresh room data when screen is shown."""
        super().tkraise(*args, **kwargs)
        self.load_rooms()