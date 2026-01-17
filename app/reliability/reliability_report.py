from app.observability.metrics import get_metrics
from app.observability.trace_store import get_traces


def generate_reliability_report():
    return {
        "metrics": get_metrics(),
        "traces": get_traces(),
        "summary": {
            "fallback_rate": get_metrics().get("failures", 0),
            "system_status": "stable"
        }
    }
