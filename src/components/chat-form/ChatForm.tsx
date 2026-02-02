'use client';

import React, { type ReactNode, useCallback, type FormEvent } from 'react';
import { ChatFormProvider, useChatForm } from './ChatFormContext';

interface ChatFormProps {
  title: string;
  children: ReactNode;
  onSubmit: () => void | Promise<void>;
  onCancel?: () => void;
  submitLabel?: string;
  cancelLabel?: string;
  isValid?: boolean;
  error?: string | null;
  className?: string;
}

function ChatFormInner({
  title,
  children,
  onSubmit,
  onCancel,
  submitLabel = 'Submit',
  cancelLabel = 'Cancel',
  isValid = true,
  error,
  className = '',
}: ChatFormProps) {
  const { isSubmitting, setIsSubmitting } = useChatForm();

  const handleSubmit = useCallback(async (e: FormEvent) => {
    e.preventDefault();
    if (!isValid || isSubmitting) return;

    setIsSubmitting(true);
    try {
      await onSubmit();
    } finally {
      setIsSubmitting(false);
    }
  }, [isValid, isSubmitting, onSubmit, setIsSubmitting]);

  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    // Enter to submit (only if not in a textarea)
    if (e.key === 'Enter' && !e.shiftKey) {
      const target = e.target as HTMLElement;
      if (target.tagName !== 'TEXTAREA') {
        e.preventDefault();
        if (isValid && !isSubmitting) {
          handleSubmit(e as unknown as FormEvent);
        }
      }
    }

    // Escape to cancel
    if (e.key === 'Escape' && onCancel) {
      e.preventDefault();
      onCancel();
    }
  }, [isValid, isSubmitting, handleSubmit, onCancel]);

  return (
    <form
      onSubmit={handleSubmit}
      onKeyDown={handleKeyDown}
      className={`chat-form tui-frame ${className}`}
      role="form"
    >
      {/* Title Bar */}
      <div className="chat-form-title tui-frame-title">
        {title}
      </div>

      {/* Form Body */}
      <div className="chat-form-body">
        {children}

        {/* Error Display */}
        {error && (
          <div className="chat-form-error" role="alert">
            {error}
          </div>
        )}
      </div>

      {/* Footer with Shortcuts */}
      <div className="chat-form-footer">
        <div className="chat-form-shortcuts">
          <span className="chat-form-shortcut">
            <kbd>Tab</kbd> Next
          </span>
          {onCancel && (
            <span className="chat-form-shortcut">
              <kbd>Esc</kbd> {cancelLabel}
            </span>
          )}
          <span className="chat-form-shortcut">
            <kbd>Enter</kbd> {submitLabel}
          </span>
        </div>

        {/* Action Buttons */}
        <div className="chat-form-actions">
          {onCancel && (
            <button
              type="button"
              onClick={onCancel}
              className="tui-btn"
              disabled={isSubmitting}
            >
              {cancelLabel}
            </button>
          )}
          <button
            type="submit"
            className="tui-btn chat-form-submit"
            disabled={!isValid || isSubmitting}
          >
            {isSubmitting ? 'Saving...' : submitLabel}
          </button>
        </div>
      </div>
    </form>
  );
}

export default function ChatForm(props: ChatFormProps) {
  return (
    <ChatFormProvider onSubmit={props.onSubmit} onCancel={props.onCancel}>
      <ChatFormInner {...props} />
    </ChatFormProvider>
  );
}
