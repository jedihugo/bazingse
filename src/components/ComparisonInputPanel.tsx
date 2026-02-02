'use client';

import { useCallback, useMemo } from 'react';
import { useTranslations } from 'next-intl';
import { type StoredFormData } from '@/lib/api';
import { GuidedTimeInput } from './chat-form';

interface ComparisonInputPanelProps {
  formData: StoredFormData;
  updateFormData: (updates: Partial<StoredFormData>) => void;
  chartData: any;
}

export default function ComparisonInputPanel({
  formData,
  updateFormData,
  chartData,
}: ComparisonInputPanelProps) {
  const t = useTranslations('forms');
  const isEnabled = formData.showAnalysisPeriod;

  // Get 10Y luck timing from the correct location
  const luckMisc = chartData?.hs_10yl?.misc || chartData?.eb_10yl?.misc;
  const tenYrStartYear = luckMisc?.start_date?.split('-')[0];
  const tenYrEndYear = luckMisc?.end_date?.split('-')[0];

  // Check if each level is available (progressive unlocking)
  const hasAnnual = isEnabled && formData.analysisYear;
  const hasMonthly = hasAnnual && formData.includeAnnualLuck && formData.analysisMonth;
  const hasDaily = hasMonthly && formData.includeMonthlyLuck && formData.analysisDay;
  const hasHourly = hasDaily && formData.includeDailyLuck;

  // Parse analysis time into hour and minute
  const [analysisHour, analysisMinute] = useMemo(() => {
    if (!formData.analysisTime) return ['', ''];
    const [h, m] = formData.analysisTime.split(':');
    return [h || '', m || ''];
  }, [formData.analysisTime]);

  // Handle analysis time changes
  const handleAnalysisHourChange = useCallback((value: string) => {
    const newTime = `${value.padStart(2, '0')}:${analysisMinute.padStart(2, '0')}`;
    updateFormData({ analysisTime: newTime });
  }, [analysisMinute, updateFormData]);

  const handleAnalysisMinuteChange = useCallback((value: string) => {
    const newTime = `${analysisHour.padStart(2, '0')}:${value.padStart(2, '0')}`;
    updateFormData({ analysisTime: newTime });
  }, [analysisHour, updateFormData]);

  // Handle year input with auto-advance
  const handleYearChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    // Only allow digits
    if (!/^\d*$/.test(value)) return;

    const num = parseInt(value, 10);
    updateFormData({ analysisYear: isNaN(num) ? null : num });
  }, [updateFormData]);

  // Handle month input with auto-advance
  const handleMonthChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    if (!/^\d*$/.test(value) || value.length > 2) return;

    const num = parseInt(value, 10);
    if (num > 12) return;

    updateFormData({ analysisMonth: isNaN(num) ? null : num });
  }, [updateFormData]);

  // Handle day input with auto-advance
  const handleDayChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    if (!/^\d*$/.test(value) || value.length > 2) return;

    const num = parseInt(value, 10);
    if (num > 31) return;

    updateFormData({ analysisDay: isNaN(num) ? null : num });
  }, [updateFormData]);

  return (
    <div className="px-2 py-1">
      {/* TUI-style inline form row */}
      <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs">
        {/* Time Travel Toggle */}
        <label className="cursor-pointer flex items-center gap-1">
          <input
            type="checkbox"
            checked={formData.showAnalysisPeriod}
            onChange={(e) => {
              const showAnalysis = e.target.checked;
              updateFormData({
                showAnalysisPeriod: showAnalysis,
                analysisYear: showAnalysis ? new Date().getFullYear() : null,
              });
            }}
            className="sr-only"
          />
          <span className={isEnabled ? 'tui-text-purple' : 'tui-text-muted'}>
            [{isEnabled ? '×' : ' '}]
          </span>
          <span className="tui-text-purple">Time Travel</span>
        </label>

        {/* Year Input */}
        {isEnabled && (
          <>
            <div className="flex items-center gap-1">
              <label className="cursor-pointer flex items-center gap-0.5">
                <input
                  type="checkbox"
                  checked={formData.includeAnnualLuck}
                  onChange={(e) => updateFormData({ includeAnnualLuck: e.target.checked })}
                  className="sr-only"
                />
                <span className={formData.includeAnnualLuck ? 'tui-text' : 'tui-text-muted'}>
                  [{formData.includeAnnualLuck ? '×' : ' '}]
                </span>
              </label>
              <span className="tui-text-dim">Year:</span>
              <input
                value={formData.analysisYear || ''}
                onChange={handleYearChange}
                type="text"
                inputMode="numeric"
                pattern="[0-9]*"
                placeholder="YYYY"
                className={`tui-input guided-input-year text-center ${formData.includeAnnualLuck ? '' : 'opacity-50'}`}
                disabled={!formData.includeAnnualLuck}
                autoComplete="off"
              />
            </div>

            {/* Month Input - unlocks after Annual */}
            {hasAnnual && formData.includeAnnualLuck && (
              <div className="flex items-center gap-1">
                <label className="cursor-pointer flex items-center gap-0.5">
                  <input
                    type="checkbox"
                    checked={formData.includeMonthlyLuck}
                    onChange={(e) => updateFormData({ includeMonthlyLuck: e.target.checked })}
                    className="sr-only"
                  />
                  <span className={formData.includeMonthlyLuck ? 'tui-text' : 'tui-text-muted'}>
                    [{formData.includeMonthlyLuck ? '×' : ' '}]
                  </span>
                </label>
                <span className="tui-text-dim">Month:</span>
                <input
                  value={formData.analysisMonth || ''}
                  onChange={handleMonthChange}
                  type="text"
                  inputMode="numeric"
                  pattern="[0-9]*"
                  placeholder="MM"
                  className={`tui-input guided-input-month text-center ${formData.includeMonthlyLuck ? '' : 'opacity-50'}`}
                  disabled={!formData.includeMonthlyLuck}
                  autoComplete="off"
                />
              </div>
            )}

            {/* Day Input - unlocks after Monthly */}
            {hasMonthly && formData.includeMonthlyLuck && (
              <div className="flex items-center gap-1">
                <label className="cursor-pointer flex items-center gap-0.5">
                  <input
                    type="checkbox"
                    checked={formData.includeDailyLuck}
                    onChange={(e) => updateFormData({ includeDailyLuck: e.target.checked })}
                    className="sr-only"
                  />
                  <span className={formData.includeDailyLuck ? 'tui-text' : 'tui-text-muted'}>
                    [{formData.includeDailyLuck ? '×' : ' '}]
                  </span>
                </label>
                <span className="tui-text-dim">Day:</span>
                <input
                  value={formData.analysisDay || ''}
                  onChange={handleDayChange}
                  type="text"
                  inputMode="numeric"
                  pattern="[0-9]*"
                  placeholder="DD"
                  className={`tui-input guided-input-day text-center ${formData.includeDailyLuck ? '' : 'opacity-50'}`}
                  disabled={!formData.includeDailyLuck}
                  autoComplete="off"
                />
              </div>
            )}

            {/* Hour Input - unlocks after Daily, using GuidedTimeInput */}
            {hasDaily && formData.includeDailyLuck && (
              <div className="flex items-center gap-1">
                <label className="cursor-pointer flex items-center gap-0.5">
                  <input
                    type="checkbox"
                    checked={formData.includeHourlyLuck}
                    onChange={(e) => updateFormData({ includeHourlyLuck: e.target.checked })}
                    className="sr-only"
                  />
                  <span className={formData.includeHourlyLuck ? 'tui-text' : 'tui-text-muted'}>
                    [{formData.includeHourlyLuck ? '×' : ' '}]
                  </span>
                </label>
                <span className="tui-text-dim">Hour:</span>
                <div className={formData.includeHourlyLuck ? '' : 'opacity-50'}>
                  <GuidedTimeInput
                    hour={analysisHour}
                    minute={analysisMinute}
                    onHourChange={handleAnalysisHourChange}
                    onMinuteChange={handleAnalysisMinuteChange}
                    disabled={!formData.includeHourlyLuck}
                  />
                </div>
              </div>
            )}

            {/* 10-Year Luck indicator */}
            {chartData?.analysis_info?.has_luck_pillar && (
              <div className="flex items-center gap-1 tui-text-dim">
                <span>10Y:</span>
                <span className="tui-text-purple">
                  {tenYrStartYear}-{tenYrEndYear}
                </span>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
