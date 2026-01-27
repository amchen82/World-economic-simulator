"""
Firm class for the economic simulator.

Represents firm agents with production, labor demand, and investment behavior.
"""
import math


class Firm:
    """Represents a firm agent in the economic simulation."""
    
    def __init__(self, firm_id, sector_name, wage_baseline, productivity, 
                 alpha, investment_rate):
        """
        Initialize a firm.
        
        Args:
            firm_id: Unique identifier for the firm
            sector_name: Name of the sector this firm belongs to
            wage_baseline: Base wage level for the sector
            productivity: Productivity multiplier for the sector
            alpha: Capital share in Cobb-Douglas production function
            investment_rate: Fraction of profits invested
        """
        self.id = firm_id
        self.sector = sector_name
        self.wage_baseline = wage_baseline
        self.productivity = productivity
        self.alpha = alpha
        self.investment_rate = investment_rate
        
        # State variables
        self.capital = 100.0  # Initial capital stock
        self.labor = 0.0
        self.desired_labor = 0.0  # Labor demand before market clearing
        self.output = 0.0
        self.revenue = 0.0
        self.wage_bill = 0.0
        self.profits = 0.0
        self.investment = 0.0
        self.taxes = 0.0
    
    def set_wage(self):
        """
        Set wage based on sector baseline and productivity.
        Wage setting: sector wage baseline * productivity
        """
        return self.wage_baseline * self.productivity
    
    def calculate_labor_demand(self, total_labor_supply):
        """
        Calculate labor demand based on profit maximization.
        Simplified: proportional allocation based on capital stock.
        
        Args:
            total_labor_supply: Total available workers in the economy
        
        Returns:
            Desired labor demand (may be rationed by market clearing)
        """
        # Simplified labor demand with diminishing returns to capital
        # Use a square root to prevent explosive growth
        base_demand = max(1.0, (self.capital ** 0.5) * 0.5)
        # Cap labor demand at reasonable level
        self.desired_labor = min(base_demand, 100.0)
        return self.desired_labor
    
    def produce(self):
        """
        Produce output using Cobb-Douglas production function.
        Production: Y = A * K^alpha * L^(1-alpha)
        """
        if self.labor > 0:
            self.output = self.productivity * (
                (self.capital ** self.alpha) * 
                (self.labor ** (1 - self.alpha))
            )
        else:
            self.output = 0.0
    
    def calculate_revenue(self, price_level=1.0):
        """Calculate revenue from output at given price level."""
        self.revenue = self.output * price_level
    
    def pay_wages(self):
        """Calculate wage bill for employed labor."""
        wage = self.set_wage()
        self.wage_bill = wage * self.labor
    
    def calculate_profits(self, tax_rate):
        """
        Calculate profits after wages and before taxes.
        Then calculate and pay taxes on profits.
        """
        gross_profits = self.revenue - self.wage_bill
        self.taxes = max(0.0, gross_profits * tax_rate)
        self.profits = gross_profits - self.taxes
    
    def invest(self):
        """
        Invest a fraction of profits in capital accumulation.
        Investment: fraction of profits
        """
        self.investment = max(0.0, self.profits * self.investment_rate)
        # Capital accumulation (with 5% depreciation)
        depreciation_rate = 0.05
        self.capital = self.capital * (1 - depreciation_rate) + self.investment
    
    def reset_period(self):
        """Reset flow variables at the start of each period."""
        self.labor = 0.0
        self.desired_labor = 0.0
        self.output = 0.0
        self.revenue = 0.0
        self.wage_bill = 0.0
        self.profits = 0.0
        self.investment = 0.0
        self.taxes = 0.0
