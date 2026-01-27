# Product Requirements Document: World Economic Simulator

## Executive Summary
The World Economic Simulator is a mid-level realism economic modeling system designed to simulate the collective behavior of economic agents (households, firms, government, and central bank) over time. The simulator aims to provide insights into macroeconomic dynamics through agent-based modeling.

## Requirements Development: Expert Q&A

### Software Engineering Perspective

#### Q1: What is the primary purpose of this simulator?
**A:** The simulator serves as a computational platform for exploring macroeconomic phenomena through agent-based modeling. It enables users to:
- Observe emergent macroeconomic patterns from individual agent behaviors
- Test policy interventions and economic shocks
- Generate time-series data for economic indicators
- Validate economic theories through computational experiments

#### Q2: What are the key non-functional requirements?
**A:** 
- **Performance:** Capable of simulating 1000+ agents over 1000+ time steps in reasonable time (<5 minutes)
- **Reproducibility:** Deterministic execution with seed control for research validation
- **Extensibility:** Modular architecture allowing new agent types and behaviors
- **Configurability:** All parameters controllable via configuration files
- **Observability:** Comprehensive logging and metrics collection at each time step

#### Q3: What technical constraints should guide the design?
**A:**
- Single-threaded execution initially (simplifies state management)
- Deterministic update ordering (ensures reproducibility)
- Memory-efficient data structures (support large agent populations)
- Clear separation between simulation engine and economic models
- Platform-independent implementation

#### Q4: What are the data input and output requirements?
**A:**
- **Input:** Configuration files (YAML/JSON) specifying initial conditions, parameters, and shock scenarios
- **Output:** Time-series data in CSV/JSON format, aggregated metrics, visualization-ready datasets
- **State Management:** Ability to save/load simulation state for checkpoint-restart

#### Q5: What quality assurance mechanisms are needed?
**A:**
- Unit tests for individual agent behaviors
- Integration tests for multi-agent interactions
- Regression tests comparing outputs to baseline scenarios
- Parameter validation and bounds checking
- Reproducibility tests (same config yields same results)

### Economic Modeling Perspective

#### Q6: What level of economic realism is appropriate?
**A:** Mid-level realism balancing:
- **Sufficient complexity:** Capture key economic mechanisms (production, consumption, monetary policy)
- **Manageable simplicity:** Avoid overfitting and computational intractability
- **Theoretical grounding:** Based on established macroeconomic frameworks
- **Practical usefulness:** Generates meaningful insights without excessive calibration

#### Q7: What are the essential economic agents to model?
**A:**
- **Households:** Consumer-workers who supply labor, consume goods, save, and pay taxes
- **Firms:** Producers organized by sectors who hire labor, produce goods, invest, and set prices
- **Government:** Fiscal authority that collects taxes, provides transfers, and manages public debt
- **Central Bank:** Monetary authority that sets policy rates and targets inflation
- **Banking System (optional):** Credit intermediaries that enable borrowing and enforce constraints

#### Q8: What are the critical economic flows to capture?
**A:**
- **Labor market:** Wage determination, employment/unemployment dynamics
- **Goods market:** Production, consumption, inventory adjustments
- **Credit flows:** Lending, borrowing, debt accumulation
- **Fiscal flows:** Tax collection, government spending, deficit/surplus
- **Monetary flows:** Interest rates, inflation, monetary policy transmission
- **Trade flows (optional):** Imports, exports, exchange rates

#### Q9: What behavioral rules should govern agents?
**A:**
- **Households:** 
  - Consumption follows propensity to consume out of disposable income
  - Labor supply determined by participation rates
  - Savings as residual between income and consumption
- **Firms:**
  - Production via Cobb-Douglas function
  - Labor demand from profit maximization
  - Wages set by sector and productivity
  - Investment as fraction of profits
- **Government:**
  - Flat tax rates on income and profits
  - Per-capita transfers
  - Budget constraint tracking
- **Central Bank:**
  - Taylor-rule type policy rate setting
  - Inflation targeting

#### Q10: What macroeconomic indicators should be tracked?
**A:**
- **Output:** GDP (aggregate production), GDP growth rate
- **Employment:** Total employment, unemployment rate, labor force participation
- **Prices:** Inflation rate, price level, real vs nominal measures
- **Income distribution:** Gini coefficient, income shares by quintile
- **Fiscal:** Government revenue, spending, deficit/surplus, debt-to-GDP ratio
- **Monetary:** Policy rate, real interest rate
- **Trade (if applicable):** Net exports, trade balance
- **Financial:** Credit volumes, default rates, household/firm debt levels

#### Q11: How should time be modeled?
**A:**
- Discrete time steps (e.g., daily, monthly, quarterly)
- Configurable simulation horizon (number of steps)
- Sequential processing within each time step
- Clear temporal ordering of decisions (wages → production → consumption → policy)

#### Q12: What types of shocks and interventions should be supported?
**A:**
- **Demand shocks:** Changes in household consumption propensity
- **Supply shocks:** Changes in productivity or production capacity
- **Policy shocks:** Changes in tax rates, transfers, or policy rules
- **Financial shocks:** Changes in credit constraints or default rates
- **External shocks:** Changes in trade parameters or foreign conditions
- All shocks should be schedulable at specific time steps

#### Q13: How should heterogeneity be incorporated?
**A:**
- **Households:** Different income levels, consumption propensities, skill levels
- **Firms:** Different sectors, productivity levels, sizes
- **Spatial (optional):** Geographic regions with different characteristics
- Heterogeneity should be parameterizable to study distributional effects

#### Q14: What economic validation is required?
**A:**
- Steady-state properties should be economically reasonable
- Responses to standard shocks should align with economic theory
- Key ratios (consumption/GDP, investment/GDP, etc.) should match empirical ranges
- No unintended explosive or degenerative dynamics in baseline scenario

## Functional Requirements

### FR1: Simulation Engine
- **FR1.1:** Execute discrete time-step loop up to configurable horizon
- **FR1.2:** Initialize all agents with specified distributions and parameters
- **FR1.3:** Process agents in deterministic order within each time step
- **FR1.4:** Support checkpoint save/load for long simulations
- **FR1.5:** Provide progress indicators for long-running simulations

### FR2: Household Agent
- **FR2.1:** Calculate disposable income (wages + transfers - taxes)
- **FR2.2:** Determine consumption based on propensity to consume
- **FR2.3:** Calculate savings as residual
- **FR2.4:** Supply labor based on participation rate
- **FR2.5:** Track individual wealth accumulation

### FR3: Firm Agent
- **FR3.1:** Produce output using Cobb-Douglas production function
- **FR3.2:** Determine labor demand from profit maximization
- **FR3.3:** Set wages based on sector baseline and productivity
- **FR3.4:** Make investment decisions based on profit share
- **FR3.5:** Track capital stock with depreciation

### FR4: Government Agent
- **FR4.1:** Collect taxes at specified rates
- **FR4.2:** Distribute transfers to households
- **FR4.3:** Track budget balance each time step
- **FR4.4:** Accumulate public debt
- **FR4.5:** Support policy rule changes via configuration

### FR5: Central Bank Agent
- **FR5.1:** Calculate inflation from price changes
- **FR5.2:** Set policy rate using Taylor-type rule
- **FR5.3:** Maintain inflation target parameter
- **FR5.4:** Influence credit market rates

### FR6: Banking System (Optional)
- **FR6.1:** Extend credit to households and firms
- **FR6.2:** Apply loan-to-income constraints
- **FR6.3:** Track credit volumes and outstanding debt
- **FR6.4:** Process defaults deterministically

### FR7: Trade Module (Optional)
- **FR7.1:** Calculate net exports based on openness and relative prices
- **FR7.2:** Apply tariffs to imports
- **FR7.3:** Track trade balance

### FR8: Metrics and Reporting
- **FR8.1:** Calculate all specified macroeconomic indicators each step
- **FR8.2:** Store time-series data in memory-efficient format
- **FR8.3:** Export data to CSV and JSON formats
- **FR8.4:** Generate visualization-ready datasets
- **FR8.5:** Produce summary statistics and reports

### FR9: Configuration Management
- **FR9.1:** Load all parameters from YAML/JSON configuration files
- **FR9.2:** Validate parameter ranges and consistency
- **FR9.3:** Support multiple configuration profiles
- **FR9.4:** Document all parameters with descriptions and defaults

### FR10: Shock Scenarios
- **FR10.1:** Support scheduling shocks at specific time steps
- **FR10.2:** Allow multiple shock types in single simulation
- **FR10.3:** Validate shock parameters before execution
- **FR10.4:** Log all shocks applied during simulation

## Non-Functional Requirements

### NFR1: Performance
- Simulate 1000 agents over 1000 steps in under 5 minutes on standard hardware
- Memory usage scales linearly with agent count
- Time-step processing time constant regardless of simulation length

### NFR2: Reliability
- Deterministic execution for same configuration and seed
- No crashes from valid input configurations
- Graceful handling of edge cases (e.g., zero employment)

### NFR3: Maintainability
- Modular code structure with clear separation of concerns
- Comprehensive inline documentation
- Consistent coding style and naming conventions
- Minimal external dependencies

### NFR4: Usability
- Clear error messages with actionable guidance
- Example configurations for common scenarios
- Comprehensive user documentation
- Simple command-line interface

### NFR5: Testability
- All core behaviors unit tested
- Reproducibility verified through regression tests
- Test coverage >80% for core modules

## Success Criteria

1. **Baseline Scenario:** Simulator runs to completion without errors and produces economically reasonable steady state
2. **Shock Response:** Simulator correctly responds to standard demand and supply shocks
3. **Reproducibility:** Identical configurations produce identical outputs across runs
4. **Performance:** Meets performance benchmarks for agent count and time steps
5. **Validation:** Key economic ratios fall within empirically observed ranges
6. **Documentation:** Complete documentation enables new users to run and understand simulations

## Out of Scope (Version 1)

- Stochastic agent behaviors (all rules deterministic)
- Spatial/geographic modeling
- Endogenous technical change
- Detailed financial markets (stocks, bonds)
- Firm entry and exit dynamics
- Expectations formation models
- Multi-country modeling
- Real-time visualization during simulation
- Web-based user interface

## Future Enhancements (Post-V1)

- Stochastic shocks and agent behaviors
- Learning and adaptive expectations
- Endogenous innovation and productivity growth
- Richer financial sector with asset markets
- Demographic dynamics (birth, death, aging)
- Environmental and sustainability metrics
- Machine learning for parameter calibration
- Interactive web-based dashboard
