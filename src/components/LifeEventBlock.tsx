'use client';

import { useState, useRef, useEffect } from 'react';
import BaZiChart from './BaZiChart';
import ElementAnalysis from './ElementAnalysis';
import WealthStorageDisplay from './WealthStorageDisplay';
import NarrativeDisplay from './NarrativeDisplay';
import ClientSummaryDisplay from './ClientSummaryDisplay';
import { type LifeEvent, updateLifeEvent } from '@/lib/api';
import { tri, triCompact, ACTIONS, STATUS, LOCATION, CHART, SPIRITUAL } from '@/lib/t';


interface LifeEventBlockProps {
  profileId: string;
  event: LifeEvent;
  chartData: any;
  isLoading?: boolean;
  error?: string | null;
  isNatal?: boolean;
  onDelete?: () => void;
  onEventUpdate?: (event: LifeEvent) => void;
}

function formatDateLabel(event: LifeEvent): string {
  const parts = [event.year.toString()];
  if (event.month) {
    const monthName = new Date(2000, event.month - 1, 1).toLocaleString('default', { month: 'short' });
    parts.push(monthName);
  }
  if (event.day) {
    parts.push(event.day.toString());
  }
  return parts.join(' - ');
}

export default function LifeEventBlock({
  profileId,
  event,
  chartData,
  isLoading = false,
  error = null,
  isNatal = false,
  onDelete,
  onEventUpdate,
}: LifeEventBlockProps) {
  const [isEditingNotes, setIsEditingNotes] = useState(false);
  const [notes, setNotes] = useState(event.notes || '');
  const [isSaving, setIsSaving] = useState(false);
  const [isTogglingAbroad, setIsTogglingAbroad] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Sync notes state with prop
  useEffect(() => {
    setNotes(event.notes || '');
  }, [event.notes]);

  // Auto-resize textarea
  useEffect(() => {
    if (isEditingNotes && textareaRef.current) {
      textareaRef.current.focus();
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
    }
  }, [isEditingNotes, notes]);

  const handleSaveNotes = async () => {
    if (isSaving) return;

    const trimmedNotes = notes.trim();

    // Only save if changed
    if (trimmedNotes === (event.notes || '')) {
      setIsEditingNotes(false);
      return;
    }

    try {
      setIsSaving(true);
      const updated = await updateLifeEvent(profileId, event.id, {
        notes: trimmedNotes || null,
      });
      onEventUpdate?.(updated);
    } catch (err) {
      console.error('Failed to save notes:', err);
      // Revert on error
      setNotes(event.notes || '');
    } finally {
      setIsSaving(false);
      setIsEditingNotes(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      setNotes(event.notes || '');
      setIsEditingNotes(false);
    }
    // Allow Enter for newlines, Cmd/Ctrl+Enter to save
    if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
      handleSaveNotes();
    }
  };

  const handleDelete = () => {
    setShowDeleteConfirm(false);
    onDelete?.();
  };

  const handleToggleAbroad = async () => {
    if (isTogglingAbroad) return;
    try {
      setIsTogglingAbroad(true);
      const newValue = !event.is_abroad;
      const updated = await updateLifeEvent(profileId, event.id, {
        is_abroad: newValue,
      });
      onEventUpdate?.(updated);
    } catch (err) {
      console.error('Failed to toggle abroad:', err);
    } finally {
      setIsTogglingAbroad(false);
    }
  };

  return (
    <div className="tui-frame overflow-hidden" style={isNatal ? { borderColor: 'var(--tui-accent-purple)' } : {}}>
      {/* Header */}
      <div
        className="px-4 py-2"
        style={isNatal
          ? { background: 'color-mix(in srgb, var(--tui-accent-purple) 15%, var(--tui-bg))' }
          : { background: 'var(--tui-bg-alt)' }
        }
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="font-semibold" style={isNatal ? { color: 'var(--tui-accent-purple)' } : { color: 'var(--tui-fg-dim)' }}>
              {isNatal ? tri(CHART.birth_chart) : formatDateLabel(event)}
            </span>
            {isNatal && (
              <span
                className="text-xs px-2 py-0.5"
                style={{ background: 'var(--tui-accent-purple)', color: 'var(--tui-bg)' }}
              >{triCompact(CHART.birth)}</span>
            )}
            {chartData?.school && chartData.school !== 'classic' && (
              <span
                className="text-xs px-2 py-0.5"
                style={{ background: 'var(--tui-water)', color: 'var(--tui-bg)' }}
              >{chartData.school}</span>
            )}
            {chartData?.hs_10yl?.misc && (
              <span className="text-xs tui-text-muted">
                10Y: {chartData.hs_10yl.misc.start_date?.split('-')[0]} - {chartData.hs_10yl.misc.end_date?.split('-')[0]}
              </span>
            )}
          </div>

          {/* Delete button */}
          {!isNatal && onDelete && (
            <div className="relative">
              {showDeleteConfirm ? (
                <div className="flex items-center gap-2">
                  <span className="text-xs tui-text-muted">{triCompact(ACTIONS.delete)}?</span>
                  <button
                    onClick={handleDelete}
                    className="text-xs px-2 py-1"
                    style={{ background: 'var(--tui-error)', color: 'var(--tui-bg)' }}
                  >
                    {triCompact(ACTIONS.yes)}
                  </button>
                  <button
                    onClick={() => setShowDeleteConfirm(false)}
                    className="tui-btn text-xs px-2 py-1"
                  >
                    {triCompact(ACTIONS.no)}
                  </button>
                </div>
              ) : (
                <button
                  onClick={() => setShowDeleteConfirm(true)}
                  className="tui-text-muted p-1"
                  title={tri(ACTIONS.delete)}
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                </button>
              )}
            </div>
          )}
        </div>
        {/* Location line with abroad toggle */}
        {!isNatal && event.location && (
          <div className="text-xs mt-1 flex items-center gap-2 flex-wrap">
            <span className="tui-text-dim">{event.location}</span>
            <button
              onClick={handleToggleAbroad}
              disabled={isTogglingAbroad}
              className="inline-flex items-center gap-1 px-1.5 py-0.5 transition-colors"
              style={{
                color: event.is_abroad ? 'var(--tui-water)' : 'var(--tui-fg-muted)',
                background: event.is_abroad ? 'color-mix(in srgb, var(--tui-water) 15%, var(--tui-bg))' : 'transparent',
                border: `1px solid ${event.is_abroad ? 'var(--tui-water)' : 'var(--tui-border)'}`,
                opacity: isTogglingAbroad ? 0.5 : 1,
              }}
              title={tri(LOCATION.abroad_hint)}
            >
              <span style={{ fontFamily: 'monospace' }}>{event.is_abroad ? '[x]' : '[_]'}</span>
              <span>{triCompact(LOCATION.abroad)}</span>
            </button>
          </div>
        )}
      </div>

      {/* Content */}
      <div className="p-2">
        {isLoading ? (
          <div className="py-8 text-center tui-text-muted">
            <div className="inline-block animate-spin h-5 w-5 border-2 tui-border mr-2" style={{ borderTopColor: 'var(--tui-water)' }}></div>
            {tri(STATUS.loading_chart)}
          </div>
        ) : error ? (
          <div className="py-4 px-3 text-sm" style={{ background: 'color-mix(in srgb, var(--tui-error) 10%, var(--tui-bg))', color: 'var(--tui-error)' }}>{error}</div>
        ) : chartData ? (
          <>
            {/* Row 1: Natal only (Hour | Day | Month | Year) */}
            <BaZiChart
              chartData={chartData}
              showNatal={true}
              showLuck={false}
              showTalisman={false}
              showLocation={false}
            />

            {/* Row 2: Aligned comparison (Hourly|Daily|Monthly|Annual|10Y) */}
            {!isNatal && chartData?.analysis_info?.year && (
              <div className="mt-1">
                <BaZiChart
                  chartData={chartData}
                  showNatal={false}
                  showLuck={true}
                  showTalisman={false}
                  showLocation={false}
                />
              </div>
            )}

            {/* Element Analysis */}
            <ElementAnalysis chartData={chartData} />

            {/* Wealth Storage Analysis */}
            <WealthStorageDisplay chartData={chartData} />

            {/* Spiritual Sensitivity (natal only) */}
            {isNatal && chartData?.spiritual_sensitivity && (() => {
              const ss = chartData.spiritual_sensitivity;
              const score: number = ss.score ?? 0;
              const filled = Math.round(score / 10);
              const empty = 10 - filled;
              const bar = '\u2588'.repeat(filled) + '\u2591'.repeat(empty);

              // Score color thresholds
              const scoreColor =
                score <= 20 ? 'var(--tui-wood)' :
                score <= 40 ? 'var(--tui-warning)' :
                score <= 60 ? 'var(--tui-accent-orange)' :
                score <= 80 ? 'var(--tui-fire)' :
                'var(--tui-accent-purple)';

              const indicators: Array<{ name: string; name_zh: string; weight: number; reason: string }> = ss.indicators || [];

              return (
                <div className="tui-frame mt-2">
                  <div className="tui-frame-title flex items-center justify-between">
                    <span>{tri(SPIRITUAL.title)}</span>
                    <span
                      className="text-xs px-1.5 py-0.5"
                      style={{ background: scoreColor, color: 'var(--tui-bg)' }}
                    >
                      {ss.label_zh || ss.level}
                    </span>
                  </div>

                  <div className="p-2 font-mono space-y-2">
                    {/* Score bar */}
                    <div className="flex items-center gap-2 text-sm">
                      <span className="tui-text-muted w-10 text-right">{score}</span>
                      <span style={{ color: scoreColor, letterSpacing: '1px' }}>{bar}</span>
                      <span className="tui-text-muted">100</span>
                    </div>

                    {/* Level label */}
                    <div className="text-xs tui-text-dim">
                      {ss.label_zh && ss.label_en
                        ? `${ss.label_zh} / ${ss.label_en}`
                        : ss.label_en || ss.label_zh || ss.level}
                    </div>

                    {/* Description */}
                    {(ss.description_en || ss.description_zh) && (
                      <div className="text-xs tui-text-dim" style={{ lineHeight: '1.5' }}>
                        {ss.description_zh || ss.description_en}
                      </div>
                    )}

                    {/* Indicators (collapsible) */}
                    {indicators.length > 0 && (
                      <details className="mt-1">
                        <summary className="text-xs tui-text-muted cursor-pointer py-1">
                          {tri(CHART.indicators)} ({indicators.length})
                        </summary>
                        <div className="space-y-1 mt-1">
                          {indicators.map((ind, i) => (
                            <div key={i} className="text-xs flex gap-2 flex-wrap">
                              <span
                                className="px-1"
                                style={{ color: scoreColor, border: `1px solid ${scoreColor}` }}
                              >
                                +{ind.weight}
                              </span>
                              <span className="tui-text-dim">
                                {ind.name_zh} {ind.name}
                              </span>
                              {ind.reason && (
                                <span className="tui-text-muted">{ind.reason}</span>
                              )}
                            </div>
                          ))}
                        </div>
                      </details>
                    )}

                    {/* Guidance (collapsible) */}
                    {(ss.guidance_en || ss.guidance_zh) && (
                      <details className="mt-1">
                        <summary className="text-xs tui-text-muted cursor-pointer py-1">
                          {tri(CHART.guidance)}
                        </summary>
                        <div className="text-xs tui-text-dim mt-1" style={{ lineHeight: '1.5' }}>
                          {ss.guidance_zh || ss.guidance_en}
                        </div>
                      </details>
                    )}
                  </div>
                </div>
              );
            })()}

            {/* Interaction-Based Narratives (collapsed) */}
            {isNatal && chartData?.narrative_analysis && (
              <details className="mt-3">
                <summary className="text-xs font-semibold tui-text-dim cursor-pointer p-2 tui-bg-alt tui-border">
                  {tri(CHART.interaction_analysis)}
                </summary>
                <NarrativeDisplay chartData={chartData} />
              </details>
            )}

            {/* Client Summary — replaces old health/wealth/learning boxes */}
            {chartData?.client_summary && (
              <ClientSummaryDisplay chartData={chartData} />
            )}
          </>
        ) : (
          <div className="py-8 text-center tui-text-muted">{tri(STATUS.no_data)}</div>
        )}
      </div>

      {/* Notes section (only for non-natal events) */}
      {!isNatal && !isLoading && !error && (
        <div className="border-t tui-border-color px-4 py-3">
          {isEditingNotes ? (
            <div className="relative">
              <textarea
                ref={textareaRef}
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                onBlur={handleSaveNotes}
                onKeyDown={handleKeyDown}
                placeholder={tri(CHART.add_notes)}
                className="tui-input w-full text-sm px-3 py-2 resize-none min-h-[60px]"
                maxLength={10000}
              />
              <div className="flex justify-between items-center mt-1 text-xs tui-text-muted">
                <span>{tri(CHART.esc_cancel)}</span>
                {isSaving && <span>{tri(STATUS.saving)}</span>}
              </div>
            </div>
          ) : (
            <div
              onClick={() => setIsEditingNotes(true)}
              className={`text-sm cursor-pointer px-2 py-1 -mx-2 ${
                notes ? 'tui-text-dim' : 'tui-text-muted italic'
              }`}
              title={tri(CHART.click_add_notes)}
            >
              {notes || tri(CHART.click_add_notes)}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
