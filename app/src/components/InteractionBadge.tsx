'use client';

interface BadgeData {
  badge?: string;
  type?: string;
  size?: string;
  interaction_id?: string;
  strength?: string;
}

interface InteractionBadgeProps {
  badge: BadgeData;
  type: 'negative' | 'transformation' | 'combination' | 'wealth_storage';
  mappings?: any;
  hoveredInteractionId?: string | null;
  onHoverInteraction?: (id: string | null) => void;
}

// Element to Chinese character
const ELEMENT_CHINESE: Record<string, string> = {
  'Wood': '木', 'Fire': '火', 'Earth': '土', 'Metal': '金', 'Water': '水'
};

// TUI-style text labels for negative interactions (no icons)
const NEGATIVE_LABELS: Record<string, string> = {
  'clash': '沖',
  'harm': '害',
  'punishment': '刑',
  'destruction': '破',
  'stem_conflict': '剋',
};

// Helper to extract element from badge data
function extractElement(badge: BadgeData): string | null {
  if ((badge as any).result_element) return (badge as any).result_element;
  if ((badge as any).element) return (badge as any).element;
  const badgeText = badge.badge || badge.type || '';
  for (const el of ['Wood', 'Fire', 'Earth', 'Metal', 'Water']) {
    if (badgeText.includes(el)) return el;
  }
  return null;
}

// Element to TUI color class
const ELEMENT_TO_TUI_CLASS: Record<string, string> = {
  'Wood': 'tui-text-wood',
  'Fire': 'tui-text-fire',
  'Earth': 'tui-text-earth',
  'Metal': 'tui-text-metal',
  'Water': 'tui-text-water',
};

export default function InteractionBadge({ badge, type, mappings = {}, hoveredInteractionId, onHoverInteraction }: InteractionBadgeProps) {
  const interactionId = badge.interaction_id;
  const isHighlighted = interactionId && hoveredInteractionId === interactionId;

  const handleMouseEnter = () => {
    if (interactionId && onHoverInteraction) {
      onHoverInteraction(interactionId);
    }
  };

  const handleMouseLeave = () => {
    if (onHoverInteraction) {
      onHoverInteraction(null);
    }
  };

  // TUI style: simple text badges with element colors
  if (type === 'negative') {
    const negType = badge.type || 'clash';
    const label = NEGATIVE_LABELS[negType] || negType.charAt(0).toUpperCase();

    return (
      <span
        className={`tui-badge tui-badge-negative cursor-help ${isHighlighted ? 'underline' : ''}`}
        title={badge.type || 'Negative interaction'}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
      >
        {label}
      </span>
    );
  }

  if (type === 'transformation') {
    const element = extractElement(badge);
    const hanzi = element ? ELEMENT_CHINESE[element] : '化';
    const colorClass = element ? ELEMENT_TO_TUI_CLASS[element] : 'tui-text';

    return (
      <span
        className={`tui-badge ${colorClass} cursor-help ${isHighlighted ? 'underline' : ''}`}
        title={badge.badge || 'Transformation'}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
      >
        化{hanzi}
      </span>
    );
  }

  if (type === 'combination') {
    const element = extractElement(badge);
    const stemName = badge.badge || '';
    const stemMapping = mappings?.heavenly_stems?.[stemName];
    const hanzi = stemMapping?.chinese || (element ? ELEMENT_CHINESE[element] : '合');
    const colorClass = element ? ELEMENT_TO_TUI_CLASS[element] : 'tui-text-dim';

    return (
      <span
        className={`tui-badge ${colorClass} cursor-help ${isHighlighted ? 'underline' : ''}`}
        title={badge.badge || 'Combination'}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
      >
        {hanzi}
      </span>
    );
  }

  if (type === 'wealth_storage') {
    const element = extractElement(badge) || 'Earth';
    const colorClass = ELEMENT_TO_TUI_CLASS[element] || 'tui-text-earth';

    return (
      <span
        className={`tui-badge ${colorClass} cursor-help ${isHighlighted ? 'underline' : ''}`}
        title={badge.badge || 'Wealth Storage'}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
      >
        库
      </span>
    );
  }

  // Default
  return (
    <span className="tui-badge tui-text-muted" title={badge.badge || badge.type || 'Badge'}>
      {badge.badge?.charAt(0) || '?'}
    </span>
  );
}
