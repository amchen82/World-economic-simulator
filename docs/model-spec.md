# Model Specification

## Level of Realism
- Mid‑level realism with simplified behavioral rules.

## Households
- Income = wages + transfers − taxes
- Consumption rule: c = propensity * disposable_income
- Savings = disposable_income − consumption
- Labor supply: fixed participation rate by demographic bucket

## Firms
- Production function: Cobb‑Douglas
- Labor demand from profit maximization
- Wage setting: sector wage baseline * productivity
- Investment: fraction of profits

## Government
- Taxes: flat rate on wages and profits
- Transfers: basic per‑capita payment
- Budget balance tracked each step

## Central Bank
- Policy rate rule: Taylor‑style around inflation gap
- Inflation target fixed

## Trade (optional)
- Net exports proportional to openness and relative prices

## Banking/Credit (optional)
- Credit constraints based on loan‑to‑income
- Defaults tracked deterministically

## Shocks
- Deterministic scheduled shocks in v1 (configurable)

## Outputs
- Macro indicators listed in requirements
- Daily time‑series outputs
