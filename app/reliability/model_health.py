from app.reliability.circuit_breaker import CircuitBreaker

MODEL_HEALTH = {}

def get_circuit(model_name):
    if model_name not in MODEL_HEALTH:
        MODEL_HEALTH[model_name] = CircuitBreaker()
    return MODEL_HEALTH[model_name]
