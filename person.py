class Person():
    def __init__(self, id, name, surname, age, gender):
        self.id = id
        self.name = name
        self.surname = surname
        self.age = age
        self.gender = gender
        self.notifications = []
        
    def get_info(self, attribute):
        getattr(self, attribute, 'Attribute not found')
    
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
    
class Person:
    def __init__(self, id, name, surname, age, gender):
        self.id = id
        self.name = name
        self.surname = surname
        self.age = age
        self.sex = gender
        self.notifications = []

    def get_info(self, attribute):
        return getattr(self, attribute, 'Attribute not found')

    def set_info(self, attribute, value):
        try:
            if type(getattr(self, attribute)) in [str, bool, float, int]:
                setattr(self, attribute, value)
            elif type(getattr(self, attribute)) in [list, set, dict]:
                getattr(self, attribute).append(value)
        except AttributeError:
            print('Attribute not found')
        except TypeError:
            print('Invalid value')
        except Exception as e:
            print(f'An error occurred: {e}')

    def add_notification(self, notification):
        self.notifications.append(notification)

    def display_last_notification(self):
        if self.notifications:
            return self.notifications[-1]
        else:
            return 'No notifications'