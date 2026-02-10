# Examples and Use Cases

This document provides examples of how to use the World Economic Simulator for different scenarios.

## Basic Usage

### Running the Default Simulation

```bash
python main.py
```

This runs a 100-step simulation with 1000 households and 150 firms across 2 sectors.

### Custom Configuration

Create a custom configuration file:

```json
{
  "simulation": {
    "time_steps": 50,
    "random_seed": 123
  },
  "households": {
    "count": 500,
    "labor_participation_rate": 0.7,
    "consumption_propensity": 0.85
  },
  "firms": {
    "sectors": [
      {
        "name": "technology",
        "firm_count": 25,
        "wage_baseline": 80000,
        "productivity": 1.5
      }
    ],
    "cobb_douglas_alpha": 0.35,
    "investment_rate": 0.25
  },
  "government": {
    "tax_rate": 0.2,
    "transfer_per_capita": 3000
  },
  "central_bank": {
    "inflation_target": 0.02,
    "policy_rate_baseline": 0.025,
    "taylor_coefficient": 2.0
  }
}
```

Run with custom config:
```bash
python main.py my_scenario.json
```

## Programmatic Usage

### Running Simulations in Python

```python
from simulator import EconomicSimulator
from metrics import MetricsReporter

# Initialize simulator
sim = EconomicSimulator('config.json')

# Run simulation
metrics = sim.run()

# Generate reports
reporter = MetricsReporter(output_dir='my_results')
reporter.save_to_csv(metrics)
reporter.save_to_json(metrics)
reporter.generate_charts(metrics)
reporter.print_summary(metrics)
```

### Analyzing Results

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load results
df = pd.read_csv('output/simulation_results.csv')

# Custom analysis
print(f"Average GDP: {df['gdp'].mean():.2f}")
print(f"GDP Growth: {(df['gdp'].iloc[-1] / df['gdp'].iloc[0] - 1) * 100:.2f}%")

# Custom visualization
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(df['step'], df['gdp'])
plt.title('GDP Trajectory')
plt.subplot(1, 2, 2)
plt.plot(df['step'], df['unemployment_rate'])
plt.title('Unemployment Rate')
plt.tight_layout()
plt.savefig('my_analysis.png')
```

## Scenario Examples

### High Productivity Economy

```json
{
  "firms": {
    "sectors": [
      {
        "name": "high_tech",
        "firm_count": 100,
        "wage_baseline": 100000,
        "productivity": 2.0
      }
    ]
  }
}
```

### Low Tax, Low Transfer Economy

```json
{
  "government": {
    "tax_rate": 0.15,
    "transfer_per_capita": 2000
  }
}
```

### Aggressive Monetary Policy

```json
{
  "central_bank": {
    "inflation_target": 0.02,
    "policy_rate_baseline": 0.05,
    "taylor_coefficient": 3.0
  }
}
```

## Interpreting Results

### Key Metrics

- **GDP**: Total economic output value (price_level × total_output)
- **Inflation Rate**: Percentage change in price level
- **Unemployment Rate**: Fraction of labor force not employed
- **Budget Balance**: Government surplus (positive) or deficit (negative)
- **Government Debt**: Cumulative government debt
- **Policy Rate**: Central bank interest rate

### Expected Behaviors

1. **Stable Inflation**: With default Taylor rule, inflation should converge to target (2%)
2. **Government Debt**: Typically accumulates due to transfers exceeding tax revenue
3. **Employment**: Usually near full employment in baseline scenario
4. **Consumption**: Should dominate GDP due to high consumption propensity

## Testing Scenarios

### Comparing Two Scenarios

```python
# Run baseline
sim1 = EconomicSimulator('baseline.json')
metrics1 = sim1.run()

# Run alternative
sim2 = EconomicSimulator('alternative.json')
metrics2 = sim2.run()

# Compare
import pandas as pd
df1 = pd.DataFrame(metrics1)
df2 = pd.DataFrame(metrics2)

print("Baseline final GDP:", df1['gdp'].iloc[-1])
print("Alternative final GDP:", df2['gdp'].iloc[-1])
```

## Advanced Usage

### Custom Metrics Calculation

```python
from simulator import EconomicSimulator

sim = EconomicSimulator('config.json')

# Run step by step for custom analysis
for step in range(sim.time_steps):
    sim.step()
    
    # Access current state
    if step % 10 == 0:
        total_wealth = sum(h.wealth for h in sim.households)
        total_capital = sum(f.capital for f in sim.firms)
        print(f"Step {step}: Wealth={total_wealth:.2f}, Capital={total_capital:.2f}")

# Get final metrics
metrics = sim.get_metrics()
```

## Validation

Run the test suite to ensure the simulator is working correctly:

```bash
python -m unittest test_simulator.py -v
```

Expected output: All tests should pass with OK status.
