# CLAUDE.md — gptusa (USA Signal Bot)

Always-on kurallar. Ayrıntılar normal metinle belirtilen dosyalarda; yalnız göreve gerekirse oku (toplu docs taraması yapma, `@import` kullanma).

## Proje
- Python paketi `usa_signal_bot/` (giriş: `python -m usa_signal_bot`, CLI: `usa_signal_bot/app/cli.py`). ABD hisseleri için sinyal/araştırma sistemi: yfinance verisi, feature/factor, rejim, ML araştırma, backtest, portföy, paper-güvenlik kapıları.
- Durum: 160 fazlık prompt zinciri TAMAMLANDI (Faz 160 = tasarım/kod mimarisi kapanışı). Bu canlı/paper trading aktivasyonu, broker aktivasyonu, deployment onayı ya da yatırım tavsiyesi DEĞİLDİR. Kanonik durum: `docs/PROJECT_FINAL_STATUS.md`.
- Sistem read-only / non-executing metadata üretimi olarak çalışır; aktivasyon ayrı ve açık bir iş olmalıdır.

## Kesin yasaklar (docs/DEVELOPMENT_RULES.md)
1. Ücretli API (OpenAI vb.) yok. 2. Web scraping / HTML parsing yok. 3. Broker order routing yok (Alpaca vb. canlı/demo istek kodu bile yazma). 4. Dashboard framework (FastAPI, Flask, Streamlit) yok.
- Paper/live execution, state mutation, order üretimi ekleme; mevcut "no-execution / firewall / blocker / quarantine" modülleri bu sınırı korur, gevşetme.

## Mühendislik kuralları
- Küçük, geri alınabilir, CLI'dan bağımsız test edilebilir modüller; her davranış için test.
- Deterministik: zamanı/rastgeleliği enjekte et; atomic IO ve idempotency (`docs/ATOMIC_IO_AND_IDEMPOTENCY.md`).
- ML: data leakage kontrolü zorunlu. Optimizer sonuçları out-of-sample doğrulanmadan raporlanmaz. Backtest edilmemiş strateji güvenilir sayılmaz.
- Sır/anahtar commit etme: `config/runtime.env` yerel; örnek `config/runtime.env.example`, `config/local.example.yaml`.
- Mevcut `.gitignore` `*.json, *.csv, *.txt, scripts/, data/, tests/fixtures/` gibi yolları yok sayar; yeni dosya eklerken `git status` ile gerçekten izlendiğini doğrula.

## Doğrulama
- Test: `python -m pytest tests/<ilgili_test>.py` (pytest.ini: `pythonpath = .`; ~2000 test dosyası, tüm süiti yalnız gerektiğinde çalıştır). Paket içi testler: `usa_signal_bot/tests/`.
- Bağımlılıklar: `requirements.txt` (PyYAML, pytest, yfinance, pandas). Windows başlatma: `start_windows.bat` (`RUN_WINDOWS.md`).

## Git
- Branch: `master`, remote `origin` (github.com/aydhn/gptusa). Commit/push yalnız kullanıcı isteyince; bitişte working tree temiz olmalı.

## Navigasyon (on-demand)
- `docs/` ~900 dosya, ad kalıpları: `PHASE_<n>_SUMMARY.md` / `_LIMITATIONS.md` (faz geçmişi), `*_SAFETY_GUARDS.md` / `*_LIMITATIONS.md` (modül sınırları), `ARCHITECTURE.md`, `ROADMAP.md`, `OPERATOR_RUNBOOK.md`, `INCIDENT_RUNBOOK.md`, `CONFIGURATION.md`, `STORAGE.md`. Konuya göre `Grep`/`Glob` ile ilgili dosyayı bul.
- Paket modül dizinleri `usa_signal_bot/<alan>/` (data, features, regimes, ml, backtesting, portfolio, paper_*, risk, strategies, ...); ilgili alanı ada göre ara.
- Faz geçmişi için önce `docs/PHASE_<n>_SUMMARY.md`; geçmişi bu dosyada tutma.
