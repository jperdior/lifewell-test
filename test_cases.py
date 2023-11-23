from metric_aggregation import MetricAggregation


def test_simple_case():
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
    assert metric_aggregation.get_metric() == {
        "foo": {"average": 1.0, "std_dev": 0.816496580927726}
    }


def test_several_variables():
    metric_aggregation_serveral_var = MetricAggregation()
    metric_aggregation_serveral_var.handle_event(
        event={"action": "insert", "variable": "foo", "value": 0}, context={}
    )
    metric_aggregation_serveral_var.handle_event(
        event={"action": "insert", "variable": "foo", "value": 1}, context={}
    )
    metric_aggregation_serveral_var.handle_event(
        event={"action": "insert", "variable": "foo", "value": 2}, context={}
    )
    metric_aggregation_serveral_var.handle_event(
        event={"action": "insert", "variable": "bar", "value": 1}, context={}
    )
    metric_aggregation_serveral_var.handle_event(
        event={"action": "insert", "variable": "bar", "value": 1}, context={}
    )
    metric_aggregation_serveral_var.handle_event(
        event={"action": "insert", "variable": "bar", "value": 1}, context={}
    )
    assert metric_aggregation_serveral_var.get_metric() == {
        "foo": {"average": 1.0, "std_dev": 0.816496580927726},
        "bar": {"average": 1.0, "std_dev": 0.0},
    }


def test_modify_event():
    metric_aggregation_modify = MetricAggregation()
    metric_aggregation_modify.handle_event(
        event={"action": "insert", "variable": "foo", "value": 0}, context={}
    )

    metric_aggregation_modify.handle_event(
        event={"action": "modify", "variable": "foo", "value": 1, "old_value": 0},
        context={},
    )

    metric_aggregation_modify.handle_event(
        event={"action": "insert", "variable": "foo", "value": 2}, context={}
    )
    assert metric_aggregation_modify.get_metric() == {
        "foo": {"average": 1.5, "std_dev": 0.5}
    }


def test_delete_event():
    metric_aggregation_delete = MetricAggregation()
    metric_aggregation_delete.handle_event(
        event={"action": "insert", "variable": "foo", "value": 0}, context={}
    )

    metric_aggregation_delete.handle_event(
        event={"action": "delete", "variable": "foo", "old_value": 0}, context={}
    )

    metric_aggregation_delete.handle_event(
        event={"action": "insert", "variable": "foo", "value": 2}, context={}
    )
    assert metric_aggregation_delete.get_metric() == {
        "foo": {"average": 2.0, "std_dev": 0.0}
    }


def test_wrong_action():
    metric_aggregation_wrong_action = MetricAggregation()
    try:
        metric_aggregation_wrong_action.handle_event(
            event={"action": "wrong", "variable": "foo", "value": 0}, context={}
        )
    except Exception as e:
        assert type(e).__name__ == "InvalidActionException"


def test_missing_value():
    metric_aggregation_missing_value = MetricAggregation()
    try:
        metric_aggregation_missing_value.handle_event(
            event={
                "action": "insert",
                "variable": "foo",
            },
            context={},
        )
    except Exception as e:
        assert type(e).__name__ == "MissingValueException"


def test_missing_old_value():
    metric_aggregation_missing_old_value = MetricAggregation()
    try:
        metric_aggregation_missing_old_value.handle_event(
            event={
                "action": "delete",
                "variable": "foo",
            },
            context={},
        )
    except Exception as e:
        assert type(e).__name__ == "MissingOldValueException"
