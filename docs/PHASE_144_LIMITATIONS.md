# PHASE_144_LIMITATIONS

## Limitations
- **No Real-Time Capabilities:** Phase 144 cannot monitor live data feeds.
- **No Heavy ML Frameworks:** The drift calculations rely on standard library and lightweight libraries like `pandas`, actively avoiding heavy dependencies like `scikit-learn` or `torch` to maintain the boundary requirements.
- **Diagnostic Only:** The drift metrics generated are diagnostic tools for researchers. They are mathematically incapable of executing trades or updating the active strategy engine.
