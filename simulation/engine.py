"""Core simulation engine for economic model"""
import numpy as np
from typing import Dict, List, Any
from dataclasses import dataclass, field


@dataclass
class SimulationParameters:
    """Parameters for the economic simulation"""
    # Time parameters
    time_steps: int = 100
    
    # Household parameters
    num_households: int = 1000
    consumption_propensity: float = 0.8
    labor_participation_rate: float = 0.65
    
    # Firm parameters
    num_firms: int = 100
    productivity: float = 1.0
    wage_baseline: float = 50000.0
    investment_rate: float = 0.15
    
    # Government parameters
    tax_rate: float = 0.25
    transfer_per_capita: float = 5000.0
    
    # Central bank parameters
    inflation_target: float = 0.02
    policy_rate_baseline: float = 0.03
    taylor_rule_sensitivity: float = 1.5
    
    # Initial conditions
    initial_capital: float = 1000000.0
    initial_price_level: float = 1.0


@dataclass
class SimulationState:
    """Current state of the simulation"""
    time: int = 0
    
    # Aggregate variables
    gdp: float = 0.0
    consumption: float = 0.0
    investment: float = 0.0
    government_spending: float = 0.0
    
    # Labor market
    employment: float = 0.0
    unemployment_rate: float = 0.0
    average_wage: float = 0.0
    
    # Prices and monetary
    price_level: float = 1.0
    inflation_rate: float = 0.0
    policy_rate: float = 0.03
    
    # Fiscal
    tax_revenue: float = 0.0
    government_transfers: float = 0.0
    budget_balance: float = 0.0
    government_debt: float = 0.0
    
    # Capital and productivity
    capital_stock: float = 0.0
    output: float = 0.0


class EconomicSimulator:
    """Main economic simulation engine"""
    
    def __init__(self, parameters: SimulationParameters):
        self.params = parameters
        self.state = SimulationState()
        self.history: List[Dict[str, Any]] = []
        self._initialize_state()
    
    def _initialize_state(self):
        """Initialize the simulation state"""
        self.state.time = 0
        self.state.capital_stock = self.params.initial_capital
        self.state.price_level = self.params.initial_price_level
        self.state.policy_rate = self.params.policy_rate_baseline
        self.state.average_wage = self.params.wage_baseline
        
        # Initial employment
        labor_force = self.params.num_households * self.params.labor_participation_rate
        self.state.employment = labor_force * 0.95  # Start with 5% unemployment
        self.state.unemployment_rate = 0.05
    
    def _calculate_output(self) -> float:
        """Calculate output using Cobb-Douglas production function"""
        alpha = 0.3  # Labor share
        K = self.state.capital_stock
        L = self.state.employment
        A = self.params.productivity
        
        # Y = A * K^(1-alpha) * L^alpha
        output = A * (K ** (1 - alpha)) * (L ** alpha)
        return output
    
    def _update_labor_market(self):
        """Update employment and wages"""
        labor_force = self.params.num_households * self.params.labor_participation_rate
        
        # Employment as a fraction of labor force, influenced by economic conditions
        # Base employment rate around 95% (5% natural unemployment)
        base_employment_rate = 0.95
        
        # Adjust for capital accumulation (more capital = more jobs)
        capital_effect = (self.state.capital_stock / self.params.initial_capital - 1) * 0.1
        
        # Adjust for real wage pressure (higher wages = fewer jobs)
        wage_effect = (self.state.average_wage / self.params.wage_baseline - 1) * -0.2
        
        employment_rate = base_employment_rate + capital_effect + wage_effect
        employment_rate = max(0.90, min(0.98, employment_rate))  # Keep between 90% and 98%
        
        target_employment = labor_force * employment_rate
        
        # Smooth adjustment toward target
        adjustment_speed = 0.15
        self.state.employment = self.state.employment + (target_employment - self.state.employment) * adjustment_speed
        
        # Calculate unemployment
        self.state.unemployment_rate = max(0.0, (labor_force - self.state.employment) / labor_force)
        
        # Wage adjustment based on unemployment (Phillips curve)
        if self.state.unemployment_rate < 0.04:
            self.state.average_wage *= 1.01  # Wage increases when tight labor market
        elif self.state.unemployment_rate > 0.07:
            self.state.average_wage *= 0.995  # Wage decreases when slack
    
    def _update_households(self):
        """Update household consumption and saving"""
        # Calculate disposable income
        wage_income = self.state.employment * self.state.average_wage
        transfers = self.params.transfer_per_capita * self.params.num_households
        taxes = wage_income * self.params.tax_rate
        
        disposable_income = wage_income + transfers - taxes
        
        # Consumption based on propensity
        self.state.consumption = self.params.consumption_propensity * disposable_income
    
    def _update_firms(self):
        """Update firm investment and capital accumulation"""
        output = self._calculate_output()
        wage_bill = self.state.employment * self.state.average_wage
        profits = max(0, output - wage_bill)
        
        # Investment as fraction of profits, plus some baseline investment
        baseline_investment = self.state.capital_stock * 0.03  # Replace 3% depreciation
        profit_investment = self.params.investment_rate * profits
        self.state.investment = baseline_investment + profit_investment
        
        # Capital accumulation (with 3% depreciation)
        depreciation = 0.03 * self.state.capital_stock
        self.state.capital_stock += self.state.investment - depreciation
        self.state.capital_stock = max(self.params.initial_capital * 0.5, self.state.capital_stock)  # Floor
    
    def _update_government(self):
        """Update government finances"""
        wage_income = self.state.employment * self.state.average_wage
        self.state.tax_revenue = wage_income * self.params.tax_rate
        self.state.government_transfers = self.params.transfer_per_capita * self.params.num_households
        self.state.government_spending = self.state.government_transfers
        
        self.state.budget_balance = self.state.tax_revenue - self.state.government_spending
        self.state.government_debt -= self.state.budget_balance
    
    def _update_prices(self):
        """Update price level and inflation"""
        # Simple inflation based on output gap and unemployment
        potential_output = self._calculate_output()
        actual_output = self.state.output
        
        # Inflation increases with low unemployment
        if self.state.unemployment_rate < 0.05:
            inflation_shock = 0.005
        elif self.state.unemployment_rate > 0.08:
            inflation_shock = -0.003
        else:
            inflation_shock = 0.0
        
        self.state.inflation_rate = self.params.inflation_target + inflation_shock
        self.state.price_level *= (1 + self.state.inflation_rate)
    
    def _update_monetary_policy(self):
        """Update policy rate using Taylor rule"""
        inflation_gap = self.state.inflation_rate - self.params.inflation_target
        self.state.policy_rate = (
            self.params.policy_rate_baseline +
            self.params.taylor_rule_sensitivity * inflation_gap
        )
        self.state.policy_rate = max(0.0, self.state.policy_rate)  # Zero lower bound
    
    def step(self):
        """Execute one time step of the simulation"""
        self.state.time += 1
        
        # Update in sequence
        self._update_labor_market()
        self.state.output = self._calculate_output()
        self._update_households()
        self._update_firms()
        self._update_government()
        self._update_prices()
        self._update_monetary_policy()
        
        # Calculate GDP
        self.state.gdp = (
            self.state.consumption +
            self.state.investment +
            self.state.government_spending
        )
        
        # Record history
        self._record_state()
    
    def _record_state(self):
        """Record current state to history"""
        record = {
            'time': self.state.time,
            'gdp': self.state.gdp,
            'consumption': self.state.consumption,
            'investment': self.state.investment,
            'government_spending': self.state.government_spending,
            'employment': self.state.employment,
            'unemployment_rate': self.state.unemployment_rate,
            'average_wage': self.state.average_wage,
            'price_level': self.state.price_level,
            'inflation_rate': self.state.inflation_rate,
            'policy_rate': self.state.policy_rate,
            'tax_revenue': self.state.tax_revenue,
            'government_transfers': self.state.government_transfers,
            'budget_balance': self.state.budget_balance,
            'government_debt': self.state.government_debt,
            'capital_stock': self.state.capital_stock,
            'output': self.state.output,
        }
        self.history.append(record)
    
    def run(self):
        """Run the full simulation"""
        for _ in range(self.params.time_steps):
            self.step()
        return self.history
    
    def get_results(self) -> Dict[str, List[float]]:
        """Get simulation results as time series"""
        if not self.history:
            return {}
        
        results = {}
        keys = self.history[0].keys()
        for key in keys:
            results[key] = [record[key] for record in self.history]
        
        return results
