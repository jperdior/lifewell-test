from .value_objects import EventValueObject
from .equations import Equations
import logging


class MetricAggregation:
    def __init__(self) -> None:
        self.variables: dict = {}

    def handle_event(self, event: dict, context: dict) -> None:
        try:
            event_object = EventValueObject(
                action=event["action"],
                variable=event["variable"],
                value=event.get("value"),
                old_value=event.get("old_value"),
            )
        except Exception as e:
            # event should go to an error queue
            logging.error(f"Invalid event: {event}, {e}")
            return
        if event_object.variable not in self.variables:
            self.new_variable(event_object.variable)
        if event_object.action == "insert":
            logging.info(f"Handling insert event: {event_object}")
            self.handle_insert_event(event_object)
        elif event_object.action == "delete":
            logging.info(f"Handling delete event: {event_object}")
            self.handle_delete_event(event_object)
        elif event_object.action == "modify":
            logging.info(f"Handling modify event: {event_object}")
            self.handle_modify_event(event_object)

    def new_variable(self, variable: str) -> None:
        self.variables[variable] = {"count": 0, "average": 0, "std_deviation": 0}

    def handle_insert_event(self, event: EventValueObject) -> None:
        old_average = self.variables[event.variable]["average"]
        self.variables[event.variable]["count"] += 1
        assert event.value is not None
        self.variables[event.variable]["average"] = Equations.update_average(
            average_n_minus_1=old_average,
            n=self.variables[event.variable]["count"],
            x_n=event.value,
        )
        old_std_deviation = self.variables[event.variable]["std_deviation"]
        variance = Equations.calculate_variance(
            x_n=event.value,
            std_deviation_n_minus_1=old_std_deviation,
            n=self.variables[event.variable]["count"],
            average_n_minus_1=old_average,
            average_n=self.variables[event.variable]["average"],
        )
        self.variables[event.variable][
            "std_deviation"
        ] = Equations.update_std_deviation(variance)

    def handle_modify_event(self, event: EventValueObject) -> None:
        self.handle_delete_event(event)
        self.handle_insert_event(event)

    def handle_delete_event(self, event: EventValueObject) -> None:
        self.variables[event.variable]["count"] -= 1
        old_average = self.variables[event.variable]["average"]
        assert event.old_value is not None
        self.variables[event.variable][
            "average"
        ] = Equations.update_average_with_delete(
            average_n=self.variables[event.variable]["average"],
            n=self.variables[event.variable]["count"],
            x_n=event.old_value,
        )
        assert event.old_value is not None
        variance = Equations.calculate_variance_from_delete(
            std_deviation_n=self.variables[event.variable]["std_deviation"] ** 2,
            x_n=event.old_value,
            average_n=old_average,
            average_n_minus_1=self.variables[event.variable]["average"],
            n=self.variables[event.variable]["count"],
        )
        self.variables[event.variable][
            "std_deviation"
        ] = Equations.update_std_deviation(variance)

    def get_metric(self) -> dict:
        metric = {}
        for variable, data in self.variables.items():
            metric[variable] = {
                "average": data["average"],
                "std_dev": data["std_deviation"],
            }

        return metric
