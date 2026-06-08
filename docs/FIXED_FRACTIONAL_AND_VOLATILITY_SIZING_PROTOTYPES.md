# Fixed Fractional and Volatility Sizing Prototypes

## Fixed Fractional Prototype
A constant exposure assigned to each eligible candidate based on the `base_prototype_fraction`.

## Volatility Adjusted Prototype
Modulates the baseline fraction via an inversely proportional (or inverse variance) relationship to the candidate's volatility proxy. A high volatility proxy increases the penalty applied.

**Important**: These values are raw fractions in `[0,1]` and do not translate into real capital amounts or broker executions.
