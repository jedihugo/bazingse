import 'server-only';

// =============================================================================
// BAZI MODULE - Master Barrel Export
// =============================================================================
// Top-level re-exports for all BaZi sub-modules.
// =============================================================================

// Core types and data
export * from './core';

// Derived data (computed from core)
export * from './derived';

// Chart construction
export * from './chart';

// Seasonal
export * from './seasonal';

// Qi Phase (Twelve Life Stages)
export * from './qi-phase';

// Physics school
export * from './physics';

// Distance calculations
export * from './distance';

// Combinations (positive branch interactions)
export * from './combinations';

// Conflicts (negative branch interactions)
export * from './conflicts';

// Wealth Storage
export * from './wealth-storage';

// Wu Xing Unity
export * from './unity';

// Dong Gong Calendar
export * from './dong-gong';

// Sub-modules (re-exported as namespaces via barrel files)
// Use: import { ... } from '@/lib/bazi/comprehensive'
// Use: import { ... } from '@/lib/bazi/narrative'
// Use: import { ... } from '@/lib/bazi/life-aspects'
// Use: import { ... } from '@/lib/bazi/pattern-engine'
