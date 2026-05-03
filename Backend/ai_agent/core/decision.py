class DecisionMaker:
    """Hard-coded rules or heuristics for agent decisions (complementary to LLM)."""
    
    @staticmethod
    def should_escalate(vitals: dict) -> bool:
        """Determines if a situation is critical based on vitals."""
        critical_vitals = ["bp_gte_180", "hr_gt_120", "spo2_lt_85"]
        for vital in critical_vitals:
            if vitals.get(vital) is True:
                return True
        return False

    @staticmethod
    def is_diagnosis_complete(kbs_result: dict) -> bool:
        """Checks if the KBS has enough information for a high-confidence diagnosis."""
        confidence = kbs_result.get("confidence", 0)
        return confidence > 0.8
