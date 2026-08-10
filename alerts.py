def generate_alert(vehicle_count, density):
    """
    Generate traffic alerts based on vehicle count
    and traffic density.
    """

    if density == "HIGH":
        return {
            "status": "HIGH",
            "message": "🚨 Heavy Traffic Detected",
            "recommendation": "Increase green signal timing and deploy traffic personnel."
        }

    elif density == "MEDIUM":
        return {
            "status": "MEDIUM",
            "message": "⚠ Moderate Traffic",
            "recommendation": "Monitor traffic flow closely."
        }

    else:
        return {
            "status": "LOW",
            "message": "✅ Traffic Flow Normal",
            "recommendation": "No action required."
        }