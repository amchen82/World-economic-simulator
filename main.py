#!/usr/bin/env python3
"""
Main entry point for the World Economic Simulator.

Usage:
    python main.py [config_file]
    
Example:
    python main.py config.json
"""
import sys
from simulator import EconomicSimulator
from metrics import MetricsReporter


def main():
    """Run the economic simulation."""
    # Get config file from command line or use default
    config_file = sys.argv[1] if len(sys.argv) > 1 else 'config.json'
    
    print("="*60)
    print("WORLD ECONOMIC SIMULATOR")
    print("="*60)
    print(f"Configuration: {config_file}\n")
    
    # Initialize simulator
    simulator = EconomicSimulator(config_file)
    
    # Run simulation
    metrics_history = simulator.run()
    
    # Generate reports
    reporter = MetricsReporter()
    reporter.save_to_csv(metrics_history)
    reporter.save_to_json(metrics_history)
    reporter.generate_charts(metrics_history)
    reporter.print_summary(metrics_history)
    
    print("All outputs saved to 'output' directory")


if __name__ == '__main__':
    main()
