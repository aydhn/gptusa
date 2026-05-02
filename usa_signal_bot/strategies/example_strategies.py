import datetime
from typing import List, Dict, Any, Optional
from usa_signal_bot.strategies.strategy_interface import Strategy
from usa_signal_bot.strategies.strategy_metadata import StrategyMetadata
from usa_signal_bot.strategies.strategy_params import StrategyParameterSchema, StrategyParameterSpec
from usa_signal_bot.strategies.strategy_input import StrategyInputBatch
from usa_signal_bot.strategies.signal_contract import StrategySignal, create_watch_signal
from usa_signal_bot.core.enums import StrategyCategory, StrategyStatus, SignalAction

class TrendFollowingSkeletonStrategy(Strategy):
    @property
    def metadata(self) -> StrategyMetadata:
        return StrategyMetadata(
            name="trend_following_skeleton",
            version="0.1.0",
            category=StrategyCategory.TREND_FOLLOWING,
            status=StrategyStatus.EXPERIMENTAL,
            description="A simple trend following skeleton strategy using EMA crossovers.",
            required_features=["close_ema_20", "close_ema_50"],
            produces_actions=[SignalAction.WATCH],
            experimental=True,
            notes=["Candidate only, no execution"]
        )

    @property
    def parameter_schema(self) -> StrategyParameterSchema:
        return StrategyParameterSchema(
            strategy_name="trend_following_skeleton",
            parameters=[
                StrategyParameterSpec(name="fast_ema_col", param_type="str", default="close_ema_20"),
                StrategyParameterSpec(name="slow_ema_col", param_type="str", default="close_ema_50"),
                StrategyParameterSpec(name="confidence_level", param_type="float", default=0.60)
            ]
        )

    def generate_signals(self, batch: StrategyInputBatch, params: Optional[Dict[str, Any]] = None) -> List[StrategySignal]:
        self.assert_no_execution()
        p = self.validate_params(params)
        fast_col = p["fast_ema_col"]
        slow_col = p["slow_ema_col"]
        conf = p["confidence_level"]

        signals = []
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()

        for frame in batch.frames:
            if not frame.rows:
                continue

            last_row = frame.rows[-1]
            if fast_col in last_row and slow_col in last_row:
                fast_val = last_row[fast_col]
                slow_val = last_row[slow_col]

                if fast_val is not None and slow_val is not None:
                    if fast_val > slow_val:
                        sig = create_watch_signal(
                            strategy_name=self.metadata.name,
                            symbol=frame.symbol,
                            timeframe=frame.timeframe,
                            timestamp_utc=last_row.get("timestamp_utc", now),
                            reason=f"{fast_col} ({fast_val:.2f}) > {slow_col} ({slow_val:.2f})",
                            confidence=conf
                        )
                        sig.feature_snapshot = {fast_col: fast_val, slow_col: slow_val}
                        signals.append(sig)

        return signals

class MeanReversionSkeletonStrategy(Strategy):
    @property
    def metadata(self) -> StrategyMetadata:
        return StrategyMetadata(
            name="mean_reversion_skeleton",
            version="0.1.0",
            category=StrategyCategory.MEAN_REVERSION,
            status=StrategyStatus.EXPERIMENTAL,
            description="A simple mean reversion skeleton using Bollinger Percent B.",
            required_features=["close_bb_percent_b_20_2.0"],
            produces_actions=[SignalAction.WATCH],
            experimental=True,
            notes=["Candidate only, no execution"]
        )

    @property
    def parameter_schema(self) -> StrategyParameterSchema:
        return StrategyParameterSchema(
            strategy_name="mean_reversion_skeleton",
            parameters=[
                StrategyParameterSpec(name="pb_col", param_type="str", default="close_bb_percent_b_20_2.0"),
                StrategyParameterSpec(name="lower_thresh", param_type="float", default=0.05),
                StrategyParameterSpec(name="upper_thresh", param_type="float", default=0.95),
                StrategyParameterSpec(name="confidence_level", param_type="float", default=0.55)
            ]
        )

    def generate_signals(self, batch: StrategyInputBatch, params: Optional[Dict[str, Any]] = None) -> List[StrategySignal]:
        self.assert_no_execution()
        p = self.validate_params(params)
        pb_col = p["pb_col"]
        lower = p["lower_thresh"]
        upper = p["upper_thresh"]
        conf = p["confidence_level"]

        signals = []
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()

        for frame in batch.frames:
            if not frame.rows:
                continue

            last_row = frame.rows[-1]
            if pb_col in last_row:
                pb_val = last_row[pb_col]

                if pb_val is not None:
                    if pb_val < lower or pb_val > upper:
                        sig = create_watch_signal(
                            strategy_name=self.metadata.name,
                            symbol=frame.symbol,
                            timeframe=frame.timeframe,
                            timestamp_utc=last_row.get("timestamp_utc", now),
                            reason=f"{pb_col} ({pb_val:.2f}) outside bounds ({lower}-{upper})",
                            confidence=conf
                        )
                        sig.feature_snapshot = {pb_col: pb_val}
                        signals.append(sig)

        return signals

class MomentumSkeletonStrategy(Strategy):
    @property
    def metadata(self) -> StrategyMetadata:
        return StrategyMetadata(
            name="momentum_skeleton",
            version="0.1.0",
            category=StrategyCategory.MOMENTUM,
            status=StrategyStatus.EXPERIMENTAL,
            description="A simple momentum skeleton using RSI and ROC.",
            required_features=["close_rsi_14", "close_roc_12"],
            produces_actions=[SignalAction.WATCH],
            experimental=True,
            notes=["Candidate only, no execution"]
        )

    @property
    def parameter_schema(self) -> StrategyParameterSchema:
        return StrategyParameterSchema(
            strategy_name="momentum_skeleton",
            parameters=[
                StrategyParameterSpec(name="rsi_col", param_type="str", default="close_rsi_14"),
                StrategyParameterSpec(name="roc_col", param_type="str", default="close_roc_12"),
                StrategyParameterSpec(name="confidence_level", param_type="float", default=0.65)
            ]
        )

    def generate_signals(self, batch: StrategyInputBatch, params: Optional[Dict[str, Any]] = None) -> List[StrategySignal]:
        self.assert_no_execution()
        p = self.validate_params(params)
        rsi_col = p["rsi_col"]
        roc_col = p["roc_col"]
        conf = p["confidence_level"]

        signals = []
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()

        for frame in batch.frames:
            if not frame.rows:
                continue

            last_row = frame.rows[-1]
            if rsi_col in last_row and roc_col in last_row:
                rsi_val = last_row[rsi_col]
                roc_val = last_row[roc_col]

                if rsi_val is not None and roc_val is not None:
                    if rsi_val > 70 or rsi_val < 30 or roc_val > 5 or roc_val < -5:
                        sig = create_watch_signal(
                            strategy_name=self.metadata.name,
                            symbol=frame.symbol,
                            timeframe=frame.timeframe,
                            timestamp_utc=last_row.get("timestamp_utc", now),
                            reason=f"{rsi_col}={rsi_val:.2f}, {roc_col}={roc_val:.2f}",
                            confidence=conf
                        )
                        sig.feature_snapshot = {rsi_col: rsi_val, roc_col: roc_val}
                        signals.append(sig)

        return signals

class VolatilityBreakoutSkeletonStrategy(Strategy):
    @property
    def metadata(self) -> StrategyMetadata:
        return StrategyMetadata(
            name="volatility_breakout_skeleton",
            version="0.1.0",
            category=StrategyCategory.VOLATILITY,
            status=StrategyStatus.EXPERIMENTAL,
            description="A simple volatility breakout skeleton.",
            required_features=["volatility_compression_20_100", "breakout_distance_pct_20"],
            produces_actions=[SignalAction.WATCH],
            experimental=True,
            notes=["Candidate only, no execution"]
        )

    @property
    def parameter_schema(self) -> StrategyParameterSchema:
        return StrategyParameterSchema(
            strategy_name="volatility_breakout_skeleton",
            parameters=[
                StrategyParameterSpec(name="comp_col", param_type="str", default="volatility_compression_20_100"),
                StrategyParameterSpec(name="dist_col", param_type="str", default="breakout_distance_pct_20"),
                StrategyParameterSpec(name="confidence_level", param_type="float", default=0.50)
            ]
        )

    def generate_signals(self, batch: StrategyInputBatch, params: Optional[Dict[str, Any]] = None) -> List[StrategySignal]:
        self.assert_no_execution()
        p = self.validate_params(params)
        comp_col = p["comp_col"]
        dist_col = p["dist_col"]
        conf = p["confidence_level"]

        signals = []
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()

        for frame in batch.frames:
            if not frame.rows:
                continue

            last_row = frame.rows[-1]
            if comp_col in last_row and dist_col in last_row:
                comp_val = last_row[comp_col]
                dist_val = last_row[dist_col]

                if comp_val is not None and dist_val is not None:
                    if comp_val > 0 and abs(dist_val) > 0.02:
                        sig = create_watch_signal(
                            strategy_name=self.metadata.name,
                            symbol=frame.symbol,
                            timeframe=frame.timeframe,
                            timestamp_utc=last_row.get("timestamp_utc", now),
                            reason=f"Compression={comp_val:.2f}, Breakout Dist={dist_val:.2%}",
                            confidence=conf
                        )
                        sig.feature_snapshot = {comp_col: comp_val, dist_col: dist_val}
                        signals.append(sig)

        return signals
