import customtkinter as ctk
from tkinter import ttk, messagebox
import datetime as dt
import tkinter as tk

class PatientNotifications(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Patient Notifications"
        
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
            text="My Notifications", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        header_label.pack(pady=10)

        # Treeview Frame
        frame = ctk.CTkFrame(self)
        frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        # Treeview Style - Create custom tags for read/unread
        style = ttk.Style()
        style.configure('Treeview', rowheight=30, font=('Helvetica', 12))
        style.configure('Treeview.Heading', font=('Helvetica', 13, 'bold'))
        
        # Define tag styles for read/unread messages
        style.map('Treeview', background=[('selected', '#4a6984')])
        
        # Create custom tags (will be applied to rows)
        style.configure("unread.Treeview.Row", font=('Helvetica', 12, 'bold'), background="#e6f7ff")
        style.configure("read.Treeview.Row", font=('Helvetica', 12), background="white")

        # Treeview setup
        columns = ("ID", "Sender", "Sent at", "Type", "Title", "Status")
        self.tree = ttk.Treeview(frame, columns=columns, show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)

        # Configure columns width and alignment
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Sender", width=80, anchor="center")
        self.tree.column("Sent at", width=150, anchor="center")
        self.tree.column("Type", width=120, anchor="center")
        self.tree.column("Title", width=250, anchor="w")
        self.tree.column("Status", width=80, anchor="center")

        # Configure headings with sort commands
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_treeview(c))
        
        self.tree.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Create tags for read/unread status
        self.tree.tag_configure('unread', background='#e6f7ff', font=('Helvetica', 12, 'bold'))
        self.tree.tag_configure('read', background='white', font=('Helvetica', 12))
        
        # Disable column resizing by capturing and canceling the resize events
        def block_column_resize(event):
            if self.tree.identify_region(event.x, event.y) == "separator":
                return "break"

        self.tree.bind('<Button-1>', block_column_resize)

        # Initialize sort order tracking
        self.sort_order = {col: False for col in columns}  # False = Ascending, True = Descending

        # Event binding for selection
        self.tree.bind("<<TreeviewSelect>>", self.selected)
        self.tree.bind("<Double-1>", lambda event: self.see_details())

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
        
        # View details button (right side)
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
            # Integer sorting with error handling
            def int_sort_key(x):
                try:
                    return int(x[0])
                except ValueError:
                    return 0
            items.sort(key=int_sort_key, reverse=self.sort_order[col])
        elif col == "Sent at":
            # DateTime sorting with error handling
            def datetime_sort_key(x):
                try:
                    return dt.datetime.strptime(x[0], "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    try:
                        return dt.datetime.strptime(x[0], "%Y-%m-%d %H:%M")
                    except ValueError:
                        return dt.datetime.min
            items.sort(key=datetime_sort_key, reverse=self.sort_order[col])
        else:
            # Default string sorting
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
        """Load the notifications for the current patient."""
        self.tree.delete(*self.tree.get_children())
        
        # Get patient data
        patient_data = self.controller.current_user_data
        if not patient_data:
            messagebox.showinfo("No Data", "Patient data not available.")
            return
            
        # Get notifications list
        notifications_list = patient_data.get_protected_attribute("notifications")
        if not notifications_list or notifications_list == "[]":
            messagebox.showinfo("No Notifications", "You have no notifications.")
            return
            
        # Process each notification
        for notification_id in notifications_list:
            if not isinstance(notification_id, int):
                continue
                
            # Handle list of notifications
            if isinstance(notification_id, list) and len(notification_id) == 1:
                notification_id = notification_id[0]
                
            try:
                # Get notification data
                notification = self.controller.hospital.notifications.get(notification_id)
                if not notification:
                    continue
                    
                # Extract notification details
                id = notification.get("notification_id")
                sender = notification.get("sender_hid")
                
                # Format datetime
                sent_at = notification.get("datetime")
                if isinstance(sent_at, dt.datetime):
                    sent_at = sent_at.strftime("%Y-%m-%d %H:%M")
                
                notification_type = notification.get("notif_type")
                title = notification.get("title")
                read_status = "Read" if notification.get("read") else "Unread"
                
                # Insert into treeview
                item_id = self.tree.insert(
                    "", "end", 
                    values=(id, sender, sent_at, notification_type, title, read_status)
                )
                
                # Apply tag based on read status
                if notification.get("read"):
                    self.tree.item(item_id, tags=('read',))
                else:
                    self.tree.item(item_id, tags=('unread',))
                    
            except Exception as e:
                print(f"Error loading notification {notification_id}: {e}")
                
    def see_details(self):
        """View details of the selected notification."""
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
                    # Store selected notification and navigate to details
                    self.controller.selected_notification = notification
                    self.controller.show_frame("NotificationsDetails")
                else:
                    messagebox.showerror("Error", "Notification not found.")
            except (ValueError, TypeError) as e:
                messagebox.showerror("Error", f"Failed to load notification details: {e}")
        else:
            messagebox.showerror("Error", "No notification selected.")

    def selected(self, event=None):
        """Handle selection events for the treeview."""
        pass

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.load_notifications()