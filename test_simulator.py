"""
Unit tests for the World Economic Simulator.

Tests core behaviors of households, firms, government, and the simulation engine.
"""
import unittest
import json
import os
import sys
from household import Household
from firm import Firm
from government import Government
from central_bank import CentralBank
from simulator import EconomicSimulator


class TestHousehold(unittest.TestCase):
    """Test household behavior."""
    
    def test_household_initialization(self):
        """Test household is properly initialized."""
        h = Household(1, 0.8, 0.7)
        self.assertEqual(h.id, 1)
        self.assertEqual(h.consumption_propensity, 0.8)
        self.assertTrue(h.is_working)
        self.assertEqual(h.wealth, 0.0)
    
    def test_consumption_rule(self):
        """Test consumption follows propensity rule."""
        h = Household(1, 0.8, 0.7)
        h.receive_wages(1000)
        h.pay_taxes(0.25)  # 25% tax rate
        h.receive_transfers(100)
        h.calculate_disposable_income()
        h.consume()
        
        # Disposable income = 1000 - 250 + 100 = 850
        self.assertEqual(h.disposable_income, 850)
        # Consumption = 0.8 * 850 = 680
        self.assertEqual(h.consumption, 680)
        # Savings = 850 - 680 = 170
        self.assertEqual(h.savings, 170)
        self.assertEqual(h.wealth, 170)


class TestFirm(unittest.TestCase):
    """Test firm behavior."""
    
    def test_firm_initialization(self):
        """Test firm is properly initialized."""
        f = Firm(1, "manufacturing", 50000, 1.0, 0.3, 0.2)
        self.assertEqual(f.id, 1)
        self.assertEqual(f.sector, "manufacturing")
        self.assertEqual(f.capital, 100.0)
    
    def test_production_function(self):
        """Test Cobb-Douglas production."""
        f = Firm(1, "manufacturing", 50000, 1.0, 0.3, 0.2)
        f.labor = 10.0
        f.capital = 100.0
        f.produce()
        
        # Y = 1.0 * (100^0.3) * (10^0.7)
        expected_output = 1.0 * (100 ** 0.3) * (10 ** 0.7)
        self.assertAlmostEqual(f.output, expected_output, places=2)
    
    def test_wage_setting(self):
        """Test wage is set correctly."""
        f = Firm(1, "manufacturing", 50000, 1.2, 0.3, 0.2)
        wage = f.set_wage()
        # Wage = baseline * productivity = 50000 * 1.2
        self.assertEqual(wage, 60000)
    
    def test_investment(self):
        """Test investment and capital accumulation."""
        f = Firm(1, "manufacturing", 50000, 1.0, 0.3, 0.2)
        initial_capital = f.capital
        f.profits = 1000
        f.invest()
        
        # Investment = 0.2 * 1000 = 200
        self.assertEqual(f.investment, 200)
        # Capital = 100 * 0.95 + 200 = 295
        expected_capital = initial_capital * 0.95 + 200
        self.assertAlmostEqual(f.capital, expected_capital, places=2)


class TestGovernment(unittest.TestCase):
    """Test government behavior."""
    
    def test_government_initialization(self):
        """Test government is properly initialized."""
        g = Government(0.25, 5000)
        self.assertEqual(g.tax_rate, 0.25)
        self.assertEqual(g.transfer_per_capita, 5000)
        self.assertEqual(g.debt, 0.0)
    
    def test_budget_balance(self):
        """Test budget balance calculation."""
        g = Government(0.25, 5000)
        
        # Create test households
        households = [Household(i, 0.8, 0.7) for i in range(10)]
        for h in households:
            h.taxes = 250
        
        # Create test firms
        firms = [Firm(i, "test", 50000, 1.0, 0.3, 0.2) for i in range(5)]
        for f in firms:
            f.taxes = 500
        
        g.collect_taxes(households, firms)
        g.distribute_transfers(households)
        g.calculate_budget_balance()
        
        # Tax revenue = 10 * 250 + 5 * 500 = 5000
        self.assertEqual(g.tax_revenue, 5000)
        # Transfers = 10 * 5000 = 50000
        self.assertEqual(g.total_transfers, 50000)
        # Balance = 5000 - 50000 = -45000 (deficit)
        self.assertEqual(g.budget_balance, -45000)
        # Debt increases by deficit
        self.assertEqual(g.debt, 45000)


class TestCentralBank(unittest.TestCase):
    """Test central bank behavior."""
    
    def test_central_bank_initialization(self):
        """Test central bank is properly initialized."""
        cb = CentralBank(0.02, 0.03, 1.5)
        self.assertEqual(cb.inflation_target, 0.02)
        self.assertEqual(cb.policy_rate, 0.03)
    
    def test_taylor_rule(self):
        """Test Taylor rule for policy rate."""
        cb = CentralBank(0.02, 0.03, 1.5)
        
        # Test with inflation above target
        rate = cb.set_policy_rate(0.04)
        # rate = 0.03 + 1.5 * (0.04 - 0.02) = 0.03 + 0.03 = 0.06
        self.assertAlmostEqual(rate, 0.06, places=4)
        
        # Test with inflation below target
        rate = cb.set_policy_rate(0.01)
        # rate = 0.03 + 1.5 * (0.01 - 0.02) = 0.03 - 0.015 = 0.015
        self.assertAlmostEqual(rate, 0.015, places=4)
        
        # Test that policy rate doesn't go negative
        cb2 = CentralBank(0.02, 0.01, 2.0)
        rate = cb2.set_policy_rate(-0.01)
        self.assertGreaterEqual(rate, 0.0)


class TestSimulator(unittest.TestCase):
    """Test the main simulator."""
    
    def test_simulator_initialization(self):
        """Test simulator initializes correctly from config."""
        sim = EconomicSimulator('config.json')
        self.assertGreater(len(sim.households), 0)
        self.assertGreater(len(sim.firms), 0)
        self.assertIsNotNone(sim.government)
        self.assertIsNotNone(sim.central_bank)
    
    def test_simulation_runs(self):
        """Test that simulation runs without errors."""
        # Create a minimal config for testing
        test_config = {
            "simulation": {"time_steps": 5, "random_seed": 42},
            "households": {
                "count": 10,
                "labor_participation_rate": 0.65,
                "consumption_propensity": 0.8
            },
            "firms": {
                "sectors": [
                    {"name": "test", "firm_count": 5, "wage_baseline": 50000, "productivity": 1.0}
                ],
                "cobb_douglas_alpha": 0.3,
                "investment_rate": 0.2
            },
            "government": {"tax_rate": 0.25, "transfer_per_capita": 5000},
            "central_bank": {
                "inflation_target": 0.02,
                "policy_rate_baseline": 0.03,
                "taylor_coefficient": 1.5
            },
            "trade": {"openness": 0.3, "tariff_rate": 0.05},
            "banking": {"loan_to_income_max": 3.0, "credit_spread": 0.02}
        }
        
        # Write test config
        with open('/tmp/test_config.json', 'w') as f:
            json.dump(test_config, f)
        
        sim = EconomicSimulator('/tmp/test_config.json')
        metrics = sim.run()
        
        # Check that we have metrics for all steps
        self.assertEqual(len(metrics), 5)
        
        # Check that metrics have expected keys
        expected_keys = ['step', 'gdp', 'consumption', 'investment', 'employment', 
                        'inflation_rate', 'policy_rate', 'government_debt']
        for key in expected_keys:
            self.assertIn(key, metrics[0])
        
        # Clean up
        os.remove('/tmp/test_config.json')
    
    def test_reproducibility(self):
        """Test that simulation is reproducible with same seed."""
        # Create test config
        test_config = {
            "simulation": {"time_steps": 3, "random_seed": 123},
            "households": {
                "count": 10,
                "labor_participation_rate": 0.65,
                "consumption_propensity": 0.8
            },
            "firms": {
                "sectors": [
                    {"name": "test", "firm_count": 5, "wage_baseline": 50000, "productivity": 1.0}
                ],
                "cobb_douglas_alpha": 0.3,
                "investment_rate": 0.2
            },
            "government": {"tax_rate": 0.25, "transfer_per_capita": 5000},
            "central_bank": {
                "inflation_target": 0.02,
                "policy_rate_baseline": 0.03,
                "taylor_coefficient": 1.5
            },
            "trade": {"openness": 0.3, "tariff_rate": 0.05},
            "banking": {"loan_to_income_max": 3.0, "credit_spread": 0.02}
        }
        
        with open('/tmp/test_config.json', 'w') as f:
            json.dump(test_config, f)
        
        # Run simulation twice
        sim1 = EconomicSimulator('/tmp/test_config.json')
        metrics1 = sim1.run()
        
        sim2 = EconomicSimulator('/tmp/test_config.json')
        metrics2 = sim2.run()
        
        # Results should be identical
        self.assertEqual(metrics1, metrics2)
        
        # Clean up
        os.remove('/tmp/test_config.json')


if __name__ == '__main__':
    unittest.main()
