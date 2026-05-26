from typing import List, Dict, Any, Optional
from usa_signal_bot.core.exceptions import CrossSectionalUniverseError
from usa_signal_bot.core.enums import CrossSectionalUniverseStatus, AdvancedFeatureRiskFlag
from usa_signal_bot.feature_engine.advanced_features.phase118_models import CrossSectionalUniverse, create_cross_sectional_universe_id
import datetime

def _now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def build_cross_sectional_universe(symbols: Optional[List[str]] = None, benchmark_symbol: Optional[str] = "SPY") -> CrossSectionalUniverse:
    """Builds a cross-sectional universe definition."""
    if symbols is None:
        symbols = ["AAPL", "MSFT", "SPY"]

    status = CrossSectionalUniverseStatus.CREATED
    warnings = []
    errors = []
    risk_flags = []

    # Validation
    if len(symbols) < 2:
        status = CrossSectionalUniverseStatus.BLOCKED
        errors.append("Universe must contain at least 2 symbols.")
        risk_flags.append(AdvancedFeatureRiskFlag.INSUFFICIENT_SYMBOLS)

    contains_benchmark = False
    if benchmark_symbol:
        contains_benchmark = benchmark_symbol in symbols
        if not contains_benchmark:
            warnings.append(f"Benchmark symbol {benchmark_symbol} is not in the universe.")

    if not errors:
        status = CrossSectionalUniverseStatus.VALIDATED

    return CrossSectionalUniverse(
        universe_id=create_cross_sectional_universe_id(),
        created_at_utc=_now(),
        name="Phase118_Universe",
        symbols=symbols,
        min_required_symbols=2,
        status=status,
        research_data_only=True,
        contains_benchmark_symbol=contains_benchmark,
        benchmark_symbol=benchmark_symbol,
        warnings=warnings,
        errors=errors,
        risk_flags=risk_flags,
        metadata={}
    )

def validate_cross_sectional_universe(universe: CrossSectionalUniverse) -> List[str]:
    errors = []
    if len(universe.symbols) < universe.min_required_symbols:
        errors.append(f"Insufficient symbols. Has {len(universe.symbols)}, requires {universe.min_required_symbols}.")
    if not universe.research_data_only:
        errors.append("research_data_only must be True.")
    if universe.status in [CrossSectionalUniverseStatus.BLOCKED, CrossSectionalUniverseStatus.FAILED]:
        errors.append(f"Universe status is {universe.status.value}.")
    return errors

def universe_has_symbol(universe: CrossSectionalUniverse, symbol: str) -> bool:
    return symbol in universe.symbols

def cross_sectional_universe_summary(universe: CrossSectionalUniverse) -> Dict[str, Any]:
    return {
        "universe_id": universe.universe_id,
        "symbol_count": len(universe.symbols),
        "status": universe.status.value,
        "is_valid": len(validate_cross_sectional_universe(universe)) == 0
    }

def cross_sectional_universe_to_text(universe: CrossSectionalUniverse) -> str:
    return f"Universe {universe.universe_id}: {len(universe.symbols)} symbols [{universe.status.value}]"
