import customtkinter as ctk
from tkinter import ttk, messagebox

class DoctorNotifications(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Doctor Notifications"

        self.back_button = ctk.CTkButton(self, text="Go Back", command=lambda: self.controller.show_frame("DoctorMainScreen"))
        self.back_button.pack(pady=10)

        frame = ctk.CTkFrame(self)
        frame.pack(pady=20, expand=True, fill='both')

        style = ttk.Style()
        style.configure('Treeview', background='white', foreground='black', rowheight=30, fieldbackground='#e5e5e5', font=('Helvetica', 14))
        style.configure('Treeview.Heading', font=('Helvetica', 16, 'bold'))
        style.map('Treeview', background=[('selected', 'grey30')])

        self.tree = ttk.Treeview(frame, columns=("ID", "Sender", "Sent at", "Type", "Title"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Sender", text="Sender")
        self.tree.heading("Sent at", text="Sent at")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Title", text="Title")
        self.tree.pack(expand=True, fill='both')

        self.tree.bind("<<TreeviewSelect>>", self.selected)

        self.see_details_button = ctk.CTkButton(self, text="See Details", command=self.see_details)
        self.see_details_button.pack(side=ctk.LEFT, padx=20, pady=10)

        # self.delete_button = ctk.CTkButton(self, text="Delete Notification", command=self.delete_notification)
        # self.delete_button.pack(side=ctk.RIGHT, padx=20, pady=10)
                
    def load_notifications(self):
        """Load the notifications from the controller's doctor data."""
        self.tree.delete(*self.tree.get_children())
        doctor_data = self.controller.current_user_data
        print("Doctor Data:", doctor_data)
        print("Notifications:", doctor_data.get_protected_attribute("notifications"))
        if not doctor_data or doctor_data.get_protected_attribute("notifications") == "[]" or doctor_data.get_protected_attribute("notifications") == None:
            messagebox.showinfo("No Notifications", "You have no notifications.")
            # print("No notifications found.")
            return
        for notification_id in doctor_data.get_protected_attribute("notifications"):
            if not isinstance(notification_id, int):
                continue
            print("notification type", type(notification_id)) # Debugging purposes
            if isinstance(notification_id, list) and len(notification_id) == 1:
                notification_id = notification_id[0]
            print("Notification ID:", notification_id) # Debugging purposes
            print("Notifications:", type(doctor_data.get_protected_attribute("notifications"))) # Debugging purposes
            try:
                notification = self.controller.hospital.notifications.get(notification_id)
                id = notification.get("notification_id")
                sender = notification.get("sender_hid")
                sent_at = notification.get("datetime")
                notification_type = notification.get("notif_type")
                title = notification.get("title")
                print("Notification Data:", id, sender, sent_at, notification_type, title)
                self.tree.insert("", "end", values=(id, sender, sent_at, notification_type, title))
            except ValueError as exc:
                messagebox.showerror("Error", exc)
            except KeyError:
                messagebox.showerror("Error", "Notification data not found.")
                
    def see_details(self):
        """
        Handle the see details button action.
        """
        selected_item = self.tree.selection()
        if selected_item:
            items = self.tree.item(selected_item[0], "values")
            print("Selected row:", items)
            if items:
                print("Notification ID:", items[0], type(items[0]))
                notification = self.controller.hospital.notifications.get(int(items[0]))
                print("Notification:", notification)
                if notification:
                    self.controller.selected_notification = notification
                    if self.controller.selected_notification.get("notif_type") == "Appointment Request":
                        self.controller.show_frame("DoctorNotificationsDetailsRequest")
                    else:
                        self.controller.show_frame("DoctorNotificationsDetails")
                    
                else:
                    messagebox.showerror("Error", "Notification not found.")
            else:
                messagebox.showerror("Error", "No notification selected.")
        else:
            messagebox.showerror("Error", "No notification selected.")
            
    # def delete_notification(self):
    #     """
    #     Handle the delete notification button action.
    #     """
    #     selected_item = self.tree.selection()
    #     if selected_item:
    #         items = self.tree.item(selected_item[0], "values")
    #         # print("Selected row:", items)
    #         if items:
    #             notification = self.controller.hospital.notifications.get(items[0])
    #             if notification:
    #                 self.controller.hospital.delete_notification(notification) # Not implemented yet
    #                 self.load_notifications()
    #             else:
    #                 messagebox.showerror("Error", "Notification not found.")
    #         else:
    #             messagebox.showerror("Error", "No notification selected.")
    #     else:
    #         messagebox.showerror("Error", "No notification selected.")

    def process_time_tuples(self, time):
        """Convert a tuple of time strings to a single string."""
        return f"{time[0]} - {time[1]}"

    def selected(self, event=None):
        """
        Handle selection events for the treeview.
        """
        _ = event # To avoid the unused variable warning
        selected_item = self.tree.selection()
        if selected_item:
            items = self.tree.item(selected_item[0], "values")
            # print("Selected row:", items)

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.load_notifications()
        # print("Appointments loaded.")