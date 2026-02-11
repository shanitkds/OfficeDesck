import numpy as np

def ai_performance_analysis(attendance, task, review):
    """
    Advanced NumPy-based AI performance analysis
    - Normalized KPIs
    - Weighted performance index
    - Consistency-aware adjustment
    """

    # 1️⃣ Normalize KPI values (0–1 scale)
    kpis = np.array([
        attendance / 40.0,
        task / 40.0,
        review / 20.0
    ], dtype=float)

    # 2️⃣ KPI importance weights (domain knowledge)
    weights = np.array([0.4, 0.4, 0.2], dtype=float)

    # 3️⃣ Base performance index
    base_score = np.dot(kpis, weights) * 100  # 0–100

    # 4️⃣ Consistency factor (low variance = better)
    variance = np.var(kpis)
    consistency_penalty = variance * 10  # small, controlled penalty

    final_score = max(0, base_score - consistency_penalty)

    # 5️⃣ Professional HR classification
    if final_score >= 80:
        level = "EXCELLENT"
    elif final_score >= 65:
        level = "GOOD"
    elif final_score >= 45:
        level = "AVERAGE"
    else:
        level = "POOR"

    return {
        "base_score": round(base_score, 2),
        "final_score": round(float(final_score), 2),
        "performance_level": level
    }
