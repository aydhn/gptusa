import sys
import types

import pytest

# Safety net against test-collection pollution: a test module that assigns a
# non-module object (MagicMock, stub class, ...) to sys.modules for a project or
# core third-party package at import time poisons every module imported later
# in the same pytest process (e.g. dataclasses.asdict then deep-copies leaked
# MagicMocks, which made the full suite hang). Such a file now fails at
# collection with a clear message and the original sys.modules entries are
# restored. Use monkeypatch / patch.dict(sys.modules, ...) inside a test instead.
_GUARDED_MODULE_PREFIXES = ("usa_signal_bot", "pandas", "numpy", "yfinance", "yaml")


def _guarded_entries():
    return {
        name: mod
        for name, mod in list(sys.modules.items())
        if name.split(".", 1)[0] in _GUARDED_MODULE_PREFIXES
    }


@pytest.hookimpl(hookwrapper=True)
def pytest_make_collect_report(collector):
    if not isinstance(collector, pytest.Module):
        yield
        return
    before = _guarded_entries()
    outcome = yield
    after = _guarded_entries()
    leaked = sorted(
        name
        for name, mod in after.items()
        if mod is not None
        and not isinstance(mod, types.ModuleType)
        and before.get(name) is not mod
    )
    if not leaked:
        return
    for name in leaked:
        if name in before:
            sys.modules[name] = before[name]
        else:
            sys.modules.pop(name, None)
    # Project modules first imported while the fake was installed captured it;
    # drop them so later test files re-import them against the real modules.
    for name in after:
        if name not in before and name.startswith("usa_signal_bot"):
            sys.modules.pop(name, None)
    outcome.force_result(
        pytest.CollectReport(
            collector.nodeid,
            "failed",
            longrepr=(
                f"{collector.nodeid} replaced sys.modules entries with non-module "
                f"objects at import time: {', '.join(leaked)}. This leaks into other "
                "test files; use monkeypatch or patch.dict(sys.modules, ...) inside "
                "the test instead. (Entries restored.)"
            ),
            result=[],
        )
    )


@pytest.fixture
def mocker(pytestconfig):
    try:
        from pytest_mock import MockerFixture
        return MockerFixture(pytestconfig)
    except ImportError:
        class MockObj:
            def __init__(self, spec=None):
                if spec:
                    self.__class__ = spec
            def __call__(self, *args, **kwargs):
                return self
            def __getattr__(self, name):
                return MockObj()
        class Mocker:
            Mock = MockObj
            def patch(self, *args, **kwargs):
                return MockObj()
        return Mocker()
