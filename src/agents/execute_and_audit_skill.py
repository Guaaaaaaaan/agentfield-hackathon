from __future__ import annotations

from src.common.contracts import CollectionStrategy
from src.services.execution_service import ExecutionResult
from src.skills.execute_and_audit_skill import execute_and_audit_skill as _execute_and_audit_skill


def execute_and_audit_skill(strategy: CollectionStrategy) -> ExecutionResult:
    """Compatibility wrapper to keep agent import path stable."""
    return _execute_and_audit_skill(strategy)
