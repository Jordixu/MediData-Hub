class Drug():
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
        self.drug_id = drug_id
        self.__name = name
        self.__price = price
        self.__company = company
        self.__prescription = prescription
        

    def __str__(self):
        return f'{self.__name} {self.__price}'
    
    def get_all_attributes(self):
        attributes = self.__dict__
        attributes['name'] = self.__name
        attributes['price'] = self.__price
        attributes['company'] = self.__company
        attributes['prescription'] = self.__prescription
        return attributes
    
    def get(self, attribute):
        try:
            if attribute == 'drug_id':
                return self.drug_id
            return getattr(self, f'__{attribute}')
        except AttributeError:
            return f'The attribute {attribute} does not exist'
        
    def change_private_info(self, attribute, value):
        try:
            setattr(self, f'__{attribute}', value)
            return f'The {attribute} is now {value}'
        except AttributeError:
            return f'The attribute {attribute} does not exist'
        
    def change_info(self, attribute, value):
        try:
            setattr(self, attribute, value)
            return f'The {attribute} is now {value}'
        except AttributeError:
            return f'The attribute {attribute} does not exist'
    
    # TO BE IMPLEMENTED...