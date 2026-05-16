import os
import re

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"Created {path}")

# --- Config and Schema Updates ---

schema_path = "usa_signal_bot/core/config_schema.py"
try:
    with open(schema_path, "r") as f:
        schema_content = f.read()

    new_schema = """
@dataclass
class PortfolioConstructionConfig:
    enabled: bool = True
    mode: str = "HYBRID"
    write_construction_reports: bool = True
    warn_not_investment_advice: bool = True
    warn_no_broker_execution: bool = True
    warn_sector_cluster_is_proxy: bool = True

@dataclass
class SectorClusterRegistryConfig:
    enabled: bool = True
    registry_file: str = "config/portfolio/sector_cluster_registry.example.json"
    use_manual_registry: bool = True
    use_etf_proxy_heuristic: bool = True
    unknown_sector_bucket: str = "unknown_sector"
    unknown_cluster_bucket: str = "unknown_cluster"
    minimum_coverage_pct_warning: float = 70.0

@dataclass
class PortfolioExposureLimitsConfig:
    enabled: bool = True
    max_gross_exposure_pct_equity: float = 100.0
    max_abs_net_exposure_pct_equity: float = 80.0
    max_long_exposure_pct_equity: float = 100.0
    max_short_exposure_pct_equity: float = 50.0
    reduce_on_warning: bool = True
    block_on_critical: bool = True

@dataclass
class PortfolioConcentrationLimitsConfig:
    enabled: bool = True
    max_symbol_pct_equity: float = 10.0
    max_strategy_pct_equity: float = 25.0
    max_sector_pct_equity: float = 30.0
    max_cluster_pct_equity: float = 20.0
    max_regime_pct_equity: float = 50.0
    max_thin_liquidity_pct_equity: float = 25.0
    max_high_cost_pct_equity: float = 20.0

@dataclass
class PortfolioCorrelationProxyConfig:
    enabled: bool = True
    same_symbol_bucket: str = "VERY_HIGH"
    same_cluster_bucket: str = "HIGH"
    same_sector_bucket: str = "MODERATE"
    reduce_on_high_proxy_correlation: bool = True

@dataclass
class PortfolioBalancingConfig:
    enabled: bool = True
    pro_rata_reduce_on_limit: bool = True
    prefer_higher_score_on_conflict: bool = True
    prefer_lower_risk_on_conflict: bool = True
    suppress_lowest_quality_first: bool = True
    min_final_notional_usd: float = 10.0

@dataclass
class PortfolioConstructionNotificationsConfig:
    enabled: bool = True
    dry_run: bool = True
    notify_portfolio_construction_report: bool = True
    notify_exposure_limit_warning: bool = True
    notify_concentration_risk_warning: bool = True
    default_channel: str = "DRY_RUN"
    warn_no_real_send_default: bool = True
"""
    if "PortfolioConstructionConfig" not in schema_content:
        # insert before the main AppConfig or at end
        schema_content += new_schema
        # modify AppConfig to include these
        if "class AppConfig" in schema_content:
            schema_content = re.sub(
                r'(class AppConfig.*?):(.*?)',
                r'\1:\n    portfolio_construction: PortfolioConstructionConfig = field(default_factory=PortfolioConstructionConfig)\n    sector_cluster_registry: SectorClusterRegistryConfig = field(default_factory=SectorClusterRegistryConfig)\n    portfolio_exposure_limits: PortfolioExposureLimitsConfig = field(default_factory=PortfolioExposureLimitsConfig)\n    portfolio_concentration_limits: PortfolioConcentrationLimitsConfig = field(default_factory=PortfolioConcentrationLimitsConfig)\n    portfolio_correlation_proxy: PortfolioCorrelationProxyConfig = field(default_factory=PortfolioCorrelationProxyConfig)\n    portfolio_balancing: PortfolioBalancingConfig = field(default_factory=PortfolioBalancingConfig)\n    portfolio_construction_notifications: PortfolioConstructionNotificationsConfig = field(default_factory=PortfolioConstructionNotificationsConfig)\2',
                schema_content, flags=re.DOTALL
            )
        with open(schema_path, "w") as f:
            f.write(schema_content)
        print("Updated config_schema.py")
except Exception as e:
    print(f"Failed to update config schema: {e}")

# --- core/exceptions.py ---
exc_path = "usa_signal_bot/core/exceptions.py"
try:
    with open(exc_path, "r") as f:
        exc_content = f.read()

    new_excs = """
class PortfolioConstructionError(Exception): pass
class SectorClusterRegistryError(PortfolioConstructionError): pass
class SectorClusterResolverError(PortfolioConstructionError): pass
class ExposureCalculationError(PortfolioConstructionError): pass
class ExposureLimitError(PortfolioConstructionError): pass
class ConcentrationGuardError(PortfolioConstructionError): pass
class CorrelationProxyError(PortfolioConstructionError): pass
class PortfolioAllocationPlannerError(PortfolioConstructionError): pass
class PortfolioBalancerError(PortfolioConstructionError): pass
class PortfolioConflictResolverError(PortfolioConstructionError): pass
class PortfolioConstructionStorageError(PortfolioConstructionError): pass
class PortfolioConstructionValidationError(PortfolioConstructionError): pass
class PortfolioConstructionReportingError(PortfolioConstructionError): pass
"""
    if "PortfolioConstructionError" not in exc_content:
        exc_content += new_excs
        with open(exc_path, "w") as f:
            f.write(exc_content)
        print("Updated exceptions.py")
except Exception as e:
    print(f"Failed to update exceptions: {e}")

print("Generated step 9")
