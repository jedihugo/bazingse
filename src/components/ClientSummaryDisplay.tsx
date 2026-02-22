'use client';

import { useT } from './LanguageProvider';
import { CHART } from '@/lib/t';

interface SectionItem {
  label: string;
  value: string;
  severity?: string;
}

interface Section {
  id: string;
  title: string;
  title_zh?: string;
  severity?: string;
  text?: string;
  items?: SectionItem[];
}

interface ClientSummary {
  tier: string;
  sections: Section[];
}

function SeverityBadge({ severity }: { severity: string }) {
  const styleMap: Record<string, { bg: string; color: string }> = {
    strong: { bg: 'var(--tui-wood)', color: 'var(--tui-bg)' },
    weak: { bg: 'var(--tui-fire)', color: 'var(--tui-bg)' },
    neutral: { bg: 'var(--tui-water)', color: 'var(--tui-bg)' },
    positive: { bg: 'var(--tui-wood)', color: 'var(--tui-bg)' },
    info: { bg: 'var(--tui-water)', color: 'var(--tui-bg)' },
    warning: { bg: 'var(--tui-accent-orange, var(--tui-earth))', color: 'var(--tui-bg)' },
    alert: { bg: 'var(--tui-fire)', color: 'var(--tui-bg)' },
    severe: { bg: 'var(--tui-fire)', color: 'var(--tui-bg)' },
    negative: { bg: 'var(--tui-fire)', color: 'var(--tui-bg)' },
    moderate: { bg: 'var(--tui-earth)', color: 'var(--tui-bg)' },
    mild: { bg: 'var(--tui-metal)', color: 'var(--tui-bg)' },
  };
  const style = styleMap[severity] || styleMap.info;
  return (
    <span
      className="text-xs px-1.5 py-0.5 ml-2"
      style={{ background: style.bg, color: style.color }}
    >
      {severity}
    </span>
  );
}

function severityColor(severity?: string): string {
  const map: Record<string, string> = {
    positive: 'var(--tui-wood)',
    info: 'var(--tui-water)',
    warning: 'var(--tui-accent-orange, var(--tui-earth))',
    alert: 'var(--tui-fire)',
    severe: 'var(--tui-fire)',
    negative: 'var(--tui-fire)',
    moderate: 'var(--tui-earth)',
    mild: 'var(--tui-metal)',
  };
  return severity ? (map[severity] || 'var(--tui-fg-dim)') : 'var(--tui-fg-dim)';
}

export default function ClientSummaryDisplay({ chartData }: { chartData: any }) {
  const { t } = useT();
  const summary: ClientSummary | undefined = chartData?.client_summary;
  if (!summary?.sections?.length) return null;

  // Sections that should be open by default
  const defaultOpen = new Set(
    summary.tier === 'full'
      ? ['luck_pillar', 'element_shift', 'ten_gods_diff', 'interactions_diff', 'shen_sha_diff']
      : ['red_flags', 'summary', 'chart_overview', 'strength']
  );

  return (
    <div className="mt-3 space-y-1">
      <div className="text-xs tui-text-muted px-2 py-1">
        {summary.tier === 'full' ? t(CHART.what_changed) : t(CHART.natal_analysis)}
      </div>
      {summary.sections.map((section: Section) => (
        <details
          key={section.id}
          open={defaultOpen.has(section.id) || undefined}
          className="tui-frame"
        >
          <summary
            className="px-3 py-2 cursor-pointer text-sm font-medium flex items-center justify-between"
            style={{ background: 'var(--tui-bg-alt)' }}
          >
            <span>
              {section.title}
              {section.title_zh && (
                <span className="tui-text-muted ml-1">{section.title_zh}</span>
              )}
            </span>
            {section.severity && <SeverityBadge severity={section.severity} />}
          </summary>
          <div className="px-3 py-2 text-sm space-y-1">
            {section.text && (
              <p className="tui-text-dim">{section.text}</p>
            )}
            {section.items?.map((item, i) => (
              <div
                key={i}
                className="flex gap-2 text-xs py-0.5"
                style={{
                  borderLeft: item.severity ? `2px solid ${severityColor(item.severity)}` : undefined,
                  paddingLeft: item.severity ? '8px' : undefined,
                }}
              >
                <span className="font-medium shrink-0" style={{ color: severityColor(item.severity) }}>
                  {item.label}
                </span>
                <span className="tui-text-dim">{item.value}</span>
              </div>
            ))}
            {!section.text && (!section.items || section.items.length === 0) && (
              <p className="tui-text-muted text-xs">{t(CHART.no_section_data)}</p>
            )}
          </div>
        </details>
      ))}
    </div>
  );
}
