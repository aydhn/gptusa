from typing import Any

def aggregate_gate_evaluations(gates: list[dict[str, Any]]) -> dict[str, Any]:
    return {"total": len(gates), "counts": count_gate_statuses(gates)}

def count_gate_statuses(gates: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"PASS": 0, "WARNING": 0, "FAIL": 0}
    for g in gates:
        st = g.get("status", "FAIL")
        counts[st] = counts.get(st, 0) + 1
    return counts

def gate_failures(gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [g for g in gates if g.get("status") == "FAIL"]

def gate_warnings(gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [g for g in gates if g.get("status") == "WARNING"]

def gates_block_promotion(gates: list[dict[str, Any]]) -> bool:
    for g in gates:
        if g.get("status") == "FAIL" and g.get("name", "") == "NO_LEAKAGE":
            return True
    return False

def gate_aggregation_to_text(summary: dict[str, Any]) -> str:
    return f"Gate Aggregation Summary: {summary}"
