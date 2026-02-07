'use client';

import React, { useState, useCallback, useRef, useEffect } from 'react';
import { useTranslations } from 'next-intl';
import { ChatForm, GuidedYearInput } from './chat-form';
import { createLifeEvent, type LifeEventCreate, type LifeEvent } from '@/lib/api';

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
  const tForms = useTranslations('forms');
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
      setError('Please enter a valid year (1900-2100)');
      return;
    }

    if (isDuplicate) {
      setError('This date already exists in your life events');
      return;
    }

    if (dayNum && !monthNum) {
      setError('Please specify a month when adding a day');
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
      setError(err instanceof Error ? err.message : 'Failed to create life event');
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
  const handleKeyDown = useCallback((
    e: React.KeyboardEvent<HTMLInputElement>,
    currentRef: React.RefObject<HTMLInputElement | null>,
    prevRef?: React.RefObject<HTMLInputElement | null>
  ) => {
    if (e.key === 'Backspace' && currentRef.current?.value === '' && prevRef) {
      e.preventDefault();
      prevRef.current?.focus();
    }
  }, []);

  return (
    <ChatForm
      title="Add Life Event"
      onSubmit={handleSubmit}
      onCancel={onCancel}
      submitLabel="Add"
      cancelLabel="Cancel"
      isValid={isValid && !isDuplicate}
      error={error}
      className={className}
    >
      {/* Date Fields - Year / Month / Day */}
      <div className="chat-field">
        <div className="chat-field-label-row">
          <span className="chat-field-label">
            Date:<span className="chat-field-required">*</span>
          </span>
          <span className="chat-field-cursor chat-field-cursor-active">{'>'}</span>
        </div>
        <div className="chat-field-input">
          <div className="guided-date-input">
            {/* Year */}
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

            {/* Month */}
            <input
              ref={monthRef}
              type="text"
              inputMode="numeric"
              pattern="[0-9]*"
              value={month}
              onChange={handleMonthChange}
              onKeyDown={(e) => handleKeyDown(e, monthRef, yearRef)}
              placeholder="MM"
              disabled={isSubmitting}
              className="guided-input-segment guided-input-month tui-input"
              aria-label="Month (optional)"
              autoComplete="off"
            />
            <span className="guided-input-separator">/</span>

            {/* Day */}
            <input
              ref={dayRef}
              type="text"
              inputMode="numeric"
              pattern="[0-9]*"
              value={day}
              onChange={handleDayChange}
              onKeyDown={(e) => handleKeyDown(e, dayRef, monthRef)}
              placeholder="DD"
              disabled={isSubmitting || !monthNum}
              className="guided-input-segment guided-input-day tui-input"
              style={!monthNum ? { opacity: 0.5 } : {}}
              aria-label="Day (optional)"
              autoComplete="off"
            />
          </div>
        </div>
        <div className="chat-field-hint">
          Year required, month and day optional
        </div>
      </div>

      {/* Location Field */}
      <div className="chat-field">
        <div className="chat-field-label-row">
          <span className="chat-field-label">
            Location:
            <span className="tui-text-muted" style={{ fontSize: '0.625rem', marginLeft: '0.25rem' }}>
              (optional)
            </span>
          </span>
          <span className="chat-field-cursor">{'>'}</span>
        </div>
        <div className="chat-field-input">
          <input
            ref={locationRef}
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="Where did this happen?"
            className="tui-input w-full"
            maxLength={200}
            disabled={isSubmitting}
            autoComplete="off"
          />
        </div>
        {/* Abroad toggle - only shown when location is filled */}
        {location.trim() && (
          <div className="mt-1">
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
              title={tForms('location.abroad_hint')}
            >
              <span style={{ fontFamily: 'monospace' }}>{isAbroad ? '[x]' : '[_]'}</span>
              <span>{tForms('location.abroad')}</span>
            </button>
          </div>
        )}
      </div>

      {/* Notes Field */}
      <div className="chat-field">
        <div className="chat-field-label-row">
          <span className="chat-field-label">
            Notes:
            <span className="tui-text-muted" style={{ fontSize: '0.625rem', marginLeft: '0.25rem' }}>
              (optional)
            </span>
          </span>
          <span className="chat-field-cursor">{'>'}</span>
        </div>
        <div className="chat-field-input">
          <textarea
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            placeholder="What happened during this period?"
            className="tui-input w-full resize-none"
            rows={2}
            maxLength={10000}
            disabled={isSubmitting}
          />
        </div>
      </div>

      {/* Duplicate warning */}
      {isDuplicate && (
        <div className="chat-form-error" role="alert">
          This date already exists in your life events
        </div>
      )}
    </ChatForm>
  );
}
