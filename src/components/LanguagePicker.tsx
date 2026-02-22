'use client';

import { useT } from './LanguageProvider';
import type { LangMode } from '@/lib/t';

const MODES: LangMode[] = ['en', 'id', 'zh', 'en-zh'];

const MODE_LABEL: Record<LangMode, string> = {
  'en': 'EN',
  'id': 'ID',
  'zh': '中',
  'en-zh': 'E/中',
};

const MODE_TITLE: Record<LangMode, string> = {
  'en': 'English',
  'id': 'Bahasa Indonesia',
  'zh': '中文',
  'en-zh': 'English / 中文',
};

export default function LanguagePicker() {
  const { mode, setMode } = useT();

  const cycle = () => {
    const idx = MODES.indexOf(mode);
    setMode(MODES[(idx + 1) % MODES.length]);
  };

  return (
    <button
      onClick={cycle}
      className="tui-btn"
      title={`Language: ${MODE_TITLE[mode]} (click to cycle)`}
      aria-label={`Current language: ${MODE_TITLE[mode]}. Click to change.`}
    >
      [{MODE_LABEL[mode]}]
    </button>
  );
}
