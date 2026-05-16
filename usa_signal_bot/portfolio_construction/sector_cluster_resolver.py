from usa_signal_bot.portfolio_construction.portfolio_models import SectorClusterRecord, PortfolioCandidate, create_sector_cluster_record_id
from usa_signal_bot.core.enums import SectorClusterSource

class SectorClusterResolver:
    def __init__(self, records: list[SectorClusterRecord] | None = None, config: dict | None = None):
        self.records = records or []
        self.config = config or {}
        self.unknown_sector_bucket = self.config.get("unknown_sector_bucket", "unknown_sector")
        self.unknown_cluster_bucket = self.config.get("unknown_cluster_bucket", "unknown_cluster")
        self.use_etf_proxy = self.config.get("use_etf_proxy_heuristic", True)

    def resolve(self, symbol: str) -> SectorClusterRecord:
        for r in self.records:
            if r.symbol == symbol:
                return r

        # ETF proxy heuristic
        if self.use_etf_proxy and symbol in ["SPY", "QQQ", "IWM", "DIA", "VOO", "VTI"]:
            return SectorClusterRecord(
                record_id=create_sector_cluster_record_id(symbol),
                symbol=symbol,
                sector="broad_market",
                industry="etf",
                cluster="index_proxy",
                source=SectorClusterSource.ETF_PROXY_HEURISTIC,
                confidence=80.0
            )

        return SectorClusterRecord(
            record_id=create_sector_cluster_record_id(symbol),
            symbol=symbol,
            sector=self.unknown_sector_bucket,
            industry=None,
            cluster=self.unknown_cluster_bucket,
            source=SectorClusterSource.UNKNOWN,
            confidence=0.0
        )

    def resolve_many(self, symbols: list[str]) -> list[SectorClusterRecord]:
        return [self.resolve(s) for s in symbols]

    def sector_for_symbol(self, symbol: str) -> str | None:
        return self.resolve(symbol).sector

    def cluster_for_symbol(self, symbol: str) -> str | None:
        return self.resolve(symbol).cluster

    def resolve_candidate(self, candidate: PortfolioCandidate) -> PortfolioCandidate:
        rec = self.resolve(candidate.symbol)
        candidate.sector = rec.sector
        candidate.cluster = rec.cluster
        return candidate
