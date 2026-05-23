# NON-EXECUTION SEAL INTEGRITY AUDIT

## Amacı
Phase 93'te üretilen NonExecutionAcceptanceSeal nesnesinin değiştirilmediğini ve içinde beyan edilen "execution yok" garantilerinin geçerliliğini koruduğunu doğrulamaktır.

## Mantığı
- Kaydedilen `seal_hash` yeniden hesaplanarak uyumluluğu kontrol edilir (`seal_hash_matches`).
- `confirmed_non_execution`, `confirmed_no_broker`, vb. gereksinimlerin `True` olduğu test edilir.
- `seal_is_metadata_only` flag'inin `True` olduğu zorunlu kılınır.

## CLI Örnekleri
```bash
python -m usa_signal_bot --seal-integrity-audit
python -m usa_signal_bot --seal-integrity-validate
```
