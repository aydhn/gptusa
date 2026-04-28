# Geliştirme Kuralları (Development Rules)

Projenin her aşamasında uyulması zorunlu geliştirme kuralları şunlardır:

## Yasaklar
1. **Ücretli API Yok:** Asla openai, vb. API entegrasyonu ekleme.
2. **Web Scraping Yok:** İstisnasız DOM scraping, requests html parsing ekleme.
3. **Broker Order Routing Yok:** Canlı ya da demo piyasalara istek atan (Alpaca vb.) kod bloku dahi yazılamaz.
4. **Dashboard Yok:** FastAPI, Flask, Streamlit dahil edilemez.

## Mimari Prensipler
* **Önce test edilebilir kod:** İş mantığı CLI bağımsız olarak doğrudan test edilebilir şekilde izole edilmelidir.
* **Küçük adımlar:** Her faz küçük, net ve geri alınabilir olmalıdır.
* **Varsayım:** Kod ajanı varsayım yapabilir ancak yukarıdaki ana yasakları asla ihlal edemez.
* **Risk Yönetimi:** Risk yönetimi olmadan sinyal üretimi ileriki fazlarda aktif edilmeyecektir.
* **Backtest Güvenilirliği:** Backtest edilmemiş hiçbir strateji güvenilir sayılmaz ve paper trading engine'e verilmez.
* **ML Leakage:** Gelecek fazlarda eklenecek makine öğrenimi modellerinde "Data Leakage (Sızıntı)" kontrolü zorunludur.
* **Optimizer Out-of-Sample:** Optimizer sonuçları mutlaka out-of-sample test edilmeden raporlanmamalı ve kabul edilmemelidir.
