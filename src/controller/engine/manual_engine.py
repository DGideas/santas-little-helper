from src.data.enums import SantasOperationEngine

from .base_engine import BaseEngine


class ManualEngine(BaseEngine):
    __ENGINE__ = SantasOperationEngine.ENGINE_MANUAL
