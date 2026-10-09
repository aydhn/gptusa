# CLAUDE.md — gptusa (USA Signal Bot)

Always-on çekirdek. Ayrıntılar normal metinle belirtilen yerlerde; yalnız göreve gerekirse oku. `@import` kullanma, `docs/` klasörünü toplu okuma.

## Proje
- Python 3.12 paketi `usa_signal_bot/` (~3000 .py, ~96 üst paket). Giriş: `python -m usa_signal_bot` → `usa_signal_bot/app/cli.py`. ABD hisseleri için araştırma/sinyal sistemi: yfinance + yerel CSV verisi, feature/factor, rejim, ML araştırma, backtest, portföy, paper-güvenlik kapıları.
- Durum: 160 fazlık prompt zinciri TAMAMLANDI. Faz 160 = tasarım/kod mimarisi kapanışı; canlı/paper trading, broker aktivasyonu, deployment onayı veya yatırım tavsiyesi DEĞİLDİR. Kanonik durum: `docs/PROJECT_FINAL_STATUS.md`. Sistem read-only / non-executing metadata üretir.

## Kesin yasaklar (`docs/DEVELOPMENT_RULES.md`)
1. Ücretli API (OpenAI vb.) yok. 2. Web scraping / HTML parsing yok. 3. Broker order routing yok (Alpaca vb. canlı/demo istek kodu bile yazma). 4. Dashboard framework (FastAPI, Flask, Streamlit) yok.
- Order üretimi, paper/live execution, paper-state mutation, sinyal iletimi ekleme. `core/types.py`: `ExecutionMode = Literal["local_paper_only"]`. Mevcut no-execution/firewall/blocker/quarantine/non-activation modüllerini ve `activation_allowed`, `broker_execution_enabled`, `order_creation_enabled` gibi bayrakların `False` kalmasını gevşetme.

## Mimari harita (üst paket → rol)
- **Temel:** `core` (enums.py str-Enum UPPER_CASE, exceptions.py kök `USASignalBotError`, config.py+config_schema.py YAML→dataclass, types.py, paths.py), `utils`, `storage` (json/jsonl/csv store, manifest, integrity), `app` (CLI).
- **Veri:** `data`, `data_providers` (abstraction/registry/selector + adapters), `providers`, `provider_*` (cache, quality, orchestration, governance, freeze, final_acceptance), `data_provider_runtime` (dry-run fetch planı), `universe`, `universe_lifecycle`, `calendar`, `corporate_actions`, `event_metadata`, `event_impact`, `quality`.
- **Araştırma:** `features` (Indicator arayüzü), `feature_engine` (faz 116-125 alt aşamaları: core_indicators, advanced_features, enriched_features, factor_*, integration_freeze, final_closure), `regimes`, `regime_classification` (faz 126-135), `regime_map`, `regime_costs`, `strategies` (abstract `Strategy`), `strategy_adaptation`, `ml`, `ml_research` (faz 136-145: baseline_training, calibration_diagnostics, ensemble_*, drift_monitoring, ml_governance_closure), `research_workflow`/`research_governance`/`research_execution`, `diagnostics`, `comparison`, `attribution`.
- **Backtest/portföy/risk:** `backtesting` (alt: realistic_engine, analytics, walk_forward, stress_robustness, closure), `transaction_costs`, `cost_robustness`, `execution` (tradability/realism proxy, gerçek execution değil), `allocation`, `portfolio` (+ `portfolio_construction`, `portfolio_rebalance`), `optimization`, `risk`, `performance`, `reports`, `regression`.
- **Runtime/operasyon:** `runtime`, `runtime_lifecycle`, `runtime_service_graph`, `core_runtime_acceptance`, `advanced_runtime`, `advanced_transition`, `integration` (faz 157-159), `release`, `release_packaging`, `release_sandbox`, `scheduler` (lock/idempotency/atomic_io), `taskqueue`, `retention`, `observability`, `profiling`, `incident`, `notifications` (telegram_sender burada; `telegram/` boş yer tutucu).
- **Paper-güvenlik katmanı:** `paper` (hesap/ledger/analytics simülasyonu) ve ~24 `paper_*` + `pre_paper_handoff_freeze_gate` + `local_paper_admission_simulator_*` paketi: saf dossier/gate/replay/seal katmanlarıdır, order göndermez. Bunlar `paper_safe_gate`, `paper_quarantine`, `paper_sandbox_bridge`, `paper_shadow`, `paper_observer`, `paper_readiness_*`, `paper_no_write_*`, `paper_firewall_audit` vb. şeklindedir.

- **Araştırma hattı (Aşama 2-4, çalışan çekirdek):** `evidence/` (walk-forward kanıt raporu, `evidence-run`), `decision/` (karar hattı + yerel simüle ledger + NYSE seans takvimi, `decision-simulate`), `ml_loop/` (purged CV, leakage guard, registry, insan onaylı promosyon, `ml-loop-train/approve`). Yeni araştırma kodunu bunlara bağla; `paper_*` dossier katmanlarını çoğaltma. Gerçek veri sonucu henüz yok (`docs/EVIDENCE_REPORT_2026-10-09.md`).

## Kod kalıpları (yeni kodda uy)
- Faz-numaralı, dosya-başına-aşama modüller; tipik ek: `*_models.py` (dataclass), `*_validator/_validation`, `*_safety_validator`, `*_store.py`, `*_report/_reporting`, `*_readiness_gate`, `*_boundary`, `*_adapter`. `paper_*` paketleri ~23-26 dosyalık aynı iskeleti izler (models, ingestion, eligibility_checker, replay_engine/analyzer, audit, continuity, safety_validator, store, report). Yeni paket eklemek yerine mevcut iskeleti kopyala.
- Hata: `core.exceptions` kökünden türet; enum: `class X(str, Enum)` UPPER_CASE değer; yollar `core.paths`; JSON/JSONL/CSV yazımı `storage/` veya paketin `*_store.py`'si üzerinden, atomic IO (`scheduler/atomic_io.py`, `docs/ATOMIC_IO_AND_IDEMPOTENCY.md`).
- Deterministik: zaman/rastgelelik enjekte et (`backtesting/realistic_engine/deterministic_simulation_clock.py`).
- ML: leakage kontrolü zorunlu; optimizer sonuçları out-of-sample doğrulanmadan raporlanmaz; backtest edilmemiş strateji güvenilir sayılmaz; risk yönetimi olmadan sinyal aktifleştirme yok.
- Küçük, geri alınabilir, CLI'dan bağımsız test edilebilir adımlar.
- Tuzaklar: komutlar yalnız `app/cli.py::_command_registrars()` listesine eklenen `setup_*_cli` ile kaydolur (aynı komut adı iki kez = argparse hatası). Yama betiği yazma: import anında kendi dosyasına yazan kod ve `scripts/` altından çekirdek dosyayı yeniden yazan betikler geçmişte `core/enums.py`/`exceptions.py` içeriğini sildi; kaybolan tanımlar `core/_recovered_*.py` ve bazı modüllerin sonunda "recovered" bloğunda. Yeni enum/exception doğrudan `core/enums.py`/`exceptions.py`'ye. `paper_*` ortak IO/doğrulama tabanı: `paper_common/`. Kısmi `__init__` API: `core`, `data`, `features`; diğer `__init__.py`'ler boş olabilir, sembolleri modülden import et.
- Bilinen kırıklar (Aşama 1 sonrası, tam süit ~3277 geçti / ~771 kaldı / ~84 hata): ortamda `yfinance` yoksa veri modülleri import edilemez; bazı enum üyeleri eksik (örn. `DataCoverageStatus.COMPLETE`); `paper_promotion_dossier.dossier_models.PromotionEvidenceIndex` yok; testler arası mock sızıntısı var (tek başına geçen test süitte kalabilir). Karşılaştırma için önce/sonra aynı komutla koş.

## Doğrulama
- Test: `python -m pytest tests/<ilgili>.py` (`pytest.ini`: `pythonpath = .`). `tests/` altında ~2000 dosya (`test_<modül>.py`, bazı alt klasörler) ve `usa_signal_bot/tests/`; tüm süiti yalnız gerektiğinde çalıştır. `tests/conftest.py` `mocker` fixture'ı pytest-mock yoksa sahte sağlar.
- Bağımlılık: `requirements.txt` (PyYAML, pytest, yfinance, pandas); `click`/`typer` kullanma (yüklü değil). Windows: `start_windows.bat`, `RUN_WINDOWS.md`.
- `.gitignore` `*.json, *.csv, *.txt, *.sh, scripts/, data/, tests/fixtures/` yok sayar; yeni dosyanın gerçekten izlendiğini `git status` ile doğrula.
- Sır commit etme: `config/runtime.env` yerel; örnekler `config/runtime.env.example`, `config/local.example.yaml`.

## Git
- Branch `master`, remote `origin` (github.com/aydhn/gptusa). Commit/push yalnız kullanıcı isteyince; bitişte working tree temiz.

## Navigasyon (on-demand)
- `docs/` (~935 dosya; faz tablosu `PHASES_INDEX.md`, ücretsiz veri karşılaştırması `FREE_DATA_SOURCES.md`): `PHASE_<n>_SUMMARY.md`/`_LIMITATIONS.md` faz geçmişi; `*_SAFETY_GUARDS.md`/`*_LIMITATIONS.md` modül sınırları; `ARCHITECTURE.md`, `OPERATOR_RUNBOOK.md`, `INCIDENT_RUNBOOK.md`, `CONFIGURATION.md`, `STORAGE.md`, `ROADMAP.md`. Ayrıca `usa_signal_bot/docs/`. Konuya göre Grep/Glob ile tek dosya bul; faz geçmişini bu dosyada tutma.
