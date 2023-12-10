
class UniqueSlugError(Exception):
    """
    Exception raised when a unique slug cannot be created.

    Attributes:
        name (str): The name used to generate the slug.
        type (str): The type of the object for which the slug is being generated.
        msg (str, optional): A custom error message. Defaults to None.

    Methods:
        __str__: Returns a string representation of the exception.
    """
    def __init__(self, name, type, msg=None):
        self.name = name
        self.type = type
        self.msg = msg
        super().__init__(f"Unable to create a unique slug for name: {name}, type: {type}")
    
    def __str__(self):
        if self.msg:
            return f"\n\n {self.msg}: <name: {self.name}, type: {self.type}> \n\n"
        else:
            return f"\n\n Unable to create a unique slug for name: {self.name}, type: {self.type} \n\n"

