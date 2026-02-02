'use client';

interface RemedyBadgeProps {
  element: string;
  colors?: string[];
  numbers?: number[];
  direction?: string;
}

// Element colors
const ELEMENT_COLORS: Record<string, { bg: string; text: string; border: string }> = {
  Wood: { bg: '#dcfce7', text: '#166534', border: '#22c55e' },
  Fire: { bg: '#fee2e2', text: '#991b1b', border: '#ef4444' },
  Earth: { bg: '#fef3c7', text: '#92400e', border: '#f59e0b' },
  Metal: { bg: '#f3f4f6', text: '#374151', border: '#9ca3af' },
  Water: { bg: '#dbeafe', text: '#1e40af', border: '#3b82f6' },
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
