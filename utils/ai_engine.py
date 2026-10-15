def analyze_water_data(ph, turbidity, tds):
    """Evaluates water quality using threshold logic and AI/WQI scoring algorithms."""
    warnings = []
    if not (6.5 <= ph <= 8.5):
        warnings.append(f"pH level ({ph}) is outside safe drinking bounds (6.5-8.5).")
    if turbidity > 5.0:
        warnings.append(f"Turbidity ({turbidity} NTU) is high — water clarity compromised.")
    if tds > 500:
        warnings.append(f"TDS ({tds} ppm) exceeds standard limit (500 ppm).")

    # AI / WQI Mathematical Scoring (0-100 scale)
    ph_score = max(0, 100 - abs(7.2 - ph) * 30)
    turbidity_score = max(0, 100 - (turbidity / 10.0) * 100)
    tds_score = max(0, 100 - (tds / 1000.0) * 100)
    wqi_score = round((ph_score * 0.4) + (turbidity_score * 0.3) + (tds_score * 0.3), 1)

    if wqi_score >= 80 and not warnings:
        status = "OPTIMAL"
    elif wqi_score >= 50:
        status = "WARNING"
    else:
        status = "HAZARDOUS"

    return status, wqi_score, warnings