from foundation import Foundation

class Drug(Foundation):
    """
    This class represents a drug in the hospital system.
    
    Attributes:
        drug_id (int): The ID of the drug.
        name (str): The name of the drug.
        price (float): The price of the drug.
        company (str): The company that produces the drug.
        prescription (bool): Whether the drug requires a prescription.
        
    Methods:
        get_all_attributes(): Returns all the attributes of the drug.
        get(attribute): Returns the value of the attribute.
        change_private_info(attribute, value): Changes the value of a private attribute.
        change_info(attribute, value): Changes the value of an attribute.
    """
    def __init__(self, drug_id, name, price, company=None, prescription=False):
        self.__drug_id = drug_id
        self.__name = name
        self.__price = price
        self.__company = company
        self.__prescription = prescription
        

    def __str__(self):
        return f'{self.__name} {self.__price}'
    
    # TO BE IMPLEMENTED...