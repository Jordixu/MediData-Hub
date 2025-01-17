from person import Person

"""
Aún está por determinar si al final se implementará la clase Administrator.
"""

class Administrator(Person):
    def __init__(self, id, name, surname, age, sex, salary, socialsecurity):
        super().__init__(id, name, surname, age, sex)
        self.salary = salary
        self.socialsecurity = socialsecurity