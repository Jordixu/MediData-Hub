class Drug():
    def __init__(self, name, price, company=None):
        self.__name = name
        self.__price = price
        self.__company = company
        

    def __str__(self):
        return f"{self.name} costs {self.price}."

    def __repr__(self):
        return f"Drug({self.name}, {self.price})"