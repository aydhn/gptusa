# Kanıt Hattı Güncellemesi (2026-10-10)

> Araştırma çıktısıdır; yatırım tavsiyesi değildir, kâr garantisi yoktur. Emir/broker/canlı bağlantı yok. Önceki rapor: `EVIDENCE_REPORT_2026-10-09.md`.

## Ne değişti
- **book_to_price bölünme kusuru giderildi:** `evidence/fundamentals.py::split_adjust_shares` raporlanan hisse sayısını dosyalama tarihinden sonraki bölünmelerle bugünkü (bölünme-düzeltmeli) fiyat tabanına çevirir; `fundamental_frames(..., splits)`. Test: `tests/test_evidence_split_shares.py`.
- **Gerçek temel veri:** `evidence-fetch` komutu yfinance fiyatı + SEC EDGAR XBRL companyfacts (resmî JSON, ≤10 req/s, `SEC_USER_AGENT` ortam değişkeni; **repo'ya yazılmaz**, tek seferlik oturum değişkeni) indirir. 50 hisselik listede 50/50, 400'lük SEC-sıralı evrende 381/400 hissede EDGAR verisi bulundu (19 hata: XBRL yok/CIK eşleşmedi).
- **FRED:** DTB3 (tarihsel nakit faizi) ve CPIAUCSL (gerçek enflasyon; `--inflation-csv`, veri aralığındaki bileşik yıllık enflasyon ≈ %2,6) resmî CSV'den çekildi (`fetch_fred_csv`; varsayılan User-Agent FRED tarafından reddediliyordu, tarayıcı benzeri UA eklendi).
- **Yeni kıyasa-göre aileler** (`evidence/factors_rel.py`): beta+eğim, düşük devirli çok-faktör, vol hedefli beta, rejim beta; gerçek temel aileler: değer, kalite, değer+kalite. Hepsi aynı walk-forward + maliyet + purge + nakit faizi hattından geçer, hipotez günlüğüne yazılır.
- **Vergi/komisyon duyarlılığı** rapora eklendi (vergi: yıllık gerçekleşen kâr üzerinden %0/15/25, ceza yönlü basitleştirme; ek maliyet +5/+10 bps × turnover).
- **ML:** `ml_loop/tree_cpcv.py` (scikit-learn HistGradientBoosting/RandomForest, isteğe bağlı meta-labeling) CPCV yolları üzerinde değerlendirilir; ELIGIBLE yalnız sızıntı temiz + yol medyanı kıyasa göre Sharpe>0 + DSR(kıyasa göre)≥0,95 + SPA p≤0,05 + pozitif yol oranı ≥%60 ise (`ModelRegistry.evaluate_cpcv_promotion`). `ml_loop/drift.py` (PSI) → `retrain_trigger` artık gerçek girdi alır; `ml_research` drift sonuçlarının `drift_severity` alanını da okur. Aktivasyon yok, onay insanda (`ml-loop-approve`).
- **Trader raporları:** `decision-report` → karar günlüğü (JSONL), "neden bu pozisyon" izi, günlük kıyasa-göre sapma + risk bütçesi CSV, haftalık özet (nakit faizi ve reel getiri her raporda). Yerel simüle ledger.

## Sonuçlar (tarihsel nakit faizi DTB3, gerçek CPI)
**50 hisse (statik liste), 44 aday, Hansen SPA p ≈ 0,54:** 15 ailenin 14'ü NEGATİF, 1'i (düşük devirli çok-faktör: OOS CAGR ~%17,4 vs kıyas ~%17,3, Sharpe 1,07 vs 1,06) BELİRSİZ; kıyasa göre DSR ≤ ~0,11. Kıyası geçen kanıtlı edge yok.

**400 hisse (SEC sıralı, bugünkü liste), 44 aday, SPA p ≈ 0,09 (RC ≈ 0,07):** kıyas CAGR ~%20,6 (Sharpe 1,16); 14 aile NEGATİF, kalite (vekil) BELİRSİZ; kıyasa göre DSR ≈ 0–0,02. En yakın SPA değeri bile %5 eşiğinin üstünde ve kıyasa göre DSR ≈ 0 → **kıyası geçen edge yok**. Fiyat doğrulama uyarısı 37 (bölünme tablosu ile fiyat uyuşmazlığı; incelenmedi).

**ML (50 hisse, CPCV 5 yol, N=45-48):** HGB: yol medyanı CAGR ~%14,6 vs kıyas ~%16,4, kıyasa göre DSR 0,08 → REJECTED. HGB+meta: ~%6,8, REJECTED. RF: ~%16,1, DSR 0,21, SPA p 0,57 → REJECTED. RF+meta: ~%7,4 → REJECTED. Özellik kayması (PSI, ilk/ikinci yarı): vol_21/vol_126 YÜKSEK → yeniden eğitim adayı tetiklenir, ancak aktivasyon yok.

**Öneri (yatırım tavsiyesi değildir):** bu veriyle ucuz, çeşitlendirilmiş beta + boştaki nakit faizi, aktif stratejilerden daha iyi savunulabilir.

## Sınırlar
Statik/bugünkü evren → hayatta kalma yanlılığı (kaldırılamadı; gerçek çözüm ücretli noktasal-zamanlı veri, bütçe belirtilmedi). 400'lük evren SEC dosya sırasıyla seçildi (endeks değil). Yahoo verisi revize edilebilir. Vergi modeli basit. Tek dönem (2010+), 44 aday. Bu çıktı yatırım tavsiyesi veya kâr beklentisi değildir.

## Yeniden çalıştırma
```
set SEC_USER_AGENT=<ad> <e-posta>   (yalnız oturum; commit etme)
python -m usa_signal_bot evidence-fetch --universe sec-top --n 400 --prices --csv-dir data/prices400 --fundamentals-dir data/fundamentals400
python -m usa_signal_bot evidence-run --source csv --csv-dir data/prices400 --cash-rate-csv data/evidence/DTB3.csv --inflation-csv data/evidence/CPIAUCSL.csv --fundamentals-dir data/fundamentals400 --hypothesis-log data/evidence/hyp_400.jsonl --write
python -m usa_signal_bot ml-loop-cpcv --source csv --csv-dir data/prices --model rf --meta --hypothesis-log data/evidence/hyp_real.jsonl
python -m usa_signal_bot decision-report --source csv --csv-dir data/prices --cash-rate-csv data/evidence/DTB3.csv --inflation-csv data/evidence/CPIAUCSL.csv
```

---

# Ek Bölüm — 2026-10-10 (ikinci tur)

> Araştırma çıktısıdır; yatırım tavsiyesi değildir, kâr garantisi yoktur. Emir/broker/canlı yok.

## Yapılan
- **Fiyat doğrulama (37 uyarı):** kök neden bölünme uyuşmazlığı DEĞİL; 37'nin tamamı `UNEXPLAINED_JUMP` idi ve çoğu gerçek hareket (Mart 2020 enerji çöküşü, VRTX/NFLX/CVNA kazanç günleri, MRNA +%177). `validate_adjusted_prices` artık bölünme tarihine ±3 gün tolerans verir, bölünme oranı biçiminde olmayan büyük hareketi `LARGE_MOVE` sayar (varsayılan raporlanmaz). 400 hisse: 37 → 1 (HTHIY ADR, ≈-%49,5, elle incelenmeli). Test: `tests/test_evidence_price_validation.py`.
- **Ölü kod:** `app/runtime.py` ve `core/runtime_state.py` (importer yok, `config.runtime.*` okuyordu) silindi; `core/config.py`'deki tanımsız üç şema bloğu (NameError riski) kaldırıldı. `AppConfig` onarılmadı (kullanıcısı yok).
- **Yeni aday aileler** (`evidence/macro_regime.py`, `sector_rotation.py`, `earnings_drift.py`): hepsi aynı walk-forward+maliyet+purge+DTB3 hattında, hipotez günlüğünde (81 deneme), sızıntı testli (`tests/test_evidence_new_families.py`).
- **Öğrenme döngüsü:** `ml-loop-cycle` (`ml_loop/auto_cycle.py`; drift→tetik→CPCV→kapı→rapor; aynı gün tekrar = no-op; aktivasyon yok, terfi yalnız `ml-loop-approve`). Runbook: `docs/AUTO_CYCLE_RUNBOOK.md`.
- **Rapor paketi:** `decision-package` (`decision/package.py`): karar günlüğü, neden-izi, kıyasa göre sapma+risk bütçesi, hipotez özeti, reel getiri; markdown/CSV.
- **Test:** `test_data_cache` flaky kökü: Windows dosya mtime'ı `time.time()`'dan ileri → negatif yaş (`cache_file_age_seconds` sıfıra sıkıştırıldı; 30/30 geçti, öncesi ~2/15 hata). 10 yinelenen test adı `_pkg`/`_pq` ekiyle benzersizleştirildi.

## Sonuç (400 hisse, 81 deneme, PBO ≈ 0,29, SPA p ≈ 0,15, White RC p ≈ 0,13)
| Aile | OOS CAGR / Sharpe | Kıyas CAGR / Sharpe | Kıyasa göre DSR | Karar |
|---|---|---|---|---|
| Makro rejim (FRED) | ~%14,6 / 1,44 | ~%20,6 / 1,16 | ≈0 | NEGATİF |
| Dosyalama sonrası sürüklenme | ~%19,8 / 1,13 | ~%20,6 / 1,16 | ≈0 | NEGATİF |
| Sektör momentum (ETF) | ~%10,6 / 0,65 | ~%14,8 / 0,92 | ≈0 | NEGATİF |
| Sektör düşük vol (ETF) | ~%11,7 / 0,87 | ~%14,8 / 0,92 | ≈0 | NEGATİF |

**Kıyası geçen kanıtlı edge YOK** (eşik: kıyasa göre DSR≥0,95 ve SPA p≤0,05; hiçbiri sağlamadı). Makro rejim Sharpe'ı yüksek, maxDD ≈ -%12 ama nakitte beklerken CAGR'dan vazgeçiyor.

## Belirsiz / sınırlar
- ETF aileleri SPY'a, diğerleri 400'lük eşit ağırlığa göre ölçülür; havuzlanmış SPA tam eşdeğer değil.
- Hayatta kalma yanlılığı devam ediyor; kazanç ailesi 10-K/10-Q dosyalama tarihi kullanır (duyuru tarihi değil), tepki kısmen bayat.
- SEC_USER_AGENT bu turda yok; yeni SEC isteği yapılmadı. HTHIY elle incelenmedi.
- Hipotez günlüğü değil, simüle defterden gelen kıyasa göre istatistikler paket raporunda kullanılır (günlük ham Sharpe tutar).
- Test: `tests` 4078 → 4100 geçti/2 atlandı; `usa_signal_bot/tests` 123 → 123 geçti.
