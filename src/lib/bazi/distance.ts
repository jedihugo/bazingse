import 'server-only';

// =============================================================================
// NODE-BASED DISTANCE MAPPING (2D GRID SYSTEM)
// =============================================================================
// Simple 2D grid coordinates (like a chessboard)
// Manhattan distance: distance = abs(x1 - x2) + abs(y1 - y2)
// CRITICAL: 10-year luck has special rule (distance = 1 to all natal)

type Coord = readonly [number, number];

// Position coordinates (x, y) where x = pillar column, y = layer (HS=0, EB=1)
export const NODE_COORDINATES: Readonly<Record<string, Coord | null>> = {
  // Natal chart (4 pillars x 2 layers = 8 nodes)
  hs_y: [0, 0], eb_y: [0, 1],
  hs_m: [1, 0], eb_m: [1, 1],
  hs_d: [2, 0], eb_d: [2, 1],
  hs_h: [3, 0], eb_h: [3, 1],

  // 10-year luck (special: distance = 1 to all natal)
  hs_10yl: null,  // Special handling
  eb_10yl: null,  // Special handling

  // Luck sequence (follows same 4x2 grid as natal)
  hs_yl: [0, 0], eb_yl: [0, 1],
  hs_ml: [1, 0], eb_ml: [1, 1],
  hs_dl: [2, 0], eb_dl: [2, 1],
  hs_hl: [3, 0], eb_hl: [3, 1],

  // Talisman nodes (special: distance = 1 to all natal, like luck pillars)
  hs_ty: null,  // Special handling (external harmony tool)
  eb_ty: null,  // Special handling
  hs_tm: null,  // Special handling
  eb_tm: null,  // Special handling
  hs_td: null,  // Special handling
  eb_td: null,  // Special handling
  hs_th: null,  // Special handling
  eb_th: null,  // Special handling
};

const NATAL_NODES = new Set([
  "hs_y", "eb_y", "hs_m", "eb_m", "hs_d", "eb_d", "hs_h", "eb_h",
]);

const SPECIAL_NODES = new Set([
  "hs_10yl", "eb_10yl",
  "hs_ty", "eb_ty", "hs_tm", "eb_tm", "hs_td", "eb_td", "hs_th", "eb_th",
]);

const SAME_PILLAR_PAIRS: readonly (readonly [string, string])[] = [
  ["hs_10yl", "eb_10yl"],
  ["hs_ty", "eb_ty"],
  ["hs_tm", "eb_tm"],
  ["hs_td", "eb_td"],
  ["hs_th", "eb_th"],
];

/**
 * Get distance key for two nodes using 2D grid coordinates (Manhattan distance).
 *
 * Grid layout (4x2 chessboard):
 *      y    m    d    h
 * HS: (0,0)(1,0)(2,0)(3,0)
 * EB: (0,1)(1,1)(2,1)(3,1)
 */
export function getDistanceKey(node1: string, node2: string): string {
  // Special case: Luck and talisman nodes are always distance 1 to all natal nodes
  if (
    (SPECIAL_NODES.has(node1) && NATAL_NODES.has(node2)) ||
    (SPECIAL_NODES.has(node2) && NATAL_NODES.has(node1))
  ) {
    return "1";
  }

  // Special case: Within same pillar (HS/EB pairs of luck or talisman)
  for (const [hs, eb] of SAME_PILLAR_PAIRS) {
    if ((node1 === hs && node2 === eb) || (node1 === eb && node2 === hs)) {
      return "1";
    }
  }

  // Get coordinates
  let coord1 = NODE_COORDINATES[node1] ?? null;
  let coord2 = NODE_COORDINATES[node2] ?? null;

  if (coord1 === null && SPECIAL_NODES.has(node1)) {
    const layer = node1.startsWith("hs_") ? 0 : 1;
    coord1 = [0, layer];
  }
  if (coord2 === null && SPECIAL_NODES.has(node2)) {
    const layer = node2.startsWith("hs_") ? 0 : 1;
    coord2 = [0, layer];
  }

  // Calculate Manhattan distance
  const distance = Math.abs(coord1![0] - coord2![0]) + Math.abs(coord1![1] - coord2![1]);

  // Ensure minimum distance of 1
  return String(Math.max(1, distance));
}

/**
 * Get distance key for three nodes (for THREE_MEETINGS, THREE_COMBINATIONS).
 * Returns the maximum pairwise distance (the "span" of the 3-node formation).
 */
export function getDistanceKey3Nodes(
  node1: string,
  node2: string,
  node3: string,
): string {
  const d12 = parseInt(getDistanceKey(node1, node2), 10);
  const d13 = parseInt(getDistanceKey(node1, node3), 10);
  const d23 = parseInt(getDistanceKey(node2, node3), 10);

  return String(Math.max(d12, d13, d23));
}
