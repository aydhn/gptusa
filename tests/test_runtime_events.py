import pytest
from usa_signal_bot.runtime.runtime_events import (
    create_runtime_event, runtime_event_to_dict, filter_runtime_events,
    write_runtime_events_jsonl, read_runtime_events_jsonl, runtime_events_to_text
)
from usa_signal_bot.core.enums import RuntimeEventType, PipelineStepName

def test_runtime_events(tmp_path):
    ev = create_runtime_event("run1", RuntimeEventType.RUN_STARTED, "test")
    assert ev.run_id == "run1"
    assert ev.event_type == RuntimeEventType.RUN_STARTED

    d = runtime_event_to_dict(ev)
    assert d["run_id"] == "run1"

    ev2 = create_runtime_event("run1", RuntimeEventType.STEP_STARTED, "test", step_name=PipelineStepName.PREFLIGHT)

    filtered = filter_runtime_events([ev, ev2], event_type=RuntimeEventType.STEP_STARTED)
    assert len(filtered) == 1

    filtered = filter_runtime_events([ev, ev2], step_name=PipelineStepName.PREFLIGHT)
    assert len(filtered) == 1

    p = tmp_path / "events.jsonl"
    write_runtime_events_jsonl(p, [ev, ev2])
    data = read_runtime_events_jsonl(p)
    assert len(data) == 2

    text = runtime_events_to_text([ev, ev2])
    assert "run_started" in text
