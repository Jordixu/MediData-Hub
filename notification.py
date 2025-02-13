from foundation import Foundation
class Notification(Foundation): # Unfinished
    """
    Represents a notification in a hospital.
    
    Attributes:
        message (str): The message of the notification.
        datetime (str): The date and time the notification was sent.
        sender_id (int): The ID of the sender of the notification.
        receiver_id (int): The ID of the receiver of the notification.
        
    Methods:
        get_message(): Returns the message of the notification.
        get_datetime(): Returns the date and time the notification was sent.
        get_sender(): Returns the ID of the sender of the notification.
        get_receiver(): Returns the ID of the receiver of the notification.
    """
    def __init__(self, title, datetime, sender_id, receiver_id, notif_type, message = None):
        self.__title = title
        self.__message = message
        self.__datetime = datetime 
        self.__sender_id = sender_id
        self.__receiver_id = receiver_id
        self.__type = notif_type
    
    def __str__(self):
        # for debugging purposes
        return f'{self.__message} {self.__datetime} {self.__sender_id} {self.__receiver_id}'