"""
Metrics and Reporting Module

Handles output of simulation results to CSV/JSON and chart generation.
"""
import json
import os
import pandas as pd
import matplotlib.pyplot as plt


class MetricsReporter:
    """Handles metrics reporting and visualization."""
    
    def __init__(self, output_dir='output'):
        """
        Initialize metrics reporter.
        
        Args:
            output_dir: Directory to save output files
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, 'charts'), exist_ok=True)
    
    def save_to_csv(self, metrics_history, filename='simulation_results.csv'):
        """
        Save metrics history to CSV file.
        
        Args:
            metrics_history: List of metric dictionaries
            filename: Output CSV filename
        """
        df = pd.DataFrame(metrics_history)
        filepath = os.path.join(self.output_dir, filename)
        df.to_csv(filepath, index=False)
        print(f"Saved results to {filepath}")
        return filepath
    
    def save_to_json(self, metrics_history, filename='simulation_results.json'):
        """
        Save metrics history to JSON file.
        
        Args:
            metrics_history: List of metric dictionaries
            filename: Output JSON filename
        """
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(metrics_history, f, indent=2)
        print(f"Saved results to {filepath}")
        return filepath
    
    def generate_charts(self, metrics_history):
        """
        Generate charts for key economic indicators.
        
        Args:
            metrics_history: List of metric dictionaries
        """
        df = pd.DataFrame(metrics_history)
        charts_dir = os.path.join(self.output_dir, 'charts')
        
        # Chart 1: GDP over time
        plt.figure(figsize=(10, 6))
        plt.plot(df['step'], df['gdp'])
        plt.title('GDP Over Time')
        plt.xlabel('Time Step')
        plt.ylabel('GDP')
        plt.grid(True)
        plt.savefig(os.path.join(charts_dir, 'gdp.png'))
        plt.close()
        
        # Chart 2: Inflation and Policy Rate
        plt.figure(figsize=(10, 6))
        plt.plot(df['step'], df['inflation_rate'], label='Inflation Rate')
        plt.plot(df['step'], df['policy_rate'], label='Policy Rate')
        plt.title('Inflation and Policy Rate')
        plt.xlabel('Time Step')
        plt.ylabel('Rate')
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(charts_dir, 'inflation_policy.png'))
        plt.close()
        
        # Chart 3: Unemployment Rate
        plt.figure(figsize=(10, 6))
        plt.plot(df['step'], df['unemployment_rate'])
        plt.title('Unemployment Rate Over Time')
        plt.xlabel('Time Step')
        plt.ylabel('Unemployment Rate')
        plt.grid(True)
        plt.savefig(os.path.join(charts_dir, 'unemployment.png'))
        plt.close()
        
        # Chart 4: Government Debt
        plt.figure(figsize=(10, 6))
        plt.plot(df['step'], df['government_debt'])
        plt.title('Government Debt Over Time')
        plt.xlabel('Time Step')
        plt.ylabel('Debt')
        plt.grid(True)
        plt.savefig(os.path.join(charts_dir, 'government_debt.png'))
        plt.close()
        
        # Chart 5: Consumption and Investment
        plt.figure(figsize=(10, 6))
        plt.plot(df['step'], df['consumption'], label='Consumption')
        plt.plot(df['step'], df['investment'], label='Investment')
        plt.title('Consumption and Investment')
        plt.xlabel('Time Step')
        plt.ylabel('Amount')
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(charts_dir, 'consumption_investment.png'))
        plt.close()
        
        # Chart 6: Budget Balance
        plt.figure(figsize=(10, 6))
        plt.plot(df['step'], df['budget_balance'])
        plt.axhline(y=0, color='r', linestyle='--', alpha=0.3)
        plt.title('Government Budget Balance')
        plt.xlabel('Time Step')
        plt.ylabel('Balance (Surplus/Deficit)')
        plt.grid(True)
        plt.savefig(os.path.join(charts_dir, 'budget_balance.png'))
        plt.close()
        
        print(f"Generated charts in {charts_dir}")
    
    def print_summary(self, metrics_history):
        """
        Print summary statistics of the simulation.
        
        Args:
            metrics_history: List of metric dictionaries
        """
        df = pd.DataFrame(metrics_history)
        
        print("\n" + "="*60)
        print("SIMULATION SUMMARY")
        print("="*60)
        print(f"\nTotal time steps: {len(metrics_history)}")
        print(f"\nFinal GDP: {df['gdp'].iloc[-1]:,.2f}")
        print(f"Average GDP: {df['gdp'].mean():,.2f}")
        print(f"\nFinal Inflation Rate: {df['inflation_rate'].iloc[-1]:.2%}")
        print(f"Average Inflation Rate: {df['inflation_rate'].mean():.2%}")
        print(f"\nFinal Unemployment Rate: {df['unemployment_rate'].iloc[-1]:.2%}")
        print(f"Average Unemployment Rate: {df['unemployment_rate'].mean():.2%}")
        print(f"\nFinal Government Debt: {df['government_debt'].iloc[-1]:,.2f}")
        print(f"Final Budget Balance: {df['budget_balance'].iloc[-1]:,.2f}")
        print(f"\nFinal Policy Rate: {df['policy_rate'].iloc[-1]:.2%}")
        print("="*60 + "\n")
