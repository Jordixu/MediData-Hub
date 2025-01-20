class Person():
    def __init__(self, personal_id, hospital_id, password, name, surname, age, gender):
        self.personal_id = personal_id
        self.hospital_id = hospital_id
        self.password = password
        self.name = name
        self.surname = surname
        self.age = age
        self.gender = gender
        self.notifications = []
        
    def get_info(self, attribute):
        getattr(self, attribute, 'Attribute not found')
        
    def __name__(self):
        return self.name + ' ' + self.surname
    
    def set_info(self, attribute, value):
        try:
            if type(self.attribute) is str or type(self.attribute) is bool or type(self.attribute) is float or type(self.attribute) is int:
                setattr(self, attribute, value)
            elif type(self.attribute) is list or type(self.attribute) is set or type(self.attribute) is dict:
                self.attribute.append(value)
        except AttributeError:
            print('Attribute not found')
        except TypeError:
            print('Invalid value')
        except:
            print('An error occurred')
            
    def add_notification(self, notification):
        self.notifications.append(notification)
        
    def display_last_notification(self):
        return self.notifications[-1]