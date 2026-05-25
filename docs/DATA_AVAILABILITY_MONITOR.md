# Data Availability Monitor

## Overview
Checks if the local cache or providers have coverage for symbols.

## Components
- Cache Availability Checker
- Provider Availability Checker
- Symbol Coverage Monitor
- Computes `coverage_ratio` and missing/partial states.
- Does **not** perform network requests. Operates offline.
