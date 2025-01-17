class Notification():
    def __init__(self, message, date, time, sender, receiver):
        self.__message = message # string
        self.__date = date # date
        self.__time = time # date
        self.__sender = sender # Person: Doctor or Patient
        self.__receiver = receiver # Person: Doctor or Patient
        
    def get_message(self):
        return self.__message
    
    def get_datetime(self):
        return "The message was sent on " + self.__date + " at " + self.__time
    
    def get_sender(self):
        return self.__sender
    
    def get_receiver(self):
        return self.__receiver