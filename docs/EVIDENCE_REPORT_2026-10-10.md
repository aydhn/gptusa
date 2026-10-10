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
