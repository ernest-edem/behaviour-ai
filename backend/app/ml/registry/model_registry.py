from typing import Dict, Optional, List

from app.ml.models.base_model import BaseModelInterface
from app.ml.common.exceptions import (
    ModelNotFoundError,
)


class ModelRegistry:
    """
    Central registry for ML models.

    Responsibilities:
    - Model registration
    - Active model management
    - Version tracking
    - Metadata lookup
    - Hot model swapping
    """

    def __init__(self) -> None:
        self._models: Dict[str, BaseModelInterface] = {}
        self._versions: Dict[str, str] = {}
        self._active_model_name: Optional[str] = None

    # ==================================================
    # REGISTRATION
    # ==================================================

    def register(
        self,
        name: str,
        model: BaseModelInterface,
        version: str = "1.0.0",
    ) -> None:

        self._models[name] = model
        self._versions[name] = version

        if self._active_model_name is None:
            self._active_model_name = name

    # ==================================================
    # RETRIEVAL
    # ==================================================

    def get(
        self,
        name: str,
    ) -> BaseModelInterface:

        model = self._models.get(name)

        if model is None:
            raise ModelNotFoundError(
                f"Model '{name}' is not registered."
            )

        return model

    def get_active_model(
        self,
    ) -> BaseModelInterface:

        if self._active_model_name is None:
            raise ModelNotFoundError(
                "No active model configured."
            )

        return self.get(
            self._active_model_name
        )

    # ==================================================
    # ACTIVE MODEL
    # ==================================================

    def set_active_model(
        self,
        name: str,
    ) -> None:

        if name not in self._models:
            raise ModelNotFoundError(
                f"Model '{name}' is not registered."
            )

        self._active_model_name = name

    def get_active_model_name(
        self,
    ) -> str:

        if self._active_model_name is None:
            raise ModelNotFoundError(
                "No active model configured."
            )

        return self._active_model_name

    # ==================================================
    # VERSIONING
    # ==================================================

    def get_version(
        self,
        name: str,
    ) -> str:

        if name not in self._versions:
            raise ModelNotFoundError(
                f"Version for model '{name}' not found."
            )

        return self._versions[name]

    # ==================================================
    # MODEL METADATA
    # ==================================================

    def get_model_metadata(
        self,
        name: str,
    ) -> Dict:

        model = self.get(name)

        try:
            return model.get_metadata()
        except Exception:
            return {
                "name": name,
                "version": self.get_version(name),
            }

    def get_active_model_metadata(
        self,
    ) -> Dict:

        model = self.get_active_model()

        try:
            return model.get_metadata()
        except Exception:
            return {
                "name": self.get_active_model_name(),
                "version": self.get_version(
                    self.get_active_model_name()
                ),
            }

    # ==================================================
    # LISTING
    # ==================================================

    def get_registered_models(
        self,
    ) -> Dict[str, str]:

        return dict(self._versions)

    def list_models(
        self,
    ) -> List[str]:

        return list(
            self._models.keys()
        )

    def is_registered(
        self,
        name: str,
    ) -> bool:

        return name in self._models

    def count(
        self,
    ) -> int:

        return len(self._models)

    # ==================================================
    # REMOVAL
    # ==================================================

    def unregister(
        self,
        name: str,
    ) -> None:

        if name not in self._models:
            return

        del self._models[name]
        del self._versions[name]

        if self._active_model_name == name:

            self._active_model_name = None

            if self._models:
                self._active_model_name = next(
                    iter(self._models)
                )

    def clear(
        self,
    ) -> None:

        self._models.clear()
        self._versions.clear()
        self._active_model_name = None

    # ==================================================
    # DEBUG
    # ==================================================

    def summary(
        self,
    ) -> Dict:

        return {
            "active_model": self._active_model_name,
            "registered_models": self.get_registered_models(),
            "count": self.count(),
        }


# ==================================================
# GLOBAL REGISTRY
# ==================================================

model_registry = ModelRegistry()

def safe_get_active_model(self):
    try:
        return self.get_active_model()
    except Exception:
        return None