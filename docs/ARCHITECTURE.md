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
