# Strategy Conflict Resolution

## Overview
Conflicts are inevitable when evaluating multiple strategies in parallel. The conflict resolver identifies and mitigates:
- Direction Conflicts (LONG vs SHORT)
- Family Conflicts (e.g., BREAKOUT vs RANGE)
- Regime/Alignment Conflicts
- Cost Realism Conflicts

## Resolution
Conflicts do not issue broker cancellations or orders; they produce metadata suggesting which strategy holds stronger regime compatibility to inform the adaptive ensemble.

## CLI Example
```bash
python -m usa_signal_bot strategy-conflicts --write
```
