# Entity Model Document: World Economic Simulator

## 1. Overview

This document provides a detailed specification of all entities (agents) in the World Economic Simulator, their attributes, behaviors, relationships, and lifecycle management.

## 2. Entity Hierarchy

```
Entity (Abstract Base)
├── EconomicAgent (Abstract)
│   ├── Household
│   ├── Firm
│   ├── Government
│   └── CentralBank
└── Market (Abstract)
    ├── LaborMarket
    ├── GoodsMarket
    └── CreditMarket (Optional)
```

## 3. Base Entity Specification

### 3.1 Entity (Abstract Base Class)

**Purpose:** Provides common interface for all simulation entities

**Attributes:**
- `id: string` - Unique identifier
- `created_at: int` - Simulation time when entity was created
- `active: boolean` - Whether entity is currently active

**Methods:**
- `initialize(config: dict) -> void` - Set up initial state
- `update(world_state: WorldState) -> void` - Process one time step
- `get_state() -> dict` - Return current state as dictionary
- `set_state(state: dict) -> void` - Restore state from dictionary
- `validate() -> ValidationResult` - Check internal consistency

### 3.2 EconomicAgent (Abstract Base Class)

**Purpose:** Common functionality for all economic decision-makers

**Extends:** Entity

**Additional Attributes:**
- `wealth: float` - Net worth/assets
- `income: float` - Current period income
- `expenses: float` - Current period expenses

**Additional Methods:**
- `calculate_budget() -> float` - Compute budget constraint
- `make_decision(context: DecisionContext) -> Decision` - Core decision logic
- `record_history() -> void` - Store historical data

## 4. Household Entity

### 4.1 Overview
Represents a consumer-worker unit that supplies labor, consumes goods, saves, and pays taxes.

### 4.2 Attributes

#### Identity Attributes
- `id: string` - Unique household identifier (e.g., "HH_0001")
- `household_size: int` - Number of members (default: 1 for simplicity)
- `age_group: string` - Demographic category (optional)

#### State Variables (Current Period)
- `income: float` - Total income in current period
  - Calculated as: wages + transfers + capital_income
- `wage_income: float` - Labor income earned
- `transfer_income: float` - Government transfers received
- `capital_income: float` - Income from savings/investments
- `disposable_income: float` - After-tax income
  - Calculated as: income - taxes_paid
- `consumption: float` - Consumption expenditure
- `savings: float` - Amount saved in current period
  - Calculated as: disposable_income - consumption
- `wealth: float` - Accumulated savings (stock variable)
- `taxes_paid: float` - Total taxes paid in current period

#### Labor Attributes
- `labor_supply: float` - Hours/units of labor supplied
- `employed: boolean` - Employment status
- `wage_rate: float` - Wage per unit of labor
- `skill_level: float` - Productivity multiplier (0.5 to 2.0)
- `participation_rate: float` - Labor force participation (0 to 1)

#### Behavioral Parameters
- `consumption_propensity: float` - Marginal propensity to consume (0.6 to 0.9)
  - Default: 0.8
- `risk_aversion: float` - Risk preference parameter (optional)
- `time_preference: float` - Discount rate for future consumption (optional)

#### Historical Data
- `income_history: List[float]` - Time series of income
- `consumption_history: List[float]` - Time series of consumption
- `wealth_history: List[float]` - Time series of wealth

### 4.3 Behaviors

#### 4.3.1 Labor Supply Decision
```python
def supply_labor(self):
    """Determine labor supply based on participation rate"""
    if random() < self.participation_rate:
        self.labor_supply = self.skill_level * BASE_LABOR_HOURS
        return self.labor_supply
    else:
        self.labor_supply = 0
        return 0
```

#### 4.3.2 Consumption Decision
```python
def decide_consumption(self):
    """Calculate consumption based on disposable income"""
    # Calculate disposable income
    self.disposable_income = self.income - self.taxes_paid
    
    # Apply consumption function
    self.consumption = self.consumption_propensity * self.disposable_income
    
    # Ensure non-negative
    self.consumption = max(0, self.consumption)
    
    return self.consumption
```

#### 4.3.3 Savings Calculation
```python
def calculate_savings(self):
    """Compute savings as residual"""
    self.savings = self.disposable_income - self.consumption
    
    # Update wealth stock
    self.wealth += self.savings
    
    return self.savings
```

#### 4.3.4 Income Calculation
```python
def calculate_income(self):
    """Aggregate all income sources"""
    self.income = (
        self.wage_income + 
        self.transfer_income + 
        self.capital_income
    )
    return self.income
```

### 4.4 Lifecycle

```
Initialization:
1. Assign unique ID
2. Set skill level (from distribution)
3. Set consumption propensity (from distribution)
4. Set participation rate (from config)
5. Initialize wealth (from distribution)
6. Clear income and consumption

Each Time Step:
1. Calculate labor supply
2. Receive wage income (from labor market)
3. Receive transfers (from government)
4. Calculate capital income (from wealth)
5. Calculate total income
6. Pay taxes
7. Calculate disposable income
8. Decide consumption
9. Calculate savings
10. Update wealth
11. Record history
```

### 4.5 Constraints and Validation

- `0 <= consumption_propensity <= 1`
- `0 <= participation_rate <= 1`
- `consumption >= 0` (non-negative consumption)
- `disposable_income >= 0` (if violated, set consumption to max affordable)
- `skill_level > 0` (positive productivity)

## 5. Firm Entity

### 5.1 Overview
Represents a production unit that hires labor, produces goods, invests in capital, and generates profits.

### 5.2 Attributes

#### Identity Attributes
- `id: string` - Unique firm identifier (e.g., "FIRM_0001")
- `sector: string` - Industry classification (e.g., "manufacturing", "services")
- `firm_size: string` - Size category (small, medium, large)

#### Production Attributes
- `capital_stock: float` - Current capital (K)
- `labor_employed: float` - Current labor (L)
- `output: float` - Production in current period (Y)
- `productivity: float` - Total Factor Productivity (TFP/A)
- `alpha: float` - Capital elasticity in production function (0.2 to 0.4)
  - Default: 0.3
- `depreciation_rate: float` - Capital depreciation per period (0.05 to 0.1)
  - Default: 0.05

#### Financial Attributes
- `revenue: float` - Sales revenue
- `costs: float` - Total costs (wages + capital costs)
- `wage_bill: float` - Total wages paid
- `profits: float` - Earnings
  - Calculated as: revenue - costs
- `investment: float` - Capital expenditure
- `price: float` - Output price

#### Labor Attributes
- `labor_demand: float` - Desired labor input
- `wage_rate: float` - Wage paid per unit labor
- `sector_wage_baseline: float` - Base wage for sector

#### Behavioral Parameters
- `investment_propensity: float` - Share of profits invested (0.1 to 0.3)
  - Default: 0.2
- `markup: float` - Price markup over costs (1.1 to 1.5)
  - Default: 1.2
- `wage_adjustment_speed: float` - Rate of wage changes

#### Historical Data
- `output_history: List[float]`
- `profit_history: List[float]`
- `employment_history: List[float]`

### 5.3 Behaviors

#### 5.3.1 Production Function (Cobb-Douglas)
```python
def produce(self):
    """Calculate output using production function"""
    # Y = A * K^alpha * L^(1-alpha)
    self.output = (
        self.productivity * 
        (self.capital_stock ** self.alpha) * 
        (self.labor_employed ** (1 - self.alpha))
    )
    return self.output
```

#### 5.3.2 Labor Demand Calculation
```python
def calculate_labor_demand(self, wage_rate: float):
    """Determine optimal labor demand via profit maximization"""
    # Marginal product of labor = wage
    # MPL = (1-alpha) * A * K^alpha * L^(-alpha)
    # Solving for L:
    
    if wage_rate <= 0:
        return 0
    
    base_term = (1 - self.alpha) * self.productivity * self.price
    exponent = 1.0 / self.alpha
    
    self.labor_demand = (
        (base_term / wage_rate) ** exponent * 
        self.capital_stock
    )
    
    return self.labor_demand
```

#### 5.3.3 Wage Setting
```python
def set_wage(self, market_conditions: dict):
    """Determine wage offer"""
    # Base wage adjusted for productivity and market tightness
    
    productivity_factor = self.productivity / BASELINE_PRODUCTIVITY
    market_tightness = market_conditions['tightness']  # >1 means tight
    
    self.wage_rate = (
        self.sector_wage_baseline * 
        productivity_factor * 
        (1 + self.wage_adjustment_speed * (market_tightness - 1))
    )
    
    # Apply floor
    self.wage_rate = max(self.wage_rate, MINIMUM_WAGE)
    
    return self.wage_rate
```

#### 5.3.4 Investment Decision
```python
def decide_investment(self):
    """Determine capital investment"""
    # Invest a fraction of profits
    if self.profits > 0:
        self.investment = self.investment_propensity * self.profits
    else:
        self.investment = 0  # No investment if unprofitable
    
    return self.investment
```

#### 5.3.5 Capital Accumulation
```python
def update_capital(self):
    """Update capital stock with investment and depreciation"""
    depreciation = self.depreciation_rate * self.capital_stock
    
    self.capital_stock += self.investment - depreciation
    
    # Ensure non-negative
    self.capital_stock = max(0, self.capital_stock)
    
    return self.capital_stock
```

#### 5.3.6 Price Setting
```python
def set_price(self):
    """Set output price with markup over unit cost"""
    if self.output > 0:
        unit_cost = self.costs / self.output
        self.price = self.markup * unit_cost
    else:
        self.price = self.price  # Keep previous price
    
    # Apply floor
    self.price = max(self.price, MIN_PRICE)
    
    return self.price
```

#### 5.3.7 Profit Calculation
```python
def calculate_profits(self):
    """Compute profits"""
    self.revenue = self.output * self.price
    self.wage_bill = self.labor_employed * self.wage_rate
    self.costs = self.wage_bill  # Simplified: only labor costs
    
    self.profits = self.revenue - self.costs
    
    return self.profits
```

### 5.4 Lifecycle

```
Initialization:
1. Assign unique ID and sector
2. Set production parameters (alpha, TFP)
3. Initialize capital stock (from distribution)
4. Set behavioral parameters
5. Set initial price

Each Time Step:
1. Set wage rate based on market conditions
2. Calculate labor demand
3. Receive labor allocation (from labor market)
4. Produce output using production function
5. Set output price
6. Calculate revenue and costs
7. Calculate profits
8. Decide investment
9. Update capital stock (investment - depreciation)
10. Record history
```

### 5.5 Constraints and Validation

- `capital_stock >= 0` (non-negative capital)
- `labor_employed >= 0` (non-negative labor)
- `0 < alpha < 1` (valid production parameter)
- `productivity > 0` (positive TFP)
- `0 < depreciation_rate < 1` (valid depreciation)
- `price > 0` (positive price)
- `wage_rate >= MINIMUM_WAGE` (wage floor)

## 6. Government Entity

### 6.1 Overview
Represents the fiscal authority that collects taxes, provides transfers, and manages public finances.

### 6.2 Attributes

#### Revenue Attributes
- `tax_revenue: float` - Total taxes collected
- `income_tax_collected: float` - Taxes from household income
- `profit_tax_collected: float` - Taxes from firm profits
- `other_revenue: float` - Other government revenue (optional)

#### Expenditure Attributes
- `transfer_payments: float` - Total transfers to households
- `per_capita_transfer: float` - Transfer amount per household
- `government_spending: float` - Government consumption (optional)
- `total_expenditure: float` - Sum of all spending

#### Fiscal Position
- `budget_balance: float` - Revenue - Expenditure
  - Positive: surplus, Negative: deficit
- `public_debt: float` - Accumulated debt (stock)
- `debt_to_gdp: float` - Debt as percentage of GDP

#### Policy Parameters
- `income_tax_rate: float` - Tax rate on household income (0.1 to 0.4)
  - Default: 0.2
- `profit_tax_rate: float` - Tax rate on firm profits (0.15 to 0.35)
  - Default: 0.25
- `transfer_rule: string` - How transfers are calculated
  - Options: "per_capita", "means_tested", "unemployment_benefit"

#### Historical Data
- `revenue_history: List[float]`
- `expenditure_history: List[float]`
- `debt_history: List[float]`

### 6.3 Behaviors

#### 6.3.1 Tax Collection
```python
def collect_taxes(self, households: List[Household], firms: List[Firm]):
    """Collect taxes from all agents"""
    
    # Income tax from households
    self.income_tax_collected = 0
    for household in households:
        tax = self.income_tax_rate * household.income
        household.taxes_paid = tax
        self.income_tax_collected += tax
    
    # Profit tax from firms
    self.profit_tax_collected = 0
    for firm in firms:
        if firm.profits > 0:
            tax = self.profit_tax_rate * firm.profits
            self.profit_tax_collected += tax
            # Firm pays tax (reduces net profits)
    
    # Total revenue
    self.tax_revenue = (
        self.income_tax_collected + 
        self.profit_tax_collected + 
        self.other_revenue
    )
    
    return self.tax_revenue
```

#### 6.3.2 Transfer Distribution
```python
def distribute_transfers(self, households: List[Household]):
    """Distribute transfers to households"""
    
    if self.transfer_rule == "per_capita":
        # Equal amount to all households
        for household in households:
            transfer = self.per_capita_transfer
            household.transfer_income = transfer
        
        self.transfer_payments = (
            self.per_capita_transfer * len(households)
        )
    
    elif self.transfer_rule == "means_tested":
        # Higher transfers to lower-income households
        # Implementation depends on specific rule
        pass
    
    elif self.transfer_rule == "unemployment_benefit":
        # Transfers only to unemployed
        for household in households:
            if not household.employed:
                household.transfer_income = UNEMPLOYMENT_BENEFIT
            else:
                household.transfer_income = 0
        
        unemployed_count = sum(1 for h in households if not h.employed)
        self.transfer_payments = UNEMPLOYMENT_BENEFIT * unemployed_count
    
    return self.transfer_payments
```

#### 6.3.3 Budget Calculation
```python
def calculate_budget_balance(self):
    """Compute budget surplus/deficit"""
    
    self.total_expenditure = (
        self.transfer_payments + 
        self.government_spending
    )
    
    self.budget_balance = self.tax_revenue - self.total_expenditure
    
    return self.budget_balance
```

#### 6.3.4 Debt Accumulation
```python
def update_debt(self):
    """Update public debt based on deficit"""
    
    # Deficit increases debt, surplus decreases it
    self.public_debt += (-self.budget_balance)
    
    # Debt cannot be negative (no sovereign wealth fund in v1)
    self.public_debt = max(0, self.public_debt)
    
    return self.public_debt
```

#### 6.3.5 Fiscal Indicators
```python
def calculate_fiscal_indicators(self, gdp: float):
    """Calculate fiscal ratios"""
    
    if gdp > 0:
        self.debt_to_gdp = self.public_debt / gdp
        self.revenue_to_gdp = self.tax_revenue / gdp
        self.spending_to_gdp = self.total_expenditure / gdp
    else:
        self.debt_to_gdp = 0
        self.revenue_to_gdp = 0
        self.spending_to_gdp = 0
    
    return {
        'debt_to_gdp': self.debt_to_gdp,
        'revenue_to_gdp': self.revenue_to_gdp,
        'spending_to_gdp': self.spending_to_gdp
    }
```

### 6.4 Lifecycle

```
Initialization:
1. Set tax rates from configuration
2. Set transfer rules and amounts
3. Initialize debt level
4. Clear revenue and expenditure

Each Time Step:
1. Collect taxes from households and firms
2. Distribute transfers to households
3. Calculate total expenditure
4. Calculate budget balance
5. Update public debt
6. Calculate fiscal indicators
7. Record history
```

### 6.5 Constraints and Validation

- `0 <= income_tax_rate < 1` (valid tax rate)
- `0 <= profit_tax_rate < 1` (valid tax rate)
- `per_capita_transfer >= 0` (non-negative transfers)
- `public_debt >= 0` (no negative debt in v1)

## 7. Central Bank Entity

### 7.1 Overview
Represents the monetary authority that sets policy interest rates and targets inflation.

### 7.2 Attributes

#### Monetary Variables
- `policy_rate: float` - Nominal policy interest rate (e.g., 0.02 = 2%)
- `real_rate: float` - Policy rate adjusted for inflation
- `inflation_rate: float` - Current inflation rate
- `inflation_target: float` - Target inflation rate (e.g., 0.02 = 2%)
  - Default: 0.02

#### Price Level Tracking
- `price_level: float` - Aggregate price index
- `price_level_prev: float` - Previous period price level

#### Policy Parameters
- `taylor_inflation_coefficient: float` - Response to inflation gap (>1)
  - Default: 1.5
- `taylor_output_coefficient: float` - Response to output gap (>0)
  - Default: 0.5
- `neutral_rate: float` - Long-run equilibrium rate (r*)
  - Default: 0.02
- `rate_floor: float` - Lower bound on policy rate (e.g., 0 or -0.005)
  - Default: 0.0
- `rate_ceiling: float` - Upper bound on policy rate
  - Default: 0.20

#### Historical Data
- `policy_rate_history: List[float]`
- `inflation_history: List[float]`

### 7.3 Behaviors

#### 7.3.1 Inflation Calculation
```python
def calculate_inflation(self, current_price_level: float):
    """Compute inflation from price level changes"""
    
    if self.price_level_prev > 0:
        self.inflation_rate = (
            (current_price_level - self.price_level_prev) / 
            self.price_level_prev
        )
    else:
        self.inflation_rate = 0
    
    # Update price level history
    self.price_level_prev = self.price_level
    self.price_level = current_price_level
    
    return self.inflation_rate
```

#### 7.3.2 Policy Rate Setting (Taylor Rule)
```python
def set_policy_rate(self, output_gap: float):
    """Set policy rate using Taylor-type rule"""
    
    # Inflation gap
    inflation_gap = self.inflation_rate - self.inflation_target
    
    # Taylor rule: r = r* + phi_pi*(pi - pi*) + phi_y*y_gap
    self.policy_rate = (
        self.neutral_rate + 
        self.taylor_inflation_coefficient * inflation_gap + 
        self.taylor_output_coefficient * output_gap
    )
    
    # Apply bounds
    self.policy_rate = max(self.rate_floor, self.policy_rate)
    self.policy_rate = min(self.rate_ceiling, self.policy_rate)
    
    return self.policy_rate
```

#### 7.3.3 Real Rate Calculation
```python
def calculate_real_rate(self):
    """Compute real interest rate (Fisher equation)"""
    
    # r_real ≈ r_nominal - inflation
    self.real_rate = self.policy_rate - self.inflation_rate
    
    return self.real_rate
```

### 7.4 Lifecycle

```
Initialization:
1. Set inflation target
2. Set Taylor rule parameters
3. Set initial policy rate
4. Initialize price level tracking

Each Time Step:
1. Receive aggregate price level (from goods market)
2. Calculate inflation rate
3. Receive output gap (from metrics aggregator)
4. Set policy rate using Taylor rule
5. Calculate real rate
6. Transmit policy rate to credit market (if applicable)
7. Record history
```

### 7.5 Constraints and Validation

- `0 <= inflation_target <= 0.10` (reasonable target)
- `taylor_inflation_coefficient > 1` (Taylor principle for stability)
- `taylor_output_coefficient >= 0` (non-negative response)
- `rate_floor <= policy_rate <= rate_ceiling` (bounded rate)

## 8. Market Entities

### 8.1 Labor Market

**Purpose:** Match labor supply (households) and demand (firms), determine employment and wages

**Attributes:**
- `total_labor_supply: float` - Aggregate supply
- `total_labor_demand: float` - Aggregate demand
- `market_wage: float` - Equilibrium or average wage
- `total_employment: float` - Jobs filled
- `unemployment_rate: float` - Share unemployed
- `labor_force: float` - Active participants
- `tightness: float` - Demand/supply ratio

**Methods:**
```python
def clear_market(self, households: List[Household], firms: List[Firm]):
    """Match workers and jobs"""
    
    # Aggregate supply and demand
    self.total_labor_supply = sum(h.labor_supply for h in households)
    self.total_labor_demand = sum(f.labor_demand for f in firms)
    
    # Determine employment
    self.total_employment = min(self.total_labor_supply, self.total_labor_demand)
    
    # Calculate unemployment
    if self.total_labor_supply > 0:
        self.unemployment_rate = (
            (self.total_labor_supply - self.total_employment) / 
            self.total_labor_supply
        )
    else:
        self.unemployment_rate = 0
    
    # Calculate tightness
    if self.total_labor_supply > 0:
        self.tightness = self.total_labor_demand / self.total_labor_supply
    else:
        self.tightness = 1
    
    # Allocate employment (simplified: pro-rata)
    if self.total_labor_demand > 0:
        employment_ratio = self.total_employment / self.total_labor_demand
        for firm in firms:
            firm.labor_employed = firm.labor_demand * employment_ratio
    
    # Set employment status for households (simplified)
    employed_count = 0
    for household in households:
        if household.labor_supply > 0:
            if employed_count < self.total_employment:
                household.employed = True
                household.wage_income = household.wage_rate * household.labor_supply
                employed_count += household.labor_supply
            else:
                household.employed = False
                household.wage_income = 0
    
    return self.total_employment
```

### 8.2 Goods Market

**Purpose:** Match production (supply) and consumption (demand), determine prices

**Attributes:**
- `total_supply: float` - Aggregate production
- `total_demand: float` - Consumption + investment + government
- `aggregate_price: float` - Average price level
- `excess_demand: float` - Demand - supply
- `price_adjustment_speed: float` - How fast prices change

**Methods:**
```python
def clear_market(self, firms: List[Firm], total_demand: float):
    """Match supply and demand, adjust prices"""
    
    # Aggregate supply
    self.total_supply = sum(f.output for f in firms)
    self.total_demand = total_demand
    
    # Calculate excess demand
    self.excess_demand = self.total_demand - self.total_supply
    
    # Adjust prices based on excess demand
    if self.total_supply > 0:
        excess_ratio = self.excess_demand / self.total_supply
        
        price_change_rate = self.price_adjustment_speed * excess_ratio
        
        for firm in firms:
            firm.price *= (1 + price_change_rate)
            firm.price = max(MIN_PRICE, firm.price)  # Floor
    
    # Calculate aggregate price level
    if len(firms) > 0:
        self.aggregate_price = sum(f.price for f in firms) / len(firms)
    
    return self.aggregate_price
```

### 8.3 Credit Market (Optional)

**Purpose:** Allocate credit to borrowers, enforce constraints, track debt

**Attributes:**
- `total_credit_demand: float`
- `total_credit_supply: float`
- `credit_allocated: float`
- `policy_rate: float` - From central bank
- `lending_spread: float` - Risk premium
- `loan_to_income_limit: float` - Constraint ratio
- `total_debt_outstanding: float`
- `default_threshold: float`
- `defaults: float`

**Methods:**
```python
def allocate_credit(self, borrowers: List, policy_rate: float):
    """Extend credit subject to constraints"""
    
    self.policy_rate = policy_rate
    lending_rate = policy_rate + self.lending_spread
    
    # Calculate credit demand
    self.total_credit_demand = sum(b.credit_requested for b in borrowers)
    
    # Apply loan-to-income constraints
    constrained_demand = 0
    for borrower in borrowers:
        max_affordable = borrower.income * self.loan_to_income_limit
        borrower.credit_eligible = min(borrower.credit_requested, max_affordable)
        constrained_demand += borrower.credit_eligible
    
    # Determine credit supply (simplified: unlimited at the rate)
    self.total_credit_supply = constrained_demand
    
    # Allocate credit
    for borrower in borrowers:
        borrower.credit_received = borrower.credit_eligible
        borrower.debt_outstanding += borrower.credit_received
    
    self.credit_allocated = constrained_demand
    
    # Process defaults
    for borrower in borrowers:
        if borrower.debt_outstanding > borrower.income * self.default_threshold:
            self.defaults += borrower.debt_outstanding
            borrower.debt_outstanding = 0  # Default clears debt
    
    return self.credit_allocated
```

## 9. Entity Relationships

### 9.1 Relationship Diagram

```
┌─────────────┐      labor supply      ┌─────────────┐
│  Household  │────────────────────────>│Labor Market │
│             │<───────wages────────────│             │
└─────────────┘                         └─────────────┘
       │                                       ^
       │ consumption                           │ labor demand
       │ demand                                │
       v                                       │
┌─────────────┐      goods supply      ┌─────────────┐
│   Goods     │<───────────────────────│    Firm     │
│   Market    │─────goods/prices───────>│             │
└─────────────┘                         └─────────────┘
       ^                                       │
       │                                       │ profit taxes
       │ transfers                             │
       │ (from taxes)                          v
┌─────────────┐      tax revenue       ┌─────────────┐
│  Household  │────────────────────────>│ Government  │
│             │<───────transfers────────│             │
└─────────────┘                         └─────────────┘
                                               │
                                               │ fiscal data
                                               v
┌─────────────┐      inflation         ┌─────────────┐
│ Central     │<───────price level─────│ Goods Market│
│ Bank        │─────policy rate────────>│(& Credit)   │
└─────────────┘                         └─────────────┘
```

### 9.2 Relationship Matrix

| From/To | Household | Firm | Government | Central Bank | Labor Market | Goods Market | Credit Market |
|---------|-----------|------|------------|--------------|--------------|--------------|---------------|
| **Household** | - | Consumption demand | Tax payments | - | Labor supply | Demand | Credit demand |
| **Firm** | Wage payments | - | Profit taxes | - | Labor demand | Supply | Credit demand |
| **Government** | Transfers | - | - | Fiscal data | - | - | - |
| **Central Bank** | - | - | - | - | - | Price target | Policy rate |
| **Labor Market** | Employment, wages | Employment, wage bill | - | - | - | - | - |
| **Goods Market** | Goods, prices | Revenue | - | Price level | - | - | - |
| **Credit Market** | Loans, debt | Loans, debt | - | Interest rates | - | - | - |

### 9.3 Dependency Graph

**Temporal Ordering within Time Step:**

1. **Firms** → Set wages, calculate labor demand
2. **Labor Market** → Clear (employment, wages)
3. **Firms** → Produce output
4. **Government** → Collect taxes, distribute transfers
5. **Households** → Calculate income, decide consumption
6. **Goods Market** → Clear (prices)
7. **Firms** → Calculate profits, decide investment
8. **Central Bank** → Update policy rate
9. **Credit Market** → Allocate credit (optional)
10. **All Agents** → Update state variables

This ordering ensures:
- Wages known before household decisions
- Production before consumption
- Prices determined by supply-demand
- Profits computed before investment

## 10. Entity State Transitions

### 10.1 Household State Machine

```
[Initialized] 
    ↓ (start simulation)
[Supplying Labor] 
    ↓ (market clears)
[Employed/Unemployed] 
    ↓ (receive income)
[Calculating Income] 
    ↓ (pay taxes, receive transfers)
[Deciding Consumption] 
    ↓ (purchase goods)
[Saving/Updating Wealth] 
    ↓ (next time step)
[Supplying Labor] ...
```

### 10.2 Firm State Machine

```
[Initialized] 
    ↓ (start simulation)
[Setting Wage, Calculating Labor Demand] 
    ↓ (labor market clears)
[Producing Output] 
    ↓ (use production function)
[Setting Price] 
    ↓ (goods market clears)
[Calculating Profits] 
    ↓ (decide investment)
[Investing in Capital] 
    ↓ (update capital stock)
[Depreciating Capital] 
    ↓ (next time step)
[Setting Wage...] ...
```

## 11. Aggregate World State

**Purpose:** Container for all entity states at a given time step

**Structure:**
```python
class WorldState:
    time: int
    households: List[Household]
    firms: List[Firm]
    government: Government
    central_bank: CentralBank
    labor_market: LaborMarket
    goods_market: GoodsMarket
    credit_market: CreditMarket (optional)
    
    # Aggregate metrics
    gdp: float
    unemployment_rate: float
    inflation_rate: float
    average_wage: float
    total_wealth: float
    gini_coefficient: float
    
    # Configuration
    config: Configuration
    
    # Methods
    def snapshot() -> dict
    def restore(snapshot: dict) -> void
```

## 12. Entity Persistence

### 12.1 Serialization Format (JSON)

```json
{
  "household": {
    "id": "HH_0001",
    "income": 45000.0,
    "consumption": 36000.0,
    "wealth": 12000.0,
    "employed": true,
    "consumption_propensity": 0.8,
    "skill_level": 1.2
  },
  "firm": {
    "id": "FIRM_0001",
    "sector": "manufacturing",
    "capital_stock": 500000.0,
    "labor_employed": 50.0,
    "output": 75000.0,
    "profits": 15000.0,
    "alpha": 0.3,
    "productivity": 1.0
  }
}
```

### 12.2 State Checkpointing

- Save every N time steps (configurable)
- Include all agent states, markets, and random generator state
- Enable simulation restart from checkpoint

## 13. Conclusion

This entity model provides:
- **Clear specifications** for each agent type
- **Well-defined behaviors** and decision rules
- **Explicit relationships** between entities
- **Lifecycle management** for initialization and updates
- **Validation constraints** for consistency
- **Temporal ordering** for deterministic execution

The model balances economic realism with computational tractability, enabling meaningful simulations while maintaining simplicity and extensibility.
