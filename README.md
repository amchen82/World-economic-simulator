# World Economic Simulator

An agent-based macroeconomic simulation system that models the collective behavior of economic agents (households, firms, government, and central bank) to explore macroeconomic phenomena.

## Overview

The World Economic Simulator uses agent-based modeling to simulate how individual economic decisions aggregate into economy-wide patterns. The simulator features:

- **Mid-level economic realism** balancing complexity with tractability
- **Deterministic execution** for reproducibility in research
- **Flexible configuration** via YAML/JSON files
- **Comprehensive metrics** tracking GDP, unemployment, inflation, inequality, and more
- **Shock scenarios** to test policy interventions and economic disturbances

## Documentation

Complete documentation is available in the [docs](./docs) directory:

### Core Documentation

1. **[Documentation Index](./docs/README.md)** - Start here for an overview and navigation guide

2. **[Product Requirements](./docs/product-requirements.md)** - What the simulator does and why
   - Expert Q&A covering software engineering and economic perspectives
   - Functional and non-functional requirements
   - Success criteria and scope definition

3. **[System Architecture](./docs/system-architecture.md)** - How the system is structured
   - Layered architecture design
   - Component specifications and data flow
   - Technology stack and design patterns

4. **[Entity Model](./docs/entity-model.md)** - Detailed agent specifications
   - Complete specifications for Households, Firms, Government, and Central Bank
   - Behavioral algorithms and decision rules
   - Entity relationships and market mechanisms

5. **[Simulator Execution Flow](./docs/simulator-execution.md)** - How the simulator runs
   - Initialization procedures
   - Time-step processing details
   - Output generation and data export

### Additional Resources

- **[Model Specification](./docs/model-spec.md)** - Concise economic model summary
- **[Development Backlog](./docs/backlog.md)** - Feature roadmap and epics

## Quick Start

### For Users

1. Read the [Product Requirements](./docs/product-requirements.md) to understand capabilities
2. Review the [Simulator Execution Flow](./docs/simulator-execution.md) for usage instructions
3. Explore configuration examples and shock scenarios

### For Developers

1. Start with [System Architecture](./docs/system-architecture.md) for overall design
2. Implement agents following [Entity Model](./docs/entity-model.md) specifications
3. Build execution engine per [Simulator Execution Flow](./docs/simulator-execution.md)
4. Reference [Product Requirements](./docs/product-requirements.md) for detailed specs

### For Economists

1. Review economic modeling approach in [Product Requirements Q&A](./docs/product-requirements.md#economic-modeling-perspective)
2. Study behavioral specifications in [Entity Model](./docs/entity-model.md)
3. Understand temporal dynamics in [Simulator Execution Flow](./docs/simulator-execution.md)

## Key Features

### Agent Types

- **Households:** Supply labor, consume goods, save, and pay taxes
- **Firms:** Produce output, hire workers, invest in capital, and set prices
- **Government:** Collect taxes, provide transfers, manage public finances
- **Central Bank:** Set policy rates, target inflation using Taylor rule

### Market Mechanisms

- **Labor Market:** Matches workers and jobs, determines wages and employment
- **Goods Market:** Matches production and consumption, determines prices
- **Credit Market (Optional):** Allocates credit with loan-to-income constraints

### Macroeconomic Indicators

- Output: GDP, growth rates
- Employment: Unemployment rate, participation
- Prices: Inflation, price levels
- Distribution: Gini coefficient, income shares
- Fiscal: Tax revenue, spending, debt-to-GDP
- Monetary: Policy rates, real rates

## Configuration Example

```yaml
simulation:
  time_steps: 1000
  random_seed: 42

agents:
  households:
    count: 1000
    consumption_propensity: 0.8
  
  firms:
    count: 100
    production_alpha: 0.3
  
  government:
    income_tax_rate: 0.2
  
  central_bank:
    inflation_target: 0.02
    taylor_inflation_coeff: 1.5

shocks:
  - type: demand
    time: 500
    change: -0.1
```

## Technology Stack

**Recommended Implementation:**
- Python 3.8+
- NumPy (numerical operations)
- Pandas (data handling)
- Matplotlib (visualization)
- PyYAML (configuration)
- pytest (testing)

## Project Status

This project currently includes comprehensive **design documentation**. Implementation is planned following the specifications in the docs directory.

## Contributing

Contributions are welcome! Please:
- Follow the architecture and design patterns documented
- Maintain consistency with specifications
- Include tests for new features
- Update documentation as needed

## License

[To be determined]

## Contact

[To be determined]
