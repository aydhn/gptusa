# Kanıt Hattı Durumu (2026-10-09)

**Gerçek piyasa verisiyle sonuç YOKTUR.** Ortamda `yfinance` kurulu değil ve veri indirme sizin onayınızı gerektiriyor; bu yüzden boru hattı sentetik, tohumlu rastgele yürüyüş verisiyle doğrulandı. Sentetik sonuç strateji kanıtı değildir: yalnız hattın sızıntısız, maliyetli ve deterministik çalıştığını gösterir.

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

## Gerçek veriyle çalıştırma (sizin adımınız)
1. `pip install -r requirements.txt` ve ücretsiz kaynaktan (bkz. `FREE_DATA_SOURCES.md`) her sembol için `data/prices/<SYMBOL>.csv` (Date, Adj Close) hazırlayın; mümkünse `symbol,start,end` üyelik tablosu ve `splits.csv` ekleyin.
2. `python -m usa_signal_bot evidence-run --source csv --csv-dir data/prices --memberships data/memberships.csv --write`
3. Üyelik tablosu yoksa rapor "hayatta kalma yanlılığı" uyarısı basar; bu durumda sonuç iyimserdir.
