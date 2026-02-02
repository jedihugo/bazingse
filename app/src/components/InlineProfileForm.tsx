'use client';

import React, { useState, useCallback, useRef, useEffect } from 'react';
import { ChatForm, GuidedDateInput, GuidedTimeInput, GenderSelector } from './chat-form';
import { createProfile, type ProfileCreate } from '@/lib/api';

interface InlineProfileFormProps {
  onSuccess?: (profile: { id: string; name: string }) => void;
  onCancel?: () => void;
  className?: string;
}

export default function InlineProfileForm({
  onSuccess,
  onCancel,
  className = '',
}: InlineProfileFormProps) {
  // Form state
  const [name, setName] = useState('');
  const [year, setYear] = useState<number | string>('');
  const [month, setMonth] = useState<number | string>('');
  const [day, setDay] = useState<number | string>('');
  const [hour, setHour] = useState('');
  const [minute, setMinute] = useState('');
  const [unknownTime, setUnknownTime] = useState(false);
  const [gender, setGender] = useState<'male' | 'female'>('male');

  // UI state
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Refs for focus management
  const nameRef = useRef<HTMLInputElement>(null);
  const yearRef = useRef<HTMLInputElement>(null);
  const hourRef = useRef<HTMLInputElement>(null);

  // Auto-focus name field on mount
  useEffect(() => {
    nameRef.current?.focus();
  }, []);

  // Validation
  const isValidDate = useCallback((): boolean => {
    const y = typeof year === 'string' ? parseInt(year, 10) : year;
    const m = typeof month === 'string' ? parseInt(month, 10) : month;
    const d = typeof day === 'string' ? parseInt(day, 10) : day;

    if (isNaN(y) || isNaN(m) || isNaN(d)) return false;
    if (y < 1900 || y > 2100) return false;
    if (m < 1 || m > 12) return false;
    if (d < 1 || d > 31) return false;

    // Check for valid date
    const date = new Date(y, m - 1, d);
    return date.getFullYear() === y && date.getMonth() === m - 1 && date.getDate() === d;
  }, [year, month, day]);

  const isValid = name.trim().length > 0 && isValidDate();

  // Format date for API
  const formatDate = (): string => {
    const y = typeof year === 'string' ? year.padStart(4, '0') : String(year).padStart(4, '0');
    const m = typeof month === 'string' ? month.padStart(2, '0') : String(month).padStart(2, '0');
    const d = typeof day === 'string' ? day.padStart(2, '0') : String(day).padStart(2, '0');
    return `${y}-${m}-${d}`;
  };

  // Format time for API
  const formatTime = (): string | undefined => {
    if (unknownTime) return undefined;
    if (!hour && !minute) return undefined;
    const h = hour.padStart(2, '0');
    const min = minute.padStart(2, '0');
    return `${h}:${min}`;
  };

  // Handle form submission
  const handleSubmit = useCallback(async () => {
    if (!isValid) {
      setError('Please fill in all required fields');
      return;
    }

    setError(null);
    setIsSubmitting(true);

    try {
      const data: ProfileCreate = {
        name: name.trim(),
        birth_date: formatDate(),
        birth_time: formatTime(),
        gender,
      };

      const profile = await createProfile(data);
      onSuccess?.({ id: profile.id, name: profile.name });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create profile');
    } finally {
      setIsSubmitting(false);
    }
  }, [isValid, name, gender, formatDate, formatTime, onSuccess]);

  // Handle field transitions (auto-advance)
  const handleNameKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'Enter' || e.key === 'Tab') {
      if (e.key === 'Enter') e.preventDefault();
      // Focus year input after name
      setTimeout(() => yearRef.current?.focus(), 0);
    }
  }, []);

  const handleDateComplete = useCallback(() => {
    // Focus hour input after date
    setTimeout(() => hourRef.current?.focus(), 0);
  }, []);

  const handleTimeComplete = useCallback(() => {
    // Form is complete - no need to advance further
    // User can press Enter to submit
  }, []);

  return (
    <ChatForm
      title="Create New Profile"
      onSubmit={handleSubmit}
      onCancel={onCancel}
      submitLabel="Create"
      cancelLabel="Cancel"
      isValid={isValid}
      error={error}
      className={className}
    >
      {/* Name Field */}
      <div className="chat-field">
        <div className="chat-field-label-row">
          <span className="chat-field-label">
            Name:<span className="chat-field-required">*</span>
          </span>
          <span className="chat-field-cursor chat-field-cursor-active">{'>'}</span>
        </div>
        <div className="chat-field-input">
          <input
            ref={nameRef}
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            onKeyDown={handleNameKeyDown}
            placeholder="Enter name"
            className="tui-input w-full"
            disabled={isSubmitting}
            autoComplete="off"
          />
        </div>
      </div>

      {/* Birth Date Field */}
      <div className="chat-field">
        <div className="chat-field-label-row">
          <span className="chat-field-label">
            Birth Date:<span className="chat-field-required">*</span>
          </span>
          <span className="chat-field-cursor">{'>'}</span>
        </div>
        <div className="chat-field-input">
          <GuidedDateInput
            year={year}
            month={month}
            day={day}
            onYearChange={setYear}
            onMonthChange={setMonth}
            onDayChange={setDay}
            onComplete={handleDateComplete}
            disabled={isSubmitting}
            hasError={year !== '' && month !== '' && day !== '' && !isValidDate()}
            yearRef={yearRef}
          />
        </div>
        {year !== '' && month !== '' && day !== '' && !isValidDate() && (
          <div className="chat-field-hint chat-field-hint-error">
            Invalid date
          </div>
        )}
      </div>

      {/* Birth Time Field */}
      <div className="chat-field">
        <div className="chat-field-label-row">
          <span className="chat-field-label">
            Birth Time:
            <span className="tui-text-muted" style={{ fontSize: '0.625rem', marginLeft: '0.25rem' }}>
              (optional)
            </span>
          </span>
          <span className="chat-field-cursor">{'>'}</span>
        </div>
        <div className="chat-field-input">
          <GuidedTimeInput
            hour={hour}
            minute={minute}
            onHourChange={setHour}
            onMinuteChange={setMinute}
            onComplete={handleTimeComplete}
            disabled={isSubmitting}
            showUnknownToggle={true}
            isUnknown={unknownTime}
            onUnknownChange={setUnknownTime}
            hourRef={hourRef}
          />
        </div>
      </div>

      {/* Gender Field */}
      <div className="chat-field">
        <div className="chat-field-label-row">
          <span className="chat-field-label">
            Gender:<span className="chat-field-required">*</span>
          </span>
          <span className="chat-field-cursor">{'>'}</span>
        </div>
        <div className="chat-field-input">
          <GenderSelector
            value={gender}
            onChange={setGender}
            disabled={isSubmitting}
          />
        </div>
        <div className="chat-field-hint">
          Press M or F to select
        </div>
      </div>
    </ChatForm>
  );
}
