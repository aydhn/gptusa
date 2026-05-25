import abc
from typing import Any, Dict

class DataProviderAdapterBase(abc.ABC):
    @abc.abstractmethod
    def adapter_spec(self) -> Dict[str, Any]:
        pass

    @abc.abstractmethod
    def validate_contract(self) -> list[str]:
        pass
