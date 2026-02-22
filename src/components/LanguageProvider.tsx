'use client';

import { createContext, useContext, useState, useEffect, useCallback, useMemo } from 'react';
import { type TriEntry, type LangMode, tFor, tCompactFor, tPillarFor } from '@/lib/t';

interface LanguageContextValue {
  mode: LangMode;
  setMode: (mode: LangMode) => void;
  t: (e: TriEntry) => string;
  tCompact: (e: TriEntry) => string;
  tPillar: (e: TriEntry) => string;
}

const LanguageContext = createContext<LanguageContextValue | null>(null);

const STORAGE_KEY = 'bazingse_lang';

export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const [mode, setModeState] = useState<LangMode>('en-zh');
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY) as LangMode | null;
    if (saved && ['en', 'id', 'zh', 'en-zh'].includes(saved)) {
      setModeState(saved);
    }
    setMounted(true);
  }, []);

  const setMode = useCallback((newMode: LangMode) => {
    setModeState(newMode);
    localStorage.setItem(STORAGE_KEY, newMode);
  }, []);

  const t = useCallback((e: TriEntry) => tFor(mode, e), [mode]);
  const tCompact = useCallback((e: TriEntry) => tCompactFor(mode, e), [mode]);
  const tPillar = useCallback((e: TriEntry) => tPillarFor(mode, e), [mode]);

  const value = useMemo(() => ({
    mode, setMode, t, tCompact, tPillar,
  }), [mode, setMode, t, tCompact, tPillar]);

  // Prevent hydration mismatch — render with default mode until mounted
  if (!mounted) {
    return <LanguageContext.Provider value={value}>{children}</LanguageContext.Provider>;
  }

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useT() {
  const ctx = useContext(LanguageContext);
  if (!ctx) throw new Error('useT must be used within LanguageProvider');
  return ctx;
}
