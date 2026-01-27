# World Economic Simulator - Documentation Index

## Overview

Welcome to the World Economic Simulator documentation. This comprehensive documentation set provides complete specifications for an agent-based macroeconomic simulation system. The simulator models the collective behavior of economic agents (households, firms, government, and central bank) to explore macroeconomic phenomena.

## Documentation Structure

This documentation is organized into four main documents, each serving a specific purpose:

### 1. [Product Requirements Document](product-requirements.md)

**Purpose:** Defines what the simulator should do and why

**Key Contents:**
- **Expert Q&A Format:** 14 questions answered from both software engineering and economic perspectives
- **Functional Requirements:** Detailed specifications for all system components
- **Non-Functional Requirements:** Performance, reliability, maintainability criteria
- **Success Criteria:** Clear metrics for project completion
- **Scope Definition:** What's included in V1 and what's deferred

**Read this if you want to:**
- Understand the purpose and goals of the simulator
- Learn about the economic and technical requirements
- Understand design decisions and tradeoffs
- See what features are planned vs. out of scope

**Key Highlights:**
- Mid-level economic realism balancing complexity and tractability
- Deterministic execution for reproducibility
- Support for 1000+ agents over 1000+ time steps
- Comprehensive macroeconomic indicator tracking
- Flexible shock and policy intervention framework

### 2. [System Architecture Document](system-architecture.md)

**Purpose:** Describes how the system is structured and organized

**Key Contents:**
- **Layered Architecture:** Presentation, Application, Domain, and Infrastructure layers
- **Component Specifications:** Detailed design of each major component
- **Data Flow Diagrams:** How information moves through the system
- **Design Patterns:** Strategy, Observer, Command, Factory, Singleton patterns
- **Technology Stack:** Recommended implementation technologies
- **Performance Considerations:** Optimization strategies and scalability

**Read this if you want to:**
- Understand the overall system structure
- Learn how components interact
- Implement the simulator
- Extend or modify the architecture
- Understand design patterns used

**Key Components:**
- **Simulation Controller:** Orchestrates the time-step loop
- **Agent System:** Manages households, firms, government, central bank
- **Market Mechanisms:** Labor, goods, and credit market clearing
- **Metrics Aggregator:** Calculates macroeconomic indicators
- **Configuration Manager:** Handles parameter management
- **Data Storage Handler:** Persists simulation data

### 3. [Entity Model Document](entity-model.md)

**Purpose:** Specifies all entities, their attributes, behaviors, and relationships

**Key Contents:**
- **Entity Hierarchy:** Abstract base classes and concrete implementations
- **Detailed Specifications:** For each agent type (Household, Firm, Government, Central Bank)
- **Behavioral Algorithms:** Pseudocode for all decision rules
- **Entity Relationships:** How entities interact and depend on each other
- **Market Entities:** Labor market, goods market, credit market specifications
- **State Transitions:** Lifecycle and state machines for each entity

**Read this if you want to:**
- Understand what each agent does and how it decides
- Implement agent behaviors
- Understand economic model specifications
- See how agents interact with each other
- Learn about market clearing mechanisms

**Key Entities:**

**Household Agent:**
- Supplies labor based on participation rate
- Consumes based on propensity to consume
- Saves residual income
- Accumulates wealth

**Firm Agent:**
- Produces using Cobb-Douglas production function
- Hires labor based on profit maximization
- Sets wages by sector and productivity
- Invests fraction of profits in capital

**Government Agent:**
- Collects income and profit taxes
- Distributes per-capita transfers
- Tracks budget balance and debt

**Central Bank Agent:**
- Calculates inflation from price changes
- Sets policy rate using Taylor rule
- Targets inflation

### 4. [Simulator Execution Flow Document](simulator-execution.md)

**Purpose:** Describes how the simulator runs from start to finish

**Key Contents:**
- **Phase-by-Phase Execution:** From configuration loading to output generation
- **Detailed Algorithms:** Pseudocode for each processing phase
- **Time-Step Processing:** Exact ordering of operations within each step
- **Initialization Procedures:** How agents and markets are created
- **Metrics Calculation:** How aggregate indicators are computed
- **Output Generation:** Export to CSV, JSON, and visualizations
- **Error Handling:** Validation, recovery, and termination conditions

**Read this if you want to:**
- Understand the execution sequence
- Implement the simulation loop
- Debug simulation issues
- Understand temporal ordering and dependencies
- Learn about data export and visualization

**Execution Phases:**
1. **Configuration Loading:** Parse YAML/JSON configuration files
2. **Parameter Validation:** Check ranges and consistency
3. **System Initialization:** Create agents, markets, data storage
4. **Simulation Loop:** Execute time steps with deterministic ordering
5. **Output Generation:** Export results in multiple formats
6. **Cleanup and Exit:** Save final state and summary statistics

**Time-Step Execution Order:**
1. Firms set wages and calculate labor demand
2. Labor market clears (employment, wages)
3. Firms produce output
4. Government collects taxes and distributes transfers
5. Households decide consumption
6. Goods market clears (prices)
7. Firms calculate profits and invest
8. Households save and update wealth
9. Government updates budget and debt
10. Central bank sets policy rate
11. Credit market allocates credit (optional)
12. Aggregate metrics calculated and stored

## Quick Start Guide

### For Users

1. **Start with:** [Product Requirements](product-requirements.md) to understand what the simulator does
2. **Then read:** [Simulator Execution Flow](simulator-execution.md) to learn how to configure and run simulations
3. **Reference:** [Entity Model](entity-model.md) to understand specific agent behaviors

### For Developers

1. **Start with:** [System Architecture](system-architecture.md) to understand the overall design
2. **Then read:** [Entity Model](entity-model.md) to implement agents and behaviors
3. **Then read:** [Simulator Execution Flow](simulator-execution.md) to implement the execution engine
4. **Reference:** [Product Requirements](product-requirements.md) for detailed specifications

### For Economists

1. **Start with:** Product Requirements Q&A (questions 6-14) for economic modeling approach
2. **Then read:** [Entity Model](entity-model.md) for complete behavioral specifications
3. **Reference:** [Simulator Execution Flow](simulator-execution.md) for temporal ordering

## Key Concepts

### Agent-Based Modeling
The simulator uses **agent-based modeling (ABM)** where individual economic agents (households, firms, etc.) are modeled explicitly with their own states and decision rules. Macroeconomic patterns emerge from the interactions of these agents.

### Discrete Time Steps
The simulation proceeds in **discrete time steps** (e.g., days, months, quarters). Within each step, all agents update their states in a deterministic order to ensure reproducibility.

### Market Clearing
**Markets** match supply and demand:
- **Labor market:** Matches workers and jobs, determines employment and wages
- **Goods market:** Matches production and consumption, determines prices
- **Credit market (optional):** Matches lenders and borrowers, allocates credit

### Deterministic Execution
The simulator is **fully deterministic** when given the same configuration and random seed, ensuring reproducibility for scientific research.

### Configurable Parameters
All behavioral parameters, initial conditions, and shock scenarios are specified in **configuration files** (YAML/JSON), allowing easy experimentation.

## Economic Model Summary

### Household Behavior
- **Income:** Wages + transfers + capital income
- **Consumption:** Propensity to consume × disposable income
- **Savings:** Residual between income and consumption
- **Labor supply:** Fixed participation rate

### Firm Behavior
- **Production:** Cobb-Douglas function Y = A × K^α × L^(1-α)
- **Labor demand:** From profit maximization (MPL = wage)
- **Wages:** Sector baseline × productivity × market conditions
- **Investment:** Fraction of profits
- **Capital:** Accumulates with investment, depreciates over time

### Government Policy
- **Taxes:** Flat rates on household income and firm profits
- **Transfers:** Per-capita payments to households
- **Budget:** Deficit/surplus tracked, debt accumulates

### Monetary Policy
- **Inflation:** Calculated from price level changes
- **Policy rate:** Taylor rule: r = r* + 1.5×(π - π*) + 0.5×output_gap
- **Transmission:** Affects credit market rates

## Macroeconomic Indicators Tracked

The simulator tracks comprehensive macroeconomic indicators:

**Output:**
- GDP (total production)
- GDP growth rate
- GDP per capita

**Employment:**
- Total employment
- Unemployment rate
- Labor force participation

**Prices:**
- Aggregate price level
- Inflation rate
- Real vs. nominal measures

**Distribution:**
- Gini coefficient
- Income/wealth by quintile

**Fiscal:**
- Tax revenue
- Government spending
- Budget balance
- Debt-to-GDP ratio

**Monetary:**
- Policy interest rate
- Real interest rate

**Financial (optional):**
- Credit volumes
- Debt levels
- Default rates

## Implementation Recommendations

### Recommended Technology Stack

**Language:** Python 3.8+
- Rich scientific computing ecosystem
- Easy prototyping and iteration
- Good balance of performance and productivity

**Core Libraries:**
- **NumPy:** Efficient arrays and numerical operations
- **Pandas:** Data manipulation and export
- **PyYAML/JSON:** Configuration parsing
- **Matplotlib/Plotly:** Visualization
- **pytest:** Testing framework

**Optional Performance:**
- **Numba:** JIT compilation for hot loops
- **Cython:** Performance-critical components

### Development Approach

1. **Start Simple:** Implement baseline version with minimal features
2. **Test Thoroughly:** Unit tests for each agent behavior
3. **Validate Economics:** Check steady-state properties
4. **Iterate:** Add features incrementally
5. **Document:** Keep code well-documented

### Testing Strategy

**Unit Tests:**
- Test each agent decision rule independently
- Test market clearing algorithms
- Test metrics calculations

**Integration Tests:**
- Test multi-agent interactions
- Test full time-step execution
- Test shock application

**Validation Tests:**
- Verify steady-state properties
- Check responses to standard shocks
- Validate economic ratios against empirical ranges

**Reproducibility Tests:**
- Same configuration → same results
- Checkpoint/resume produces identical output

## Configuration Example

```yaml
simulation:
  time_steps: 1000
  random_seed: 42
  checkpoint_interval: 100

agents:
  households:
    count: 1000
    consumption_propensity: 0.8
    labor_participation: 0.65
    
  firms:
    count: 100
    production_alpha: 0.3
    depreciation_rate: 0.05
    investment_propensity: 0.2
    
  government:
    income_tax_rate: 0.2
    profit_tax_rate: 0.25
    per_capita_transfer: 100
    
  central_bank:
    inflation_target: 0.02
    taylor_inflation_coeff: 1.5
    taylor_output_coeff: 0.5

shocks:
  - type: demand
    time: 500
    parameter: consumption_propensity
    change: -0.1

output:
  formats: [csv, json]
  directory: ./results
```

## Usage Example

```bash
# Run simulation with default configuration
python simulator.py

# Run with custom configuration
python simulator.py --config scenarios/baseline.yaml

# Specify output directory
python simulator.py --config scenarios/baseline.yaml --output ./results/baseline

# Set random seed
python simulator.py --config scenarios/baseline.yaml --seed 42

# Resume from checkpoint
python simulator.py --resume checkpoints/checkpoint_001000.pkl
```

## Extending the Simulator

### Adding a New Agent Type

1. Create class extending `EconomicAgent`
2. Implement required methods: `update()`, `get_state()`, `set_state()`
3. Define attributes and behavioral parameters
4. Add to configuration schema
5. Integrate into simulation loop
6. Add tests

### Adding a New Shock Type

1. Define shock parameters in configuration schema
2. Implement shock application logic in `apply_shocks()`
3. Document shock effects
4. Add validation
5. Add test scenarios

### Adding a New Metric

1. Implement calculation function in `calculate_metrics()`
2. Add to data storage schema
3. Include in output exports
4. Add visualization if needed
5. Document interpretation

## Validation and Calibration

### Steady-State Validation

The baseline configuration should produce economically reasonable steady states:
- GDP grows at sustainable rate (1-3% per period)
- Unemployment settles in reasonable range (4-8%)
- Inflation near target (2%)
- Gini coefficient in empirical range (0.3-0.5)
- Government debt stable or slowly growing

### Shock Response Validation

Responses to shocks should align with economic theory:
- **Demand shock (consumption drop):** GDP falls, unemployment rises, inflation falls
- **Supply shock (productivity increase):** GDP rises, prices fall, wages rise
- **Tax increase:** Consumption falls, GDP falls
- **Monetary tightening:** Inflation moderates, output may decline

### Calibration Approach

1. **Literature Review:** Survey parameters from academic studies
2. **Empirical Matching:** Adjust to match key macro ratios
3. **Sensitivity Analysis:** Test robustness to parameter variations
4. **Expert Judgment:** Validate reasonableness with economists

## Common Issues and Solutions

### Issue: GDP Explodes or Collapses
**Cause:** Unstable parameter combination
**Solution:** 
- Check Taylor rule coefficient > 1
- Verify depreciation rate < investment rate
- Ensure consumption propensity < 1

### Issue: Simulation is Slow
**Cause:** Large agent population or inefficient implementation
**Solution:**
- Use vectorized NumPy operations
- Profile code to find bottlenecks
- Consider Numba JIT compilation
- Reduce agent count for testing

### Issue: Results Not Reproducible
**Cause:** Non-deterministic execution or uncontrolled randomness
**Solution:**
- Ensure random seed is set
- Check for race conditions (if parallelized)
- Verify update ordering is deterministic
- Check for floating-point non-determinism

## Future Enhancements

### Version 2.0 (Potential Features)

- **Stochastic Behaviors:** Random shocks and agent decisions
- **Heterogeneous Expectations:** Agents form expectations differently
- **Endogenous Innovation:** Productivity growth from R&D
- **Firm Dynamics:** Entry, exit, mergers
- **Spatial Modeling:** Geographic regions with trade
- **Richer Finance:** Asset markets, portfolio choice
- **Demographics:** Aging, birth, death dynamics
- **Environmental:** Carbon emissions, sustainability metrics

### Performance Optimization

- **Parallelization:** Multi-threaded agent updates
- **GPU Acceleration:** Large-scale agent populations
- **Distributed Computing:** Multi-node simulations
- **Database Backend:** Efficient storage for large runs

### User Interface

- **Web Dashboard:** Interactive configuration and visualization
- **Real-time Visualization:** Watch simulation progress
- **Parameter Tuning:** GUI for parameter adjustment
- **Scenario Library:** Pre-configured experiments

## Contributing

### Documentation Contributions

This documentation is living and should be updated as the project evolves:
- Fix errors or unclear sections
- Add examples and use cases
- Expand on implementation details
- Document new features

### Code Contributions

When implementing the simulator:
- Follow the architecture and design patterns
- Maintain consistency with this documentation
- Update documentation when adding features
- Include comprehensive tests
- Document all public APIs

## References and Further Reading

### Economic Modeling

- **Agent-Based Computational Economics:** Leigh Tesfatsion and Kenneth Judd
- **Monetary Policy, Inflation, and the Business Cycle:** Jordi Galí
- **Agent-Based Models of Economic Interactions:** Domenico Delli Gatti et al.

### Software Architecture

- **Design Patterns:** Gang of Four (GoF)
- **Clean Architecture:** Robert C. Martin
- **Domain-Driven Design:** Eric Evans

### Macroeconomic Theory

- **Taylor Rule:** John B. Taylor (1993)
- **NK-DSGE Models:** New Keynesian Dynamic Stochastic General Equilibrium
- **Income Distribution:** Thomas Piketty, Anthony Atkinson

## Conclusion

This documentation provides a comprehensive blueprint for building the World Economic Simulator. The four main documents cover:

1. **What** to build (Product Requirements)
2. **How** to structure it (System Architecture)  
3. **What** the agents are and do (Entity Model)
4. **How** it executes (Simulator Execution Flow)

Together, they form a complete specification that balances:
- **Economic rigor** with computational tractability
- **Flexibility** with deterministic reproducibility
- **Simplicity** with sufficient realism
- **Extensibility** with clear boundaries

The simulator will enable exploration of macroeconomic phenomena through agent-based modeling, providing insights into how individual behaviors aggregate to produce economy-wide patterns.

---

**Document Version:** 1.0  
**Last Updated:** 2026-01-27  
**Status:** Complete Draft for Review
