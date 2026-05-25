
import datetime
from typing import List, Optional, Dict, Any
from usa_signal_bot.core.enums import MarketEventSource
from usa_signal_bot.event_metadata.phase111_models import MacroSeriesMetadata, create_macro_series_id

def build_default_macro_series_catalog() -> List[MacroSeriesMetadata]:
    defaults = [
        ("CPIAUCSL", "CPI", "monthly", "index", "US"),
        ("UNRATE", "unemployment rate", "monthly", "percent", "US"),
        ("FEDFUNDS", "effective federal funds rate", "monthly", "percent", "US"),
        ("DGS10", "10-year treasury yield", "daily", "percent", "US"),
        ("GDP", "gross domestic product", "quarterly", "index", "US"),
        ("PAYEMS", "nonfarm payrolls", "monthly", "count", "US"),
        ("VIXCLS", "VIX close", "daily", "index", "US"),
    ]
    catalog = []
    for sid, name, freq, units, country in defaults:
        catalog.append(MacroSeriesMetadata(
            series_id=sid,
            created_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            name=name,
            source=MarketEventSource.FRED_COMPATIBLE_METADATA,
            category="Macro",
            frequency=freq,
            units=units,
            country=country,
            provider_hint=None,
            requires_api_key=False,
            paid_api=False,
            network_enabled_now=False,
            scraping_required=False,
            html_parsing_required=False,
            metadata_only=True,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        ))
    return catalog

def macro_series_by_id(series_id: str, catalog: Optional[List[MacroSeriesMetadata]] = None) -> Optional[MacroSeriesMetadata]:
    cat = catalog if catalog is not None else build_default_macro_series_catalog()
    for c in cat:
        if c.series_id == series_id:
            return c
    return None

def validate_macro_metadata_catalog(catalog: List[MacroSeriesMetadata]) -> List[str]:
    errs = []
    for c in catalog:
        if c.network_enabled_now: errs.append(f"{c.series_id} network_enabled_now is True")
        if c.paid_api: errs.append(f"{c.series_id} paid_api is True")
        if c.scraping_required: errs.append(f"{c.series_id} scraping_required is True")
        if c.html_parsing_required: errs.append(f"{c.series_id} html_parsing_required is True")
        if not c.metadata_only: errs.append(f"{c.series_id} metadata_only is False")
    return errs

def macro_metadata_catalog_summary(catalog: List[MacroSeriesMetadata]) -> Dict[str, Any]:
    return {"count": len(catalog), "valid": len(validate_macro_metadata_catalog(catalog)) == 0}

def macro_metadata_catalog_to_text(catalog: List[MacroSeriesMetadata], limit: int = 200) -> str:
    return f"Macro Catalog: {len(catalog)} items"
