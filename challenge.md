# Summary

You are tasked with creating a metrics aggregation component.
This function is part of an _event-based_, _serverless_ backend system. 
It will receive events and is expected to keep a list of aggregation metrics for all the variables it has received.
It should not store each of the events it receives.

You must create a python class called `MetricAggregation` that implements, at least, the following two methods: `handle_event` and `get_metrics`.
Expected behavior is described below

## `handle_event`

This is the main event handler. This method will be continuously invoked with new events and should return `None`.

The expected signature is:
`def handle_event(self, event: dict, context: dict) -> None:`

### Input

`event` has the following structure:

``` python
{
    "body": {
        "action": "insert", # one of: insert, delete, modify
        "value": 0, # int, only present for "insert" and "modify" events
        "old_value": 1, # int, only present for "delete" and "modify" events
        "variable": "foo", # variable name
    },
    ... # other event fields can be ignored
}
```

Disregard the `context` variable.

### Output

This method should return `None`

### Exceptions

This method is expected to raise exceptions in reasonable cases (e.g. validation error).
You are free to add exceptions where sensible.

## `get_metrics`

This method should get no input and return a dict of all aggregated data. In particular, it should return the `average` and `standard deviation` of all the metrics it has seen.

The expected signautre is:
`def get_metrics(self):`

### Input

No input

### Output

A dict with the `average` and `standard deviation` of all the metrics seen in events.

``` python
{
    "a": {
        "average": 2,
        "std_dev": 0.2
    },
    "b": {
        "average": 1,
        "std_dev": 0.1
    },
    ...
}
```

## Notes

- Do not use AI/LLMs to figure out/code your solution (ChatGPT, CoPilot, etc.). These tools make it harder for us to gauge your coding hability. We won't like it if you use them.
- Do not handle json-string serialization/deserialization. Input/output are dicts, not json-strings.
- For this exercise, store metrics in memory. In a real environment, metrics would be stored in a separate DB.
- Remember to use best coding practices (SOLID).
- Code is written once and read 100 times. Think about the readability of your code.
- You're free to consider if/how to perform validation, logging and aggregation.
- Think about the memory and time complexity of your solution. We're aiming for O(1) time and space/memory complexity.
- For incremental formulas of average and std_dev, this article may help: http://datagenetics.com/blog/november22017/index.html

## Equations

### Average

Given a list of n elements, the arithmetic mean is calculated as follows:
``` python
average = sum([x_1, x_2, ..., x_n]) / n
```

If a number is inserted, we can calculate the new mean based on the previous mean as follows:
``` python
average_n = average_n_minus_1 + (x_n - average_n_minus_1) / n
```

Conversely, if a number is removed, we can calculate the new mean by inverting the previous equation:
``` python
average_n_minus_1 = ((n * average_n) - x_n) / (n - 1)
```


### Std Dev

The Variance is the average squared distance from each element of a distribution to the arithmetic mean.
Standard Deviation is the square root of the Variance.

The Standard Deviation of a single number is 0.

If a number is inserted, we can calculate the new std_dev based on the previous std_dev, and the previous and new averages as follows:
``` python
variance_n_minus_1 = std_dev_n_minus_1 ** 2

term_1 = (n - 1) * variance_n_minus_1 
term_2 = (x_n - average_n_minus_1) * (x_n - average_n)

variance_n = (term_1 + term_2) / (n) 

std_dev_n = variance_n ** 0.5 
```

Conversely, if a number is deleted, we can calculate the new std_dev by inverting the previous equation:
```
variance_n = std_dev_n ** 2

variance_n_minus_1 = ((variance_n * n) - (x_n - average_n) * (x_n - average_n_minus_1)) / (n - 1)

std_dev_n_minus_1 = variance_n_minus_1 ** 0.5 
```


## Example Cases

### Simple Case

```
- `handle_event() invoked with {"body": {"action": "insert", "value": 0, "variable": "foo"}}
- `handle_event() invoked with {"body": {"action": "insert", "value": 1, "variable": "foo"}}
- `handle_event() invoked with {"body": {"action": "insert", "value": 2, "variable": "foo"}}

- `get_metrics() invoked. Returns {"foo": {"average": 1, "std_dev": 0.81649658092773}}
```

### Multiple Variable Case

```
- `handle_event() invoked with {"body": {"action": "insert", "value": 0, "variable": "foo"}}
- `handle_event() invoked with {"body": {"action": "insert", "value": 1, "variable": "foo"}}
- `handle_event() invoked with {"body": {"action": "insert", "value": 2, "variable": "foo"}}
- `handle_event() invoked with {"body": {"action": "insert", "value": 1, "variable": "bar"}}
- `handle_event() invoked with {"body": {"action": "insert", "value": 1, "variable": "bar"}}
- `handle_event() invoked with {"body": {"action": "insert", "value": 1, "variable": "bar"}}


- `get_metrics() invoked. Returns {"foo": {"average": 1, "std_dev": 0.81649658092773}, "bar": {"average": 1, "std_dev": 0}}
```

### Modify Case

```
- `handle_event() invoked with {"body": {"action": "insert", "value": 0, "variable": "foo"}}
- `handle_event() invoked with {"body": {"action": "modify", "value": 1, "old_value": 0, "variable": "foo"}}
- `handle_event() invoked with {"body": {"action": "insert", "value": 2, "variable": "foo"}}

- `get_metrics() invoked. Returns {"foo": {"average": 1.5, "std_dev": 0.5}}
```

### Delete Case

```
- `handle_event() invoked with {"body": {"action": "insert", "value": 0, "variable": "foo"}}
- `handle_event() invoked with {"body": {"action": "delete", "old_value": 0, "variable": "foo"}}
- `handle_event() invoked with {"body": {"action": "insert", "value": 2, "variable": "foo"}}

- `get_metrics() invoked. Returns {"foo": {"average": 2, "std_dev": 0}}
```

