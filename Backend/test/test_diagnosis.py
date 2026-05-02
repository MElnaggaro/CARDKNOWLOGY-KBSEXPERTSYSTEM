import sys
from pathlib import Path

# Add Backend directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from engine.runner import run_diagnosis

#Test 1:This test checks whether the system can correctly produce a diagnosis when given strong, relevant symptoms.
# purpose : Validates correctness of outputs 
def test_chf_diagnosis():
    inputs = {
        "symptoms": {
            "shortness_of_breath": True,
            "orthopnea": True,
            "edema": True,
        },
        "vitals": {},
        "background": {
            "heart_disease": True,
        },
    }

    result = run_diagnosis(inputs)

    assert result["primary_disease"] is not None
    assert result["confidence"] > 0.5


#test 2: Runs the same input twice and compares results. 
#This test checks for consistency in the diagnosis engine's outputs, ensuring that the same inputs yield the same diagnosis and confidence levels across multiple runs.
# purpose:
# Ensures the system is Deterministic , Not random ,Produces stable reasoning

def test_consistency():
    inputs = {
        "symptoms": {
            "shortness_of_breath": True,
            "orthopnea": True,
            "edema": True,
        },
        "vitals": {},
        "background": {
            "heart_disease": True,
        },
    }

    result1 = run_diagnosis(inputs)
    result2 = run_diagnosis(inputs)

    assert result1["primary_disease"] == result2["primary_disease"]
    assert result1["confidence"] == result2["confidence"]


#test 3: Checks that the system provides a proper explanation format
# purpose: 
# Ensures the system :Explains its decisions, Returns structured reasoning, Supports transparency (important in healthcare)

def test_explanation_structure():
    inputs = {
        "symptoms": {"edema": True},
        "vitals": {},
        "background": {},
    }

    result = run_diagnosis(inputs)

    explanation = result["explanation"]

    assert "fired_rules" in explanation
    assert "key_facts" in explanation
    assert "all_conditions" in explanation
    assert isinstance(explanation["fired_rules"], list)



#test 4: Test that the diagnosis engine handles edge cases gracefully, such as when no inputs are provided or when all inputs are Invalid.
@pytest.mark.parametrize("bad_input", [
    {},
    {"symptoms": {}, "vitals": {}, "background": {}},
])
def test_edge_cases(bad_input):
    result = run_diagnosis(bad_input)

    assert result is not None



#test 5: Tests input with irrelevant or insufficient symptom.
# Consolidated Weak/Incomplete Data Test
@pytest.mark.parametrize("weak_inputs", [
    {"symptoms": {"shortness_of_breath": True}}, # This alone is not specific enough for a diagnosis
    {"symptoms": {"fatigue": True}},              # Fatigue is very non-specific and should not trigger a diagnosis on its own
    {"symptoms": {"cough": True}}                 # Additional edge case
])
def test_insufficient_evidence(weak_inputs):
    # This covers the logic that the system is 'safe' and doesn't guess
    inputs = {"symptoms": {}, "vitals": {}, "background": {}, **weak_inputs}
    result = run_diagnosis(inputs)
    
    # more specific evidence to fire rules (Specificity > Sensitivity)
    assert result["primary_disease"] is None
    assert len(result["explanation"]["fired_rules"]) == 0


# Test 6: Conflict Resolution & Priority
# Purpose: Ensures that when multiple diseases are triggered, 
# the system correctly selects the one with the highest Certainty Factor.
def test_disease_differentiation():
    inputs = {
        "symptoms": {
            "palpitations": True,    # Suggests AFib
            "chest_pain": True,      # Suggests MI/ACS
            "syncope": True          # Suggests MI/SCA
        },
        "vitals": {
            "hr_100_120": True       # Suggests AFib
        },
        "background": {
            "previous_heart_attack": True # Heavily suggests MI
        }
    }

    result = run_diagnosis(inputs)

    # Even though AFib rules might fire (due to palpitations/HR), 
    # MI should have a much higher CF due to previous_heart_attack and chest_pain.
    assert result["primary_disease"] == "Acute Myocardial Infarction"
    assert "Atrial Fibrillation" in result["explanation"]["all_conditions"]
    
    # Validation of logic: MI confidence should be higher than AFib confidence
    mi_cf = result["explanation"]["all_conditions"]["Acute Myocardial Infarction"]
    afib_cf = result["explanation"]["all_conditions"]["Atrial Fibrillation"]
    assert mi_cf > afib_cf




    # Test 7: Chained Reasoning (Multistage Inference)
# Purpose: Ensures the engine can perform forward chaining where one 
# inferred conclusion acts as a fact for a subsequent rule.
def test_chained_inference_adhf():
    # Provide inputs that trigger Chronic Heart Failure (CHF) first
    # and then add a vital sign that triggers the ADHF chain (Rule R6 or R9)
    inputs = {
        "symptoms": {
            "shortness_of_breath": True,
            "low_activity": True,
            "edema": True
        },
        "vitals": {
            "spo2_85_90": True  # This vital sign, combined with CHF, triggers ADHF
        },
        "background": {
            "hypertension": True
        }
    }

    result = run_diagnosis(inputs)

    # The system should first infer CHF (Moderate) and then upgrade it 
    # to ADHF (High/Critical) because of the low SpO2.
    assert result["primary_disease"] == "Acute Decompensated Heart Failure"
    
    # Check the explanation facility to see if both rules are present
    fired_rules = result["explanation"]["fired_rules"]
    
    # Ensure a CHF rule fired to provide the foundation for the ADHF rule
    # CHF rules are R12-R16; ADHF rules are R1-R9
    has_chf_rule = any(r in fired_rules for r in ["R12", "R13", "R14", "R15", "R16"])
    has_adhf_chain = any(r in fired_rules for r in ["R6", "R9"])
    
    assert has_chf_rule, "Should have inferred Chronic Heart Failure first"
    assert has_adhf_chain, "Should have used CHF to chain into ADHF"

    # 8. REALISTIC SCENARIO TEST (Ahmed Hassan Case) 
def test_ahmed_hassan_scenario():
    # case study
    inputs = {
        "symptoms": {
            "shortness_of_breath": True, "orthopnea": True, "edema": True,
            "chest_tightness": True, "cough": True, "low_activity": True, "dizziness": True
        },
        "vitals": {
            "bp_140_179": True, "hr_100_120": True, "rr_gt_22": True, "spo2_90_94": True
        },
        "background": {
            "hypertension": True, "diabetes": True, "heart_disease": True, "obesity": True, "smoking": True
        }
    }
    result = run_diagnosis(inputs)
    assert result["primary_disease"] == "Acute Decompensated Heart Failure"
    assert result["urgency"] == "HIGH"
    assert result["confidence"] > 0.90