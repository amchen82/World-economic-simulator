# System Architecture Document: World Economic Simulator

## 1. Overview

### 1.1 Purpose
This document describes the system architecture for the World Economic Simulator, a discrete-time agent-based economic modeling platform. The architecture is designed to support reproducible, extensible, and performant simulations of macroeconomic dynamics.

### 1.2 Architectural Goals
- **Modularity:** Clear separation between simulation engine, economic models, and data management
- **Extensibility:** Easy addition of new agent types and behavioral rules
- **Performance:** Efficient processing of large agent populations over many time steps
- **Reproducibility:** Deterministic execution for scientific validity
- **Testability:** Components designed for independent testing

### 1.3 Architectural Style
The system follows a **layered architecture** combined with **agent-based modeling** patterns:
- **Presentation Layer:** CLI and data export interfaces
- **Application Layer:** Simulation orchestration and control flow
- **Domain Layer:** Economic agents and behavioral models
- **Infrastructure Layer:** Data persistence, configuration, and utilities

## 2. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                       │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │ CLI        │  │ Data Export  │  │ Visualization    │   │
│  │ Interface  │  │ (CSV/JSON)   │  │ Generation       │   │
│  └────────────┘  └──────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                        │
│  ┌────────────────────────────────────────────────────┐    │
│  │         Simulation Controller                      │    │
│  │  - Time-step loop                                  │    │
│  │  - Agent orchestration                             │    │
│  │  - Shock application                               │    │
│  └────────────────────────────────────────────────────┘    │
│  ┌────────────────────────────────────────────────────┐    │
│  │         Metrics Aggregator                         │    │
│  │  - Indicator calculation                           │    │
│  │  - Time-series storage                             │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────────┐
│                      Domain Layer                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Household │  │  Firm    │  │Government│  │ Central  │   │
│  │  Agent   │  │  Agent   │  │  Agent   │  │   Bank   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Market Mechanisms                       │  │
│  │  - Labor market clearing                            │  │
│  │  - Goods market clearing                            │  │
│  │  - Credit market (optional)                         │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           │
┌─────────────────────────────────────────────────────────────┐
│                   Infrastructure Layer                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │Configuration │  │ Data Storage │  │   Logging    │     │
│  │   Manager    │  │   Handler    │  │   Service    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Utilities                               │  │
│  │  - Random number generation                          │  │
│  │  - Mathematical helpers                              │  │
│  │  - Validation functions                              │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 3. Core Components

### 3.1 Simulation Controller

**Responsibility:** Orchestrates the entire simulation lifecycle

**Key Functions:**
- Initialize simulation state from configuration
- Execute time-step loop with deterministic ordering
- Apply scheduled shocks at appropriate time steps
- Coordinate agent updates and market clearing
- Collect and store metrics at each step
- Manage checkpointing and state persistence

**Interfaces:**
- `initialize(config: Configuration) -> SimulationState`
- `run(steps: int) -> SimulationResults`
- `step() -> StepMetrics`
- `apply_shock(shock: Shock, time: int) -> void`
- `save_checkpoint(path: string) -> void`
- `load_checkpoint(path: string) -> SimulationState`

**Algorithm (per time step):**
```
1. Update time counter
2. Apply any scheduled shocks for current time
3. Update agents in order:
   a. Firms decide production and labor demand
   b. Labor market clears (wage and employment determination)
   c. Firms produce output
   d. Government collects taxes and distributes transfers
   e. Households determine consumption and savings
   f. Goods market clears (price adjustment)
   g. Firms make investment decisions
   h. Central bank updates policy rate
   i. Banking system updates credit (if enabled)
4. Calculate and store aggregate metrics
5. Update agent states for next period
6. Check termination conditions
```

### 3.2 Agent System

**Base Agent Interface:**
```
interface Agent {
    id: string
    update(state: WorldState) -> void
    get_state() -> AgentState
    set_state(state: AgentState) -> void
}
```

#### 3.2.1 Household Agent

**State Variables:**
- Income (current and historical)
- Wealth/savings
- Consumption
- Labor supply
- Tax burden
- Transfers received

**Behaviors:**
- Calculate disposable income
- Determine consumption (propensity * disposable income)
- Calculate savings (residual)
- Supply labor (fixed participation rate)

**Parameters:**
- Consumption propensity
- Labor participation rate
- Initial wealth
- Skill level (affects wage)

#### 3.2.2 Firm Agent

**State Variables:**
- Capital stock
- Labor employed
- Output produced
- Wages paid
- Profits
- Prices
- Investment

**Behaviors:**
- Determine labor demand (profit maximization)
- Produce output (Cobb-Douglas function)
- Set wages (sector baseline * productivity)
- Make investment decisions (fraction of profits)
- Update capital stock (investment - depreciation)

**Parameters:**
- Production function parameters (alpha, TFP)
- Depreciation rate
- Investment propensity
- Sector classification
- Initial capital

#### 3.2.3 Government Agent

**State Variables:**
- Tax revenue (current and historical)
- Transfer payments
- Budget balance
- Public debt
- Spending

**Behaviors:**
- Collect taxes (flat rates on income and profits)
- Distribute transfers (per-capita)
- Calculate budget balance
- Accumulate debt

**Parameters:**
- Income tax rate
- Profit tax rate
- Per-capita transfer amount
- Initial debt level

#### 3.2.4 Central Bank Agent

**State Variables:**
- Policy rate (current and historical)
- Inflation rate
- Inflation target

**Behaviors:**
- Calculate inflation (from price level changes)
- Set policy rate (Taylor rule)
- Influence credit market rates

**Parameters:**
- Inflation target
- Taylor rule coefficients (inflation gap, output gap)
- Initial policy rate

### 3.3 Market Mechanisms

#### 3.3.1 Labor Market

**Function:** Match labor supply and demand, determine wages and employment

**Algorithm:**
```
1. Aggregate labor supply from all households
2. Aggregate labor demand from all firms
3. If demand > supply:
   - Employment = supply (full employment)
   - Upward wage pressure
4. If supply > demand:
   - Employment = demand (unemployment exists)
   - Downward wage pressure (with floor)
5. Distribute employment to workers
6. Update unemployment rate
```

**Outputs:**
- Total employment
- Unemployment rate
- Average wage
- Labor force participation

#### 3.3.2 Goods Market

**Function:** Match production and consumption, determine prices

**Algorithm:**
```
1. Aggregate production from all firms
2. Aggregate consumption demand from households + investment + government
3. Calculate excess demand/supply
4. Adjust prices:
   - If excess demand: raise prices
   - If excess supply: lower prices (with floor)
5. Clear market (adjust inventories or rationing if needed)
```

**Outputs:**
- Price level
- Inflation rate
- Inventories (if modeled)

#### 3.3.3 Credit Market (Optional)

**Function:** Allocate credit to borrowers subject to constraints

**Algorithm:**
```
1. Calculate borrowing demand (households + firms)
2. Apply loan-to-income constraints
3. Determine credit supply
4. Allocate credit (pro-rata if constrained)
5. Update debt stocks
6. Process defaults (deterministic thresholds)
7. Calculate interest rates (policy rate + spread)
```

**Outputs:**
- Total credit extended
- Credit constraint indicators
- Default rates
- Debt levels

### 3.4 Metrics Aggregator

**Responsibility:** Calculate macroeconomic indicators from agent-level data

**Key Metrics:**

**Output & Growth:**
- GDP (sum of firm production)
- GDP growth rate
- GDP per capita

**Employment:**
- Total employment
- Unemployment rate
- Labor force participation rate

**Prices & Inflation:**
- Price level (aggregate)
- Inflation rate (% change in prices)
- Real vs nominal GDP

**Income Distribution:**
- Gini coefficient
- Income quintiles/deciles
- Share of income by group

**Fiscal:**
- Government revenue
- Government spending
- Budget deficit/surplus
- Debt-to-GDP ratio

**Monetary:**
- Policy interest rate
- Real interest rate
- Money supply (if modeled)

**Financial (if applicable):**
- Total credit
- Household debt
- Firm debt
- Default rates

**Trade (if applicable):**
- Exports
- Imports
- Net exports
- Trade balance

**Interfaces:**
- `calculate_gdp(firms: List[Firm]) -> float`
- `calculate_unemployment(households: List[Household]) -> float`
- `calculate_inflation(prices: TimeSeries) -> float`
- `calculate_gini(incomes: List[float]) -> float`
- `get_all_metrics() -> MetricsSnapshot`

### 3.5 Configuration Manager

**Responsibility:** Load, validate, and provide access to simulation parameters

**Configuration Structure:**
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
    initial_wealth_distribution: "uniform"
  
  firms:
    count: 100
    sectors: ["manufacturing", "services", "agriculture"]
    production_alpha: 0.3
    depreciation_rate: 0.05
    investment_propensity: 0.2
  
  government:
    income_tax_rate: 0.2
    profit_tax_rate: 0.25
    per_capita_transfer: 100
    initial_debt: 0
  
  central_bank:
    inflation_target: 0.02
    taylor_rule_inflation_coeff: 1.5
    taylor_rule_output_coeff: 0.5

shocks:
  - type: "demand"
    time: 500
    parameter: "consumption_propensity"
    change: -0.1
  
  - type: "productivity"
    time: 750
    parameter: "TFP"
    change: 0.05

output:
  formats: ["csv", "json"]
  metrics: ["gdp", "unemployment", "inflation", "gini"]
  aggregation_level: "timestep"
```

**Interfaces:**
- `load_config(path: string) -> Configuration`
- `validate_config(config: Configuration) -> ValidationResult`
- `get_parameter(path: string) -> Any`
- `set_parameter(path: string, value: Any) -> void`

### 3.6 Data Storage Handler

**Responsibility:** Persist simulation data efficiently

**Storage Strategy:**
- **In-memory:** Time-series data during simulation (arrays/matrices)
- **Disk:** Final results, checkpoints, configuration

**Data Structures:**
- Time-series: NumPy arrays or similar for efficient numerical operations
- Agent states: Structured arrays or dataframes
- Metadata: JSON for configuration and parameters

**Interfaces:**
- `store_timestep(time: int, metrics: MetricsSnapshot) -> void`
- `export_csv(metrics: List[str], path: string) -> void`
- `export_json(path: string) -> void`
- `save_state(state: SimulationState, path: string) -> void`
- `load_state(path: string) -> SimulationState`

## 4. Data Flow

### 4.1 Initialization Flow
```
1. Load configuration file
2. Validate parameters
3. Initialize random number generator with seed
4. Create agents:
   - Generate agent populations
   - Assign initial parameters
   - Set initial states
5. Initialize markets
6. Initialize metrics storage
7. Create initial snapshot
```

### 4.2 Time-Step Processing Flow
```
┌─────────────────┐
│  Time Step t    │
└────────┬────────┘
         │
         ├──────> 1. Firms: Labor Demand Calculation
         │           ↓
         ├──────> 2. Labor Market Clearing
         │           ├─> Employment Determination
         │           └─> Wage Setting
         │           ↓
         ├──────> 3. Firms: Production
         │           └─> Output = f(Capital, Labor)
         │           ↓
         ├──────> 4. Government: Tax & Transfers
         │           ├─> Collect Taxes
         │           └─> Distribute Transfers
         │           ↓
         ├──────> 5. Households: Consumption Decision
         │           ├─> Calculate Disposable Income
         │           └─> Determine Consumption & Savings
         │           ↓
         ├──────> 6. Goods Market Clearing
         │           ├─> Match Supply & Demand
         │           └─> Price Adjustment
         │           ↓
         ├──────> 7. Firms: Investment Decision
         │           └─> Capital Accumulation
         │           ↓
         ├──────> 8. Central Bank: Policy Rate
         │           └─> Set Rate Based on Inflation
         │           ↓
         ├──────> 9. Banking: Credit Update (optional)
         │           ↓
         ├──────> 10. Metrics Calculation
         │           └─> Aggregate All Indicators
         │           ↓
         └──────> 11. State Update & Storage
                     ↓
                ┌──────────┐
                │ Time t+1 │
                └──────────┘
```

### 4.3 Data Export Flow
```
1. Simulation completes
2. Aggregate metrics from all time steps
3. Calculate summary statistics
4. Transform data to export format
5. Write to files (CSV/JSON)
6. Generate visualization datasets
7. Log completion status
```

## 5. Design Patterns

### 5.1 Strategy Pattern (Agent Behaviors)
Different behavioral rules can be swapped without changing agent structure:
- Consumption strategies (Keynesian, life-cycle, etc.)
- Wage-setting strategies (competitive, sticky, bargaining)
- Investment strategies (accelerator, q-theory, etc.)

### 5.2 Observer Pattern (Metrics Collection)
Metrics aggregator observes agent state changes:
- Agents notify on state updates
- Aggregator collects and processes updates
- Decouples agents from metrics calculation

### 5.3 Command Pattern (Shocks)
Shocks encapsulated as commands:
- Each shock type is a command object
- Supports undo/redo for experimentation
- Easy scheduling and composition

### 5.4 Factory Pattern (Agent Creation)
Agent factories handle instantiation:
- Configuration-driven agent creation
- Consistent initialization
- Easy to extend with new agent types

### 5.5 Singleton Pattern (Configuration, RNG)
Single instances for global resources:
- Configuration manager
- Random number generator (for reproducibility)
- Logging service

## 6. Technology Stack

### 6.1 Recommended Technologies

**Core Language:** Python 3.8+
- Rationale: Rich ecosystem for scientific computing, easy prototyping, good libraries

**Data Structures:**
- NumPy: Efficient arrays for time-series and agent states
- Pandas: Data manipulation and export
- NetworkX (optional): If modeling network effects

**Configuration:**
- PyYAML or JSON: Configuration file parsing

**Testing:**
- pytest: Unit and integration testing
- hypothesis: Property-based testing for validation

**Performance (if needed):**
- Numba: JIT compilation for hot loops
- Cython: Performance-critical components

**Visualization:**
- Matplotlib: Chart generation
- Plotly (optional): Interactive visualizations

**Documentation:**
- Sphinx: API documentation
- Markdown: User guides

### 6.2 Alternative Technology Stacks

**For High Performance:**
- Core: Julia or C++
- Bindings: Python wrapper for user interface

**For Distributed Simulation:**
- Apache Spark: Parallel agent processing
- Dask: Distributed computing in Python

## 7. Deployment Architecture

### 7.1 Local Execution
```
User Machine
├── Python Environment
├── Simulator Code
├── Configuration Files
├── Input Data
└── Output Data
```

### 7.2 Batch Processing
```
Compute Cluster
├── Job Scheduler (SLURM, PBS)
├── Multiple Simulation Instances
├── Shared File System
│   ├── Configurations
│   └── Results
└── Post-Processing Pipeline
```

### 7.3 Cloud Deployment (Future)
```
Cloud Platform (AWS/GCP/Azure)
├── Compute: Container instances (Docker)
├── Storage: Object storage (S3/GCS)
├── Orchestration: Kubernetes
└── API: REST API for remote execution
```

## 8. Security and Reliability

### 8.1 Input Validation
- Validate all configuration parameters
- Check for logical consistency (e.g., rates between 0 and 1)
- Sanitize file paths
- Limit resource usage (memory, time)

### 8.2 Error Handling
- Graceful degradation on non-critical errors
- Clear error messages with actionable guidance
- Logging of all errors and warnings
- Automatic checkpoint on crashes (if possible)

### 8.3 Reproducibility Mechanisms
- Deterministic random number generation with seed control
- Fixed update ordering
- Version tracking of configuration and code
- Checksums for configuration files

## 9. Performance Considerations

### 9.1 Optimization Strategies
- Vectorized operations for agent updates where possible
- Efficient data structures (NumPy arrays vs Python lists)
- Minimize object creation in hot loops
- Cache frequently accessed values
- Profile-guided optimization

### 9.2 Scalability
- Memory: O(N*T) where N=agents, T=time steps
- Computation: O(N*T) for agent updates
- Target: 1000 agents × 1000 steps in <5 minutes

### 9.3 Bottleneck Mitigation
- Market clearing can be O(N log N) with efficient sorting
- Agent updates embarrassingly parallel (future enhancement)
- Metrics calculation can be incremental

## 10. Testing Strategy

### 10.1 Unit Tests
- Individual agent behaviors
- Market clearing mechanisms
- Metrics calculations
- Configuration validation

### 10.2 Integration Tests
- Multi-agent interactions
- Full time-step processing
- Shock application
- Data export

### 10.3 Validation Tests
- Steady-state properties
- Known shock responses
- Economic consistency checks
- Reproducibility verification

### 10.4 Performance Tests
- Benchmark scenarios
- Memory profiling
- Scalability testing

## 11. Future Architectural Enhancements

### 11.1 Parallel Processing
- Multi-threaded agent updates
- Distributed simulation across nodes
- GPU acceleration for large populations

### 11.2 Real-time Interaction
- Web-based dashboard
- Parameter adjustment during simulation
- Live visualization

### 11.3 Machine Learning Integration
- Parameter calibration using ML
- Agent behavior learning
- Prediction and forecasting

### 11.4 Modular Plugin System
- External agent behavior plugins
- Custom metric calculators
- Third-party shock scenarios

## 12. Conclusion

This architecture provides a solid foundation for the World Economic Simulator that balances:
- **Simplicity:** Clear structure, easy to understand
- **Extensibility:** New agents and behaviors can be added
- **Performance:** Efficient for target scale
- **Reliability:** Deterministic and testable
- **Maintainability:** Well-organized, documented code

The layered architecture with clear separation of concerns enables independent development and testing of components while maintaining system coherence.
