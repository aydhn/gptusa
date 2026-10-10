# AUTO_CYCLE_RUNBOOK - yerel, insan onaylı öğrenme döngüsü

Kapsam: yalnız araştırma + yerel simüle ledger. Emir, broker, ücretli API, scraping yok. Döngü HİÇBİR ŞEYİ aktifleştirmez
(`activation: none`, `activation_allowed=False`). Yatırım tavsiyesi değildir.

## Akış (`ml-loop-cycle`, `usa_signal_bot/ml_loop/auto_cycle.py`)
1. (İsteğe bağlı, yalnız `--refresh`) `evidence/fetch.py` ile fiyat yenileme (yfinance, günlük önbellek). Varsayılan: mevcut CSV'ler.
2. Özellik drift'i (PSI, `ml_loop/drift.py`) -> `retrain_trigger.evaluate_retrain`.
3. Tetiklenirse (veya `--train-anyway`) `tree_cpcv` ile CPCV adayı eğitilir, `ModelRegistry.evaluate_cpcv_promotion` (CPCV+DSR+SPA, kıyasa göre) kapısından geçer. Sonuç en iyi ihtimalle `ELIGIBLE`; asla `APPROVED` değil.
4. Rapor: `<out-dir>/cycle_report.md` + `cycle_report.json` (varsayılan `data/ml_cycle/<UTC tarih>`).

Kilit + idempotency: `scheduler/lock_manager.py` kilidi ve `duplicate_run_guard.py` anahtarı kullanılır; aynı gün ikinci çalıştırma
no-op'tur (`skipped_duplicate`). Zorlamak için `--force`. Hata ile biten çalıştırma kaydı silinir, yeniden denenebilir.

## Çalıştırma
```
python -m usa_signal_bot ml-loop-cycle --source csv --csv-dir data/prices --memberships data/memberships.csv --hypothesis-log data/hypothesis_log.jsonl
python -m usa_signal_bot ml-loop-cycle --source csv --csv-dir data/prices --refresh      # önce veri yenile
```
Terfi (yalnız ELIGIBLE, adı belli insan): `python -m usa_signal_bot ml-loop-approve --model-id <id> --approver <ad> --note "<gerekçe>"`.
Rapor paketi için: `python -m usa_signal_bot decision-package --out-dir data/report_packages`.

## Windows Task Scheduler ile dışarıdan zamanlama (yalnız komut; sürekli çalışan betik yok)
Günlük bir kez çalışır, biter. Örnek (yönetici gerekmez):
```
schtasks /Create /SC DAILY /ST 07:30 /TN "gptusa-ml-cycle" /TR "cmd /c cd /d C:\Projelerim\gptusa && set PYTHONIOENCODING=utf-8 && python -m usa_signal_bot ml-loop-cycle --source csv --csv-dir data\prices"
```
Kaldırma: `schtasks /Delete /TN "gptusa-ml-cycle" /F`. `--refresh` kullanacaksanız `SEC_USER_AGENT` gerekmez (yalnız fiyat); EDGAR çekimi bu döngüde yoktur.

## Sınırlar
- Aynı gün/aynı parametre ikinci çalıştırma yeni aday üretmez (`--force` hariç). Kilit dosyası `<out-dir>/.locks/`.
- Rapor her zaman `activation: none` der; kapıyı geçen aday bile insan onayı olmadan kullanılmaz.
- Statik evren -> hayatta kalma yanlılığı; kapı sonuçları kanıtlı edge anlamına gelmez (`docs/EVIDENCE_REPORT_2026-10-10.md`).
