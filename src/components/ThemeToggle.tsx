'use client';

import { useEffect, useState } from 'react';

type Theme = 'system' | 'light' | 'dark';

export default function ThemeToggle() {
  const [theme, setTheme] = useState<Theme>('system');
  const [mounted, setMounted] = useState(false);

  // Load saved theme on mount
  useEffect(() => {
    setMounted(true);
    const saved = localStorage.getItem('theme') as Theme | null;
    if (saved && ['system', 'light', 'dark'].includes(saved)) {
      setTheme(saved);
      applyTheme(saved);
    }
  }, []);

  // Apply theme to document
  const applyTheme = (newTheme: Theme) => {
    if (newTheme === 'system') {
      document.documentElement.removeAttribute('data-theme');
    } else {
      document.documentElement.setAttribute('data-theme', newTheme);
    }
  };

  // Cycle through themes: system -> dark -> light -> system
  const cycleTheme = () => {
    const nextTheme: Theme = theme === 'system' ? 'dark' : theme === 'dark' ? 'light' : 'system';
    setTheme(nextTheme);
    localStorage.setItem('theme', nextTheme);
    applyTheme(nextTheme);
  };

  // Prevent hydration mismatch - show nothing until mounted
  if (!mounted) {
    return <button className="tui-btn opacity-0" aria-hidden>[A]</button>;
  }

  // Icon based on current theme
  const icon = theme === 'system' ? 'A' : theme === 'dark' ? 'D' : 'L';
  const label = theme === 'system' ? 'Auto' : theme === 'dark' ? 'Dark' : 'Light';

  return (
    <button
      onClick={cycleTheme}
      className="tui-btn"
      title={`Theme: ${label} (click to cycle)`}
      aria-label={`Current theme: ${label}. Click to change.`}
    >
      [{icon}]
    </button>
  );
}
