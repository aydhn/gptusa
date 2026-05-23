# PRE-PAPER LOCAL RUNTIME MAP REPLAY

## Amacı
Bu sistemin amacı paper_safe_dossier içerisinde bulunan runtime_map'i metadata-only olarak tekrar replay etmek ve execution path'inde herhangi bir risk olmadığını kanıtlamaktır.

## Mantığı
- Read-only, preview ve dry-run route'ları safe metadata olarak kabul edilir.
- Write, order, broker, config, telegram, active paper ve paper admission izinleri tehlikeli (dangerous) kabul edilir ve bunların reddedildiği doğrulanır.
- Eğer tehlikeli bir route `ALLOWED` görünüyorsa, replay süreci anında `BLOCK` veya `FAILED` kararı üretir.

## CLI Örnekleri
```bash
python -m usa_signal_bot --runtime-map-replay-plan
python -m usa_signal_bot --runtime-map-replay-run
python -m usa_signal_bot --runtime-map-replay-analyze
```
