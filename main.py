from metric_aggregation import MetricAggregation

metric_aggregation = MetricAggregation()

metric_aggregation.handle_event(event={
    'action': 'insert',
    'variable': 'foo',
    'value': 0
},context={})
metric_aggregation.handle_event(event={
    'action': 'insert',
    'variable': 'foo',
    'value': 1
}, context={})
metric_aggregation.handle_event(event={
    'action': 'insert',
    'variable': 'foo',
    'value': 2
},context={})

print(metric_aggregation.get_metric())

metric_aggregation_serveral_var = MetricAggregation()

metric_aggregation_serveral_var.handle_event(event={
    'action': 'insert',
    'variable': 'foo',
    'value': 0
},context={})

metric_aggregation_serveral_var.handle_event(event={
    'action': 'insert',
    'variable': 'foo',
    'value': 1
}, context={})

metric_aggregation_serveral_var.handle_event(event={
    'action': 'insert',
    'variable': 'foo',
    'value': 2
},context={})

metric_aggregation_serveral_var.handle_event(event={
    'action': 'insert',
    'variable': 'bar',
    'value': 1
},context={})

metric_aggregation_serveral_var.handle_event(event={
    'action': 'insert',
    'variable': 'bar',
    'value': 1
},context={})

metric_aggregation_serveral_var.handle_event(event={
    'action': 'insert',
    'variable': 'bar',
    'value': 1
},context={})

print(metric_aggregation_serveral_var.get_metric())

metric_aggregation_modify = MetricAggregation()

metric_aggregation_modify.handle_event(event={
    'action': 'insert',
    'variable': 'foo',
    'value': 0
},context={})

metric_aggregation_modify.handle_event(event={
    'action': 'modify',
    'variable': 'foo',
    'value': 1,
    'old_value': 0
}, context={})

metric_aggregation_modify.handle_event(event={
    'action': 'insert',
    'variable': 'foo',
    'value': 2
},context={})

print(metric_aggregation_modify.get_metric())

metric_aggregation_delete = MetricAggregation()

metric_aggregation_delete.handle_event(event={
    'action': 'insert',
    'variable': 'foo',
    'value': 0
},context={})

metric_aggregation_delete.handle_event(event={
    'action': 'delete',
    'variable': 'foo',
    'old_value': 0
}, context={})

metric_aggregation_delete.handle_event(event={
    'action': 'insert',
    'variable': 'foo',
    'value': 2
},context={})

print(metric_aggregation_delete.get_metric())

def generate_insert_events(variable, values):
    for value in values:
        yield {'action': 'insert', 'variable': variable, 'value': value}

insert_events = generate_insert_events('foo', [x for x in range(10000)])

epic_metric_aggregation = MetricAggregation()

for event in insert_events:
    epic_metric_aggregation.handle_event(event, {})

print(epic_metric_aggregation.get_metric())