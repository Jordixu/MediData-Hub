import datetime as dt
class Foundation:
    """
    This class is the foundation for all classes in the hospital system (excluding the main class and the UI).
    
    Methods:
        set(attribute, value, value_type): Changes the value of an attribute.
        get(attribute): Returns the value of the attribute.
        get_protected_attribute(attribute): Returns the value of a protected attribute.
        set_protected_info(attribute, value, type): Changes the value of a protected attribute.
        get_all_attributes(): Returns all the attributes of the object.
    """
    def set(self, attribute, value, value_type):
        """
        Changes the value of a private attribute.

        Args:
            attribute (str): The name of the attribute.
            value: The new value for the attribute.
            value_type (str): The type of the value ('int', 'str', 'float', 'bool').

        Raises:
            AttributeError: If the attribute is not found.
            TypeError: If the value type is invalid.
            ValueError: If an error occurs in setting the attribute.
        """
        try:
            mangled_name = f"_{self.__class__.__name__}__{attribute}"
            if value_type == 'int':
                setattr(self, mangled_name, int(value))
            elif value_type == 'str':
                setattr(self, mangled_name, str(value))
            elif value_type == 'float':
                setattr(self, mangled_name, float(value))
            elif value_type == 'bool':
                setattr(self, mangled_name, bool(value))
        except AttributeError as exc:
            raise AttributeError('Attribute not found') from exc
        except TypeError as exc:
            raise TypeError('Invalid value') from exc
        except ValueError as exc:
            raise ValueError('An error occurred in setting the attribute') from exc

    def get(self, attribute):
        """
        Get the value of a private attribute.
        
        Args:
            attribute (str): The name of the attribute.
            
        Returns:
            The value of the attribute.
            
        Raises:
            AttributeError: If the attribute is not found.
            TypeError: If the value type is invalid.
            ValueError: If an error occurs in getting the attribute.
        """
        try:
            mangled_name = f"_{self.__class__.__name__}__{attribute}"
            return getattr(self, mangled_name)
        except AttributeError as exc:
            raise AttributeError('Attribute not found') from exc
        except TypeError as exc:
            raise TypeError('Invalid value') from exc
        except Exception as exc:
            raise ValueError('An error occurred in getting the attribute') from exc
        
    def get_protected_attribute(self, attribute):
        """
        Get the value of a protected attribute.
        
        Args:
            attribute (str): The name of the attribute.
            
        Returns:
            The value of the attribute.
        
        Raises:
            AttributeError: If the attribute is not found.
            TypeError: If the value type is invalid.
            ValueError: If an error occurs in getting the attribute.
        """
        try:
            return getattr(self, "_" + attribute)
        except AttributeError as exc:
            raise AttributeError('Attribute not found') from exc
        except TypeError as exc:
            raise TypeError('Invalid value') from exc
        except Exception as exc:
            raise ValueError('An error occurred in getting the attribute') from exc
        
    def set_protected_info(self, attribute, value, type):
        """
        Set the value of a protected attribute.
        
        Args:
            attribute (str): The name of the attribute.
            value: The new value for the attribute.
            type (str): The type of the value ('int', 'str', 'float', 'bool').
        
        Raises:
            AttributeError: If the attribute is not found.
            TypeError: If the value type is invalid.
            ValueError: If an error occurs in setting the attribute.
        """
        try:
            if type == 'int':
                setattr(self, "_" + attribute, int(value))
            elif type == 'str':
                setattr(self, "_" + attribute, str(value))
            elif type == 'float':
                setattr(self, "_" + attribute, float(value))
            elif type == 'bool':
                setattr(self, "_" + attribute, bool(value))
        except AttributeError as exc:
            raise AttributeError('Attribute not found') from exc
        except TypeError as exc:
            raise TypeError('Invalid value') from exc
        except Exception as exc:
            raise ValueError('An error occurred in setting the attribute') from exc
        
    def get_all_attributes(self):
        """
        Get all the attributes of the object.
        
        Returns:
            A dictionary containing all the attributes of the object.
        """
        attributes = self.__dict__.copy()
        result = {}
        for attribute, value in attributes.items():
            if isinstance(value, tuple): # Convert time tuples to strings
                if isinstance(value[0], dt.time) and isinstance(value[1], dt.time):
                    value = (value[0].strftime('%H:%M:%S'), value[1].strftime('%H:%M:%S'))
            if isinstance(value, dt.date): # Convert date objects to strings
                value = value.strftime('%Y-%m-%d')
            if isinstance(value, dict):
                if isinstance(value.keys(), dt.date):
                    value = {key.strftime('%Y-%m-%d'): value[key] for key in value.keys()}
            if attribute.startswith(f"_{self.__class__.__name__}__"): # Remove name mangling
                result[attribute.split(f"_{self.__class__.__name__}__")[1]] = value
            elif attribute.startswith('_'): # Remove protected attribute prefix
                result[attribute[1:]] = value
            else:
                result[attribute] = value
        return result