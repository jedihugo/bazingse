'use client';

import React, { type ReactNode } from 'react';
import { useChatFormField } from './ChatFormContext';

interface ChatFormFieldProps {
  id: string;
  label: string;
  order: number;
  children: ReactNode;
  required?: boolean;
  hint?: string;
  error?: string;
  className?: string;
}

export default function ChatFormField({
  id,
  label,
  order,
  children,
  required = false,
  hint,
  error,
  className = '',
}: ChatFormFieldProps) {
  const { isFocused } = useChatFormField(id, order);

  return (
    <div
      className={`chat-field ${isFocused ? 'chat-field-focused' : ''} ${error ? 'chat-field-error' : ''} ${className}`}
      role="group"
      aria-labelledby={`${id}-label`}
    >
      {/* Label with cursor indicator */}
      <div className="chat-field-label-row">
        <span id={`${id}-label`} className="chat-field-label">
          {label}:
          {required && <span className="chat-field-required">*</span>}
        </span>
        <span className={`chat-field-cursor ${isFocused ? 'chat-field-cursor-active' : ''}`}>
          {isFocused ? '>' : ' '}
        </span>
      </div>

      {/* Input area */}
      <div className="chat-field-input">
        {children}
      </div>

      {/* Hint or Error */}
      {(hint || error) && (
        <div className={`chat-field-hint ${error ? 'chat-field-hint-error' : ''}`}>
          {error || hint}
        </div>
      )}
    </div>
  );
}

// Simplified version without label (for inline use)
interface ChatFieldInputProps {
  id: string;
  order: number;
  children: (props: {
    ref: React.RefObject<HTMLElement | null>;
    onFocus: () => void;
    onBlur: () => void;
    isFocused: boolean;
  }) => ReactNode;
}

export function ChatFieldInput({ id, order, children }: ChatFieldInputProps) {
  const { ref, isFocused, handleFocus, handleBlur } = useChatFormField(id, order);

  return (
    <>
      {children({
        ref,
        onFocus: handleFocus,
        onBlur: handleBlur,
        isFocused,
      })}
    </>
  );
}
