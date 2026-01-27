"""
Household class for the economic simulator.

Represents household agents with income, consumption, and savings behavior.
"""


class Household:
    """Represents a household agent in the economic simulation."""
    
    def __init__(self, household_id, consumption_propensity, labor_participation_rate):
        """
        Initialize a household.
        
        Args:
            household_id: Unique identifier for the household
            consumption_propensity: Fraction of disposable income spent on consumption
            labor_participation_rate: Probability of participating in labor market
        """
        self.id = household_id
        self.consumption_propensity = consumption_propensity
        self.is_working = labor_participation_rate > 0.5  # Simplified for deterministic behavior
        
        # State variables
        self.wages = 0.0
        self.transfers = 0.0
        self.taxes = 0.0
        self.disposable_income = 0.0
        self.consumption = 0.0
        self.savings = 0.0
        self.wealth = 0.0
    
    def receive_wages(self, wage_amount):
        """Record wages received from employment."""
        self.wages = wage_amount if self.is_working else 0.0
    
    def receive_transfers(self, transfer_amount):
        """Record transfers received from government."""
        self.transfers = transfer_amount
    
    def pay_taxes(self, tax_rate):
        """Calculate and pay taxes on wages."""
        self.taxes = self.wages * tax_rate
    
    def calculate_disposable_income(self):
        """Calculate disposable income after taxes and transfers."""
        self.disposable_income = self.wages + self.transfers - self.taxes
    
    def consume(self):
        """
        Determine consumption based on disposable income and propensity.
        Consumption rule: c = propensity * disposable_income
        """
        self.consumption = self.consumption_propensity * self.disposable_income
        self.savings = self.disposable_income - self.consumption
        self.wealth += self.savings
    
    def reset_period(self):
        """Reset flow variables at the start of each period."""
        self.wages = 0.0
        self.transfers = 0.0
        self.taxes = 0.0
        self.disposable_income = 0.0
        self.consumption = 0.0
        self.savings = 0.0
