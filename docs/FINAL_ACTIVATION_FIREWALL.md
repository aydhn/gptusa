# Final Activation Firewall
Denies all activation attempts and overrides any permissions ensuring no live or active paper deployment takes place.
## Commands
`python -m usa_signal_bot activation-firewall-rules --write`
`python -m usa_signal_bot activation-firewall-evaluate --attempt-type enable_active_paper --write`
`python -m usa_signal_bot activation-attempt-simulate --write`
