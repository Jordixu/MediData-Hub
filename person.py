class Person():
    def __init__(self, personal_id, hospital_id, password, name, surname, age, gender):
        self.personal_id = personal_id
        self.hospital_id = hospital_id
        self._password = password
        self.name = name
        self.surname = surname
        self.age = age
        self.gender = gender
        self._notifications = []
        
    def get(self, attribute):
        try:
            return getattr(self, attribute)
        except AttributeError:
            print('Attribute not found')
        except TypeError:
            print('Invalid value')
        except:
            print('An error occurred')
        
    def __name__(self):
        return self.name + ' ' + self.surname
    
    def check_password(self, password):
        return self._password == password
    
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
        except AttributeError:
            print('Attribute not found')
        except TypeError:
            print('Invalid value')
        except:
            print('An error occurred')
        
            
    def add_notification(self, notification):
        self._notifications.append(notification)
        
    def display_last_notification(self):
        return self._notifications[-1]
    
    def get_all_attributes(self):
        return self.__dict__