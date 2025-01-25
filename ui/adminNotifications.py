import tkinter as tk
import customtkinter as ctk

class AdminNotifications(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.title = "Admin Appointments"
        
        # Create the "Go Back" button
        go_back_button = ctk.CTkButton(self, text="Go Back")
        go_back_button.pack(side="top", anchor="w", pady=(0, 10))
        

        # Create a frame for the search section
        search_frame = ctk.CTkFrame(self)
        search_frame.pack(padx=10, pady=10, fill="x")

        # Create the search label and entry fields
        search_label = ctk.CTkLabel(search_frame, text="Search for (Any)")
        search_label.grid(row=0, column=0, columnspan=2, pady=5)

        attribute1_label = ctk.CTkLabel(search_frame, text="Attribute 1:")
        attribute1_label.grid(row=1, column=0, pady=5)

        attribute1_entry = ctk.CTkEntry(search_frame)
        attribute1_entry.grid(row=1, column=1, pady=5)

        attribute2_label = ctk.CTkLabel(search_frame, text="Attribute 2:")
        attribute2_label.grid(row=2, column=0, pady=5)

        attribute2_entry = ctk.CTkEntry(search_frame)
        attribute2_entry.grid(row=2, column=1, pady=5)

        # Create the "Search" button
        search_button = ctk.CTkButton(search_frame, text="Search")
        search_button.grid(row=3, column=1, pady=5)
        

        # Create a frame for the table
        table_frame = ctk.CTkFrame(self)
        table_frame.pack(padx=10, pady=10, fill="x")

        # Create the table header
        header_frame = ctk.CTkFrame(table_frame)
        header_frame.pack(fill="x")

        attribute1_header = ctk.CTkLabel(header_frame, text="Attribute 1")
        attribute1_header.grid(row=0, column=0, padx=5, pady=5)

        other_header = ctk.CTkLabel(header_frame, text="...")
        other_header.grid(row=0, column=1, padx=5, pady=5)

        # Create rows in the table
        for i in range(4):  # Adjust the number of rows as needed
            row_frame = ctk.CTkFrame(table_frame)
            row_frame.pack(fill="x", pady=2)

            attribute1_data = ctk.CTkLabel(row_frame, text=f"Data {i+1}")
            attribute1_data.grid(row=0, column=0, padx=5, pady=5)

            other_data = ctk.CTkLabel(row_frame, text="...")
            other_data.grid(row=0, column=1, padx=5, pady=5)

            select_button = ctk.CTkButton(row_frame, text="Select")
            select_button.grid(row=0, column=2, padx=5, pady=5)

        # Create the "More" button
        more_button = ctk.CTkButton(self, text="More")
        more_button.pack(padx=10, pady=10)

        # Create a frame for the action buttons at the bottom
        action_frame = ctk.CTkFrame(self)
        action_frame.pack(padx=10, pady=10, fill="x")

        # Create action buttons
        add_button = ctk.CTkButton(action_frame, text="Add new item")
        add_button.grid(row=0, column=0, padx=5, pady=5)

        modify_button = ctk.CTkButton(action_frame, text="Modify selected")
        modify_button.grid(row=0, column=1, padx=5, pady=5)

        delete_button = ctk.CTkButton(action_frame, text="Delete selected")
        delete_button.grid(row=0, column=2, padx=5, pady=5)