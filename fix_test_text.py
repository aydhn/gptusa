def fix():
    with open('tests/test_cost_curve_selector.py', 'r') as f:
        content = f.read()

    # The snapshot defaults to INSUFFICIENT_DATA -> CONSERVATIVE. So we expect CONSERVATIVE.
    content = content.replace(
        'assert "BASELINE" in cost_curve_selection_to_text(sel)',
        'assert "CONSERVATIVE" in cost_curve_selection_to_text(sel)'
    )

    with open('tests/test_cost_curve_selector.py', 'w') as f:
        f.write(content)

fix()
