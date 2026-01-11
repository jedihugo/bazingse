# * -------------------------
# * NODE-BASED DISTANCE MAPPING (2D GRID SYSTEM)
# * -------------------------
# Simple 2D grid coordinates (like a chessboard)
# Manhattan distance: distance = abs(x1 - x2) + abs(y1 - y2)
# CRITICAL: 10-year luck has special rule (distance = 1 to all natal)

# Position coordinates (x, y) where x = pillar column, y = layer (HS=0, EB=1)
NODE_COORDINATES = {
    # Natal chart (4 pillars x 2 layers = 8 nodes)
    "hs_y": (0, 0), "eb_y": (0, 1),
    "hs_m": (1, 0), "eb_m": (1, 1),
    "hs_d": (2, 0), "eb_d": (2, 1),
    "hs_h": (3, 0), "eb_h": (3, 1),

    # 10-year luck (special: distance = 1 to all natal)
    "hs_10yl": None,  # Special handling
    "eb_10yl": None,  # Special handling

    # Luck sequence (follows same 4x2 grid as natal)
    "hs_yl": (0, 0), "eb_yl": (0, 1),
    "hs_ml": (1, 0), "eb_ml": (1, 1),
    "hs_dl": (2, 0), "eb_dl": (2, 1),
    "hs_hl": (3, 0), "eb_hl": (3, 1),

    # Talisman nodes (special: distance = 1 to all natal, like luck pillars)
    "hs_ty": None,  # Special handling (external harmony tool)
    "eb_ty": None,  # Special handling
    "hs_tm": None,  # Special handling
    "eb_tm": None,  # Special handling
    "hs_td": None,  # Special handling
    "eb_td": None,  # Special handling
    "hs_th": None,  # Special handling
    "eb_th": None,  # Special handling
}


def get_distance_key(node1, node2):
    """
    Get distance key for two nodes using 2D grid coordinates (Manhattan distance).

    Grid layout (4x2 chessboard):
         y    m    d    h
    HS: (0,0)(1,0)(2,0)(3,0)
    EB: (0,1)(1,1)(2,1)(3,1)

    Manhattan distance = abs(x1 - x2) + abs(y1 - y2)

    Args:
        node1: Node ID (e.g., "hs_y", "eb_m", "hs_10yl")
        node2: Node ID (e.g., "hs_d", "eb_yl", "hs_h")

    Returns:
        str: "1", "2", "3", or "4"

    Examples:
        get_distance_key("hs_y", "hs_m") -> "1" (adjacent same layer)
        get_distance_key("hs_y", "eb_y") -> "1" (same pillar cross layer)
        get_distance_key("hs_y", "eb_m") -> "2" (adjacent cross layer: 1+1)
        get_distance_key("hs_y", "eb_h") -> "4" (far cross layer: 3+1)
        get_distance_key("hs_10yl", "eb_m") -> "1" (10-year luck always 1 to natal)
    """
    # Special case: Luck and talisman nodes are always distance 1 to all natal nodes
    # (temporal overlays and external harmony tools have full adjacency to natal)
    natal_nodes = {"hs_y", "eb_y", "hs_m", "eb_m", "hs_d", "eb_d", "hs_h", "eb_h"}
    special_nodes = {"hs_10yl", "eb_10yl", "hs_ty", "eb_ty", "hs_tm", "eb_tm", "hs_td", "eb_td", "hs_th", "eb_th"}

    if (node1 in special_nodes and node2 in natal_nodes) or \
       (node2 in special_nodes and node1 in natal_nodes):
        return "1"

    # Special case: Within same pillar (HS/EB pairs of luck or talisman)
    same_pillar_pairs = [
        ("hs_10yl", "eb_10yl"),
        ("hs_ty", "eb_ty"),
        ("hs_tm", "eb_tm"),
        ("hs_td", "eb_td"),
        ("hs_th", "eb_th")
    ]
    for hs, eb in same_pillar_pairs:
        if (node1 == hs and node2 == eb) or (node1 == eb and node2 == hs):
            return "1"

    # Get coordinates
    coord1 = NODE_COORDINATES.get(node1)
    coord2 = NODE_COORDINATES.get(node2)

    if coord1 is None or coord2 is None:
        # One is special node (luck/talisman), but not covered by special cases above
        # (e.g., 10-year luck to other luck nodes, talisman to talisman, etc.)
        # Treat special nodes as position (0,0) for special-to-special or special-to-luck distance
        if node1 in special_nodes:
            # HS nodes at layer 0, EB nodes at layer 1
            layer = 0 if node1.startswith("hs_") else 1
            coord1 = (0, layer)
        if node2 in special_nodes:
            layer = 0 if node2.startswith("hs_") else 1
            coord2 = (0, layer)

    # Calculate Manhattan distance (pure, no adjustments)
    # Luck pillars OVERLAP their corresponding natal pillars at same coordinates
    # Example: hs_yl (0,0) overlaps hs_y (0,0), so hs_yl-to-hs_h = hs_y-to-hs_h = 3
    distance = abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

    # Ensure minimum distance of 1 (overlapping nodes like eb_yl-eb_y are still distinct)
    distance = max(1, distance)

    return str(distance)


def get_distance_key_3nodes(node1, node2, node3):
    """
    Get distance key for three nodes (for THREE_MEETINGS, THREE_COMBINATIONS).
    Returns the maximum pairwise distance (the "span" of the 3-node formation).

    Formula: max(d12, d13, d23) where dXY = Manhattan distance between nodes X and Y

    Args:
        node1, node2, node3: Node IDs

    Returns:
        str: "2", "3", "4", "5", "6", "7", "8" (max pairwise distance)

    Examples:
        get_distance_key_3nodes("eb_y", "eb_m", "eb_d") -> "2"
            (distances: y-m=1, m-d=1, y-d=2, max=2)
        get_distance_key_3nodes("eb_y", "eb_m", "eb_h") -> "3"
            (distances: y-m=1, m-h=2, y-h=3, max=3)
    """
    # Calculate all three pairwise distances
    d12 = int(get_distance_key(node1, node2))
    d13 = int(get_distance_key(node1, node3))
    d23 = int(get_distance_key(node2, node3))

    # Return the maximum pairwise distance (the "span")
    return str(max(d12, d13, d23))
