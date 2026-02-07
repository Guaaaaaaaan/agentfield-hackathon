from __future__ import annotations

from src.common.contracts import CollectionStrategy
from src.services.execution_service import ExecutionResult, execute_collection_action


def execute_and_audit_skill(strategy: CollectionStrategy) -> ExecutionResult:
    """Execute strategy and return a structured result for stable audit assembly."""
    return execute_collection_action(strategy)
