# Notification Templates

## Overview
Templates govern how Domain Objects (Scan Results, Candidate Selection, Risk Decisions) are formatted before string dispatch.

## Limitations and Language Filtering
Templates scrub strings corresponding to direct investment/trade advice (e.g., "kesin al", "garanti kâr") and apply standard chunking if the target messenger platform sets message length caps.

## Message Chunking
Messages exceeding `max_message_length` (e.g. 3500 bytes) will automatically be divided over sequentially numbered parts (`(1/2)`, `(2/2)`).

## Preview CLI
To preview how a particular template operates without enqueueing messages, use:
`python -m usa_signal_bot notification-template-preview --type scan_summary`
