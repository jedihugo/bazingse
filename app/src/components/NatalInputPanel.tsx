'use client';

import { useCallback, useMemo } from 'react';
import { useTranslations } from 'next-intl';
import { type StoredFormData } from '@/lib/api';
import { GuidedDateInput, GuidedTimeInput, GenderSelector } from './chat-form';

interface NatalInputPanelProps {
  formData: StoredFormData;
  updateFormData: (updates: Partial<StoredFormData>) => void;
  isValidBirthDate: boolean;
  showLocation?: boolean;
}

export default function NatalInputPanel({
  formData,
  updateFormData,
  isValidBirthDate,
  showLocation = true,
}: NatalInputPanelProps) {
  const t = useTranslations('forms');

  // Parse birth time into hour and minute
  const [hour, minute] = useMemo(() => {
    if (!formData.birthTime) return ['', ''];
    const [h, m] = formData.birthTime.split(':');
    return [h || '', m || ''];
  }, [formData.birthTime]);

  // Handle date changes
  const handleYearChange = useCallback((value: number | string) => {
    const num = typeof value === 'string' ? parseInt(value, 10) : value;
    updateFormData({ yearInput: isNaN(num) ? 0 : num });
  }, [updateFormData]);

  const handleMonthChange = useCallback((value: number | string) => {
    const num = typeof value === 'string' ? parseInt(value, 10) : value;
    updateFormData({ monthInput: isNaN(num) ? 0 : num });
  }, [updateFormData]);

  const handleDayChange = useCallback((value: number | string) => {
    const num = typeof value === 'string' ? parseInt(value, 10) : value;
    updateFormData({ dayInput: isNaN(num) ? 0 : num });
  }, [updateFormData]);

  // Handle time changes - combine into HH:MM format
  const handleHourChange = useCallback((value: string) => {
    const newTime = `${value.padStart(2, '0')}:${minute.padStart(2, '0')}`;
    updateFormData({ birthTime: newTime });
  }, [minute, updateFormData]);

  const handleMinuteChange = useCallback((value: string) => {
    const newTime = `${hour.padStart(2, '0')}:${value.padStart(2, '0')}`;
    updateFormData({ birthTime: newTime });
  }, [hour, updateFormData]);

  const handleUnknownChange = useCallback((unknown: boolean) => {
    updateFormData({
      unknownHour: unknown,
      birthTime: unknown ? '' : '12:00',
    });
  }, [updateFormData]);

  return (
    <div className="w-full px-2 py-1">
      {/* TUI-style inline form row */}
      <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs">
        {/* Gender Toggle - Using InlineSelector */}
        <div className="flex items-center gap-1">
          <span className="tui-text-dim">Gender:</span>
          <GenderSelector
            value={formData.gender}
            onChange={(value) => updateFormData({ gender: value })}
          />
        </div>

        {/* Date Input - Using GuidedDateInput */}
        <div className="flex items-center gap-1">
          <span className="tui-text-dim">Date:</span>
          <GuidedDateInput
            year={formData.yearInput || ''}
            month={formData.monthInput || ''}
            day={formData.dayInput || ''}
            onYearChange={handleYearChange}
            onMonthChange={handleMonthChange}
            onDayChange={handleDayChange}
            hasError={!isValidBirthDate && (formData.yearInput > 0 || formData.monthInput > 0 || formData.dayInput > 0)}
          />
        </div>

        {/* Time Input - Using GuidedTimeInput */}
        <div className="flex items-center gap-1">
          <span className="tui-text-dim">Hour:</span>
          <GuidedTimeInput
            hour={hour}
            minute={minute}
            onHourChange={handleHourChange}
            onMinuteChange={handleMinuteChange}
            showUnknownToggle={true}
            isUnknown={formData.unknownHour}
            onUnknownChange={handleUnknownChange}
          />
        </div>

        {/* Location Toggle */}
        {showLocation && (
          <div className="flex items-center gap-1">
            <label className="cursor-pointer flex items-center gap-1">
              <input
                type="checkbox"
                checked={formData.showLocation}
                onChange={(e) => updateFormData({ showLocation: e.target.checked })}
                className="sr-only"
              />
              <span className={formData.showLocation ? 'tui-text' : 'tui-text-muted'}>
                [{formData.showLocation ? '×' : ' '}]
              </span>
              <span className="tui-text-dim">Loc</span>
            </label>
            {formData.showLocation && (
              <div className="flex items-center gap-1 ml-1">
                <label className="cursor-pointer">
                  <input
                    type="radio"
                    checked={formData.locationType === 'overseas'}
                    onChange={() => updateFormData({ locationType: 'overseas' })}
                    className="sr-only"
                  />
                  <span className={formData.locationType === 'overseas' ? 'tui-text-water' : 'tui-text-muted'}>
                    ({formData.locationType === 'overseas' ? '●' : '○'})海外
                  </span>
                </label>
                <label className="cursor-pointer">
                  <input
                    type="radio"
                    checked={formData.locationType === 'birthplace'}
                    onChange={() => updateFormData({ locationType: 'birthplace' })}
                    className="sr-only"
                  />
                  <span className={formData.locationType === 'birthplace' ? 'tui-text-earth' : 'tui-text-muted'}>
                    ({formData.locationType === 'birthplace' ? '●' : '○'})故乡
                  </span>
                </label>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
