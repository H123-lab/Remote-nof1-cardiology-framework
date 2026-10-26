import pytest
import numpy as np
from core_pipeline import analytics

def test_bayesian_threshold_boundary_precision():
    """
    TEST 1: Verifies the exact boundary behavior of the Bayesian decision rule:
    - Probability exactly at 0.90 (Inclusive boundary threshold: >= 0.90)
    - Probability just above 0.90 (0.9001) -> Triggers active treatment selection
    - Probability just below 0.90 (0.8999) -> Triggers adaptive analytical abstention
    """
    inclusive_threshold = 0.90
    
    # 1. Exact boundary case (Inclusive: Should trigger an active decision)
    decision_exact = analytics.evaluate_posterior_decision_rule(posterior_prob=0.90, threshold=inclusive_threshold)
    assert decision_exact['Decision_Status'] == 'Active_Selection', "Inclusive threshold at exactly 0.90 failed to issue an active decision"
    
    # 2. Case just above boundary (Should trigger an active decision)
    decision_above = analytics.evaluate_posterior_decision_rule(posterior_prob=0.9001, threshold=inclusive_threshold)
    assert decision_above['Decision_Status'] == 'Active_Selection', "Posterior probability just above 0.90 failed to issue an active decision"
    
    # 3. Case just below boundary (Should trigger an automated abstention)
    decision_below = analytics.evaluate_posterior_decision_rule(posterior_prob=0.8999, threshold=inclusive_threshold)
    assert decision_below['Decision_Status'] == 'Abstain_Inconclusive', "Posterior probability just below 0.90 failed to trigger an analytical abstention"

def test_high_uncertainty_and_certain_negative_cases():
    """
    TEST 2: Verifies structural risk-mitigation profiles under challenging distributions:
    - Case A: Positive estimated effect but with high posterior variance (uncertainty)
    - Case B: Negative estimated effect with high posterior certainty
    - Case C: Standard inconclusive case falling within the region of indifference
    """
    inclusive_threshold = 0.90
    
    # Case A: Positive effect with high uncertainty (e.g., mean = +0.4 mmHg, but wide SD = 1.2)
    # Pr(delta > 0) will fall below 0.90 due to the high variance.
    prob_high_uncertainty = 0.632
    decision_uncertain = analytics.evaluate_posterior_decision_rule(posterior_prob=prob_high_uncertainty, threshold=inclusive_threshold)
    assert decision_uncertain['Decision_Status'] == 'Abstain_Inconclusive', "Positive effect with high uncertainty failed to trigger a safe abstention"
    
    # Case B: Negative effect with high certainty (e.g., Pr(delta > 0) = 0.02)
    prob_certain_negative = 0.020
    decision_negative = analytics.evaluate_posterior_decision_rule(posterior_prob=prob_certain_negative, threshold=inclusive_threshold)
    assert decision_negative['Decision_Status'] == 'Active_Rejection_Or_Maintain', "Certain negative treatment effect failed to issue a definitive rejection/maintenance action"
    
    # Case C: Standard inconclusive case (e.g., Pr(delta > 0) = 0.75)
    prob_inconclusive = 0.750
    decision_inconclusive = analytics.evaluate_posterior_decision_rule(posterior_prob=prob_inconclusive, threshold=inclusive_threshold)
    assert decision_inconclusive['Decision_Status'] == 'Abstain_Inconclusive', "Intermediate probability failed to be classified as an inconclusive outcome"

def test_manuscript_threshold_agreement():
    """
    TEST 3: Enforces absolute mathematical agreement between the repository code 
    and the documented main text specifications in your manuscript.
    """
    # Verifies that the internal software core engine default configuration 
    # locks the threshold at exactly 0.90 inclusive, matching Section 2.4 and Table 10
    assert analytics.get_pipeline_default_threshold() == 0.90
    assert analytics.is_threshold_inclusive() == True
