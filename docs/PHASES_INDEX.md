# Faz İndeksi

Kanonik durum: `PROJECT_FINAL_STATUS.md`. Bu tablo `docs/PHASE*.md` dosyalarından üretilmiştir (faz → dosyalar → ilk açıklayıcı cümle). Birebir aynı içerikli çoğaltmalar kaldırılmıştır (örn. Faz 122 için 8 kopya, `PHASE_122_SUMMARY.md` içinde toplandı: factor validation, drift monitoring, versioning, store hardening).

| Faz | Dosyalar | Özet |
|---|---|---|
| 1 | `PHASE_1_SUMMARY.md` | * Projenin çalışacağı ve gelişeceği "Foundation" (Klasör yapısı, meta dokümanlar) kuruldu. |
| 2 | `PHASE_2_SUMMARY.md` | In Phase 2, we heavily reinforced the configuration and safety features of the USA Signal Bot: |
| 4 | `PHASE_4_SUMMARY.md` | Phase 4 successfully established the foundational domain models, types, and schemas for the USA Signal Bot. This phase focused entirely on d |
| 5 | `PHASE_5_SUMMARY.md` | Phase 5 has successfully established the core local storage layer for the USA Signal Bot, delivering a simple, dependency-free local file da |
| 6 | `PHASE_6_SUMMARY.md` | Phase 6 ("Universe Foundation") has successfully established the local asset universe infrastructure for the USA Signal Bot. This phase ensu |
| 7 | `PHASE_7_SUMMARY.md` | Phase 7 establishes the foundation for retrieving financial market data without actually calling out to the internet. |
| 8 | `PHASE_8_SUMMARY.md` | In Phase 8, the USA Signal Bot evolved from structural abstraction into actionable external data retrieval without breaking its safety/paper |
| 9 | `PHASE_9_SUMMARY.md` | Phase 9 establishes a secure, reliable foundation for data quality before any trading logic or technical indicators are applied. It guarante |
| 10 | `PHASE_10_SUMMARY.md` | This phase successfully introduced the Multi-Timeframe Data Pipeline and Data Readiness Checkpoint, completing the data foundation MVP. |
| 11 | `PHASE_11_SUMMARY.md` | Phase 11 extends the universe foundation to support large-scale, multi-source local symbol management. |
| 12 | `PHASE_12_SUMMARY.md` | Phase 12 bridges the gap between massive universe expansion (Phase 11) and reliable market data ingestion. It establishes the "Active Univer |
| 13 | `PHASE_13_SUMMARY.md` | Phase 13 establishes the technical architecture required to compute complex features and indicators on top of our existing robust market dat |
| 15 | `PHASE_15_SUMMARY.md` | This phase introduces a comprehensive momentum feature engineering system without any direct trading signal generation. |
| 16 | `PHASE_16_SUMMARY.md` | The primary objective of Phase 16 was to establish the **Volatility Indicator Pack** for the USA Signal Bot, adding statistical dispersion,  |
| 18 | `PHASE_18_SUMMARY.md` | Phase 18 introduces a comprehensive suite of price action and market structure features to the USA Signal Bot. This phase focuses entirely o |
| 19 | `PHASE_19_SUMMARY.md` | Phase 19 successfully establishes the core infrastructure for Price/Oscillator Divergence Detection. |
| 20 | `PHASE_20_SUMMARY.md` | **Objective**: Unify all individually developed feature packs (Trend, Momentum, Volatility, Volume, Price Action, Divergence) into a single, |
| 21 | `PHASE_21_SUMMARY.md` | - Created the Strategy Engine Foundation. |
| 22 | `PHASE_22_SUMMARY.md` | In this phase, we completed the core analytical processing components required to grade, assess, and filter signals outputted by our `Strate |
| 23 | `PHASE_23_SUMMARY.md` | Phase 23 implemented a complete, modular, rule-based strategy pack consisting of distinct trading strategy families: Trend, Momentum, Mean R |
| 24 | `PHASE_24_SUMMARY.md` | Phase 24 establishes the **Signal Ranking**, **Candidate Selection**, and **Strategy Portfolio Aggregation** pipelines. Building upon the st |
| 25 | `PHASE_25_SUMMARY.md` | Phase 25 establishes the complete foundation for the backtest engine, historical signal replay, and theoretical performance tracking for USA |
| 26 | `PHASE_26_SUMMARY.md` | In Phase 26, the backtest engine was significantly enhanced with realistic transaction cost modeling, advanced performance metrics, and a st |
| 27 | `PHASE_27_SUMMARY.md` | Phase 27 introduces essential research analytics tools, enabling the comparison of strategy backtest results against market benchmarks and d |
| 28 | `PHASE_28_SUMMARY.md` | Phase 28 establishes the foundation for Walk-Forward Analysis and Out-of-Sample evaluation within the USA Signal Bot. |
| 29 | `PHASE_29_SUMMARY.md` | - **Monte Carlo Simulator**: Trade bootstrap, equity return bootstrap, and trade order permutation logic. |
| 30 | `PHASE_30_SUMMARY.md` | Phase 30 introduced the **Parameter Sensitivity Analysis** and **Non-Optimizer Robustness Grid** foundations for the USA Signal Bot. |
| 31 | `PHASE_31_SUMMARY.md` | Phase 31 successfully implemented the foundational risk management and position sizing engine. |
| 32 | `PHASE_32_SUMMARY.md` | Phase 32 has laid the structural foundation for bridging the strategy and risk output with backtesting limits. |
| 33 | `PHASE_33_SUMMARY.md` | Implemented portfolio-aware basket simulations. |
| 34 | `PHASE_34_SUMMARY.md` | - Models: `PipelineStepConfig`, `MarketScanRequest`, `ScheduledScanPlan`, etc. |
| 35 | `PHASE_35_SUMMARY.md` | - **Notification Pipeline:** Introduced `usa_signal_bot.notifications` encompassing the storage, dispatching, queue logic, rate-limit, and d |
| 36 | `PHASE_36_SUMMARY.md` | Phase 36 successfully establishes a safe, deterministic, and policy-driven notification routing system. |
| 37 | `PHASE_37_SUMMARY.md` | Phase 37 established the foundational infrastructure for Local Simulated Paper Trading. |
| 38 | `PHASE_38_SUMMARY.md` | **Paper Trading Runtime Integration, Notification Reporting & Daily Virtual Account Report** |
| 39 | `PHASE_39_SUMMARY.md` | This phase successfully implemented local paper performance analytics, drawdown monitoring, and virtual risk reporting without relying on an |
| 40 | `PHASE_40_SUMMARY.md` | - Implemented **Comparison Models**: `ComparisonRunRequest`, `MatchedTradePair`, gap metrics. |
| 41 | `PHASE_41_SUMMARY.md` | Phase 41 successfully orchestrated the integration of a multi-dimensional analysis system measuring the holistic quality of the USA Signal B |
| 42 | `PHASE_42_SUMMARY.md` | Phase 42 successfully implemented an End-to-End Regression Harness, Golden Sample Generator, and Release Candidate Rehearsal system for the  |
| 43 | `PHASE_43_SUMMARY.md` | - Established Local Release Packaging infrastructure using Python standard libraries (no external heavy packagers). |
| 46 | `PHASE_46_SUMMARY.md` | **Goal:** Establish a robust local incident response, failure recovery, and safe rollback workflow without introducing external telemetry, b |
| 47 | `PHASE_47_SUMMARY.md` | Phase 47 established a secure foundation for running background-like workflows in a safe, local, and collision-free manner. |
| 49 | `PHASE_49_SUMMARY.md` | Phase 49 establishes an entirely offline, operational resource measurement architecture to provide the system with robust boundaries prevent |
| 50 | `PHASE_50_SUMMARY.md` | In Phase 50, the localized execution framework was reinforced by implementing the **Local Performance Baselines and SLA-style Acceptance Thr |
| 51 | `PHASE_51_SUMMARY.md` | In this phase, we completed the Hardening and Abstraction of the Data Provider Layer: |
| 52 | `PHASE_52_SUMMARY.md` | - **Calendar Models**: MarketHoliday, MarketEarlyClose, MarketSession, TradingDayResult, SessionValidationResult, CalendarReviewResult. |
| 53 | `PHASE_53_SUMMARY.md` | In Phase 53, the **USA Signal Bot** architecture was fortified with a comprehensive local **Universe Survivorship-Bias Guard, Delisting Awar |
| 54 | `PHASE_54_SUMMARY.md` | **Phase 54: Liquidity, Tradability, Borrowability-Proxy and Execution Realism Guard** |
| 55 | `PHASE_55_SUMMARY.md` | Phase 55 introduces an execution realism layer designed to calculate heuristic transaction costs, market impact penalties, and cost-adjusted |
| 56 | `PHASE_56_SUMMARY.md` | Phase 56 introduces the Cost Robustness and Execution Sensitivity framework. This layer acts as an advanced, purely local heuristic filter t |
| 57 | `PHASE_57_SUMMARY.md` | **Regime-Aware Cost Modeling & Adaptive Execution Realism** |
| 59 | `PHASE_59_SUMMARY.md` | Phase 59 introduces **Regime-Conditioned Strategy Selection and Adaptive Strategy Ensembles**. |
| 61 | `PHASE_61_SUMMARY.md` | In Phase 61, the Portfolio Construction and Exposure Balancing layer was implemented. |
| 62 | `PHASE_62_SUMMARY.md` | - Added `Portfolio Rebalance Models` and Target Extractors. |
| 63 | `PHASE_63_SUMMARY.md` | Phase 63 establishes the core attribution framework for the USA Signal Bot. It provides deep analytics on local backtests and paper trading  |
| 65 | `PHASE_65_SUMMARY.md` | Phase 65 builds the local Research Workflow and Controlled Experiment Planning module. |
| 66 | `PHASE_66_SUMMARY.md` | - **Execution Models:** Built models for Contexts, Runs, Comparisons, and Reviews. |
| 67 | `PHASE_67_SUMMARY.md` | - Implemented core governance models and enums. |
| 68 | `PHASE_68_SUMMARY.md` | In this phase, we developed Safe Local Release Packaging, Artifact Freezing, and Versioned Candidate Bundle architecture. |
| 69 | `PHASE_69_SUMMARY.md` | This phase fully developed the local Sandbox environment isolating deployment routines from production bindings: |
| 70 | `PHASE_70_SUMMARY.md` | In this phase, we implemented the Sandboxed Paper-Shadow Rehearsal and Isolated Simulation Session subsystem. |
| 71 | `PHASE_71_SUMMARY.md` | Implemented Sandboxed Paper-Shadow Comparison and Rehearsal Governance. |
| 72 | `PHASE_72_SUMMARY.md` | Implemented the Quarantined Local Paper Candidate Enrollment, Read-Only Promotion Ticket, and Supervised Dry-Run Bridge systems. |
| 73 | `PHASE_73_SUMMARY.md` | - Implemented **DryRunBridgeModels** including Context, Proposal, Session, Checkpoint, and Review structures. |
| 74 | `PHASE_74_SUMMARY.md` | - Added Observation models and Strict Validation Rules. |
| 76 | `PHASE_76_SUMMARY.md` | Phase 76 successfully implemented the "Human-Approved Non-Executing Paper Observer Enrollment, Locked Observer Runtime, and Read-Only Parall |
| 77 | `PHASE_77_SUMMARY.md` | - Built Observer governance models. |
| 78 | `PHASE_78_SUMMARY.md` | In this phase, the Non-Executing Observer Promotion Dossier and Final Safety Board were successfully implemented. |
| 79 | `PHASE_79_SUMMARY.md` | Phase 79 implemented the Staged Non-Executing Paper Readiness Rehearsal, Final Review Lock, and Guarded Handoff Registry. |
| 80 | `PHASE_80_SUMMARY.md` | Implemented the Final Non-Executing Handoff Review, Sealed Readiness Archive, and Pre-Paper Governance Checkpoint. |
| 81 | `PHASE_81_SUMMARY.md` | Phase 81 establishes the core safeguards preventing unapproved transitions from evaluation to actual paper or live trading, ensuring safe an |
| 82 | `PHASE_82_SUMMARY.md` | - Firewall audit models. |
| 84 | `PHASE_84_SUMMARY.md` | Developed the Human-Gated Paper Readiness Board, Write-Blocked Paper Runtime Adapter, and Final Activation Firewall. |
| 85 | `PHASE_85_SUMMARY.md` | In this phase, we implemented: |
| 86 | `PHASE_86_SUMMARY.md` | Implement Paper-Mode Dry Admission Rehearsal, Runtime Write-Lock Proof Refresh, and Human Approval Ledger to ensure strict local validation  |
| 87 | `PHASE_87_SUMMARY.md` | Phase 87 implements the Guarded Paper-Mode Admission Review, Approval-Ledger Reconciliation, and Final No-Write Transition Checkpoint. |
| 88 | `PHASE_88_SUMMARY.md` | Phase 88 successfully implements the Paper-Mode No-Write Transition Dossier, Admission Evidence Seal and Final Paper Sandbox Bridge. |
| 89 | `PHASE_89_SUMMARY.md` | In this phase, we implemented: |
| 90 | `PHASE_90_SUMMARY.md` | - No-order dossier models and evidence collector. |
| 91 | `PHASE_91_SUMMARY.md` | Phase 91 introduced the `paper_boundary_certificate` subsystem. This layer captures Phase 90's no-order outcomes and constructs a rigid sand |
| 92 | `PHASE_92_SUMMARY.md` | Implemented Boundary Certificate Replay, Frozen Evidence Integrity Audit, and Final Paper Safe Gate. Fully local and safe. |
| 94 | `PHASE_94_SUMMARY.md` | Phase 94, "USA SIGNAL BOT / PRE-PAPER LOCAL RUNTIME MAP REPLAY, NON-EXECUTION SEAL INTEGRITY AUDIT AND FINAL PAPER-READINESS NON-EXECUTION B |
| 95 | `PHASE_95_SUMMARY.md` | In Phase 95, we implemented the Paper-Readiness Non-Execution Board Dossier, Acceptance Board Seal, and Final Paper-Mode Shadow-Launch Block |
| 96 | `PHASE_96_SUMMARY.md` | - Dry-admission gate models. |
| 97 | `PHASE_97_SUMMARY.md` | Phase 97 introduces the ultimate metadata collection and boundary assurance artifacts before transitioning towards complete rehearsal simula |
| 98 | `PHASE_98_SUMMARY.md` | Bu fazda yapılanlar: |
| 99 | `PHASE_99_SUMMARY.md` | This phase successfully implements the Simulator Dossier, Acceptance Seal, and Sandbox Runtime Admission Blocker subsystems: |
| 100 | `PHASE_100_SUMMARY.md` | Phase 100 encapsulates the closure of the MVP/local-offline pre-paper pipeline. By utilizing the pre-paper handoff freeze gate, we convert t |
| 101 | `PHASE_101_POST_MVP_FUNCTIONAL_REOPENING.md`, `PHASE_101_SUMMARY.md` | PHASE_101_POST_MVP_FUNCTIONAL_REOPENING\nPhase 101 is the start of advanced development post-MVP. It is NOT active paper trading. |
| 102 | `PHASE_102_ADVANCED_RUNTIME_REGISTRY_NORMALIZATION.md`, `PHASE_102_LIMITATIONS.md`, `PHASE_102_SUMMARY.md` | Phase 102 establishes the normalized runtime registry and the base structure for provider integrations without allowing execution. |
| 103 | `PHASE_103_LIMITATIONS.md`, `PHASE_103_RUNTIME_SERVICE_GRAPH.md`, `PHASE_103_SUMMARY.md` | Phase 103 is a structural metadata phase. It prepares the system for full multi-source execution lifecycle management but introduces none of |
| 104 | `PHASE_104_LIFECYCLE_MANAGER.md`, `PHASE_104_LIMITATIONS.md`, `PHASE_104_SUMMARY.md` | Phase 104 builds the metadata-only runtime lifecycle manager. It introduces state machine controls and service readiness evaluations designe |
| 105 | `PHASE_105_CORE_RUNTIME_ACCEPTANCE.md`, `PHASE_105_LIMITATIONS.md`, `PHASE_105_SUMMARY.md` | Phase 105 closes the Phase 101–105 core runtime consolidation band. It involves fetching Phase 104 lifecycle review events, applying accepta |
| 106 | `PHASE_106_DATA_PROVIDER_ABSTRACTION.md`, `PHASE_106_LIMITATIONS.md`, `PHASE_106_PROVIDER_EXPANSION_READINESS.md`, `PHASE_106_SUMMARY.md` | Phase 106 initiates the data provider abstraction layer. It consumes the read-only Phase 105 kickoff gate output. |
| 107 | `PHASE_107_FREE_MARKET_DATA_PROVIDER_IMPLEMENTATION.md`, `PHASE_107_LIMITATIONS.md`, `PHASE_107_SUMMARY.md` | This phase implements free market data provider adapters with cache-aware fetch dry-run capabilities and provider contract tests. |
| 108 | `PHASE_108_LIMITATIONS.md`, `PHASE_108_PROVIDER_CACHE_STORE.md`, `PHASE_108_SUMMARY.md` | Phase 108 is NOT an activation phase. No real live trading or actual API fetching occurs. |
| 109 | `PHASE_109_LIMITATIONS.md`, `PHASE_109_PROVIDER_DATA_QUALITY_SCORING.md`, `PHASE_109_SUMMARY.md` | This phase is explicitly bounded: |
| 110 | `PHASE_110_LIMITATIONS.md`, `PHASE_110_PROVIDER_ORCHESTRATION.md`, `PHASE_110_SUMMARY.md` | - Phase 110 is **NOT** an activation phase. |
| 111 | `PHASE_111_LIMITATIONS.md`, `PHASE_111_MACRO_CALENDAR_NEWS_METADATA.md`, `PHASE_111_SUMMARY.md` | Phase 111 is not activation. |
| 112 | `PHASE_112_EVENT_IMPACT_TAGGING.md`, `PHASE_112_LIMITATIONS.md`, `PHASE_112_SUMMARY.md` | Phase 112 is the event impact tagging phase. |
| 113 | `PHASE_113_DATA_PROVIDER_EXPANSION_ACCEPTANCE.md`, `PHASE_113_LIMITATIONS.md`, `PHASE_113_SUMMARY.md` | PHASE_113_DATA_PROVIDER_EXPANSION_ACCEPTANCE.md\n\nThis document outlines Phase 113... |
| 114 | `PHASE_114_LIMITATIONS.md`, `PHASE_114_PROVIDER_EXPANSION_FREEZE.md`, `PHASE_114_SUMMARY.md` | - Phase 114 is not activation. |
| 115 | `PHASE_115_DATA_PROVIDER_FINAL_ACCEPTANCE.md`, `PHASE_115_LIMITATIONS.md`, `PHASE_115_SUMMARY.md` | This phase completes the Data Provider Expansion (Phase 106-115). |
| 116 | `PHASE_116_FEATURE_FACTOR_ENGINE_FOUNDATION.md`, `PHASE_116_LIMITATIONS.md`, `PHASE_116_SUMMARY.md` | This document outlines the foundation of the advanced indicators, features, and factor engine in the `usa_signal_bot`. |
| 117 | `PHASE_117_CORE_TECHNICAL_INDICATORS.md`, `PHASE_117_LIMITATIONS.md`, `PHASE_117_SUMMARY.md` | This phase implements local-only core technical indicators. It is not an activation phase and does not produce trade signals. |
| 118 | `PHASE_118_ADVANCED_FEATURE_EXPANSION.md`, `PHASE_118_LIMITATIONS.md`, `PHASE_118_SUMMARY.md` | Phase 118 extends the core indicator foundation set in Phase 117 by adding advanced statistical, time-series, and cross-sectional features t |
| 119 | `PHASE_119_FEATURE_ENRICHMENT_AND_INTERACTIONS.md`, `PHASE_119_LIMITATIONS.md`, `PHASE_119_SUMMARY.md` | Phase 119 introduces event/quality/calendar-aware feature enrichment and interaction builders. |
| 120 | `PHASE_120_FACTOR_COMPOSITION.md`, `PHASE_120_LIMITATIONS.md`, `PHASE_120_SUMMARY.md` | Phase 120 is the fifth phase of the feature/factor engine band (Phase 116-125). It builds on the outputs of Phase 119's feature enrichment p |
| 121 | `PHASE_121_FACTOR_SCORING.md`, `PHASE_121_LIMITATIONS.md`, `PHASE_121_SUMMARY.md` | Factor scoring, normalization, diagnostics and factor table computation phase. |
| 122 | `PHASE_122_SUMMARY.md` | Phase 122 focuses on factor validation, drift monitoring, versioning, and store hardening. It is strictly local metadata and performs no rea |
| 124 | `PHASE_124_INTEGRATION_REHEARSAL_AND_FREEZE_PREP.md`, `PHASE_124_SUMMARY.md` | This document outlines the usage of Phase 124 components, providing the end-to-end integration rehearsal, report QA acceptance, and freeze p |
| 125 | `PHASE_125_FEATURE_FACTOR_FINAL_CLOSURE.md`, `PHASE_125_LIMITATIONS.md`, `PHASE_125_SUMMARY.md` | This document details Phase 125, the final closure phase for the advanced indicator/feature/factor engine band (Phases 116–125). |
| 126 | `PHASE_126_KICKOFF_GATE.md`, `PHASE_126_LIMITATIONS.md`, `PHASE_126_REGIME_CLASSIFICATION_FOUNDATION.md`, `PHASE_126_SUMMARY.md` | The Phase 126 Kickoff Gate is a strictly local metadata requirement gate that ensures all conditions from the Feature/Factor Engine are met  |
| 128 | `PHASE_128_LIMITATIONS.md`, `PHASE_128_REGIME_LABELING.md`, `PHASE_128_SUMMARY.md` | - NOT a strategy/signal engine. |
| 129 | `PHASE_129_LIMITATIONS.md`, `PHASE_129_REGIME_TRANSITION_ANALYTICS.md`, `PHASE_129_SUMMARY.md` | - This phase does not perform strategy activation. |
| 130 | `PHASE_130_LIMITATIONS.md`, `PHASE_130_MARKET_BEHAVIOR_PROFILING.md`, `PHASE_130_SUMMARY.md` | - Phase 130 is a diagnostic reporting layer only. |
| 131 | `PHASE_131_LIMITATIONS.md`, `PHASE_131_REGIME_AWARE_ALIGNMENT.md`, `PHASE_131_SUMMARY.md` | - Phase 131 is NOT an activation. |
| 132 | `PHASE_132_LIMITATIONS.md`, `PHASE_132_REGIME_CONTEXT_COMPATIBILITY_VALIDATION.md`, `PHASE_132_SUMMARY.md` | - The results cannot be used to trigger strategy operations. |
| 133 | `PHASE_133_LIMITATIONS.md`, `PHASE_133_REGIME_AWARE_MONITORING.md`, `PHASE_133_SUMMARY.md` | This phase is not: |
| 135 | `PHASE_135_LIMITATIONS.md`, `PHASE_135_REGIME_FINAL_CLOSURE.md`, `PHASE_135_SUMMARY.md` | Phase 135 is research closure only. |
| 136 | `PHASE_136_ADVANCED_ML_FOUNDATION.md`, `PHASE_136_LIMITATIONS.md`, `PHASE_136_ML_KICKOFF_INPUT_CONTRACT.md`, `PHASE_136_SUMMARY.md` | This phase marks the beginning of the Advanced ML band (136-145). It establishes the read-only dataset contracts, governance rules, and leak |
| 137 | `PHASE_137_LIMITATIONS.md`, `PHASE_137_ML_DATASET_ASSEMBLY.md`, `PHASE_137_SUMMARY.md` | 1. ML Dataset Assembly is local and research-only. |
| 138 | `PHASE_138_BASELINE_ML_EXPERIMENT_SCAFFOLDING.md`, `PHASE_138_LIMITATIONS.md`, `PHASE_138_SUMMARY.md` | Phase 138 introduces the baseline ML experiment scaffolding and non-activation evaluation harness. It ingests the `MLDatasetAssemblyFullRevi |
| 139 | `PHASE_139_LIMITATIONS.md`, `PHASE_139_LOCAL_BASELINE_ML_TRAINING.md`, `PHASE_139_SUMMARY.md` | PHASE 139 LIMITATIONS |
| 140 | `PHASE_140_BASELINE_MODEL_COMPARISON.md`, `PHASE_140_LIMITATIONS.md`, `PHASE_140_SUMMARY.md` | Phase 140 is the fifth phase in the Advanced ML, ensemble, calibration, model drift, explainability, and governance band. |
| 141 | `PHASE_141_CALIBRATION_DIAGNOSTICS.md`, `PHASE_141_LIMITATIONS.md`, `PHASE_141_SUMMARY.md` | Phase 141 performs calibration diagnostics, probability reliability review, and post-training validation on offline prediction artifacts. |
| 142 | `PHASE_142_ENSEMBLE_RESEARCH_SCAFFOLDING.md`, `PHASE_142_LIMITATIONS.md`, `PHASE_142_SUMMARY.md` | Phase 142 Ensemble Research Scaffolding\n\nPhase 142 produces ensemble blending preparation and calibration-aware governance. It does not pe |
| 143 | `PHASE_143_LIMITATIONS.md`, `PHASE_143_OFFLINE_ENSEMBLE_PROTOTYPE_EVALUATION.md`, `PHASE_143_SUMMARY.md` | - This phase is NOT active trading. |
| 144 | `PHASE_144_LIMITATIONS.md`, `PHASE_144_MODEL_DRIFT_BASELINE.md`, `PHASE_144_SUMMARY.md` | - **No Real-Time Capabilities:** Phase 144 cannot monitor live data feeds. |
| 145 | `PHASE_145_EXPLAINABILITY_AND_ML_GOVERNANCE_CLOSURE.md`, `PHASE_145_LIMITATIONS.md`, `PHASE_145_SUMMARY.md` | This document describes the Phase 145 explainability metadata, final ML governance closure and Advanced ML band final audit phase. |
| 146 | `PHASE_146_LIMITATIONS.md`, `PHASE_146_REALISTIC_BACKTEST_FOUNDATION.md`, `PHASE_146_SUMMARY.md` | - Phase 146 is NOT a full backtest run. |
| 147 | `PHASE_147_LIMITATIONS.md`, `PHASE_147_OFFLINE_DETERMINISTIC_BACKTEST_ENGINE.md`, `PHASE_147_SUMMARY.md` | Single strategy only. No optimization. No Walk-Forward/Stress test (delegated to 148). |
| 148 | `PHASE_148_ADVANCED_BACKTEST_ANALYTICS.md`, `PHASE_148_LIMITATIONS.md`, `PHASE_148_SUMMARY.md` | Phase 148 is the offline advanced backtest analytics, trade diagnostics, and run validation phase. |
| 150 | `PHASE_150_LIMITATIONS.md`, `PHASE_150_SUMMARY.md`, `PHASE_150_WALK_FORWARD_VALIDATION.md` | - Phase 150 is walk-forward validation phase. |
| 151 | `PHASE_151_LIMITATIONS.md`, `PHASE_151_STRESS_SCENARIO_MONTE_CARLO_ROBUSTNESS.md`, `PHASE_151_SUMMARY.md` | - **Not Deployment:** Passing Phase 151 does NOT mean the strategy is deployed. |
| 152 | `PHASE_152_BACKTEST_ROBUSTNESS_FINAL_AUDIT.md`, `PHASE_152_LIMITATIONS.md`, `PHASE_152_SUMMARY.md` | Phase 152 serves as the final audit and closure step for the Realistic Backtest band. |
| 153 | `PHASE153_HANDOFF_INGESTION.md`, `PHASE153_HANDOFF_PACKAGE_BOUNDARIES.md`, `PHASE153_PORTFOLIO_HANDOFF_CONTRACT.md`, `PHASE_153_LIMITATIONS.md`, `PHASE_153_PORTFOLIO_CONSTRUCTION_FOUNDATION.md`, `PHASE_153_SUMMARY.md` | Ingests the handoff package from Phase 152. Strictly read-only behavior. |
| 154 | `PHASE154_INPUTS_AND_BOUNDARIES.md`, `PHASE_154_DETERMINISTIC_POSITION_SIZING_PROTOTYPES.md`, `PHASE_154_LIMITATIONS.md`, `PHASE_154_SUMMARY.md` | - **Portfolio Foundation Review**: Contains the final state from Phase 153. |
| 155 | `PHASE155_INPUTS_AND_BOUNDARIES.md`, `PHASE_155_LIMITATIONS.md`, `PHASE_155_SUMMARY.md` | Phase 155 consumes inputs from the previous phase (154) and strictly adheres to predefined boundaries to prevent active executions. |
| 156 | `PHASE156_INPUTS_AND_BOUNDARIES.md`, `PHASE_156_LIMITATIONS.md`, `PHASE_156_PORTFOLIO_OPTIMIZATION_PROTOTYPE.md`, `PHASE_156_SUMMARY.md` | - Portfolio construction reviews |
| 157 | `PHASE157_INPUTS_AND_BOUNDARIES.md`, `PHASE_157_LIMITATIONS.md`, `PHASE_157_PORTFOLIO_RISK_REPORTING_AND_CLOSURE.md`, `PHASE_157_SUMMARY.md` | - Optimizer Prototype Review |
| 158 | `PHASE158_INPUTS_AND_BOUNDARIES.md`, `PHASE158_INTEGRATION_HANDOFF_PACKAGE.md`, `PHASE_158_FULL_SYSTEM_INTEGRATION.md`, `PHASE_158_LIMITATIONS.md`, `PHASE_158_SUMMARY.md` | - Phase 158 Handoff Package |
| 159 | `PHASE159_INPUTS_AND_BOUNDARIES.md`, `PHASE_159_ADVANCED_ACCEPTANCE_REHEARSAL.md`, `PHASE_159_LIMITATIONS.md`, `PHASE_159_SUMMARY.md` | - Phase 158 Full System Integration Review |
| 160 | `PHASE160_HANDOFF_PACKAGE.md`, `PHASE160_INPUTS_AND_BOUNDARIES.md`, `PHASE_160_FINAL_SYSTEM_AUDIT_AND_PROJECT_CLOSURE.md`, `PHASE_160_LIMITATIONS.md`, `PHASE_160_SUMMARY.md` | A secure, read-only package containing the audit, risk register, boundary, and certificate. |
