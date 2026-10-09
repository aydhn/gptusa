# Ücretsiz Veri Kaynakları Karşılaştırması (Aşama 0)

Erişim tarihi (tüm satırlar): 2026-10-09. Sayılar yalnız kaynak sayfasında görülenlerdir; görülemeyen "doğrulanamadı" yazılmıştır. Bu belge yatırım tavsiyesi değildir; yalnız veri kaynağı değerlendirmesidir. Proje kuralı: scraping/HTML parsing yok, ücretli API yok.

## Karşılaştırma

| Kaynak | Kapsam | Günlük derinlik | Gün içi tarihsel derinlik | Rate limit | Lisans / kullanım notu | Scraping gerekir mi | Öneri |
|---|---|---|---|---|---|---|---|
| yfinance (Yahoo Finance) | ABD hisse, ETF, endeks vb.; Yahoo'nun gayriresmî API'sinden okur | Doğrulanamadı (resmi sayı yok) | 1m/5m/15m/1h için derinlik sınırı resmi dokümandan doğrulanamadı; pratikte kısa pencereler beklenir, kodda sınır testi yapılmalı | Doğrulanamadı (yayımlanmış resmi limit yok) | Kütüphane Apache-2.0; proje kendini Yahoo ile ilgisiz, araştırma/eğitim amaçlı ve Yahoo API'sini kişisel kullanım için olarak tanımlıyor; veri hakları Yahoo şartlarına bağlı | Hayır (API çağrısı), ancak resmî olmayan uç nokta; kırılganlık riski | Mevcut yedek/prototip kaynağı; kişisel araştırma ile sınırlı, veri yeniden dağıtılmaz |
| Stooq | Çok varlıklı küresel günlük/geçmiş veri; toplu CSV/ZIP anlık görüntüleri | Doğrulanamadı | Doğrulanamadı | Günlük istek kotası var (3. taraf kaynaklar); API anahtarı gerektiği bildiriliyor (CAPTCHA ile); kesin sayı doğrulanamadı | Resmi ToS metni doğrulanamadı; kullanmadan önce stooq.com şartları elle okunmalı | Toplu `db` indirmesi var, scraping gerekmez; CAPTCHA'lı anahtar adımı otomatikleştirilmemeli (CAPTCHA aşılmaz) | Lisans doğrulanana kadar yalnız manuel indirilen yerel CSV olarak, düşük öncelik |
| Alpha Vantage (ücretsiz) | Hisse, FX, kripto, göstergeler | Doğrulanamadı | Doğrulanamadı | Günde 25 istek; dakika limiti sayfada belirtilmemiş | ABD gerçek zamanlı/15 dk gecikmeli veri ücretli plan gerektirir; doğrulanmış açık kaynak/eğitim projeleri için sınırsız istek bildirilmiş | Hayır | Günde 25 istek geniş evren için yetersiz; yalnız küçük doğrulama örnekleri |
| Polygon.io (şimdi Massive; /pricing yönlendiriyor) | ABD hisse ve diğer pazarlar | 2 yıl (ücretsiz Basic) | Dakika agregaları listeli ama plan "End of Day" olarak tanımlı; gün içi erişim net doğrulanamadı | Dakikada 5 çağrı | Lisans metni doğrulanamadı | Hayır | Sığ geçmiş ve düşük kota; yalnız çapraz doğrulama |
| Tiingo (ücretsiz Starter) | Hisse/ETF, temel veriler | Fiyat geçmişi 30+ yıl; temel veri 5 yıl | IEX gün içi erişimi bu planda doğrulanamadı | Saatte 50, günde 1.000 istek; ayda 500 benzersiz sembol; ayda 1 GB | "Internal Use Only": yalnız kişisel kullanım, gösterme/paylaşma yok | Hayır | Günlük veri için en güçlü ücretsiz aday; kota evreni sınırlar (500 sembol/ay) |
| SEC EDGAR | Şirket dosyaları, XBRL temel veriler (fiyat verisi değil) | Dosyalama geçmişi (fiyat yok) | Yok | Adil erişim: saniyede en fazla 10 istek (makine sayısından bağımsız) | Resmi API; anahtar/kimlik doğrulama yok; aşırı istekte IP engellenebilir; toplu `companyfacts.zip` ve `submissions.zip` gecelik yenilenir | Hayır | Temel veri/olay metadatası için ilk tercih; toplu ZIP ile istek azalt |
| FRED | Makroekonomik seriler | Seriye bağlı | Yok | Sayfalarda limit belirtilmemiş: doğrulanamadı | Her istek API anahtarı gerektirir (ücretsiz hesapla alınır); kullanım şartları sayfası ayrıca okunmalı | Hayır | Makro/rejim girdileri için uygun; anahtar `config/runtime.env` içinde, commit edilmez |

### User-Agent notu (EDGAR)
SEC geliştirici sayfaları bu fetch'te açık bir User-Agent kuralı göstermedi; SEC'in Developer FAQ'ı ayrıca kontrol edilmeli. Doğrulanamadı; yine de kimlik belirten (iletişim içeren) bir User-Agent göndermek makul önlemdir.

## Kaynaklar (erişim 2026-10-09)

| Kaynak | URL |
|---|---|
| yfinance | https://github.com/ranaroussi/yfinance ; https://ranaroussi.github.io/yfinance/reference/api/yfinance.Ticker.history.html (interval sınırları bu sayfada yok) |
| Stooq | https://stooq.com/db/h/ (fetch boş döndü); üçüncü taraf: https://providers.apievangelist.com/providers/stooq/ |
| Alpha Vantage | https://alphavantage.co/support/ |
| Polygon.io / Massive | https://massive.com/pricing (polygon.io/pricing 301 ile yönlendirir) |
| Tiingo | https://www.tiingo.com/about/pricing |
| SEC EDGAR | https://www.sec.gov/search-filings/edgar-application-programming-interfaces ; https://www.sec.gov/about/developer-resources |
| FRED | https://fred.stlouisfed.org/docs/api/api_key.html ; https://fred.stlouisfed.org/docs/api/fred/v2/index.html |

## Öneri (kombinasyon ve sınırlar)

- Günlük fiyat: Tiingo (kişisel kullanım, 500 sembol/ay) birincil; yfinance yerel önbellekle yedek/çapraz doğrulama. Stooq lisansı doğrulanana kadar kullanma.
- Gün içi: ücretsiz kaynaklarda güvenilir doğrulanmış derin tarihsel gün içi veri bulunamadı; yfinance ile yalnız kısa pencere biriktirilip yerel depoya yazılarak kendi geçmişin oluşturulmalı. Derinlik sınırı gün içi araştırmanın ana kısıtıdır.
- Temel veri/olaylar: SEC EDGAR toplu ZIP; makro: FRED.
- Survivorship bias: ücretsiz kaynaklar çoğunlukla bugün listelenen sembolleri verir; delisted hisseler eksik olabilir (doğrulanamadı, kaynak bazında test et). Sonuçlar bu önyargıyla işaretlenmeli.
- Düzeltilmiş fiyat güvenilirliği: split/temettü düzeltmeleri kaynaktan kaynağa farklı olabilir; iki kaynakla karşılaştır, `corporate_actions` paketiyle tutarlılık kontrolü yap.
- Tüm kaynaklar kişisel/araştırma kullanımıdır; veri yeniden dağıtılmaz, anahtarlar commit edilmez, kota aşımı için önbellek ve backoff kullanılır.
