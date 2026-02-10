"""
Central Bank class for the economic simulator.

Implements monetary policy with Taylor-style rule.
"""


class CentralBank:
    """Represents the central bank in the economic simulation."""
    
    def __init__(self, inflation_target, policy_rate_baseline, taylor_coefficient):
        """
        Initialize central bank.
        
        Args:
            inflation_target: Target inflation rate
            policy_rate_baseline: Baseline policy interest rate
            taylor_coefficient: Coefficient for Taylor rule response to inflation gap
        """
        self.inflation_target = inflation_target
        self.policy_rate_baseline = policy_rate_baseline
        self.taylor_coefficient = taylor_coefficient
        
        # State variables
        self.policy_rate = policy_rate_baseline
        self.inflation_rate = 0.0
    
    def set_policy_rate(self, current_inflation):
        """
        Set policy rate using Taylor-style rule.
        Policy rate = baseline + taylor_coefficient * (inflation - target)
        
        Args:
            current_inflation: Current inflation rate
        """
        self.inflation_rate = current_inflation
        inflation_gap = current_inflation - self.inflation_target
        self.policy_rate = self.policy_rate_baseline + self.taylor_coefficient * inflation_gap
        # Ensure policy rate is non-negative
        self.policy_rate = max(0.0, self.policy_rate)
        return self.policy_rate
