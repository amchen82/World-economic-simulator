"""
Economic Simulator Engine

Main simulation class that orchestrates the economic model.
"""
import json
import random
from household import Household
from firm import Firm
from government import Government
from central_bank import CentralBank


class EconomicSimulator:
    """Main simulation engine for the economic model."""
    
    def __init__(self, config_path='config.json'):
        """
        Initialize the economic simulator from configuration.
        
        Args:
            config_path: Path to JSON configuration file
        """
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # Set random seed for reproducibility
        random.seed(self.config['simulation'].get('random_seed', 42))
        
        # Initialize agents
        self.households = self._create_households()
        self.firms = self._create_firms()
        self.government = self._create_government()
        self.central_bank = self._create_central_bank()
        
        # Simulation state
        self.current_step = 0
        self.time_steps = self.config['simulation']['time_steps']
        self.metrics_history = []
        
        # Economic state
        self.price_level = 1.0
        self.previous_price_level = 1.0
    
    def _create_households(self):
        """Create household agents from configuration."""
        config = self.config['households']
        households = []
        for i in range(config['count']):
            household = Household(
                household_id=i,
                consumption_propensity=config['consumption_propensity'],
                labor_participation_rate=config['labor_participation_rate']
            )
            households.append(household)
        return households
    
    def _create_firms(self):
        """Create firm agents from configuration."""
        config = self.config['firms']
        firms = []
        firm_id = 0
        for sector in config['sectors']:
            for _ in range(sector['firm_count']):
                firm = Firm(
                    firm_id=firm_id,
                    sector_name=sector['name'],
                    wage_baseline=sector['wage_baseline'],
                    productivity=sector['productivity'],
                    alpha=config['cobb_douglas_alpha'],
                    investment_rate=config['investment_rate']
                )
                firms.append(firm)
                firm_id += 1
        return firms
    
    def _create_government(self):
        """Create government from configuration."""
        config = self.config['government']
        return Government(
            tax_rate=config['tax_rate'],
            transfer_per_capita=config['transfer_per_capita']
        )
    
    def _create_central_bank(self):
        """Create central bank from configuration."""
        config = self.config['central_bank']
        return CentralBank(
            inflation_target=config['inflation_target'],
            policy_rate_baseline=config['policy_rate_baseline'],
            taylor_coefficient=config['taylor_coefficient']
        )
    
    def step(self):
        """
        Execute one time step of the simulation.
        
        Update ordering:
        1. Firms determine labor demand and production
        2. Households receive wages
        3. Government collects taxes and distributes transfers
        4. Households consume and save
        5. Firms invest
        6. Central bank adjusts policy rate
        7. Calculate metrics
        """
        # Reset period for all agents
        for household in self.households:
            household.reset_period()
        for firm in self.firms:
            firm.reset_period()
        self.government.reset_period()
        
        # 1. Firms determine labor demand and produce
        total_labor_supply = sum(1 for h in self.households if h.is_working)
        total_labor_demand = 0
        for firm in self.firms:
            labor_demand = firm.calculate_labor_demand(total_labor_supply)
            total_labor_demand += labor_demand
        
        # Allocate labor to firms based on supply constraints
        if total_labor_demand > 0:
            # If demand exceeds supply, ration proportionally
            allocation_ratio = min(1.0, total_labor_supply / total_labor_demand)
            for firm in self.firms:
                firm.labor = firm.desired_labor * allocation_ratio
        else:
            for firm in self.firms:
                firm.labor = 0.0
        
        # Firms produce with allocated labor
        for firm in self.firms:
            firm.produce()
            firm.calculate_revenue(self.price_level)
            firm.pay_wages()
        
        # 2. Distribute wages to working households
        working_households = [h for h in self.households if h.is_working]
        if working_households:
            # Calculate average wage from all firms
            total_wage_bill = sum(f.wage_bill for f in self.firms)
            avg_wage = total_wage_bill / max(1, len(working_households))
            for household in working_households:
                household.receive_wages(avg_wage)
        
        # 3. Government operations
        # First distribute transfers
        self.government.distribute_transfers(self.households)
        
        # Then households pay taxes
        for household in self.households:
            household.pay_taxes(self.government.tax_rate)
        
        # Firms pay taxes on profits (calculated after wage bill)
        for firm in self.firms:
            firm.calculate_profits(self.government.tax_rate)
        
        # Collect all taxes
        self.government.collect_taxes(self.households, self.firms)
        self.government.calculate_budget_balance()
        
        # 4. Households consume and save
        for household in self.households:
            household.calculate_disposable_income()
            household.consume()
        
        # 5. Firms invest
        for firm in self.firms:
            firm.invest()
        
        # 6. Update price level and inflation
        # Simplified: price level adjusts based on demand/supply balance
        total_output = sum(f.output for f in self.firms)
        total_consumption = sum(h.consumption for h in self.households)
        self.previous_price_level = self.price_level
        
        if total_output > 0 and total_consumption > 0:
            # Small adjustment to price level based on demand-supply gap
            demand_supply_ratio = total_consumption / total_output
            # Cap the adjustment to prevent explosive growth
            adjustment = max(0.98, min(1.02, 0.99 + 0.01 * (demand_supply_ratio - 1)))
            self.price_level = self.price_level * adjustment
        
        inflation = (self.price_level - self.previous_price_level) / max(0.0001, self.previous_price_level)
        
        # 7. Central bank sets policy rate
        self.central_bank.set_policy_rate(inflation)
        
        # 8. Calculate and store metrics
        metrics = self._calculate_metrics()
        self.metrics_history.append(metrics)
        
        self.current_step += 1
    
    def _calculate_metrics(self):
        """Calculate aggregate economic metrics for the current step."""
        total_output = sum(f.output for f in self.firms)
        total_consumption = sum(h.consumption for h in self.households)
        total_investment = sum(f.investment for f in self.firms)
        total_wages = sum(h.wages for h in self.households)
        total_employment = sum(1 for h in self.households if h.is_working and h.wages > 0)
        total_labor_force = sum(1 for h in self.households if h.is_working)
        
        metrics = {
            'step': self.current_step,
            'gdp': total_output * self.price_level,
            'consumption': total_consumption,
            'investment': total_investment,
            'government_spending': self.government.total_transfers,
            'net_exports': 0.0,  # Simplified for now
            'total_output': total_output,
            'employment': total_employment,
            'unemployment_rate': (total_labor_force - total_employment) / max(1, total_labor_force),
            'average_wage': total_wages / max(1, total_employment),
            'inflation_rate': self.central_bank.inflation_rate,
            'policy_rate': self.central_bank.policy_rate,
            'government_debt': self.government.debt,
            'budget_balance': self.government.budget_balance,
            'price_level': self.price_level,
            'total_household_wealth': sum(h.wealth for h in self.households),
            'total_capital': sum(f.capital for f in self.firms)
        }
        return metrics
    
    def run(self):
        """Run the full simulation for the configured number of time steps."""
        print(f"Starting economic simulation for {self.time_steps} time steps...")
        print(f"Households: {len(self.households)}, Firms: {len(self.firms)}")
        
        for step in range(self.time_steps):
            self.step()
            if step % 10 == 0:
                print(f"Step {step}/{self.time_steps} completed")
        
        print("Simulation complete!")
        return self.metrics_history
    
    def get_metrics(self):
        """Return the collected metrics history."""
        return self.metrics_history
