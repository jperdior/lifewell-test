class EventValueObject:

    def __init__(self, action: str, variable: str,value: int = None, old_value: int = None):
        if action not in ['insert', 'delete','modify']:
            raise ValueError('action must be insert, delete or modify')
        self.action = action
        if action in ['insert','modify'] and value is None:
            raise ValueError('value must be specified for insert or modify')
        self.value = value
        if action in ['delete','modify'] and old_value is None:
            raise ValueError('old_value must be specified for delete or modify')
        self.old_value = old_value
        self.variable = variable