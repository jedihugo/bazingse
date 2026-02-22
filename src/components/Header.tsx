'use client';

import Image from 'next/image';
import Link from 'next/link';
import ThemeToggle from './ThemeToggle';
import LanguagePicker from './LanguagePicker';
import { useT } from './LanguageProvider';
import { CALENDAR } from '@/lib/t';

export default function Header() {
  const { tCompact } = useT();

  return (
    <header className="tui-bg-panel border-b tui-border-color">
      <div className="max-w-7xl mx-auto px-1 py-1 sm:px-2 sm:py-2 md:px-3 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2 no-underline">
          <Image
            src="/bazingse-logo.png"
            alt="BaZingSe Logo"
            width={48}
            height={48}
            className="w-12 h-12 object-contain"
          />
          <h1 className="text-xl font-bold tui-text">
            BaZingSe
          </h1>
        </Link>
        <div className="flex items-center gap-2">
          <Link href="/calendar" className="tui-btn text-xs px-2 py-1 no-underline">
            {tCompact(CALENDAR.title)}
          </Link>
          <LanguagePicker />
          <ThemeToggle />
        </div>
      </div>
    </header>
  );
}
