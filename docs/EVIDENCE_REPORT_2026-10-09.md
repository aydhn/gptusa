# Kanıt Hattı Durumu (2026-10-09)

**Gerçek veri sonucu aşağıda ("Gerçek veri sonucu" bölümü): iki strateji de kıyasın altında kaldı, karar NEGATİF.** Boru hattı ayrıca sentetik veriyle doğrulandı; sentetik sonuç strateji kanıtı değildir.

## Ne var (`usa_signal_bot/evidence/`)
- `universe.py`: point-in-time üyelik (başlangıç/bitiş), ileriye bakış yok.
- `corporate_actions.py`: düzeltilmiş fiyatta split artığı (`UNADJUSTED_SPLIT`) ve açıklanamayan sıçrama kontrolü.
- `costs.py`, `strategies.py`, `walk_forward.py`: komisyon+kayma, SMA trend ve 12-1 momentum, purge'lü walk-forward; parametre yalnız eğitim penceresinde seçilir, ağırlıklar t+1'de uygulanır.
- `metrics.py`, `report.py`: OOS CAGR/Sharpe/MaxDD, blok-bootstrap %95 Sharpe aralığı, kıyas (eşit ağırlık evren) ve açık karar kuralı.
- Testler: `tests/test_evidence_pipeline.py` (gelecek fiyat değişince geçmiş ağırlık değişmiyor, maliyet getiriyi düşürüyor, rapor deterministik).

## Sentetik doğrulama çıktısı (sızıntı yok, gerçek alfa yok)
| Strateji | OOS CAGR | OOS Sharpe | Sharpe %95 GA | MaxDD | Yıllık turnover | Kıyas CAGR | Kıyas Sharpe | Karar |
|---|---|---|---|---|---|---|---|---|
| SMA trend | 9.3% | 0.62 | [-0.13, 1.35] | -32.7% | 53.8 | 10.6% | 0.72 | NEGATİF |
| Momentum 12-1 | 6.8% | 0.47 | [-0.32, 1.18] | -36.4% | 33.7 | 10.6% | 0.72 | NEGATİF |

İki strateji de sentetik (alfasız) piyasada kıyasın altında kaldı: beklenen sonuç, hat sahte alfa üretmiyor.

## Gerçek veri sonucu (yfinance, 2010-01-01 sonrası, 50 büyük hisse, 4217 gün)
Veri: `usa_signal_bot/evidence/fetch.py` ile Yahoo (ücretsiz, resmi olmayan uç) günlük düzeltilmiş kapanış; 50/50 sembol, 32 split satırı, fiyat doğrulama sorunu 0. Maliyet: 1 bps komisyon + 5 bps kayma. Walk-forward: 504 gün eğitim / 126 test / 5 gün purge.

| Strateji | OOS CAGR | Sharpe (%95 CI) | MaxDD | Kıyas CAGR / Sharpe | Karar |
|---|---|---|---|---|---|
| SMA trend | ~%15,4 | 1,00 [0,56; 1,58] | ~%-27,7 | ~%17,3 / 1,06 | NEGATİF |
| Momentum 12-1 | ~%17,1 | 0,93 [0,46; 1,46] | ~%-37,1 | ~%17,3 / 1,06 | NEGATİF |

Kıyas: eşit ağırlıklı aynı evren. İki strateji de kıyası geçemedi.

**Sınırlar:** evren elle seçilmiş, bugün hayatta olan büyük isimler (statik liste) → hayatta kalma yanlılığı; gerçek sonuç bundan daha kötü olabilir, daha iyi değil. Yahoo verisi revize edilebilir/eksik olabilir. Tek dönem, tek parametre ızgarası. Bu, yatırım tavsiyesi veya kâr beklentisi değildir.

Diğer hatlar aynı veriyle: `decision-simulate` (yerel simüle ledger) son özkaynak 101.942 / başlangıç 100.000, CAGR ~%0,1, Sharpe ~0,05, MaxDD ~%-22,1. `ml-loop-train`: OOS rank IC ~0,0126 (eşik 0,02), baz çizgisi 0, sızıntı temiz → REJECTED; aktivasyon yok.

## Yeniden çalıştırma
1. `python -c "from usa_signal_bot.evidence.fetch import fetch_daily, DEFAULT_TICKERS; print(fetch_daily(DEFAULT_TICKERS, 'data/prices'))"` (indirme; `data/` gitignore'da).
2. `python -m usa_signal_bot evidence-run --source csv --csv-dir data/prices --write`
3. Üyelik tablosu (`--memberships`) verilirse hayatta kalma uyarısı kalkar.

## Aşama 5 genişletmesi: DSR/PBO + yeni strateji aileleri (aynı gerçek veri, 50 hisse, statik liste)
Yeni modüller: `evidence/stats.py` (PSR, beklenen-max-Sharpe — örnek uzunluğu T'ye bağlı —, DSR [Bailey & López de Prado 2014], PBO/CSCV [Bailey ve ark. 2017]), `ml_loop/cpcv.py` (Combinatorial Purged CV), `evidence/factors.py` (düşük oynaklık, değer/kalite **vekilleri**, faktör karışımı, rejim filtresi, vol hedefi). Toplam 23 aday denendi; DSR bu N için düzeltilir. "Kıyasa göre DSR" = (OOS − kıyas) getirisinin DSR'ı.

| Strateji | OOS CAGR | OOS Sharpe | DSR | Kıyasa göre DSR | PBO | Karar |
|---|---|---|---|---|---|---|
| SMA trend | ~%15,4 | 1,00 | 1,00 | 0,00 | 0,17 | NEGATİF |
| Momentum 12-1 | ~%17,1 | 0,93 | 1,00 | 0,02 | 0,14 | NEGATİF |
| Düşük oynaklık | ~%11,8 | 0,91 | 1,00 | 0,00 | 0,77 | NEGATİF |
| Değer (vekil) | ~%18,9 | 0,91 | 1,00 | 0,10 | 0,57 | NEGATİF |
| Kalite (vekil) | ~%17,6 | 1,05 | 1,00 | 0,02 | 0,51 | NEGATİF |
| Faktör karışımı | ~%16,1 | 0,98 | 1,00 | 0,00 | 0,71 | NEGATİF |
| Karışım + rejim filtresi | ~%13,4 | 1,03 | 1,00 | 0,00 | 0,71 | NEGATİF |
| Karışım + vol hedefi | ~%11,7 | 1,05 | 1,00 | 0,00 | 0,40 | NEGATİF |

Kıyas (eşit ağırlık): CAGR ~%17,3, Sharpe 1,06. **Sonuç: hiçbir aile kıyasa göre anlamlı üstünlük göstermedi (karar NEGATİF).** Mutlak DSR ≈ 1,00 yalnız "Sharpe sıfırdan farklı" demektir (uzun örnek, ~4200 gün; piyasa betası); kıyasa göre DSR ≈ 0–0,10. Tüm adaylar PBO ≈ 0,40. İlk sürümdeki karar kuralı yalnız CAGR'a baktığı için iki vekil aileyi "POZİTİF" göstermişti; kural düzeltildi (kıyastan düşük Sharpe veya kıyasa göre DSR < 0,95 → pozitif olamaz).

**Sınırlar (değişmedi):** statik 50 hisselik liste, hayatta kalma yanlılığı; değer/kalite gerçek temel veri değil fiyat vekili; tek dönem. `evidence/edgar.py` SEC EDGAR'dan delist (Form 25/15-12) tarihlerini önbellekli ve ≤10 req/s çeker; ancak EDGAR endeks (S&P) üyelik geçmişi ve delist edilmiş hisselerin fiyatını vermez, delist hisselerin CIK'i çağıran tarafından sağlanmalıdır ve ücretsiz kaynaklarda fiyatları çoğunlukla yoktur — bu yüzden hayatta kalma yanlılığı **kaldırılmış sayılmaz**, yalnız üyelik tablosu üretimi ve sınırı belgelenmiştir. Bu çıktı yatırım tavsiyesi değildir.

Topluluk kodları (pypbo, purgedcv, skfolio) yalnız çapraz kontrol fikri olarak düşünüldü; kod kopyalanmadı, yeni bağımlılık eklenmedi. Formüller makaleye göre ve birim testlerle (Monte Carlo ile E[max], T bağımlılığı, bilinen PSR değeri, gürültü→PBO≈0,5) doğrulandı: `tests/test_selection_bias_stats.py`.
