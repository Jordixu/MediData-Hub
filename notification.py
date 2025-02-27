from foundation import Foundation
class Notification(Foundation): # Unfinished
    """
    Represents a notification in a hospital.
    
    Attributes:
        message (str): The message of the notification.
        datetime (datetime): The date and time the notification was sent.
        sender_id (int): The ID of the sender of the notification.
        receiver_id (int): The ID of the receiver of the notification.
        
    Methods:
        get_message(): Returns the message of the notification.
        get_datetime(): Returns the date and time the notification was sent.
        get_sender(): Returns the ID of the sender of the notification.
        get_receiver(): Returns the ID of the receiver of the notification.
    """
    def __init__(self, notification_id, title, datetime, sender_hid, receiver_hid, notif_type, message = None, appointment_id = None):
        self.__notification_id = notification_id
        self.__title = title
        self.__message = message
        self.__datetime = datetime 
        self.__sender_hid = sender_hid
        self.__receiver_hid = receiver_hid
        self.__notif_type = notif_type
        self.__appointment_id = appointment_id
    
    def __str__(self):
        # for debugging purposes
        return f'{self.__message} {self.__datetime} {self.__sender_hid} {self.__receiver_hid}'