import customtkinter as ctk
from tkinter import ttk, messagebox
import datetime as dt
import tkinter as tk

class AdminNotifications(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Admin Notifications"

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
            text="Notifications Management", 
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
        columns = ("ID", "Title", "Date/Time", "Sender", "Receiver", "Type", "Appointment ID", "Read")
        self.tree = ttk.Treeview(frame, columns=columns, show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)

        # columns width and alignment
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Title", width=200, anchor="w")
        self.tree.column("Date/Time", width=150, anchor="center")
        self.tree.column("Sender", width=70, anchor="center")
        self.tree.column("Receiver", width=70, anchor="center")
        self.tree.column("Type", width=100, anchor="center")
        self.tree.column("Appointment ID", width=100, anchor="center")
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
            command=lambda: self.controller.show_frame("AdminMainScreen"),
            width=150,
            height=40,
            fg_color="#555555",
            hover_color="#666666"
        )
        self.back_button.pack(side=tk.LEFT, padx=10)
        
        # Action buttons (right side)
        action_buttons = ctk.CTkFrame(button_frame, fg_color="transparent")
        action_buttons.pack(side=tk.RIGHT)
        
        self.view_button = ctk.CTkButton(
            action_buttons, 
            text="View Details", 
            command=self.view_notification,
            width=150,
            height=40,
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        self.view_button.pack(side=tk.LEFT, padx=10)

        self.delete_button = ctk.CTkButton(
            action_buttons, 
            text="Delete Notification", 
            command=self.delete_notification,
            width=150,
            height=40,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        self.delete_button.pack(side=tk.LEFT, padx=10)

    def sort_treeview(self, col):
        # Get all items and their current values in the selected column
        items = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]
        
        # Determine sorting key based on column type
        if col in ("ID", "Sender", "Receiver", "Appointment ID"):
            # Integer sorting with N/A handling
            def int_sort_key(x):
                if x[0] == "N/A":
                    return -999999 if self.sort_order[col] else 999999
                try:
                    return int(x[0])
                except ValueError:
                    return 0
            items.sort(key=int_sort_key, reverse=self.sort_order[col])
        elif col == "Date/Time":
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
        """Load all notifications in the system."""
        self.tree.delete(*self.tree.get_children(''))
        
        # Get all notifications from the hospital
        notifications = self.controller.hospital.notifications
        
        if not notifications:
            messagebox.showinfo("No Notifications", "There are no notifications in the system.")
            return
            
        for notification_id, notification in notifications.items():
            try:
                notif_id = notification.get("notification_id")
                title = notification.get("title") if notification.get("title") else "N/A"
                
                # Format datetime
                datetime_val = notification.get("datetime")
                if isinstance(datetime_val, dt.datetime):
                    datetime_str = datetime_val.strftime("%Y-%m-%d %H:%M")
                elif isinstance(datetime_val, str):
                    datetime_str = datetime_val
                else:
                    datetime_str = "N/A"
                    
                sender_id = notification.get("sender_hid")
                receiver_id = notification.get("receiver_hid")
                notif_type = notification.get("notif_type")
                appointment_id = notification.get("appointment_id") if notification.get("appointment_id") else "N/A"
                read_status = "Read" if notification.get("read") else "Unread"
                
                # Insert the row and get the item ID
                item_id = self.tree.insert(
                    "", "end", 
                    values=(notif_id, title, datetime_str, sender_id, receiver_id, notif_type, appointment_id, read_status)
                )
                
                # Apply tag based on read status
                if notification.get("read"):
                    self.tree.item(item_id, tags=('read',))
                else:
                    self.tree.item(item_id, tags=('unread',))
                    
            except Exception as e:
                # Skip notifications that cause errors
                print(f"Exception loading notification {notification_id}: {e}")
                continue

    def selected(self, event=None):
        """
        Handle selection events for the treeview.
        """
        _ = event  # To avoid the unused variable warning

    def view_notification(self):
        """
        View details of the selected notification.
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
                    self.controller.show_frame("NotificationsDetails")
                else:
                    messagebox.showwarning("Not Found", f"Notification ID {notification_id} could not be found.")
            except (ValueError, TypeError) as e:
                messagebox.showerror("Error", f"Failed to load notification details: {e}")

    def delete_notification(self):
        """
        Delete the selected notification.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a notification to delete.")
            return
            
        notification_values = self.tree.item(selected_item[0], "values")
        try:
            notification_id = int(notification_values[0])
            
            # Confirm deletion
            confirm = messagebox.askyesno(
                "Confirm Deletion", 
                f"Are you sure you want to delete notification {notification_id}?"
            )
            
            if confirm:
                # Delete the notification
                self.controller.hospital.remove_notification(notification_id)
                messagebox.showinfo("Success", f"Notification {notification_id} has been deleted.")
                self.load_notifications()  # Refresh the list
        except ValueError as e:
            messagebox.showerror("Error", f"Failed to delete notification: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.load_notifications()