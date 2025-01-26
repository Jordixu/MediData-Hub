class Person():
    """
    The base class for all people in the hospital.
    
    Attributes:
        personal_id (int): The personal ID of the person.
        hospital_id (int): The hospital ID of the person.
        password (str): The password for the person's account.
        name (str): The first name of the person.
        surname (str): The surname of the person.
        birthday (date): The birth date of the person
    
    Methods:
        get(attribute): Returns the value of the attribute.
        get_private_info(attribute): Returns the value of a private attribute.
        set_private_info(attribute, value): Changes the value of a private attribute.
        __name__(): Returns the full name of the person.
        check_password(password): Checks if the password is correct.
        set_info(attribute, value, type): Changes the value of an attribute.
        add_notification(notification_id): Adds a notification to the person.
        display_last_notification(): Displays the last notification the person received.
        add_appointment(appointment_id): Adds an appointment to the person.
    """
    def __init__(self, personal_id, hospital_id, password, name, surname, birthday, gender, appointments = None):
        self.personal_id = personal_id
        self.hospital_id = hospital_id
        self.password = password
        self.name = name
        self.surname = surname
        self.birthday = birthday
        self.gender = gender
        self.appointments = appointments if appointments is not None else {}
        
    def get(self, attribute):
        try:
            return getattr(self, attribute)
        except AttributeError as exc:
            raise AttributeError('Attribute not found') from exc
        except TypeError as exc:
            raise TypeError('Invalid value') from exc
        except Exception as exc:
            raise Exception('An error occurred in getting the attribute') from exc
            
    def get_private_info(self, attribute):
        return getattr(self, "__" + attribute)
    
    def set_private_info(self, attribute, value):
        setattr(self, "__" + attribute, value)
        
    def __name__(self):
        return self.name + ' ' + self.surname
    
    def check_password(self, password):
        return self.password == password
    
    def set_info(self, attribute, value, type):
        try:
            if type == 'int':
                setattr(self, attribute, int(value))
            elif type == 'str':
                setattr(self, attribute, str(value))
            elif type == 'float':
                setattr(self, attribute, float(value))
            elif type == 'bool':
                setattr(self, attribute, bool(value))
        except AttributeError as exc:
            raise AttributeError('Attribute not found') from exc
        except TypeError as exc:
            raise TypeError('Invalid value') from exc
        except:
            raise Exception('An error occurred in setting the attribute')

    # def add_notification(self, notification_id):
    #     self.__notifications.append(notification_id)

    # def display_last_notification(self):
    #     return self.__notifications[-1]
    
    def add_appointment(self, appointment_id):
        self.appointments.append(appointment_id)