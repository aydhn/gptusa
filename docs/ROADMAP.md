# Proje Yol Haritası (Roadmap)

Genel olarak proje, yaklaşık 160 fazlık bir üst seviye yol haritası düşünülerek aşama aşama büyütülecek şekilde tasarlanmıştır. Her faz küçük, geri alınabilir ve bağımsız modüllerden oluşur.

## Faz 1: Foundation (Temel Yapı) - Mevcut Aşama
* Projenin iskelet klasör ve modül yapısının oluşturulması.
* Config, Logging, Exception ve temel Utils mekanizmalarının inşası.
* Katı kuralların (broker routing, scraping, dashboard yasağı) belirlenmesi ve belgelendirilmesi.

## Faz 2: Config ve Environment Hardening
* Gelişmiş tip doğrulaması (ör. Pydantic entegrasyonuna doğru hazırlık).
* Güvenlik yapılandırmaları ve ortam (environment) değişkenlerinin tam oturtulması.

## Faz 3 ve Sonrası (Özet)
* **Faz 3:** Yfinance tabanlı ücretsiz veri çekme motorunun (Data Downloader) inşası.
* **Faz 4:** Finansal metrik ve teknik analiz (Features) hesaplama pipeline'ı.
* **Faz 5:** Kural tabanlı ilk alım-satım stratejisi tasarımı.
* **Faz 6:** Basit Vectorized Backtest altyapısı.
* **Faz 7:** Event-Driven Paper Trade simülasyon motoru.
* **Faz 8:** Telegram entegrasyonu ve Raporlama oluşturucuları.
* **Sonraki Fazlar:** Machine Learning tabanlı sinyal iyileştirmesi, Optimizer tasarımı, Portföy (Portfolio) optimizasyonu ve Rejim (Regimes) tespiti...
