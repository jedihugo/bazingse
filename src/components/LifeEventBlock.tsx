'use client';

import { useState, useRef, useEffect } from 'react';
import { useTranslations, useLocale } from 'next-intl';
import BaZiChart from './BaZiChart';
import ElementAnalysis from './ElementAnalysis';
import NarrativeDisplay from './NarrativeDisplay';
import PhysicsAnalysisDisplay from './PhysicsAnalysisDisplay';
import { type LifeEvent, updateLifeEvent } from '@/lib/api';

// Helper to get localized analysis text from API response
function getLocalizedAnalysisText(analysis: any, locale: string): string {
  if (!analysis) return '';

  // Map locale to API field suffix
  if (locale === 'zh') {
    return analysis.analysis_text_chinese || analysis.analysis_text || '';
  } else if (locale === 'id') {
    return analysis.analysis_text_id || analysis.analysis_text || '';
  }
  // Default to English
  return analysis.analysis_text || '';
}

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
  const t = useTranslations();
  const tCommon = useTranslations('common');
  const tHealth = useTranslations('lifeAspects.health');
  const tWealth = useTranslations('lifeAspects.wealth');
  const tLearning = useTranslations('lifeAspects.learning');
  const tTenGods = useTranslations('lifeAspects.ten_gods');
  const locale = useLocale();

  const tForms = useTranslations('forms');

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

  // Translate severity category
  const getSeverityLabel = (severity: string) => {
    const severityMap: Record<string, string> = {
      'severe': tHealth('severity.severe'),
      'moderate': tHealth('severity.moderate'),
      'mild': tHealth('severity.mild'),
      'balanced': tHealth('severity.balanced'),
    };
    return severityMap[severity] || severity;
  };

  // Translate outlook
  const getOutlookLabel = (outlook: string, section: 'wealth' | 'learning') => {
    const t = section === 'wealth' ? tWealth : tLearning;
    const outlookMap: Record<string, string> = {
      'favorable': t('outlook.favorable'),
      'neutral': t('outlook.neutral'),
      'challenging': t('outlook.challenging'),
    };
    return outlookMap[outlook] || outlook;
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
              {isNatal ? 'Birth Chart' : formatDateLabel(event)}
            </span>
            {isNatal && (
              <span
                className="text-xs px-2 py-0.5"
                style={{ background: 'var(--tui-accent-purple)', color: 'var(--tui-bg)' }}
              >Birth</span>
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
                  <span className="text-xs tui-text-muted">{tCommon('actions.delete')}?</span>
                  <button
                    onClick={handleDelete}
                    className="text-xs px-2 py-1"
                    style={{ background: 'var(--tui-error)', color: 'var(--tui-bg)' }}
                  >
                    {tCommon('actions.yes')}
                  </button>
                  <button
                    onClick={() => setShowDeleteConfirm(false)}
                    className="tui-btn text-xs px-2 py-1"
                  >
                    {tCommon('actions.no')}
                  </button>
                </div>
              ) : (
                <button
                  onClick={() => setShowDeleteConfirm(true)}
                  className="tui-text-muted p-1"
                  title={tCommon('actions.delete')}
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
              title={tForms('location.abroad_hint')}
            >
              <span style={{ fontFamily: 'monospace' }}>{event.is_abroad ? '[x]' : '[_]'}</span>
              <span>{tForms('location.abroad')}</span>
            </button>
          </div>
        )}
      </div>

      {/* Content */}
      <div className="p-2">
        {isLoading ? (
          <div className="py-8 text-center tui-text-muted">
            <div className="inline-block animate-spin h-5 w-5 border-2 tui-border mr-2" style={{ borderTopColor: 'var(--tui-water)' }}></div>
            {tCommon('status.loading_chart')}
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

            {/* Physics Analysis (only shown when school=physics and data exists) */}
            {chartData?.physics_analysis && (
              <PhysicsAnalysisDisplay physicsAnalysis={chartData.physics_analysis} mappings={chartData.mappings} />
            )}

            {/* Interaction-Based Narratives (collapsed) */}
            {isNatal && chartData?.narrative_analysis && (
              <details className="mt-3">
                <summary className="text-xs font-semibold tui-text-dim cursor-pointer p-2 tui-bg-alt tui-border">
                  Interaction Analysis (Advanced)
                </summary>
                <NarrativeDisplay chartData={chartData} />
              </details>
            )}

            {/* Life Aspects Analysis - Pattern Engine Enhanced */}
            {!isNatal && chartData?.analysis_info?.year && (
              <div className="mt-3 space-y-2">
                {/* Health Analysis - Pattern Engine */}
                {chartData?.health_analysis?.pattern_engine && (
                  <div
                    className="px-3 py-2 text-sm"
                    style={{
                      background: 'color-mix(in srgb, var(--tui-fire) 15%, var(--tui-bg))',
                      border: '1px solid color-mix(in srgb, var(--tui-fire) 40%, var(--tui-bg))'
                    }}
                  >
                    <div className="flex items-center justify-between">
                      <div className="font-medium" style={{ color: 'var(--tui-fire)' }}>{tHealth('title')}</div>
                      <span
                        className="text-xs px-1.5 py-0.5 rounded"
                        style={{
                          background: chartData.health_analysis.pattern_engine.severity_level === 'critical' ? 'var(--tui-fire)' :
                            chartData.health_analysis.pattern_engine.severity_level === 'major' ? 'var(--tui-accent-orange)' :
                            chartData.health_analysis.pattern_engine.severity_level === 'moderate' ? 'var(--tui-earth)' :
                            'var(--tui-wood)',
                          color: 'var(--tui-bg)'
                        }}
                      >
                        {chartData.health_analysis.pattern_engine.severity_level || 'balanced'}
                      </span>
                    </div>
                    {/* Pattern Engine Recommendations */}
                    {chartData.health_analysis.pattern_engine.recommendations?.map((rec: any, i: number) => (
                      <div key={i} className="mt-1" style={{ color: 'var(--tui-fire)' }}>
                        <span className="font-medium">{rec.title}</span>: {rec.description}
                      </div>
                    ))}
                    {/* Top Patterns */}
                    {chartData.health_analysis.pattern_engine.top_patterns?.length > 0 && (
                      <div
                        className="mt-2 text-xs px-2 py-1 rounded"
                        style={{
                          background: 'color-mix(in srgb, var(--tui-fire) 25%, var(--tui-bg))',
                          color: 'var(--tui-fire)'
                        }}
                      >
                        {chartData.health_analysis.pattern_engine.top_patterns.slice(0, 3).map((p: any, i: number) => (
                          <div key={i}>
                            {p.chinese_name}: {p.severity?.toFixed(0)} ({p.level})
                          </div>
                        ))}
                      </div>
                    )}
                    {/* Fallback to old analysis if no pattern engine recommendations */}
                    {!chartData.health_analysis.pattern_engine.recommendations?.length && chartData.health_analysis.analysis_text && (
                      <div className="mt-1" style={{ color: 'var(--tui-fire)' }}>{getLocalizedAnalysisText(chartData.health_analysis, locale)}</div>
                    )}
                  </div>
                )}
                {/* Fallback: Old Health Analysis if no pattern engine */}
                {!chartData?.health_analysis?.pattern_engine && chartData?.health_analysis?.analysis_text && (
                  <div
                    className="px-3 py-2 text-sm"
                    style={{
                      background: 'color-mix(in srgb, var(--tui-fire) 15%, var(--tui-bg))',
                      border: '1px solid color-mix(in srgb, var(--tui-fire) 40%, var(--tui-bg))'
                    }}
                  >
                    <div className="flex items-center justify-between">
                      <div className="font-medium" style={{ color: 'var(--tui-fire)' }}>{tHealth('title')}</div>
                      <span
                        className="text-xs px-1.5 py-0.5 rounded"
                        style={{
                          background: chartData.health_analysis.severity_category === 'severe' ? 'var(--tui-fire)' :
                            chartData.health_analysis.severity_category === 'moderate' ? 'var(--tui-accent-orange)' :
                            chartData.health_analysis.severity_category === 'mild' ? 'var(--tui-earth)' :
                            'var(--tui-wood)',
                          color: 'var(--tui-bg)'
                        }}
                      >
                        {getSeverityLabel(chartData.health_analysis.severity_category || 'balanced')}
                      </span>
                    </div>
                    <div className="mt-1" style={{ color: 'var(--tui-fire)' }}>{getLocalizedAnalysisText(chartData.health_analysis, locale)}</div>
                  </div>
                )}

                {/* Wealth Analysis - Pattern Engine */}
                {chartData?.wealth_analysis?.pattern_engine && (
                  <div
                    className="px-3 py-2 text-sm"
                    style={{
                      background: 'color-mix(in srgb, var(--tui-earth) 15%, var(--tui-bg))',
                      border: '1px solid color-mix(in srgb, var(--tui-earth) 40%, var(--tui-bg))'
                    }}
                  >
                    <div className="flex items-center justify-between">
                      <div className="font-medium" style={{ color: 'var(--tui-earth)' }}>{tWealth('title')}</div>
                      <span
                        className="text-xs px-1.5 py-0.5 rounded"
                        style={{
                          background: chartData.wealth_analysis.pattern_engine.severity_level === 'critical' ? 'var(--tui-fire)' :
                            chartData.wealth_analysis.pattern_engine.severity_level === 'major' ? 'var(--tui-accent-orange)' :
                            chartData.wealth_analysis.pattern_engine.severity_level === 'moderate' ? 'var(--tui-earth)' :
                            'var(--tui-wood)',
                          color: 'var(--tui-bg)'
                        }}
                      >
                        {chartData.wealth_analysis.pattern_engine.severity_level || 'balanced'}
                      </span>
                    </div>
                    {/* Pattern Engine Recommendations */}
                    {chartData.wealth_analysis.pattern_engine.recommendations?.map((rec: any, i: number) => (
                      <div key={i} className="mt-1" style={{ color: 'var(--tui-earth)' }}>
                        <span className="font-medium">{rec.title}</span>: {rec.description}
                      </div>
                    ))}
                    {/* Top Patterns */}
                    {chartData.wealth_analysis.pattern_engine.top_patterns?.length > 0 && (
                      <div
                        className="mt-2 text-xs px-2 py-1 rounded"
                        style={{
                          background: 'color-mix(in srgb, var(--tui-earth) 25%, var(--tui-bg))',
                          color: 'var(--tui-earth)'
                        }}
                      >
                        {chartData.wealth_analysis.pattern_engine.top_patterns.slice(0, 3).map((p: any, i: number) => (
                          <div key={i}>
                            {p.chinese_name}: {p.severity?.toFixed(0)} ({p.level})
                          </div>
                        ))}
                      </div>
                    )}
                    {/* Fallback to old analysis */}
                    {!chartData.wealth_analysis.pattern_engine.recommendations?.length && chartData.wealth_analysis.analysis_text && (
                      <div className="mt-1" style={{ color: 'var(--tui-earth)' }}>{getLocalizedAnalysisText(chartData.wealth_analysis, locale)}</div>
                    )}
                  </div>
                )}
                {/* Fallback: Old Wealth Analysis if no pattern engine */}
                {!chartData?.wealth_analysis?.pattern_engine && chartData?.wealth_analysis?.analysis_text && (
                  <div
                    className="px-3 py-2 text-sm"
                    style={{
                      background: 'color-mix(in srgb, var(--tui-earth) 15%, var(--tui-bg))',
                      border: '1px solid color-mix(in srgb, var(--tui-earth) 40%, var(--tui-bg))'
                    }}
                  >
                    <div className="flex items-center justify-between">
                      <div className="font-medium" style={{ color: 'var(--tui-earth)' }}>{tWealth('title')}</div>
                      <span className="text-xs px-1.5 py-0.5 rounded" style={{
                        background: chartData.wealth_analysis.outlook === 'favorable' ? 'var(--tui-wood)' :
                          chartData.wealth_analysis.outlook === 'challenging' ? 'var(--tui-fire)' :
                          'var(--tui-metal)',
                        color: 'var(--tui-bg)'
                      }}>
                        {getOutlookLabel(chartData.wealth_analysis.outlook, 'wealth')}
                      </span>
                    </div>
                    <div className="mt-1" style={{ color: 'var(--tui-earth)' }}>{getLocalizedAnalysisText(chartData.wealth_analysis, locale)}</div>
                  </div>
                )}

                {/* Learning Analysis - Pattern Engine */}
                {chartData?.learning_analysis?.pattern_engine && (
                  <div
                    className="px-3 py-2 text-sm"
                    style={{
                      background: 'color-mix(in srgb, var(--tui-water) 15%, var(--tui-bg))',
                      border: '1px solid color-mix(in srgb, var(--tui-water) 40%, var(--tui-bg))'
                    }}
                  >
                    <div className="flex items-center justify-between">
                      <div className="font-medium" style={{ color: 'var(--tui-water)' }}>{tLearning('title')}</div>
                      <span
                        className="text-xs px-1.5 py-0.5 rounded"
                        style={{
                          background: chartData.learning_analysis.pattern_engine.severity_level === 'critical' ? 'var(--tui-fire)' :
                            chartData.learning_analysis.pattern_engine.severity_level === 'major' ? 'var(--tui-accent-orange)' :
                            chartData.learning_analysis.pattern_engine.severity_level === 'moderate' ? 'var(--tui-earth)' :
                            'var(--tui-wood)',
                          color: 'var(--tui-bg)'
                        }}
                      >
                        {chartData.learning_analysis.pattern_engine.severity_level || 'balanced'}
                      </span>
                    </div>
                    {/* Top Patterns */}
                    {chartData.learning_analysis.pattern_engine.top_patterns?.length > 0 && (
                      <div
                        className="mt-2 text-xs px-2 py-1 rounded"
                        style={{
                          background: 'color-mix(in srgb, var(--tui-water) 25%, var(--tui-bg))',
                          color: 'var(--tui-water)'
                        }}
                      >
                        {chartData.learning_analysis.pattern_engine.top_patterns.slice(0, 3).map((p: any, i: number) => (
                          <div key={i}>
                            {p.chinese_name}: {p.severity?.toFixed(0)} ({p.level})
                          </div>
                        ))}
                      </div>
                    )}
                    {/* Fallback to old analysis */}
                    {chartData.learning_analysis.analysis_text && (
                      <div className="mt-1" style={{ color: 'var(--tui-water)' }}>{getLocalizedAnalysisText(chartData.learning_analysis, locale)}</div>
                    )}
                  </div>
                )}
                {/* Fallback: Old Learning Analysis if no pattern engine */}
                {!chartData?.learning_analysis?.pattern_engine && chartData?.learning_analysis?.analysis_text && (
                  <div
                    className="px-3 py-2 text-sm"
                    style={{
                      background: 'color-mix(in srgb, var(--tui-water) 15%, var(--tui-bg))',
                      border: '1px solid color-mix(in srgb, var(--tui-water) 40%, var(--tui-bg))'
                    }}
                  >
                    <div className="flex items-center justify-between">
                      <div className="font-medium" style={{ color: 'var(--tui-water)' }}>{tLearning('title')}</div>
                      <span className="text-xs px-1.5 py-0.5 rounded" style={{
                        background: chartData.learning_analysis.outlook === 'favorable' ? 'var(--tui-wood)' :
                          chartData.learning_analysis.outlook === 'challenging' ? 'var(--tui-fire)' :
                          'var(--tui-metal)',
                        color: 'var(--tui-bg)'
                      }}>
                        {getOutlookLabel(chartData.learning_analysis.outlook, 'learning')}
                      </span>
                    </div>
                    <div className="mt-1" style={{ color: 'var(--tui-water)' }}>{getLocalizedAnalysisText(chartData.learning_analysis, locale)}</div>
                  </div>
                )}

                {/* Special Stars */}
                {chartData?.special_stars?.length > 0 && (
                  <div
                    className="px-3 py-2 text-sm"
                    style={{
                      background: 'color-mix(in srgb, var(--tui-accent-purple) 15%, var(--tui-bg))',
                      border: '1px solid color-mix(in srgb, var(--tui-accent-purple) 40%, var(--tui-bg))'
                    }}
                  >
                    <div className="font-medium mb-1" style={{ color: 'var(--tui-accent-purple)' }}>神煞 Special Stars</div>
                    <div className="space-y-1">
                      {chartData.special_stars.map((star: any, i: number) => (
                        <div key={i} className="text-xs" style={{ color: 'var(--tui-accent-purple)' }}>
                          <span className="font-medium">{star.chinese_name}</span> ({star.english_name}) - {star.target_branch}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Unified Recommendations */}
                {chartData?.recommendations?.length > 0 && (
                  <div
                    className="px-3 py-2 text-sm"
                    style={{
                      background: 'color-mix(in srgb, var(--tui-wood) 15%, var(--tui-bg))',
                      border: '1px solid color-mix(in srgb, var(--tui-wood) 40%, var(--tui-bg))'
                    }}
                  >
                    <div className="font-medium mb-1" style={{ color: 'var(--tui-wood)' }}>Recommendations</div>
                    <div className="space-y-2">
                      {chartData.recommendations.map((rec: any, i: number) => (
                        <div
                          key={i}
                          className="text-xs p-2 rounded"
                          style={{
                            background: rec.priority === 'high'
                              ? 'color-mix(in srgb, var(--tui-fire) 25%, var(--tui-bg))'
                              : rec.priority === 'medium'
                              ? 'color-mix(in srgb, var(--tui-earth) 25%, var(--tui-bg))'
                              : 'color-mix(in srgb, var(--tui-wood) 25%, var(--tui-bg))',
                            color: rec.priority === 'high'
                              ? 'var(--tui-fire)'
                              : rec.priority === 'medium'
                              ? 'var(--tui-earth)'
                              : 'var(--tui-wood)'
                          }}
                        >
                          <div className="font-medium">[{rec.priority?.toUpperCase()}] {rec.title}</div>
                          <div className="mt-0.5">{rec.description}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Ten Gods Detail - Pillar Analysis (kept for reference) */}
                {chartData?.ten_gods_detail?.warnings?.length > 0 && (
                  <div className="px-3 py-2 tui-bg-alt tui-frame text-sm">
                    <div className="font-medium tui-text mb-1">{tTenGods('warnings_title')}</div>
                    <div className="space-y-1">
                      {chartData.ten_gods_detail.warnings.map((w: any, i: number) => {
                        // Localize Ten God name
                        const tenGodName = locale === 'zh'
                          ? w.ten_god_chinese || w.ten_god
                          : w.ten_god_english || w.ten_god;
                        // Localize pillar name
                        const pillarMap: Record<string, Record<string, string>> = {
                          year: { en: 'year', zh: '年', id: 'tahun' },
                          month: { en: 'month', zh: '月', id: 'bulan' },
                          day: { en: 'day', zh: '日', id: 'hari' },
                          hour: { en: 'hour', zh: '時', id: 'jam' },
                        };
                        const pillarName = pillarMap[w.pillar]?.[locale] || w.pillar;
                        // Get localized message
                        const message = locale === 'zh' ? w.message_chinese :
                          locale === 'id' ? (w.message_id || w.message) :
                          w.message;
                        return (
                          <div key={i} className="tui-text-dim text-xs">
                            <span className="font-medium">{tenGodName}</span> @ {pillarName}: {message}
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}
              </div>
            )}
          </>
        ) : (
          <div className="py-8 text-center tui-text-muted">{tCommon('status.no_data')}</div>
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
                placeholder="Add notes about this period..."
                className="tui-input w-full text-sm px-3 py-2 resize-none min-h-[60px]"
                maxLength={10000}
              />
              <div className="flex justify-between items-center mt-1 text-xs tui-text-muted">
                <span>Press Escape to cancel, Cmd+Enter to save</span>
                {isSaving && <span>{tCommon('actions.loading')}</span>}
              </div>
            </div>
          ) : (
            <div
              onClick={() => setIsEditingNotes(true)}
              className={`text-sm cursor-pointer px-2 py-1 -mx-2 ${
                notes ? 'tui-text-dim' : 'tui-text-muted italic'
              }`}
              title="Click to add notes"
            >
              {notes || 'Click to add notes...'}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
