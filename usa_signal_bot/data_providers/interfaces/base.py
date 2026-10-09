import abc
from typing import Any, Dict

class DataProviderAdapterBase(abc.ABC):
    @abc.abstractmethod
    def adapter_spec(self) -> Dict[str, Any]:
        pass

    @abc.abstractmethod
    def validate_contract(self) -> list[str]:
        pass


# --- Definitions recovered from git history (deleted by an accidental overwrite) ---
from usa_signal_bot.core.enums import DataProviderName
from usa_signal_bot.core.enums import DataProviderKind
from usa_signal_bot.core.enums import DataProviderCapability
from usa_signal_bot.core.enums import DataProviderPermission
from usa_signal_bot.data_providers.phase106_models import ProviderAdapterSpec


class BaseDataProvider:
    provider_name: 'DataProviderName'
    provider_kind: 'DataProviderKind'
    skeleton_only: 'bool' = True

    def adapter_spec(self) -> 'ProviderAdapterSpec':
        raise NotImplementedError()

    def health_metadata(self) -> 'dict[str, Any]':
        return {'status': 'ok', 'skeleton_only': self.skeleton_only}

    def capabilities(self) -> 'list[DataProviderCapability]':
        return []

    def permissions(self) -> 'list[DataProviderPermission]':
        return [DataProviderPermission.METADATA_ONLY]

    def validate_request(self, request: 'Any') -> 'list[str]':
        return []

    def execute_metadata_only(self, request: 'Any') -> 'dict[str, Any]':
        return {}
