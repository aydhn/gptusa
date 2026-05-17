# Failure Mode Mining

This module mines repeated failure signatures and clusters. It classifies failures into modes like REGIME_MISMATCH or HIGH_SLIPPAGE. It provides local hints but does not prove causality or provide trading advice.

CLI commands:
python -m usa_signal_bot failure-signature-mining --min-count 3
python -m usa_signal_bot failure-cluster-ranking
