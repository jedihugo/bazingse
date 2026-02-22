'use client';

import React, { useState, useCallback, useRef, useEffect } from 'react';
import { createLifeEvent, type LifeEventCreate, type LifeEvent } from '@/lib/api';
import { useT } from './LanguageProvider';
import { ACTIONS, EVENT_FORM, LOCATION, PROFILE_FORM } from '@/lib/t';

interface InlineLifeEventFormProps {
  profileId: string;
  onSuccess?: (event: LifeEvent) => void;
  onCancel?: () => void;
  existingDates?: { year: number; month?: number | null; day?: number | null }[];
  className?: string;
}

export default function InlineLifeEventForm({
  profileId,
  onSuccess,
  onCancel,
  existingDates = [],
  className = '',
}: InlineLifeEventFormProps) {
  const { t, tCompact } = useT();
  const currentYear = new Date().getFullYear();

  // Form state
  const [year, setYear] = useState<number | string>(currentYear.toString());
  const [month, setMonth] = useState<number | string>('');
  const [day, setDay] = useState<number | string>('');
  const [location, setLocation] = useState('');
  const [isAbroad, setIsAbroad] = useState(false);
  const [notes, setNotes] = useState('');

  // UI state
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Refs
  const yearRef = useRef<HTMLInputElement>(null);
  const monthRef = useRef<HTMLInputElement>(null);
  const dayRef = useRef<HTMLInputElement>(null);
  const locationRef = useRef<HTMLInputElement>(null);

  // Auto-focus year on mount
  useEffect(() => {
    yearRef.current?.focus();
  }, []);

  // Validation
  const yearNum = typeof year === 'string' ? parseInt(year, 10) : year;
  const monthNum = typeof month === 'string' && month !== '' ? parseInt(month, 10) : null;
  const dayNum = typeof day === 'string' && day !== '' ? parseInt(day, 10) : null;

  const isValidYear = !isNaN(yearNum) && yearNum >= 1900 && yearNum <= 2100;
  const isValid = isValidYear;

  // Check for duplicate
  const isDuplicate = existingDates.some(d =>
    d.year === yearNum &&
    (d.month || null) === monthNum &&
    (d.day || null) === dayNum
  );

  // Handle form submission
  const handleSubmit = useCallback(async () => {
    setError(null);

    if (!isValidYear) {
      setError(t(EVENT_FORM.valid_year));
      return;
    }

    if (isDuplicate) {
      setError(t(EVENT_FORM.duplicate));
      return;
    }

    if (dayNum && !monthNum) {
      setError(t(EVENT_FORM.specify_month));
      return;
    }

    setIsSubmitting(true);

    try {
      const eventData: LifeEventCreate = {
        year: yearNum,
        month: monthNum,
        day: dayNum,
        location: location.trim() || null,
        notes: notes.trim() || null,
        is_abroad: location.trim() ? isAbroad : false,
      };

      const newEvent = await createLifeEvent(profileId, eventData);
      onSuccess?.(newEvent);
    } catch (err) {
      setError(err instanceof Error ? err.message : t(EVENT_FORM.failed_create));
    } finally {
      setIsSubmitting(false);
    }
  }, [isValidYear, isDuplicate, yearNum, monthNum, dayNum, location, notes, profileId, onSuccess]);

  // Handle month input
  const handleMonthChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    if (!/^\d*$/.test(value) || value.length > 2) return;

    const num = parseInt(value, 10);
    if (num > 12) return;

    setMonth(value);

    // Auto-advance: 2 digits OR single digit > 1
    if (value.length === 2 || (value.length === 1 && num > 1)) {
      setTimeout(() => dayRef.current?.focus(), 0);
    }
  }, []);

  // Handle day input
  const handleDayChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    if (!/^\d*$/.test(value) || value.length > 2) return;

    const num = parseInt(value, 10);
    if (num > 31) return;

    setDay(value);

    // Auto-advance: 2 digits
    if (value.length === 2) {
      setTimeout(() => locationRef.current?.focus(), 0);
    }
  }, []);

  // Handle year completion
  const handleYearComplete = useCallback(() => {
    setTimeout(() => monthRef.current?.focus(), 0);
  }, []);

  // Handle backspace for navigation
  const handleFieldKeyDown = useCallback((
    e: React.KeyboardEvent<HTMLInputElement>,
    currentRef: React.RefObject<HTMLInputElement | null>,
    prevRef?: React.RefObject<HTMLInputElement | null>
  ) => {
    if (e.key === 'Backspace' && currentRef.current?.value === '' && prevRef) {
      e.preventDefault();
      prevRef.current?.focus();
    }
  }, []);

  // Keyboard handling for the form wrapper
  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    // Enter to submit (only if not in a textarea)
    if (e.key === 'Enter' && !e.shiftKey) {
      const target = e.target as HTMLElement;
      if (target.tagName !== 'TEXTAREA') {
        e.preventDefault();
        if (isValid && !isDuplicate && !isSubmitting) {
          handleSubmit();
        }
      }
    }

    // Escape to cancel
    if (e.key === 'Escape' && onCancel) {
      e.preventDefault();
      onCancel();
    }
  }, [isValid, isDuplicate, isSubmitting, handleSubmit, onCancel]);

  return (
    <div className={`tui-frame ${className}`} onKeyDown={handleKeyDown}>
      <div className="tui-frame-title">{t(EVENT_FORM.add_title)}</div>
      <table className="tui-table-form">
        <tbody>
          <tr>
            <td>{t(EVENT_FORM.date)}*</td>
            <td>
              <div className="guided-date-input">
                <input
                  ref={yearRef}
                  type="text"
                  inputMode="numeric"
                  pattern="[0-9]*"
                  value={year}
                  onChange={(e) => {
                    const value = e.target.value;
                    if (!/^\d*$/.test(value) || value.length > 4) return;
                    setYear(value);
                    if (value.length === 4) {
                      const num = parseInt(value, 10);
                      if (num >= 1900 && num <= 2100) {
                        handleYearComplete();
                      }
                    }
                  }}
                  placeholder="YYYY"
                  disabled={isSubmitting}
                  className="guided-input-segment guided-input-year tui-input"
                  style={!isValidYear && year !== '' ? { borderColor: 'var(--tui-error)' } : {}}
                  aria-label="Year"
                  autoComplete="off"
                />
                <span className="guided-input-separator">/</span>
                <input
                  ref={monthRef}
                  type="text"
                  inputMode="numeric"
                  pattern="[0-9]*"
                  value={month}
                  onChange={handleMonthChange}
                  onKeyDown={(e) => handleFieldKeyDown(e, monthRef, yearRef)}
                  placeholder="MM"
                  disabled={isSubmitting}
                  className="guided-input-segment guided-input-month tui-input"
                  aria-label="Month (optional)"
                  autoComplete="off"
                />
                <span className="guided-input-separator">/</span>
                <input
                  ref={dayRef}
                  type="text"
                  inputMode="numeric"
                  pattern="[0-9]*"
                  value={day}
                  onChange={handleDayChange}
                  onKeyDown={(e) => handleFieldKeyDown(e, dayRef, monthRef)}
                  placeholder="DD"
                  disabled={isSubmitting || !monthNum}
                  className="guided-input-segment guided-input-day tui-input"
                  style={!monthNum ? { opacity: 0.5 } : {}}
                  aria-label="Day (optional)"
                  autoComplete="off"
                />
              </div>
              <div style={{ fontSize: '0.625rem', color: 'var(--tui-fg-muted)', marginTop: '0.125rem' }}>
                {t(EVENT_FORM.year_required)}
              </div>
            </td>
          </tr>
          <tr>
            <td>{t(EVENT_FORM.location)}</td>
            <td>
              <input
                ref={locationRef}
                type="text"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                placeholder={t(EVENT_FORM.where_happened)}
                maxLength={200}
                disabled={isSubmitting}
                autoComplete="off"
              />
              {location.trim() && (
                <div style={{ marginTop: '0.25rem' }}>
                  <button
                    type="button"
                    onClick={() => setIsAbroad(!isAbroad)}
                    disabled={isSubmitting}
                    className="inline-flex items-center gap-1 px-1.5 py-0.5 text-xs transition-colors"
                    style={{
                      color: isAbroad ? 'var(--tui-water)' : 'var(--tui-fg-muted)',
                      background: isAbroad ? 'color-mix(in srgb, var(--tui-water) 15%, var(--tui-bg))' : 'transparent',
                      border: `1px solid ${isAbroad ? 'var(--tui-water)' : 'var(--tui-border)'}`,
                    }}
                    title={t(LOCATION.abroad_hint)}
                  >
                    <span style={{ fontFamily: 'monospace' }}>{isAbroad ? '[x]' : '[_]'}</span>
                    <span>{tCompact(LOCATION.abroad)}</span>
                  </button>
                </div>
              )}
            </td>
          </tr>
          <tr>
            <td>{t(EVENT_FORM.notes)}</td>
            <td>
              <textarea
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                placeholder={t(EVENT_FORM.what_happened)}
                className="resize-none"
                rows={2}
                maxLength={10000}
                disabled={isSubmitting}
              />
            </td>
          </tr>
        </tbody>
      </table>
      {isDuplicate && (
        <div className="tui-form-error" role="alert">{t(EVENT_FORM.duplicate)}</div>
      )}
      {error && <div className="tui-form-error" role="alert">{error}</div>}
      <div className="tui-form-actions">
        {onCancel && (
          <button type="button" onClick={onCancel} className="tui-btn" disabled={isSubmitting}>
            {tCompact(ACTIONS.cancel)}
          </button>
        )}
        <button
          type="button"
          onClick={handleSubmit}
          className="tui-btn"
          disabled={!isValid || isDuplicate || isSubmitting}
        >
          {isSubmitting ? '...' : tCompact(ACTIONS.add)}
        </button>
      </div>
    </div>
  );
}
