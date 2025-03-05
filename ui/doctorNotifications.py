import customtkinter as ctk
from tkinter import ttk, messagebox
import datetime as dt
import tkinter as tk

class DoctorNotifications(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Doctor Notifications"

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
            text="Your Notifications", 
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
        
        # Define tag styles for read/unread messages
        style.map('Treeview', background=[('selected', '#4a6984')])
        
        # Create custom tags
        style.configure("unread.Treeview.Row", font=('Helvetica', 12, 'bold'), background="#e6f7ff")
        style.configure("read.Treeview.Row", font=('Helvetica', 12), background="white")

        # Treeview setup
        columns = ("ID", "Title", "Sent at", "Sender", "Type", "Read")
        self.tree = ttk.Treeview(frame, columns=columns, show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)

        # columns width and alignment
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Title", width=250, anchor="w")
        self.tree.column("Sent at", width=150, anchor="center")
        self.tree.column("Sender", width=70, anchor="center")
        self.tree.column("Type", width=150, anchor="center")
        self.tree.column("Read", width=80, anchor="center")

        # Configure headings with sort commands
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c))
        
        self.tree.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Create tags for read/unread status
        self.tree.tag_configure('unread', background='#e6f7ff', font=('Helvetica', 12, 'bold'))
        self.tree.tag_configure('read', background='white', font=('Helvetica', 12))
        
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
            command=lambda: self.controller.show_frame("DoctorMainScreen"),
            width=150,
            height=40,
            fg_color="#555555",
            hover_color="#666666"
        )
        self.back_button.pack(side=tk.LEFT, padx=10)
        
        # Action buttons (right side)
        self.see_details_button = ctk.CTkButton(
            button_frame, 
            text="View Details", 
            command=self.see_details,
            width=150,
            height=40,
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        self.see_details_button.pack(side=tk.RIGHT, padx=10)

    def sort_treeview(self, col):
        # Get all items and their current values in the selected column
        items = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]
        
        # Determine sorting key based on column type
        if col in ("ID", "Sender"):
            # Integer sorting with N/A handling
            def int_sort_key(x):
                if x[0] == "N/A":
                    return -999999 if self.sort_order[col] else 999999
                try:
                    return int(x[0])
                except ValueError:
                    return 0
            items.sort(key=int_sort_key, reverse=self.sort_order[col])
        elif col == "Sent at":
            # DateTime sorting with N/A handling
            def datetime_sort_key(x):
                if x[0] == "N/A":
                    return dt.datetime.min if self.sort_order[col] else dt.datetime.max
                try:
                    return dt.datetime.strptime(x[0], "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    try:
                        return dt.datetime.strptime(x[0], "%Y-%m-%d %H:%M")
                    except ValueError:
                        return dt.datetime.min
            items.sort(key=datetime_sort_key, reverse=self.sort_order[col])
        else:
            # Default string sorting for other columns (like Title, Type)
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

    def load_notifications(self):
        """Load the notifications from the controller's doctor data."""
        self.tree.delete(*self.tree.get_children())
        doctor_data = self.controller.current_user_data
        
        if not doctor_data or not hasattr(doctor_data, "get_protected_attribute"):
            messagebox.showinfo("No Notifications", "No doctor data available.")
            return
            
        notifications = doctor_data.get_protected_attribute("notifications")
        if not notifications or notifications == [] or notifications == "[]":
            self.tree.insert("", "end", values=("N/A", "No notifications found", "N/A", "N/A", "N/A", "N/A"))
            return
            
        for notification_id in notifications:
            if not isinstance(notification_id, int):
                continue
                
            if isinstance(notification_id, list) and len(notification_id) == 1:
                notification_id = notification_id[0]
                
            try:
                notification = self.controller.hospital.notifications.get(notification_id)
                if not notification:
                    continue
                    
                id = notification.get("notification_id")
                title = notification.get("title", "N/A")
                
                # Format datetime
                datetime_val = notification.get("datetime")
                if isinstance(datetime_val, dt.datetime):
                    sent_at = datetime_val.strftime("%Y-%m-%d %H:%M")
                elif isinstance(datetime_val, str):
                    sent_at = datetime_val
                else:
                    sent_at = "N/A"
                    
                sender = notification.get("sender_hid", "N/A")
                notification_type = notification.get("notif_type", "N/A")
                read_status = "Read" if notification.get("read") else "Unread"
                
                # Insert the row and get the item ID
                item_id = self.tree.insert(
                    "", "end", 
                    values=(id, title, sent_at, sender, notification_type, read_status)
                )
                
                # Apply tag based on read status
                if notification.get("read"):
                    self.tree.item(item_id, tags=('read',))
                else:
                    self.tree.item(item_id, tags=('unread',))
                    
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

                
    def see_details(self):
        """
        Handle the see details button action.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("No Selection", "Please select a notification to view.")
            return
            
        items = self.tree.item(selected_item[0], "values")
        if items:
            try:
                notification_id = int(items[0])
                notification = self.controller.hospital.notifications.get(notification_id)
                if notification:
                    self.controller.selected_notification = notification
                    if notification.get("notif_type") == "Appointment Request" and notification.get("read") == False:
                        self.controller.show_frame("DoctorNotificationsDetailsRequest")
                    else:
                        self.controller.show_frame("NotificationsDetails")
                else:
                    messagebox.showwarning("Not Found", f"Notification ID {notification_id} could not be found.")
            except (ValueError, TypeError) as e:
                messagebox.showerror("Error", f"Failed to load notification details: {e}")

    def selected(self, event=None):
        """
        Handle selection events for the treeview.
        """
        _ = event  # To avoid the unused variable warning

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.load_notifications()