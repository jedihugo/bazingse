'use client';

import React, { useCallback, useRef, useEffect } from 'react';

interface SelectorOption<T = string> {
  value: T;
  label: string;
  shortcut?: string; // Single character shortcut (e.g., 'm' for Male)
}

interface InlineSelectorProps<T = string> {
  options: SelectorOption<T>[];
  value: T;
  onChange: (value: T) => void;
  disabled?: boolean;
  className?: string;
  name?: string;
  autoFocus?: boolean;
  onComplete?: () => void;
}

export default function InlineSelector<T extends string = string>({
  options,
  value,
  onChange,
  disabled = false,
  className = '',
  name = 'inline-selector',
  autoFocus = false,
  onComplete,
}: InlineSelectorProps<T>) {
  const containerRef = useRef<HTMLDivElement>(null);
  const currentIndex = options.findIndex(opt => opt.value === value);

  useEffect(() => {
    if (autoFocus && containerRef.current) {
      containerRef.current.focus();
    }
  }, [autoFocus]);

  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (disabled) return;

    // Arrow navigation
    if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
      e.preventDefault();
      const prevIndex = currentIndex > 0 ? currentIndex - 1 : options.length - 1;
      onChange(options[prevIndex].value);
    } else if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
      e.preventDefault();
      const nextIndex = currentIndex < options.length - 1 ? currentIndex + 1 : 0;
      onChange(options[nextIndex].value);
    }

    // Space/Enter to confirm current selection and move to next field
    else if (e.key === ' ' || e.key === 'Enter') {
      e.preventDefault();
      onComplete?.();
    }

    // Shortcut keys (case-insensitive)
    else {
      const key = e.key.toLowerCase();
      const matchingOption = options.find(
        opt => opt.shortcut?.toLowerCase() === key
      );
      if (matchingOption) {
        e.preventDefault();
        onChange(matchingOption.value);
        // Auto-advance after shortcut selection
        setTimeout(() => onComplete?.(), 50);
      }
    }
  }, [disabled, currentIndex, options, onChange, onComplete]);

  const handleOptionClick = useCallback((optValue: T) => {
    if (disabled) return;
    onChange(optValue);
    // Focus container after click for continued keyboard navigation
    containerRef.current?.focus();
  }, [disabled, onChange]);

  return (
    <div
      ref={containerRef}
      className={`inline-selector ${className}`}
      role="radiogroup"
      aria-label={name}
      tabIndex={disabled ? -1 : 0}
      onKeyDown={handleKeyDown}
    >
      {options.map((option) => {
        const isSelected = option.value === value;
        return (
          <label
            key={String(option.value)}
            className={`inline-selector-option ${isSelected ? 'inline-selector-option-selected' : ''}`}
            onClick={() => handleOptionClick(option.value)}
          >
            <input
              type="radio"
              name={name}
              value={String(option.value)}
              checked={isSelected}
              onChange={() => onChange(option.value)}
              disabled={disabled}
              className="sr-only"
              aria-checked={isSelected}
            />
            <span className={isSelected ? 'tui-text' : 'tui-text-muted'}>
              ({isSelected ? '●' : '○'})
              {option.label}
              {option.shortcut && (
                <span className="inline-selector-shortcut">
                  [{option.shortcut.toUpperCase()}]
                </span>
              )}
            </span>
          </label>
        );
      })}
    </div>
  );
}

// Pre-configured gender selector
interface GenderSelectorProps {
  value: 'male' | 'female';
  onChange: (value: 'male' | 'female') => void;
  disabled?: boolean;
  className?: string;
  autoFocus?: boolean;
  onComplete?: () => void;
}

export function GenderSelector({
  value,
  onChange,
  disabled,
  className,
  autoFocus,
  onComplete,
}: GenderSelectorProps) {
  return (
    <InlineSelector<'male' | 'female'>
      options={[
        { value: 'male', label: 'M', shortcut: 'm' },
        { value: 'female', label: 'F', shortcut: 'f' },
      ]}
      value={value}
      onChange={onChange}
      disabled={disabled}
      className={className}
      name="gender"
      autoFocus={autoFocus}
      onComplete={onComplete}
    />
  );
}
