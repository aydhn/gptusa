from usa_signal_bot.regime_classification.foundation.final_closure_ingestion import ingest_final_closure_review_payload

def test_ingest_final_closure_review_payload_valid():
    payload = {
        "review_id": "rev_123",
        "context": {
            "context_id": "ctx_123",
            "final_artifacts_ready": True,
            "final_checks_passed": True,
            "freeze_seal_ready": True,
            "feature_factor_engine_final_closed": True,
            "ready_for_phase126": True,
            "research_data_only": True,
            "activation_allowed": False,
            "strategy_activation_allowed": False,
            "deployment_allowed": False,
            "active_paper_enabled": False,
            "broker_execution_enabled": False,
            "order_creation_enabled": False,
            "paper_state_mutation_enabled": False,
            "telegram_real_send_enabled": False,
            "scraping_enabled": False,
            "html_parse_enabled": False,
            "paid_api_enabled": False,
            "dashboard_enabled": False,
            "network_default_enabled": False,
            "produces_trade_signal": False,
            "produces_order_decision": False,
            "produces_portfolio_weights": False,
            "investment_advice": False
        },
        "engine_certificate": {
            "certificate_valid": True
        },
        "phase126_kickoff_gate": {
            "gate_passed": True
        }
    }

    res = ingest_final_closure_review_payload(payload)
    print(res.errors)
    assert res.valid_for_phase126 is True
    assert res.ready_for_phase126 is True

def test_ingest_final_closure_review_payload_invalid_activation():
    payload = {
        "review_id": "rev_123",
        "context": {
            "context_id": "ctx_123",
            "final_artifacts_ready": True,
            "final_checks_passed": True,
            "freeze_seal_ready": True,
            "feature_factor_engine_final_closed": True,
            "ready_for_phase126": True,
            "research_data_only": True,
            "activation_allowed": True, # invalid
            "produces_trade_signal": False
        },
        "engine_certificate": {
            "certificate_valid": True
        },
        "phase126_kickoff_gate": {
            "gate_passed": True
        }
    }

    res = ingest_final_closure_review_payload(payload)
    assert res.valid_for_phase126 is False
