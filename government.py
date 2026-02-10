"""
Government class for the economic simulator.

Manages tax collection, transfers, and budget balance.
"""


class Government:
    """Represents the government in the economic simulation."""
    
    def __init__(self, tax_rate, transfer_per_capita):
        """
        Initialize government.
        
        Args:
            tax_rate: Flat tax rate on wages and profits
            transfer_per_capita: Basic per-capita transfer payment
        """
        self.tax_rate = tax_rate
        self.transfer_per_capita = transfer_per_capita
        
        # State variables
        self.tax_revenue = 0.0
        self.total_transfers = 0.0
        self.budget_balance = 0.0
        self.debt = 0.0
    
    def collect_taxes(self, households, firms):
        """
        Collect taxes from households and firms.
        
        Args:
            households: List of household agents
            firms: List of firm agents
        """
        household_taxes = sum(h.taxes for h in households)
        firm_taxes = sum(f.taxes for f in firms)
        self.tax_revenue = household_taxes + firm_taxes
    
    def distribute_transfers(self, households):
        """
        Distribute transfers to households.
        
        Args:
            households: List of household agents
        """
        self.total_transfers = len(households) * self.transfer_per_capita
        for household in households:
            household.receive_transfers(self.transfer_per_capita)
    
    def calculate_budget_balance(self):
        """
        Calculate budget balance and update debt.
        Budget balance = tax revenue - transfers
        """
        self.budget_balance = self.tax_revenue - self.total_transfers
        self.debt -= self.budget_balance  # Surplus reduces debt, deficit increases it
    
    def reset_period(self):
        """Reset flow variables at the start of each period."""
        self.tax_revenue = 0.0
        self.total_transfers = 0.0
        self.budget_balance = 0.0
