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

    def get(self, attribute, default=None):
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
            return default
        
    def get_protected_attribute(self, attribute, default=None):
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
            return default
        
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
        Get all attributes of the object, converting dates/times to strings for serialization.
        
        Returns:
            A dictionary with all attributes, including nested structures.
        """
        def serialize(value):
            # Recursively serialize dates and times
            if isinstance(value, dt.date) and not isinstance(value, dt.datetime):
                return value.strftime('%Y-%m-%d')
            elif isinstance(value, dt.time):
                return value.strftime('%H:%M:%S')
            elif isinstance(value, dt.datetime):
                return value.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(value, tuple):
                # Handle tuples of time objects (e.g., timeframe tuples)
                return tuple(serialize(item) for item in value)
            elif isinstance(value, dict):
                # Serialize dictionary keys and values
                return {serialize(k): serialize(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [serialize(item) for item in value]
            elif isinstance(value, set):
                return {serialize(item) for item in value}
            else:
                return value

        attributes = self.__dict__.copy()
        result = {}
        for attribute, value in attributes.items():
            # Remove name mangling and prefixes
            if attribute.startswith(f"_{self.__class__.__name__}__"):  
                key = attribute.split(f"_{self.__class__.__name__}__")[1]
            elif attribute.startswith('_'):  
                key = attribute[1:]
            else:
                key = attribute
            
            # Serialize dates, times, and nested structures
            result[key] = serialize(value)

        return result