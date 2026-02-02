'use client';

import React, { createContext, useContext, useState, useCallback, useRef, type ReactNode, type RefObject } from 'react';

interface FieldRegistration {
  id: string;
  ref: RefObject<HTMLElement | null>;
  order: number;
}

interface ChatFormContextValue {
  // Current focused field
  focusedFieldId: string | null;
  setFocusedFieldId: (id: string | null) => void;

  // Field registration for Tab navigation
  registerField: (id: string, ref: RefObject<HTMLElement | null>, order: number) => void;
  unregisterField: (id: string) => void;

  // Navigation
  focusNextField: () => void;
  focusPreviousField: () => void;
  focusField: (id: string) => void;

  // Form state
  isSubmitting: boolean;
  setIsSubmitting: (value: boolean) => void;
}

const ChatFormContext = createContext<ChatFormContextValue | null>(null);

interface ChatFormProviderProps {
  children: ReactNode;
  onSubmit?: () => void;
  onCancel?: () => void;
}

export function ChatFormProvider({ children, onSubmit, onCancel }: ChatFormProviderProps) {
  const [focusedFieldId, setFocusedFieldId] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const fieldsRef = useRef<Map<string, FieldRegistration>>(new Map());

  const registerField = useCallback((id: string, ref: RefObject<HTMLElement | null>, order: number) => {
    fieldsRef.current.set(id, { id, ref, order });
  }, []);

  const unregisterField = useCallback((id: string) => {
    fieldsRef.current.delete(id);
  }, []);

  const getSortedFields = useCallback(() => {
    return Array.from(fieldsRef.current.values()).sort((a, b) => a.order - b.order);
  }, []);

  const focusField = useCallback((id: string) => {
    const field = fieldsRef.current.get(id);
    if (field?.ref.current) {
      field.ref.current.focus();
      setFocusedFieldId(id);
    }
  }, []);

  const focusNextField = useCallback(() => {
    const fields = getSortedFields();
    if (fields.length === 0) return;

    const currentIndex = fields.findIndex(f => f.id === focusedFieldId);
    const nextIndex = currentIndex < fields.length - 1 ? currentIndex + 1 : 0;
    const nextField = fields[nextIndex];

    if (nextField?.ref.current) {
      nextField.ref.current.focus();
      setFocusedFieldId(nextField.id);
    }
  }, [focusedFieldId, getSortedFields]);

  const focusPreviousField = useCallback(() => {
    const fields = getSortedFields();
    if (fields.length === 0) return;

    const currentIndex = fields.findIndex(f => f.id === focusedFieldId);
    const prevIndex = currentIndex > 0 ? currentIndex - 1 : fields.length - 1;
    const prevField = fields[prevIndex];

    if (prevField?.ref.current) {
      prevField.ref.current.focus();
      setFocusedFieldId(prevField.id);
    }
  }, [focusedFieldId, getSortedFields]);

  // Handle global keyboard events
  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'Escape' && onCancel) {
      e.preventDefault();
      onCancel();
    }

    // Note: Enter to submit is handled at the form level, not here
    // Tab navigation is handled natively with field order
  }, [onCancel]);

  const value: ChatFormContextValue = {
    focusedFieldId,
    setFocusedFieldId,
    registerField,
    unregisterField,
    focusNextField,
    focusPreviousField,
    focusField,
    isSubmitting,
    setIsSubmitting,
  };

  return (
    <ChatFormContext.Provider value={value}>
      <div onKeyDown={handleKeyDown}>
        {children}
      </div>
    </ChatFormContext.Provider>
  );
}

export function useChatForm() {
  const context = useContext(ChatFormContext);
  if (!context) {
    throw new Error('useChatForm must be used within a ChatFormProvider');
  }
  return context;
}

// Hook for registering a field with the form context
export function useChatFormField(id: string, order: number) {
  const context = useContext(ChatFormContext);
  const ref = useRef<HTMLElement | null>(null);

  React.useEffect(() => {
    if (context) {
      context.registerField(id, ref, order);
      return () => context.unregisterField(id);
    }
  }, [context, id, order]);

  const isFocused = context?.focusedFieldId === id;

  const handleFocus = useCallback(() => {
    context?.setFocusedFieldId(id);
  }, [context, id]);

  const handleBlur = useCallback(() => {
    // Small delay to allow focus to move to another field
    setTimeout(() => {
      if (context?.focusedFieldId === id) {
        context?.setFocusedFieldId(null);
      }
    }, 100);
  }, [context, id]);

  return {
    ref,
    isFocused,
    handleFocus,
    handleBlur,
    focusNext: context?.focusNextField,
    focusPrevious: context?.focusPreviousField,
  };
}

export default ChatFormContext;
