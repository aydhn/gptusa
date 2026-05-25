
from typing import Any
from usa_signal_bot.core.enums import DataProviderName, DataProviderKind, DataProviderCapability, DataProviderPermission
from usa_signal_bot.data_providers.phase106_models import ProviderAdapterSpec

class BaseDataProvider:
    provider_name: DataProviderName
    provider_kind: DataProviderKind
    skeleton_only: bool = True

    def adapter_spec(self) -> ProviderAdapterSpec:
        raise NotImplementedError()

    def health_metadata(self) -> dict[str, Any]:
        return {"status": "ok", "skeleton_only": self.skeleton_only}

    def capabilities(self) -> list[DataProviderCapability]:
        return []

    def permissions(self) -> list[DataProviderPermission]:
        return [DataProviderPermission.METADATA_ONLY]

    def validate_request(self, request: Any) -> list[str]:
        return []

    def execute_metadata_only(self, request: Any) -> dict[str, Any]:
        return {}
