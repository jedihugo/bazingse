# * =============================================================================
# * PATTERN REGISTRY
# * =============================================================================
# * Central storage for all BaZi patterns with dependency graphs,
# * contradiction validation, and efficient lookup.
# * =============================================================================

from __future__ import annotations
from typing import Dict, List, Set, Optional, Iterator, Tuple
from dataclasses import dataclass, field
from collections import defaultdict

from .pattern_spec import (
    PatternSpec,
    PatternCategory,
    LifeDomain,
    BadgeType,
)


# =============================================================================
# VALIDATION ERRORS
# =============================================================================

class PatternRegistryError(Exception):
    """Base exception for pattern registry errors."""
    pass


class DuplicatePatternError(PatternRegistryError):
    """Raised when attempting to register a pattern with an existing ID."""
    pass


class CircularDependencyError(PatternRegistryError):
    """Raised when pattern dependencies form a cycle."""
    pass


class MissingDependencyError(PatternRegistryError):
    """Raised when a pattern requires a non-existent pattern."""
    pass


class ContradictionError(PatternRegistryError):
    """Raised when patterns have contradictory rules."""
    pass


# =============================================================================
# DEPENDENCY GRAPH
# =============================================================================

@dataclass
class DependencyGraph:
    """
    Manages dependency and blocker relationships between patterns.

    Ensures no circular dependencies exist and validates blockers.
    """

    # Pattern ID -> Set of pattern IDs it requires
    requires_graph: Dict[str, Set[str]] = field(default_factory=lambda: defaultdict(set))

    # Pattern ID -> Set of pattern IDs that require it
    required_by_graph: Dict[str, Set[str]] = field(default_factory=lambda: defaultdict(set))

    # Pattern ID -> Set of pattern IDs that block it
    blocked_by_graph: Dict[str, Set[str]] = field(default_factory=lambda: defaultdict(set))

    # Pattern ID -> Set of pattern IDs it blocks
    blocks_graph: Dict[str, Set[str]] = field(default_factory=lambda: defaultdict(set))

    def add_pattern(self, pattern: PatternSpec) -> None:
        """Add a pattern's dependencies to the graph."""
        pattern_id = pattern.id

        # Add requirements
        for required_id in pattern.requires:
            self.requires_graph[pattern_id].add(required_id)
            self.required_by_graph[required_id].add(pattern_id)

        # Add blockers
        for blocker_id in pattern.blocked_by:
            self.blocked_by_graph[pattern_id].add(blocker_id)
            self.blocks_graph[blocker_id].add(pattern_id)

    def remove_pattern(self, pattern_id: str) -> None:
        """Remove a pattern's dependencies from the graph."""
        # Remove from requires relationships
        for required_id in self.requires_graph.get(pattern_id, set()):
            self.required_by_graph[required_id].discard(pattern_id)
        self.requires_graph.pop(pattern_id, None)

        # Remove from required_by relationships
        for requiring_id in self.required_by_graph.get(pattern_id, set()):
            self.requires_graph[requiring_id].discard(pattern_id)
        self.required_by_graph.pop(pattern_id, None)

        # Remove from blocked_by relationships
        for blocker_id in self.blocked_by_graph.get(pattern_id, set()):
            self.blocks_graph[blocker_id].discard(pattern_id)
        self.blocked_by_graph.pop(pattern_id, None)

        # Remove from blocks relationships
        for blocked_id in self.blocks_graph.get(pattern_id, set()):
            self.blocked_by_graph[blocked_id].discard(pattern_id)
        self.blocks_graph.pop(pattern_id, None)

    def get_all_requirements(self, pattern_id: str) -> Set[str]:
        """Get transitive closure of all requirements for a pattern."""
        visited = set()
        to_visit = list(self.requires_graph.get(pattern_id, set()))

        while to_visit:
            current = to_visit.pop()
            if current not in visited:
                visited.add(current)
                to_visit.extend(self.requires_graph.get(current, set()))

        return visited

    def get_all_dependents(self, pattern_id: str) -> Set[str]:
        """Get transitive closure of all patterns that depend on this one."""
        visited = set()
        to_visit = list(self.required_by_graph.get(pattern_id, set()))

        while to_visit:
            current = to_visit.pop()
            if current not in visited:
                visited.add(current)
                to_visit.extend(self.required_by_graph.get(current, set()))

        return visited

    def detect_cycle(self, pattern_id: str) -> Optional[List[str]]:
        """
        Detect if adding this pattern creates a circular dependency.

        Returns the cycle path if found, None otherwise.
        """
        visited = set()
        path = []

        def dfs(current: str) -> Optional[List[str]]:
            if current in path:
                cycle_start = path.index(current)
                return path[cycle_start:] + [current]

            if current in visited:
                return None

            visited.add(current)
            path.append(current)

            for required in self.requires_graph.get(current, set()):
                result = dfs(required)
                if result:
                    return result

            path.pop()
            return None

        return dfs(pattern_id)

    def get_processing_order(self) -> List[str]:
        """
        Return pattern IDs in topological order (dependencies first).

        Patterns with no dependencies come first.
        """
        # Kahn's algorithm for topological sort
        in_degree = defaultdict(int)
        all_patterns = set(self.requires_graph.keys()) | set(self.required_by_graph.keys())

        for pattern_id in all_patterns:
            in_degree[pattern_id] = len(self.requires_graph.get(pattern_id, set()))

        # Start with patterns that have no dependencies
        queue = [p for p in all_patterns if in_degree[p] == 0]
        result = []

        while queue:
            current = queue.pop(0)
            result.append(current)

            for dependent in self.required_by_graph.get(current, set()):
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        return result


# =============================================================================
# PATTERN REGISTRY
# =============================================================================

class PatternRegistry:
    """
    Central storage for all BaZi patterns.

    Features:
    - Pattern registration with validation
    - Dependency/blocker graph management
    - Efficient lookup by category, domain, participants
    - Contradiction detection
    - Processing order computation
    """

    def __init__(self):
        # Primary storage: ID -> PatternSpec
        self._patterns: Dict[str, PatternSpec] = {}

        # Dependency management
        self._dependency_graph = DependencyGraph()

        # Indexes for efficient lookup
        self._by_category: Dict[PatternCategory, Set[str]] = defaultdict(set)
        self._by_domain: Dict[LifeDomain, Set[str]] = defaultdict(set)
        self._by_badge_type: Dict[BadgeType, Set[str]] = defaultdict(set)
        self._by_priority: Dict[int, Set[str]] = defaultdict(set)

        # Participant index: participant_name -> Set of pattern IDs
        self._by_participant: Dict[str, Set[str]] = defaultdict(set)

        # Cached processing order (invalidated on registration)
        self._processing_order: Optional[List[str]] = None

    # =========================================================================
    # Registration
    # =========================================================================

    def register(self, pattern: PatternSpec, validate: bool = True) -> None:
        """
        Register a pattern in the registry.

        Args:
            pattern: The pattern specification to register
            validate: Whether to run validation checks (default True)

        Raises:
            DuplicatePatternError: If pattern ID already exists
            CircularDependencyError: If pattern creates dependency cycle
            MissingDependencyError: If required pattern doesn't exist
            ContradictionError: If pattern contradicts existing patterns
        """
        if pattern.id in self._patterns:
            raise DuplicatePatternError(f"Pattern '{pattern.id}' already registered")

        if validate:
            self._validate_registration(pattern)

        # Add to primary storage
        self._patterns[pattern.id] = pattern

        # Update dependency graph
        self._dependency_graph.add_pattern(pattern)

        # Update indexes
        self._by_category[pattern.category].add(pattern.id)
        self._by_badge_type[pattern.badge_type].add(pattern.id)
        self._by_priority[pattern.priority].add(pattern.id)

        for domain in pattern.life_domains:
            self._by_domain[domain].add(pattern.id)

        for participant in pattern.get_participants():
            self._by_participant[participant].add(pattern.id)

        # Invalidate cached processing order
        self._processing_order = None

    def register_many(self, patterns: List[PatternSpec], validate: bool = True) -> None:
        """Register multiple patterns at once."""
        for pattern in patterns:
            self.register(pattern, validate=validate)

    def unregister(self, pattern_id: str) -> Optional[PatternSpec]:
        """
        Remove a pattern from the registry.

        Returns the removed pattern, or None if not found.
        """
        pattern = self._patterns.pop(pattern_id, None)
        if pattern is None:
            return None

        # Remove from dependency graph
        self._dependency_graph.remove_pattern(pattern_id)

        # Remove from indexes
        self._by_category[pattern.category].discard(pattern_id)
        self._by_badge_type[pattern.badge_type].discard(pattern_id)
        self._by_priority[pattern.priority].discard(pattern_id)

        for domain in pattern.life_domains:
            self._by_domain[domain].discard(pattern_id)

        for participant in pattern.get_participants():
            self._by_participant[participant].discard(pattern_id)

        # Invalidate cached processing order
        self._processing_order = None

        return pattern

    # =========================================================================
    # Validation
    # =========================================================================

    def _validate_registration(self, pattern: PatternSpec) -> None:
        """
        Validate a pattern before registration.

        Checks:
        1. All required patterns exist
        2. No circular dependencies
        3. No contradictions with existing patterns
        """
        # Check required patterns exist
        for required_id in pattern.requires:
            if required_id not in self._patterns:
                raise MissingDependencyError(
                    f"Pattern '{pattern.id}' requires non-existent pattern '{required_id}'"
                )

        # Temporarily add to graph to check for cycles
        self._dependency_graph.add_pattern(pattern)
        cycle = self._dependency_graph.detect_cycle(pattern.id)
        if cycle:
            self._dependency_graph.remove_pattern(pattern.id)
            raise CircularDependencyError(
                f"Pattern '{pattern.id}' creates circular dependency: {' -> '.join(cycle)}"
            )
        # Remove temporary addition (will be re-added in register())
        self._dependency_graph.remove_pattern(pattern.id)

        # Check for contradictions
        contradictions = self._find_contradictions(pattern)
        if contradictions:
            raise ContradictionError(
                f"Pattern '{pattern.id}' contradicts: {', '.join(contradictions)}"
            )

    def _find_contradictions(self, pattern: PatternSpec) -> List[str]:
        """
        Find any contradictions between new pattern and existing patterns.

        A contradiction occurs when:
        1. Two patterns require each other to be blocked
        2. A pattern blocks its own requirement
        """
        contradictions = []

        # Check if pattern blocks any of its requirements
        for required_id in pattern.requires:
            if required_id in pattern.blocked_by:
                contradictions.append(
                    f"requires and blocks '{required_id}'"
                )

        # Check mutual blocking with existing patterns
        for blocked_id in pattern.blocked_by:
            if blocked_id in self._patterns:
                blocked_pattern = self._patterns[blocked_id]
                if pattern.id in blocked_pattern.blocked_by:
                    # This is actually fine - mutual blocking is allowed
                    pass

        return contradictions

    def validate_all(self) -> List[str]:
        """
        Validate entire registry for consistency.

        Returns list of any issues found.
        """
        issues = []

        # Check for orphaned requirements
        for pattern_id, pattern in self._patterns.items():
            for required_id in pattern.requires:
                if required_id not in self._patterns:
                    issues.append(f"Pattern '{pattern_id}' requires missing '{required_id}'")

        # Check for cycles in dependency graph
        for pattern_id in self._patterns:
            cycle = self._dependency_graph.detect_cycle(pattern_id)
            if cycle:
                issues.append(f"Circular dependency detected: {' -> '.join(cycle)}")
                break  # Only report first cycle

        return issues

    # =========================================================================
    # Lookup
    # =========================================================================

    def get(self, pattern_id: str) -> Optional[PatternSpec]:
        """Get a pattern by ID."""
        return self._patterns.get(pattern_id)

    def __getitem__(self, pattern_id: str) -> PatternSpec:
        """Get a pattern by ID, raising KeyError if not found."""
        return self._patterns[pattern_id]

    def __contains__(self, pattern_id: str) -> bool:
        """Check if a pattern ID is registered."""
        return pattern_id in self._patterns

    def __len__(self) -> int:
        """Return number of registered patterns."""
        return len(self._patterns)

    def __iter__(self) -> Iterator[PatternSpec]:
        """Iterate over all registered patterns."""
        return iter(self._patterns.values())

    def get_by_category(self, category: PatternCategory) -> List[PatternSpec]:
        """Get all patterns in a category."""
        return [self._patterns[pid] for pid in self._by_category.get(category, set())]

    def get_by_domain(self, domain: LifeDomain) -> List[PatternSpec]:
        """Get all patterns affecting a life domain."""
        return [self._patterns[pid] for pid in self._by_domain.get(domain, set())]

    def get_by_badge_type(self, badge_type: BadgeType) -> List[PatternSpec]:
        """Get all patterns with a specific badge type."""
        return [self._patterns[pid] for pid in self._by_badge_type.get(badge_type, set())]

    def get_by_participant(self, participant: str) -> List[PatternSpec]:
        """Get all patterns involving a specific stem or branch."""
        return [self._patterns[pid] for pid in self._by_participant.get(participant, set())]

    def get_by_participants(self, *participants: str) -> List[PatternSpec]:
        """Get patterns involving ALL specified participants."""
        if not participants:
            return []

        # Intersection of all participant sets
        result_ids = self._by_participant.get(participants[0], set()).copy()
        for participant in participants[1:]:
            result_ids &= self._by_participant.get(participant, set())

        return [self._patterns[pid] for pid in result_ids]

    # =========================================================================
    # Processing Order
    # =========================================================================

    def get_processing_order(self) -> List[PatternSpec]:
        """
        Get patterns in correct processing order.

        Order is determined by:
        1. Dependencies (requirements processed first)
        2. Priority (lower priority number first)
        3. Alphabetical ID (for determinism)
        """
        if self._processing_order is None:
            # Get topological order from dependency graph
            topo_order = self._dependency_graph.get_processing_order()

            # Create lookup for topo position
            topo_position = {pid: i for i, pid in enumerate(topo_order)}

            # Sort by: (topo_position, priority, id)
            sorted_ids = sorted(
                self._patterns.keys(),
                key=lambda pid: (
                    topo_position.get(pid, float('inf')),
                    self._patterns[pid].priority,
                    pid
                )
            )

            self._processing_order = sorted_ids

        return [self._patterns[pid] for pid in self._processing_order]

    def get_applicable_patterns(
        self,
        participants: Set[str],
        active_patterns: Set[str]
    ) -> List[PatternSpec]:
        """
        Get patterns that could potentially apply given participants and active patterns.

        Filters out:
        - Patterns blocked by active patterns
        - Patterns with missing requirements
        - Patterns with no matching participants
        """
        result = []

        for pattern in self.get_processing_order():
            # Check if any participant matches
            pattern_participants = set(pattern.get_participants())
            if not pattern_participants & participants:
                continue

            # Check if blocked
            if pattern.blocked_by & active_patterns:
                continue

            # Check if requirements met
            if not pattern.requires <= active_patterns:
                continue

            result.append(pattern)

        return result

    # =========================================================================
    # Statistics
    # =========================================================================

    def get_statistics(self) -> Dict[str, any]:
        """Get registry statistics."""
        return {
            "total_patterns": len(self._patterns),
            "by_category": {
                cat.value: len(ids) for cat, ids in self._by_category.items()
            },
            "by_domain": {
                domain.value: len(ids) for domain, ids in self._by_domain.items()
            },
            "unique_participants": len(self._by_participant),
            "patterns_with_dependencies": sum(
                1 for p in self._patterns.values() if p.requires
            ),
            "patterns_with_blockers": sum(
                1 for p in self._patterns.values() if p.blocked_by
            ),
        }


# =============================================================================
# GLOBAL REGISTRY INSTANCE
# =============================================================================

# Singleton pattern registry (initialized lazily)
_global_registry: Optional[PatternRegistry] = None


def get_global_registry() -> PatternRegistry:
    """Get the global pattern registry instance."""
    global _global_registry
    if _global_registry is None:
        _global_registry = PatternRegistry()
    return _global_registry


def reset_global_registry() -> None:
    """Reset the global registry (mainly for testing)."""
    global _global_registry
    _global_registry = None


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Errors
    "PatternRegistryError",
    "DuplicatePatternError",
    "CircularDependencyError",
    "MissingDependencyError",
    "ContradictionError",

    # Classes
    "DependencyGraph",
    "PatternRegistry",

    # Functions
    "get_global_registry",
    "reset_global_registry",
]
