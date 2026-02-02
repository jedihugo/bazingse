'use client';

import React, { useState, useCallback, useRef, useEffect } from 'react';

interface TypeaheadOption<T = string> {
  value: T;
  label: string;
  searchTerms?: string[]; // Additional terms to match against
}

interface TypeaheadSelectProps<T = string> {
  options: TypeaheadOption<T>[];
  value: T | null;
  onChange: (value: T | null) => void;
  placeholder?: string;
  disabled?: boolean;
  hasError?: boolean;
  className?: string;
  allowClear?: boolean;
  onComplete?: () => void;
  autoFocus?: boolean;
}

export default function TypeaheadSelect<T extends string = string>({
  options,
  value,
  onChange,
  placeholder = 'Type to search...',
  disabled = false,
  hasError = false,
  className = '',
  allowClear = true,
  onComplete,
  autoFocus = false,
}: TypeaheadSelectProps<T>) {
  const [isOpen, setIsOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [highlightedIndex, setHighlightedIndex] = useState(0);

  const inputRef = useRef<HTMLInputElement>(null);
  const listRef = useRef<HTMLUListElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Get selected option label for display
  const selectedOption = options.find(opt => opt.value === value);
  const displayValue = isOpen ? searchTerm : (selectedOption?.label || '');

  // Filter options based on search term
  const filteredOptions = searchTerm
    ? options.filter(opt => {
        const search = searchTerm.toLowerCase();
        const matchesLabel = opt.label.toLowerCase().includes(search);
        const matchesValue = String(opt.value).toLowerCase().includes(search);
        const matchesTerms = opt.searchTerms?.some(term =>
          term.toLowerCase().includes(search)
        );
        return matchesLabel || matchesValue || matchesTerms;
      })
    : options;

  // Auto-focus on mount if requested
  useEffect(() => {
    if (autoFocus && inputRef.current) {
      inputRef.current.focus();
    }
  }, [autoFocus]);

  // Reset highlighted index when filtered options change
  useEffect(() => {
    setHighlightedIndex(0);
  }, [filteredOptions.length]);

  // Scroll highlighted option into view
  useEffect(() => {
    if (isOpen && listRef.current) {
      const highlightedEl = listRef.current.children[highlightedIndex] as HTMLElement;
      if (highlightedEl) {
        highlightedEl.scrollIntoView({ block: 'nearest' });
      }
    }
  }, [highlightedIndex, isOpen]);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setIsOpen(false);
        setSearchTerm('');
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
    setIsOpen(true);
    setHighlightedIndex(0);
  }, []);

  const handleInputFocus = useCallback(() => {
    setIsOpen(true);
    setSearchTerm('');
  }, []);

  const selectOption = useCallback((opt: TypeaheadOption<T>) => {
    onChange(opt.value);
    setIsOpen(false);
    setSearchTerm('');
    onComplete?.();
  }, [onChange, onComplete]);

  const clearSelection = useCallback(() => {
    onChange(null);
    setSearchTerm('');
    inputRef.current?.focus();
  }, [onChange]);

  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (disabled) return;

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        if (!isOpen) {
          setIsOpen(true);
        } else {
          setHighlightedIndex(prev =>
            prev < filteredOptions.length - 1 ? prev + 1 : 0
          );
        }
        break;

      case 'ArrowUp':
        e.preventDefault();
        if (isOpen) {
          setHighlightedIndex(prev =>
            prev > 0 ? prev - 1 : filteredOptions.length - 1
          );
        }
        break;

      case 'Enter':
        e.preventDefault();
        if (isOpen && filteredOptions[highlightedIndex]) {
          selectOption(filteredOptions[highlightedIndex]);
        } else if (!isOpen) {
          setIsOpen(true);
        }
        break;

      case 'Escape':
        e.preventDefault();
        if (isOpen) {
          setIsOpen(false);
          setSearchTerm('');
        }
        break;

      case 'Backspace':
        if (searchTerm === '' && value && allowClear) {
          clearSelection();
        }
        break;

      case 'Tab':
        // Allow natural tab behavior but close dropdown
        if (isOpen) {
          setIsOpen(false);
          setSearchTerm('');
        }
        break;
    }
  }, [disabled, isOpen, filteredOptions, highlightedIndex, searchTerm, value, allowClear, selectOption, clearSelection]);

  const errorStyle = hasError ? { borderColor: 'var(--tui-error)' } : {};

  return (
    <div
      ref={containerRef}
      className={`typeahead-container ${isOpen ? 'typeahead-open' : ''} ${className}`}
    >
      <div className="typeahead-input-wrapper">
        <input
          ref={inputRef}
          type="text"
          value={displayValue}
          onChange={handleInputChange}
          onFocus={handleInputFocus}
          onKeyDown={handleKeyDown}
          placeholder={value ? '' : placeholder}
          disabled={disabled}
          className="typeahead-input tui-input"
          style={errorStyle}
          role="combobox"
          aria-expanded={isOpen}
          aria-haspopup="listbox"
          aria-controls="typeahead-listbox"
          autoComplete="off"
        />

        {/* Clear button */}
        {allowClear && value && !disabled && (
          <button
            type="button"
            onClick={clearSelection}
            className="typeahead-clear tui-btn"
            aria-label="Clear selection"
          >
            ×
          </button>
        )}

        {/* Dropdown indicator */}
        <span className="typeahead-arrow" aria-hidden="true">
          {isOpen ? '▲' : '▼'}
        </span>
      </div>

      {/* Dropdown list */}
      {isOpen && (
        <ul
          ref={listRef}
          id="typeahead-listbox"
          className="typeahead-dropdown"
          role="listbox"
        >
          {filteredOptions.length === 0 ? (
            <li className="typeahead-no-results tui-text-muted">
              No matches found
            </li>
          ) : (
            filteredOptions.map((opt, index) => (
              <li
                key={String(opt.value)}
                onClick={() => selectOption(opt)}
                onMouseEnter={() => setHighlightedIndex(index)}
                className={`typeahead-option ${
                  index === highlightedIndex ? 'typeahead-option-highlighted' : ''
                } ${opt.value === value ? 'typeahead-option-selected' : ''}`}
                role="option"
                aria-selected={opt.value === value}
              >
                {opt.value === value && <span className="typeahead-check">●</span>}
                {opt.label}
              </li>
            ))
          )}
        </ul>
      )}
    </div>
  );
}
