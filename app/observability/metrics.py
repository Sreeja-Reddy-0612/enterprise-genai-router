_metrics = {
    "total_requests": 0,
    "by_model": {},
    "failures": 0
}

def record_request(model_name: str, success: bool):
    _metrics["total_requests"] += 1
    _metrics["by_model"].setdefault(model_name, 0)
    _metrics["by_model"][model_name] += 1

    if not success:
        _metrics["failures"] += 1


def get_metrics():
    return _metrics
