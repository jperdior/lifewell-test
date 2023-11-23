from metric_aggregation import MetricAggregation

metric_aggregation = MetricAggregation()
metric_aggregation.handle_event(
    event={"action": "insert", "variable": "foo", "value": 0}, context={}
)
metric_aggregation.handle_event(
    event={"action": "insert", "variable": "foo", "value": 1}, context={}
)
metric_aggregation.handle_event(
    event={"action": "insert", "variable": "foo", "value": 2}, context={}
)

print(metric_aggregation.get_metric())

def generate_insert_events(variable, values):
    for value in values:
        yield {"action": "insert", "variable": variable, "value": value}


insert_events = generate_insert_events("foo", [x for x in range(10000)])

epic_metric_aggregation = MetricAggregation()

for event in insert_events:
    epic_metric_aggregation.handle_event(event, {})

print(epic_metric_aggregation.get_metric())
