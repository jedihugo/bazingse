'use client';

import { useState, useEffect, useCallback } from 'react';
import { tri, triCompact, AUTH, ACTIONS, STATUS } from '@/lib/t';

const CORRECT_PASSWORD = 'lombok29';
const AUTH_KEY = 'bazingse_auth';

interface PasswordGateProps {
  children: React.ReactNode;
}

export default function PasswordGate({ children }: PasswordGateProps) {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
  const [password, setPassword] = useState('');
  const [error, setError] = useState(false);
  const [shake, setShake] = useState(false);

  // Check auth on mount
  useEffect(() => {
    const auth = sessionStorage.getItem(AUTH_KEY);
    setIsAuthenticated(auth === 'true');
  }, []);

  const handleSubmit = useCallback((e?: React.FormEvent) => {
    e?.preventDefault();

    if (password === CORRECT_PASSWORD) {
      sessionStorage.setItem(AUTH_KEY, 'true');
      setIsAuthenticated(true);
    } else {
      setError(true);
      setShake(true);
      setPassword('');
      setTimeout(() => setShake(false), 500);
    }
  }, [password]);

  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSubmit();
    }
  }, [handleSubmit]);

  // Still checking auth status
  if (isAuthenticated === null) {
    return (
      <div className="min-h-screen tui-bg flex items-center justify-center">
        <div className="tui-text-muted">{tri(STATUS.loading)}</div>
      </div>
    );
  }

  // Authenticated - show app
  if (isAuthenticated) {
    return <>{children}</>;
  }

  // Not authenticated - show password gate
  return (
    <div className="min-h-screen tui-bg flex items-center justify-center p-4">
      <div
        className={`tui-frame p-6 w-full max-w-sm ${shake ? 'animate-shake' : ''}`}
      >
        <div className="text-center mb-6">
          <h1 className="text-xl font-bold tui-text mb-2">BaZingSe</h1>
          <p className="tui-text-muted text-sm">{tri(AUTH.enter_password)}</p>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <div className="flex items-center gap-2">
              <span className="tui-text-water">&gt;</span>
              <input
                type="password"
                value={password}
                onChange={(e) => {
                  setPassword(e.target.value);
                  setError(false);
                }}
                onKeyDown={handleKeyDown}
                className="flex-1 bg-transparent tui-text outline-none border-b tui-border-color focus:border-[var(--tui-water)] transition-colors"
                placeholder={tri(AUTH.password)}
                autoFocus
                autoComplete="off"
              />
            </div>
            {error && (
              <p className="mt-2 text-sm" style={{ color: 'var(--tui-fire)' }}>
                {tri(AUTH.incorrect)}
              </p>
            )}
          </div>

          <button
            type="submit"
            className="w-full tui-btn py-2"
          >
            {triCompact(ACTIONS.enter)}
          </button>
        </form>

        <div className="mt-4 text-center">
          <span className="tui-text-dim text-xs">[Enter] {triCompact(ACTIONS.submit)}</span>
        </div>
      </div>

    </div>
  );
}
