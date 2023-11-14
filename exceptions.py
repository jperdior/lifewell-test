class InvalidActionException(Exception):
    
    def __init__(self):
        super().__init__("action must be insert, delete or modify")
        
class MissingValueException(Exception):

    def __init__(self):
        super().__init__("value must be specified for insert or modify")

class MissingOldValueException(Exception):

    def __init__(self):
        super().__init__("old_value must be specified for delete or modify")
