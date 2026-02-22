import 'server-only';

// =============================================================================
// PATTERN REGISTRY
// =============================================================================
// Registry for managing and looking up PatternSpec objects.
// Ported from api/library/pattern_engine/pattern_registry.py
// =============================================================================

import type { PatternSpec } from './pattern-spec';

// ---------------------------------------------------------------------------
// Error Classes
// ---------------------------------------------------------------------------

export class PatternRegistryError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'PatternRegistryError';
  }
}

export class DuplicatePatternError extends PatternRegistryError {
  constructor(patternId: string) {
    super(`Pattern '${patternId}' is already registered`);
    this.name = 'DuplicatePatternError';
  }
}

export class CircularDependencyError extends PatternRegistryError {
  constructor(cycle: string[]) {
    super(`Circular dependency detected: ${cycle.join(' -> ')}`);
    this.name = 'CircularDependencyError';
  }
}

export class MissingDependencyError extends PatternRegistryError {
  constructor(patternId: string, depId: string) {
    super(`Pattern '${patternId}' depends on missing pattern '${depId}'`);
    this.name = 'MissingDependencyError';
  }
}

export class ContradictionError extends PatternRegistryError {
  constructor(msg: string) {
    super(msg);
    this.name = 'ContradictionError';
  }
}

// ---------------------------------------------------------------------------
// Dependency Graph (Kahn's Algorithm)
// ---------------------------------------------------------------------------

export class DependencyGraph {
  private adjacency: Map<string, Set<string>> = new Map();
  private inDegree: Map<string, number> = new Map();

  addNode(nodeId: string): void {
    if (!this.adjacency.has(nodeId)) {
      this.adjacency.set(nodeId, new Set());
      this.inDegree.set(nodeId, 0);
    }
  }

  addEdge(from: string, to: string): void {
    this.addNode(from);
    this.addNode(to);
    const edges = this.adjacency.get(from)!;
    if (!edges.has(to)) {
      edges.add(to);
      this.inDegree.set(to, (this.inDegree.get(to) ?? 0) + 1);
    }
  }

  topologicalSort(): string[] {
    const result: string[] = [];
    const queue: string[] = [];

    for (const [node, degree] of this.inDegree) {
      if (degree === 0) {
        queue.push(node);
      }
    }

    while (queue.length > 0) {
      const node = queue.shift()!;
      result.push(node);

      const neighbors = this.adjacency.get(node) ?? new Set();
      for (const neighbor of neighbors) {
        const newDegree = (this.inDegree.get(neighbor) ?? 0) - 1;
        this.inDegree.set(neighbor, newDegree);
        if (newDegree === 0) {
          queue.push(neighbor);
        }
      }
    }

    // Check for cycles
    if (result.length < this.adjacency.size) {
      const remaining = [...this.adjacency.keys()].filter(
        (k) => !result.includes(k)
      );
      throw new CircularDependencyError(remaining);
    }

    return result;
  }
}

// ---------------------------------------------------------------------------
// Pattern Registry
// ---------------------------------------------------------------------------

export class PatternRegistry {
  private patterns: Map<string, PatternSpec> = new Map();
  private byCategory: Map<string, PatternSpec[]> = new Map();

  register(pattern: PatternSpec, validate: boolean = true): void {
    if (this.patterns.has(pattern.id)) {
      // Skip if already registered (don't throw)
      return;
    }

    this.patterns.set(pattern.id, pattern);

    const catKey = pattern.category;
    if (!this.byCategory.has(catKey)) {
      this.byCategory.set(catKey, []);
    }
    this.byCategory.get(catKey)!.push(pattern);
  }

  get(patternId: string): PatternSpec | undefined {
    return this.patterns.get(patternId);
  }

  has(patternId: string): boolean {
    return this.patterns.has(patternId);
  }

  getByCategory(category: string): PatternSpec[] {
    return this.byCategory.get(category) ?? [];
  }

  getAll(): PatternSpec[] {
    return [...this.patterns.values()];
  }

  get size(): number {
    return this.patterns.size;
  }

  [Symbol.iterator](): Iterator<[string, PatternSpec]> {
    return this.patterns.entries();
  }

  getProcessingOrder(): PatternSpec[] {
    // Sort by priority (lower number = higher priority)
    return [...this.patterns.values()].sort((a, b) => a.priority - b.priority);
  }
}

// ---------------------------------------------------------------------------
// Global Registry Singleton
// ---------------------------------------------------------------------------

let globalRegistry: PatternRegistry | null = null;

export function getGlobalRegistry(): PatternRegistry {
  if (!globalRegistry) {
    globalRegistry = new PatternRegistry();
  }
  return globalRegistry;
}

export function resetGlobalRegistry(): void {
  globalRegistry = null;
}
