_traces = {}

def start_trace(request_id):
    _traces[request_id] = []

def add_trace_step(request_id, step):
    _traces.setdefault(request_id, []).append(step)

def get_traces(request_id=None):
    if request_id:
        return _traces.get(request_id, [])
    return _traces
