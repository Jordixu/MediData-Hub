class Drug():
    def __init__(self, drug_id, name, price, company=None, prescription=False):
        self.drug_id = drug_id
        self.__name = name
        self.__price = price
        self.__company = company
        self.__prescription = prescription
        

    def __str__(self):
        return f"{self.name} costs {self.price}."

    def __repr__(self):
        return f"Drug({self.name}, {self.price})"