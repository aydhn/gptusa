from typing import List, Dict, Any, Optional
from usa_signal_bot.strategies.strategy_interface import Strategy
from usa_signal_bot.strategies.strategy_metadata import StrategyMetadata
from usa_signal_bot.strategies.strategy_params import StrategyParameterSchema, StrategyParameterSpec
from usa_signal_bot.strategies.strategy_input import StrategyInputBatch
from usa_signal_bot.strategies.signal_contract import StrategySignal
from usa_signal_bot.core.enums import StrategyCategory, StrategyStatus, SignalAction, RuleStrategyFamily, RuleConditionOperator
from usa_signal_bot.strategies.rule_models import RuleStrategyDefinition, RuleCondition, RuleEvaluation
from usa_signal_bot.strategies.rule_utils import evaluate_conditions, get_latest_feature_row, get_previous_feature_row, calculate_rule_score, normalize_rule_score, classify_rule_bias, build_rule_reasons
from usa_signal_bot.strategies.rule_feature_requirements import momentum_strategy_required_features
from usa_signal_bot.strategies.rule_signal_builder import build_signal_from_rule_evaluation, create_no_feature_watch_signal

class MomentumContinuationRuleStrategy(Strategy):

    @property
    def metadata(self) -> StrategyMetadata:
        return StrategyMetadata(
            name="momentum_continuation_rule",
            version="0.1.0",
            category=StrategyCategory.MOMENTUM,
            status=StrategyStatus.EXPERIMENTAL,
            description="Rule-based momentum continuation candidate generator.",
            required_features=momentum_strategy_required_features(),
            produces_actions=[SignalAction.WATCH, SignalAction.LONG, SignalAction.FLAT],
            experimental=True,
            notes=["Produces signal candidates, not for execution"]
        )

    @property
    def parameter_schema(self) -> StrategyParameterSchema:
        return StrategyParameterSchema(
            strategy_name="momentum_continuation_rule",
            parameters=[
                StrategyParameterSpec(name="min_score", param_type="float", default=55.0, min_value=0.0, max_value=100.0),
                StrategyParameterSpec(name="watch_only", param_type="bool", default=True),
                StrategyParameterSpec(name="rsi_lower", param_type="float", default=50.0, min_value=0.0, max_value=100.0),
                StrategyParameterSpec(name="rsi_upper", param_type="float", default=75.0, min_value=0.0, max_value=100.0)
            ]
        )

    def _build_definition(self, min_score: float, rsi_lower: float, rsi_upper: float) -> RuleStrategyDefinition:
        return RuleStrategyDefinition(
            name="momentum_continuation_rule",
            family=RuleStrategyFamily.MOMENTUM,
            description="Positive momentum confirmation",
            conditions=[
                RuleCondition(
                    name="rsi_supportive",
                    feature_name="close_rsi_14",
                    operator=RuleConditionOperator.BETWEEN,
                    lower=rsi_lower,
                    upper=rsi_upper,
                    weight=40.0,
                    description="RSI in supportive momentum zone"
                ),
                RuleCondition(
                    name="roc_positive",
                    feature_name="close_roc_12",
                    operator=RuleConditionOperator.GT,
                    threshold=0.0,
                    weight=30.0,
                    description="Rate of Change is positive"
                ),
                RuleCondition(
                    name="momentum_positive",
                    feature_name="close_momentum_10",
                    operator=RuleConditionOperator.GT,
                    threshold=0.0,
                    weight=30.0,
                    description="Momentum oscillator is positive"
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

        definition = self._build_definition(p["min_score"], p["rsi_lower"], p["rsi_upper"])
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

            raw_score = calculate_rule_score(results)
            max_possible = sum(c.weight for c in definition.conditions)
            norm_score = normalize_rule_score(raw_score, max_possible)

            bias = classify_rule_bias(definition.family, norm_score, SignalAction.WATCH)
            reasons = build_rule_reasons(results)

            if norm_score >= definition.min_normalized_score and passed >= definition.min_passed_conditions:
                 bias = classify_rule_bias(definition.family, norm_score, SignalAction.LONG)

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
