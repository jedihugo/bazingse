'use client';

import React, { useRef, useCallback, useEffect } from 'react';

interface GuidedDateInputProps {
  year: number | string;
  month: number | string;
  day: number | string;
  onYearChange: (value: number | string) => void;
  onMonthChange: (value: number | string) => void;
  onDayChange: (value: number | string) => void;
  onComplete?: () => void;
  disabled?: boolean;
  hasError?: boolean;
  yearPlaceholder?: string;
  monthPlaceholder?: string;
  dayPlaceholder?: string;
  className?: string;
  // Allows auto-focus on year when component mounts
  autoFocusYear?: boolean;
  // Ref forwarding for external focus control
  yearRef?: React.RefObject<HTMLInputElement | null>;
}

export default function GuidedDateInput({
  year,
  month,
  day,
  onYearChange,
  onMonthChange,
  onDayChange,
  onComplete,
  disabled = false,
  hasError = false,
  yearPlaceholder = 'YYYY',
  monthPlaceholder = 'MM',
  dayPlaceholder = 'DD',
  className = '',
  autoFocusYear = false,
  yearRef: externalYearRef,
}: GuidedDateInputProps) {
  const internalYearRef = useRef<HTMLInputElement>(null);
  const yearRef = externalYearRef || internalYearRef;
  const monthRef = useRef<HTMLInputElement>(null);
  const dayRef = useRef<HTMLInputElement>(null);

  // Auto-focus year on mount if requested
  useEffect(() => {
    if (autoFocusYear && yearRef.current) {
      yearRef.current.focus();
    }
  }, [autoFocusYear, yearRef]);

  const isValidYear = (value: string): boolean => {
    const num = parseInt(value, 10);
    return !isNaN(num) && num >= 1900 && num <= 2100;
  };

  const handleYearChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    // Only allow digits, max 4 characters
    if (!/^\d*$/.test(value) || value.length > 4) return;

    onYearChange(value);

    // Auto-advance: 4 digits AND valid year -> move to month
    if (value.length === 4 && isValidYear(value)) {
      setTimeout(() => monthRef.current?.focus(), 0);
    }
  }, [onYearChange]);

  const handleMonthChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    // Only allow digits, max 2 characters
    if (!/^\d*$/.test(value) || value.length > 2) return;

    const num = parseInt(value, 10);

    // Clamp to valid month range
    if (num > 12) return;

    onMonthChange(value);

    // Auto-advance: 2 digits OR single digit > 1 (can only be 2-9) -> move to day
    if (value.length === 2 || (value.length === 1 && num > 1)) {
      setTimeout(() => dayRef.current?.focus(), 0);
    }
  }, [onMonthChange]);

  const handleDayChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    // Only allow digits, max 2 characters
    if (!/^\d*$/.test(value) || value.length > 2) return;

    const num = parseInt(value, 10);

    // Clamp to valid day range
    if (num > 31) return;

    onDayChange(value);

    // Auto-complete: 2 digits -> trigger onComplete
    if (value.length === 2) {
      onComplete?.();
    }
  }, [onDayChange, onComplete]);

  // Handle backspace to move to previous field when empty
  const handleKeyDown = useCallback((
    e: React.KeyboardEvent<HTMLInputElement>,
    currentRef: React.RefObject<HTMLInputElement | null>,
    prevRef?: React.RefObject<HTMLInputElement | null>
  ) => {
    if (e.key === 'Backspace' && currentRef.current?.value === '' && prevRef) {
      e.preventDefault();
      prevRef.current?.focus();
    }

    // Allow Tab to naturally move focus
    // Arrow keys within the same input work naturally
  }, []);

  const errorStyle = hasError ? { borderColor: 'var(--tui-error)' } : {};

  return (
    <div className={`guided-date-input ${className}`} role="group" aria-label="Date input">
      {/* Year */}
      <input
        ref={yearRef as React.RefObject<HTMLInputElement>}
        type="text"
        inputMode="numeric"
        pattern="[0-9]*"
        value={year}
        onChange={handleYearChange}
        onKeyDown={(e) => handleKeyDown(e, yearRef as React.RefObject<HTMLInputElement>)}
        placeholder={yearPlaceholder}
        disabled={disabled}
        className="guided-input-segment guided-input-year tui-input"
        style={errorStyle}
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
        onKeyDown={(e) => handleKeyDown(e, { current: monthRef.current }, yearRef as React.RefObject<HTMLInputElement>)}
        placeholder={monthPlaceholder}
        disabled={disabled}
        className="guided-input-segment guided-input-month tui-input"
        style={errorStyle}
        aria-label="Month"
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
        onKeyDown={(e) => handleKeyDown(e, { current: dayRef.current }, { current: monthRef.current })}
        placeholder={dayPlaceholder}
        disabled={disabled}
        className="guided-input-segment guided-input-day tui-input"
        style={errorStyle}
        aria-label="Day"
        autoComplete="off"
      />
    </div>
  );
}

// Year-only variant for life events
interface GuidedYearInputProps {
  year: number | string;
  onYearChange: (value: number | string) => void;
  onComplete?: () => void;
  disabled?: boolean;
  hasError?: boolean;
  placeholder?: string;
  className?: string;
  autoFocus?: boolean;
}

export function GuidedYearInput({
  year,
  onYearChange,
  onComplete,
  disabled = false,
  hasError = false,
  placeholder = 'YYYY',
  className = '',
  autoFocus = false,
}: GuidedYearInputProps) {
  const yearRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (autoFocus && yearRef.current) {
      yearRef.current.focus();
    }
  }, [autoFocus]);

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    if (!/^\d*$/.test(value) || value.length > 4) return;

    onYearChange(value);

    if (value.length === 4) {
      const num = parseInt(value, 10);
      if (num >= 1900 && num <= 2100) {
        onComplete?.();
      }
    }
  }, [onYearChange, onComplete]);

  const errorStyle = hasError ? { borderColor: 'var(--tui-error)' } : {};

  return (
    <input
      ref={yearRef}
      type="text"
      inputMode="numeric"
      pattern="[0-9]*"
      value={year}
      onChange={handleChange}
      placeholder={placeholder}
      disabled={disabled}
      className={`guided-input-segment guided-input-year tui-input ${className}`}
      style={errorStyle}
      aria-label="Year"
      autoComplete="off"
    />
  );
}
