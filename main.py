from metric_aggregation import MetricAggregation

def generate_insert_events(variable, values):
    for value in values:
        yield {'action': 'insert', 'variable': variable, 'value': value}

insert_events = generate_insert_events('foo', [x for x in range(10000)])

epic_metric_aggregation = MetricAggregation()

for event in insert_events:
    epic_metric_aggregation.handle_event(event, {})

print(epic_metric_aggregation.get_metric())