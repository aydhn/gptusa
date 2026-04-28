# USA Signal Bot

## Proje Adı
USA Signal Bot

## Amaç
USA hisse ve ETF evreninde fırsat arayan lokal bir sinyal botu geliştirmek.
Bu proje, saatte birkaç kaliteli sinyal üreten, risk kontrollü, ölçülebilir, backtest edilebilir ve geliştirilebilir bir araştırma/paper trade sistemi oluşturmayı hedefler.

## Kritik Sınırlar
- **Ücretli Servis Yok:** OpenAI API, Twitter/X API, ücretli market/haber/broker API, cloud, veritabanı kullanımı yasaktır. Tamamen lokal ve ücretsizdir.
- **Canlı Emir İletimi Yok:** Gerçek emir, demo broker emri, API üzerinden borsaya emir iletimi yapılmaz. Sadece lokal paper broker simülasyonu mevcuttur.
- **Web Scraping Yok:** HTML kazıma, BeautifulSoup, Selenium, Playwright, Scrapy kullanılamaz. Sadece resmi Python kütüphaneleri ve ücretsiz veri erişim yöntemleri geçerlidir.
- **Dashboard Yok:** Streamlit, Dash, Flask/FastAPI vb. dashboard arayüzleri olmayacaktır. Sadece CLI, Telegram, loglar ve lokal dosya raporları kullanılacaktır.

## Felsefe
Tamamen lokal, ücretsiz araçlar (yfinance vb.) ve açık kaynak Python kütüphaneleri kullanılarak çalışacak bir mimari oluşturmak.

## Kapsam (Phase 1)
Bu faz, projenin temel yapı taşlarını ve sınırlarını oluşturur (Foundation):
- Temiz klasör yapısı
- Python paket iskeleti
- Config ve Path yönetimi
- Logging altyapısı
- Global sabitler ve istisnalar
- CLI ve Smoke Test altyapısı

> **Not:** Bu aşamada henüz canlı veri çekme, strateji, backtest, ML, optimizer, Telegram etkileşimi veya paper trade motoru bulunmamaktadır. Bunlar gelecek fazların konusudur.

## Kurulum
```bash
pip install -r requirements.txt
```

## Kullanım
```bash
python -m usa_signal_bot smoke
python -m usa_signal_bot show-config
python -m usa_signal_bot show-paths
```

## Sonraki Fazlarda Gelecek Modüller
- Veri indirme altyapısı (yfinance vb.)
- Feature Engineering ve Sinyal Stratejileri
- Backtest motoru
- Paper Trade simülasyon motoru
- Optimizasyon ve ML modelleri (GPU bağımsız olarak başlayıp ilerleyen aşamalarda genişletilecek)
- Telegram Bildirim Entegrasyonu
