from pydantic import BaseModel, field_validator, ValidationInfo
from exceptions import (InvalidActionException, MissingValueException, MissingOldValueException)
from typing import Optional

class EventValueObject(BaseModel):
    action: str
    variable: str
    value: Optional[int] = None
    old_value: Optional[int] = None

    @field_validator("action")
    def validate_action(cls, v: str) -> str:
        if v not in ["insert", "delete", "modify"]:
            raise InvalidActionException()
        return v
    
    @field_validator("value")
    def validate_value(cls, value: int, info: ValidationInfo) -> int:
        if info.data["action"] in ["insert", "modify"] and value is None:
            raise MissingValueException()
        return value
    
    @field_validator("old_value")
    def validate_old_value(cls, v, info: ValidationInfo) -> int:
        if info.data["action"] in ["delete", "modify"] and v is None:
            raise MissingOldValueException()
        return v
