import pytest

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
