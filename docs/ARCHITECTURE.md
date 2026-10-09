# Mimari Vizyon (Architecture)

## Genel Mimari Vizyonu
USA Signal Bot, modüler, test edilebilir ve genişletilebilir bir lokal algoritmik ticaret ve sinyal araştırma platformudur. Amacı tamamen ücretsiz veri ve lokal hesaplama gücü ile hisse senedi ve ETF pazarını analiz edip kağıt üzerinde alım-satım performansı (paper trading) ölçmektir.

Sistem, basit CLI tabanlı bir yapıya sahiptir. Ağır web arayüzlerinden, bulut servislerinden ve bağımlılıklardan kaçınır.

## Temel İş Akışı
Mimari genel veri işleme boru hattı (pipeline) şu şekildedir:
**Data → Features → Strategies → Backtest → Paper → Reports → Telegram**

1. **Data:** Yalnızca `yfinance` gibi ücretsiz araçlarla statik piyasa verisini indirir ve önbelleğe (cache) alır.
2. **Features:** Finansal göstergeler ve algoritmik özellikler hesaplar.
3. **Strategies:** Önceden tanımlı kural kümeleriyle alım-satım sinyalleri oluşturur.
4. **Backtest:** Tarihsel verilerle stratejileri test eder, risk limitlerini kontrol eder.
5. **Paper:** Güncel piyasa kapanış veya periyodik verilerle kağıt (sanal) emir simülasyonu çalıştırır.
6. **Reports:** Sonuçları text/csv formatında lokal klasörlerde özetler.
7. **Telegram:** Üretilen rapor ve uyarıları bot olarak kullanıcıya push mesajı ile bildirir.

## Mimari Sınırlar ve Sebepleri
*   **Broker Order Routing Kesinlikle Yasaktır:** Proje, üretim ortamında mali kayıpları engellemek, risk düzeyini minimize etmek ve saf araştırma odaklı kalmak amacıyla broker entegrasyonlarını desteklemez. Sistem her zaman lokal çalışır.
*   **Web Scraping Kesinlikle Yasaktır:** Kurumsal veri akışlarının tutarlılığı ve yasallığı açısından DOM kazıma, Selenium, BeautifulSoup gibi yöntemler kullanılmaz. Yalnızca kütüphaneler aracılığıyla temiz API'lerden veri çekilir.
*   **Dashboard Yok:** Sunucu maliyetleri ve bağımlılıklarını sıfıra indirmek için Dashboard yapılmamış, bunun yerine log dosyaları ve Telegram bilgilendirmesi tercih edilmiştir.

## Paket Sınırları (Aşama 1 refactor sonrası)
*   **`core`**: enum/exception/config/types/paths. Hiçbir üst paketten import etmez. Genel API `core/__init__.py` (`SignalAction`, `DataProviderName`, `RunLockScope`, `USASignalBotError`). `core/_recovered_enums.py` ve `core/_recovered_exceptions.py` git geçmişinden geri yüklenen tanımlardır (bkz. commit `079f840`); `enums.py`/`exceptions.py` sonunda `import *` ile birleşir. Yeni enum/exception doğrudan `enums.py`/`exceptions.py` içine eklenir.
*   **`data`, `features`**: paylaşılan veri/indikatör şekilleri; `__init__` genel API sunar. Somut boru hatları `data_providers`, `feature_engine` altındadır.
*   **`app`**: CLI. Tüm komut kayıt fonksiyonları `app/cli.py::_command_registrars()` listesindedir; yeni `setup_*_cli` buraya eklenir (komut adı çakışması argparse hatası verir).
*   **`paper_common`**: ~30 `paper_*` / `pre_paper_*` / `local_paper_admission_simulator_*` paketinin ortak IO (`io.py`) ve doğrulama tabanı (`validation_types.py`). Bu paketler saf dossier/gate/replay katmanlarıdır; emir üretmez. Özel encoder veya testte patch'lenen store'lar bilerek yerel bırakılmıştır.
*   **Yasak yapılar**: import anında kendi kaynak dosyasına yazan kod, `scripts/` altında çekirdek modülleri yeniden yazan yama betikleri. `tests/test_all_modules_parse.py` tüm kaynakların derlenebildiğini doğrular.
*   Faz geçmişi için `docs/PHASES_INDEX.md`; ücretsiz veri kaynakları karşılaştırması `docs/FREE_DATA_SOURCES.md`.

## Araştırma Hattı Paketleri (Aşama 2-4)
*   **`evidence`**: point-in-time evren, düzeltilmiş fiyat/split doğrulama, maliyetli walk-forward, bootstrap güven aralıklı OOS raporu. CLI: `evidence-run`. Durum ve gerçek veri talimatı: `EVIDENCE_REPORT_2026-10-09.md`.
*   **`decision`**: tek karar hattı (sinyal → rejim ağırlığı → ters-volatilite boyutlama → risk limitleri → çıkış kuralları) ve yerel simüle paper ledger (`ORDER_ROUTING_ENABLED = False`, `EXECUTION_MODE = "local_paper_only"`). `sessions.py`: NYSE tatil/erken kapanış/DST-uyumlu seans takvimi (America/New_York). CLI: `decision-simulate`.
*   **`ml_loop`**: purged K-fold + embargo, sızıntı korumaları, JSON model registry, promosyon kapısı. Kapı yalnız `ELIGIBLE` yapar; `APPROVED_FOR_RESEARCH` için adı ve notu olan insan onayı (`ml-loop-approve`) gerekir; `activation_allowed` hiçbir yolla True olmaz. CLI: `ml-loop-train`, `ml-loop-approve`.
