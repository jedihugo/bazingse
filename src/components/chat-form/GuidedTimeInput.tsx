'use client';

import React, { useRef, useCallback, useEffect, useState } from 'react';

interface GuidedTimeInputProps {
  hour: string;
  minute: string;
  onHourChange: (value: string) => void;
  onMinuteChange: (value: string) => void;
  onComplete?: () => void;
  disabled?: boolean;
  hasError?: boolean;
  showUnknownToggle?: boolean;
  isUnknown?: boolean;
  onUnknownChange?: (unknown: boolean) => void;
  className?: string;
  autoFocus?: boolean;
  hourRef?: React.RefObject<HTMLInputElement | null>;
}

export default function GuidedTimeInput({
  hour,
  minute,
  onHourChange,
  onMinuteChange,
  onComplete,
  disabled = false,
  hasError = false,
  showUnknownToggle = false,
  isUnknown = false,
  onUnknownChange,
  className = '',
  autoFocus = false,
  hourRef: externalHourRef,
}: GuidedTimeInputProps) {
  const internalHourRef = useRef<HTMLInputElement>(null);
  const hourRef = externalHourRef || internalHourRef;
  const minuteRef = useRef<HTMLInputElement>(null);
  const [showUnknown, setShowUnknown] = useState(isUnknown);

  useEffect(() => {
    setShowUnknown(isUnknown);
  }, [isUnknown]);

  useEffect(() => {
    if (autoFocus && hourRef.current && !showUnknown) {
      hourRef.current.focus();
    }
  }, [autoFocus, hourRef, showUnknown]);

  const handleHourChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    // Only allow digits, max 2 characters
    if (!/^\d*$/.test(value) || value.length > 2) return;

    const num = parseInt(value, 10);
    if (num > 23) return;

    onHourChange(value);

    // Auto-advance: 2 digits OR single digit > 2 (3-9 can only be 03-09, 10-19, 20-23)
    if (value.length === 2 || (value.length === 1 && num > 2)) {
      setTimeout(() => minuteRef.current?.focus(), 0);
    }
  }, [onHourChange]);

  const handleMinuteChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    // Only allow digits, max 2 characters
    if (!/^\d*$/.test(value) || value.length > 2) return;

    const num = parseInt(value, 10);
    if (num > 59) return;

    onMinuteChange(value);

    // Auto-complete: 2 digits -> trigger onComplete
    if (value.length === 2) {
      onComplete?.();
    }
  }, [onMinuteChange, onComplete]);

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

  const handleUnknownToggle = useCallback(() => {
    const newUnknown = !showUnknown;
    setShowUnknown(newUnknown);
    onUnknownChange?.(newUnknown);

    if (newUnknown) {
      // Clear time values when marking as unknown
      onHourChange('');
      onMinuteChange('');
    } else {
      // Set default time when unmarking as unknown
      onHourChange('12');
      onMinuteChange('00');
      setTimeout(() => hourRef.current?.focus(), 0);
    }
  }, [showUnknown, onUnknownChange, onHourChange, onMinuteChange, hourRef]);

  const errorStyle = hasError ? { borderColor: 'var(--tui-error)' } : {};

  if (showUnknown) {
    return (
      <div className={`guided-time-input ${className}`} role="group" aria-label="Time input">
        <span className="guided-time-unknown tui-input tui-text-muted">??:??</span>
        {showUnknownToggle && (
          <button
            type="button"
            onClick={handleUnknownToggle}
            className="guided-time-toggle tui-btn tui-border-bright"
            title="I know the birth time"
            aria-pressed={showUnknown}
          >
            ?
          </button>
        )}
      </div>
    );
  }

  return (
    <div className={`guided-time-input ${className}`} role="group" aria-label="Time input">
      {/* Hour */}
      <input
        ref={hourRef as React.RefObject<HTMLInputElement>}
        type="text"
        inputMode="numeric"
        pattern="[0-9]*"
        value={hour}
        onChange={handleHourChange}
        onKeyDown={(e) => handleKeyDown(e, hourRef as React.RefObject<HTMLInputElement>)}
        placeholder="HH"
        disabled={disabled}
        className="guided-input-segment guided-input-hour tui-input"
        style={errorStyle}
        aria-label="Hour"
        autoComplete="off"
      />
      <span className="guided-input-separator">:</span>

      {/* Minute */}
      <input
        ref={minuteRef}
        type="text"
        inputMode="numeric"
        pattern="[0-9]*"
        value={minute}
        onChange={handleMinuteChange}
        onKeyDown={(e) => handleKeyDown(e, { current: minuteRef.current }, hourRef as React.RefObject<HTMLInputElement>)}
        placeholder="MM"
        disabled={disabled}
        className="guided-input-segment guided-input-minute tui-input"
        style={errorStyle}
        aria-label="Minute"
        autoComplete="off"
      />

      {/* Unknown toggle button */}
      {showUnknownToggle && (
        <button
          type="button"
          onClick={handleUnknownToggle}
          className="guided-time-toggle tui-btn"
          title="I don't know the birth time"
          aria-pressed={showUnknown}
        >
          ?
        </button>
      )}
    </div>
  );
}
