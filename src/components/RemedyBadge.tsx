'use client';

interface RemedyBadgeProps {
  element: string;
  colors?: string[];
  numbers?: number[];
  direction?: string;
}

// Theme-aware color helper
const themeColor = (cssVar: string) => ({
  bg: `color-mix(in srgb, ${cssVar} 15%, var(--tui-bg))`,
  text: cssVar,
  border: `color-mix(in srgb, ${cssVar} 40%, var(--tui-bg))`,
});

// Element colors - theme-aware via CSS variables
const ELEMENT_COLORS: Record<string, { bg: string; text: string; border: string }> = {
  Wood: themeColor('var(--tui-wood)'),
  Fire: themeColor('var(--tui-fire)'),
  Earth: themeColor('var(--tui-earth)'),
  Metal: themeColor('var(--tui-metal)'),
  Water: themeColor('var(--tui-water)'),
};

// Element Chinese characters
const ELEMENT_CHINESE: Record<string, string> = {
  Wood: '木',
  Fire: '火',
  Earth: '土',
  Metal: '金',
  Water: '水',
};

export default function RemedyBadge({ element, colors, numbers, direction }: RemedyBadgeProps) {
  const elementColors = ELEMENT_COLORS[element] || ELEMENT_COLORS.Earth;
  const elementChinese = ELEMENT_CHINESE[element] || element;

  return (
    <div
      className="remedy-badge p-2 rounded-lg text-center min-w-[80px]"
      style={{
        backgroundColor: elementColors.bg,
        border: `2px solid ${elementColors.border}`,
      }}
    >
      {/* Element Name */}
      <div
        className="text-xs font-bold mb-1"
        style={{ color: elementColors.text }}
      >
        <span className="mr-1">{elementChinese}</span>
        <span>{element}</span>
      </div>

      {/* Lucky Info */}
      <div className="space-y-0.5 text-[9px]" style={{ color: elementColors.text }}>
        {/* Colors */}
        {colors && colors.length > 0 && (
          <div className="flex items-center justify-center gap-1">
            <span className="opacity-60">Color:</span>
            <span className="font-medium capitalize">{colors[0]}</span>
          </div>
        )}

        {/* Numbers */}
        {numbers && numbers.length > 0 && (
          <div className="flex items-center justify-center gap-1">
            <span className="opacity-60">Lucky #:</span>
            <span className="font-mono font-medium">{numbers.join(', ')}</span>
          </div>
        )}

        {/* Direction */}
        {direction && (
          <div className="flex items-center justify-center gap-1">
            <span className="opacity-60">Dir:</span>
            <span className="font-medium">{direction}</span>
          </div>
        )}
      </div>

      {/* Label */}
      <div className="mt-1 pt-1 border-t text-[8px] opacity-60" style={{ borderColor: elementColors.border }}>
        Favorable Element
      </div>
    </div>
  );
}
