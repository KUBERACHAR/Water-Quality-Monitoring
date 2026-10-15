import random
from datetime import datetime

def simulate_sensor_input():
    """Generates mock digital telemetry data mimicking an API payload or log stream."""
    return {
        "device_id": "virtual_node_alpha",
        "timestamp": datetime.now().isoformat(),
        # "ph": round(random.uniform(6.0, 9.0), 2),
        # "turbidity_ntu": round(random.uniform(0.5, 8.0), 2),
        # "tds_ppm": round(random.uniform(150, 550), 1)
        "ph": 8.2,
        "turbidity_ntu": 0.5,
        "tds_ppm": 300.0
    }