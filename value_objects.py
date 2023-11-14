from exceptions import InvalidActionException, MissingValueException, MissingOldValueException

class EventValueObject:

    def __init__(self, action: str, variable: str,value: int = None, old_value: int = None):
        if action not in ['insert', 'delete','modify']:
            raise InvalidActionException()
        self.action = action
        if action in ['insert','modify'] and value is None:
            raise MissingValueException()
        self.value = value
        if action in ['delete','modify'] and old_value is None:
            raise MissingOldValueException()
        self.old_value = old_value
        self.variable = variable