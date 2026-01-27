# Simulator Execution Flow Document

## 1. Overview

This document describes how the World Economic Simulator executes, from initialization through time-step processing to final output generation. It provides detailed algorithmic specifications and control flow diagrams.

## 2. High-Level Execution Flow

```
┌─────────────────────────────────────────────────────────────┐
│                   Simulator Lifecycle                       │
│                                                             │
│  1. Load Configuration                                      │
│       ↓                                                     │
│  2. Validate Parameters                                     │
│       ↓                                                     │
│  3. Initialize System                                       │
│       ├─> Create Agents                                    │
│       ├─> Initialize Markets                               │
│       ├─> Set Initial State                                │
│       └─> Prepare Data Storage                             │
│       ↓                                                     │
│  4. Run Simulation Loop                                     │
│       ├─> Execute Time Step 1                              │
│       ├─> Execute Time Step 2                              │
│       ├─> ...                                              │
│       └─> Execute Time Step T                              │
│       ↓                                                     │
│  5. Generate Outputs                                        │
│       ├─> Export Time Series                               │
│       ├─> Calculate Statistics                             │
│       └─> Create Visualizations                            │
│       ↓                                                     │
│  6. Cleanup and Exit                                        │
└─────────────────────────────────────────────────────────────┘
```

## 3. Detailed Phase Descriptions

### Phase 1: Configuration Loading

**Purpose:** Read and parse simulation parameters from configuration files

**Steps:**
1. Locate configuration file (path provided via command line or default)
2. Parse YAML/JSON file
3. Load parameter values into Configuration object
4. Set default values for unspecified parameters

**Input:** Configuration file path
**Output:** Configuration object
**Error Handling:** 
- Missing file → Use default configuration or abort
- Malformed file → Report syntax errors with line numbers
- Unknown parameters → Warning (ignored) or error (strict mode)

**Pseudocode:**
```python
def load_configuration(config_path: str) -> Configuration:
    """Load simulation configuration from file"""
    
    # Check file exists
    if not file_exists(config_path):
        if USE_DEFAULTS:
            log.warning(f"Config file {config_path} not found, using defaults")
            return Configuration.defaults()
        else:
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    # Parse file
    try:
        with open(config_path, 'r') as f:
            if config_path.endswith('.yaml') or config_path.endswith('.yml'):
                config_dict = yaml.safe_load(f)
            elif config_path.endswith('.json'):
                config_dict = json.load(f)
            else:
                raise ValueError(f"Unsupported config format: {config_path}")
    except Exception as e:
        raise ConfigurationError(f"Failed to parse config: {e}")
    
    # Create Configuration object
    config = Configuration.from_dict(config_dict)
    
    # Apply defaults for missing values
    config.apply_defaults()
    
    return config
```

### Phase 2: Parameter Validation

**Purpose:** Ensure all parameters are within valid ranges and logically consistent

**Validation Checks:**

**Range Checks:**
- `0 <= tax rates <= 1`
- `0 <= propensities <= 1`
- `0 < alpha < 1` (production parameter)
- `depreciation_rate > 0`
- `time_steps > 0`
- `agent_counts > 0`

**Consistency Checks:**
- Taylor coefficient > 1 (stability)
- Sum of sector weights = 1 (if applicable)
- Initial debt >= 0
- Scheduled shocks within time horizon

**Economic Reasonableness:**
- Inflation target: 0% to 10%
- Consumption propensity: 0.5 to 0.95
- Investment propensity: 0.05 to 0.4
- Tax rates: typical ranges based on empirical data

**Pseudocode:**
```python
def validate_configuration(config: Configuration) -> ValidationResult:
    """Validate all configuration parameters"""
    
    errors = []
    warnings = []
    
    # Range validations
    if not (0 <= config.income_tax_rate <= 1):
        errors.append("Income tax rate must be between 0 and 1")
    
    if not (0 < config.production_alpha < 1):
        errors.append("Production alpha must be between 0 and 1")
    
    if config.time_steps <= 0:
        errors.append("Time steps must be positive")
    
    if config.household_count <= 0:
        errors.append("Household count must be positive")
    
    # Consistency checks
    if config.taylor_inflation_coeff <= 1:
        warnings.append("Taylor coefficient <= 1 may cause instability")
    
    # Economic reasonableness
    if config.inflation_target > 0.10:
        warnings.append(f"Inflation target {config.inflation_target} unusually high")
    
    # Shock validation
    for shock in config.shocks:
        if shock.time > config.time_steps:
            errors.append(f"Shock at time {shock.time} exceeds simulation horizon")
    
    return ValidationResult(
        valid=(len(errors) == 0),
        errors=errors,
        warnings=warnings
    )
```

### Phase 3: System Initialization

**Purpose:** Create all entities and set initial conditions

#### 3.1 Agent Creation

**Households:**
```python
def create_households(config: Configuration) -> List[Household]:
    """Create household agent population"""
    
    households = []
    
    for i in range(config.household_count):
        household = Household(id=f"HH_{i:05d}")
        
        # Assign parameters from distributions
        household.consumption_propensity = sample_from_distribution(
            config.consumption_propensity_dist
        )
        
        household.skill_level = sample_from_distribution(
            config.skill_level_dist
        )
        
        household.participation_rate = config.labor_participation_rate
        
        # Initialize state
        household.wealth = sample_from_distribution(
            config.initial_wealth_dist
        )
        
        household.income = 0
        household.consumption = 0
        household.employed = False
        
        households.append(household)
    
    return households
```

**Firms:**
```python
def create_firms(config: Configuration) -> List[Firm]:
    """Create firm agent population"""
    
    firms = []
    
    # Distribute firms across sectors
    firms_per_sector = allocate_firms_to_sectors(
        config.firm_count,
        config.sector_weights
    )
    
    firm_id = 0
    for sector, count in firms_per_sector.items():
        for i in range(count):
            firm = Firm(id=f"FIRM_{firm_id:05d}", sector=sector)
            
            # Set production parameters
            firm.alpha = config.production_alpha
            firm.productivity = sample_from_distribution(
                config.productivity_dist
            )
            firm.depreciation_rate = config.depreciation_rate
            
            # Initialize capital
            firm.capital_stock = sample_from_distribution(
                config.initial_capital_dist
            )
            
            # Set behavioral parameters
            firm.investment_propensity = config.investment_propensity
            firm.markup = config.price_markup
            
            # Initialize state
            firm.labor_employed = 0
            firm.output = 0
            firm.price = 1.0  # Normalized initial price
            
            firms.append(firm)
            firm_id += 1
    
    return firms
```

**Government:**
```python
def create_government(config: Configuration) -> Government:
    """Create government agent"""
    
    government = Government(id="GOV_001")
    
    # Set policy parameters
    government.income_tax_rate = config.income_tax_rate
    government.profit_tax_rate = config.profit_tax_rate
    government.per_capita_transfer = config.per_capita_transfer
    
    # Initialize state
    government.public_debt = config.initial_public_debt
    government.tax_revenue = 0
    government.transfer_payments = 0
    government.budget_balance = 0
    
    return government
```

**Central Bank:**
```python
def create_central_bank(config: Configuration) -> CentralBank:
    """Create central bank agent"""
    
    central_bank = CentralBank(id="CB_001")
    
    # Set policy parameters
    central_bank.inflation_target = config.inflation_target
    central_bank.taylor_inflation_coeff = config.taylor_inflation_coeff
    central_bank.taylor_output_coeff = config.taylor_output_coeff
    central_bank.neutral_rate = config.neutral_interest_rate
    
    # Initialize state
    central_bank.policy_rate = config.initial_policy_rate
    central_bank.inflation_rate = 0
    central_bank.price_level = 1.0  # Normalized
    central_bank.price_level_prev = 1.0
    
    return central_bank
```

#### 3.2 Market Initialization

```python
def create_markets(config: Configuration) -> Markets:
    """Create market mechanisms"""
    
    markets = Markets()
    
    # Labor market
    markets.labor_market = LaborMarket()
    markets.labor_market.minimum_wage = config.minimum_wage
    
    # Goods market
    markets.goods_market = GoodsMarket()
    markets.goods_market.price_adjustment_speed = config.price_adjustment_speed
    
    # Credit market (optional)
    if config.enable_credit_market:
        markets.credit_market = CreditMarket()
        markets.credit_market.loan_to_income_limit = config.loan_to_income_limit
        markets.credit_market.lending_spread = config.lending_spread
    
    return markets
```

#### 3.3 Data Storage Preparation

```python
def initialize_data_storage(config: Configuration) -> DataStorage:
    """Prepare data structures for storing time series"""
    
    storage = DataStorage()
    
    # Pre-allocate arrays for time series
    T = config.time_steps
    
    storage.time = np.arange(T)
    storage.gdp = np.zeros(T)
    storage.unemployment = np.zeros(T)
    storage.inflation = np.zeros(T)
    storage.policy_rate = np.zeros(T)
    storage.gini = np.zeros(T)
    storage.government_debt = np.zeros(T)
    # ... other metrics
    
    # Agent-level data (optional, memory-intensive)
    if config.store_agent_level_data:
        N_households = config.household_count
        N_firms = config.firm_count
        
        storage.household_income = np.zeros((T, N_households))
        storage.household_wealth = np.zeros((T, N_households))
        storage.firm_output = np.zeros((T, N_firms))
        # ... other agent-level variables
    
    return storage
```

#### 3.4 Random Number Generator Setup

```python
def initialize_rng(config: Configuration) -> RandomGenerator:
    """Initialize random number generator with seed for reproducibility"""
    
    if config.random_seed is not None:
        seed = config.random_seed
        log.info(f"Initializing RNG with seed: {seed}")
    else:
        seed = int(time.time())
        log.info(f"No seed provided, using timestamp: {seed}")
    
    rng = np.random.RandomState(seed)
    
    # Also set global random state for libraries that use it
    np.random.seed(seed)
    random.seed(seed)
    
    return rng
```

### Phase 4: Simulation Loop

**Purpose:** Execute the time-step loop, the core of the simulation

**Main Loop Structure:**
```python
def run_simulation(
    config: Configuration,
    agents: Agents,
    markets: Markets,
    storage: DataStorage
) -> SimulationResults:
    """Execute the main simulation loop"""
    
    log.info(f"Starting simulation: {config.time_steps} time steps")
    
    for t in range(config.time_steps):
        
        # Progress indicator
        if t % 100 == 0:
            log.info(f"Time step {t}/{config.time_steps}")
        
        # Apply scheduled shocks
        apply_shocks(t, config.shocks, agents)
        
        # Execute time step
        metrics = execute_time_step(t, agents, markets, config)
        
        # Store metrics
        store_metrics(storage, t, metrics, agents)
        
        # Checkpoint if needed
        if config.checkpoint_interval > 0 and t % config.checkpoint_interval == 0:
            save_checkpoint(t, agents, markets, config)
        
        # Check termination conditions
        if check_early_termination(metrics, config):
            log.warning(f"Early termination at step {t}")
            break
    
    log.info("Simulation completed successfully")
    
    return SimulationResults(storage, agents, config)
```

**Single Time Step Execution:**
```python
def execute_time_step(
    t: int,
    agents: Agents,
    markets: Markets,
    config: Configuration
) -> Metrics:
    """Execute one discrete time step"""
    
    households = agents.households
    firms = agents.firms
    government = agents.government
    central_bank = agents.central_bank
    
    # ========== Step 1: Firm Wage Setting and Labor Demand ==========
    
    # Firms observe market conditions and set wages
    market_conditions = markets.labor_market.get_conditions()
    
    for firm in firms:
        firm.set_wage(market_conditions)
        firm.calculate_labor_demand(firm.wage_rate)
    
    # ========== Step 2: Labor Market Clearing ==========
    
    # Households supply labor
    for household in households:
        household.supply_labor()
    
    # Market matches supply and demand
    employment = markets.labor_market.clear_market(households, firms)
    
    # Update household employment status and wage income
    # (done within labor market clearing)
    
    # ========== Step 3: Production ==========
    
    for firm in firms:
        firm.produce()  # Uses production function with K and L
    
    # ========== Step 4: Government Tax Collection and Transfers ==========
    
    # Calculate income for households
    for household in households:
        household.calculate_income()  # wage + transfers + capital income
    
    # Government collects taxes
    government.collect_taxes(households, firms)
    
    # Government distributes transfers
    government.distribute_transfers(households)
    
    # Households recalculate disposable income after taxes/transfers
    for household in households:
        household.disposable_income = household.income - household.taxes_paid
    
    # ========== Step 5: Household Consumption Decision ==========
    
    total_consumption_demand = 0
    for household in households:
        household.decide_consumption()
        total_consumption_demand += household.consumption
    
    # ========== Step 6: Goods Market Clearing ==========
    
    # Aggregate demand includes consumption + investment + government
    # (For simplicity, investment calculated after goods market in this version)
    government_demand = 0  # Simplified: government consumes zero in v1
    
    # Firms made investment decisions (we'll calculate this after profit)
    # For now, use total consumption as main demand
    
    total_demand = total_consumption_demand + government_demand
    
    # Goods market clears, adjusts prices
    aggregate_price = markets.goods_market.clear_market(firms, total_demand)
    
    # ========== Step 7: Firm Profit Calculation and Investment ==========
    
    for firm in firms:
        firm.calculate_profits()
        firm.decide_investment()
        firm.update_capital()
    
    # ========== Step 8: Household Savings ==========
    
    for household in households:
        household.calculate_savings()  # Updates wealth
    
    # ========== Step 9: Government Budget Balance ==========
    
    government.calculate_budget_balance()
    government.update_debt()
    
    # ========== Step 10: Central Bank Policy Rate ==========
    
    # Calculate output gap (current GDP vs potential)
    current_gdp = sum(firm.output for firm in firms)
    potential_gdp = calculate_potential_gdp(firms)  # Assumes full employment
    output_gap = (current_gdp - potential_gdp) / potential_gdp if potential_gdp > 0 else 0
    
    # Central bank calculates inflation
    central_bank.calculate_inflation(aggregate_price)
    
    # Central bank sets policy rate
    central_bank.set_policy_rate(output_gap)
    
    # ========== Step 11: Credit Market (Optional) ==========
    
    if markets.credit_market is not None:
        # Agents request credit
        borrowers = households + firms  # Simplified
        markets.credit_market.allocate_credit(borrowers, central_bank.policy_rate)
    
    # ========== Step 12: Aggregate Metrics ==========
    
    metrics = calculate_metrics(
        households=households,
        firms=firms,
        government=government,
        central_bank=central_bank,
        markets=markets
    )
    
    return metrics
```

### Phase 5: Output Generation

**Purpose:** Export simulation results in usable formats

#### 5.1 Time Series Export (CSV)

```python
def export_csv(storage: DataStorage, config: Configuration):
    """Export time series data to CSV files"""
    
    output_dir = config.output_directory
    
    # Aggregate metrics
    df_aggregate = pd.DataFrame({
        'time': storage.time,
        'gdp': storage.gdp,
        'unemployment_rate': storage.unemployment,
        'inflation_rate': storage.inflation,
        'policy_rate': storage.policy_rate,
        'gini_coefficient': storage.gini,
        'government_debt': storage.government_debt,
        # ... other metrics
    })
    
    df_aggregate.to_csv(
        os.path.join(output_dir, 'aggregate_metrics.csv'),
        index=False
    )
    
    log.info(f"Exported aggregate metrics to {output_dir}/aggregate_metrics.csv")
    
    # Agent-level data (if stored)
    if config.store_agent_level_data:
        # Household data
        # (Can export as wide format or long format)
        # Long format example:
        household_records = []
        for t in range(len(storage.time)):
            for h in range(storage.household_income.shape[1]):
                household_records.append({
                    'time': t,
                    'household_id': h,
                    'income': storage.household_income[t, h],
                    'wealth': storage.household_wealth[t, h]
                })
        
        df_households = pd.DataFrame(household_records)
        df_households.to_csv(
            os.path.join(output_dir, 'household_data.csv'),
            index=False
        )
```

#### 5.2 JSON Export

```python
def export_json(storage: DataStorage, agents: Agents, config: Configuration):
    """Export results as JSON for flexibility"""
    
    output_dir = config.output_directory
    
    results = {
        'metadata': {
            'time_steps': config.time_steps,
            'household_count': config.household_count,
            'firm_count': config.firm_count,
            'random_seed': config.random_seed,
            'timestamp': datetime.now().isoformat()
        },
        'configuration': config.to_dict(),
        'time_series': {
            'time': storage.time.tolist(),
            'gdp': storage.gdp.tolist(),
            'unemployment': storage.unemployment.tolist(),
            'inflation': storage.inflation.tolist(),
            # ... other series
        },
        'final_state': {
            'households': [h.to_dict() for h in agents.households],
            'firms': [f.to_dict() for f in agents.firms],
            'government': agents.government.to_dict(),
            'central_bank': agents.central_bank.to_dict()
        },
        'summary_statistics': calculate_summary_statistics(storage)
    }
    
    with open(os.path.join(output_dir, 'results.json'), 'w') as f:
        json.dump(results, f, indent=2)
    
    log.info(f"Exported JSON results to {output_dir}/results.json")
```

#### 5.3 Visualization Preparation

```python
def generate_visualizations(storage: DataStorage, config: Configuration):
    """Create standard charts"""
    
    output_dir = config.output_directory
    
    # GDP time series
    plt.figure(figsize=(10, 6))
    plt.plot(storage.time, storage.gdp)
    plt.xlabel('Time Step')
    plt.ylabel('GDP')
    plt.title('GDP Over Time')
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'gdp_timeseries.png'))
    plt.close()
    
    # Unemployment rate
    plt.figure(figsize=(10, 6))
    plt.plot(storage.time, storage.unemployment * 100)
    plt.xlabel('Time Step')
    plt.ylabel('Unemployment Rate (%)')
    plt.title('Unemployment Rate Over Time')
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'unemployment_timeseries.png'))
    plt.close()
    
    # Inflation rate
    plt.figure(figsize=(10, 6))
    plt.plot(storage.time, storage.inflation * 100)
    plt.axhline(y=config.inflation_target * 100, color='r', linestyle='--', label='Target')
    plt.xlabel('Time Step')
    plt.ylabel('Inflation Rate (%)')
    plt.title('Inflation Rate Over Time')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(output_dir, 'inflation_timeseries.png'))
    plt.close()
    
    # Multiple series dashboard
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    axes[0, 0].plot(storage.time, storage.gdp)
    axes[0, 0].set_title('GDP')
    axes[0, 0].grid(True)
    
    axes[0, 1].plot(storage.time, storage.unemployment * 100)
    axes[0, 1].set_title('Unemployment Rate (%)')
    axes[0, 1].grid(True)
    
    axes[1, 0].plot(storage.time, storage.inflation * 100)
    axes[1, 0].set_title('Inflation Rate (%)')
    axes[1, 0].grid(True)
    
    axes[1, 1].plot(storage.time, storage.gini)
    axes[1, 1].set_title('Gini Coefficient')
    axes[1, 1].grid(True)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'dashboard.png'))
    plt.close()
    
    log.info(f"Generated visualizations in {output_dir}")
```

### Phase 6: Cleanup and Exit

```python
def cleanup_and_exit(storage: DataStorage, config: Configuration):
    """Final cleanup and exit"""
    
    # Log summary statistics
    log.info("=== Simulation Summary ===")
    log.info(f"Total time steps: {len(storage.time)}")
    log.info(f"Final GDP: {storage.gdp[-1]:.2f}")
    log.info(f"Final unemployment: {storage.unemployment[-1]*100:.2f}%")
    log.info(f"Final inflation: {storage.inflation[-1]*100:.2f}%")
    log.info(f"Average GDP: {np.mean(storage.gdp):.2f}")
    log.info(f"GDP growth (total): {(storage.gdp[-1]/storage.gdp[0] - 1)*100:.2f}%")
    
    # Close any open files
    # (handled by context managers in Python)
    
    # Clear large data structures if needed
    # (handled by garbage collector in Python)
    
    log.info("Simulation completed successfully. Exiting.")
```

## 4. Shock Application Mechanism

**Purpose:** Modify parameters or inject events at specified time steps

```python
def apply_shocks(t: int, shocks: List[Shock], agents: Agents):
    """Apply any scheduled shocks for current time step"""
    
    for shock in shocks:
        if shock.time == t:
            log.info(f"Applying shock at time {t}: {shock}")
            
            if shock.type == "demand":
                # Modify consumption propensity
                for household in agents.households:
                    if shock.parameter == "consumption_propensity":
                        household.consumption_propensity += shock.change
                        # Ensure valid range
                        household.consumption_propensity = np.clip(
                            household.consumption_propensity, 0.0, 1.0
                        )
            
            elif shock.type == "productivity":
                # Modify TFP
                for firm in agents.firms:
                    if shock.parameter == "TFP":
                        firm.productivity *= (1 + shock.change)
            
            elif shock.type == "policy":
                # Modify government policy
                if shock.parameter == "income_tax_rate":
                    agents.government.income_tax_rate += shock.change
                    agents.government.income_tax_rate = np.clip(
                        agents.government.income_tax_rate, 0.0, 1.0
                    )
                elif shock.parameter == "per_capita_transfer":
                    agents.government.per_capita_transfer += shock.change
            
            elif shock.type == "monetary":
                # Modify central bank parameters
                if shock.parameter == "inflation_target":
                    agents.central_bank.inflation_target += shock.change
            
            else:
                log.warning(f"Unknown shock type: {shock.type}")
```

## 5. Metrics Calculation

```python
def calculate_metrics(
    households: List[Household],
    firms: List[Firm],
    government: Government,
    central_bank: CentralBank,
    markets: Markets
) -> Metrics:
    """Calculate all aggregate metrics for current time step"""
    
    metrics = Metrics()
    
    # GDP (sum of firm output)
    metrics.gdp = sum(firm.output for firm in firms)
    
    # Employment
    total_labor_supply = sum(h.labor_supply for h in households)
    total_employment = sum(h.labor_supply for h in households if h.employed)
    
    if total_labor_supply > 0:
        metrics.unemployment_rate = (
            (total_labor_supply - total_employment) / total_labor_supply
        )
    else:
        metrics.unemployment_rate = 0
    
    metrics.total_employment = total_employment
    
    # Inflation (from central bank)
    metrics.inflation_rate = central_bank.inflation_rate
    
    # Policy rate
    metrics.policy_rate = central_bank.policy_rate
    
    # Wages
    employed_households = [h for h in households if h.employed]
    if employed_households:
        metrics.average_wage = np.mean([h.wage_rate for h in employed_households])
    else:
        metrics.average_wage = 0
    
    # Income distribution (Gini coefficient)
    incomes = [h.income for h in households]
    metrics.gini_coefficient = calculate_gini(incomes)
    
    # Wealth distribution
    wealth_values = [h.wealth for h in households]
    metrics.total_wealth = sum(wealth_values)
    metrics.median_wealth = np.median(wealth_values)
    
    # Fiscal
    metrics.government_revenue = government.tax_revenue
    metrics.government_spending = government.total_expenditure
    metrics.budget_balance = government.budget_balance
    metrics.public_debt = government.public_debt
    
    if metrics.gdp > 0:
        metrics.debt_to_gdp = government.public_debt / metrics.gdp
    else:
        metrics.debt_to_gdp = 0
    
    # Firm metrics
    metrics.total_capital = sum(f.capital_stock for f in firms)
    metrics.total_profits = sum(f.profits for f in firms)
    metrics.average_price = np.mean([f.price for f in firms])
    
    # Credit metrics (if applicable)
    if markets.credit_market is not None:
        metrics.total_credit = markets.credit_market.credit_allocated
        metrics.total_debt = markets.credit_market.total_debt_outstanding
        metrics.default_rate = (
            markets.credit_market.defaults / markets.credit_market.total_debt_outstanding
            if markets.credit_market.total_debt_outstanding > 0 else 0
        )
    
    return metrics
```

## 6. Utility Functions

### 6.1 Gini Coefficient Calculation

```python
def calculate_gini(values: List[float]) -> float:
    """Calculate Gini coefficient for a distribution"""
    
    # Remove negative values and convert to array
    values = np.array([max(0, v) for v in values])
    
    if len(values) == 0 or values.sum() == 0:
        return 0.0
    
    # Sort values
    sorted_values = np.sort(values)
    n = len(values)
    
    # Calculate Gini
    # G = (2 * sum(i * x_i)) / (n * sum(x_i)) - (n+1)/n
    cumsum = np.cumsum(sorted_values)
    gini = (2 * np.sum((np.arange(n) + 1) * sorted_values)) / (n * cumsum[-1]) - (n + 1) / n
    
    return gini
```

### 6.2 Potential GDP Calculation

```python
def calculate_potential_gdp(firms: List[Firm]) -> float:
    """Calculate potential GDP assuming full employment"""
    
    # Use each firm's production function at full labor capacity
    potential = 0
    
    for firm in firms:
        # Assume firm can hire desired labor without constraints
        # (This is a simplification; more sophisticated methods exist)
        max_labor = firm.labor_demand * 1.1  # 10% above current demand
        
        potential_output = (
            firm.productivity * 
            (firm.capital_stock ** firm.alpha) * 
            (max_labor ** (1 - firm.alpha))
        )
        
        potential += potential_output
    
    return potential
```

### 6.3 Checkpointing

```python
def save_checkpoint(
    t: int,
    agents: Agents,
    markets: Markets,
    config: Configuration
):
    """Save simulation state to disk"""
    
    checkpoint_dir = config.checkpoint_directory
    checkpoint_path = os.path.join(checkpoint_dir, f'checkpoint_{t:06d}.pkl')
    
    state = {
        'time': t,
        'agents': agents,
        'markets': markets,
        'rng_state': np.random.get_state()  # For reproducibility
    }
    
    with open(checkpoint_path, 'wb') as f:
        pickle.dump(state, f)
    
    log.info(f"Saved checkpoint at time {t} to {checkpoint_path}")

def load_checkpoint(checkpoint_path: str) -> Tuple[int, Agents, Markets]:
    """Load simulation state from disk"""
    
    with open(checkpoint_path, 'rb') as f:
        state = pickle.load(f)
    
    # Restore RNG state
    np.random.set_state(state['rng_state'])
    
    log.info(f"Loaded checkpoint from {checkpoint_path} (time={state['time']})")
    
    return state['time'], state['agents'], state['markets']
```

## 7. Error Handling and Recovery

### 7.1 Common Error Scenarios

**Numerical Issues:**
- Division by zero (e.g., zero production)
- Overflow/underflow in calculations
- NaN or Inf values

**Mitigation:**
```python
def safe_divide(numerator: float, denominator: float, default: float = 0) -> float:
    """Safely divide with default for zero denominator"""
    if denominator == 0 or np.isnan(denominator):
        return default
    result = numerator / denominator
    if np.isnan(result) or np.isinf(result):
        return default
    return result

def validate_state(agents: Agents) -> bool:
    """Check for invalid states"""
    for household in agents.households:
        if np.isnan(household.income) or np.isinf(household.income):
            log.error(f"Invalid income for household {household.id}")
            return False
        if household.wealth < -1e6:  # Allow small negative but catch large
            log.error(f"Unreasonable wealth for household {household.id}: {household.wealth}")
            return False
    
    for firm in agents.firms:
        if firm.capital_stock < 0:
            log.warning(f"Negative capital for firm {firm.id}, setting to zero")
            firm.capital_stock = 0
    
    return True
```

### 7.2 Early Termination Conditions

```python
def check_early_termination(metrics: Metrics, config: Configuration) -> bool:
    """Determine if simulation should terminate early"""
    
    # Check for explosive dynamics
    if metrics.gdp > 1e12:  # Unreasonably large
        log.error("GDP exploded, terminating")
        return True
    
    if metrics.gdp < 0:
        log.error("Negative GDP, terminating")
        return True
    
    # Check for collapse
    if metrics.unemployment_rate > 0.99:
        log.error("Near-complete unemployment, terminating")
        return True
    
    # Check for numerical issues
    if np.isnan(metrics.gdp) or np.isinf(metrics.gdp):
        log.error("NaN or Inf in GDP, terminating")
        return True
    
    return False
```

## 8. Parallelization Opportunities (Future)

While Version 1 uses sequential execution, future versions could parallelize:

**Agent Updates:**
- Household decisions are independent → parallelize
- Firm production calculations independent → parallelize

**Market Clearing:**
- More complex but can use parallel algorithms for matching

**Scenario Exploration:**
- Run multiple configurations in parallel
- Monte Carlo simulations with different random seeds

**Implementation Sketch:**
```python
# Parallel household updates (future)
from multiprocessing import Pool

def update_household(household, world_state):
    household.decide_consumption()
    return household

with Pool(processes=N_CORES) as pool:
    households = pool.starmap(
        update_household,
        [(h, world_state) for h in households]
    )
```

## 9. Command-Line Interface

**Basic Usage:**
```bash
# Run with default configuration
python simulator.py

# Run with custom config
python simulator.py --config my_config.yaml

# Specify output directory
python simulator.py --config my_config.yaml --output ./results

# Resume from checkpoint
python simulator.py --resume checkpoint_001000.pkl

# Run multiple scenarios
python simulator.py --batch scenarios/*.yaml
```

**CLI Implementation:**
```python
def main():
    parser = argparse.ArgumentParser(
        description='World Economic Simulator'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='config/default.yaml',
        help='Path to configuration file'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='./output',
        help='Output directory for results'
    )
    
    parser.add_argument(
        '--resume',
        type=str,
        help='Resume from checkpoint file'
    )
    
    parser.add_argument(
        '--seed',
        type=int,
        help='Random seed (overrides config)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Set up logging
    setup_logging(verbose=args.verbose)
    
    # Load configuration
    config = load_configuration(args.config)
    
    if args.seed:
        config.random_seed = args.seed
    
    config.output_directory = args.output
    
    # Validate
    validation = validate_configuration(config)
    if not validation.valid:
        log.error("Configuration validation failed:")
        for error in validation.errors:
            log.error(f"  - {error}")
        sys.exit(1)
    
    # Run simulation
    if args.resume:
        results = resume_simulation(args.resume, config)
    else:
        results = run_full_simulation(config)
    
    log.info("Done!")
```

## 10. Summary

This execution flow document provides:
- **Complete initialization sequence** from config to ready state
- **Detailed time-step algorithm** with precise ordering
- **Output generation pipeline** for all formats
- **Error handling** and validation throughout
- **Reproducibility mechanisms** via seeding and checkpointing
- **Extensibility points** for future enhancements

The execution flow is deterministic, well-ordered, and designed for both clarity and performance.
