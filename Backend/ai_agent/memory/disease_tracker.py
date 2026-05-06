class DiseaseTracker:
    """Tracks suspected diseases and their confidence levels over time."""
    
    def __init__(self):
        self.hypotheses = {}  # {disease_name: confidence}
        self.diagnosis_history = []

    def update_hypothesis(self, disease: str, confidence: float):
        self.hypotheses[disease] = confidence
        self.diagnosis_history.append({"disease": disease, "confidence": confidence})

    def get_top_hypotheses(self, limit: int = 3):
        sorted_h = sorted(self.hypotheses.items(), key=lambda x: x[1], reverse=True)
        return sorted_h[:limit]
