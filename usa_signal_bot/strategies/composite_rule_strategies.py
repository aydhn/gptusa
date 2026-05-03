from typing import List, Dict, Any, Optional
from usa_signal_bot.strategies.strategy_interface import Strategy
from usa_signal_bot.strategies.strategy_metadata import StrategyMetadata
from usa_signal_bot.strategies.strategy_params import StrategyParameterSchema, StrategyParameterSpec
from usa_signal_bot.strategies.strategy_input import StrategyInputBatch
from usa_signal_bot.strategies.signal_contract import StrategySignal
from usa_signal_bot.core.enums import StrategyCategory, StrategyStatus, SignalAction, RuleStrategyFamily, RuleConditionOperator
from usa_signal_bot.strategies.rule_models import RuleStrategyDefinition, RuleCondition, RuleEvaluation
from usa_signal_bot.strategies.rule_utils import evaluate_conditions, get_latest_feature_row, get_previous_feature_row, calculate_rule_score, normalize_rule_score, classify_rule_bias, build_rule_reasons
from usa_signal_bot.strategies.rule_feature_requirements import composite_rule_required_features
from usa_signal_bot.strategies.rule_signal_builder import build_signal_from_rule_evaluation, create_no_feature_watch_signal

class CompositeTechnicalRuleStrategy(Strategy):

    @property
    def metadata(self) -> StrategyMetadata:
        return StrategyMetadata(
            name="composite_technical_rule",
            version="0.1.0",
            category=StrategyCategory.COMPOSITE,
            status=StrategyStatus.EXPERIMENTAL,
            description="Multi-factor technical rule evaluation.",
            required_features=composite_rule_required_features(),
            produces_actions=[SignalAction.WATCH],
            experimental=True,
            notes=["Produces signal candidates, not for execution"]
        )

    @property
    def parameter_schema(self) -> StrategyParameterSchema:
        return StrategyParameterSchema(
            strategy_name="composite_technical_rule",
            parameters=[
                StrategyParameterSpec(name="min_score", param_type="float", default=60.0, min_value=0.0, max_value=100.0),
                StrategyParameterSpec(name="watch_only", param_type="bool", default=True),
                StrategyParameterSpec(name="require_volume_confirmation", param_type="bool", default=False),
                StrategyParameterSpec(name="require_trend_alignment", param_type="bool", default=False)
            ]
        )

    def _build_definition(self, min_score: float, req_vol: bool, req_trend: bool) -> RuleStrategyDefinition:
        return RuleStrategyDefinition(
            name="composite_technical_rule",
            family=RuleStrategyFamily.COMPOSITE,
            description="Combination of trend, momentum, breakout and volume",
            conditions=[
                RuleCondition(
                    name="trend_aligned",
                    feature_name="close_trend_strength_basic_20",
                    operator=RuleConditionOperator.GT,
                    threshold=0.0,
                    weight=25.0,
                    required=req_trend,
                    description="Trend strength is positive"
                ),
                RuleCondition(
                    name="momentum_supportive",
                    feature_name="close_momentum_10",
                    operator=RuleConditionOperator.GT,
                    threshold=0.0,
                    weight=25.0,
                    description="Momentum is positive"
                ),
                RuleCondition(
                    name="breakout_present",
                    feature_name="breakout_distance_pct_20",
                    operator=RuleConditionOperator.GTE,
                    threshold=0.0,
                    weight=25.0,
                    description="Price near or above breakout"
                ),
                RuleCondition(
                    name="volume_confirmation",
                    feature_name="volume_relative_volume_20",
                    operator=RuleConditionOperator.GT,
                    threshold=1.2,
                    weight=25.0,
                    required=req_vol,
                    description="Relative volume > 1.2"
                )
            ],
            required_features=self.required_features(),
            default_action=SignalAction.WATCH,
            min_passed_conditions=2,
            min_normalized_score=min_score
        )

    def generate_signals(self, batch: StrategyInputBatch, params: Optional[Dict[str, Any]] = None) -> List[StrategySignal]:
        self.assert_no_execution()
        p = self.validate_params(params)

        definition = self._build_definition(
            p["min_score"], p["require_volume_confirmation"], p["require_trend_alignment"]
        )
        signals = []

        for frame in batch.frames:
            latest_row = get_latest_feature_row(frame.rows)
            prev_row = get_previous_feature_row(frame.rows)

            if not latest_row:
                continue

            missing = [f for f in self.required_features() if f not in latest_row]
            if missing:
                sig = create_no_feature_watch_signal(
                    self.metadata.name, frame.symbol, frame.timeframe, latest_row.get("timestamp_utc", ""), missing
                )
                signals.append(sig)
                continue

            results = evaluate_conditions(latest_row, prev_row, definition.conditions)

            passed = sum(1 for r in results if r.passed)
            failed = sum(1 for r in results if r.status.value == "FAILED")
            missing_c = sum(1 for r in results if r.status.value == "MISSING_FEATURE")

            # Check mandatory conditions
            mandatory_failed = any(r.status.value == "FAILED" for r in results if r.condition.required)

            raw_score = calculate_rule_score(results)
            max_possible = sum(c.weight for c in definition.conditions)
            norm_score = normalize_rule_score(raw_score, max_possible)

            bias = classify_rule_bias(definition.family, norm_score, SignalAction.WATCH)
            if norm_score >= definition.min_normalized_score and passed >= definition.min_passed_conditions and not mandatory_failed:
                 bias = classify_rule_bias(definition.family, norm_score, SignalAction.LONG)
            else:
                 bias = classify_rule_bias(definition.family, norm_score, SignalAction.FLAT)

            reasons = build_rule_reasons(results)
            if mandatory_failed:
                 reasons.append("A required condition failed")

            eval_res = RuleEvaluation(
                symbol=frame.symbol,
                timeframe=frame.timeframe,
                timestamp_utc=latest_row.get("timestamp_utc", ""),
                strategy_name=definition.name,
                family=definition.family,
                condition_results=results,
                passed_count=passed,
                failed_count=failed,
                missing_count=missing_c,
                raw_score=raw_score,
                normalized_score=norm_score,
                bias=bias,
                reasons=reasons,
                warnings=[]
            )

            sig = build_signal_from_rule_evaluation(
                eval_res, definition, latest_row, watch_only=p["watch_only"]
            )
            signals.append(sig)

        return signals
