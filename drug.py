from foundation import Foundation

class Drug(Foundation):
    def __init__(self, drug_id, name, commercial_name, price, company=None, prescription=False):
        self.__drug_id = drug_id
        self.__name = name
        self.__commercial_name = commercial_name
        self.__price = price
        self.__company = company
        self.__prescription = prescription
        

    def __str__(self):
        return f'{self.__name} {self.__price}'
    
    # Unfinished class