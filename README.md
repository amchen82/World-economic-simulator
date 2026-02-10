# World Economic Simulator

A Python-based economic simulation engine that models household, firm, government, and central bank behavior to simulate macroeconomic dynamics.

## Overview

This simulator implements a mid-level realism economic model with simplified behavioral rules based on agent-based modeling principles. It tracks households, firms across sectors, government fiscal policy, and central bank monetary policy over discrete time steps.

## Features

- **Agent-Based Modeling**: Simulates individual households and firms with behavioral rules
- **Macroeconomic Dynamics**: Tracks GDP, inflation, unemployment, and other key indicators
- **Government Sector**: Tax collection, transfers, and budget balance tracking
- **Monetary Policy**: Central bank with Taylor-rule policy rate setting
- **Time-Series Analysis**: Generates comprehensive metrics for each simulation step
- **Visualization**: Automatic chart generation for key economic indicators
- **Configurable**: JSON-based configuration for all model parameters

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/amchen82/World-economic-simulator.git
cd World-economic-simulator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running a Simulation

Run the simulator with the default configuration:
```bash
python main.py
```

Or specify a custom configuration file:
```bash
python main.py my_config.json
```

### Configuration

The simulation is configured via a JSON file (`config.json` by default). Key parameters:

```json
{
  "simulation": {
    "time_steps": 100,
    "random_seed": 42
  },
  "households": {
    "count": 1000,
    "labor_participation_rate": 0.65,
    "consumption_propensity": 0.8
  },
  "firms": {
    "sectors": [...],
    "cobb_douglas_alpha": 0.3,
    "investment_rate": 0.2
  },
  "government": {
    "tax_rate": 0.25,
    "transfer_per_capita": 5000
  },
  "central_bank": {
    "inflation_target": 0.02,
    "policy_rate_baseline": 0.03,
    "taylor_coefficient": 1.5
  }
}
```

### Output

The simulator generates several outputs in the `output/` directory:

- **simulation_results.csv**: Time-series data in CSV format
- **simulation_results.json**: Time-series data in JSON format
- **charts/**: Directory containing PNG charts for:
  - GDP over time
  - Inflation and policy rate
  - Unemployment rate
  - Government debt
  - Consumption and investment
  - Budget balance

### Running Tests

Run the test suite to verify the implementation:
```bash
python -m unittest test_simulator.py
```

Or run with verbose output:
```bash
python -m unittest test_simulator.py -v
```

## Model Specification

### Households
- **Income**: wages + transfers − taxes
- **Consumption**: c = propensity × disposable_income
- **Savings**: disposable_income − consumption
- **Labor Supply**: Fixed participation rate

### Firms
- **Production**: Cobb-Douglas function Y = A × K^α × L^(1-α)
- **Wage Setting**: sector_baseline × productivity
- **Investment**: Fraction of profits reinvested
- **Capital Accumulation**: With 5% depreciation

### Government
- **Taxes**: Flat rate on wages and profits
- **Transfers**: Per-capita payments
- **Budget**: Balanced tracking with debt accumulation

### Central Bank
- **Policy Rule**: Taylor-style rule around inflation gap
- **Policy Rate**: baseline + coefficient × (inflation - target)

### Metrics Tracked
- GDP (nominal and real)
- Consumption and Investment
- Employment and Unemployment Rate
- Wages and Prices
- Inflation Rate
- Government Debt and Budget Balance
- Policy Interest Rate
- Household Wealth
- Capital Stock

## Project Structure

```
World-economic-simulator/
├── main.py              # Entry point
├── simulator.py         # Main simulation engine
├── household.py         # Household agent class
├── firm.py              # Firm agent class
├── government.py        # Government class
├── central_bank.py      # Central bank class
├── metrics.py           # Metrics reporting and visualization
├── test_simulator.py    # Unit tests
├── config.json          # Default configuration
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── docs/               # Documentation
    ├── backlog.md      # Development backlog
    └── model-spec.md   # Detailed model specification
```

## Development Roadmap

See [docs/backlog.md](docs/backlog.md) for the full development backlog and planned features.

### Implemented Features (Epic 1-4)
- ✅ Core simulation engine with time-step loop
- ✅ Household agents with consumption and savings
- ✅ Firm agents with production and investment
- ✅ Government with taxes and transfers
- ✅ Central bank with policy rate setting
- ✅ Metrics collection and reporting
- ✅ CSV/JSON export
- ✅ Chart generation
- ✅ Unit tests

### Future Enhancements (Epic 5)
- Trade flows and tariffs
- Banking sector with credit constraints
- Advanced shocks and scenarios

## Examples

### Quick Start Example
```python
from simulator import EconomicSimulator
from metrics import MetricsReporter

# Create and run simulation
sim = EconomicSimulator('config.json')
metrics = sim.run()

# Generate reports
reporter = MetricsReporter()
reporter.save_to_csv(metrics)
reporter.generate_charts(metrics)
reporter.print_summary(metrics)
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is open source and available under the MIT License.

## Acknowledgments

Based on standard macroeconomic modeling principles with simplified agent-based behavioral rules.
