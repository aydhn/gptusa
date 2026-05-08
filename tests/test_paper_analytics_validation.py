from usa_signal_bot.paper.paper_analytics_validation import validate_no_investment_advice_language_in_paper_analytics

def test_validation():
    report1 = validate_no_investment_advice_language_in_paper_analytics("This is absolutely kesin al!")
    assert not report1.valid

    report2 = validate_no_investment_advice_language_in_paper_analytics("This is a local simulation and not investment advice.")
    assert report2.valid
